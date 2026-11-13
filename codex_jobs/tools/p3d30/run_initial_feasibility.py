#!/usr/bin/env python3
"""Run the p3d30 hard model, LP family filter, and at most one drainage fallback."""
from __future__ import annotations

import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "codex_jobs/tools/p3d30"
RESULTS = TOOLS / "results"
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
SOURCE = Path("/tmp/p3d22_v3_source.json.gz")
TRANSFER = RELIEF3D / "neu/p3d21_transfer_base_route3_v29.json"
CUTS = RESULTS / "p3d30_V3_R00_cuts.json"
R8_CENTER = ("152.6292918620858", "28.353590994151514")


def run_model(name: str, *, mode: str, groups: list[str]) -> dict:
    out = RESULTS / f"p3d30_V3_{name}.json"
    command = [
        sys.executable, str(TOOLS / "run_diagnostic.py"),
        "--geometry", "V3", "--scenario", "joint",
        "--source-relief", str(SOURCE), "--transfer-base", str(TRANSFER),
        "--r8-center", *R8_CENTER, "--event-cuts", str(CUTS),
        "--out", str(out), "--time-limit", "600", "--keep-solution",
        "--objective-mode", "step", "--reference-solution",
        str(RELIEF3D / "neu/p3d17_joint_mesh_v22.json"), "--groups", *groups,
    ]
    env = dict(os.environ)
    env["P3D30_DRAINAGE_MODE"] = mode
    env["P3D30_DRAINAGE_VARIANT"] = "1"
    completed = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(
            f"{name} failed ({completed.returncode}): "
            f"stderr={completed.stderr[-2000:]} stdout={completed.stdout[-1500:]}"
        )
    result = json.loads(out.read_text(encoding="utf-8"))
    result["invocation"] = {
        "mode": mode, "groups": groups, "time_limit_s": 600,
        "variant": "1", "command": command,
    }
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if not TRANSFER.is_file() or not CUTS.is_file():
        raise RuntimeError("Transferbasis oder Start-Eventcuts fehlen")
    if len(gzip.decompress(SOURCE.read_bytes())) == 0:
        raise RuntimeError("p3d30 source relief is empty")

    hard = run_model("hard_feasibility", mode="hard", groups=[])
    filter_path = RESULTS / "p3d30_V3_lp_group_filter.json"
    group_filter = None
    fallback = None
    fallback_attempted = False
    if not hard.get("primal_feasible"):
        filtered = subprocess.run(
            [sys.executable, str(TOOLS / "diagnose_groups_p3d30.py"),
             "--source-relief", str(SOURCE)],
            cwd=ROOT, capture_output=True, text=True,
        )
        if filtered.returncode != 0:
            raise RuntimeError(
                f"LP group filter failed ({filtered.returncode}): "
                f"stderr={filtered.stderr[-2000:]} stdout={filtered.stdout[-1500:]}"
            )
        group_filter = json.loads(filter_path.read_text(encoding="utf-8"))
        remaining = set(group_filter.get("remaining_group_conflict", []))
        positive = set(group_filter.get("positive_slack_groups", []))
        if "p3d30_drainage" in remaining or "p3d30_drainage" in positive:
            fallback_attempted = True
            fallback = run_model(
                "soft_drainage_fallback", mode="soft", groups=["p3d30_drainage"],
            )

    selected = hard if hard.get("primal_feasible") else fallback
    selected_mode = "hard" if selected is hard else "soft" if selected is fallback and fallback else "hard"
    result = {
        "tag": "p3d30", "variant": "1",
        "method": "hard MIP first; if infeasible, LP relaxation group filter; at most one weighted drainage-slack fallback",
        "source_relief": str(SOURCE), "source_relief_sha256": source_hash,
        "transfer_base": str(TRANSFER),
        "hard_solve": {
            "status": hard.get("status"), "status_code": hard.get("status_code"),
            "primal_feasible": hard.get("primal_feasible"),
            "optimality_proven": hard.get("optimality_proven"),
            "variables": hard.get("variables"), "constraints": hard.get("constraints"),
            "construction": hard.get("p3d30_construction"),
            "solution_json": str((RESULTS / "p3d30_V3_hard_feasibility.json").relative_to(ROOT)),
        },
        "lp_group_filter": (str(filter_path.relative_to(ROOT)) if group_filter else None),
        "lp_remaining_group_conflict": (group_filter.get("remaining_group_conflict") if group_filter else []),
        "soft_fallback_attempted": fallback_attempted,
        "soft_fallback": ({
            "status": fallback.get("status"), "status_code": fallback.get("status_code"),
            "primal_feasible": fallback.get("primal_feasible"),
            "optimality_proven": fallback.get("optimality_proven"),
            "drainage_slack_max_m": fallback.get("slack_values", {}).get("p3d30_drainage_extra_m"),
            "drainage_slack_sum_m": fallback.get("drainage_l1_sum_m"),
            "drainage_slack_weighted_l1": fallback.get("drainage_weighted_l1_value"),
            "solution_json": str((RESULTS / "p3d30_V3_soft_drainage_fallback.json").relative_to(ROOT)),
        } if fallback else None),
        "selected_drainage_mode": selected_mode,
        "probe_allowed": bool(selected and selected.get("primal_feasible")),
        "selected_solution_json": (
            str((RESULTS / ("p3d30_V3_hard_feasibility.json" if selected is hard
                           else "p3d30_V3_soft_drainage_fallback.json")).relative_to(ROOT))
            if selected and selected.get("primal_feasible") else None
        ),
    }
    out = RESULTS / "p3d30_V3_feasibility.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "out": str(out), "hard_status": hard.get("status"),
        "LP_filter": bool(group_filter), "fallback_attempted": fallback_attempted,
        "selected_drainage_mode": selected_mode,
        "probe_allowed": result["probe_allowed"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
