#!/usr/bin/env python3
"""Build p3d31 V1 and record whether its no-drainage MIP is probeable."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "codex_jobs/tools/p3d31"
RESULTS = TOOLS / "results"
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
SOURCE = Path("/tmp/p3d22_v3_source.json.gz")
TRANSFER = RELIEF3D / "neu/p3d21_transfer_base_route3_v29.json"
CUTS = RESULTS / "p3d31_V3_R00_cuts.json"
SOLUTION = RESULTS / "p3d31_V3_round01_model.json"
OUT = RESULTS / "p3d31_V3_feasibility.json"
EXPECTED_SOURCE_SHA256 = "b1e347e048d1f26d79b812b795645bf348ef83e831209669cf5cbd2f7717b4a6"
EXPECTED_TRANSFER_SHA256 = "07c140cffa97df408f2c688ee910b4085e429e986b047f15b62551727ea69287"


def main() -> None:
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != EXPECTED_SOURCE_SHA256:
        raise RuntimeError("p3d31 V3 source relief is missing or has an unexpected hash")
    if hashlib.sha256(TRANSFER.read_bytes()).hexdigest() != EXPECTED_TRANSFER_SHA256:
        raise RuntimeError("p3d31 V3 transfer base has an unexpected hash")
    RESULTS.mkdir(parents=True, exist_ok=True)
    CUTS.write_text("[]\n", encoding="utf-8")
    command = [
        sys.executable, str(TOOLS / "run_diagnostic.py"),
        "--geometry", "V3", "--scenario", "joint",
        "--source-relief", str(SOURCE), "--transfer-base", str(TRANSFER),
        "--r8-center", "152.6292918620858", "28.353590994151514",
        "--event-cuts", str(CUTS), "--out", str(SOLUTION),
        "--time-limit", "600", "--keep-solution", "--objective-mode", "step",
        "--reference-solution", str(RELIEF3D / "neu/p3d17_joint_mesh_v22.json"),
        "--groups",
    ]
    env = dict(os.environ)
    env["P3D31_VARIANT"] = "1"
    run = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
    if run.returncode:
        raise RuntimeError(
            f"V1 hard solve failed ({run.returncode}): "
            f"{run.stderr[-2000:]} {run.stdout[-1200:]}"
        )
    solution = json.loads(SOLUTION.read_text(encoding="utf-8"))
    construction = solution.get("p3d31_construction", {})
    result = {
        "tag": "p3d31", "geometry": "V3", "selected_variant": "1",
        "selected_drainage_variant": "1",
        "selected_drainage_mode": "off",
        "method": "hard all-family MIP without per-cell drainage constraints; official checker cuts enforce budgets",
        "source_relief": str(SOURCE), "source_relief_sha256": EXPECTED_SOURCE_SHA256,
        "transfer_base": TRANSFER.name, "transfer_base_sha256": EXPECTED_TRANSFER_SHA256,
        "time_limit_s": 600, "threads": 1,
        "status": solution.get("status"), "status_code": solution.get("status_code"),
        "primal_feasible": bool(solution.get("primal_feasible")),
        "optimality_proven": bool(solution.get("optimality_proven")),
        "variables": solution.get("variables"), "constraints": solution.get("constraints"),
        "drainage_model_variables": {
            "successor_binary": construction.get("drainage_binary_variables"),
            "network_flow": construction.get("drainage_flow_variables"),
            "edge_slack": construction.get("drainage_slack_variables"),
            "potential_candidates": construction.get("drainage_candidates", {}).get("candidate_edges"),
            "modeled_candidates": construction.get("modeled_drainage_candidate_count"),
        },
        "official_sink_policy": solution.get("official_sink_policy"),
        "solution_json": str(SOLUTION.relative_to(ROOT)),
        "probe_allowed": bool(solution.get("primal_feasible")),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
