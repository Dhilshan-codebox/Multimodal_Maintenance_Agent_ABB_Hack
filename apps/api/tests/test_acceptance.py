"""
Acceptance Tests for Multimodal Maintenance Intelligence Agent (Day 1 Exit Gate)

Validates task requirements:
1. Repository starts successfully / GET /health returns status and demo scenario info.
2. Seed corpus directory exists and contains expected files.
3. Schemas can be imported and instantiated properly.
4. Evaluation questions file exists, is readable, and contains 10 positive + 2 negative questions.
5. Upload API placeholder route exists and accepts file payloads.
"""

import json
from pathlib import Path
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.domain.schemas import (
    Document,
    DocumentType,
    Evidence,
    EvidenceType,
    RetrievalMethod,
    Citation,
    Answer,
)

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "demo_scenario" in data
    assert data["demo_scenario"]["equipment"] == "Industrial Pump Motor (CentriFlow Pro 5000)"
    assert data["demo_scenario"]["failure_mode"] == "Motor does not start after overload reset"
    assert "The motor does not start after overload reset" in data["demo_scenario"]["primary_question"]


def test_seed_corpus_exists_and_populated():
    seed_dir = Path("data/seed")
    assert seed_dir.exists() and seed_dir.is_dir()

    files = [f.name for f in seed_dir.iterdir() if f.is_file()]
    assert len(files) >= 5

    expected_files = [
        "pump_motor_maintenance_manual.md",
        "scanned_overload_reset_procedure.txt",
        "troubleshooting_table_matrix.md",
        "wiring_diagram_schematic.svg",
        "equipment_spec_sheet.md",
    ]
    for exp_file in expected_files:
        assert exp_file in files, f"Missing expected seed corpus file: {exp_file}"


def test_domain_schemas_instantiation():
    doc = Document(
        document_id="DOC-TEST-001",
        title="Test Manual",
        file_path="data/seed/pump_motor_maintenance_manual.md",
        document_type=DocumentType.MANUAL,
        page_count=3,
    )
    assert doc.document_id == "DOC-TEST-001"

    evidence = Evidence(
        evidence_id="EVID-001",
        source_id=doc.document_id,
        page=2,
        evidence_type=EvidenceType.TEXT,
        text="Sample evidence text",
        score=0.92,
        retrieval_method=RetrievalMethod.HYBRID,
    )
    assert evidence.score == 0.92
    assert evidence.retrieval_method == RetrievalMethod.HYBRID

    citation = Citation(
        citation_id="CIT-001",
        evidence_id=evidence.evidence_id,
        document_title=doc.title,
        page=evidence.page,
        snippet="Snippet text",
        confidence=0.92,
    )
    assert citation.confidence == 0.92

    answer = Answer(
        answer_id="ANS-001",
        query="Test query",
        answer_text="Test answer",
        citations=[citation],
        evidences=[evidence],
        confidence_score=0.92,
        is_supported=True,
    )
    assert len(answer.citations) == 1
    assert answer.is_supported is True


def test_evaluations_file_readable_and_structured():
    eval_path = Path("evals/evaluation_questions.json")
    assert eval_path.exists()

    with open(eval_path, "r") as f:
        data = json.load(f)

    assert "scenario" in data
    assert "questions" in data
    questions = data["questions"]
    assert len(questions) == 12

    positives = [q for q in questions if q["type"] == "positive"]
    negatives = [q for q in questions if q["type"] == "negative"]

    assert len(positives) == 10
    assert len(negatives) == 2

    for q in questions:
        assert "id" in q
        assert "type" in q
        assert "question" in q
        assert "expected_answer_summary" in q
        assert "expected_source_document" in q
        assert "expected_page_or_region" in q
        assert "safety_notes" in q
        assert "expected_confidence_level" in q


def test_upload_endpoint_placeholder():
    response = client.post(
        "/api/v1/upload",
        files={"file": ("test_doc.pdf", b"Dummy PDF bytes", "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test_doc.pdf"
    assert data["status"] == "uploaded"


def test_query_endpoint():
    response = client.post(
        "/api/v1/query",
        json={"query": "The motor does not start after overload reset. What should I check next?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer_text" in data
    assert len(data["citations"]) > 0
    assert len(data["evidences"]) > 0
    assert data["is_supported"] is True
