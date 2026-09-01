# Day 1 Architectural Decisions & Design Rationale

## Decision 1: Narrow Scenario Selection
- **Choice**: CentriFlow Pro 5000 Industrial Pump Motor — "Motor does not start after overload reset".
- **Rationale**: Provides a realistic, high-impact industrial troubleshooting path involving electromechanical components (bimetallic overload OL-1, phase protection relay PPR-2, control fuse F2, stator thermal switches TS1/TS2). This scenario stresses multimodal document types: narrative text manuals, scanned SOPs, matrix tables, electrical schematics, and spec sheets.

## Decision 2: Schema First Architecture with Evidence Primacy
- **Choice**: Defined Pydantic and TypeScript domain models upfront before service implementation.
- **Rationale**: Ensures that every downstream retrieval and generation service adheres to the core requirement: every answer must be constructed from scored, cited evidence containing `evidence_id`, `source_id`, `page`, `region`, `evidence_type`, `text`, `score`, and `retrieval_method`.

## Decision 3: Abstract Service Interfaces
- **Choice**: Introduced `DocumentParser`, `OCRService`, `ChunkingService`, `EmbeddingService`, `KeywordSearchService`, `VectorSearchService`, `RetrievalService`, `AnswerService`, and `CitationValidator` as Python Abstract Base Classes (`ABC`).
- **Rationale**: Keeps the Day 1 project runnable without binding prematurely to heavy external OCR models, vector database instances, or LLM providers.

## Decision 4: Seed Corpus Composition
- **Choice**: Provided 5 distinct document types in `data/seed/`:
  1. `pump_motor_maintenance_manual.md`: Text-based maintenance manual.
  2. `scanned_overload_reset_procedure.txt`: Scanned PDF OCR procedure format.
  3. `troubleshooting_table_matrix.md`: Structured markdown table matrix.
  4. `wiring_diagram_schematic.svg`: Scalable electrical schematic with defined diagnostic regions (Region A through Region D).
  5. `equipment_spec_sheet.md`: Equipment technical specification document.

## Decision 5: Verified Evaluation Suite
- **Choice**: Created `evals/evaluation_questions.json` containing 10 positive answerable questions and 2 negative unsupported questions.
- **Rationale**: Establishes a concrete benchmark for accuracy, citation provenance, and safety warning verification. Negative questions verify that the agent correctly refuses to hallucinate answers for out-of-scope queries (e.g. Modbus RTU configuration or hydraulic swashplates).
