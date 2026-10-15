"""Tools, the tool-calling agent loop, Router and Verifier agents, and every compared system."""
import json
import re
import time
from pathlib import Path

from .textutil import citations, identifiers, is_abstention, tokenize

ANSWER_RULES = (
    "You answer questions about {company}'s internal data documentation. Use ONLY information returned by your "
    "tools or given in the context. Cite every source you rely on in square brackets with its path, e.g. "
    "[wiki/finance/revenue.md]. If the information is not in the sources, start your reply with \"I don't know\". "
    "Prefer documents marked CURRENT; never base the answer on DEPRECATED or STALE documents. "
    "Answer directly and concisely; do not describe outdated versions.")


# ============================== knowledge bundle ==============================
class Bundle:
    def __init__(self, bundle_dir):
        self.dir = Path(bundle_dir)
        self.concepts = {p.relative_to(self.dir).as_posix()[:-3]: p.read_text(encoding="utf-8")
                         for p in self.dir.rglob("*.md") if p.name != "index.md"}
        self.index_text = (self.dir / "index.md").read_text(encoding="utf-8")
        g = self.dir / "graph.json"
        self.graph = json.loads(g.read_text()) if g.exists() else None

    def read(self, cid):
        cid = (cid or "").strip().strip("[]").removesuffix(".md").removeprefix("bundle/")
        if cid in self.concepts:
            return f"[bundle/{cid}.md]\n{self.concepts[cid]}"
        q = set(tokenize(cid.replace("/", " ").replace("-", " ")))
        best = max(self.concepts, key=lambda c: len(q & set(tokenize(c.replace("/", " ").replace("-", " ")))), default=None)
        if best and q & set(tokenize(best.replace("/", " ").replace("-", " "))):
            return f"[bundle/{best}.md] (closest match for '{cid}')\n{self.concepts[best]}"
        return f"Concept '{cid}' not found. Available: {', '.join(sorted(self.concepts))}"

    def doc_status(self, path):
        if not self.graph:
            return None
        return self.graph["docs"].get(path)


def tool_schema(name, desc, param, pdesc):
    return {"type": "function", "function": {"name": name, "description": desc, "parameters": {
        "type": "object", "properties": {param: {"type": "string", "description": pdesc}}, "required": [param]}}}


READ_SCHEMA = tool_schema("read_concept", "Read one curated concept page from the knowledge bundle (complete, unchunked). "
                          "Use the ids shown in the bundle index, e.g. 'definitions/revenue'.", "concept_id", "Concept id from the index")
SEARCH_SCHEMA = tool_schema("search_docs", "Search the raw document corpus (wiki, schemas, decision records, meeting notes, "
                            "support tickets). Best for incidents, tickets and specific past events.", "query", "Search query")


def make_search(index, bundle=None, status_aware=False, k=5):
    def search(query):
        hits = index.hybrid(query, k=k * 2 if status_aware else k)
        if status_aware and bundle and bundle.graph:
            def rank(h):
                s = (bundle.doc_status(h["source"]) or {}).get("status", "current")
                return 1 if s in ("deprecated", "stale", "internal") else 0
            hits = sorted(hits, key=rank)[:k]
        blocks = []
        for h in hits:
            hdr = f"[{h['source']}"
            if status_aware and bundle and bundle.graph:
                st = bundle.doc_status(h["source"]) or {}
                hdr += f" | status: {st.get('status', 'unknown').upper()}"
                if st.get("superseded_by"):
                    hdr += f" | superseded by: {', '.join(st['superseded_by'])}"
            blocks.append(hdr + "]\n" + h["text"][:700])
        return "\n\n---\n\n".join(blocks) if blocks else "No results."
    return search


# ============================== agent loop ==============================
def run_agent(llm, system, user, tools, max_steps=6):
    """tools: dict name -> (schema, fn). Returns answer + full trace + cost counters."""
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    schemas = [s for s, _ in tools.values()]
    trace, pt, ct, calls = [], 0, 0, 0
    for _ in range(max_steps):
        r = llm.chat(msgs, tools=schemas or None)
        calls += 1
        pt += r["prompt_tokens"]; ct += r["completion_tokens"]
        if not r["tool_calls"]:
            return {"answer": r["content"], "trace": trace, "prompt_tokens": pt, "completion_tokens": ct, "llm_calls": calls}
        msgs.append({"role": "assistant", "content": r["content"], "tool_calls": r["tool_calls"]})
        for tc in r["tool_calls"]:
            fn = tools.get(tc["name"], (None, None))[1]
            arg = next(iter(tc["args"].values()), "") if tc["args"] else ""
            out = fn(arg) if fn else f"Unknown tool {tc['name']}. Available: {', '.join(tools)}"
            trace.append({"tool": tc["name"], "arg": arg, "output": out})
            msgs.append({"role": "tool", "tool_call_id": tc["id"], "name": tc["name"], "content": out})
    msgs.append({"role": "user", "content": "Step limit reached. Give your final answer now using what you have."})
    r = llm.chat(msgs)
    return {"answer": r["content"], "trace": trace, "prompt_tokens": pt + r["prompt_tokens"],
            "completion_tokens": ct + r["completion_tokens"], "llm_calls": calls + 1}


# ============================== router agent ==============================
INTENTS = ["definition", "table_choice", "schema", "incident", "policy", "other"]
ROUTER_SYS = ("You route questions about a company's internal documentation. Classify the question intent as one of: "
              "definition (how a metric or business rule is defined/calculated), table_choice (which table/source to use), "
              "schema (columns/fields of a table), incident (something that happened: outages, bugs, tickets, a specific month), "
              "policy (a company policy or rule that may or may not be documented), other. "
              'Respond only with JSON: {"intent": "...", "reason": "..."}')
KEYWORDS = [
    ("incident", r"\b(incident|ticket|outage|happened|went wrong|caused|cause|failed|fail|issue|delays?|duplicat\w*|double|"
                 r"slowdown|january|february|march|april|may|june|july|august|september|october|november|december)\b"),
    ("schema", r"\b(column|field|stored|store|stores|holds|record)\b"),
    ("table_choice", r"\b(which table|source table|query for|table should)\b"),
    ("definition", r"\b(calculate|definition|defin|formula|count|rules?|valid|compute|computing|condition)\b"),
    ("policy", r"\b(policy|allowed|limit|schedule|leave|discount|how often)\b"),
]


class Router:
    def __init__(self, llm, use_llm=True):
        self.llm, self.use_llm = llm, use_llm

    def fallback(self, q):
        for intent, pat in KEYWORDS:
            if re.search(pat, q, re.I):
                return intent
        return "other"

    def route(self, q):
        cost = 0
        intent, how = None, "keywords"
        if self.use_llm:
            try:
                r = self.llm.chat([{"role": "system", "content": ROUTER_SYS}, {"role": "user", "content": q}], json_mode=True)
                cost = r["prompt_tokens"] + r["completion_tokens"]
                intent = json.loads(r["content"] or "{}").get("intent")
                how = "llm"
            except Exception:
                intent = None
        if intent not in INTENTS:
            intent, how = self.fallback(q), "keywords"
        return intent, how, cost


PLANS = {  # intent -> (tools exposed first, hint)
    "definition": (["read_concept"], "Read the matching concept page; it already merges rules from all sources."),
    "table_choice": (["read_concept"], "Read the table-family concept to see which table is CURRENT."),
    "schema": (["read_concept"], "Read the family concept, then the CURRENT table's concept page for its full column list."),
    "incident": (["search_docs"], "Incidents live in support tickets; search for them."),
    "policy": (["read_concept"], "Check the index; if no concept covers this policy, say you don't know."),
    "other": (["read_concept", "search_docs"], "Use whichever tool fits."),
}


# ============================== verifier agent ==============================
class Verifier:
    """Deterministic checks over the answer and the evidence the agent actually saw."""

    def __init__(self, bundle):
        self.bundle = bundle

    def check(self, question, intent, result):
        problems = []
        answer, evidence = result["answer"], "\n".join(t["output"] for t in result["trace"])
        used = {t["tool"] for t in result["trace"]}
        if is_abstention(answer):
            if intent != "policy" and "search_docs" not in used:
                problems.append("You said you don't know without searching the raw corpus. Use search_docs before giving up.")
            return problems
        if not result["trace"]:
            problems.append("You answered without consulting any tool. Look the answer up first.")
        for c in citations(answer):
            st = self.bundle.doc_status(c) if self.bundle else None
            if st and st["status"] in ("deprecated", "stale"):
                rep = ", ".join(st["superseded_by"]) or "the CURRENT document"
                problems.append(f"You cited {c}, which is {st['status'].upper()} (superseded by {rep}). Answer from the current source.")
        ungrounded = identifiers(answer) - identifiers(evidence) - identifiers(question)
        if ungrounded:
            problems.append(f"These terms do not appear in any source you retrieved: {', '.join(sorted(ungrounded))}. "
                            "Remove them or find evidence.")
        return problems


# ============================== systems ==============================
class System:
    name = "base"

    def __init__(self, llm, company):
        self.llm, self.company = llm, company
        self.sys_prompt = ANSWER_RULES.format(company=company)

    def answer(self, q):
        t0 = time.time()
        r = self._answer(q)
        r["latency_s"] = round(time.time() - t0, 3)
        r["tool_calls"] = len(r.get("trace", []))
        r.setdefault("meta", {})
        return r


class RAG(System):
    def __init__(self, llm, company, index, mode="dense", k=5):
        super().__init__(llm, company)
        self.index, self.mode, self.k = index, mode, k
        self.name = f"rag_{mode}"

    def _answer(self, q):
        hits = self.index.dense(q, self.k) if self.mode == "dense" else self.index.hybrid(q, self.k)
        ctx = "\n\n---\n\n".join(f"[{h['source']}]\n{h['text']}" for h in hits)
        r = self.llm.chat([{"role": "system", "content": self.sys_prompt},
                           {"role": "user", "content": f"CONTEXT:\n{ctx}\n\nQUESTION: {q}"}])
        return {"answer": r["content"], "trace": [], "prompt_tokens": r["prompt_tokens"],
                "completion_tokens": r["completion_tokens"], "llm_calls": 1,
                "meta": {"retrieved": [h["source"] for h in hits]}}


class Agentic(System):
    """Generic tool agent: agentic RAG (search only), OKF (bundle only), OKF+RAG (both)."""

    def __init__(self, llm, company, name, bundle=None, index=None, use_bundle=True, use_search=True):
        super().__init__(llm, company)
        self.name, self.bundle = name, bundle
        self.tools = {}
        if use_bundle and bundle:
            self.tools["read_concept"] = (READ_SCHEMA, bundle.read)
        if use_search and index:
            self.tools["search_docs"] = (SEARCH_SCHEMA, make_search(index))

    def _answer(self, q):
        user = (f"BUNDLE INDEX:\n{self.bundle.index_text}\n\n" if "read_concept" in self.tools else "") + f"QUESTION: {q}"
        return run_agent(self.llm, self.sys_prompt, user, self.tools)


class DecoyRE(System):
    """Router -> Answerer (curated bundle + status-aware search) -> Verifier -> one revision."""

    def __init__(self, llm, company, bundle, index, router=True, verifier=True, status_aware=True,
                 router_llm=True, name="decoyre"):
        super().__init__(llm, company)
        self.name, self.bundle = name, bundle
        self.router = Router(llm, use_llm=router_llm) if router else None
        self.verifier = Verifier(bundle) if verifier else None
        self.all_tools = {"read_concept": (READ_SCHEMA, bundle.read),
                          "search_docs": (SEARCH_SCHEMA, make_search(index, bundle, status_aware=status_aware))}

    def _run(self, q, tool_names, hint, feedback=None):
        tools = {n: self.all_tools[n] for n in tool_names}
        user = ""
        if "read_concept" in tools:
            user += f"BUNDLE INDEX:\n{self.bundle.index_text}\n\n"
        if hint:
            user += f"ROUTER HINT: {hint}\n\n"
        if feedback:
            user += "VERIFIER FEEDBACK on your previous answer (fix these):\n- " + "\n- ".join(feedback) + "\n\n"
        return run_agent(self.llm, self.sys_prompt, user + f"QUESTION: {q}", tools)

    def _answer(self, q):
        meta, extra_tokens = {}, 0
        if self.router:
            intent, how, cost = self.router.route(q)
            extra_tokens += cost
            names, hint = PLANS[intent]
            meta.update(intent=intent, routed_by=how)
        else:
            intent, names, hint = "other", list(self.all_tools), None
        r = self._run(q, names, hint)
        meta["verifier"] = []
        if self.verifier:
            problems = self.verifier.check(q, intent, r)
            meta["verifier"].append(problems)
            if problems:
                r2 = self._run(q, list(self.all_tools), hint, feedback=problems)
                for key in ("prompt_tokens", "completion_tokens", "llm_calls"):
                    r2[key] += r[key]
                r2["trace"] = r["trace"] + r2["trace"]
                r2["first_answer"] = r["answer"]
                meta["verifier"].append(self.verifier.check(q, intent, r2))
                r = r2
        r["prompt_tokens"] += extra_tokens
        r["meta"] = meta
        return r
