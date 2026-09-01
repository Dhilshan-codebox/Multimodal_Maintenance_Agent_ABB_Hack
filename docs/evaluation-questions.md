# Evaluation Questions Summary

The evaluation suite is stored in `evals/evaluation_questions.json` and consists of 12 structured questions (10 positive, 2 negative).

## Overview Matrix

| Question ID | Type | Target Question | Expected Source Document | Expected Page / Region | Expected Confidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EVAL-001** | Positive | Motor does not start after overload reset. What should I check next? | DOC-MAN-2024-CF5K | Page 2, Section 2.2 | HIGH |
| **EVAL-002** | Positive | What resistance across OL-1 terminals 95-96 during normal conditions? | DOC-SOP-2024-OLR | Page 1, Step 4a | HIGH |
| **EVAL-003** | Positive | If Phase Protection Relay (PPR-2) shows RED ALARM LED, what is the cause? | DOC-TBL-2024-TSG | Page 1, Row 3 | HIGH |
| **EVAL-004** | Positive | How long must technician wait for TS1/TS2 stator thermal switches to cool down? | DOC-MAN-2024-CF5K | Page 2, Section 2.2 #4 | HIGH |
| **EVAL-005** | Positive | Which safety components are in series before M1 contactor coil in wiring diagram? | DWG-ELEC-2024-CF5K | Region B and C | HIGH |
| **EVAL-006** | Positive | What is the full load current (FLC) and overload trip threshold setting? | DOC-SPEC-2024-CF5K | Page 1, Sec 1 & 2 | HIGH |
| **EVAL-007** | Positive | What rating and type of fuse is specified for control circuit fuse F2? | DOC-MAN-2024-CF5K | Page 2, Section 2.2 #2 | HIGH |
| **EVAL-008** | Positive | What grease type and quantity for Drive End (DE) bearing, and service interval? | DOC-MAN-2024-CF5K | Page 3, Section 3.1 | HIGH |
| **EVAL-009** | Positive | What maximum radial offset is allowed during shaft alignment? | DOC-MAN-2024-CF5K | Page 3, Section 3.2 | HIGH |
| **EVAL-010** | Positive | What maximum number of consecutive overload resets permitted in 1 hour? | DOC-SOP-2024-OLR | Page 2 | HIGH |
| **EVAL-011** | Negative | How to program Modbus RTU RS-485 address on motor controller? | NONE (Unsupported) | N/A | ZERO |
| **EVAL-012** | Negative | Replacement procedure for hydraulic variable displacement swashplate? | NONE (Unsupported) | N/A | ZERO |

## Safety Warnings Requirements
Every evaluation item specifies safety prerequisites:
- Mandatory Lockout/Tagout (LOTO) on disconnect switch DS-1 before opening panels.
- Zero voltage verification using CAT III 1000V rated multimeters.
- Max 3 resets per hour limit to prevent stator winding burn-out.
