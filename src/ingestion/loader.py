"""
Document Loader: Scans and parses markdown files from the raw corpus directory.
Extracts metadata (Doc ID, Category, Title, Domain, Summary) and text contents.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import re
from pydantic import BaseModel, Field


class Document(BaseModel):
    doc_id: str
    title: str
    category: str
    domain: str
    summary: str
    content: str
    filepath: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DocumentLoader:
    def __init__(self, raw_data_dir: Path):
        self.raw_data_dir = Path(raw_data_dir)

    def load_file(self, filepath: Path) -> Document:
        """Parses a single markdown document and extracts structured headers and body."""
        text = filepath.read_text(encoding="utf-8")
        
        # Default fallbacks
        doc_id = filepath.stem
        title = filepath.stem.replace("_", " ").title()
        category = filepath.parent.name
        domain = "General Technical Documentation"
        summary = ""

        # Extract title from first markdown header
        title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()

        # Extract metadata fields
        doc_id_match = re.search(r"\*\*Doc ID:\*\*\s+`([^`]+)`", text)
        if doc_id_match:
            doc_id = doc_id_match.group(1).strip()

        cat_match = re.search(r"\*\*Category:\*\*\s+`([^`]+)`", text)
        if cat_match:
            category = cat_match.group(1).strip()

        domain_match = re.search(r"\*\*Domain:\*\*\s+`([^`]+)`", text)
        if domain_match:
            domain = domain_match.group(1).strip()

        summary_match = re.search(r"\*\*Summary:\*\*\s+(.+)$", text, re.MULTILINE)
        if summary_match:
            summary = summary_match.group(1).strip()

        # Clean body text (remove the metadata header block for pure ingestion)
        body_parts = text.split("---", 1)
        content_body = body_parts[1].strip() if len(body_parts) > 1 else text.strip()

        return Document(
            doc_id=doc_id,
            title=title,
            category=category,
            domain=domain,
            summary=summary,
            content=content_body,
            filepath=str(filepath.resolve()),
            metadata={
                "source_file": filepath.name,
                "category": category,
                "domain": domain,
                "title": title
            }
        )

    def load_all(self) -> List[Document]:
        """Recursively scans raw_data_dir for all .md files and returns parsed documents."""
        if not self.raw_data_dir.exists():
            raise FileNotFoundError(f"Raw data directory does not exist: {self.raw_data_dir}")

        md_files = sorted(list(self.raw_data_dir.rglob("*.md")))
        documents = [self.load_file(f) for f in md_files]
        return documents
