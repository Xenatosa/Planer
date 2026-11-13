#!/usr/bin/env python3
"""Serial LP family deletion filter for a p3d29 infeasibility report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "codex_jobs/tools/p3d29"
RESULTS = TOOLS / "results"
RUNNER = TOOLS / "run_diagnostic.py"
SOURCE_DEFAULT = Path("/tmp/p3d22_v3_source.json.gz")
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
TRANSFER = RELIEF3D / "neu/p3d21_transfer_base_route3_v29.json"
CUTS = RESULTS / "p3d29_V3_R00_cuts.json"
GROUPS = (
    "r3_long", "r3_quer", "r3_wob", "crossing_stage", "axis_supports",
    "plane_core", "endpoint_stage", "safety_gitter", "safety_quer",
    "safety_single_quer", "g5", "r5_hole", "r8b", "r4",
    "grade_cross", "grade_same", "endpoint_r8a", "plane_slope_polygon",
    "plane_slope_box", "variable_bounds", "route_profile_slope", "source_monotone",
    "g11", "p3d29_locality", "p3d29_drainage", "p3d29_cliff_form",
    "p3d29_tree_ground",
)


def run(groups: list[str], source: Path, name: str) -> dict:
    output = RESULTS / f"p3d29_V3_lp_{name}.json"
    command = [
        sys.executable, str(RUNNER), "--geometry", "V3", "--scenario", "joint",
        "--source-relief", str(source), "--transfer-base", str(TRANSFER),
        "--r8-center", "152.6292918620858", "28.353590994151514",
        "--event-cuts", str(CUTS), "--out", str(output),
        "--time-limit", "600", "--objective-mode", "diagnostic",
        "--relax-integrality", "--groups", *groups,
    ]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(f"LP group solve {name} failed: {completed.stderr[-1500:]} {completed.stdout[-1000:]}")
    result = json.loads(output.read_text(encoding="utf-8"))
    result["filter_groups_enabled"] = groups
    result["filter_model_json"] = str(output.relative_to(ROOT))
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-relief", type=Path, default=SOURCE_DEFAULT)
    args = ap.parse_args()
    RESULTS.mkdir(parents=True, exist_ok=True)
    all_open = run(list(GROUPS), args.source_relief, "all_open")
    positive = sorted(
        name.removesuffix("_extra_m").removesuffix("_extra_hits").removesuffix("_extra_pp")
        for name, value in all_open.get("normalized_slack_values", {}).items()
        if float(value) > 1e-7
    )
    # Map the actual slack variable prefixes back to diagnostic group names.
    slack_to_group = {
        "p3d29_locality": "p3d29_locality", "p3d29_drainage": "p3d29_drainage",
        "p3d29_cliff_form": "p3d29_cliff_form", "p3d29_tree_ground": "p3d29_tree_ground",
        "r3_long": "r3_long", "r3_quer": "r3_quer", "r3_wob": "r3_wob",
        "crossing_stage": "crossing_stage", "axis_tolerance": "axis_supports",
        "plane_tolerance": "plane_core", "endpoint_stage": "endpoint_stage",
        "safety_gitter": "safety_gitter", "safety_quer": "safety_quer",
        "safety_single_quer": "safety_single_quer", "g5_total": "g5", "g5_d1": "g5",
        "r5_total": "r5_hole", "r5_d1": "r5_hole", "r8b_d1": "r8b", "r4_d1": "r4",
        "g11_d1": "g11", "grade_cross": "grade_cross", "grade_same": "grade_same",
        "endpoint_r8a": "endpoint_r8a", "plane_slope_polygon": "plane_slope_polygon",
        "plane_slope_box": "plane_slope_box", "variable_bounds": "variable_bounds",
        "route_profile_slope": "route_profile_slope", "source_monotone": "source_monotone",
    }
    enabled = set()
    for slack_name, value in all_open.get("normalized_slack_values", {}).items():
        if float(value) <= 1e-7:
            continue
        prefix = slack_name
        for suffix in ("_extra_m", "_extra_hits", "_extra_pp"):
            prefix = prefix.removesuffix(suffix)
        group = slack_to_group.get(prefix)
        if group:
            enabled.add(group)
    # A diagnostic minimum may be zero in one slack dimension but still carry
    # an interdependent row family. The recorded all-open set is the full set
    # of positive groups; these deterministic trials retain only necessary ones.
    active = set(enabled)
    records = []
    for index, group in enumerate(sorted(enabled), 1):
        trial = sorted(active - {group})
        record = run(trial, args.source_relief, f"filter_{index:02d}_{group}")
        feasible = bool(record.get("primal_feasible"))
        records.append({
            "index": index, "hard_family": group, "enabled_groups": trial,
            "status": record.get("status"), "primal_feasible": feasible,
            "removed_from_conflict_set": feasible,
            "normalized_slack_values": record.get("normalized_slack_values"),
            "family_max_relaxation_locations": record.get("family_max_relaxation_locations"),
            "model_json": record.get("filter_model_json"),
        })
        if feasible:
            active.remove(group)
    result = {
        "method": "serial greedy family deletion filter over p3d29 LP relaxation",
        "source_relief": str(args.source_relief),
        "all_open": {
            "status": all_open.get("status"),
            "primal_feasible": all_open.get("primal_feasible"),
            "normalized_slack_values": all_open.get("normalized_slack_values"),
            "slack_values": all_open.get("slack_values"),
            "family_max_relaxation_locations": all_open.get("family_max_relaxation_locations"),
            "model_json": all_open.get("filter_model_json"),
        },
        "positive_slack_groups": sorted(enabled),
        "remaining_group_conflict": sorted(active),
        "records": records,
        "scope": "LP relaxation and group-level deletion only; not an exact row IIS or integer IIS",
    }
    path = RESULTS / "p3d29_V3_lp_group_filter.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"out": str(path), "positive_slack_groups": sorted(enabled),
                      "remaining_group_conflict": sorted(active),
                      "all_open_status": all_open.get("status")}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
