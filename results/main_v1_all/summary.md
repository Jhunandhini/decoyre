# DecoyRE results

## Overall

| System | N | Acc % (95% CI) | Lenient % | Decoy % | Abstain-correct % | False-abstain % | Prompt tok | LLM calls | Tool calls | Latency s |
|---|---|---|---|---|---|---|---|---|---|---|
| rag_dense | 72 | 75.0 (63.9-84.7) | 76.4 | 1.7 | 91.7 | 5.0 | 551 | 1.00 | 0.00 | 35.55 |
| rag_hybrid | 72 | 70.8 (59.7-80.6) | 72.2 | 3.3 | 75.0 | 5.0 | 576 | 1.00 | 0.00 | 24.68 |
| agent_search | 72 | 45.8 (34.7-56.9) | 45.8 | 0.0 | 91.7 | 25.0 | 630 | 1.46 | 0.46 | 26.84 |
| okf_rag_gold | 72 | 51.4 (40.3-62.5) | 51.4 | 0.0 | 100.0 | 28.3 | 686 | 1.31 | 0.31 | 17.55 |
| decoyre | 72 | 77.8 (66.7-87.5) | 77.8 | 0.0 | 91.7 | 13.3 | 1443 | 2.19 | 0.88 | 45.41 |
| okf_gold | 72 | 43.1 (31.9-54.2) | 43.1 | 0.0 | 100.0 | 31.7 | 476 | 1.17 | 0.17 | 13.32 |
| decoyre_no_verifier | 72 | 54.2 (41.7-65.3) | 54.2 | 0.0 | 100.0 | 16.7 | 993 | 1.54 | 0.54 | 35.26 |
| decoyre_no_router | 72 | 87.5 (79.2-94.4) | 87.5 | 0.0 | 83.3 | 0.0 | 1904 | 2.93 | 1.07 | 52.43 |
| decoyre_no_status | 72 | 77.8 (66.7-86.1) | 77.8 | 0.0 | 100.0 | 13.3 | 1444 | 2.18 | 0.88 | 45.96 |
| decoyre_date_only | 72 | 68.1 (56.9-79.2) | 68.1 | 13.3 | 100.0 | 11.7 | 1344 | 2.07 | 0.82 | 46.49 |

## Accuracy by failure category (%)

| System | deprecated | validity | homonym | split_table | composition | absence | long_tail |
|---|---|---|---|---|---|---|---|
| rag_dense | 100.0 | 88.9 | 83.3 | 33.3 | 50.0 | 91.7 | 91.7 |
| rag_hybrid | 88.9 | 100.0 | 83.3 | 41.7 | 58.3 | 75.0 | 66.7 |
| agent_search | 0.0 | 66.7 | 0.0 | 33.3 | 8.3 | 91.7 | 91.7 |
| okf_rag_gold | 22.2 | 44.4 | 100.0 | 75.0 | 33.3 | 100.0 | 0.0 |
| decoyre | 88.9 | 88.9 | 100.0 | 66.7 | 33.3 | 91.7 | 91.7 |
| okf_gold | 22.2 | 22.2 | 100.0 | 41.7 | 33.3 | 100.0 | 0.0 |
| decoyre_no_verifier | 11.1 | 22.2 | 100.0 | 41.7 | 16.7 | 100.0 | 91.7 |
| decoyre_no_router | 88.9 | 100.0 | 100.0 | 91.7 | 66.7 | 83.3 | 91.7 |
| decoyre_no_status | 88.9 | 88.9 | 100.0 | 66.7 | 33.3 | 100.0 | 83.3 |
| decoyre_date_only | 33.3 | 33.3 | 100.0 | 58.3 | 58.3 | 100.0 | 91.7 |

## Paired exact McNemar test (DecoyRE vs baseline)

| Baseline | N | Only DecoyRE correct | Only baseline correct | p |
|---|---|---|---|---|
| rag_dense | 72 | 11 | 9 | 0.8238 |
| rag_hybrid | 72 | 13 | 8 | 0.3833 |
| agent_search | 72 | 28 | 5 | 0.0001 |
| okf_rag_gold | 72 | 25 | 6 | 0.0009 |
| okf_gold | 72 | 30 | 5 | 0.0000 |
| decoyre_no_verifier | 72 | 18 | 1 | 0.0001 |
| decoyre_no_router | 72 | 4 | 11 | 0.1185 |
| decoyre_no_status | 72 | 1 | 1 | 1.0000 |
| decoyre_date_only | 72 | 12 | 5 | 0.1435 |

## Curation accuracy (document status vs ground truth)

| Domain | Full curator | Date-only ablation |
|---|---|---|
| retail-v1 | 1.0 | 0.5 |
| saas-v1 | 1.0 | 0.643 |
| logistics-v1 | 1.0 | 0.786 |
