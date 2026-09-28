"""
Qdrant Vector Store Management: Handles collection lifecycle, payload schema indexing,
point upserts, and vector similarity search.
Supports both local embedded persistence and remote Docker/Cloud Qdrant instances.
"""

from typing import List, Dict, Any, Optional
import uuid
from pathlib import Path
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams
from src.ingestion.chunker import Chunk


class QdrantVectorStore:
    def __init__(
        self,
        collection_name: str = "rag_baseline_corpus",
        vector_dim: int = 384,
        storage_path: Optional[str] = None,
        qdrant_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        self.collection_name = collection_name
        self.vector_dim = vector_dim
        self.storage_path = storage_path
        self.qdrant_url = qdrant_url
        self.api_key = api_key

        if self.qdrant_url:
            self.client = QdrantClient(url=self.qdrant_url, api_key=self.api_key or None)
        elif self.storage_path:
            path_obj = Path(self.storage_path)
            path_obj.mkdir(parents=True, exist_ok=True)
            self.client = QdrantClient(path=str(path_obj))
        else:
            self.client = QdrantClient(":memory:")

        self.ensure_collection()

    def ensure_collection(self) -> None:
        """Creates the Qdrant collection if it does not already exist."""
        collections = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in collections:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_dim, distance=Distance.COSINE),
            )
            # Create payload indexes on metadata for rapid filtering
            self._create_payload_indexes()

    def _create_payload_indexes(self) -> None:
        """Indexes key payload attributes for fast pre-filtering (ready for Project 2 ACL)."""
        fields = ["doc_id", "category", "chunk_id", "domain"]
        for field in fields:
            try:
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name=field,
                    field_schema=models.PayloadSchemaType.KEYWORD,
                )
            except Exception:
                pass

    def upsert_chunks(
        self,
        chunks: List[Chunk],
        embeddings: List[List[float]],
        batch_size: int = 64
    ) -> int:
        """Batch upserts chunks with their embeddings and metadata payloads."""
        if len(chunks) != len(embeddings):
            raise ValueError(f"Mismatch: {len(chunks)} chunks vs {len(embeddings)} embeddings")

        total_upserted = 0
        points: List[models.PointStruct] = []

        for chunk, emb in zip(chunks, embeddings):
            # Deterministic UUID5 based on chunk_id namespace
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.chunk_id))
            payload = {
                "chunk_id": chunk.chunk_id,
                "doc_id": chunk.doc_id,
                "chunk_index": chunk.chunk_index,
                "text": chunk.text,
                "token_count": chunk.token_count,
                "char_length": chunk.char_length,
                **chunk.metadata
            }
            points.append(models.PointStruct(id=point_id, vector=emb, payload=payload))

            if len(points) >= batch_size:
                self.client.upsert(collection_name=self.collection_name, points=points)
                total_upserted += len(points)
                points = []

        if points:
            self.client.upsert(collection_name=self.collection_name, points=points)
            total_upserted += len(points)

        return total_upserted

    def search(
        self,
        query_vector: List[float],
        limit: int = 5,
        score_threshold: Optional[float] = None,
        query_filter: Optional[models.Filter] = None
    ) -> List[Dict[str, Any]]:
        """
        Executes approximate nearest neighbor (ANN) vector search.
        Returns list of matched points with similarity score, text, and metadata.
        """
        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            query_filter=query_filter,
            with_payload=True,
            with_vectors=False
        )

        results = []
        for hit in response.points:
            results.append({
                "id": str(hit.id),
                "score": float(hit.score),
                "chunk_id": hit.payload.get("chunk_id", ""),
                "doc_id": hit.payload.get("doc_id", ""),
                "title": hit.payload.get("title", ""),
                "category": hit.payload.get("category", ""),
                "text": hit.payload.get("text", ""),
                "metadata": hit.payload
            })
        return results

    def count(self) -> int:
        """Returns the number of points in the collection."""
        res = self.client.count(collection_name=self.collection_name, exact=True)
        return res.count

    def clear(self) -> None:
        """Deletes and recreates the collection."""
        self.client.delete_collection(collection_name=self.collection_name)
        self.ensure_collection()

    def close(self) -> None:
        """Gracefully closes underlying client connections and locks."""
        try:
            self.client.close()
        except Exception:
            pass
