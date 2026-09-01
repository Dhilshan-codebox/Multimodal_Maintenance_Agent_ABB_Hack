# Multimodal Maintenance Intelligence Agent

An AI assistant built to help industrial technicians troubleshoot equipment using manuals, scanned PDFs, tables, images, wiring diagrams, and engineering drawings.

---

## Selected Demo Scenario
- **Equipment Family**: Industrial Pump Motor (CentriFlow Pro 5000 / 75 kW 3-Phase Induction Motor)
- **Failure Mode**: Motor does not start after overload reset
- **Primary Technician Question**:
  > *"The motor does not start after overload reset. What should I check next?"*

---

## Directory Structure
```text
.
├── apps/
│   ├── api/                  # FastAPI backend service
│   │   ├── domain/           # Data domain models and schemas (Document, Chunk, Evidence, Citation, etc.)
│   │   ├── services/         # Service interfaces (DocumentParser, OCRService, RetrievalService, etc.)
│   │   ├── workers/          # Background task workers placeholder
│   │   └── main.py           # FastAPI entrypoint
│   └── web/                  # React + Vite frontend application
│       ├── src/              # React components & UI logic
│       └── package.json
├── packages/
│   └── shared/               # Shared TypeScript schemas (schemas.ts)
├── data/
│   └── seed/                 # Seed corpus files (Manual, Scanned SOP, Table Matrix, Wiring Diagram, Spec Sheet)
├── evals/
│   └── evaluation_questions.json # Verified 10 positive + 2 negative question evaluation set
├── infra/                    # Dockerfiles for API and Web services
├── docs/                     # Project scope, architecture, decisions, and evaluation documentation
├── docker-compose.yml        # Multi-container local orchestration
└── requirements.txt          # Python dependencies
```

---

## Quick Start Instructions

### Prerequisites
- Python 3.12+
- Node.js v20+ / npm 10+
- Docker & Docker Compose (Optional)

---

### Running Locally without Docker

#### 1. Start the FastAPI Backend
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
```
Backend Health Check Endpoint: `http://localhost:8000/health`

#### 2. Start the React Frontend
In a separate terminal:
```bash
cd apps/web
npm install
npm run dev
```
Frontend URL: `http://localhost:3000`

---

### Running with Docker Compose

```bash
# Build and start services
docker-compose up --build
```
- Web Application: `http://localhost:3000`
- API Health Check: `http://localhost:8000/health`

---

## Running Tests

Execute acceptance test suite:
```bash
pytest apps/api/tests/ -v
```

---

## Day 1 Documentation
- [`docs/project-scope.md`](docs/project-scope.md): Project objectives and scope boundaries.
- [`docs/architecture-overview.md`](docs/architecture-overview.md): System design diagram and component layers.
- [`docs/day-1-decisions.md`](docs/day-1-decisions.md): Architecture decisions and rationale.
- [`docs/evaluation-questions.md`](docs/evaluation-questions.md): Benchmark questions and target citations.
