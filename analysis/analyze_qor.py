
from pathlib import Path
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "results"
OUTPUT = ROOT / "analysis"

def read(name):
    return (REPORTS / name).read_text(encoding="utf-8", errors="replace")

def metric(text, pattern, label):
    match = re.search(pattern, text, re.I | re.M)
    if not match:
        raise ValueError(f"Missing metric: {label}")
    return float(match.group(1))

def floorplan(name):
    content = read(name)
    area = metric(
        content, r"\[INFO IFP-0102\]\s*Core area:\s*([\d.]+)",
        "Core area"
    )
    util = metric(
        content, r"\[INFO IFP-0104\]\s*Effective utilization:\s*([\d.]+)",
        "Utilization"
    )
    return area, round(util * 100, 2)

base_area, base_util = floorplan("floorplan_30pct.log")
final_area, final_util = floorplan("floorplan_5pct.log")

synth = read("synth_stat.txt")
timing = read("final_timing.rpt")
routing = read("detailed_routing.log")
simulation = read("simulation_result.txt")

cells = int(metric(
    synth, r"^\s*(\d+)\s+[\d.]+\s+\d+\s+[\d.]+\s+cells\s*$",
    "Synthesized cells"
))

cell_area = metric(
    synth, r"Chip area for module.*?:\s*([\d.]+)",
    "Synthesis cell area"
)

slack = metric(
    timing, r"worst slack max\s+(-?[\d.]+)",
    "Worst max-delay slack"
)

setup = int(metric(
    timing, r"setup violation count\s+(\d+)",
    "Setup violations"
))
hold = int(metric(
    timing, r"hold violation count\s+(\d+)",
    "Hold violations"
))

violations = re.findall(
    r"\[INFO DRT-0199\]\s*Number of violations\s*=\s*(\d+)",
    routing
)
if not violations:
    raise ValueError("Routing violation data not found")
final_drc = int(violations[-1])

passed_checks = int(metric(
    simulation, r"ALL TESTS PASSED\s*\((\d+)\s+checks\)",
    "Functional verification"
))

# Only the successful variant has final implementation metrics.
rows = [
    {
        "variant": "base_30pct",
        "core_area_um2": base_area,
        "utilization_pct": base_util,
        "synth_cells": "",
        "synth_area_um2": "",
        "worst_slack_ns": "",
        "setup_violations": "",
        "hold_violations": "",
        "routing_violations": ""
    },
    {
        "variant": "pdnfix_5pct",
        "core_area_um2": final_area,
        "utilization_pct": final_util,
        "synth_cells": cells,
        "synth_area_um2": cell_area,
        "worst_slack_ns": slack,
        "setup_violations": setup,
        "hold_violations": hold,
        "routing_violations": final_drc
    }
]

with (OUTPUT / "qor_summary.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

checks = {
    "Simulation checks passed": passed_checks == 266,
    "Synthesized cell count matches verified baseline": cells == 46,
    "Synthesis area matches verified baseline": abs(cell_area - 96.824) < 0.001,
    "Core area increased": final_area > base_area,
    "Worst max-delay slack is nonnegative": slack >= 0,
    "No setup violations": setup == 0,
    "No hold violations": hold == 0,
    "Final routing violations zero": final_drc == 0,
    "Final GDS file exists": (REPORTS / "final_layout.gds").is_file()
}

with (OUTPUT / "validation_checks.txt").open("w") as f:
    for label, passed in checks.items():
        line = f"{'PASS' if passed else 'FAIL'} | {label}"
        print(line)
        f.write(line + "\n")

print(f"\nResults: {OUTPUT / 'qor_summary.csv'}")
print(f"Checks passed: {sum(checks.values())}/{len(checks)}")

if not all(checks.values()):
    raise SystemExit(1)

