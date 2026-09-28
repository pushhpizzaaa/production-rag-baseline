"""
Integration tests for end-to-end RAG Pipeline using isolated in-memory vector store.
"""

from src.pipeline import RAGPipeline
from src.vectorstore.qdrant_store import QdrantVectorStore
from src.vectorstore.embeddings import MockEmbeddingProvider
from src.ingestion.chunker import Chunk
from src.retrieval.retriever import RAGRetriever
from src.generation.generator import RAGGenerator


def test_rag_pipeline_query():
    # Use isolated in-memory vector store for unit tests
    dim = 32
    embed_provider = MockEmbeddingProvider(dimension=dim)
    store = QdrantVectorStore(collection_name="test_pipeline_col", vector_dim=dim, storage_path=None)

    sample_chunks = [
        Chunk(
            chunk_id="fastapi_yield#chunk_0",
            doc_id="fastapi_yield",
            chunk_index=0,
            text="Dependencies with yield handle teardown and cleanup in a finally block.",
            token_count=15,
            char_length=70,
            metadata={"title": "Yield Dependencies", "category": "FastAPI", "doc_id": "fastapi_yield"}
        )
    ]
    embs = embed_provider.embed_documents([c.text for c in sample_chunks])
    store.upsert_chunks(sample_chunks, embs)

    retriever = RAGRetriever(vector_store=store, embedding_provider=embed_provider, top_k=2)
    generator = RAGGenerator()
    pipeline = RAGPipeline(
        embedding_provider=embed_provider,
        vector_store=store,
        retriever=retriever,
        generator=generator
    )

    try:
        response = pipeline.query("How do dependencies with yield work?", top_k=2)
        assert "dependencies with yield" in response.query
        assert len(response.retrieved_chunks) > 0
        assert len(response.citations) > 0
        assert "[Doc:" in response.answer
        assert response.retrieval_latency_ms >= 0
    finally:
        store.close()
