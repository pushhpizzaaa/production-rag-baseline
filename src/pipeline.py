"""
RAG Pipeline Orchestrator: Combines document loading, token-aware chunking,
dense vector embedding, Qdrant index management, semantic retrieval, and
grounded answer generation with citations into a unified service.
"""

import time
from typing import List, Dict, Any, Optional
from pathlib import Path
from pydantic import BaseModel, Field

from src.config import Settings, settings
from src.ingestion.loader import DocumentLoader, Document
from src.ingestion.chunker import TokenAwareChunker, Chunk
from src.vectorstore.embeddings import BaseEmbeddingProvider, get_embedding_provider
from src.vectorstore.qdrant_store import QdrantVectorStore
from src.retrieval.retriever import RAGRetriever, RetrievalHit, RetrievalResult
from src.generation.generator import RAGGenerator, GenerationResult


class IngestionStats(BaseModel):
    documents_loaded: int
    chunks_created: int
    points_indexed: int
    elapsed_seconds: float
    categories: Dict[str, int]


class RAGResponse(BaseModel):
    query: str
    answer: str
    citations: List[str]
    retrieved_chunks: List[RetrievalHit]
    model_used: str
    retrieval_latency_ms: float
    generation_latency_ms: float
    total_latency_ms: float
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float


class RAGPipeline:
    def __init__(
        self,
        config: Optional[Settings] = None,
        embedding_provider: Optional[BaseEmbeddingProvider] = None,
        vector_store: Optional[QdrantVectorStore] = None,
        retriever: Optional[RAGRetriever] = None,
        generator: Optional[RAGGenerator] = None,
    ):
        self.config = config or settings
        
        # 1. Embedding Provider
        self.embedding_provider = embedding_provider or get_embedding_provider(
            provider_name=self.config.embedding_provider,
            model_name=self.config.embedding_model,
            dimension=self.config.embedding_dim
        )

        # 2. Vector Store
        self.vector_store = vector_store or QdrantVectorStore(
            collection_name=self.config.collection_name,
            vector_dim=self.config.embedding_dim,
            storage_path=self.config.qdrant_storage_path if not self.config.qdrant_url else None,
            qdrant_url=self.config.qdrant_url or None,
            api_key=self.config.qdrant_api_key or None,
        )

        # 3. Retriever
        self.retriever = retriever or RAGRetriever(
            vector_store=self.vector_store,
            embedding_provider=self.embedding_provider,
            top_k=self.config.top_k,
            score_threshold=self.config.score_threshold,
        )

        # 4. Generator
        self.generator = generator or RAGGenerator(
            model=self.config.llm_model,
            openai_api_key=self.config.openai_api_key,
            gemini_api_key=self.config.gemini_api_key,
            anthropic_api_key=self.config.anthropic_api_key,
        )

    def ingest_corpus(
        self,
        raw_data_dir: Optional[Path] = None,
        clear_existing: bool = True,
        batch_size: int = 64
    ) -> IngestionStats:
        """
        Executes end-to-end ingestion:
        Directory -> Documents -> Token-Aware Chunks -> Dense Embeddings -> Qdrant Index.
        """
        start_time = time.perf_counter()
        target_dir = raw_data_dir or self.config.raw_data_dir

        if clear_existing:
            self.vector_store.clear()

        # Step 1: Load documents
        loader = DocumentLoader(target_dir)
        documents = loader.load_all()

        category_counts: Dict[str, int] = {}
        for d in documents:
            category_counts[d.category] = category_counts.get(d.category, 0) + 1

        # Step 2: Chunk documents with token awareness
        chunker = TokenAwareChunker(
            chunk_size_tokens=self.config.chunk_size_tokens,
            chunk_overlap_tokens=self.config.chunk_overlap_tokens
        )
        chunks = chunker.chunk_all(documents)

        # Step 3: Embed chunks
        chunk_texts = [c.text for c in chunks]
        embeddings = self.embedding_provider.embed_documents(chunk_texts)

        # Step 4: Index points in Qdrant
        indexed_count = self.vector_store.upsert_chunks(chunks, embeddings, batch_size=batch_size)

        elapsed = time.perf_counter() - start_time
        return IngestionStats(
            documents_loaded=len(documents),
            chunks_created=len(chunks),
            points_indexed=indexed_count,
            elapsed_seconds=round(elapsed, 2),
            categories=category_counts
        )

    def query(
        self,
        query_text: str,
        top_k: Optional[int] = None,
        score_threshold: Optional[float] = None,
        query_filter: Any = None
    ) -> RAGResponse:
        """
        Executes full RAG flow:
        Query -> Retrieve Top Chunks -> Grounded Generation with Citations -> Telemetry.
        """
        start_time = time.perf_counter()

        # Step 1: Semantic Retrieval
        retrieval_res: RetrievalResult = self.retriever.retrieve(
            query=query_text,
            top_k=top_k,
            score_threshold=score_threshold,
            query_filter=query_filter
        )

        # Step 2: Generation with Citations
        gen_res: GenerationResult = self.generator.generate(
            query=query_text,
            hits=retrieval_res.hits
        )

        total_latency_ms = (time.perf_counter() - start_time) * 1000.0

        return RAGResponse(
            query=query_text,
            answer=gen_res.answer,
            citations=gen_res.citations,
            retrieved_chunks=retrieval_res.hits,
            model_used=gen_res.model,
            retrieval_latency_ms=retrieval_res.retrieval_latency_ms,
            generation_latency_ms=gen_res.generation_latency_ms,
            total_latency_ms=round(total_latency_ms, 2),
            prompt_tokens=gen_res.prompt_tokens,
            completion_tokens=gen_res.completion_tokens,
            total_tokens=gen_res.total_tokens,
            estimated_cost_usd=gen_res.estimated_cost_usd
        )
