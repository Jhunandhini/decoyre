import csv
import json
import math
import random
import re
import time
from collections import defaultdict
from pathlib import Path

from .agents import RAG, Agentic, Bundle, DecoyRE
from .curator import Curator
from .retrieval import CorpusIndex, load_docs
from .textutil import is_abstention

CORE = ["rag_dense", "rag_hybrid", "agent_search", "okf_rag_gold", "decoyre"]
ALL = CORE + ["okf_gold", "decoyre_no_verifier", "decoyre_no_router", "decoyre_no_status", "decoyre_date_only"]
CATS = ["deprecated", "validity", "homonym", "split_table", "composition", "absence", "long_tail"]


# ============================== scoring ==============================
def _has(ans, alt):
    alt = alt.lower()
    if re.fullmatch(r"[\d.,]+", alt):          # numbers: 60 must not match 600
        return re.search(rf"(?<![\d.,]){re.escape(alt)}(?![\d])", ans) is not None
    return alt in ans


def score(q, answer):
    a = (answer or "").lower()
    abst = is_abstention(answer or "")
    if q["abstain"]:
        return {"correct": abst, "lenient": abst, "decoy": False, "abstained": abst, "hallucinated": not abst}
    req = all(any(_has(a, alt) for alt in g) for g in q["required"])
    decoy = any(d.lower() in a for d in q["decoys"])
    return {"correct": req and not decoy and not abst, "lenient": req, "decoy": decoy,
            "abstained": abst, "hallucinated": False}


# ============================== building ==============================
class Domain:
    def __init__(self, root, llm, recurate=False, curator_llm=True):
        self.root = Path(root)
        self.company = json.loads((self.root / "meta.json").read_text())["company"]
        self.docs = load_docs(self.root / "raw")
        self.index = CorpusIndex(self.docs, llm, self.root / "cache")
        self.gold = Bundle(self.root / "gold_bundle")
        self.curated = {}
        for mode in ("full", "date_only"):
            out = self.root / f"curated_{mode}"
            if recurate or not (out / "graph.json").exists():
                g = Curator(llm, use_llm=curator_llm, mode=mode).curate(self.root / "raw", out, self.root / "truth.json")
                print(f"[curate] {self.root.name}/{mode}: accuracy {g.get('curation_accuracy', {}).get('accuracy')}")
            self.curated[mode] = Bundle(out)

    def system(self, name, llm):
        c, ix = self.company, self.index
        full = self.curated["full"]
        table = {
            "rag_dense": lambda: RAG(llm, c, ix, "dense"),
            "rag_hybrid": lambda: RAG(llm, c, ix, "hybrid"),
            "agent_search": lambda: Agentic(llm, c, "agent_search", index=ix, use_bundle=False),
            "okf_gold": lambda: Agentic(llm, c, "okf_gold", bundle=self.gold, use_search=False),
            "okf_rag_gold": lambda: Agentic(llm, c, "okf_rag_gold", bundle=self.gold, index=ix),
            "decoyre": lambda: DecoyRE(llm, c, full, ix),
            "decoyre_no_verifier": lambda: DecoyRE(llm, c, full, ix, verifier=False, name="decoyre_no_verifier"),
            "decoyre_no_router": lambda: DecoyRE(llm, c, full, ix, router=False, name="decoyre_no_router"),
            "decoyre_no_status": lambda: DecoyRE(llm, c, full, ix, status_aware=False, name="decoyre_no_status"),
            "decoyre_date_only": lambda: DecoyRE(llm, c, self.curated["date_only"], ix, name="decoyre_date_only"),
        }
        return table[name]()


# ============================== running ==============================
def run(data_dir, llm, systems, domains=None, limit=None, out_dir="results/run", recurate=False, curator_llm=True):
    data, out = Path(data_dir), Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    qs = [json.loads(l) for l in open(data / "questions.jsonl")]
    domains = domains or sorted({q["domain"] for q in qs})
    rows_file = out / "rows.jsonl"
    done = set()
    if rows_file.exists():
        for l in open(rows_file):
            r = json.loads(l)
            done.add((r["system"], r["id"]))
    curation = {}
    with open(rows_file, "a") as f:
        for dname in domains:
            dom = Domain(data / dname, llm, recurate=recurate, curator_llm=curator_llm)
            curation[dname] = {m: b.graph.get("curation_accuracy") for m, b in dom.curated.items()}
            dq = [q for q in qs if q["domain"] == dname][:limit]
            for sname in systems:
                sysm = dom.system(sname, llm)
                todo = [q for q in dq if (sname, q["id"]) not in done]
                for i, q in enumerate(todo, 1):
                    t0 = time.time()
                    try:
                        r = sysm.answer(q["question"])
                    except Exception as e:
                        r = {"answer": f"[error: {e}]", "trace": [], "prompt_tokens": 0, "completion_tokens": 0,
                             "llm_calls": 0, "tool_calls": 0, "latency_s": time.time() - t0, "meta": {"error": str(e)}}
                    s = score(q, r["answer"])
                    row = {"system": sname, "id": q["id"], "domain": dname, "category": q["category"],
                           "question": q["question"], "answer": r["answer"], **s,
                           "prompt_tokens": r["prompt_tokens"], "completion_tokens": r["completion_tokens"],
                           "llm_calls": r["llm_calls"], "tool_calls": r["tool_calls"], "latency_s": r["latency_s"],
                           "meta": r.get("meta", {}),
                           "trace": [{"tool": t["tool"], "arg": t["arg"]} for t in r.get("trace", [])]}
                    f.write(json.dumps(row) + "\n"); f.flush()
                    print(f"[{dname}|{sname}] {i}/{len(todo)} {q['id']:<28} {'OK ' if s['correct'] else 'BAD'} "
                          f"{r['prompt_tokens']:>6} tok {r['latency_s']:.1f}s")
    (out / "curation.json").write_text(json.dumps(curation, indent=1))
    return report(out)


# ============================== statistics ==============================
def bootstrap_ci(vals, n=2000, seed=0):
    if not vals:
        return (0, 0)
    rng = random.Random(seed)
    means = sorted(sum(rng.choice(vals) for _ in vals) / len(vals) for _ in range(n))
    return means[int(0.025 * n)], means[int(0.975 * n)]


def mcnemar_exact(a, b):
    """Two-sided exact McNemar test on paired correctness vectors."""
    n01 = sum(1 for x, y in zip(a, b) if not x and y)
    n10 = sum(1 for x, y in zip(a, b) if x and not y)
    n = n01 + n10
    if n == 0:
        return n01, n10, 1.0
    k = min(n01, n10)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return n01, n10, min(1.0, 2 * p)


def report(out_dir):
    out = Path(out_dir)
    rows = [json.loads(l) for l in open(out / "rows.jsonl")]
    by_sys = defaultdict(list)
    for r in rows:
        by_sys[r["system"]].append(r)
    order = [s for s in ALL if s in by_sys] + [s for s in by_sys if s not in ALL]
    mean = lambda xs: sum(xs) / max(1, len(xs))
    summary = []
    for s in order:
        rs = by_sys[s]
        ans = [r for r in rs if r["category"] != "absence"]
        absn = [r for r in rs if r["category"] == "absence"]
        acc = [1 if r["correct"] else 0 for r in rs]
        lo, hi = bootstrap_ci(acc)
        summary.append({
            "system": s, "n": len(rs), "accuracy": mean(acc), "ci_low": lo, "ci_high": hi,
            "lenient_accuracy": mean([r["lenient"] for r in rs]),
            "decoy_rate": mean([r["decoy"] for r in ans]),
            "correct_abstention": mean([r["abstained"] for r in absn]) if absn else float("nan"),
            "false_abstention": mean([r["abstained"] for r in ans]),
            "prompt_tokens": mean([r["prompt_tokens"] for r in rs]),
            "llm_calls": mean([r["llm_calls"] for r in rs]),
            "tool_calls": mean([r["tool_calls"] for r in rs]),
            "latency_s": mean([r["latency_s"] for r in rs]),
        })
    cats = defaultdict(dict)
    for s in order:
        for c in CATS:
            rs = [r for r in by_sys[s] if r["category"] == c]
            if rs:
                cats[s][c] = mean([r["correct"] for r in rs])
    # significance: DecoyRE vs each other system on the same questions
    sig = []
    if "decoyre" in by_sys:
        ref = {r["id"]: r["correct"] for r in by_sys["decoyre"]}
        for s in order:
            if s == "decoyre":
                continue
            other = {r["id"]: r["correct"] for r in by_sys[s]}
            ids = sorted(set(ref) & set(other))
            n01, n10, p = mcnemar_exact([other[i] for i in ids], [ref[i] for i in ids])
            sig.append({"baseline": s, "n": len(ids), "decoyre_only_correct": n01, "baseline_only_correct": n10, "p_value": p})

    with open(out / "summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0]))
        w.writeheader(); w.writerows(summary)
    with open(out / "per_category.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["system"] + CATS)
        for s in order:
            w.writerow([s] + [f"{cats[s].get(c, float('nan')):.3f}" for c in CATS])
    pct = lambda x: "-" if x != x else f"{100 * x:.1f}"
    md = ["# DecoyRE results", "", "## Overall", "",
          "| System | N | Acc % (95% CI) | Lenient % | Decoy % | Abstain-correct % | False-abstain % | Prompt tok | LLM calls | Tool calls | Latency s |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in summary:
        md.append(f"| {r['system']} | {r['n']} | {pct(r['accuracy'])} ({pct(r['ci_low'])}-{pct(r['ci_high'])}) | {pct(r['lenient_accuracy'])} | "
                  f"{pct(r['decoy_rate'])} | {pct(r['correct_abstention'])} | {pct(r['false_abstention'])} | {r['prompt_tokens']:.0f} | "
                  f"{r['llm_calls']:.2f} | {r['tool_calls']:.2f} | {r['latency_s']:.2f} |")
    md += ["", "## Accuracy by failure category (%)", "", "| System | " + " | ".join(CATS) + " |", "|---" * (len(CATS) + 1) + "|"]
    for s in order:
        md.append(f"| {s} | " + " | ".join(pct(cats[s].get(c, float('nan'))) for c in CATS) + " |")
    if sig:
        md += ["", "## Paired exact McNemar test (DecoyRE vs baseline)", "",
               "| Baseline | N | Only DecoyRE correct | Only baseline correct | p |", "|---|---|---|---|---|"]
        md += [f"| {x['baseline']} | {x['n']} | {x['decoyre_only_correct']} | {x['baseline_only_correct']} | {x['p_value']:.4f} |" for x in sig]
    cur = out / "curation.json"
    if cur.exists():
        md += ["", "## Curation accuracy (document status vs ground truth)", "", "| Domain | Full curator | Date-only ablation |", "|---|---|---|"]
        for d, m in json.loads(cur.read_text()).items():
            md.append(f"| {d} | {(m.get('full') or {}).get('accuracy')} | {(m.get('date_only') or {}).get('accuracy')} |")
    (out / "summary.md").write_text("\n".join(md) + "\n")
    _figures(out, summary, cats, order)
    print("\n".join(md))
    return summary


def _figures(out, summary, cats, order):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, ax = plt.subplots(figsize=(7, 3.6))
    names = [r["system"] for r in summary]
    acc = [100 * r["accuracy"] for r in summary]
    err = [[100 * (r["accuracy"] - r["ci_low"]) for r in summary], [100 * (r["ci_high"] - r["accuracy"]) for r in summary]]
    ax.bar(names, acc, yerr=err, capsize=3, color=["#c44" if n.startswith("decoyre") else "#888" for n in names])
    ax.set_ylabel("Strict accuracy (%)"); ax.set_ylim(0, 100)
    plt.xticks(rotation=35, ha="right", fontsize=8); plt.tight_layout()
    fig.savefig(out / "fig_accuracy.png", dpi=200); plt.close(fig)

    import numpy as np
    m = np.array([[100 * cats[s].get(c, np.nan) for c in CATS] for s in order])
    fig, ax = plt.subplots(figsize=(7.5, 0.45 * len(order) + 1.2))
    im = ax.imshow(m, cmap="RdYlGn", vmin=0, vmax=100, aspect="auto")
    ax.set_xticks(range(len(CATS)), CATS, rotation=30, ha="right", fontsize=8)
    ax.set_yticks(range(len(order)), order, fontsize=8)
    for i in range(len(order)):
        for j in range(len(CATS)):
            if not np.isnan(m[i, j]):
                ax.text(j, i, f"{m[i, j]:.0f}", ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=ax, fraction=0.03); plt.tight_layout()
    fig.savefig(out / "fig_categories.png", dpi=200); plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    for r in summary:
        ax.scatter(r["prompt_tokens"], 100 * r["accuracy"], color="#c44" if r["system"].startswith("decoyre") else "#555")
        ax.annotate(r["system"], (r["prompt_tokens"], 100 * r["accuracy"]), fontsize=7, xytext=(3, 3), textcoords="offset points")
    ax.set_xlabel("Mean prompt tokens per question"); ax.set_ylabel("Strict accuracy (%)"); plt.tight_layout()
    fig.savefig(out / "fig_cost_accuracy.png", dpi=200); plt.close(fig)
