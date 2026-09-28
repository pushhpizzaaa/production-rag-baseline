"""
Unit tests for QdrantVectorStore and FastEmbed/Mock providers.
"""

from src.vectorstore.embeddings import MockEmbeddingProvider
from src.vectorstore.qdrant_store import QdrantVectorStore
from src.ingestion.chunker import Chunk


def test_qdrant_vectorstore_in_memory():
    dim = 32
    embed_provider = MockEmbeddingProvider(dimension=dim)
    store = QdrantVectorStore(collection_name="test_collection", vector_dim=dim, storage_path=None)

    try:
        chunks = [
            Chunk(
                chunk_id="doc_a#chunk_0",
                doc_id="doc_a",
                chunk_index=0,
                text="FastAPI request validation with Pydantic",
                token_count=10,
                char_length=40,
                metadata={"title": "FastAPI Validation", "category": "FastAPI", "doc_id": "doc_a"}
            ),
            Chunk(
                chunk_id="doc_b#chunk_0",
                doc_id="doc_b",
                chunk_index=0,
                text="MongoDB compound indexes following ESR rule",
                token_count=10,
                char_length=42,
                metadata={"title": "MongoDB ESR Rule", "category": "MongoDB", "doc_id": "doc_b"}
            ),
        ]

        embeddings = embed_provider.embed_documents([c.text for c in chunks])
        upserted = store.upsert_chunks(chunks, embeddings)
        assert upserted == 2
        assert store.count() == 2

        # Search
        q_vec = embed_provider.embed_query("Pydantic validation in FastAPI")
        hits = store.search(q_vec, limit=2)
        assert len(hits) == 2
        assert hits[0]["score"] > 0
    finally:
        store.close()
