# Engineering Validation Log

## 1. RTL Functional Verification

**Design:** 8-bit parameterized synchronous counter.

**Tool:** Icarus Verilog 12.0.

**Tests:** Synchronous reset, enable counting, hold, reset priority, terminal count and wraparound.

**Evidence:** `results/simulation_result.txt`

**Observed result:** 266/266 checks passed.

**Limitation:** Passing directed tests does not prove exhaustive functional correctness.

## 2. Reference EDA Environment

**Baseline:** Official ORFS GCD example.

**Result:** RTL-to-GDSII flow completed.

**Purpose:** Validate the environment before introducing the custom counter.

**Important:** GCD results are not presented as original counter results.

## 3. Initial Counter Implementation Failure

**Configuration:** 30% target core utilization.

**Failure:** PDN-0185, insufficient width for power straps.

**Evidence:** `results/floorplan_30pct.log`

**Observed:**
- Core area: 296.856 µm²
- Effective utilization: 32.6%
- Available width: 17.67 µm
- Required strap width: 28.5 µm

**Hypothesis:** The automatically generated core was too small for the default PDN structure.

## 4. Controlled Experiment

**Changed parameter:** CORE_UTILIZATION from 30 to 5.

**Unchanged:** RTL design and Nangate45 platform.

**Evidence:** `results/floorplan_5pct.log`

**Observed:**
- Core area: 1,896.580 µm²
- Effective utilization: 5.1%
- Final GDSII generated successfully

**Conclusion:** The increased floorplan area allowed the physical flow to proceed beyond the original PDN failure.

**Limitation:** 5% was a feasibility setting, not an optimized target. Other utilization values were not systematically explored.

## 5. Final Implementation Checks

**Evidence:**
- `results/final_timing.rpt`
- `results/detailed_routing.log`
- `results/synth_stat.txt`
- `results/final_layout.gds`

**Observed:**
- Synthesized cells: 46
- Synthesis cell area: 96.824 µm²
- Reported critical path slack: +7.7262 (unit to verify)
- Setup violations: 0
- Hold violations: 0
- Final detailed-routing violations: 0

**Limitation:** These are reports from the open-source implementation flow. They do not establish full commercial signoff.

## 6. Independent Validation Principles

1. Distinguish tool output from assumptions.
2. Verify commands against actual logs and documentation.
3. Do not treat successful GDS generation as proof of timing closure.
4. Record failures and controlled corrective actions.
5. Keep claims proportionate to the evidence.
