# Clock Constraint Sensitivity Experiment

**Design:** 8-bit Configurable Counter  
**Platform:** Nangate45 (OpenROAD Flow Scripts)  
**Objective:** Evaluate the effect of tightening the clock period from 10 ns to 2 ns on timing closure and physical implementation characteristics.

## 1. Hypothesis

Reducing the clock period is expected to decrease timing slack and may trigger setup violations. The stricter constraint may also influence cell sizing, buffering, and final implementation area.

## 2. Experimental Setup

The experiment used the same RTL, technology platform, core utilization target (5%), placement density (0.60), and external I/O delays (2 ns).

Only the SDC clock period was changed, from 10 ns to 2 ns. The two implementation runs used separate output variants (`pdnfix` and `clock2ns`).

Both runs completed the RTL-to-GDSII flow.

## 3. Measured Results

| Metric | 10 ns Baseline | 2 ns Experiment |
|---|---:|---:|
| Target clock period | 10 ns | 2 ns |
| Worst max-delay slack | +7.73 ns | -0.26 ns |
| Total negative slack | 0.00 ns | -2.55 ns |
| Setup violations | 0 | 17 |
| Hold violations | 0 | 0 |
| Inspected register-to-register setup slack | +9.67 ns | +1.61 ns |
| Synthesis cell area | 96.824 µm² | 96.824 µm² |
| Core area | 1,896.580 µm² | 1,896.580 µm² |
| Final CORE-type instance count | 55 | 68 |
| Final CORE-type instance area | 102.942 µm² | 156.674 µm² |
| Final filler instance count | 307 | 313 |
| Final well-tap instance count | 62 | 62 |
| Final detailed-routing violations | 0 | 0 |
| Final GDSII generated | Yes | Yes |

*The CORE-type instance area increased by approximately 52.2%. This is not a 52.2% increase in total core area.*

## 4. Timing Path Investigation

The 2 ns run reported a worst max-delay slack of approximately -0.26 ns.

**Worst reported path:**
- Startpoint: `count[3]` flip-flop
- Endpoint: `terminal_count` output
- Data arrival time: approximately 0.26 ns
- Data required time: 0.00 ns

The SDC specifies a 2 ns clock period and a 2 ns external output delay. Under these constraints, the nominal time budget remaining for the register-to-output path is zero.

The inspected register-to-register path from `count[1]` to `count[6]` still met setup timing, with approximately +1.61 ns slack.

This demonstrates the importance of identifying the timing path type before attributing a violation to the internal sequential logic.

## 5. Physical Implementation Analysis

Although the synthesized cell area remained unchanged, the final OpenDB implementation showed:

- CORE-type instances increased from 55 to 68.
- CORE-type instance area increased from 102.942 µm² to 156.674 µm².
- Filler area decreased while total core area remained constant.

The results are consistent with changes to the physical implementation under tighter timing constraints. However, the instance classification alone does not establish which additions were caused specifically by timing repair or cell resizing.

Both implementations reported zero final detailed-routing violations.

## 6. Engineering Findings

1. Completing RTL-to-GDSII does not necessarily mean timing closure has been achieved.
2. The worst 2 ns timing violation occurred on a register-to-output path, while the inspected register-to-register path met setup timing.
3. More aggressive timing constraints were associated with increased final CORE-type instance area, without achieving timing closure.
4. Timing reports must be interpreted alongside SDC constraints and path-specific evidence.

## 7. Limitations

- The design is a small educational counter using the open Nangate45 platform.
- The fixed 2 ns I/O delay is an experimental assumption, not a product-level interface requirement.
- The results do not establish the maximum achievable operating frequency of a production chip.
- Only two clock-period configurations were compared.
- The experiment does not constitute full industrial physical-design signoff or systematic PPA optimization.


**Conclusion:** This experiment illustrates how timing constraints can affect reported timing feasibility and implementation characteristics, and demonstrates the value of examining specific timing paths rather than relying solely on flow completion or summary metrics.
