#!/usr/bin/env python3
"""Build the archived V24 Round05 models without solving and trace row callsites."""
from __future__ import annotations

import gzip
import importlib.util
import json
import os
from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[3]
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
if str(RELIEF3D) not in sys.path:
    sys.path.insert(0, str(RELIEF3D))
OLD = ROOT / "codex_jobs/tools/p3d20_r3/joint_mesh_r3_exact_p3d20.py"
NEW = ROOT / "codex_jobs/tools/p3d22/diagnose_slack_p3d22.py"
CUTS = ROOT / "codex_jobs/tools/p3d20_r3/event_cuts_cumulative05.json"
SOURCE = RELIEF3D / "relief_daten.json.gz"
TRANSFER = RELIEF3D / "neu/p3d18_joint_mesh_v24.json"
CENTER = (152.54985704503775, 28.48954534572434)
OUT = ROOT / "codex_jobs/tools/p3d23/results/p3d23_round05_row_callsite_diff.json"


class StopBeforeSolve(Exception):
    pass


def instrumented_load(path: Path, name: str):
    source = path.read_text(encoding="utf-8")
    add_marker = "    def add(row: dict[int, float], bound: float) -> None:\n        rid = len(rhs)\n"
    add_instrumented = (
        "    _trace_add_calls = {}\n"
        "    def add(row: dict[int, float], bound: float) -> None:\n"
        "        _callsite = sys._getframe(1).f_lineno\n"
        "        _trace_add_calls[_callsite] = _trace_add_calls.get(_callsite, 0) + 1\n"
        "        rid = len(rhs)\n"
    )
    if add_marker not in source:
        raise RuntimeError(f"add-helper marker not found in {path}")
    source = source.replace(add_marker, add_instrumented, 1)
    matrix_marker = "    matrix = coo_matrix((vals, (row_i, col_i)), shape=(len(rhs), nvars)).tocsr()\n"
    matrix_instrumented = (
        matrix_marker
        + "    globals()['_TRACE_ADD_CALLS'] = dict(_trace_add_calls)\n"
        + "    globals()['_TRACE_MATRIX_SHAPE'] = list(matrix.shape)\n"
    )
    if matrix_marker not in source:
        raise RuntimeError(f"matrix marker not found in {path}")
    source = source.replace(matrix_marker, matrix_instrumented, 1)
    module = types.ModuleType(name)
    module.__file__ = str(path)
    module.__package__ = ""
    sys.modules[name] = module
    exec(compile(source, str(path), "exec"), module.__dict__)
    return module, source


def execute(path: Path, name: str, *, modern: bool) -> dict:
    model, source_text = instrumented_load(path, name)
    model.RELIEF = SOURCE
    os.environ["P3D20_MODEL_GITTER_LIMIT"] = "0.019"
    os.environ["P3D20_MODEL_QUER_LIMIT"] = "2.95"
    os.environ["P3D20_MODEL_SINGLE_QUER_LIMIT"] = "19.5"
    os.environ["P3D20_ENDPOINT_STAGE_LOCK"] = "1"
    os.environ["P3D20_ENDPOINT_R8A_LOCK"] = "0"
    if modern:
        model.R8_GATE_CENTER = model.np.asarray(CENTER, dtype=model.np.float64)
        model.CROSSING = model.R8_GATE_CENTER.copy()
    from neu import mesh as neu_mesh
    for slot in ("22", "24"):
        neu_mesh.KREUZUNG_SETTINGS[slot]["solution_file"] = TRANSFER.name
        neu_mesh.KREUZUNG_SETTINGS[slot]["crossing_center_map"] = list(CENTER)
    with gzip.open(SOURCE, "rt", encoding="utf-8") as f:
        data = json.load(f)
    blocker = lambda *args, **kwargs: (_ for _ in ()).throw(StopBeforeSolve())
    if modern:
        model.highs_mip_solve = blocker
    else:
        model.milp = blocker
    try:
        model.solve(
            data=data, grade=0.45, r3_limit=6, out=Path("/tmp/p3d23_rowtrace_unused.json"),
            reference_mesh_path=None, axis_tolerance=0.02, plane_tolerance=0.02,
            stage_limit=0.116, quer_limit=7, wob_limit=7,
            objective_mode="diagnostic" if modern else "feasibility",
            relax_integrality=False, mip_start_path=None, mip_start_out=None,
            time_limit_s=600.0, event_cuts_path=CUTS,
            reference_solution_path=None,
            **({"diagnostic_groups": {"r3_long", "r3_quer", "r3_wob", "crossing_stage",
                                        "axis_supports", "plane_core", "endpoint_stage",
                                        "safety_gitter", "safety_quer", "safety_single_quer",
                                        "g5", "r5_hole", "r4"}} if modern else {}),
        )
    except StopBeforeSolve:
        pass
    counts = model._TRACE_ADD_CALLS
    code_lines = source_text.splitlines()
    callsites = [{"line": int(line), "rows": int(count),
                  "source": code_lines[int(line) - 1].strip()}
                 for line, count in sorted(counts.items())]
    return {"model_file": str(path), "constraints": model._TRACE_MATRIX_SHAPE[0],
            "variables": model._TRACE_MATRIX_SHAPE[1], "callsite_rows": callsites}


def main() -> None:
    old = execute(OLD, "p3d23_trace_old", modern=False)
    new = execute(NEW, "p3d23_trace_new", modern=True)
    result = {"old_p3d20_round05": old, "p3d22_diagnostic_round05": new,
              "observed_delta_rows": new["constraints"] - old["constraints"],
              "scope": "instrumented add-callsites, exact V24 source and cumulative05 cuts; solver not invoked"}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"out": str(OUT), "old": [old["variables"], old["constraints"]],
                      "new": [new["variables"], new["constraints"]],
                      "delta": result["observed_delta_rows"]}, indent=2))


if __name__ == "__main__":
    main()
