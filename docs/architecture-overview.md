# Architecture Overview

```
+---------------------------------------------------------------------------------+
|                                 REACT WEB UI                                    |
|   - Health & Scenario Dashboard                                                 |
|   - Document Upload & Ingestion Dropzone                                       |
|   - Grounded Troubleshooting Assistant Console with Citations                    |
|   - Evaluation Set Inspector                                                   |
+---------------------------------------------------------------------------------+
                                       |
                                       | HTTP / REST API
                                       v
+---------------------------------------------------------------------------------+
|                                FASTAPI BACKEND                                  |
|                                                                                 |
|  Endpoints:                                                                     |
|    - GET  /health                   - GET  /api/v1/seed-corpus                  |
|    - GET  /api/v1/evaluations       - POST /api/v1/upload                       |
|    - POST /api/v1/query                                                         |
|                                                                                 |
|  +---------------------------------------------------------------------------+  |
|  |                              DOMAIN MODELS                                |  |
|  |  Document, Page, Chunk, Evidence, Citation, Answer, Job, BoundingBox        |  |
|  +---------------------------------------------------------------------------+  |
|                                                                                 |
|  +---------------------------------------------------------------------------+  |
|  |                            SERVICE INTERFACES                             |  |
|  |  - DocumentParser        - OCRService           - ChunkingService         |  |
|  |  - EmbeddingService      - KeywordSearchService - VectorSearchService     |  |
|  |  - RetrievalService      - AnswerService        - CitationValidator       |  |
|  +---------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------+
                                       |
                                       v
+---------------------------------------------------------------------------------+
|                          SEED CORPUS & EVALS DATA                               |
|                                                                                 |
|  data/seed/                                                                     |
|    ├── pump_motor_maintenance_manual.md        (Text Maintenance Manual)       |
|    ├── scanned_overload_reset_procedure.txt    (Scanned Procedure OCR)         |
|    ├── troubleshooting_table_matrix.md         (Troubleshooting Matrix)        |
|    ├── wiring_diagram_schematic.svg            (Electrical Schematic Drawing)  |
|    └── equipment_spec_sheet.md                 (Technical Spec Sheet)          |
|                                                                                 |
|  evals/                                                                         |
|    └── evaluation_questions.json               (10 Positive + 2 Negative)      |
+---------------------------------------------------------------------------------+
```

## System Layers

### 1. Presentation Layer (`apps/web`)
A modern React / Vite single-page application providing a clean UI for technicians:
- Real-time backend status checking via `/health`.
- Interactive file upload interface for manual PDF/schematic uploads.
- Troubleshooting query console displaying answers alongside citation badges and safety warnings.
- Inspection view for seed documents and evaluation questions.

### 2. Application API Layer (`apps/api`)
Built with FastAPI and Python 3.12:
- Exposes structured REST endpoints.
- Uses Pydantic v2 domain models enforcing the evidence schema (`evidence_id`, `source_id`, `page`, `region`, `evidence_type`, `text`, `score`, `retrieval_method`).
- Defines abstract service interfaces to guide Day 2 implementation.

### 3. Data & Evaluation Layer (`data/seed`, `evals`)
- Stores domain seed corpus covering all required document formats.
- Houses verified evaluation suite with 10 positive answerable questions and 2 negative unsupported queries.
