"""DecoyRE demo UI.  Run:  streamlit run app.py"""
import json
from pathlib import Path

import streamlit as st

from decoyre.evaluate import ALL, Domain
from decoyre.llm import make_llm

st.set_page_config(page_title="DecoyRE demo", layout="wide")
st.title("DecoyRE: decoy-aware agentic retrieval")

DATA = Path("data")
domains = sorted(p.name for p in DATA.iterdir() if (p / "raw").exists()) if DATA.exists() else []
if not domains:
    st.error("No data found. Run `python run.py generate` first.")
    st.stop()

with st.sidebar:
    backend = st.selectbox("Backend", ["ollama", "openai", "mock"])
    model = st.text_input("Model", "qwen3:8b" if backend == "ollama" else "")
    domain = st.selectbox("Domain corpus", domains)
    systems = st.multiselect("Systems to compare", ALL, default=["rag_dense", "decoyre"])


@st.cache_resource(show_spinner="Indexing corpus and loading bundles...")
def load(backend, model, domain):
    llm = make_llm(backend, model or None)
    return llm, Domain(DATA / domain, llm)


try:
    llm, dom = load(backend, model, domain)
except Exception as e:
    st.error(f"Could not reach the model backend ({e}). Is `ollama serve` running and are "
             "`qwen3:8b` and `nomic-embed-text` pulled? Choose 'mock' to browse offline.")
    st.stop()
tab_ask, tab_cur, tab_res = st.tabs(["Ask", "Curated knowledge", "Benchmark results"])

with tab_ask:
    qs = [json.loads(l) for l in open(DATA / "questions.jsonl") if json.loads(l)["domain"] == domain]
    pick = st.selectbox("Benchmark question (or type your own below)", [""] + [f"[{q['category']}] {q['question']}" for q in qs])
    question = st.text_input("Question", pick.split("] ", 1)[1] if pick else "")
    if st.button("Run", type="primary") and question:
        cols = st.columns(max(1, len(systems)))
        for col, name in zip(cols, systems):
            with col:
                st.subheader(name)
                with st.spinner("thinking..."):
                    r = dom.system(name, llm).answer(question)
                meta = r.get("meta", {})
                if "intent" in meta:
                    st.caption(f"Router: **{meta['intent']}** (via {meta['routed_by']})")
                for t in r.get("trace", []):
                    with st.expander(f"{t['tool']}({t['arg']})"):
                        st.code(t["output"][:3000])
                if meta.get("verifier"):
                    first = meta["verifier"][0]
                    if first:
                        st.warning("Verifier rejected first answer:\n\n- " + "\n- ".join(first))
                        st.caption("First answer: " + r.get("first_answer", "")[:400])
                    else:
                        st.success("Verifier: passed")
                if meta.get("retrieved"):
                    st.caption("Retrieved: " + ", ".join(meta["retrieved"]))
                st.markdown("**Answer**")
                st.write(r["answer"])
                st.caption(f"{r['prompt_tokens']} prompt tokens · {r['llm_calls']} LLM calls · {r['tool_calls']} tool calls · {r['latency_s']} s")

with tab_cur:
    g = dom.curated["full"].graph
    st.metric("Curation accuracy vs ground truth", (g.get("curation_accuracy") or {}).get("accuracy", "n/a"))
    st.markdown(dom.curated["full"].index_text)
    st.dataframe([{"document": p, "status": s["status"], "superseded_by": ", ".join(s["superseded_by"]),
                   "evidence": "; ".join(s["evidence"])} for p, s in sorted(g["docs"].items())], width="stretch")

with tab_res:
    runs = sorted(p for p in Path("results").glob("*") if (p / "summary.md").exists()) if Path("results").exists() else []
    if not runs:
        st.info("No results yet. Run `python run.py eval`.")
    else:
        run = st.selectbox("Run", runs)
        st.markdown((run / "summary.md").read_text())
        for fig in ["fig_accuracy.png", "fig_categories.png", "fig_cost_accuracy.png"]:
            if (run / fig).exists():
                st.image(str(run / fig))
