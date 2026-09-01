"""
Corpus Ingestion Pipeline Service for Multimodal Maintenance Intelligence Agent.
Stores and indexes extracted document chunks for retrieval.
"""

from pathlib import Path
from typing import List, Dict, Optional
from ..domain.schemas import Document, Page, Chunk
from .parser import SimpleDocumentParser


class IngestionService:
    """Manages document ingestion pipeline and maintains active corpus index."""

    def __init__(self, seed_dir: str = "data/seed"):
        self.seed_dir = Path(seed_dir)
        self.parser = SimpleDocumentParser()
        self.documents: Dict[str, Document] = {}
        self.pages: List[Page] = []
        self.chunks: List[Chunk] = []

    def ingest_seed_corpus(self) -> int:
        """Scan seed corpus directory and ingest all documents."""
        self.documents.clear()
        self.pages.clear()
        self.chunks.clear()

        if not self.seed_dir.exists():
            return 0

        count = 0
        for entry in self.seed_dir.iterdir():
            if entry.is_file() and not entry.name.startswith("."):
                self.ingest_file(str(entry))
                count += 1
        return count

    def ingest_file(self, file_path: str) -> Document:
        """Parse single file and append to active corpus index."""
        doc, pages, chunks = self.parser.parse_file(file_path)
        self.documents[doc.document_id] = doc
        self.pages.extend(pages)
        self.chunks.extend(chunks)
        return doc

    def get_all_chunks(self) -> List[Chunk]:
        return self.chunks

    def get_document(self, doc_id: str) -> Optional[Document]:
        return self.documents.get(doc_id)


# Global singleton instance for Day 1 ingestion index
ingestion_service = IngestionService()
