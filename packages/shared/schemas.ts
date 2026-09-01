/**
 * Shared TypeScript definitions for Multimodal Maintenance Intelligence Agent
 */

export enum DocumentType {
  MANUAL = "manual",
  SCANNED_PDF = "scanned_pdf",
  TROUBLESHOOTING_TABLE = "troubleshooting_table",
  WIRING_DIAGRAM = "wiring_diagram",
  SPEC_SHEET = "spec_sheet",
}

export enum EvidenceType {
  TEXT = "text",
  TABLE = "table",
  IMAGE_REGION = "image_region",
  DIAGRAM_SYMBOL = "diagram_symbol",
}

export enum RetrievalMethod {
  KEYWORD = "keyword",
  VECTOR = "vector",
  HYBRID = "hybrid",
  GRAPH = "graph",
}

export enum JobStatus {
  PENDING = "pending",
  PROCESSING = "processing",
  COMPLETED = "completed",
  FAILED = "failed",
}

export interface RegionBoundingBox {
  x_min: number;
  y_min: number;
  x_max: number;
  y_max: number;
  unit?: string;
}

export interface Document {
  document_id: string;
  title: string;
  file_path: string;
  document_type: DocumentType;
  page_count: number;
  metadata?: Record<string, any>;
  created_at: string;
}

export interface Page {
  page_id: string;
  document_id: string;
  page_number: number;
  text_content?: string;
  image_path?: string;
  dimensions?: { width: number; height: number };
}

export interface Chunk {
  chunk_id: string;
  document_id: string;
  page_number: number;
  text: string;
  embedding?: number[];
  bounding_box?: RegionBoundingBox;
  metadata?: Record<string, any>;
}

export interface Evidence {
  evidence_id: string;
  source_id: string;
  page: number;
  region?: RegionBoundingBox;
  evidence_type: EvidenceType;
  text: string;
  score: number;
  retrieval_method: RetrievalMethod;
}

export interface Citation {
  citation_id: string;
  evidence_id: string;
  document_title: string;
  page: number;
  snippet: string;
  confidence: number;
}

export interface Answer {
  answer_id: string;
  query: string;
  answer_text: string;
  citations: Citation[];
  evidences: Evidence[];
  confidence_score: number;
  is_supported: boolean;
  safety_warnings: string[];
  created_at: string;
}

export interface Job {
  job_id: string;
  job_type: string;
  status: JobStatus;
  progress_percentage: number;
  error_message?: string;
  payload?: Record<string, any>;
  created_at: string;
  updated_at: string;
}
