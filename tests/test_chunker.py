"""
Unit tests for DocumentLoader and TokenAwareChunker.
"""

from pathlib import Path
from src.ingestion.loader import Document, DocumentLoader
from src.ingestion.chunker import TokenAwareChunker, Chunk


def test_document_loader(tmp_path: Path):
    doc_path = tmp_path / "test_doc.md"
    doc_path.write_text(
        "# Test Document Title\n\n"
        "**Doc ID:** `test_doc_001`\n"
        "**Category:** `FastAPI`\n"
        "**Domain:** `Web APIs`\n"
        "**Summary:** Test summary text.\n\n"
        "---\n\n"
        "This is paragraph one explaining FastAPI endpoints.\n\n"
        "This is paragraph two providing additional context.\n",
        encoding="utf-8"
    )

    loader = DocumentLoader(tmp_path)
    docs = loader.load_all()
    assert len(docs) == 1
    doc = docs[0]
    assert doc.doc_id == "test_doc_001"
    assert doc.category == "FastAPI"
    assert "Test Document Title" in doc.title
    assert "paragraph one" in doc.content


def test_token_aware_chunker():
    doc = Document(
        doc_id="test_doc_002",
        title="Scaling Scikit-Learn",
        category="Scikit-Learn",
        domain="Machine Learning",
        summary="A summary on scaling",
        content="Short introductory paragraph.\n\n" + "word " * 600,
        filepath="/fake/path.md",
        metadata={"category": "Scikit-Learn"}
    )

    chunker = TokenAwareChunker(chunk_size_tokens=200, chunk_overlap_tokens=30)
    chunks = chunker.chunk_document(doc)

    assert len(chunks) >= 2
    assert chunks[0].chunk_id == "test_doc_002#chunk_0"
    assert chunks[1].chunk_id == "test_doc_002#chunk_1"
    assert "[Scikit-Learn - Scaling Scikit-Learn]" in chunks[0].text
    assert chunks[0].token_count > 0
