"""
Domain schemas for Multimodal Maintenance Intelligence Agent.
Includes definitions for Document, Page, Chunk, Evidence, Citation, Answer, and Job.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    MANUAL = "manual"
    SCANNED_PDF = "scanned_pdf"
    TROUBLESHOOTING_TABLE = "troubleshooting_table"
    WIRING_DIAGRAM = "wiring_diagram"
    SPEC_SHEET = "spec_sheet"


class EvidenceType(str, Enum):
    TEXT = "text"
    TABLE = "table"
    IMAGE_REGION = "image_region"
    DIAGRAM_SYMBOL = "diagram_symbol"


class RetrievalMethod(str, Enum):
    KEYWORD = "keyword"
    VECTOR = "vector"
    HYBRID = "hybrid"
    GRAPH = "graph"


class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class RegionBoundingBox(BaseModel):
    x_min: float = Field(..., description="Normalized min X coordinate (0.0 - 1.0)")
    y_min: float = Field(..., description="Normalized min Y coordinate (0.0 - 1.0)")
    x_max: float = Field(..., description="Normalized max X coordinate (0.0 - 1.0)")
    y_max: float = Field(..., description="Normalized max Y coordinate (0.0 - 1.0)")
    unit: str = Field(default="normalized", description="Coordinate unit type")


class Document(BaseModel):
    document_id: str
    title: str
    file_path: str
    document_type: DocumentType
    page_count: int = 1
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Page(BaseModel):
    page_id: str
    document_id: str
    page_number: int
    text_content: Optional[str] = None
    image_path: Optional[str] = None
    dimensions: Optional[Dict[str, float]] = None


class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    page_number: int
    text: str
    embedding: Optional[List[float]] = None
    bounding_box: Optional[RegionBoundingBox] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Evidence(BaseModel):
    evidence_id: str
    source_id: str
    page: int
    region: Optional[RegionBoundingBox] = None
    evidence_type: EvidenceType
    text: str
    score: float = Field(ge=0.0, le=1.0)
    retrieval_method: RetrievalMethod


class Citation(BaseModel):
    citation_id: str
    evidence_id: str
    document_title: str
    page: int
    snippet: str
    confidence: float = Field(ge=0.0, le=1.0)


class Answer(BaseModel):
    answer_id: str
    query: str
    answer_text: str
    citations: List[Citation] = Field(default_factory=list)
    evidences: List[Evidence] = Field(default_factory=list)
    confidence_score: float = Field(ge=0.0, le=1.0)
    is_supported: bool = True
    safety_warnings: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Job(BaseModel):
    job_id: str
    job_type: str
    status: JobStatus = JobStatus.PENDING
    progress_percentage: float = 0.0
    error_message: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
