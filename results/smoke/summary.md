# DecoyRE results

## Overall

| System | N | Acc % (95% CI) | Lenient % | Decoy % | Abstain-correct % | False-abstain % | Prompt tok | LLM calls | Tool calls | Latency s |
|---|---|---|---|---|---|---|---|---|---|---|
| rag_dense | 4 | 100.0 (100.0-100.0) | 100.0 | 0.0 | - | 0.0 | 494 | 1.00 | 0.00 | 38.84 |
| rag_hybrid | 4 | 100.0 (100.0-100.0) | 100.0 | 0.0 | - | 0.0 | 531 | 1.00 | 0.00 | 25.36 |
| agent_search | 4 | 50.0 (0.0-100.0) | 50.0 | 0.0 | - | 25.0 | 610 | 1.50 | 0.50 | 30.76 |
| okf_rag_gold | 4 | 25.0 (0.0-75.0) | 25.0 | 0.0 | - | 0.0 | 578 | 1.25 | 0.25 | 19.57 |
| decoyre | 4 | 100.0 (100.0-100.0) | 100.0 | 0.0 | - | 0.0 | 1860 | 3.00 | 1.00 | 69.99 |

## Accuracy by failure category (%)

| System | deprecated | validity | homonym | split_table | composition | absence | long_tail |
|---|---|---|---|---|---|---|---|
| rag_dense | 100.0 | 100.0 | - | - | - | - | - |
| rag_hybrid | 100.0 | 100.0 | - | - | - | - | - |
| agent_search | 0.0 | 100.0 | - | - | - | - | - |
| okf_rag_gold | 0.0 | 50.0 | - | - | - | - | - |
| decoyre | 100.0 | 100.0 | - | - | - | - | - |

## Paired exact McNemar test (DecoyRE vs baseline)

| Baseline | N | Only DecoyRE correct | Only baseline correct | p |
|---|---|---|---|---|
| rag_dense | 4 | 0 | 0 | 1.0000 |
| rag_hybrid | 4 | 0 | 0 | 1.0000 |
| agent_search | 4 | 2 | 0 | 0.5000 |
| okf_rag_gold | 4 | 3 | 0 | 0.2500 |

## Curation accuracy (document status vs ground truth)

| Domain | Full curator | Date-only ablation |
|---|---|---|
| retail-v1 | 1.0 | 0.5 |
