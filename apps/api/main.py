"""
FastAPI Backend Main Application
Multimodal Maintenance Intelligence Agent
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .domain.schemas import (
    Document,
    DocumentType,
    Answer,
    Evidence,
    Citation,
    EvidenceType,
    RetrievalMethod,
)
from .services.ingestion import ingestion_service
from .services.retrieval import GroundedRetrievalService
from .services.answer import GroundedAnswerService

retrieval_service = GroundedRetrievalService()
answer_service = GroundedAnswerService()

app = FastAPI(
    title="Multimodal Maintenance Intelligence Agent API",
    description="Grounded AI assistant for industrial equipment troubleshooting with page and region citations.",
    version="0.1.0",
)

@app.on_event("startup")
def startup_event():
    ingestion_service.ingest_seed_corpus()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    demo_scenario: Dict[str, str]


class QueryRequest(BaseModel):
    query: str


@app.get("/health", response_model=HealthResponse)
def get_health():
    return HealthResponse(
        status="ok",
        service="multimodal-maintenance-agent-api",
        version="0.1.0",
        demo_scenario={
            "equipment": "Industrial Pump Motor (CentriFlow Pro 5000)",
            "failure_mode": "Motor does not start after overload reset",
            "primary_question": "The motor does not start after overload reset. What should I check next?",
        },
    )


@app.get("/api/v1/seed-corpus")
def get_seed_corpus():
    seed_dir = Path("data/seed")
    if not seed_dir.exists():
        return {"files": []}
    files = [f.name for f in seed_dir.iterdir() if f.is_file()]
    return {"seed_directory": str(seed_dir.resolve()), "files": files}


@app.get("/api/v1/evaluations")
def get_evaluations():
    eval_file = Path("evals/evaluation_questions.json")
    if not eval_file.exists():
        raise HTTPException(status_code=404, detail="Evaluation file not found")
    with open(eval_file, "r") as f:
        data = json.load(f)
    return data


@app.post("/api/v1/upload", response_model=Dict[str, Any])
async def upload_document(file: UploadFile = File(...)):
    """Upload endpoint that ingests document into corpus index."""
    contents = await file.read()
    temp_path = Path("data/seed") / file.filename
    with open(temp_path, "wb") as f:
        f.write(contents)

    doc = ingestion_service.ingest_file(str(temp_path))
    return {
        "document_id": doc.document_id,
        "filename": file.filename,
        "size_bytes": len(contents),
        "status": "ingested",
        "page_count": doc.page_count,
        "message": f"Successfully ingested {file.filename} into active corpus index.",
    }


@app.post("/api/v1/query", response_model=Answer)
def query_agent(request: QueryRequest):
    """
    Grounded query endpoint using pipeline retrieval and evidence synthesis.
    """
    if not ingestion_service.get_all_chunks():
        ingestion_service.ingest_seed_corpus()

    evidences = retrieval_service.retrieve_evidences(request.query, top_k=5)
    answer = answer_service.generate_answer(request.query, evidences)
    return answer
