"""
Embedding Providers: Abstraction layer for generating dense semantic vector embeddings.
Default implementation uses FastEmbed (ONNX runtime, local, CPU-optimized, zero cost).
"""

from abc import ABC, abstractmethod
from typing import List
import numpy as np


class BaseEmbeddingProvider(ABC):
    """Abstract base class for all vector embedding providers."""

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generates dense vector embeddings for a list of document strings."""
        pass

    @abstractmethod
    def embed_query(self, query: str) -> List[float]:
        """Generates a dense vector embedding for a single user query."""
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Returns the vector dimensionality."""
        pass


class FastEmbedProvider(BaseEmbeddingProvider):
    """
    FastEmbed implementation using BAAI/bge-small-en-v1.5 or all-MiniLM-L6-v2.
    Runs locally on ONNX runtime with zero GPU or PyTorch requirement.
    """
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5", dimension: int = 384):
        from fastembed import TextEmbedding
        self._model_name = model_name
        self._dimension = dimension
        self._model = TextEmbedding(model_name=model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        embeddings_generator = self._model.embed(texts)
        return [embedding.tolist() for embedding in embeddings_generator]

    def embed_query(self, query: str) -> List[float]:
        # FastEmbed handles single query embedding efficiently
        embeddings = list(self._model.embed([query]))
        return embeddings[0].tolist()

    @property
    def dimension(self) -> int:
        return self._dimension


class MockEmbeddingProvider(BaseEmbeddingProvider):
    """Deterministic mock embedding provider for instant offline unit testing."""
    def __init__(self, dimension: int = 384):
        self._dimension = dimension

    def _hash_to_vec(self, text: str) -> List[float]:
        import hashlib
        h = hashlib.sha256(text.encode("utf-8")).digest()
        # Create deterministic normalized vector
        arr = np.frombuffer(h * ((self._dimension // len(h)) + 1), dtype=np.uint8)[:self._dimension].astype(float)
        norm = np.linalg.norm(arr)
        if norm > 0:
            arr = arr / norm
        return arr.tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._hash_to_vec(t) for t in texts]

    def embed_query(self, query: str) -> List[float]:
        return self._hash_to_vec(query)

    @property
    def dimension(self) -> int:
        return self._dimension


def get_embedding_provider(
    provider_name: str = "fastembed",
    model_name: str = "BAAI/bge-small-en-v1.5",
    dimension: int = 384
) -> BaseEmbeddingProvider:
    """Factory function to resolve and instantiate embedding provider."""
    if provider_name.lower() == "fastembed":
        return FastEmbedProvider(model_name=model_name, dimension=dimension)
    elif provider_name.lower() == "mock":
        return MockEmbeddingProvider(dimension=dimension)
    else:
        # Default to fastembed
        return FastEmbedProvider(model_name=model_name, dimension=dimension)
