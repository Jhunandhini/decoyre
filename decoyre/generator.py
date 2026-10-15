"""Generates the DecoyRE benchmark: messy raw corpus + gold bundle + questions.

Decoys planted on purpose:
  deprecated  - the old metric page is phrased like the question; it is NOT marked
                deprecated in most seeds. The deprecation lives in a separate ADR.
                In some seeds the old page also has a *newer* edit date (typo fix),
                so "pick the latest file" heuristics fail.
  validity    - same pair of docs, question asks which version is in force.
  homonym     - four tables with near-identical names; the legacy one still claims
                to feed the monthly report.
  split_table - wide schema docs whose relevant column sits far from the table name,
                so fixed-size chunking separates them.
  composition - one definition spread over 4 docs of different types.
  absence     - no answer exists; near-miss docs tempt hallucination.
  long_tail   - answer only exists in a colloquial ticket.
"""
import json
import random
import shutil
from pathlib import Path

from .domains import DOMAINS

FILLER_COLS = [
    ("created_at", "timestamp", "Row creation time"), ("updated_at", "timestamp", "Last update time"),
    ("customer_id", "bigint", "FK to customers"), ("store_id", "int", "FK to stores"),
    ("region_code", "varchar", "Region"), ("currency", "char(3)", "ISO currency"),
    ("status", "varchar", "Lifecycle status"), ("source_system", "varchar", "Ingestion source"),
    ("batch_id", "bigint", "Load batch"), ("is_test", "boolean", "Test row flag"),
    ("external_ref", "varchar", "Reference in upstream system"), ("notes", "text", "Free text notes"),
    ("created_by", "varchar", "User or service that created the row"), ("version", "int", "Row version"),
    ("country", "char(2)", "Country code"), ("city", "varchar", "City name"),
    ("pincode", "varchar", "Postal code"), ("tax_amount", "decimal", "Tax amount"),
    ("net_amount", "decimal", "Amount before tax"), ("gross_amount", "decimal", "Amount after tax"),
    ("partner_id", "int", "Partner FK"), ("priority", "int", "Priority 1-5"),
    ("tags", "jsonb", "Arbitrary tags"), ("deleted_at", "timestamp", "Soft delete time"),
]


def _slug(s):
    import re
    return re.sub(r"-+", "-", "".join(c if c.isalnum() else "-" for c in s.lower())).strip("-")


def _doc(meta, body):
    fm = "\n".join(f"{k}: {v}" for k, v in meta.items())
    return f"---\n{fm}\n---\n\n{body.strip()}\n"


def _schema_table(cols):
    rows = "\n".join(f"| {c} | {t} | {d} |" for c, t, d in cols)
    return "| column | type | description |\n|---|---|---|\n" + rows


def _wide_cols(rng, special, n_filler=22):
    cols = rng.sample(FILLER_COLS, n_filler)
    pk = [("id", "bigint", "Primary key")]
    # special columns go into the last third so they land in a later chunk
    for c in special:
        cols.insert(rng.randint(int(len(cols) * 0.7), len(cols)), c)
    return pk + cols


class Builder:
    def __init__(self, spec, rng, p_marker=0.25, p_typo_newer=0.4, p_path_ref=0.7):
        self.s, self.rng = spec, rng
        self.p_marker, self.p_typo_newer, self.p_path_ref = p_marker, p_typo_newer, p_path_ref
        self.files, self.gold, self.questions = {}, {}, []
        self.adr_n = rng.randint(10, 20)
        self.truth = {}  # path -> status, for analysis

    def add(self, path, meta, body, status="current"):
        self.files[path] = _doc(meta, body)
        self.truth[path] = status

    def q(self, category, phrasings, required, decoys=(), abstain=False, gold=""):
        for i, text in enumerate(phrasings):
            self.questions.append({
                "id": f"{self.s['name']}-{category}-{len([x for x in self.questions if x['category'] == category]) + 1:02d}",
                "domain": self.s["name"], "category": category, "question": text,
                "required": required, "decoys": list(decoys), "abstain": abstain,
                "gold_answer": gold, "paraphrase": i})

    def next_adr(self):
        self.adr_n += 1
        return self.adr_n

    # ---------- metrics: deprecated + validity ----------
    def metrics(self):
        for m in self.s["metrics"]:
            r = self.rng
            old_path = f"wiki/{_slug(m['old_title'])}.md"
            new_path = f"wiki/finance/{_slug(m['new_title'])}.md"
            n = self.next_adr()
            adr_path = f"decisions/adr-{n:03d}-{m['topic']}.md"
            old_date = f"2023-{r.randint(1, 12):02d}-{r.randint(1, 28):02d}"
            new_date = f"2025-{r.randint(1, 6):02d}-{r.randint(1, 28):02d}"
            typo = r.random() < self.p_typo_newer
            old_updated = f"2025-{r.randint(8, 12):02d}-{r.randint(1, 28):02d}" if typo else old_date
            marker = r.random() < self.p_marker
            body = (f"# {m['old_title']}\n\nThis page explains how we calculate {m['name']} at {self.s['company']}.\n\n"
                    f"## Formula\n\n`{m['old_formula']}`\n\n{m['old_explain']}\n\n"
                    f"## Where it is used\n\nWeekly business review and the leadership dashboard.\n")
            if marker:
                body = f"> Note: this page is deprecated, see {new_path}.\n\n" + body
            if typo:
                body += f"\n## Changelog\n\n- {old_updated}: fixed a typo in the heading.\n"
            self.add(old_path, {"title": m["old_title"], "topic": m["topic"], "updated": old_updated,
                                "owner": "analytics"}, body, status="deprecated")
            self.add(new_path, {"title": m["new_title"], "topic": m["topic"], "updated": new_date,
                                "owner": "finance"},
                     f"# {m['new_title']}\n\nOwner: finance analytics.\n\n`{m['new_formula']}`\n\n{m['new_explain']}\n")
            style = r.random()
            if style < 0.4:      # explicit paths: rule extractor handles it
                ref = (f"This decision replaces the definition in `{old_path}`. "
                       f"The authoritative definition is now `{new_path}`.")
            elif style < 0.7:    # explicit titles
                ref = (f"This decision replaces the old \"{m['old_title']}\" wiki page. "
                       f"The authoritative definition now lives in the page \"{m['new_title']}\".")
            else:                # implicit wording: needs reading comprehension
                ref = (f"From this quarter on, everyone should follow the finance team's page \"{m['new_title']}\". "
                       f"Please ignore the 2023 analytics write-up \"{m['old_title']}\" when building reports.")
            self.add(adr_path, {"title": f"ADR-{n:03d}: change of {m['name']} definition", "updated": new_date,
                                "owner": "data-council"},
                     f"# ADR-{n:03d}: change of {m['name']} definition\n\nStatus: Accepted\n\n## Context\n\n{m['reason']}\n\n"
                     f"## Decision\n\n{ref}\n")
            gold = f"{m['new_formula']}. {m['new_explain']}"
            self.gold[f"metrics/{m['topic']}"] = (
                f"# {m['name'].capitalize()}\n\nStatus: current (since {new_date}, {adr_path})\n\n"
                f"`{m['new_formula']}`\n\n{m['new_explain']}\n\nThe 2023 definition in {old_path} is deprecated.\n")
            self.q("deprecated", [m["questions"][0]], m["required"], m["decoys"], gold=gold)
            self.q("validity", [m["questions"][1]], m["required"], m["decoys"], gold=gold)

    # ---------- composition ----------
    def composites(self):
        for c in self.s["composites"]:
            base_path = f"wiki/{_slug(c['title'])}.md"
            self.add(base_path, {"title": c["title"], "topic": c["topic"], "updated": "2025-02-10", "owner": "product"},
                     f"# {c['title']}\n\n{c['base']}\n\nSee related decisions for exceptions.\n")
            rules = [c["base"]]
            for kind, title, text in c["parts"]:
                if kind == "decisions":
                    n = self.next_adr()
                    path, title = f"decisions/adr-{n:03d}-{_slug(title)}.md", f"ADR-{n:03d}: {title}"
                    body = f"# {title}\n\nStatus: Accepted\n\n## Decision\n\n{text}\n"
                else:
                    path = f"{kind}/{_slug(title)}.md"
                    body = f"# {title}\n\nAttendees: ops, finance, product.\n\n- Misc updates on the roadmap.\n- {text}\n- Next sync in two weeks.\n"
                self.add(path, {"title": title, "updated": "2025-04-02", "owner": kind}, body)
                rules.append(text)
            self.gold[f"definitions/{c['topic']}"] = f"# {c['title']}\n\nStatus: current\n\n" + "\n".join(f"- {x}" for x in rules) + "\n"
            self.q("composition", c["questions"], c["required"], gold=" ".join(rules))

    # ---------- tables: homonym + split ----------
    def tables(self):
        t, r = self.s["tables"], self.rng
        cur_cols = _wide_cols(r, t["current_cols"])
        leg_cols = _wide_cols(r, t["legacy_cols"])
        variants = [
            (t["old"], f"Original {t['entity']} table from 2021. Raw rows, no cleaning.", _wide_cols(r, [], 10), "deprecated"),
            (t["staging"], "Intermediate staging table loaded hourly by the ingestion job. Not for reporting.", _wide_cols(r, [], 12), "staging"),
            (t["legacy"], f"This is the table we use for the {t['report']}.", leg_cols, "deprecated"),
            (t["current"], f"Cleaned {t['entity']} table, one row per {t['entity'][:-1]}. Deduplicated.", cur_cols, "current"),
        ]
        for name, desc, cols, status in variants:
            self.add(f"schemas/{name}.md", {"title": f"Table {name}", "topic": t["topic"], "updated": "2024-11-05" if status != "current" else "2025-01-20",
                                            "owner": "data-eng"},
                     f"# Table {name}\n\n{desc}\n\n## Columns\n\n{_schema_table(cols)}\n", status=status)
        n = self.next_adr()
        self.add(f"decisions/adr-{n:03d}-{t['current'].replace('_', '-')}.md",
                 {"title": f"ADR-{n:03d}: {t['report']} source", "updated": "2025-01-25", "owner": "data-council"},
                 f"# ADR-{n:03d}: {t['report']} source\n\nStatus: Accepted\n\n## Decision\n\n"
                 f"The {t['report']} now reads from `{t['current']}`. `{t['legacy']}` is deprecated and must no longer be used. "
                 f"`{t['staging']}` is internal to ingestion.\n")
        self.gold[f"schemas/{t['current']}"] = (
            f"# Table {t['current']} (current)\n\nAuthoritative {t['entity']} table; source of the {t['report']}. "
            f"Do not use {t['legacy']} (deprecated), {t['old']} (deprecated) or {t['staging']} (ingestion only).\n\n"
            f"## Columns\n\n{_schema_table(cur_cols)}\n")
        for item in t["questions"]:
            self.q(item["category"], item["q"], item["required"], item["decoys"], gold=", ".join(g[0] for g in item["required"]))

    # ---------- absence ----------
    def absent(self):
        for a in self.s["absent"]:
            kind, title, text = a["near_miss"]
            self.add(f"{kind}/{_slug(title)}.md", {"title": title, "updated": "2025-05-12", "owner": kind},
                     f"# {title}\n\n- {text}\n- Other items: hiring, offsite logistics.\n")
            self.q("absence", a["q"], [], abstain=True, gold="Not documented.")

    # ---------- long tail ----------
    def incidents(self):
        for inc in self.s["incidents"]:
            self.add(f"ops/tickets/{inc['id']}.md", {"title": inc["id"], "updated": "2025", "owner": "support"},
                     f"# {inc['id']}\n\n{inc['text']}\n")
            self.q("long_tail", inc["q"], inc["required"], gold=inc["text"])
        for tid, text in self.s["distractor_tickets"]:
            self.add(f"ops/tickets/{tid}.md", {"title": tid, "updated": "2025", "owner": "support"}, f"# {tid}\n\n{text}\n")

    def noise(self):
        c = self.s["company"]
        self.add("wiki/onboarding.md", {"title": "Onboarding for analysts", "updated": "2024-03-01", "owner": "analytics"},
                 f"# Onboarding\n\nWelcome to {c}. Request warehouse access in the IT portal. Dashboards live in the BI tool. "
                 "Ask in #data-help before creating new tables.\n")
        self.add("notes/all-hands-2025-q1.md", {"title": "All hands Q1", "updated": "2025-03-30", "owner": "ceo-office"},
                 f"# All hands Q1\n\n- {c} grew in all regions.\n- New office opening.\n- Data council will publish ADRs for metric changes.\n")

    def build(self):
        self.metrics(); self.composites(); self.tables(); self.absent(); self.incidents(); self.noise()
        index = "\n".join(f"- [{cid}] {body.splitlines()[0].lstrip('# ').strip()}" for cid, body in sorted(self.gold.items()))
        self.gold["index"] = f"# {self.s['company']} knowledge bundle (hand-curated)\n\n{index}\n"
        return self


def generate(out_dir="data", seed=7, domains=None, variants=1, **kw):
    """variants>1 builds several independently randomised corpora per domain (retail-v1, retail-v2, ...)."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    all_q = []
    jobs = [(d, d if variants == 1 else f"{d}-v{i + 1}") for d in (domains or DOMAINS) for i in range(variants)]
    for base, name in jobs:
        rng = random.Random(f"{seed}-{name}")
        spec = dict(DOMAINS[base], name=name)
        b = Builder(spec, rng, **kw).build()
        root = out / name
        if root.exists():
            shutil.rmtree(root)
        for rel, text in b.files.items():
            p = root / "raw" / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        for cid, text in b.gold.items():
            p = root / "gold_bundle" / f"{cid}.md"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        (root / "truth.json").write_text(json.dumps(b.truth, indent=1))
        (root / "meta.json").write_text(json.dumps({"company": spec["company"], "seed": seed, "base": base}))
        all_q += b.questions
        print(f"[generate] {name}: {len(b.files)} raw docs, {len(b.gold) - 1} gold concepts, {len(b.questions)} questions")
    with open(out / "questions.jsonl", "w") as f:
        for q in all_q:
            f.write(json.dumps(q) + "\n")
    print(f"[generate] total questions: {len(all_q)} -> {out / 'questions.jsonl'}")
    return all_q
