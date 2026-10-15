"""Curator agent: turns a messy corpus into a status-aware knowledge bundle.

Pipeline (each step logged as evidence):
  1. self-markers   - docs that declare themselves deprecated
  2. decision links - decision records / notes that deprecate or promote other docs
                      (rule extractor + optional LLM extractor, results merged)
  3. resolution     - per topic, the non-deprecated doc with latest date is current
  4. composition    - rules about a concept scattered across other docs are attached
  5. emission       - concept pages (full, unchunked), index.md, graph.json

mode="date_only" is an ablation: only step 3 with dates, no evidence from steps 1-2.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

from .retrieval import load_docs

SELF_DEPRECATED = re.compile(
    r"this (?:page|document|doc|table) is (?:now )?(?:deprecated|obsolete|outdated|no longer (?:valid|used|maintained))", re.I)
OLD_WORDS = re.compile(r"replac|supersed|deprecat|no longer|must not|do not use|obsolete", re.I)
NEW_WORDS = re.compile(r"authoritative|now lives|is now|now reads|reads from|use instead|source of truth", re.I)
INTERNAL_WORDS = re.compile(r"internal to|ingestion only|not for reporting", re.I)
PATH_RE = re.compile(r"`?([\w\-/]+\.md)`?")
QUOTE_RE = re.compile(r"\"([^\"]{4,80})\"")
IDENT_RE = re.compile(r"`([a-z][a-z0-9_]+)`")

CURATOR_SYS = ("You are a documentation curator for an internal knowledge base. You read one decision record "
               "or meeting note and identify which OTHER documents it declares deprecated/replaced and which it "
               "declares authoritative/current. Respond only with JSON.")


class Curator:
    def __init__(self, llm=None, use_llm=True, mode="full"):
        self.llm, self.use_llm, self.mode = llm, use_llm and llm is not None and getattr(llm, "name", "") != "mock", mode
        self.tokens = 0

    # ---------- evidence extraction ----------
    def _rule_links(self, doc, by_title, by_ident):
        dep, new, internal = set(), set(), set()
        for sent in re.split(r"(?<=[.!?])\s+", doc["body"]):
            refs = set(PATH_RE.findall(sent))
            refs |= {by_title[t.lower()] for t in QUOTE_RE.findall(sent) if t.lower() in by_title}
            refs |= {by_ident[i] for i in IDENT_RE.findall(sent) if i in by_ident}
            refs.discard(doc["path"])
            if not refs:
                continue
            if INTERNAL_WORDS.search(sent):
                internal |= refs
            elif OLD_WORDS.search(sent):
                dep |= refs
            elif NEW_WORDS.search(sent):
                new |= refs
        return dep, new, internal

    def _llm_links(self, doc, catalog, valid):
        prompt = (f"Known documents (path - title):\n{catalog}\n\nDocument `{doc['path']}`:\n{doc['body'][:3000]}\n\n"
                  'Return JSON {"deprecates": [paths], "authoritative": [paths], "internal_only": [paths]} '
                  "using only paths from the known list. Use empty lists when the document says nothing about other documents.")
        try:
            r = self.llm.chat([{"role": "system", "content": CURATOR_SYS}, {"role": "user", "content": prompt}], json_mode=True)
            self.tokens += r["prompt_tokens"] + r["completion_tokens"]
            js = json.loads(r["content"] or "{}")
        except Exception:
            return set(), set(), set()
        pick = lambda k: {p for p in (js.get(k) or []) if isinstance(p, str) and p in valid and p != doc["path"]}
        return pick("deprecates"), pick("authoritative"), pick("internal_only")

    # ---------- main ----------
    def curate(self, raw_dir, out_dir, truth_file=None):
        docs = load_docs(raw_dir)
        by_path = {d["path"]: d for d in docs}
        by_title = {d["meta"].get("title", "").lower(): d["path"] for d in docs}
        by_ident = {}
        for d in docs:
            m = re.match(r"table ([a-z0-9_]+)", d["meta"].get("title", "").lower())
            if m:
                by_ident[m.group(1)] = d["path"]
        catalog = "\n".join(f"{d['path']} - {d['meta'].get('title', '')}" for d in docs if d["meta"]["kind"] != "ops")

        status = {d["path"]: {"status": "unknown", "superseded_by": [], "evidence": []} for d in docs}
        if self.mode == "full":
            for d in docs:
                if d["meta"]["kind"] not in ("decisions",) and SELF_DEPRECATED.search(d["body"]):
                    status[d["path"]]["status"] = "deprecated"
                    status[d["path"]]["evidence"].append("self-marker")
            for d in docs:
                if d["meta"]["kind"] not in ("decisions", "notes"):
                    continue
                dep, new, internal = self._rule_links(d, by_title, by_ident)
                if self.use_llm:
                    ld, ln, li = self._llm_links(d, catalog, by_path)
                    dep |= ld - new; new |= ln - dep; internal |= li
                for p in dep:
                    if p in status:
                        status[p]["status"] = "deprecated"
                        status[p]["evidence"].append(f"deprecated by {d['path']}")
                        status[p]["superseded_by"] += [x for x in new if x not in status[p]["superseded_by"]]
                for p in new:
                    if p in status and status[p]["status"] != "deprecated":
                        status[p]["status"] = "current"
                        status[p]["evidence"].append(f"declared authoritative by {d['path']}")
                for p in internal:
                    if p in status and status[p]["status"] == "unknown":
                        status[p]["status"] = "internal"
                        status[p]["evidence"].append(f"internal per {d['path']}")

        # ---------- resolution per topic ----------
        topics = defaultdict(list)
        for d in docs:
            if d["meta"].get("topic"):
                topics[d["meta"]["topic"]].append(d)
        for topic, group in topics.items():
            live = [d for d in group if status[d["path"]]["status"] not in ("deprecated", "internal")]
            if not live:
                continue
            if group[0]["meta"]["kind"] == "schemas" and any(status[d["path"]]["status"] == "current" for d in live):
                for d in live:
                    if status[d["path"]]["status"] == "unknown":
                        status[d["path"]]["status"] = "stale"
                        status[d["path"]]["evidence"].append("not the declared current table")
                continue
            live.sort(key=lambda d: d["meta"].get("updated", ""), reverse=True)
            winner = live[0]
            if status[winner["path"]]["status"] == "unknown":
                status[winner["path"]]["status"] = "current"
                status[winner["path"]]["evidence"].append("latest dated document in topic")
            for d in live[1:]:
                if status[d["path"]]["status"] == "unknown":
                    status[d["path"]]["status"] = "stale"
                    status[d["path"]]["superseded_by"].append(winner["path"])
                    status[d["path"]]["evidence"].append(f"older than {winner['path']}")
        for p, s in status.items():  # docs without topic and without evidence: treat as current
            if s["status"] == "unknown":
                s["status"] = "current"

        # ---------- emission ----------
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        concepts = {}
        for topic, group in topics.items():
            kind = group[0]["meta"]["kind"]
            if kind == "schemas":
                lines = []
                for d in sorted(group, key=lambda d: d["path"]):
                    s = status[d["path"]]
                    tname = d["meta"]["title"].replace("Table ", "")
                    cid = f"schemas/{tname}"
                    concepts[cid] = self._page(d, s, d["meta"]["title"], [], [])
                    lines.append(f"- `{tname}`: {s['status'].upper()} ({'; '.join(s['evidence']) or 'no evidence'}) -> read [{cid}]")
                concepts[f"schemas/{topic}"] = (f"# {topic.replace('-', ' ').title()} (which table to use)\n\n"
                                                "Status of each table in this family:\n\n" + "\n".join(lines) + "\n")
                continue
            cur = [d for d in group if status[d["path"]]["status"] == "current"] or group
            main = cur[0]
            hist = [d for d in group if d is not main]
            extra = self._composition(topic, main, docs, status)
            concepts[f"definitions/{topic}"] = self._page(main, status[main["path"]], main["meta"]["title"], extra, hist, status)

        for cid, text in concepts.items():
            p = out / f"{cid}.md"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        index = "\n".join(f"- [{cid}] {t.splitlines()[0].lstrip('# ').strip()}" for cid, t in sorted(concepts.items()))
        (out / "index.md").write_text(f"# Knowledge bundle (auto-curated by DecoyRE)\n\n{index}\n", encoding="utf-8")
        graph = {"docs": status, "concepts": sorted(concepts), "curator_tokens": self.tokens, "mode": self.mode}
        if truth_file and Path(truth_file).exists():
            graph["curation_accuracy"] = self.score(status, json.loads(Path(truth_file).read_text()))
        (out / "graph.json").write_text(json.dumps(graph, indent=1))
        return graph

    def _composition(self, topic, main, docs, status, max_lines=8):
        term = topic.replace("-", " ")
        pat = re.compile(rf"\b{re.escape(term)}s?\b", re.I)
        extra = []
        for d in docs:
            if d is main or d["meta"]["kind"] in ("ops", "schemas") or status[d["path"]]["status"] == "deprecated":
                continue
            if d["meta"].get("topic") == topic:
                continue
            for line in d["body"].splitlines():
                if line.lstrip().startswith("#"):
                    continue
                line = line.strip("-* ").strip()
                if len(line.split()) >= 6 and pat.search(line) and not PATH_RE.search(line):
                    extra.append((d["path"], line))
        return extra[:max_lines]

    @staticmethod
    def _page(doc, s, title, extra, hist, status=None):
        out = [f"# {title}", "", f"Status: {s['status'].upper()} | source: {doc['path']} | updated: {doc['meta'].get('updated', '?')}",
               f"Evidence: {'; '.join(s['evidence']) or 'none'}", "", doc["body"]]
        if extra:
            out += ["", "## Additional rules found in other documents", ""] + [f"- {t} (from {p})" for p, t in extra]
        if hist:
            out += ["", "## History (do not use)", ""]
            for h in hist:
                hs = status[h["path"]] if status else {"status": "?", "superseded_by": []}
                out.append(f"- {h['path']} is {hs['status'].upper()}"
                           + (f", superseded by {', '.join(hs['superseded_by'])}" if hs["superseded_by"] else ""))
        return "\n".join(out) + "\n"

    @staticmethod
    def score(status, truth):
        norm = {"internal": "staging", "stale": "deprecated"}
        rel = [p for p, t in truth.items() if t != "current" or p.startswith(("wiki/", "schemas/"))]
        ok = sum(norm.get(status[p]["status"], status[p]["status"]) == truth[p] for p in rel if p in status)
        bad = [p for p in rel if p in status and norm.get(status[p]["status"], status[p]["status"]) != truth[p]]
        return {"evaluated": len(rel), "correct": ok, "accuracy": round(ok / max(1, len(rel)), 3), "errors": bad}
