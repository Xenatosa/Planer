#!/usr/bin/env python3
"""Run the p3d23 family-IIS probes serially for one p3d24 start variant."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
MODEL = ROOT / "codex_jobs/tools/p3d23/run_diagnostic.py"
EMPTY_CUTS = ROOT / "codex_jobs/tools/p3d23/results/p3d23_round00_empty_cuts.json"
FAMILIES = [
    "r3_long", "r3_quer", "r3_wob", "crossing_stage", "axis_supports",
    "plane_core", "endpoint_stage", "safety_gitter", "safety_quer",
    "safety_single_quer", "g5", "r5_hole", "r4", "grade_cross", "grade_same",
    "endpoint_r8a", "plane_slope_polygon", "plane_slope_box", "variable_bounds",
    "route_profile_slope", "source_monotone", "g11",
]


def run(label: str, enabled: list[str], args, out: Path) -> dict:
    command = [
        sys.executable, str(MODEL), "--geometry", "V3", "--scenario", "joint",
        "--groups", *enabled,
        "--source-relief", str(args.source.resolve()),
        "--transfer-base", str(args.transfer.resolve()),
        "--r8-center", str(args.r8_center[0]), str(args.r8_center[1]),
        "--event-cuts", str(EMPTY_CUTS), "--out", str(out),
        "--time-limit", "600", "--keep-solution",
    ]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if completed.returncode != 0 or not out.exists():
        raise RuntimeError(
            f"{label} failed ({completed.returncode}): "
            f"{completed.stderr[-2000:]} {completed.stdout[-1000:]}"
        )
    result = json.loads(out.read_text(encoding="utf-8"))
    return {
        "label": label,
        "enabled_groups": enabled,
        "status": result.get("status"),
        "status_code": result.get("status_code"),
        "primal_feasible": result.get("primal_feasible"),
        "optimality_proven": result.get("optimality_proven"),
        "weighted_l1_value": result.get("weighted_l1_value"),
        "slack_values": result.get("slack_values"),
        "maximum_normalized_slack": result.get("maximum_normalized_slack"),
        "endpoint_R8a_pair_count": result.get("endpoint_R8a_pair_count"),
        "family_max_relaxation_locations": result.get("family_max_relaxation_locations"),
        "variables": result.get("variables"), "constraints": result.get("constraints"),
        "time_limit_s": result.get("time_limit_s"),
        "source_relief_sha256": result.get("source_relief_sha256"),
        "transfer_base_sha256": result.get("transfer_base_sha256"),
        "model_json": str(out),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=("1", "2", "3"), required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--transfer", type=Path, required=True)
    parser.add_argument("--r8-center", type=float, nargs=2, required=True)
    args = parser.parse_args()
    results = ROOT / "codex_jobs/tools/p3d24/results"
    results.mkdir(parents=True, exist_ok=True)
    scenarios = [
        ("all_open", FAMILIES),
        ("endpoint_only", ["endpoint_r8a"]),
        ("all_except_endpoint", [name for name in FAMILIES if name != "endpoint_r8a"]),
    ]
    runs = []
    for label, groups in scenarios:
        out = results / f"p3d24_v{args.variant}_{label}.json"
        runs.append(run(label, groups, args, out))

    report = {
        "tag": "p3d24", "variant": args.variant,
        "diagnosis": "p3d23 family deletion filter; empty Round00 event-cut list; serial; 600 s per solve",
        "source_relief": str(args.source.resolve()),
        "transfer_base": str(args.transfer.resolve()),
        "r8_center_unrounded_map": args.r8_center,
        "runs": runs,
        "minimal_endpoint_r8a_family_supported": bool(
            runs[0]["primal_feasible"] and runs[1]["primal_feasible"]
            and not runs[2]["primal_feasible"]
            and abs(float(runs[0]["slack_values"]["endpoint_r8a_extra_m"])) > 1e-8
        ),
    }
    out = results / f"p3d24_v{args.variant}_family_iis.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(json.dumps({
        "out": str(out),
        "runs": [{"label": r["label"], "status": r["status"],
                  "primal_feasible": r["primal_feasible"],
                  "R8a_slack_m": (r["slack_values"] or {}).get("endpoint_r8a_extra_m")}
                 for r in runs],
        "minimal_endpoint_r8a_family_supported": report["minimal_endpoint_r8a_family_supported"],
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
