"""
RAG Retriever: Handles query embedding, vector database lookup, score thresholding,
and metadata extraction for the top-k most relevant documentation passages.
"""

import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from src.vectorstore.embeddings import BaseEmbeddingProvider
from src.vectorstore.qdrant_store import QdrantVectorStore


class RetrievalHit(BaseModel):
    chunk_id: str
    doc_id: str
    title: str
    category: str
    score: float
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RetrievalResult(BaseModel):
    query: str
    hits: List[RetrievalHit]
    retrieval_latency_ms: float
    top_score: float = 0.0


class RAGRetriever:
    def __init__(
        self,
        vector_store: QdrantVectorStore,
        embedding_provider: BaseEmbeddingProvider,
        top_k: int = 5,
        score_threshold: float = 0.25,
    ):
        self.vector_store = vector_store
        self.embedding_provider = embedding_provider
        self.top_k = top_k
        self.score_threshold = score_threshold

    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        score_threshold: Optional[float] = None,
        query_filter: Any = None
    ) -> RetrievalResult:
        """
        Retrieves top-k chunks matching the query string.
        Measures exact retrieval latency in milliseconds.
        """
        k = top_k if top_k is not None else self.top_k
        threshold = score_threshold if score_threshold is not None else self.score_threshold

        clean_query = query.strip()
        start_time = time.perf_counter()

        # Step 1: Embed the user query
        query_vector = self.embedding_provider.embed_query(clean_query)

        # Step 2: ANN vector search in Qdrant
        raw_hits = self.vector_store.search(
            query_vector=query_vector,
            limit=k,
            score_threshold=threshold,
            query_filter=query_filter
        )

        latency_ms = (time.perf_counter() - start_time) * 1000.0

        hits: List[RetrievalHit] = []
        top_score = 0.0

        for h in raw_hits:
            score = float(h["score"])
            if score > top_score:
                top_score = score
            hits.append(RetrievalHit(
                chunk_id=h["chunk_id"],
                doc_id=h["doc_id"],
                title=h["title"],
                category=h["category"],
                score=score,
                text=h["text"],
                metadata=h["metadata"]
            ))

        return RetrievalResult(
            query=clean_query,
            hits=hits,
            retrieval_latency_ms=round(latency_ms, 2),
            top_score=round(top_score, 4)
        )
