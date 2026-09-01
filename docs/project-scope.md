# Project Scope & Objectives

## Mission Statement
The Multimodal Maintenance Intelligence Agent is a grounded AI assistant engineered to help industrial field technicians troubleshoot complex equipment. The system ingests and synthesizes heterogeneous technical manuals, scanned PDF procedures, diagnostic tables, single-line/wiring diagrams, and technical specification sheets.

## Core Mandate: Grounded Evidence & Citation Provenance
1. **Zero Hallucination Tolerance**: Every claim, diagnostic step, or technical measurement provided to the technician MUST be strictly backed by explicit evidence retrieved from official equipment documentation.
2. **Granular Citations**: Answers must cite source document titles, page numbers, and bounding-box coordinates for diagram symbols or table regions.
3. **Safety First**: Safety warnings, NFPA 70E PPE recommendations, and Lockout/Tagout (LOTO) requirements are dynamically attached whenever electrical or mechanical procedures are queried.

## Selected Demo Scenario
- **Equipment Family**: Industrial Pump Motor (CentriFlow Pro 5000 / 75 kW 3-Phase Induction Motor)
- **Failure Mode**: Motor does not start after overload reset
- **Primary Technician Question**:
  > "The motor does not start after overload reset. What should I check next?"

## Day 1 Non-Goals & Scope Limits
The following enterprise capabilities are deliberately excluded from Day 1 scope to maintain high delivery speed:
- Live IoT telemetry streaming / SCADA integrations
- Computerized Maintenance Management System (CMMS) work order integration
- User authentication, role-based access control (RBAC), and enterprise permissions
- Model fine-tuning or custom LLM training
- Live Neo4j graph database cluster setup
- Automated CAD / DXF parsing
- Commercial billing and multi-tenant metering
