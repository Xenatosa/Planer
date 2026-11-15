#!/usr/bin/env python3
"""Run a hard p3d37 LP and request one bounded HiGHS IIS (strategy 6)."""
from __future__ import annotations

import base64
import gzip
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
from types import SimpleNamespace

import numpy as np
from scipy.sparse import csr_matrix

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "codex_jobs/tools/p3d37"
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
SOURCE = Path("/tmp/p3d37/source.json.gz")
TRANSFER = RELIEF3D / "neu/p3d21_transfer_base_route3_v29.json"
REFERENCE = RELIEF3D / "neu/p3d17_joint_mesh_v22.json"
RESULT = TOOLS / "results/p3d37_startband_iis.json"
TMP_SUMMARY = Path("/tmp/p3d37/iis_lp_summary.json")
IIS_MODEL = Path("/tmp/p3d37/endpoint_infeasible.iis.lp")


def load_model():
    if str(RELIEF3D) not in sys.path:
        sys.path.insert(0, str(RELIEF3D))
    p3d33 = ROOT / "codex_jobs/tools/p3d33"
    if str(p3d33) not in sys.path:
        sys.path.insert(0, str(p3d33))
    path = TOOLS / "diagnose_lp_p3d37.py"
    spec = importlib.util.spec_from_file_location("p3d37_iis_model", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not import the p3d37 LP model")
    model = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = model
    spec.loader.exec_module(model)
    model.RELIEF = SOURCE.resolve()
    return model


def install_iis_solver(model, time_limit_s: float):
    def solve_with_iis(matrix, rhs, objective, integrality, lower, upper,
                       start=None, time_limit=600.0):
        import inspect
        highspy_dir = Path("/tmp/p3d18_highspy")
        if str(highspy_dir) not in sys.path:
            sys.path.insert(0, str(highspy_dir))
        import highspy

        caller = inspect.currentframe().f_back
        locals_ = caller.f_locals
        families = list(locals_["row_families"])
        profiles = locals_["profiles"]
        offsets = locals_["h_offsets"]
        width = int(locals_["width"])
        height = int(locals_["height"])
        fs = int(locals_["fs"])
        x0 = float(locals_["grid_x0"])
        z0 = float(locals_["grid_z0"])
        surface_start = int(locals_["surface_start"])

        col_names = [f"column_{i}" for i in range(matrix.shape[1])]
        for route, profile in enumerate(profiles):
            for k, station in enumerate(profile["station"]):
                col_names[offsets[route] + k] = (
                    f"route_{profile['index']}_height_station_{float(station) * model.CELL_M:.3f}m"
                )
        for flat in range(width * height):
            iz, ix = divmod(flat, width)
            col_names[surface_start + flat] = (
                f"surface_x_{x0 + ix / fs:.3f}_z_{z0 + iz / fs:.3f}"
            )

        lp = highspy.HighsLp()
        lp.num_col_ = int(matrix.shape[1])
        lp.num_row_ = int(matrix.shape[0])
        lp.col_cost_ = np.asarray(objective, dtype=np.float64).copy()
        lp.col_lower_ = np.asarray(lower, dtype=np.float64).copy()
        lp.col_upper_ = np.asarray(upper, dtype=np.float64).copy()
        lp.row_lower_ = np.full(matrix.shape[0], -np.inf, dtype=np.float64)
        lp.row_upper_ = np.asarray(rhs, dtype=np.float64).copy()
        lp.sense_ = highspy.ObjSense.kMinimize
        csc = matrix.tocsc()
        lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
        lp.a_matrix_.start_ = csc.indptr.astype(np.int32, copy=True)
        lp.a_matrix_.index_ = csc.indices.astype(np.int32, copy=True)
        lp.a_matrix_.value_ = csc.data.astype(np.float64, copy=True)
        lp.integrality_ = [highspy.HighsVarType.kContinuous] * lp.num_col_
        lp.col_names_ = col_names
        lp.row_names_ = [f"row_{i}_{families[i]}" for i in range(len(families))]

        highs = highspy.Highs()
        for name, value in {
            "output_flag": False, "presolve": "on", "threads": 1,
            "mip_rel_gap": 0.0, "time_limit": float(time_limit_s),
            "small_matrix_value": 1e-12, "iis_strategy": 6,
        }.items():
            highs.setOptionValue(name, value)
        pass_status = highs.passModel(lp)
        if pass_status not in (highspy.HighsStatus.kOk, highspy.HighsStatus.kWarning):
            raise RuntimeError(f"HiGHS passModel failed: {pass_status}")
        started = time.monotonic()
        highs.run()
        model_status = highs.getModelStatus()
        solution = highs.getSolution()
        info = highs.getInfo()
        record = {
            "tag": "p3d37_startband",
            "method": "HiGHS continuous LP IIS",
            "highspy_version": highs.version(),
            "iis_strategy": 6,
            "iis_strategy_note": "LP elasticity filter followed by reduction to an IIS",
            "threads": 1,
            "time_limit_s": float(time_limit_s),
            "iis_run_elapsed_s": time.monotonic() - started,
            "model_status": highs.modelStatusToString(model_status),
            "status_code": int(model_status.value),
            "variables": int(matrix.shape[1]),
            "constraints": int(matrix.shape[0]),
            "integer_variable_count": int(np.asarray(integrality, dtype=np.uint8).sum()),
            "objective_value": float(info.objective_function_value),
            "max_primal_infeasibility": float(getattr(info, "max_primal_infeasibility", 0.0)),
            "iis_attempted": False,
        }
        if model_status == highspy.HighsModelStatus.kInfeasible:
            record["iis_attempted"] = True
            iis_status, iis = highs.getIis()
            row_ids = [int(v) for v in iis.row_index_]
            col_ids = [int(v) for v in iis.col_index_]
            endpoint_pairs = locals_["endpoint_stage_pairs"]
            endpoint_start = next((i for i, family in enumerate(families)
                                   if family == "endpoint_stage_pairs"), None)
            row_metadata = []
            for row_id in row_ids:
                family = families[row_id]
                item = {"row_index": row_id, "family": family}
                if family == "endpoint_stage_pairs" and endpoint_start is not None:
                    within = row_id - endpoint_start
                    pair_index = within // 2
                    if 0 <= pair_index < len(endpoint_pairs):
                        pair = endpoint_pairs[pair_index]
                        midpoint = np.array([(pair[0] + pair[2]) * 0.5,
                                             (pair[1] + pair[3]) * 0.5])
                        endpoints = []
                        for profile in profiles:
                            coords = np.asarray(profile["coords"], dtype=np.float64)
                            for at_start, point in ((True, coords[0]), (False, coords[-1])):
                                distance = float(np.hypot(*(midpoint - point)))
                                endpoints.append((distance, int(profile["index"]),
                                                  "anfang" if at_start else "ende",
                                                  point.tolist()))
                        nearest = min(endpoints)
                        item.update({
                            "endpoint_pair_index": pair_index,
                            "endpoint_pair_map": [float(v) for v in pair],
                            "nearest_endpoint_id": f"rampe_{nearest[1]}_{nearest[2]}",
                            "nearest_endpoint_map": [float(v) for v in nearest[3]],
                            "pair_center_distance_to_endpoint_m": nearest[0] * model.CELL_M,
                            "directed_row": "forward" if within % 2 == 0 else "reverse",
                        })
                row_metadata.append(item)
            surface_start = int(locals_["surface_start"])
            width = int(locals_["width"])
            height = int(locals_["height"])
            x0 = float(locals_["grid_x0"])
            z0 = float(locals_["grid_z0"])
            bound_evidence = []
            slack_names = {int(column): name for name, column in locals_["slack_indices"].items()}
            for column in col_ids:
                item = {
                    "column": column,
                    "lower": float(lower[column]),
                    "upper": float(upper[column]),
                }
                if column in slack_names:
                    item.update({
                        "kind": "diagnostic_slack",
                        "name": slack_names[column],
                        "diagnostic_group": locals_["slack_spec"][slack_names[column]][0],
                    })
                if column < surface_start:
                    for route, offset in enumerate(offsets):
                        p = profiles[route]
                        if offset <= column < offset + len(p["h0"]):
                            k = column - offset
                            item.update({
                                "kind": "route_height",
                                "route": int(p["index"]),
                                "station_m": float(p["station"][k]) * model.CELL_M,
                                "coordinate_map": [float(v) for v in p["coords"][k]],
                                "profile_height_m": float(p["h0"][k]),
                            })
                            break
                elif column < surface_start + width * height:
                    index = column - surface_start
                    iz, ix = divmod(index, width)
                    item.update({
                        "kind": "surface_delta",
                        "coordinate_map": [x0 + ix / int(locals_["fs"]),
                                            z0 + iz / int(locals_["fs"])],
                    })
                bound_evidence.append(item)
            record["iis_rows_metadata"] = row_metadata
            record["iis_column_bounds"] = bound_evidence
            counts: dict[str, int] = {}
            rows = []
            for row_id in row_ids:
                family = families[row_id]
                counts[family] = counts.get(family, 0) + 1
                row = matrix.getrow(row_id)
                terms = []
                for column, coefficient in zip(row.indices, row.data):
                    if len(terms) >= 16:
                        break
                    terms.append({
                        "column": int(column), "name": col_names[int(column)],
                        "coefficient": float(coefficient),
                    })
                rows.append({
                    "row_index": row_id,
                    "row_name": f"row_{row_id}_{family}",
                    "family": family,
                    "rhs": float(rhs[row_id]),
                    "fixed_pair_delta_m": (0.054 - model.ENDPOINT_STAGE_FLOAT32_GUARD_M
                                            - float(rhs[row_id])
                                            if family == "endpoint_stage_pairs"
                                            and len(row.indices) == 1
                                            and row.indices[0] in slack_names else None),
                    "slack_required_m": (-float(rhs[row_id])
                                         if family == "endpoint_stage_pairs"
                                         and len(row.indices) == 1
                                         and row.indices[0] in slack_names else None),
                    "nonzero_count": int(row.nnz),
                    "terms_first_16": terms,
                })
            record.update({
                "iis_status": str(iis_status),
                "iis_valid": bool(iis.valid_),
                "iis_status_enum": str(iis.status_),
                "iis_rows": len(row_ids),
                "iis_columns": len(col_ids),
                "iis_row_families": dict(sorted(counts.items())),
                "iis_column_names": [col_names[i] for i in col_ids],
                "iis_rows_evidence": rows,
            })
            IIS_MODEL.parent.mkdir(parents=True, exist_ok=True)
            record["iis_model_write_status"] = str(highs.writeIisModel(str(IIS_MODEL)))
            record["iis_model_file_tmp"] = str(IIS_MODEL)
        RESULT.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8")
        print(json.dumps(record, indent=2, sort_keys=True), flush=True)
        return SimpleNamespace(
            success=model_status == highspy.HighsModelStatus.kOptimal,
            status=int(model_status.value), message=highs.modelStatusToString(model_status),
            x=np.asarray(solution.col_value, dtype=np.float64) if solution.value_valid else None,
            row_value=np.asarray(solution.row_value, dtype=np.float64) if solution.value_valid else None,
            loaded_row_upper=np.asarray(highs.getLp().row_upper_, dtype=np.float64).copy(),
            fun=float(info.objective_function_value),
            mip_dual_bound=float(info.mip_dual_bound), mip_gap=float(info.mip_gap),
            max_primal_infeasibility=float(getattr(info, "max_primal_infeasibility", 0.0)),
            loaded_matrix_delta=0.0, loaded_row_bound_delta=0.0,
        )

    model.highs_mip_solve = solve_with_iis


def main() -> None:
    import shutil
    free_gb = shutil.disk_usage(ROOT).free / (1024 ** 3)
    if free_gb < 15:
        raise SystemExit(f"Only {free_gb:.1f} GB free before IIS")
    if not SOURCE.exists():
        raise SystemExit("Missing /tmp/p3d37/source.json.gz")
    time_limit_s = float(os.environ.get("P3D37_IIS_TIME_LIMIT_S", "840"))
    if not (1.0 <= time_limit_s <= 900.0):
        raise SystemExit("IIS time limit must be between 1 and 900 seconds")
    for path in (RESULT, TMP_SUMMARY, IIS_MODEL):
        if path.exists() and path in (TMP_SUMMARY, IIS_MODEL):
            path.unlink()

    os.environ.update({
        "P3D37_POLICY": "p3d36", "P3D36_POLICY": "official",
        "P3D36_DRAINAGE_POLICY": "official", "P3D36_R3_POLICY": "official_hard",
        "P3D36_R8A_POLICY": "lazy_official", "P3D37_R3_DIAGNOSTIC_SLACKS": "0",
        "P3D20_MODEL_GITTER_LIMIT": "0.020", "P3D20_MODEL_QUER_LIMIT": "3.0",
        "P3D20_MODEL_SINGLE_QUER_LIMIT": "20.0", "P3D20_ENDPOINT_STAGE_LOCK": "1",
        "P3D20_ENDPOINT_R8A_LOCK": "1",
    })
    model = load_model()
    install_iis_solver(model, time_limit_s)
    with gzip.open(SOURCE, "rt", encoding="utf-8") as stream:
        data = json.load(stream)
    center = [152.6292918620858, 28.353590994151514]
    model.R8_GATE_CENTER = np.asarray(center, dtype=np.float64)
    model.CROSSING = model.R8_GATE_CENTER.copy()
    from neu import mesh as neu_mesh
    for slot in ("22", "24"):
        neu_mesh.KREUZUNG_SETTINGS[slot]["solution_file"] = TRANSFER.name
        neu_mesh.KREUZUNG_SETTINGS[slot]["crossing_center_map"] = center
    model.solve(
        data=data, grade=0.45, r3_limit=6, out=TMP_SUMMARY,
        reference_mesh_path=None, axis_tolerance=0.02, plane_tolerance=0.02,
        stage_limit=0.116, quer_limit=7, wob_limit=7, objective_mode="step",
        relax_integrality=True, mip_start_path=None, mip_start_out=None,
        time_limit_s=time_limit_s, event_cuts_path=Path("/tmp/p3d37/empty_event_cuts.json"),
        flood_cuts_path=None, reference_solution_path=REFERENCE,
        diagnostic_groups=set(),
    )


if __name__ == "__main__":
    main()
