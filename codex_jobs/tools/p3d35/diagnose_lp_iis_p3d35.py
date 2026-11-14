#!/usr/bin/env python3
"""Run the p3d35 continuous LP with the p3d31-style HiGHS LP-IIS capture."""
from __future__ import annotations

import importlib.util
import inspect
import json
import os
from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np
from scipy.sparse import csr_matrix

ROOT = Path(__file__).resolve().parents[3]
RESULTS = Path(__file__).with_name("results")
RESULTS.mkdir(parents=True, exist_ok=True)
RUNNER_PATH = ROOT / "codex_jobs/tools/p3d35/run_lp_p3d35.py"
MODEL_PATH = ROOT / "codex_jobs/tools/p3d35/diagnose_lp_p3d35.py"


def load_model():
    relief3d = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
    tool_dir = ROOT / "codex_jobs/tools/p3d33"
    if str(relief3d) not in sys.path:
        sys.path.insert(0, str(relief3d))
    if str(tool_dir) not in sys.path:
        sys.path.insert(0, str(tool_dir))
    spec = importlib.util.spec_from_file_location(
        "p3d35_iis_model",
        MODEL_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"LP source could not be loaded: {MODEL_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    def solve_with_iis(matrix, rhs, objective, integrality, lower, upper,
                       start=None, time_limit=600.0):
        caller = inspect.currentframe().f_back
        families = list(caller.f_locals["row_families"])
        highspy_dir = Path("/tmp/p3d18_highspy")
        if str(highspy_dir) not in sys.path:
            sys.path.insert(0, str(highspy_dir))
        import highspy

        locals_ = caller.f_locals
        profiles = locals_.get("profiles", [])
        h_offsets = locals_.get("h_offsets", [])
        rhs_used = np.asarray(rhs, dtype=np.float64).copy()
        model_tag = os.environ.get("P3D35_IIS_TAG", "official_initial")
        intervention = {"kind": os.environ.get("P3D35_INTERVENTION", "none")}
        route2_profile_index = next(
            (i for i, item in enumerate(profiles) if int(item["index"]) == 2), None,
        )
        route2_start_column = None
        route2_start_station_m = None
        if route2_profile_index is not None:
            route2_start_column = int(h_offsets[route2_profile_index])
            route2_start_station_m = float(profiles[route2_profile_index]["station"][0]) * 2.4
        relax_m = float(os.environ.get("P3D35_RELAX_M", "0"))
        changed_rows = []
        if intervention["kind"] == "rampe2_start_profile_lower_bound":
            if route2_start_column is None or relax_m <= 0.0:
                raise ValueError("start profile relaxation requires a positive P3D35_RELAX_M")
            hits = []
            for i, family in enumerate(families):
                if family != "variable_bounds":
                    continue
                row = matrix.getrow(i)
                if any(int(col) == route2_start_column and float(coeff) < 0.0
                       for col, coeff in zip(row.indices, row.data)):
                    hits.append(i)
            if len(hits) != 1:
                raise RuntimeError(f"expected one lower bound row for rampe_2 station 0, found {hits}")
            rhs_used[hits[0]] += relax_m
            changed_rows.append({"row_index": hits[0], "family": families[hits[0]],
                                 "rhs_delta_m": relax_m, "direction": "lower"})
        elif intervention["kind"] == "rampe2_start_mesh_anchor_lower_bound":
            if relax_m <= 0.0:
                raise ValueError("start mesh anchor relaxation requires a positive P3D35_RELAX_M")
            anchor = locals_.get("ramp2_row")
            if not anchor:
                raise RuntimeError("rampe_2 start anchor row is unavailable")
            hits = []
            for i, family in enumerate(families):
                if family != "p3d33_fixed_anchors":
                    continue
                row = matrix.getrow(i)
                actual = {int(col): float(coeff) for col, coeff in zip(row.indices, row.data)}
                if actual and all(abs(actual.get(int(col), 0.0) + float(coeff)) <= 1e-12
                                  for col, coeff in anchor.items()) and len(actual) == len(anchor):
                    hits.append(i)
            if len(hits) != 1:
                raise RuntimeError(f"expected one downward rampe_2 mesh-anchor row, found {hits}")
            row_index = hits[0]
            rhs_used[row_index] += relax_m
            changed_rows.append({"row_index": row_index, "family": families[row_index],
                                 "rhs_delta_m": relax_m, "direction": "lower"})
        elif intervention["kind"] != "none":
            raise ValueError(f"unknown P3D35_INTERVENTION={intervention['kind']}")
        intervention.update({
            "relax_m": relax_m,
            "rampe_2_start_profile_column": route2_start_column,
            "rampe_2_start_station_m": route2_start_station_m,
            "changed_rows": changed_rows,
            "note": "LP-only targeted row relaxation; official checker and source files are unchanged",
        })

        lp = highspy.HighsLp()
        lp.num_col_ = int(matrix.shape[1])
        lp.num_row_ = int(matrix.shape[0])
        lp.col_cost_ = np.asarray(objective, dtype=np.float64).copy()
        lp.col_lower_ = np.asarray(lower, dtype=np.float64).copy()
        lp.col_upper_ = np.asarray(upper, dtype=np.float64).copy()
        lp.row_lower_ = np.full(matrix.shape[0], -np.inf, dtype=np.float64)
        lp.row_upper_ = rhs_used.copy()
        lp.sense_ = highspy.ObjSense.kMinimize
        csc = matrix.tocsc()
        lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
        lp.a_matrix_.start_ = csc.indptr.astype(np.int32, copy=True)
        lp.a_matrix_.index_ = csc.indices.astype(np.int32, copy=True)
        lp.a_matrix_.value_ = csc.data.astype(np.float64, copy=True)
        lp.integrality_ = [highspy.HighsVarType.kContinuous] * lp.num_col_

        col_names = [f"x_{i}" for i in range(lp.num_col_)]
        surface_start = int(locals_.get("surface_start", -1))
        width = int(locals_.get("width", 0))
        height = int(locals_.get("height", 0))
        fs = int(locals_.get("fs", 0))
        grid_x0 = float(locals_.get("grid_x0", 0.0))
        grid_z0 = float(locals_.get("grid_z0", 0.0))
        for route, profile in enumerate(profiles):
            if route >= len(h_offsets):
                continue
            start_col = int(h_offsets[route])
            for k, station in enumerate(profile.get("station", [])):
                if start_col + k < len(col_names):
                    col_names[start_col + k] = (
                        f"route_{profile['index']}_height_station_{float(station) * 2.4:.6f}m"
                    )
        if surface_start >= 0 and width > 0 and fs > 0:
            for flat in range(width * height):
                iz, ix = divmod(flat, width)
                col = surface_start + flat
                if col < len(col_names):
                    col_names[col] = (
                        f"surface_x_{grid_x0 + ix / fs:.3f}_z_{grid_z0 + iz / fs:.3f}"
                    )
        lp.col_names_ = col_names
        lp.row_names_ = [f"row_{i}_{families[i]}" for i in range(len(families))]

        highs = highspy.Highs()
        options = {
            "output_flag": False,
            "presolve": "on",
            "threads": 1,
            "mip_rel_gap": 0.0,
            "time_limit": float(time_limit),
            "small_matrix_value": 1e-12,
        }
        for name, value in options.items():
            highs.setOptionValue(name, value)
        highs.setOptionValue("iis_strategy", 6)
        pass_status = highs.passModel(lp)
        if pass_status not in (highspy.HighsStatus.kOk, highspy.HighsStatus.kWarning):
            raise RuntimeError(f"HiGHS passModel failed: {pass_status}")
        highs.run()
        model_status = highs.getModelStatus()
        solution = highs.getSolution()
        info = highs.getInfo()
        result = {
            "tag": model_tag,
            "method": "HiGHS LP-IIS, p3d31 step0 strategy",
            "highspy_version": highs.version(),
            "iis_strategy": 6,
            "iis_strategy_note": "LP elasticity filter followed by reduction to an IIS, matching p3d31 step0",
            "intervention": intervention,
            "threads": 1,
            "time_limit_s": float(time_limit),
            "model_status": highs.modelStatusToString(model_status),
            "status_code": int(model_status.value),
            "variables": int(matrix.shape[1]),
            "constraints": int(matrix.shape[0]),
            "integer_variable_count": int(np.asarray(integrality, dtype=np.uint8).sum()),
            "objective_value": float(info.objective_function_value),
            "max_primal_infeasibility": float(getattr(info, "max_primal_infeasibility", 0.0)),
            "row_family_counts": dict(sorted({
                family: families.count(family) for family in set(families)
            }.items())),
            "iis_attempted": False,
        }
        if model_status == highspy.HighsModelStatus.kInfeasible:
            result["iis_attempted"] = True
            iis_status, iis = highs.getIis()
            selected_rows = [int(v) for v in iis.row_index_]
            selected_columns = [int(v) for v in iis.col_index_]
            row_counts: dict[str, int] = {}
            row_evidence = []
            route_height_names = set(col_names)
            for row_index in selected_rows:
                family = families[row_index]
                row_counts[family] = row_counts.get(family, 0) + 1
                row = matrix.getrow(row_index)
                terms = []
                for col, coeff in zip(row.indices, row.data):
                    if len(terms) < 12:
                        terms.append({
                            "column": int(col), "name": col_names[int(col)],
                            "coefficient": float(coeff),
                        })
                row_evidence.append({
                    "row_index": row_index,
                    "row_name": f"row_{row_index}_{family}",
                    "family": family,
                    "rhs": float(rhs_used[row_index]),
                    "nonzero_count": int(row.nnz),
                    "terms_first_12": terms,
                })
            result.update({
                "iis_status": str(iis_status),
                "iis_valid": bool(iis.valid_),
                "iis_status_enum": str(iis.status_),
                "iis_rows": len(selected_rows),
                "iis_columns": len(selected_columns),
                "iis_row_families": dict(sorted(row_counts.items())),
                "iis_row_indices": selected_rows,
                "iis_column_indices": selected_columns,
                "iis_column_names": [col_names[i] for i in selected_columns],
                "iis_rows_evidence": row_evidence,
            })
            iis_path = RESULTS / f"{model_tag}.iis.lp"
            result["iis_model_write_status"] = str(highs.writeIisModel(str(iis_path)))
            result["iis_model_file"] = str(iis_path.relative_to(ROOT))
        out_path = RESULTS / f"{model_tag}.json"
        out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2, sort_keys=True))
        return SimpleNamespace(
            success=model_status == highspy.HighsModelStatus.kOptimal,
            status=int(model_status.value),
            message=highs.modelStatusToString(model_status),
            x=np.asarray(solution.col_value, dtype=np.float64) if solution.value_valid else None,
            row_value=np.asarray(solution.row_value, dtype=np.float64) if solution.value_valid else None,
            loaded_row_upper=np.asarray(highs.getLp().row_upper_, dtype=np.float64).copy(),
            fun=float(info.objective_function_value),
            mip_dual_bound=float(info.mip_dual_bound),
            mip_gap=float(info.mip_gap),
            max_primal_infeasibility=float(getattr(info, "max_primal_infeasibility", 0.0)),
            loaded_matrix_delta=0.0,
            loaded_row_bound_delta=0.0,
        )

    module.highs_mip_solve = solve_with_iis
    return module


def main() -> None:
    spec = importlib.util.spec_from_file_location("p3d35_runner", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"LP runner could not be loaded: {RUNNER_PATH}")
    runner = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = runner
    spec.loader.exec_module(runner)
    runner.load_model = load_model
    runner.main()


if __name__ == "__main__":
    main()
