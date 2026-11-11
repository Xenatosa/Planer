#!/usr/bin/env python3
"""Serial deletion/sufficiency checks for p3d23 family-level IIS groups."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "codex_jobs/tools/p3d23"
RESULTS = TOOLS / "results"
EMPTY = RESULTS / "p3d23_round00_empty_cuts.json"
FAMILIES = [
    "r3_long", "r3_quer", "r3_wob", "crossing_stage", "axis_supports",
    "plane_core", "endpoint_stage", "safety_gitter", "safety_quer",
    "safety_single_quer", "g5", "r5_hole", "r4", "grade_cross", "grade_same",
    "endpoint_r8a", "plane_slope_polygon", "plane_slope_box", "variable_bounds",
    "route_profile_slope", "source_monotone",
]
GEOMETRIES = {
    "V29": ("/tmp/p3d22_v29_source.json.gz", "p3d21_transfer_base_v29.json", (152.7601173875546, 28.07128239088488)),
    "V30": ("/tmp/p3d22_v30_source.json.gz", "p3d21_transfer_base_v30.json", (152.65796405573423, 28.263810474520962)),
    "V3": ("/tmp/p3d22_v3_source.json.gz", "p3d21_transfer_base_route3_v29.json", (152.6292918620858, 28.353590994151514)),
}


def main() -> None:
    EMPTY.write_text("[]\n", encoding="utf-8")
    records = []
    for geometry, (source, base_name, center) in GEOMETRIES.items():
        base = ROOT / "team/art/dorfmap_grundgeruest/relief3d/neu" / base_name
        for trial, groups in (("endpoint_only", ["endpoint_r8a"]),
                              ("all_except_endpoint", [x for x in FAMILIES if x != "endpoint_r8a"])):
            out = RESULTS / f"p3d23_{geometry}_filter_{trial}.json"
            command = [
                sys.executable, str(TOOLS / "run_diagnostic.py"),
                "--geometry", geometry, "--scenario", "joint", "--groups", *groups,
                "--source-relief", source, "--transfer-base", str(base),
                "--r8-center", str(center[0]), str(center[1]),
                "--event-cuts", str(EMPTY), "--out", str(out), "--time-limit", "600",
            ]
            run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            if run.returncode != 0:
                raise RuntimeError(f"{geometry}/{trial}: {run.stderr[-2000:]} {run.stdout[-1000:]}")
            result = json.loads(out.read_text(encoding="utf-8"))
            family_rows = dict(result.get("family_row_counts") or {})
            pair_rows = 2 * int(result.get("route_pair_count", 0))
            same_route_rows = 2 * int(result.get("same_route_pair_count", 0))
            family_rows.pop("route_pair_grade", None)
            family_rows["route_pair_grade_cross_route"] = pair_rows - same_route_rows
            family_rows["route_pair_grade_same_route"] = same_route_rows
            records.append({
                "geometry": geometry, "trial": trial, "enabled_groups": groups,
                "status": result.get("status"), "status_code": result.get("status_code"),
                "primal_feasible": result.get("primal_feasible"),
                "weighted_l1": result.get("weighted_l1_value"),
                "slack_values": result.get("slack_values"),
                "family_row_counts": dict(sorted(family_rows.items())),
                "route_pair_count": result.get("route_pair_count"),
                "same_route_pair_count": result.get("same_route_pair_count"),
                "constraints": result.get("constraints"),
                "variables": result.get("variables"),
                "family_max_relaxation_locations": result.get("family_max_relaxation_locations"),
                "solution_json": str(out),
            })
    summary = {"method": "family deletion filter, tested as sufficient subset and necessary family", "runs": records}
    path = RESULTS / "p3d23_part_a_family_filter.json"
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"out": str(path), "runs": len(records),
                      "statuses": [{"geometry": r["geometry"], "trial": r["trial"],
                                    "status": r["status"], "primal_feasible": r["primal_feasible"]}
                                   for r in records]}, indent=2))


if __name__ == "__main__":
    main()
