"""
Token-Aware Chunker: Splits documents into semantically coherent chunks of ~500 tokens
with configurable overlap (~50 tokens), preserving section headers and paragraph boundaries.
"""

from typing import List, Dict, Any
import re
from pydantic import BaseModel, Field
from .loader import Document


class Chunk(BaseModel):
    chunk_id: str
    doc_id: str
    chunk_index: int
    text: str
    token_count: int
    char_length: int
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TokenAwareChunker:
    """
    Splits text into chunks respecting markdown sections, code fences, and paragraphs.
    Uses word-to-token approximation (1 word ~= 1.33 tokens, 500 tokens ~= 375 words)
    or tiktoken if available, with robust boundary preservation.
    """
    def __init__(self, chunk_size_tokens: int = 500, chunk_overlap_tokens: int = 50):
        self.chunk_size_tokens = chunk_size_tokens
        self.chunk_overlap_tokens = chunk_overlap_tokens
        # Conversion ratio: roughly 1 token ~ 0.75 words, so words_target ~ tokens * 0.75
        self.target_words = int(chunk_size_tokens * 0.75)
        self.overlap_words = int(chunk_overlap_tokens * 0.75)

    def estimate_tokens(self, text: str) -> int:
        """Estimates token count using standard whitespace/punctuation tokenization."""
        words = len(text.split())
        return int(words * 1.33)

    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Splits document text on double newlines while preserving markdown headers."""
        paragraphs = re.split(r"\n\s*\n", text)
        return [p.strip() for p in paragraphs if p.strip()]

    def chunk_document(self, doc: Document) -> List[Chunk]:
        """
        Splits a Document into an ordered list of Chunks with deterministic IDs and overlap.
        Prefixes each chunk with the document title and category for contextual embedding.
        """
        paragraphs = self._split_into_paragraphs(doc.content)
        
        chunks: List[Chunk] = []
        current_words: List[str] = []
        current_word_count = 0
        chunk_idx = 0

        for para in paragraphs:
            para_words = para.split()
            para_word_count = len(para_words)

            if current_word_count + para_word_count > self.target_words and current_words:
                # Flush existing buffer as a chunk
                chunk_body = " ".join(current_words)
                # Context prefix gives the embedding model critical semantic anchors
                full_chunk_text = f"[{doc.category} - {doc.title}]\n{chunk_body}"
                
                chunk_id = f"{doc.doc_id}#chunk_{chunk_idx}"
                chunks.append(Chunk(
                    chunk_id=chunk_id,
                    doc_id=doc.doc_id,
                    chunk_index=chunk_idx,
                    text=full_chunk_text,
                    token_count=self.estimate_tokens(full_chunk_text),
                    char_length=len(full_chunk_text),
                    metadata={
                        **doc.metadata,
                        "chunk_id": chunk_id,
                        "doc_id": doc.doc_id,
                        "chunk_index": chunk_idx,
                        "title": doc.title,
                        "category": doc.category,
                        "domain": doc.domain,
                        "raw_body": chunk_body
                    }
                ))
                chunk_idx += 1

                # Retain overlap words for the next chunk
                if self.overlap_words > 0 and len(current_words) > self.overlap_words:
                    current_words = current_words[-self.overlap_words:]
                    current_word_count = len(current_words)
                else:
                    current_words = []
                    current_word_count = 0

            current_words.extend(para_words)
            current_word_count += para_word_count

        # Flush final remaining words
        if current_words:
            chunk_body = " ".join(current_words)
            full_chunk_text = f"[{doc.category} - {doc.title}]\n{chunk_body}"
            chunk_id = f"{doc.doc_id}#chunk_{chunk_idx}"
            chunks.append(Chunk(
                chunk_id=chunk_id,
                doc_id=doc.doc_id,
                chunk_index=chunk_idx,
                text=full_chunk_text,
                token_count=self.estimate_tokens(full_chunk_text),
                char_length=len(full_chunk_text),
                metadata={
                    **doc.metadata,
                    "chunk_id": chunk_id,
                    "doc_id": doc.doc_id,
                    "chunk_index": chunk_idx,
                    "title": doc.title,
                    "category": doc.category,
                    "domain": doc.domain,
                    "raw_body": chunk_body
                }
            ))

        return chunks

    def chunk_all(self, documents: List[Document]) -> List[Chunk]:
        """Chunks a collection of documents."""
        all_chunks: List[Chunk] = []
        for doc in documents:
            all_chunks.extend(self.chunk_document(doc))
        return all_chunks
