#!/usr/bin/env python3
"""Run the required hard p3d29 solve and its single drainage L1 fallback."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "codex_jobs/tools/p3d29"
RESULTS = TOOLS / "results"
RUNNER = TOOLS / "run_diagnostic.py"
FILTER = TOOLS / "diagnose_groups_p3d29.py"
SOURCE = Path("/tmp/p3d22_v3_source.json.gz")
TRANSFER = ROOT / "team/art/dorfmap_grundgeruest/relief3d/neu/p3d21_transfer_base_route3_v29.json"
CUTS = RESULTS / "p3d29_V3_R00_cuts.json"
REFERENCE = ROOT / "team/art/dorfmap_grundgeruest/relief3d/neu/p3d17_joint_mesh_v22.json"
EXPECTED_SOURCE_SHA256 = "b1e347e048d1f26d79b812b795645bf348ef83e831209669cf5cbd2f7717b4a6"
EXPECTED_TRANSFER_SHA256 = "07c140cffa97df408f2c688ee910b4085e429e986b047f15b62551727ea69287"


def run(command: list[str], label: str, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{label} failed: {result.stderr[-2000:]} {result.stdout[-1000:]}")
    return result.stdout


def solve(path: Path, *, soft_drainage: bool = False) -> dict:
    command = [
        sys.executable, str(RUNNER), "--geometry", "V3", "--scenario", "joint",
        "--source-relief", str(SOURCE), "--transfer-base", str(TRANSFER),
        "--r8-center", "152.6292918620858", "28.353590994151514",
        "--event-cuts", str(CUTS), "--out", str(path),
        "--time-limit", "600", "--keep-solution", "--objective-mode", "step",
        "--reference-solution", str(REFERENCE), "--groups",
    ]
    if soft_drainage:
        command.append("p3d29_drainage")
    env = dict(os.environ)
    env["P3D29_DRAINAGE_MODE"] = "soft" if soft_drainage else "hard"
    run(command, "soft drainage L1 solve" if soft_drainage else "hard feasibility solve", env)
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    transfer_hash = hashlib.sha256(TRANSFER.read_bytes()).hexdigest()
    if source_hash != EXPECTED_SOURCE_SHA256:
        raise RuntimeError(f"V3-Reliefquelle hat unerwarteten Hash: {source_hash}")
    if transfer_hash != EXPECTED_TRANSFER_SHA256:
        raise RuntimeError(f"V3-Transferbasis hat unerwarteten Hash: {transfer_hash}")
    hard_path = RESULTS / "p3d29_V3_hard_feasibility.json"
    hard = solve(hard_path)
    record = {
        "tag": "p3d29", "source_relief_sha256": source_hash,
        "transfer_base_sha256": transfer_hash,
        "hard_model": str(hard_path.relative_to(ROOT)),
        "hard_status": hard.get("status"),
        "hard_status_code": hard.get("status_code"),
        "hard_primal_feasible": bool(hard.get("primal_feasible")),
        "hard_slack_values": hard.get("slack_values"),
        "hard_family_max_relaxation_locations": hard.get("family_max_relaxation_locations"),
        "lp_group_filter": None,
        "soft_fallback_attempted": False,
        "soft_model": None,
        "soft_status": None,
        "soft_primal_feasible": None,
        "selected_drainage_mode": None,
        "status": "hard_solve_feasible" if hard.get("primal_feasible") else "hard_solve_not_feasible",
    }
    if hard.get("primal_feasible"):
        selected_model = RESULTS / "p3d29_V3_round01_model.json"
        selected_model.write_text(hard_path.read_text(encoding="utf-8"), encoding="utf-8")
        selected_construction = hard_path.with_name(hard_path.stem + "_construction.json")
        selected_model.with_name(selected_model.stem + "_construction.json").write_text(
            selected_construction.read_text(encoding="utf-8"), encoding="utf-8",
        )
        record["selected_drainage_mode"] = "hard"
        record["selected_model"] = str(selected_model.relative_to(ROOT))
    else:
        filter_stdout = run([sys.executable, str(FILTER), "--source-relief", str(SOURCE)],
                            "LP group filter")
        record["lp_group_filter"] = str((RESULTS / "p3d29_V3_lp_group_filter.json").relative_to(ROOT))
        record["lp_group_filter_summary"] = json.loads(filter_stdout)
        # The one allowed construction fallback changes only the drainage rows:
        # all route, locality, cliff-outside-band, tree and official checker caps
        # stay hard. Its normalization scale gives a 10,000 / m L1 weight.
        soft_path = RESULTS / "p3d29_V3_round01_model.json"
        soft = solve(soft_path, soft_drainage=True)
        record["soft_fallback_attempted"] = True
        record["soft_model"] = str(soft_path.relative_to(ROOT))
        record["soft_status"] = soft.get("status")
        record["soft_status_code"] = soft.get("status_code")
        record["soft_primal_feasible"] = bool(soft.get("primal_feasible"))
        record["soft_slack_values"] = soft.get("slack_values")
        record["soft_family_max_relaxation_locations"] = soft.get("family_max_relaxation_locations")
        if soft.get("primal_feasible"):
            record["selected_drainage_mode"] = "soft"
            record["selected_model"] = str(soft_path.relative_to(ROOT))
            record["status"] = "soft_drainage_fallback_feasible"
        else:
            # The hard solve is infeasible and the single authorized soft
            # drainage attempt is also infeasible; the task stops before probes.
            record["status"] = "hard_and_single_soft_drainage_solve_infeasible"
    out = RESULTS / "p3d29_V3_feasibility.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: record.get(key) for key in (
        "status", "hard_status", "hard_primal_feasible", "soft_fallback_attempted",
        "soft_status", "soft_primal_feasible", "selected_drainage_mode", "lp_group_filter",
    )}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
