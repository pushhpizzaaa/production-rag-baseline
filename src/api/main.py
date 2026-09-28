"""
FastAPI Application Entry Point: Exposes REST endpoints for the Baseline RAG Pipeline.
Includes endpoints for corpus ingestion, grounded query execution, and health monitoring.
"""

from contextlib import asynccontextmanager
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.config import settings
from src.pipeline import RAGPipeline, IngestionStats, RAGResponse
from src.api.schemas import (
    QueryRequest,
    QueryResponse,
    ChunkResponse,
    IngestRequest,
    IngestResponse,
    HealthResponse,
)

# Global pipeline instance
pipeline: RAGPipeline = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes the RAG Pipeline and pre-warms the embedding model and vector store."""
    global pipeline
    print(f"[{settings.app_name}] Initializing pipeline and embedding models...")
    pipeline = RAGPipeline(config=settings)
    yield
    print(f"[{settings.app_name}] Shutting down pipeline and closing connections...")
    if pipeline and pipeline.vector_store:
        pipeline.vector_store.close()


app = FastAPI(
    title=settings.app_name,
    description=(
        "Production-grade Baseline RAG (Retrieval-Augmented Generation) Pipeline. "
        "Indexes 200 technical documentation files across FastAPI, Scikit-Learn, and MongoDB. "
        "Provides semantic search, citation-grounded answer generation, and evaluation harness."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Enable CORS for frontend applications or external dashboards
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Returns real-time service health, model information, and indexed vector counts."""
    global pipeline
    if not pipeline:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pipeline not yet initialized"
        )

    try:
        vector_count = pipeline.vector_store.count()
    except Exception as e:
        vector_count = -1

    return HealthResponse(
        status="healthy" if vector_count >= 0 else "degraded",
        app_name=settings.app_name,
        app_env=settings.app_env,
        embedding_model=settings.embedding_model,
        collection_name=settings.collection_name,
        indexed_vectors=vector_count,
    )


@app.post("/ingest", response_model=IngestResponse, tags=["Corpus Management"])
async def trigger_ingestion(request: IngestRequest = IngestRequest()):
    """
    Ingests all 200 documentation markdown files into Qdrant.
    Token-chunks each document (~500 tokens), embeds them, and upserts into vector collection.
    """
    global pipeline
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")

    try:
        stats: IngestionStats = pipeline.ingest_corpus(clear_existing=request.clear_existing)
        return IngestResponse(
            status="success",
            documents_loaded=stats.documents_loaded,
            chunks_created=stats.chunks_created,
            points_indexed=stats.points_indexed,
            elapsed_seconds=stats.elapsed_seconds,
            categories=stats.categories,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@app.post("/query", response_model=QueryResponse, tags=["RAG Execution"])
async def execute_query(request: QueryRequest):
    """
    Executes grounded RAG pipeline:
    1. Embeds query.
    2. Retrieves top-k matching documentation chunks from Qdrant.
    3. Synthesizes an answer with mandatory source citations: [Doc: <chunk_id>].
    4. Emits detailed latency and token telemetry.
    """
    global pipeline
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")

    try:
        response: RAGResponse = pipeline.query(
            query_text=request.query,
            top_k=request.top_k,
            score_threshold=request.score_threshold,
        )

        chunk_responses = [
            ChunkResponse(
                chunk_id=c.chunk_id,
                doc_id=c.doc_id,
                title=c.title,
                category=c.category,
                score=c.score,
                text=c.text,
            )
            for c in response.retrieved_chunks
        ]

        return QueryResponse(
            query=response.query,
            answer=response.answer,
            citations=response.citations,
            retrieved_chunks=chunk_responses,
            model_used=response.model_used,
            latency_ms={
                "retrieval": response.retrieval_latency_ms,
                "generation": response.generation_latency_ms,
                "total": response.total_latency_ms,
            },
            tokens={
                "prompt": response.prompt_tokens,
                "completion": response.completion_tokens,
                "total": response.total_tokens,
            },
            estimated_cost_usd=response.estimated_cost_usd,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host=settings.host, port=settings.port, reload=True)
