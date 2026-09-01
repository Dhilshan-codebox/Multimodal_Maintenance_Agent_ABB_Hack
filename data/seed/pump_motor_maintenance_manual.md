# CentriFlow Pro 5000 - Industrial Pump Motor Maintenance Manual

## Document ID: DOC-MAN-2024-CF5K
## Equipment: CentriFlow Pro 5000 Heavy Duty Slurry Pump Motor
## Manufacturer: Apex Dynamics Industrial Systems

---

### Page 1: General Safety & System Overview

#### 1.1 Safety Rules
1. ALWAYS perform Lockout/Tagout (LOTO) prior to opening terminal boxes or performing electrical maintenance.
2. Verify zero electrical potential using a calibrated multimeter rated CAT III 1000V.
3. Wear arc-flash rated PPE (Minimum NFPA 70E Category 2) when working near active control cabinets.

#### 1.2 System Description
The CentriFlow Pro 5000 is a 75 kW (100 HP) 3-phase induction pump motor operating at 460 VAC, 60 Hz. The motor unit drives a heavy-duty centrifugal impeller via a direct flexible coupling.

---

### Page 2: Power and Control Architecture

#### 2.1 Overload Relay (OL-1) Operation
The motor feeder circuit is protected by a bimetallic thermal overload relay (Model: OL-1) integrated into the magnetic starter box.
- Normal Operating Current: 118 A full load current (FLC).
- Overload Trip Threshold: 125% FLC (147.5 A) sustained for > 10 seconds.
- Reset Mechanism: Manual reset button (Blue) located on the front panel of starter cabinet MB-1.

#### 2.2 Post-Trip Lockout Mechanism
When thermal overload relay OL-1 trips, the NC contact 95-96 opens, de-energizing main contactor coil M1.
If the motor fails to start after pressing the manual reset button on OL-1:
1. **Mechanical Lockout Pin / Latched Trip Assembly**: Check if the mechanical trip lockout tab on relay OL-1 has been latched. Certain heavy-duty models require pulling the yellow reset release pin prior to pushing the blue reset button.
2. **Control Circuit Fuse (F2)**: Verify continuity across control circuit fuse F2 (2A 250V fast-acting). A primary coil surge during overload trip can blow F2.
3. **Phase Imbalance / Single-Phasing Guard**: Check line voltage across T1-T2, T2-T3, T1-T3. If phase voltage variance exceeds 2.5%, the downstream Phase Protection Relay (PPR-2) blocks contactor pull-in even after OL-1 reset.
4. **Winding Thermal Switches (TS1/TS2)**: Internal stator thermal switches open at 130°C and reset automatically only after stator temperature drops below 90°C (typical cool-down period: 20 to 30 minutes).

---

### Page 3: Mechanical Coupling and Bearing Maintenance

#### 3.1 Bearing Lubrication
- Drive End (DE) Bearing: 6314-C3 Deep Groove Ball Bearing. Re-grease every 2000 operating hours with Mobilith SHC 220 (15 grams).
- Non-Drive End (NDE) Bearing: 6212-C3 Deep Groove Ball Bearing. Re-grease every 2000 operating hours with Mobilith SHC 220 (10 grams).

#### 3.2 Shaft Alignment Tolerances
- Radial Alignment Max Offset: 0.05 mm (0.002 in).
- Axial Runout Max Variance: 0.03 mm (0.0012 in).
