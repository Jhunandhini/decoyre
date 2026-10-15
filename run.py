"""DecoyRE command line.

  python run.py generate                         # build benchmark into data/
  python run.py curate                           # run the Curator agent on every domain
  python run.py eval --systems core              # run experiments (resumable)
  python run.py ask -d retail "How do we calculate revenue?"
  python run.py report --out results/main        # rebuild tables/figures from rows.jsonl

Backends: --backend ollama (default, local) | openai (any OpenAI-compatible URL) | mock (offline plumbing test)
"""
import argparse
import json

from decoyre.evaluate import ALL, CORE, Domain, report, run
from decoyre.generator import generate
from decoyre.llm import make_llm


def get_llm(a):
    kw = {}
    if a.backend == "ollama":
        kw = {"embed_model": a.embed_model}
    elif a.backend == "openai" and a.embed_model != "nomic-embed-text":
        kw = {"embed_model": a.embed_model}
    return make_llm(a.backend, a.model, **kw)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["generate", "curate", "eval", "ask", "report"])
    p.add_argument("question", nargs="?")
    p.add_argument("--data", default="data")
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--variants", type=int, default=1, help="corpus instantiations per domain")
    p.add_argument("--backend", default="ollama", choices=["ollama", "openai", "mock"])
    p.add_argument("--model", default=None)
    p.add_argument("--embed-model", default="nomic-embed-text")
    p.add_argument("--systems", default="core", help="core | all | comma list")
    p.add_argument("--domains", default=None, help="comma list (retail,saas,logistics)")
    p.add_argument("--limit", type=int, default=None, help="max questions per domain (quick runs)")
    p.add_argument("--out", default="results/main")
    p.add_argument("--recurate", action="store_true")
    p.add_argument("--no-curator-llm", action="store_true", help="rule-only curation")
    p.add_argument("-d", "--domain", default="retail")
    p.add_argument("-s", "--system", default="decoyre")
    a = p.parse_intermixed_args()

    if a.cmd == "generate":
        generate(a.data, seed=a.seed, variants=a.variants)
        return
    if a.cmd == "report":
        report(a.out)
        return
    llm = get_llm(a)
    if a.cmd == "curate":
        import pathlib
        for d in (a.domains.split(",") if a.domains else sorted(x.name for x in pathlib.Path(a.data).iterdir() if x.is_dir())):
            Domain(f"{a.data}/{d}", llm, recurate=True, curator_llm=not a.no_curator_llm)
    elif a.cmd == "eval":
        systems = CORE if a.systems == "core" else ALL if a.systems == "all" else a.systems.split(",")
        run(a.data, llm, systems, a.domains.split(",") if a.domains else None, a.limit, a.out,
            a.recurate, not a.no_curator_llm)
    elif a.cmd == "ask":
        dom = Domain(f"{a.data}/{a.domain}", llm)
        r = dom.system(a.system, llm).answer(a.question)
        for t in r.get("trace", []):
            print(f"  -> {t['tool']}({t['arg']!r})  [{len(t['output'])} chars]")
        print(json.dumps(r.get("meta", {}), indent=1))
        print("\nANSWER:\n" + r["answer"])
        print(f"\n[{r['prompt_tokens']} prompt tokens, {r['llm_calls']} LLM calls, {r['latency_s']}s]")


if __name__ == "__main__":
    main()
