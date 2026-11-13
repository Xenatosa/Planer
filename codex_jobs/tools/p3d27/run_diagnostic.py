#!/usr/bin/env python3
"""Run one p3d27 family-elastic diagnostic on recorded V3 geometry."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
MODEL_PATH = Path(__file__).with_name("diagnose_slack_p3d27.py")
BASE_MODEL_PATH = ROOT / "codex_jobs/tools/p3d20_r3/joint_mesh_r3_exact_p3d20.py"
GROUPS = (
    "r3_long", "r3_quer", "r3_wob", "crossing_stage", "axis_supports",
    "plane_core", "endpoint_stage", "safety_gitter", "safety_quer",
    "safety_single_quer", "g5", "r5_hole", "r4",
    "grade_cross", "grade_same", "endpoint_r8a", "plane_slope_polygon",
    "plane_slope_box", "variable_bounds", "route_profile_slope", "source_monotone",
    "g11",
)


def load_model():
    if str(RELIEF3D) not in sys.path:
        sys.path.insert(0, str(RELIEF3D))
    spec = importlib.util.spec_from_file_location("p3d27_slack_model", MODEL_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("p3d27 model module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--geometry", choices=("V3",), required=True)
    ap.add_argument("--scenario", choices=(*GROUPS, "joint"), required=True)
    ap.add_argument("--groups", nargs="*", choices=GROUPS,
                    help="override enabled family set; used by deletion filtering")
    ap.add_argument("--source-relief", type=Path, required=True)
    ap.add_argument("--transfer-base", type=Path, required=True)
    ap.add_argument("--r8-center", type=float, nargs=2, required=True)
    ap.add_argument("--event-cuts", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--time-limit", type=float, default=600.0)
    ap.add_argument("--keep-solution", action="store_true")
    args = ap.parse_args()

    if args.transfer_base.parent.resolve() != (RELIEF3D / "neu").resolve():
        raise ValueError("Transferbasis muss eine dokumentierte Datei in relief3d/neu sein")
    if len(args.r8_center) != 2:
        raise ValueError("--r8-center erwartet x z")
    os.environ["P3D20_MODEL_GITTER_LIMIT"] = "0.019"
    os.environ["P3D20_MODEL_QUER_LIMIT"] = "2.95"
    os.environ["P3D20_MODEL_SINGLE_QUER_LIMIT"] = "19.5"
    os.environ["P3D20_ENDPOINT_STAGE_LOCK"] = "1"
    os.environ["P3D20_ENDPOINT_R8A_LOCK"] = "0" if args.geometry == "V24" else "1"
    model = load_model()
    model.RELIEF = args.source_relief.resolve()
    model.R8_GATE_CENTER = model.np.asarray(args.r8_center, dtype=model.np.float64)
    model.CROSSING = model.R8_GATE_CENTER.copy()

    from neu import mesh as neu_mesh
    for slot in ("22", "24"):
        neu_mesh.KREUZUNG_SETTINGS[slot]["solution_file"] = args.transfer_base.name
        neu_mesh.KREUZUNG_SETTINGS[slot]["crossing_center_map"] = list(args.r8_center)

    source_bytes = args.source_relief.read_bytes()
    data = json.loads(gzip.decompress(source_bytes))
    groups = (set(args.groups) if args.groups is not None else
              set(GROUPS) if args.scenario == "joint" else {args.scenario})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    result = model.solve(
        data=data,
        grade=0.45,
        r3_limit=6,
        out=args.out,
        reference_mesh_path=None,
        axis_tolerance=0.02,
        plane_tolerance=0.02,
        stage_limit=0.11599,
        quer_limit=7,
        wob_limit=7,
        objective_mode="diagnostic",
        relax_integrality=False,
        mip_start_path=None,
        mip_start_out=None,
        time_limit_s=args.time_limit,
        event_cuts_path=args.event_cuts,
        reference_solution_path=None,
        diagnostic_groups=groups,
    )
    result.update({
        "geometry": args.geometry,
        "scenario": args.scenario,
        "requested_groups": sorted(groups),
        "source_relief_path": str(args.source_relief.resolve()),
        "source_relief_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "transfer_base": args.transfer_base.name,
        "transfer_base_sha256": hashlib.sha256(args.transfer_base.read_bytes()).hexdigest(),
        "base_model_sha256": hashlib.sha256(BASE_MODEL_PATH.read_bytes()).hexdigest(),
        "diagnostic_model_sha256": hashlib.sha256(MODEL_PATH.read_bytes()).hexdigest(),
        "event_cuts_file": args.event_cuts.name,
        "event_cuts_sha256": hashlib.sha256(args.event_cuts.read_bytes()).hexdigest(),
        "r8_center_unrounded_map": list(args.r8_center),
        "time_limit_s": args.time_limit,
        "solver": "highspy.Highs; threads=1",
        "cuts_are_round05_v24_catalog_for_all_geometries": args.event_cuts.name == "event_cuts_cumulative05.json",
        "endpoint_r8a_lock_enabled": args.geometry != "V24",
        "family_iis_scope": "p3d27 V3 elastic extension; group-level only, not row IIS",
        "event_counter_model": {
            "g5_total_max": 69,
            "g5_fixed_non_d1_baseline": 67,
            "g5_d1_max": 2,
            "r5_hole_total_max": 22,
            "r5_hole_fixed_non_d1_baseline": 17,
            "r5_hole_d1_max": 5,
            "r4_d1_max": 0,
            "scope": "round05 V24 event-cut catalog; cut relaxation indicators, not a fresh official component recount",
        },
    })
    status_text = str(result.get("status", ""))
    status_match = re.search(r"HiGHS Status (\d+)", status_text)
    if status_match:
        highs_status = int(status_match.group(1))
    elif status_text == "Optimal":
        highs_status = 7
    elif "Infeasible" in status_text:
        highs_status = 8
    elif "Time limit" in status_text:
        highs_status = 13
    else:
        highs_status = result.get("status_code")
    result["highs_status_code"] = highs_status
    if highs_status is not None:
        result["status_code"] = highs_status
    result["optimality_proven"] = highs_status == 7
    result["infeasibility_proven"] = highs_status == 8
    if not args.keep_solution:
        result.pop("surface_grid", None)
        result.pop("routes", None)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {key: value for key, value in result.items()
               if key not in {"surface_grid", "routes"}}
    print(json.dumps(compact, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
