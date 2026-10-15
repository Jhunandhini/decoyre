# DecoyRE: Decoy-aware Agentic Retrieval for Enterprise Knowledge

Enterprise documentation is full of *decoys*: deprecated pages nobody deleted, tables with
near-identical names, schemas that chunking splits apart, definitions scattered across documents,
and questions whose answer simply does not exist. Plain RAG retrieves whatever is most *similar*,
not what is *valid*. DecoyRE is a multi-agent system that curates the corpus into a status-aware
knowledge bundle, routes each question to the right tool, and verifies answers before returning them.

Inspired by J. Ruiz, *rag-vs-okf* (GitHub, 2026), a 7-question demonstration that curated knowledge
(OKF) beats RAG. DecoyRE is an independent implementation with its own benchmark. It addresses that
demo's two open problems: the curated bundle had to be written by hand, and the combined agent
picked the wrong tool.

## Architecture

```
            raw corpus (wiki, schemas, ADRs, notes, tickets)
                     |
             [1] CURATOR AGENT  (rules + LLM extraction)
                 self-markers -> decision links -> per-topic resolution -> composition
                     |
          curated bundle (concept pages, index, graph.json with doc status)
                     |
 question -> [2] ROUTER AGENT -> intent -> tool plan
                     |
             [3] ANSWERER AGENT (tool loop)
                 read_concept (curated, unchunked)  |  search_docs (hybrid BM25+dense, status-aware)
                     |
             [4] VERIFIER AGENT
                 deprecated-citation check, grounding check, premature-abstention check
                 -> on failure: one revision with feedback
                     |
                  answer + citations + trace
```

## Benchmark (generated, deterministic gold)

`python run.py generate --variants 3` creates 3 domains (retail, SaaS, logistics) x 3 randomised
corpus instantiations = 9 corpora, 297 documents and 216 questions over 7 failure categories:

| Category | Decoy |
|---|---|
| deprecated | old page phrased like the question; deprecation only stated in a separate ADR; sometimes the old page has a *newer* edit date |
| validity | which of two coexisting definitions is in force |
| homonym | `orders`, `orders_staging`, `orders_v2`, `orders_legacy_pos`; the legacy doc still claims to feed the report |
| split_table | relevant column sits far from the table name in a wide schema |
| composition | one definition spread over wiki + ADR + meeting note + finance doc |
| absence | no answer exists; near-miss docs tempt hallucination |
| long_tail | answer only in a colloquial support ticket |

ADR wording comes in three styles (explicit paths, explicit titles, implicit). Rules can parse the
first two; the implicit style needs the LLM curator.

Scoring is deterministic: each question lists required facts (identifiers, numbers, ticket IDs)
and decoy facts. **Strict accuracy** means all required facts are present, no decoy appears, and the
answer is not an abstention. For absence questions, an abstention is the correct answer.

## Systems compared

| System | Description |
|---|---|
| rag_dense | top-5 dense chunks -> LLM (baseline) |
| rag_hybrid | BM25 + dense with reciprocal rank fusion |
| agent_search | ReAct-style agent with search only (agentic RAG) |
| okf_gold | agent over the hand-curated gold bundle (repo-style OKF, upper-bound curation) |
| okf_rag_gold | gold bundle + search (repo-style combined layer) |
| **decoyre** | auto-curated bundle + router + status-aware search + verifier |
| decoyre_no_verifier / _no_router / _no_status / _date_only | ablations |

## Setup

```bash
pip install -r requirements.txt
# local model (privacy-preserving, no API key)
ollama pull qwen3:8b
ollama pull nomic-embed-text
ollama serve      # if not already running
```

## Run

```bash
python run.py generate --variants 3                 # dataset -> data/
python run.py curate                                # Curator agent (LLM-assisted)
python run.py eval --systems core --domains retail-v1 --limit 4 --out results/smoke   # 2-minute smoke test
python run.py eval --systems all --domains retail-v1,saas-v1,logistics-v1 --out results/main
python run.py eval --systems core --out results/main   # adds v2, v3 (resumable; skips done rows)
python run.py report --out results/main             # tables + figures
python run.py ask -d retail-v1 -s decoyre "How do we calculate revenue?"
streamlit run app.py                                # demo UI
```

Runs are resumable: interrupt at any time and rerun the same command to continue.

Optional ablation: run `curate --no-curator-llm` into a separate data copy to measure what the LLM adds
over rule-only curation.

Other backends:
- `--backend openai --model <name>` works with any OpenAI-compatible server (Groq, OpenRouter, vLLM,
  LM Studio). Set `OPENAI_BASE_URL` and `OPENAI_API_KEY`.
- `--backend mock` runs offline for plumbing tests only. Its numbers are not results.

## Outputs (`results/<run>/`)

- `rows.jsonl` - every answer with its trace, cost and scores
- `summary.md` / `summary.csv` - overall metrics, 95% bootstrap CIs, per-category accuracy, McNemar tests vs DecoyRE, curation accuracy
- `fig_accuracy.png`, `fig_categories.png`, `fig_cost_accuracy.png`

## Code map

```
decoyre/domains.py     domain knowledge specs (3 companies)
decoyre/generator.py   benchmark generator with planted decoys
decoyre/retrieval.py   chunking, dense / BM25 / hybrid index, embedding cache
decoyre/curator.py     Curator agent
decoyre/agents.py      tools, agent loop, Router, Verifier, all systems
decoyre/evaluate.py    scoring, runner, statistics, figures
decoyre/llm.py         Ollama / OpenAI-compatible / mock backends
run.py                 CLI
app.py                 Streamlit demo
```
