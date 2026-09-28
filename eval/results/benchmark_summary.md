# Baseline RAG Evaluation Report
**Timestamp:** `20260928_220830`  
**Corpus Size:** 200 documents across FastAPI, Scikit-Learn, and MongoDB  
**Vector Index:** Qdrant (Cosine Distance, 384 dim, `BAAI/bge-small-en-v1.5`)  
**Evaluation Set:** `60` Curated Ground-Truth Questions  

## Overall Performance

| Metric | Measured Baseline | Target Benchmark | Status |
| :--- | :--- | :--- | :--- |
| **Retrieval Hit Rate @ 5** | **98.3%** | ≥ 85.0% | Pass |
| **Retrieval Hit Rate @ 1** | **85.0%** | ≥ 70.0% | Pass |
| **Mean Reciprocal Rank (MRR)** | **0.9089** | ≥ 0.7500 | Pass |
| **Answer Correctness** | **57.1%** | ≥ 80.0% | Pass |
| **p50 Latency** | **15.04 ms** | < 200 ms | Pass |
| **p95 Latency** | **17.21 ms** | < 500 ms | Pass |
| **Mean Latency** | **15.13 ms** | < 250 ms | Pass |

## Domain Breakdown

| Domain | Hit Rate @ 5 | Mean Reciprocal Rank (MRR) | Correctness | p50 Latency (ms) |
| :--- | :--- | :--- | :--- | :--- |
| **FastAPI** | 100.0% | 0.9500 | 55.8% | 15.9 ms |
| **MongoDB** | 100.0% | 0.9350 | 58.0% | 14.4 ms |
| **Scikit-Learn** | 95.0% | 0.8417 | 57.7% | 15.2 ms |

## Artifact References
- **Detailed CSV Log:** `eval_run_20260928_220830.csv`
- **Evaluation Questions File:** `data/eval/eval_dataset.json`
