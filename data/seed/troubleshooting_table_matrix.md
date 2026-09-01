# CentriFlow Pro 5000 - Troubleshooting Guide & Fault Matrix
Document ID: DOC-TBL-2024-TSG
Page 1

| Symptom / Fault Code | Possible Cause | Verification Procedure | Corrective Action | Safety / Warning Note |
| :--- | :--- | :--- | :--- | :--- |
| **Motor does not start after overload reset** | Overload Relay OL-1 contacts welded or damaged | Measure resistance across terminals 95-96 on OL-1. Expected: < 0.5 Ω. | Replace thermal overload relay OL-1 (Part # OL-CF5000-B). | Disconnect main 460V power before measuring terminal resistance. |
| **Motor does not start after overload reset** | Stator thermal switches TS1/TS2 open due to high internal heat | Measure continuity across control terminals 13-14 on terminal block TB-2. Expected: Closed (< 1 Ω). | Allow stator cool-down period (20-30 min). Do not force start. | Danger: High stator temperature can cause insulation breakdown if restarted immediately. |
| **Motor does not start after overload reset** | Phase Protection Relay PPR-2 tripped (Phase loss or >2.5% imbalance) | Inspect LED indicator on PPR-2. Red LED indicates phase fault. | Check incoming line fuses F1A/F1B/F1C and supply voltage balance across L1-L2-L3. | Ensure CAT III 1000V rated multimeter for line voltage checks. |
| **Motor does not start after overload reset** | Control circuit fuse F2 blown | Check continuity across fuse F2 (2A 250V fast-acting). | Replace fuse F2 with identical rating (2A fast-acting). | Never bypass fuse F2 with jumper wires. |
| **Excessive motor vibration (> 4.5 mm/s RMS)** | Coupling misalignment or worn DE bearing | Perform laser alignment and inspect bearing housing. | Re-align shaft to < 0.05 mm radial offset or replace DE bearing 6314-C3. | Wear safety glasses and protective gloves. |
| **High bearing temperature (> 95°C)** | Insufficient or contaminated grease | Check lubrication maintenance log and grease condition. | Purge old grease and inject 15g Mobilith SHC 220 grease into DE bearing port. | Do not over-grease. Over-greasing causes churning and overheating. |
| **Motor hums but does not rotate** | Single-phasing or locked impeller | Check 3-phase line current with clamp meter. Check impeller rotation manually (LOTO required). | Clear blockage from pump casing or replace blown supply fuse. | LOTO REQUIRED before turning pump impeller by hand. |
