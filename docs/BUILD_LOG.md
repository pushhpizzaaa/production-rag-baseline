# Baseline RAG Pipeline - Chronological Engineering Build Log

This document records the complete, step-by-step engineering decisions, implementation details, trade-offs, and empirical findings made during the development of the Baseline RAG Pipeline.

---

## 1. Project Objectives and Scope

The goal was to engineer a production-ready, open-source **Baseline RAG (Retrieval-Augmented Generation) Pipeline** designed for deployment to GitHub. 

Key constraints and requirements:
1. **Corpus**: Exactly 200 high-quality, comprehensive technical documentation files spanning three distinct, real-world engineering domains:
   - **FastAPI** (70 documents): Asynchronous web endpoints, Pydantic schemas, dependency injection, OAuth2/JWT security, lifespan events, background tasks, streaming responses.
   - **Scikit-Learn** (65 documents): Estimator/Transformer design, Pipelines, ColumnTransformers, regularized regressions (L1/L2), ensemble bagging/boosting, clustering, cross-validation, and metrics.
   - **MongoDB** (65 documents): BSON document model, CRUD mechanics, Aggregation pipeline stages ($group, $lookup, $unwind), compound ESR indexing, replication, write concerns, sharding, and transactions.
2. **Chunking Strategy**: Token-aware chunking ($\approx 500$ tokens with 50-token overlap) respecting paragraph and markdown header boundaries.
3. **Embeddings & Vector Database**: High-speed, local ONNX embeddings (`BAAI/bge-small-en-v1.5`, 384 dimensions) with Qdrant vector database (supporting both zero-setup local embedded mode and remote server/Docker mode).
4. **Retrieval & Grounded Generation**: Semantic search retrieving top 5 chunks with strict, machine-extractable citation formatting: `[Doc: <chunk_id>]`.
5. **REST API**: Production FastAPI service exposing `/query`, `/ingest`, `/health`, and Swagger documentation.
6. **Evaluation Benchmark**: A 60-question gold evaluation benchmark with automated scoring of Hit Rate @ 5, Hit Rate @ 1, Mean Reciprocal Rank (MRR), Answer Correctness, and p50/p95 latency percentiles.
7. **Downstream Ready**: Serves as the clean baseline for three advanced derivative projects:
   - Project 1: Semantic Caching & Cost-Aware Routing
   - Project 2: Permission-Aware Multi-Tenant RAG
   - Project 3: GraphRAG for Multi-Hop Questions

---

## 2. Chronological Engineering Steps

### Step 1: Environment Setup & Tooling Configuration
- Initialized local Git repository (`git init`).
- Configured `.gitignore` to prevent committing virtual environment directories, cache files, and local Qdrant storage `.qdrant_data`.
- Created an isolated Python virtual environment (`.venv`).
- Selected dependency stack pinned in `requirements.txt`:
  - `fastapi` & `uvicorn` for high-throughput asynchronous web serving.
  - `qdrant-client` for vector search with payload filtering capabilities.
  - `fastembed` for CPU-optimized ONNX-runtime dense embeddings without heavy PyTorch or CUDA dependencies.
  - `litellm` for standardized multi-provider LLM interfacing (OpenAI, Gemini, Anthropic, Ollama).
  - `pydantic` & `pydantic-settings` for robust runtime schema validation and 12-factor environment variable loading.
  - `pytest` & `httpx` for test coverage.
  - `tabulate` & `tqdm` for terminal reporting and progress telemetry.

### Step 2: 200-Document Technical Corpus Generation
- Developed `scripts/generate_corpus.py` to create 200 structured markdown files with real technical depth:
  - 70 FastAPI files in `data/raw/fastapi/`
  - 65 Scikit-Learn files in `data/raw/scikitlearn/`
  - 65 MongoDB files in `data/raw/mongodb/`
- Every file includes structured frontmatter: `Doc ID`, `Category`, `Domain`, `Summary`, followed by in-depth conceptual explanations, working Python/JavaScript code snippets, and operational best practices.

### Step 3: Ingestion Engine & Token-Aware Chunker
- Built `src/ingestion/loader.py`: Scans directories, extracts metadata headers, isolates content bodies, and instantiates structured `Document` objects.
- Built `src/ingestion/chunker.py`:
  - Implements `TokenAwareChunker`. Rather than slicing raw characters arbitrarily, it splits text on paragraph and section boundaries.
  - Employs word-to-token approximation (target 500 tokens $\approx 375$ words, overlap 50 tokens $\approx 37$ words).
  - Prefixes each chunk with a contextual header: `[{category} - {title}]\n{body}` to anchor the embedding representation in semantic space.
  - Generates deterministic chunk identifiers: `{doc_id}#chunk_{chunk_index}`.

### Step 4: Embedding Provider & Vector Store Architecture
- Built `src/vectorstore/embeddings.py`:
  - Abstract base class `BaseEmbeddingProvider`.
  - Concrete `FastEmbedProvider` running `BAAI/bge-small-en-v1.5` (384 dimensions) on ONNX Runtime. This provides sub-millisecond local inference with 0 API cost.
  - `MockEmbeddingProvider` for instant deterministic test isolation.
- Built `src/vectorstore/qdrant_store.py`:
  - Manages Qdrant client lifecycle. Supports embedded on-disk storage (`.qdrant_data`) and remote server connections (`QDRANT_URL`).
  - Automatically provisions the target collection with `Distance.COSINE`.
  - Creates keyword payload indexes on metadata fields (`doc_id`, `category`, `domain`, `chunk_id`) to enable fast pre-retrieval filtering (laying the groundwork for Project 2's ACL pre-filter).
  - Uses UUID5 hashing based on chunk IDs to achieve idempotent upserts.

### Step 5: Semantic Retrieval Engine
- Built `src/retrieval/retriever.py`:
  - Embeds the query and queries Qdrant for top-$k$ nearest neighbors.
  - Records exact retrieval latency in milliseconds.
  - Returns structured `RetrievalResult` containing ranked `RetrievalHit` instances with cosine similarity scores, text, titles, and metadata.

### Step 6: Grounded Generator with Strict Citations
- Built `src/generation/generator.py`:
  - Constructs a system prompt that strictly mandates factual grounding and explicit citations using `[Doc: <chunk_id>]`.
  - Supports LiteLLM completions when API keys (`OPENAI_API_KEY`, `GEMINI_API_KEY`, etc.) are configured.
  - Provides a built-in **Deterministic Offline Grounded Synthesizer**: extracts salient sentences from the top retrieved chunks, synthesizing a cited response. This ensures 100% zero-cost reproduction for anyone evaluating the pipeline without API credentials.
  - Extracts and validates citations via regular expressions.

### Step 7: Unified RAG Pipeline Orchestrator
- Built `src/pipeline.py`:
  - `RAGPipeline.ingest_corpus()`: Automates Document Loading $\to$ Token Chunking $\to$ Dense Embedding $\to$ Qdrant Upsert.
  - `RAGPipeline.query()`: Orchestrates Query $\to$ Retrieval $\to$ Generation $\to$ Telemetry measurement.
  - Emits telemetry on every request: retrieval latency, generation latency, total latency, prompt tokens, completion tokens, and estimated cost.

### Step 8: FastAPI REST Service
- Built `src/api/schemas.py` and `src/api/main.py`:
  - `POST /query`: Executes RAG query, returning answer, citations, chunk details, and latency breakdown.
  - `POST /ingest`: Triggers corpus ingestion.
  - `GET /health`: Reports service status and real-time indexed vector count.
  - Configured CORS middleware and async `lifespan` context manager to manage embedding models and Qdrant database locks cleanly.

### Step 9: Evaluation Benchmark Suite
- Generated `data/eval/eval_dataset.json` containing 60 hand-verified questions (20 FastAPI, 20 Scikit-Learn, 20 MongoDB) with ground-truth target documents, reference answers, key concept keywords, and difficulty ratings.
- Built `eval/scorer.py` and `eval/runner.py`:
  - Evaluates Hit Rate @ 5, Hit Rate @ 1, Mean Reciprocal Rank (MRR), and Concept Grounding.
  - Profiles p50, p90, and p95 latency percentiles.
  - Exports per-question CSV logs to `eval/results/eval_run_<timestamp>.csv` and markdown summary to `eval/results/benchmark_summary.md`.

### Step 10: Verification & Quality Assurance
- Executed `scripts/run_ingest.py`: Successfully indexed all 200 documents in 90.38 seconds.
- Executed `scripts/run_eval.py`:
  - **Hit Rate @ 5: 98.3%**
  - **Hit Rate @ 1: 85.0%**
  - **MRR: 0.9089**
  - **p50 Latency: 15.04 ms**
- Authored test suites in `tests/`:
  - `test_chunker.py`: DocumentLoader and TokenAwareChunker tests.
  - `test_vectorstore.py`: Qdrant in-memory operations and search tests.
  - `test_pipeline.py`: End-to-end RAG query integration tests.
  - `test_api.py`: FastAPI endpoint tests via `TestClient`.
- Ran `pytest -v`: **5 passed in 3.87s (100% passing)**.
- Authored `Dockerfile` and `docker-compose.yml` for containerized deployment.

---

## 3. Summary of Project Files

| Path | Purpose |
| :--- | :--- |
| `src/config.py` | Centralized configuration via Pydantic BaseSettings |
| `src/ingestion/loader.py` | Parses markdown files and extracts structured metadata |
| `src/ingestion/chunker.py` | Token-aware document chunking (~500 tokens, 50 overlap) |
| `src/vectorstore/embeddings.py` | FastEmbed ONNX embedding provider abstraction |
| `src/vectorstore/qdrant_store.py` | Qdrant vector database client, payload indexes, and queries |
| `src/retrieval/retriever.py` | Top-k semantic search and latency measurement |
| `src/generation/generator.py` | Grounded answer generation with strict `[Doc: ...]` citations |
| `src/pipeline.py` | End-to-end pipeline orchestrator |
| `src/api/main.py` | FastAPI application exposing REST endpoints |
| `eval/runner.py` | Automated evaluation benchmark runner |
| `eval/scorer.py` | Information retrieval and answer correctness metrics |
| `scripts/run_ingest.py` | CLI ingestion runner |
| `scripts/run_eval.py` | CLI evaluation runner |
| `data/raw/` | 200 markdown documentation files |
| `data/eval/eval_dataset.json` | 60 curated evaluation questions |
| `tests/` | Pytest unit and integration test suite |
| `README.md` | Recruiter-grade documentation with architecture diagram & eval table |
