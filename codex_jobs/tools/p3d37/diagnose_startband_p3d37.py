#!/usr/bin/env python3
"""Run serial p3d37 elastic filters with the rampe_11 endpoint cap kept hard."""
from __future__ import annotations

import argparse
import gzip
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
from scipy import ndimage as ndi

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "codex_jobs/tools/p3d37"
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
SOURCE = Path("/tmp/p3d37/source.json.gz")
TRANSFER = RELIEF3D / "neu/p3d21_transfer_base_route3_v29.json"
REFERENCE = RELIEF3D / "neu/p3d17_joint_mesh_v22.json"
EMPTY_CUTS = Path("/tmp/p3d37/empty_event_cuts.json")
RESULT = TOOLS / "results/p3d37_startband_filters.json"
POINTS = [(147.5, z) for z in (4.5, 4.75, 5.0, 5.25, 5.5, 5.75, 6.0)]
TARGET_PAIR = ((147.5, 5.0), (147.5, 5.25))


def load_model():
    if str(RELIEF3D) not in sys.path:
        sys.path.insert(0, str(RELIEF3D))
    p3d33 = ROOT / "codex_jobs/tools/p3d33"
    if str(p3d33) not in sys.path:
        sys.path.insert(0, str(p3d33))
    path = TOOLS / "diagnose_lp_p3d37.py"
    spec = importlib.util.spec_from_file_location("p3d37_startband_model", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not import the p3d37 LP model")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.RELIEF = SOURCE.resolve()
    return module


def sample(grid: np.ndarray, x0: float, z0: float, spacing: float,
           x: float, z: float) -> float:
    y = (z - z0) / spacing
    x_index = (x - x0) / spacing
    return float(ndi.map_coordinates(
        grid, [[y], [x_index]], order=1, mode="nearest",
    )[0])


def load_transfer(model):
    from neu import mesh as neu_mesh
    center = [152.6292918620858, 28.353590994151514]
    model.R8_GATE_CENTER = np.asarray(center, dtype=np.float64)
    model.CROSSING = model.R8_GATE_CENTER.copy()
    neu_mesh.KREUZUNG_SETTINGS["22"]["solution_file"] = TRANSFER.name
    neu_mesh.KREUZUNG_SETTINGS["24"]["solution_file"] = TRANSFER.name
    neu_mesh.KREUZUNG_SETTINGS["22"]["crossing_center_map"] = center
    neu_mesh.KREUZUNG_SETTINGS["24"]["crossing_center_map"] = center
    fixed, coverage, _, _ = model.p3d17_transfer_context()
    p3d17 = model.p3d17_reference_output()
    return fixed, coverage, p3d17


def model_command(case: str, groups: list[str], limit: int) -> list[str]:
    output = Path(f"/tmp/p3d37/{case}.json")
    return [
        sys.executable, str(TOOLS / "run_lp_p3d37.py"),
        "--geometry", "V3", "--scenario", "joint",
        "--source-relief", str(SOURCE), "--transfer-base", str(TRANSFER),
        "--r8-center", "152.6292918620858", "28.353590994151514",
        "--event-cuts", str(EMPTY_CUTS), "--out", str(output),
        "--time-limit", str(limit), "--objective-mode", "diagnostic",
        "--reference-solution", str(REFERENCE), "--relax-integrality",
        "--keep-solution", "--groups", *groups,
    ]


def collect_case(model, fixed, coverage, p3d17, case: str,
                 groups: list[str], limit: int) -> dict:
    output = Path(f"/tmp/p3d37/{case}.json")
    construction = output.with_name(output.stem + "_construction.json")
    free_gb = __import__("shutil").disk_usage(ROOT).free / (1024 ** 3)
    if free_gb < 15:
        raise RuntimeError(f"Only {free_gb:.1f} GB free before {case}; stop and clean p3d37 temp files")
    env = os.environ.copy()
    env.update({
        "P3D37_POLICY": "p3d36",
        "P3D36_POLICY": "official",
        "P3D36_DRAINAGE_POLICY": "official",
        "P3D36_R3_POLICY": "official_hard",
        "P3D36_R8A_POLICY": "lazy_official",
        "P3D20_MODEL_GITTER_LIMIT": "0.020",
        "P3D20_MODEL_QUER_LIMIT": "3.0",
        "P3D20_MODEL_SINGLE_QUER_LIMIT": "20.0",
        "P3D20_ENDPOINT_STAGE_LOCK": "1",
        "P3D20_ENDPOINT_R8A_LOCK": "1",
        "P3D37_ROW_AUDIT": "1" if case == "all_family_row_audit" else "0",
        "P3D37_R3_DIAGNOSTIC_SLACKS": (
            "1" if case.startswith("official_r3_slack_")
            or case == "all_other_hard_endpoint"
            or case.startswith("target_") else "0"
        ),
        "P3D37_TARGET_STAGE_LOCK": "1" if case.startswith("target_") else "0",
    })
    started = time.monotonic()
    proc = subprocess.run(model_command(case, groups, limit), cwd=ROOT,
                          env=env, capture_output=True, text=True,
                          timeout=limit + 90)
    elapsed = time.monotonic() - started
    if proc.returncode not in (0, 1):
        return {
            "case": case, "enabled_groups": groups,
            "status": "runner_error", "elapsed_s": elapsed,
            "stderr_tail": proc.stderr[-1500:],
            "stdout_tail": proc.stdout[-1500:],
        }
    if not output.exists():
        return {
            "case": case, "enabled_groups": groups,
            "status": "missing_solution_json", "elapsed_s": elapsed,
            "returncode": proc.returncode,
            "stderr_tail": proc.stderr[-1500:],
        }
    solution = json.loads(output.read_text(encoding="utf-8"))
    record = {
        "case": case,
        "enabled_groups": groups,
        "status": solution.get("status"),
        "status_code": solution.get("status_code"),
        "success": solution.get("success"),
        "primal_feasible": solution.get("primal_feasible"),
        "optimality_proven": solution.get("optimality_proven"),
        "variables": solution.get("variables"),
        "constraints": solution.get("constraints"),
        "elapsed_s": elapsed,
        "disk_free_before_solve_gb": free_gb,
        "positive_slacks": {
            name: value for name, value in solution.get("slack_values", {}).items()
            if value is not None and float(value) > 1e-7
        },
        "endpoint_stage": solution.get("family_max_relaxation_locations", {}).get(
            "endpoint_stage"),
        "family_max_relaxation_locations": solution.get(
            "family_max_relaxation_locations", {}),
        "endpoint_stage_pair_count": solution.get("endpoint_stage_pair_count"),
        "profile_windows": solution.get("p3d36_profile_windows"),
        "p3d37_startband_row_audit": solution.get("p3d37_startband_row_audit"),
        "status_output_tail": proc.stdout[-1200:],
    }
    if solution.get("primal_feasible") and "surface_grid" in solution:
        grid_info = solution["surface_grid"]
        target = np.asarray(grid_info["heights_m"], dtype=np.float64)
        candidate = (fixed + coverage * target).astype("<f4").astype(np.float64)
        sample_rows = []
        for x, z in POINTS:
            sample_rows.append({
                "x": x, "z": z,
                "height_m": sample(candidate, grid_info["x0"], grid_info["z0"],
                                   grid_info["spacing"], x, z),
                "p3d17_height_m": sample(p3d17, grid_info["x0"], grid_info["z0"],
                                         grid_info["spacing"], x, z),
            })
        a, b = TARGET_PAIR
        ha = sample(candidate, grid_info["x0"], grid_info["z0"], grid_info["spacing"], *a)
        hb = sample(candidate, grid_info["x0"], grid_info["z0"], grid_info["spacing"], *b)
        record["target_pair"] = {
            "a": list(a), "b": list(b), "height_a_m": ha,
            "height_b_m": hb, "delta_m": abs(ha - hb), "limit_m": 0.054,
        }
        record["profile_rampe_11"] = solution.get("routes", {}).get("rampe_11")
        record["neighbor_heights"] = sample_rows
    for path in (output, construction):
        if path.exists():
            path.unlink()
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=("all", "single", "audit", "internal", "official_r3", "all_other", "target_lock", "target_inverse"), default="all")
    parser.add_argument("--limit", type=int, default=180)
    args = parser.parse_args()
    if not SOURCE.exists() or not EMPTY_CUTS.exists():
        raise SystemExit("Expected p3d37 diagnostic inputs are missing in /tmp/p3d37")
    if args.limit < 1 or args.limit > 600:
        raise SystemExit("Per-solve time limit must be between 1 and 600 seconds")
    free = __import__("shutil").disk_usage(ROOT).free / (1024 ** 3)
    if free < 15:
        raise SystemExit(f"Only {free:.1f} GB free; clean p3d37 temporary files first")

    run_lp = load_model()
    fixed, coverage, p3d17 = load_transfer(run_lp)
    from run_lp_p3d37 import GROUPS
    all_groups = list(GROUPS)
    if args.case == "all":
        cases = [("all_family_filter", all_groups)]
        candidates = [
            "variable_bounds", "axis_supports", "route_profile_slope",
            "source_monotone", "p3d29_locality", "p3d29_cliff_form",
            "p3d29_tree_ground", "p3d31_drainage", "p3d36_crossfall",
            "endpoint_r8a", "r3_long", "r3_quer", "r3_wob",
        ]
        cases.extend((f"single_{name}", [name]) for name in candidates)
    elif args.case == "single":
        cases = [("all_family_filter", all_groups)]
    elif args.case == "audit":
        cases = [("all_family_row_audit", all_groups)]
    elif args.case == "internal":
        cases = [("internal_all_only", [
            "axis_supports", "plane_core", "variable_bounds",
            "route_profile_slope", "source_monotone", "p3d29_locality",
            "p3d31_drainage", "p3d29_cliff_form", "p3d29_tree_ground",
            "p3d36_no_crossfall",
        ])]
    elif args.case == "all_other":
        cases = [("all_other_hard_endpoint", [
            name for name in all_groups if name != "endpoint_stage"
        ])]
    elif args.case == "target_lock":
        cases = [("target_all_families_elastic", all_groups)]
    elif args.case == "target_inverse":
        candidates = [name for name in all_groups if name != "endpoint_stage"]
        cases = [(f"target_hard_{name}", [g for g in all_groups if g != name])
                 for name in candidates]
    else:
        cases = [(f"official_r3_slack_{name}", [name])
                 for name in ("r3_long", "r3_quer", "r3_wob")]

    existing = {item["case"]: item for item in json.loads(RESULT.read_text())
                .get("runs", [])} if RESULT.exists() else {}
    for case, groups in cases:
        if case in existing:
            print(f"SKIP {case}: compact result already exists", flush=True)
            continue
        free_now = __import__("shutil").disk_usage(ROOT).free / (1024 ** 3)
        print(f"START {case}: groups={groups}; free_gb={free_now:.2f}", flush=True)
        record = collect_case(run_lp, fixed, coverage, p3d17, case, groups, args.limit)
        existing[case] = record
        payload = {
            "tag": "p3d37", "method": "serial elastic family filters; no IIS",
            "iis_strategy": "not run", "solver": "HiGHS LP, one thread",
            "endpoint_cap_kept_hard_for_single_group_cases": True,
            "runs": list(existing.values()),
        }
        RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8")
        print(json.dumps({
            "case": case, "status": record.get("status"),
            "positive_slacks": record.get("positive_slacks"),
            "target_pair": record.get("target_pair"),
            "elapsed_s": record.get("elapsed_s"),
        }, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
