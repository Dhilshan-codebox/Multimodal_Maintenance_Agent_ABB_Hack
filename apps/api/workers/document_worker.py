"""
Background workers module placeholder.
Handles asynchronous document parsing, OCR, and vector indexing tasks.
"""

from ..domain.schemas import Job, JobStatus


def process_document_job(job_id: str) -> Job:
    """Placeholder task for document processing pipeline."""
    return Job(
        job_id=job_id,
        job_type="document_ingestion",
        status=JobStatus.COMPLETED,
        progress_percentage=100.0,
        payload={"message": "Document ingested successfully (Day 1 Skeleton)"},
    )
