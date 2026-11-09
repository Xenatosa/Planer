#!/usr/bin/env python3
"""Locate the exact fine-grid pairs behind D1 R8/R8a hits on the adapted mesh."""
from __future__ import annotations

import argparse
import base64
import gzip
import json
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi


CELL_M = 1.2


def samp(raw: list[list[float]]) -> tuple[np.ndarray, np.ndarray]:
    path = np.asarray(raw, dtype=np.float64)
    lengths = np.hypot(*np.diff(path, axis=0).T)
    cumulative = np.r_[0.0, np.cumsum(lengths)]
    station = np.arange(0.0, cumulative[-1] + 1e-6, 0.25)
    coords = np.column_stack((
        np.interp(station, cumulative, path[:, 0]),
        np.interp(station, cumulative, path[:, 1]),
    ))
    return coords, station


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mesh", type=Path, required=True)
    ap.add_argument("--r8", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    data = json.loads(gzip.decompress(args.mesh.read_bytes()))
    r8 = json.loads(args.r8.read_text(encoding="utf-8"))
    nx, ny, rs = int(data["nx"]), int(data["ny"]), int(data["rs"])
    fs = int(data["FW"]["fs"])
    fine_shape = (ny * fs + 1, nx * fs + 1)
    G = np.frombuffer(base64.b64decode(data["G"]), dtype=np.float32).reshape(ny * rs + 1, nx * rs + 1).astype(float)
    yy, xx = np.mgrid[0:fine_shape[0], 0:fine_shape[1]]
    H = ndi.map_coordinates(G, [yy / fs * rs, xx / fs * rs], order=1)
    FW = data["FW"]
    H.flat[np.frombuffer(base64.b64decode(FW["vid"]), dtype=np.uint32)] = np.frombuffer(
        base64.b64decode(FW["h"]), dtype=np.float32,
    )

    routes = [samp(path) for path in data["rampenwege"]]
    road_cells = np.zeros((ny, nx), dtype=bool)
    for x, z in data["wege"]:
        road_cells[int(z), int(x)] = True
    weg_a = np.frombuffer(base64.b64decode(data["WEGA"]), dtype=np.uint8).reshape(ny * rs + 1, nx * rs + 1)
    road_cells |= weg_a[:-1:rs, :-1:rs] > 20
    road_mask = np.zeros(fine_shape, dtype=bool)
    for coords, _ in routes:
        road_mask[
            np.clip(np.rint(coords[:, 1] * fs).astype(int), 0, fine_shape[0] - 1),
            np.clip(np.rint(coords[:, 0] * fs).astype(int), 0, fine_shape[1] - 1),
        ] = True
    road_mask = ndi.distance_transform_edt(~road_mask) / fs <= 1.5
    road_mask[:-1, :-1] |= np.kron(road_cells, np.ones((fs, fs), dtype=bool))

    def nearest_routes(x: float, z: float) -> list[dict]:
        result = []
        q = np.asarray([x, z])
        for route_index in (2, 11):
            coords, station = routes[route_index]
            distances = np.linalg.norm(coords - q, axis=1)
            j = int(np.argmin(distances))
            result.append({
                "route": f"rampe_{route_index}",
                "station_m": round(float(station[j] * CELL_M), 4),
                "distance_m": round(float(distances[j] * CELL_M), 4),
            })
        return sorted(result, key=lambda item: (item["distance_m"], item["route"]))

    def pair_detail(a: tuple[int, int], b: tuple[int, int], ha: float, hb: float, metric: float, extra: dict | None = None) -> dict:
        pa = (a[1] / fs, a[0] / fs)
        pb = (b[1] / fs, b[0] / fs)
        return {
            "metric_m": round(float(metric), 6),
            "point_a_map": [round(pa[0], 4), round(pa[1], 4)],
            "height_a_m": round(float(ha), 6),
            "nearest_routes_a": nearest_routes(*pa),
            "point_b_map": [round(pb[0], 4), round(pb[1], 4)],
            "height_b_m": round(float(hb), 6),
            "nearest_routes_b": nearest_routes(*pb),
            **(extra or {}),
        }

    cluster_details = []
    for cluster in r8["liste"]:
        if cluster["feld"] != "D1":
            continue
        x, z = float(cluster["x"]), float(cluster["z"])
        y0, x0 = int(round(z * fs)), int(round(x * fs))
        radius = 4 * fs
        ys = slice(max(0, y0 - radius), y0 + radius + 1)
        xs = slice(max(0, x0 - radius), x0 + radius + 1)
        A, M = H[ys, xs], road_mask[ys, xs].copy()
        gy, gx = np.mgrid[ys, xs]
        M &= np.hypot(gx / fs - x, gy / fs - z) <= 4.0 + 1e-9

        st_candidates = []
        for axis in (0, 1):
            delta = np.abs(np.diff(A, axis=axis))
            valid = (M[1:, :] & M[:-1, :]) if axis == 0 else (M[:, 1:] & M[:, :-1])
            for iy, ix in zip(*np.nonzero(valid)):
                if axis == 0:
                    a = (int(gy[iy, ix]), int(gx[iy, ix]))
                    b = (a[0] + 1, a[1])
                    ha, hb = float(A[iy, ix]), float(A[iy + 1, ix])
                else:
                    a = (int(gy[iy, ix]), int(gx[iy, ix]))
                    b = (a[0], a[1] + 1)
                    ha, hb = float(A[iy, ix]), float(A[iy, ix + 1])
                st_candidates.append((float(delta[iy, ix]), a, b, ha, hb))
        max_st = max(st_candidates, key=lambda item: item[0])
        stufe = pair_detail(max_st[1], max_st[2], max_st[3], max_st[4], max_st[0])

        di = np.hypot(gx / fs - x, gy / fs - z)
        m2 = M & (di <= 2.0)
        grid = None
        if int(m2.sum()) > 10:
            fit_x = np.c_[gx[m2] / fs - x, gy[m2] / fs - z, np.ones(int(m2.sum()))]
            co = np.linalg.lstsq(fit_x, A[m2], rcond=None)[0]
            residual = np.full(A.shape, np.nan)
            residual[m2] = A[m2] - fit_x @ co
            residual_candidates = []
            for axis in (0, 1):
                if axis == 0:
                    diff = np.abs(residual[fs:, :] - residual[:-fs, :])
                    valid = np.isfinite(residual[fs:, :]) & np.isfinite(residual[:-fs, :])
                    for iy, ix in zip(*np.nonzero(valid)):
                        la, lb = (iy, ix), (iy + fs, ix)
                        aa = (int(gy[iy, ix]), int(gx[iy, ix]))
                        bb = (aa[0] + fs, aa[1])
                        residual_candidates.append((float(diff[iy, ix]), aa, bb, float(A[la]), float(A[lb]), float(residual[la]), float(residual[lb])))
                else:
                    diff = np.abs(residual[:, fs:] - residual[:, :-fs])
                    valid = np.isfinite(residual[:, fs:]) & np.isfinite(residual[:, :-fs])
                    for iy, ix in zip(*np.nonzero(valid)):
                        la, lb = (iy, ix), (iy, ix + fs)
                        aa = (int(gy[iy, ix]), int(gx[iy, ix]))
                        bb = (aa[0], aa[1] + fs)
                        residual_candidates.append((float(diff[iy, ix]), aa, bb, float(A[la]), float(A[lb]), float(residual[la]), float(residual[lb])))
            if residual_candidates:
                item = max(residual_candidates, key=lambda row: row[0])
                grid = pair_detail(item[1], item[2], item[3], item[4], item[0], {
                    "residual_a_m": round(item[5], 6), "residual_b_m": round(item[6], 6),
                    "plane_gradient_pct_xy": [round(float(co[0] * 100), 3), round(float(co[1] * 100), 3)],
                })

        m1 = M & (di <= 1.5)
        q_pct = None
        q_gradient = None
        if int(m1.sum()) > 10:
            fit_x = np.c_[gx[m1] / fs - x, gy[m1] / fs - z, np.ones(int(m1.sum()))]
            co = np.linalg.lstsq(fit_x, A[m1], rcond=None)[0]
            q_gradient = [float(co[0]), float(co[1])]
            q_pct = float(np.hypot(co[0], co[1]) * 100.0)
            if all(item["art"].endswith(("_anfang", "_ende")) for item in [cluster]):
                route_index = int(cluster["art"].split("_")[1])
                pp = routes[route_index][0]
                if cluster["art"].endswith("_anfang"):
                    dv = pp[min(8, len(pp) - 1)] - pp[0]
                else:
                    dv = pp[-1] - pp[max(0, len(pp) - 9)]
                dv = dv / max(float(np.hypot(*dv)), 1e-9)
                q_pct = float(abs(-dv[1] * co[0] + dv[0] * co[1]) * 100.0)

        cluster_details.append({
            "cluster": cluster,
            "R8_stufe_max_pair": stufe,
            "R8_gitter_max_residual_pair": grid,
            "R8_quer_pct": None if q_pct is None else round(q_pct, 3),
            "R8_quer_gradient_per_map_unit": None if q_gradient is None else [round(float(v), 6) for v in q_gradient],
        })

    # Locate every D1 ramp-end R8a maximum, using the checker’s 4 m strip mask.
    gyF, gxF = np.gradient(H, 1.0 / fs)
    wall = np.hypot(gxF, gyF) > 1.0
    endpoint_details = []
    d1_bounds = (126.0, 0.0, 168.0, 43.0)
    for route_index in (2, 11):
        p, stations = routes[route_index]
        for end_name, (q0, q1) in (
            ("anfang", (p[0], p[min(8, len(p) - 1)])),
            ("ende", (p[-1], p[max(0, len(p) - 9)])),
        ):
            if not (d1_bounds[0] <= q0[0] <= d1_bounds[2] and d1_bounds[1] <= q0[1] <= d1_bounds[3]):
                continue
            dv = q0 - q1
            dv /= max(float(np.hypot(*dv)), 1e-9)
            nv = np.array([-dv[1], dv[0]])
            y0, x0 = int(round(q0[1] * fs)), int(round(q0[0] * fs))
            r = 6 * fs
            ys = slice(max(0, y0 - r), y0 + r + 1)
            xs = slice(max(0, x0 - r), x0 + r + 1)
            yy0, xx0 = np.mgrid[ys, xs]
            rx, rz = xx0 / fs - q0[0], yy0 / fs - q0[1]
            lo, qu = rx * dv[0] + rz * dv[1], rx * nv[0] + rz * nv[1]
            mask = (
                (lo >= -1.0) & (lo <= 4.0) & (np.abs(qu) <= 2.5)
                & ~wall[ys, xs] & (xx0 > 0) & (yy0 > 0)
                & (xx0 < fine_shape[1] - 1) & (yy0 < fine_shape[0] - 1)
            )
            A = H[ys, xs]
            candidates = []
            for axis in (0, 1):
                diff = np.abs(np.diff(A, axis=axis))
                valid = (mask[1:, :] & mask[:-1, :]) if axis == 0 else (mask[:, 1:] & mask[:, :-1])
                for iy, ix in zip(*np.nonzero(valid)):
                    if axis == 0:
                        a = (int(yy0[iy, ix]), int(xx0[iy, ix])); b = (a[0] + 1, a[1])
                        ha, hb = float(A[iy, ix]), float(A[iy + 1, ix])
                    else:
                        a = (int(yy0[iy, ix]), int(xx0[iy, ix])); b = (a[0], a[1] + 1)
                        ha, hb = float(A[iy, ix]), float(A[iy, ix + 1])
                    candidates.append((float(diff[iy, ix]), a, b, ha, hb))
            if not candidates:
                continue
            item = max(candidates, key=lambda row: row[0])
            endpoint_details.append({
                "endpoint": f"rampe_{route_index}_{end_name}",
                "endpoint_map": [round(float(q0[0]), 4), round(float(q0[1]), 4)],
                "R8a_max_pair": pair_detail(item[1], item[2], item[3], item[4], item[0]),
            })

    out = {
        "surface": "neu_mesh_adapter",
        "fine_spacing_m": CELL_M / fs,
        "R8_D1_clusters": cluster_details,
        "R8a_D1_endpoints": endpoint_details,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"D1_clusters": len(cluster_details), "D1_endpoints": len(endpoint_details), "out": str(args.out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
