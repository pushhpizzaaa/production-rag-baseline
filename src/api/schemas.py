"""
API Schemas: Pydantic request and response models for the FastAPI REST interface.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=2, example="How do dependencies with yield work in FastAPI?")
    top_k: Optional[int] = Field(default=5, ge=1, le=20, description="Number of context passages to retrieve")
    score_threshold: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Minimum cosine similarity")


class ChunkResponse(BaseModel):
    chunk_id: str
    doc_id: str
    title: str
    category: str
    score: float
    text: str


class QueryResponse(BaseModel):
    query: str
    answer: str
    citations: List[str]
    retrieved_chunks: List[ChunkResponse]
    model_used: str
    latency_ms: Dict[str, float]
    tokens: Dict[str, int]
    estimated_cost_usd: float


class IngestRequest(BaseModel):
    clear_existing: bool = Field(default=True, description="Whether to purge existing vectors before re-ingestion")


class IngestResponse(BaseModel):
    status: str
    documents_loaded: int
    chunks_created: int
    points_indexed: int
    elapsed_seconds: float
    categories: Dict[str, int]


class HealthResponse(BaseModel):
    status: str
    app_name: str
    app_env: str
    embedding_model: str
    collection_name: str
    indexed_vectors: int
