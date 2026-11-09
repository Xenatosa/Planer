#!/usr/bin/env python3
"""Write gate-sampled ramp/profile comparisons for the generated p3d15 mesh."""
from __future__ import annotations

import base64
import csv
import gzip
import json
from pathlib import Path

import numpy as np
from scipy.ndimage import map_coordinates

ROOT = Path(__file__).resolve().parents[3]
RELIEF = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
OUT = RELIEF / "pruefung/bilder_p3d15"
BOUNDS = {"D1": (126.0, 0.0, 168.0, 43.0)}
CELL_M = 1.2


def main() -> None:
    with gzip.open(RELIEF / "relief_daten.json.gz", "rt", encoding="utf-8") as f:
        source = json.load(f)
    with gzip.open(RELIEF / "neu/relief_neu.json.gz", "rt", encoding="utf-8") as f:
        package = json.load(f)
    solution = json.loads((ROOT / "codex_jobs/tools/p3d15_milp/machbarkeit_g45.json").read_text(encoding="utf-8"))
    rs = int(package["rs"])
    x0, z0, x1, z1 = BOUNDS["D1"]
    tile = package["neu_mesh_tiles"]["tiles"]["D1"]
    positions = np.frombuffer(base64.b64decode(tile["vertices_xyz_f32"]), dtype="<f4").reshape(-1, 3)
    mesh_h = positions[:, 1].reshape(int((z1 - z0) * rs) + 1, int((x1 - x0) * rs) + 1)
    source_h = np.frombuffer(base64.b64decode(source["GB"]), dtype="<f4").reshape(
        int(source["ny"]) * rs + 1, int(source["nx"]) * rs + 1,
    )

    OUT.mkdir(parents=True, exist_ok=True)
    table = OUT / "profil_tabelle.csv"
    metrics = {"variant": package["neu_mesh_tiles"]["terrain_variant"], "routes": {}}
    with table.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow((
            "route", "station_m", "x", "z", "in_D1", "source_h_m", "soll_h_m",
            "mesh_h_m", "mesh_minus_soll_m", "abs_error_le_0_02m",
        ))
        for route_index in (2, 11):
            path = np.asarray(source["rampenwege"][route_index], dtype=np.float64)
            lengths = np.hypot(*np.diff(path, axis=0).T)
            cumulative = np.r_[0.0, np.cumsum(lengths)]
            station = np.arange(0.0, cumulative[-1] + 1e-7, 0.25, dtype=np.float64)
            coords = np.column_stack((
                np.interp(station, cumulative, path[:, 0]),
                np.interp(station, cumulative, path[:, 1]),
            ))
            target = np.asarray(solution["routes"][f"rampe_{route_index}"]["h_solution"], dtype=np.float64)
            if len(target) != len(station):
                raise RuntimeError(f"rampe_{route_index}: MILP/Profilstationen verschieden lang")
            inside = (
                (coords[:, 0] >= x0 - 1e-9) & (coords[:, 0] <= x1 + 1e-9)
                & (coords[:, 1] >= z0 - 1e-9) & (coords[:, 1] <= z1 + 1e-9)
            )
            rr = (coords[inside, 1] - z0) * rs
            cc = (coords[inside, 0] - x0) * rs
            output_h = map_coordinates(mesh_h, [rr, cc], order=1, mode="nearest")
            source_values = map_coordinates(
                source_h, [coords[inside, 1] * rs, coords[inside, 0] * rs],
                order=1, mode="nearest",
            )
            difference = output_h - target[inside]
            inside_indices = np.flatnonzero(inside)
            for j, output, src, delta in zip(inside_indices, output_h, source_values, difference):
                writer.writerow((
                    f"rampe_{route_index}", f"{station[j] * CELL_M:.3f}",
                    f"{coords[j, 0]:.6f}", f"{coords[j, 1]:.6f}", "1",
                    f"{src:.9f}", f"{target[j]:.9f}", f"{output:.9f}",
                    f"{delta:.9f}", str(abs(delta) <= 0.020001),
                ))
            route_metrics = {
                "station_count_D1": int(np.count_nonzero(inside)),
                "station_count_total": int(len(station)),
                "max_abs_mesh_minus_soll_m": float(np.max(np.abs(difference))) if len(difference) else 0.0,
                "count_abs_error_over_0_02m": int(np.count_nonzero(np.abs(difference) > 0.020001)),
                "rms_mesh_minus_soll_m": float(np.sqrt(np.mean(difference ** 2))) if len(difference) else 0.0,
                "max_positive_error_m": float(np.max(difference)) if len(difference) else 0.0,
                "max_negative_error_m": float(np.min(difference)) if len(difference) else 0.0,
            }
            metrics["routes"][f"rampe_{route_index}"] = route_metrics

    solver = solution
    yy, xx = np.mgrid[0:mesh_h.shape[0], 0:mesh_h.shape[1]]
    world_x = x0 + xx / rs
    world_z = z0 + yy / rs
    dx_m = (world_x - 152.5) * CELL_M
    dz_m = (world_z - 28.5) * CELL_M
    radius = np.hypot(dx_m, dz_m)
    core = radius <= 2.25 + 1e-9
    plane = solver["Hc_m"] + solver["plane_gradient_x"] * dx_m + solver["plane_gradient_z"] * dz_m
    horizontal_core = core[:, :-1] & core[:, 1:]
    vertical_core = core[:-1, :] & core[1:, :]
    horizontal_grade = np.abs(mesh_h[:, 1:] - mesh_h[:, :-1])[horizontal_core] / (CELL_M / rs)
    vertical_grade = np.abs(mesh_h[1:, :] - mesh_h[:-1, :])[vertical_core] / (CELL_M / rs)
    metrics["plane_core"] = {
        "mesh_vertices": int(np.count_nonzero(core)),
        "max_abs_mesh_minus_plane_m": float(np.max(np.abs(mesh_h[core] - plane[core]))),
        "slope_pct": solver["plane_slope_pct"],
        "max_adjacent_grade_within_core": float(max(np.max(horizontal_grade), np.max(vertical_grade))),
    }
    metrics["mesh_hash"] = tile["height_sha256"]
    metrics["table"] = table.name
    (OUT / "profil_messung.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
