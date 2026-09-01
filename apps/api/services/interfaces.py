"""
Service Interfaces for Multimodal Maintenance Intelligence Agent.
Day 1 Skeleton - Define abstract base classes/interfaces without full implementations.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..domain.schemas import Document, Page, Chunk, Evidence, Answer, Citation


class DocumentParser(ABC):
    """Interface for parsing maintenance documents into pages and sections."""

    @abstractmethod
    def parse_document(self, file_path: str, document_type: str) -> Document:
        """Parse raw file and return Document model with page metadata."""
        pass


class OCRService(ABC):
    """Interface for Optical Character Recognition on scanned PDFs and images."""

    @abstractmethod
    def extract_text_and_regions(self, image_bytes: bytes) -> List[Dict[str, Any]]:
        """Extract text blocks and normalized bounding box regions from document images."""
        pass


class ChunkingService(ABC):
    """Interface for chunking parsed document pages into indexable chunks."""

    @abstractmethod
    def create_chunks(self, document: Document, pages: List[Page]) -> List[Chunk]:
        """Split document pages into granular text/table/diagram chunks."""
        pass


class EmbeddingService(ABC):
    """Interface for generating multimodal embeddings for chunks and queries."""

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Generate vector embedding for text query or chunk."""
        pass

    @abstractmethod
    def embed_image(self, image_bytes: bytes) -> List[float]:
        """Generate vector embedding for visual region or diagram."""
        pass


class KeywordSearchService(ABC):
    """Interface for BM25 / Full-Text keyword search over chunks."""

    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> List[Chunk]:
        """Execute keyword search and return top_k matching chunks."""
        pass


class VectorSearchService(ABC):
    """Interface for dense vector similarity search over embeddings."""

    @abstractmethod
    def search_similar(self, query_embedding: List[float], top_k: int = 5) -> List[Chunk]:
        """Execute dense vector search and return top_k matching chunks."""
        pass


class RetrievalService(ABC):
    """Interface for hybrid retrieval combining keyword and vector methods with evidence scoring."""

    @abstractmethod
    def retrieve_evidences(self, query: str, top_k: int = 5) -> List[Evidence]:
        """Retrieve and rank grounded evidence items matching the technician query."""
        pass


class AnswerService(ABC):
    """Interface for generating grounded answers backed strictly by retrieved evidence."""

    @abstractmethod
    def generate_answer(self, query: str, evidences: List[Evidence]) -> Answer:
        """Synthesize answer with inline citations and safety warnings based on retrieved evidence."""
        pass


class CitationValidator(ABC):
    """Interface for validating page-level and region-level citations against source docs."""

    @abstractmethod
    def validate_citations(self, answer: Answer, evidences: List[Evidence]) -> bool:
        """Verify that all claims in the answer are strictly supported by citations and source regions."""
        pass
