#!/usr/bin/env python3
"""Re-run the p3d30 hard V1 model and capture a HiGHS IIS for p3d31 step 0."""
from __future__ import annotations

import importlib.util
import inspect
import json
import os
from pathlib import Path
import sys

import numpy as np
from scipy.sparse import csr_matrix

ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "codex_jobs/tools/p3d31/results"
RESULTS.mkdir(parents=True, exist_ok=True)
HIGHSPY_DIR = Path("/tmp/p3d18_highspy")
if str(HIGHSPY_DIR) not in sys.path:
    sys.path.insert(0, str(HIGHSPY_DIR))
import highspy  # noqa: E402

RUN_DIAGNOSTIC_PATH = ROOT / "codex_jobs/tools/p3d30/run_diagnostic.py"


def load_p3d30_model():
    tool_dir = ROOT / "codex_jobs/tools/p3d30"
    if str(tool_dir) not in sys.path:
        sys.path.insert(0, str(tool_dir))
    path = tool_dir / "diagnose_slack_p3d30.py"
    spec = importlib.util.spec_from_file_location("p3d31_step0_p3d30_model", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("p3d30 diagnostic model could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    def solve_with_iis(matrix, rhs, objective, integrality, lower, upper,
                       start=None, time_limit=600.0):
        caller = inspect.currentframe().f_back
        families = list(caller.f_locals["row_families"])
        lp = highspy.HighsLp()
        lp.num_col_ = int(matrix.shape[1])
        lp.num_row_ = int(matrix.shape[0])
        lp.col_cost_ = np.array(objective, dtype=np.float64, copy=True)
        lp.col_lower_ = np.array(lower, dtype=np.float64, copy=True)
        lp.col_upper_ = np.array(upper, dtype=np.float64, copy=True)
        lp.row_lower_ = np.full(matrix.shape[0], -np.inf, dtype=np.float64)
        lp.row_upper_ = np.array(rhs, dtype=np.float64, copy=True)
        lp.sense_ = highspy.ObjSense.kMinimize
        columns = matrix.tocsc()
        lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
        lp.a_matrix_.start_ = columns.indptr.astype(np.int32, copy=True)
        lp.a_matrix_.index_ = columns.indices.astype(np.int32, copy=True)
        lp.a_matrix_.value_ = columns.data.astype(np.float64, copy=True)
        lp.integrality_ = [
            highspy.HighsVarType.kInteger if value else highspy.HighsVarType.kContinuous
            for value in np.asarray(integrality, dtype=np.uint8)
        ]
        highs = highspy.Highs()
        for name, value in (
            ("output_flag", False), ("presolve", "on"), ("threads", 1),
            ("mip_rel_gap", 0.0), ("time_limit", float(time_limit)),
            ("small_matrix_value", 1e-12),
        ):
            highs.setOptionValue(name, value)
        if os.environ.get("P3D31_STEP0_RELAX") == "1":
            # HiGHS' default light strategy only catches trivial bound conflicts.
            # Strategy 6 requests the LP elasticity filter plus reduction to an IIS.
            highs.setOptionValue("iis_strategy", 6)
        status = highs.passModel(lp)
        if status not in (highspy.HighsStatus.kOk, highspy.HighsStatus.kWarning):
            raise RuntimeError(f"Highs passModel failed: {status}")
        highs.run()
        model_status = highs.getModelStatus()
        result = {
            "highspy_version": highs.version(),
            "model_status": highs.modelStatusToString(model_status),
            "status_code": int(model_status.value),
            "variables": int(matrix.shape[1]),
            "constraints": int(matrix.shape[0]),
            "time_limit_s": float(time_limit),
            "threads": 1,
            "iis_attempted": False,
        }
        if model_status == highspy.HighsModelStatus.kInfeasible:
            result["iis_attempted"] = True
            iis_status, iis = highs.getIis()
            row_counts: dict[str, int] = {}
            row_examples: dict[str, list[int]] = {}
            edge_height_rows = [
                i for i, family in enumerate(families)
                if family == "p3d30_drainage_selected_edge_height"
            ]
            successor_rows = [
                i for i, family in enumerate(families)
                if family == "p3d30_drainage_successor_choice"
            ]
            candidates = caller.f_locals.get("drainage_candidates", [])
            construction = caller.f_locals.get("construction", {})
            ref = np.asarray(construction.get("reference_height_m", []), dtype=np.float64)
            coverage = np.asarray(caller.f_locals.get("transfer_coverage", []), dtype=np.float64)
            active = np.asarray(construction.get("active_mask", []), dtype=bool)
            core = np.asarray(construction.get("core_mask", []), dtype=bool)
            ring = np.asarray(construction.get("ring_mask", []), dtype=bool)
            geometry = {key: float(construction[key]) for key in ("x0", "z0")}
            fs, width = int(construction.get("fs", 1)), int(construction.get("width", 1))

            def xz(flat_index: int) -> list[float]:
                iz, ix = divmod(int(flat_index), width)
                return [geometry["x0"] + ix / fs, geometry["z0"] + iz / fs]

            edge_details = []
            for raw_index in iis.row_index_:
                index = int(raw_index)
                if index not in edge_height_rows:
                    continue
                edge_index = edge_height_rows.index(index)
                if edge_index >= len(candidates):
                    continue
                child, parent_node, eps = candidates[edge_index]
                cz, cx = divmod(int(child), width)
                pz, px = divmod(int(parent_node), width)
                edge_details.append({
                    "row_index": index, "edge_index": edge_index,
                    "child_flat": int(child), "successor_flat": int(parent_node),
                    "child_xz": xz(child), "successor_xz": xz(parent_node),
                    "required_eps_m": float(eps),
                    "p3d17_child_height_m": float(ref[cz, cx]),
                    "p3d17_successor_height_m": float(ref[pz, px]),
                    "reference_successor_minus_child_m": float(ref[pz, px] - ref[cz, cx]),
                    "child_transfer_coverage": float(coverage[cz, cx]),
                    "successor_transfer_coverage": float(coverage[pz, px]),
                    "child_work_area_core": bool(core[cz, cx]),
                    "child_work_area_ring": bool(ring[cz, cx]),
                    "successor_work_area_core": bool(core[pz, px]),
                    "successor_work_area_ring": bool(ring[pz, px]),
                })
            successor_row_details = []
            for raw_index in iis.row_index_:
                index = int(raw_index)
                if index not in successor_rows:
                    continue
                rank = successor_rows.index(index)
                node_rank = rank // 2
                nodes = caller.f_locals.get("drainage_nodes", [])
                if node_rank < len(nodes):
                    node = int(nodes[node_rank])
                    successors = [
                        {"flat": int(item[1]), "xz": xz(int(item[1]))}
                        for item in candidates if int(item[0]) == node
                    ]
                    successor_row_details.append({
                        "row_index": index, "sense": "sum(y)<=1" if rank % 2 == 0 else "sum(y)>=1",
                        "child_flat": node, "child_xz": xz(node),
                        "successors": successors,
                    })
            for raw_index in iis.row_index_:
                index = int(raw_index)
                family = families[index] if index < len(families) else "<unknown>"
                row_counts[family] = row_counts.get(family, 0) + 1
                if len(row_examples.setdefault(family, [])) < 8:
                    row_examples[family].append(index)
            result.update({
                "iis_status": str(iis_status),
                "iis_valid": bool(iis.valid_),
                "iis_status_enum": str(iis.status_),
                "iis_rows": int(len(iis.row_index_)),
                "iis_columns": int(len(iis.col_index_)),
                "iis_row_status_at_indices": [
                    int(iis.row_status_[int(index)]) for index in iis.row_index_
                ],
                "iis_column_status_at_indices": [
                    int(iis.col_status_[int(index)]) for index in iis.col_index_
                ],
                "iis_row_families": dict(sorted(row_counts.items())),
                "iis_row_examples": dict(sorted(row_examples.items())),
                "iis_drainage_edge_details": edge_details,
                "iis_drainage_successor_details": successor_row_details,
                "iis_row_indices": [int(v) for v in iis.row_index_],
                "iis_column_indices": [int(v) for v in iis.col_index_],
            })
            # Also preserve the solver-native irreducible subsystem if available.
            label = "lp" if os.environ.get("P3D31_STEP0_RELAX") == "1" else "hard_v1"
            iis_path = RESULTS / f"p3d31_step0_{label}_iis.ilp"
            write_status = highs.writeIisModel(str(iis_path))
            result["iis_model_file"] = str(iis_path.relative_to(ROOT))
            result["iis_model_write_status"] = str(write_status)
        else:
            result["iis_note"] = "HiGHS did not return an infeasible model status; no IIS requested."
        label = "lp" if os.environ.get("P3D31_STEP0_RELAX") == "1" else "hard_v1"
        out = RESULTS / f"p3d31_step0_{label}_iis.json"
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2, sort_keys=True))
        info = highs.getInfo()
        solution = highs.getSolution()
        return module.SimpleNamespace(
            success=False,
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
    spec = importlib.util.spec_from_file_location("p3d31_step0_run_diagnostic", RUN_DIAGNOSTIC_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("p3d30 run_diagnostic.py could not be loaded")
    runner = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = runner
    spec.loader.exec_module(runner)
    runner.load_model = load_p3d30_model
    relief3d = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
    if str(relief3d) not in sys.path:
        sys.path.insert(0, str(relief3d))
    source = Path("/tmp/p3d22_v3_source.json.gz")
    transfer = ROOT / "team/art/dorfmap_grundgeruest/relief3d/neu/p3d21_transfer_base_route3_v29.json"
    cuts = ROOT / "codex_jobs/tools/p3d30/results/p3d30_V3_R00_cuts.json"
    relax = os.environ.get("P3D31_STEP0_RELAX") == "1"
    label = "lp" if relax else "hard_v1"
    sys.argv = [
        str(RUN_DIAGNOSTIC_PATH), "--geometry", "V3", "--scenario", "joint",
        "--source-relief", str(source), "--transfer-base", str(transfer),
        "--r8-center", "152.6292918620858", "28.353590994151514",
        "--event-cuts", str(cuts), "--out",
        str(RESULTS / f"p3d31_step0_{label}_model.json"),
        "--time-limit", "600", "--keep-solution", "--objective-mode", "step",
        "--reference-solution",
        str(ROOT / "team/art/dorfmap_grundgeruest/relief3d/neu/p3d17_joint_mesh_v22.json"),
        "--groups",
    ]
    if relax:
        sys.argv.append("--relax-integrality")
    os.environ["P3D30_DRAINAGE_MODE"] = "hard"
    os.environ["P3D30_DRAINAGE_VARIANT"] = "1"
    runner.main()


if __name__ == "__main__":
    main()
