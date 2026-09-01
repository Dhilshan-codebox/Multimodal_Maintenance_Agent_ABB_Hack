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

app = FastAPI(
    title="Multimodal Maintenance Intelligence Agent API",
    description="Grounded AI assistant for industrial equipment troubleshooting with page and region citations.",
    version="0.1.0",
)

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
    """Placeholder upload endpoint for manual PDFs, schematics, and spec sheets."""
    contents = await file.read()
    return {
        "filename": file.filename,
        "size_bytes": len(contents),
        "status": "uploaded",
        "message": "File received. Processing pipeline placeholder (Day 1 Skeleton).",
    }


@app.post("/api/v1/query", response_model=Answer)
def query_agent(request: QueryRequest):
    """
    Placeholder query endpoint.
    On Day 1, returns a grounded response for the primary demo question or fallback.
    """
    if "overload" in request.query.lower() or "not start" in request.query.lower():
        evidence1 = Evidence(
            evidence_id="EVID-001",
            source_id="DOC-MAN-2024-CF5K",
            page=2,
            evidence_type=EvidenceType.TEXT,
            text="Verify mechanical lockout pin on OL-1, check fuse F2 continuity, inspect Phase Protection Relay PPR-2 for >2.5% phase unbalance.",
            score=0.95,
            retrieval_method=RetrievalMethod.HYBRID,
        )
        citation1 = Citation(
            citation_id="CIT-001",
            evidence_id="EVID-001",
            document_title="CentriFlow Pro 5000 Maintenance Manual",
            page=2,
            snippet="Section 2.2 Post-Trip Lockout Mechanism: Check mechanical trip lockout tab, fuse F2 (2A 250V), and PPR-2 phase balance.",
            confidence=0.95,
        )
        return Answer(
            answer_id="ANS-001",
            query=request.query,
            answer_text="Based on the CentriFlow Pro 5000 Maintenance Manual (Page 2, Section 2.2):\n1. Check if the mechanical trip lockout tab/pin on overload relay OL-1 is latched.\n2. Verify continuity across control circuit fuse F2 (2A 250V).\n3. Check line voltage balance across L1-L2-L3 (PPR-2 relay trips if variance > 2.5%).\n4. Allow 20-30 minutes for stator thermal switches (TS1/TS2) to cool below 90°C.",
            citations=[citation1],
            evidences=[evidence1],
            confidence_score=0.95,
            is_supported=True,
            safety_warnings=[
                "ALWAYS perform Lockout/Tagout (LOTO) prior to opening terminal boxes.",
                "Verify zero electrical potential with CAT III 1000V multimeter.",
            ],
        )

    return Answer(
        answer_id="ANS-UNSUPPORTED",
        query=request.query,
        answer_text="I could not find grounded evidence in the available maintenance manuals to answer this specific question.",
        citations=[],
        evidences=[],
        confidence_score=0.0,
        is_supported=False,
        safety_warnings=[],
    )
