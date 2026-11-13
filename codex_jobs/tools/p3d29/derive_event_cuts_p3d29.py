#!/usr/bin/env python3
"""Derive p3d29 local cuts; retain R5 components with no recoverable outlet as diagnostics."""
from __future__ import annotations

import argparse
import base64
import gzip
import json
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi
from skimage.morphology import reconstruction

ROOT = Path(__file__).resolve().parents[3]
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
D1 = (126.0, 0.0, 168.0, 43.0)
UNSUPPORTED_R5_NO_SADDLE: list[dict] = []


def in_d1(x: float, z: float) -> bool:
    return D1[0] <= x <= D1[2] and D1[1] <= z <= D1[3]


def sample_path(raw: list[list[float]], step: float = 0.25) -> np.ndarray:
    path = np.asarray(raw, dtype=np.float64)
    length = np.r_[0.0, np.cumsum(np.hypot(*np.diff(path, axis=0).T))]
    t = np.arange(0.0, length[-1] + 1e-6, step)
    return np.column_stack((np.interp(t, length, path[:, 0]), np.interp(t, length, path[:, 1])))


def greedy_protected(current: list[dict], baseline: list[dict], count: int) -> set[int]:
    """Match baseline D1 components to nearest current components, one-to-one."""
    remaining = set(range(len(current)))
    protected: set[int] = set()
    for old in baseline[:count]:
        if not remaining:
            break
        i = min(remaining, key=lambda j: np.hypot(current[j]["x"] - old["x"], current[j]["z"] - old["z"]))
        protected.add(i)
        remaining.remove(i)
    return protected


def g5_components(g: np.ndarray, rs: int) -> list[dict]:
    gy, gx = np.gradient(g, 1.0 / rs)
    wall = np.hypot(gx, gy) > 1.0
    dist = ndi.distance_transform_edt(~wall) / rs
    dy, dx = np.gradient(ndi.gaussian_filter(dist, rs))
    norm = np.hypot(dx, dy) + 1e-9
    dx, dy = dx / norm, dy / norm
    oben = (dist > 0.0) & (dist <= 3.0) & (g > ndi.grey_dilation(g, size=7 * rs) - 1.0)
    yy, xx = np.nonzero(oben)
    ref = np.full(len(yy), -1e9, dtype=np.float64)
    for distance in (2, 3, 4, 5):
        ref = np.maximum(ref, ndi.map_coordinates(
            g, [yy + dy[yy, xx] * distance * rs, xx + dx[yy, xx] * distance * rs],
            order=1, mode="nearest",
        ))
    bb = np.zeros_like(g, dtype=np.float64)
    bb[yy, xx] = g[yy, xx] - ref
    bb *= bb > 0.6
    labels, n = ndi.label(bb > 0)
    result = []
    for k in range(1, n + 1):
        ys, xs = np.nonzero(labels == k)
        j = int(np.argmax(bb[ys, xs]))
        py, px = int(ys[j]), int(xs[j])
        x, z = px / rs, py / rs
        if not in_d1(x, z):
            continue
        events = []
        for ey, ex in zip(ys.tolist(), xs.tolist()):
            point = [float(ex / rs), float(ey / rs)]
            refs = [[point[0] + float(dx[ey, ex]) * d,
                     point[1] + float(dy[ey, ex]) * d] for d in (2, 3, 4, 5)]
            events.append({"point": point, "references": refs})
        refs = events[j]["references"]
        result.append({
            "x": float(xs.mean() / rs), "z": float(ys.mean() / rs),
            "peak": float(bb[py, px]), "point": [x, z], "references": refs,
            "pixels": int(len(xs)), "events": events,
        })
    return result


def r5_components(g: np.ndarray, land: np.ndarray, rs: int) -> list[dict]:
    seed = g.copy()
    seed[1:-1, 1:-1] = g.max()
    fill = reconstruction(seed, g, method="erosion")
    depth = fill - g
    depth[~ndi.binary_erosion(land, iterations=2 * rs)] = 0
    labels, n = ndi.label(depth > 1.0)
    result = []
    h, w = g.shape
    for k in range(1, n + 1):
        ys, xs = np.nonzero(labels == k)
        j = int(np.argmax(depth[ys, xs]))
        py, px = int(ys[j]), int(xs[j])
        x, z = px / rs, py / rs
        if not in_d1(x, z):
            continue
        level = float(fill[py, px])
        above = g >= level - 1e-5
        edge = np.zeros_like(above)
        edge[0, :] = above[0, :]
        edge[-1, :] = above[-1, :]
        edge[:, 0] |= above[:, 0]
        edge[:, -1] |= above[:, -1]
        reachable = ndi.binary_propagation(edge, structure=ndi.generate_binary_structure(2, 1), mask=above)
        near_level = reachable & (np.abs(g - level) <= 1e-4)
        sy, sx = np.nonzero(near_level)
        if len(sx) == 0:
            sy, sx = np.nonzero(reachable)
        if len(sx) == 0:
            UNSUPPORTED_R5_NO_SADDLE.append({
                "point": [x, z], "depth_m": float(depth[py, px]),
                "fill_m": level, "pixels": int(len(xs)),
            })
            continue
        saddle_index = int(np.argmin((sx - px) ** 2 + (sy - py) ** 2))
        saddle = [float(sx[saddle_index] / rs), float(sy[saddle_index] / rs)]
        result.append({
            "x": float(xs.mean() / rs), "z": float(ys.mean() / rs),
            "depth": float(depth[py, px]), "fill": level,
            "pit": [x, z], "pits": [[float(px0 / rs), float(py0 / rs)]
                                      for py0, px0 in zip(ys.tolist(), xs.tolist())],
            "saddle": saddle, "pixels": int(len(xs)),
        })
    return result


def r8b_components(data: dict, g: np.ndarray, land: np.ndarray, rs: int) -> list[dict]:
    """Rebuild r9_form.py R8b depressions with a cut saddle for each pit."""
    seed = g.copy()
    seed[1:-1, 1:-1] = g.max()
    fill = reconstruction(seed, g, method="erosion")
    depth = fill - g
    gy, gx = np.gradient(g, 1.0 / rs)
    wall = np.hypot(gx, gy) > 1.0
    road = np.zeros_like(g, dtype=bool)
    for raw in data.get("rampenwege", []):
        path = sample_path(raw, step=0.25)
        xs = np.clip(np.rint(path[:, 0] * rs).astype(int), 0, g.shape[1] - 1)
        ys = np.clip(np.rint(path[:, 1] * rs).astype(int), 0, g.shape[0] - 1)
        road[ys, xs] = True
    for item in data.get("wege", []):
        try:
            x, z = int(item[0]), int(item[1])
        except (TypeError, ValueError, IndexError):
            continue
        road[max(0, z * rs):min(g.shape[0], z * rs + rs + 1),
             max(0, x * rs):min(g.shape[1], x * rs + rs + 1)] = True
    distance_to_road = ndi.distance_transform_edt(~road) / rs
    eligible = ((depth > 0.30) & land
                & ~ndi.binary_dilation(wall, iterations=1)
                & (distance_to_road <= 6.0 + 1e-9))
    labels, count = ndi.label(eligible)
    result = []
    structure = ndi.generate_binary_structure(2, 1)
    for label in range(1, count + 1):
        ys, xs = np.nonzero(labels == label)
        if not len(xs):
            continue
        peak_index = int(np.argmax(depth[ys, xs]))
        py, px = int(ys[peak_index]), int(xs[peak_index])
        x, z = float(px / rs), float(py / rs)
        if not in_d1(x, z):
            continue
        level = float(fill[py, px])
        above = g >= level - 1e-5
        edge = np.zeros_like(above)
        edge[0, :] = above[0, :]
        edge[-1, :] = above[-1, :]
        edge[:, 0] |= above[:, 0]
        edge[:, -1] |= above[:, -1]
        reachable = ndi.binary_propagation(edge, structure=structure, mask=above)
        saddle_mask = reachable & (np.abs(g - level) <= 1e-4)
        sy, sx = np.nonzero(saddle_mask)
        if len(sx) == 0:
            sy, sx = np.nonzero(reachable)
        if len(sx) == 0:
            continue
        saddle_index = int(np.argmin((sx - px) ** 2 + (sy - py) ** 2))
        result.append({
            "x": float(xs.mean() / rs), "z": float(ys.mean() / rs),
            "depth": float(depth[py, px]), "fill": level,
            "pit": [x, z],
            "pits": [[float(xx / rs), float(yy / rs)]
                     for yy, xx in zip(ys.tolist(), xs.tolist())],
            "saddle": [float(sx[saddle_index] / rs), float(sy[saddle_index] / rs)],
            "pixels": int(len(xs)),
        })
    return result


def r4_cuts(data: dict, g: np.ndarray, rs: int) -> list[dict]:
    def hf(x: np.ndarray, z: np.ndarray) -> np.ndarray:
        return ndi.map_coordinates(g, [np.asarray(z) * rs, np.asarray(x) * rs], order=1, mode="nearest")

    cuts = []
    for route_i, raw in enumerate(data["rampenwege"]):
        p = sample_path(raw)
        inside = np.asarray([in_d1(float(x), float(z)) for x, z in p])
        if not inside.any():
            continue
        direction = np.gradient(p, axis=0)
        direction /= np.maximum(np.linalg.norm(direction, axis=1, keepdims=True), 1e-9)
        normal = np.column_stack((-direction[:, 1], direction[:, 0]))
        plus = hf(*(p + normal * 4.0).T)
        minus = hf(*(p - normal * 4.0).T)
        center = hf(*p.T)
        signal = np.minimum(plus, minus) - center
        selected = np.nonzero(signal > 1.5)[0][::16]
        for j in selected:
            if not inside[j]:
                continue
            cuts.append({
                "kind": "R4", "route": int(route_i), "sample": int(j),
                "center": p[j].tolist(),
                "sides": [(p[j] + normal[j] * 4.0).tolist(), (p[j] - normal[j] * 4.0).tolist()],
                "signal_m": float(signal[j]),
            })
    return cuts


def g6_components(data: dict, g: np.ndarray, land: np.ndarray, rs: int) -> list[dict]:
    fw = data["FW"]
    fs = int(fw["fs"])
    fine_width, fine_height = int(data["nx"]) * fs + 1, int(data["ny"]) * fs + 1
    vid = np.frombuffer(base64.b64decode(fw["vid"]), dtype=np.uint32)
    fh = np.frombuffer(base64.b64decode(fw["h"]), dtype=np.float32).astype(float)
    fine = np.full((fine_height, fine_width), np.nan, dtype=float)
    fine[vid // fine_width, vid % fine_width] = fh
    f_coarse = fine[::fs // rs, ::fs // rs][:g.shape[0], :g.shape[1]]
    visible = np.where(np.isfinite(f_coarse), f_coarse, g)
    vgy, vgx = np.gradient(visible, 1.0 / rs)
    slope = np.hypot(vgx, vgy)
    normal = np.stack((-vgx, -vgy, np.ones_like(visible)))
    normal /= np.linalg.norm(normal, axis=0)
    dn = sum(np.abs(np.diff(normal[i], axis=1))[:-1] for i in range(3))
    gy, gx = np.gradient(g, 1.0 / rs)
    wall = np.hypot(gx, gy) > 1.0
    fac = ((dn > 0.25) & (slope[:-1, :-1] > 0.15) & (slope[:-1, :-1] < 0.8)
           & land[:-1, :-1] & ~ndi.binary_dilation(wall, iterations=rs)[:-1, :-1])
    labels, n = ndi.label(fac)
    result = []
    for k in range(1, n + 1):
        ys, xs = np.nonzero(labels == k)
        if len(xs) < 6:
            continue
        max_j = int(np.argmax(dn[ys, xs]))
        py, px = int(ys[max_j]), int(xs[max_j])
        x, z = float(px / rs), float(py / rs)
        if not in_d1(float(xs.mean() / rs), float(ys.mean() / rs)):
            continue
        result.append({
            "x": float(xs.mean() / rs), "z": float(ys.mean() / rs),
            "size": int(len(xs)), "peak_dn": float(dn[py, px]),
            "point": [x, z],
        })
    return result


def r5_spike_cuts(g: np.ndarray, rs: int) -> list[dict]:
    gy, gx = np.gradient(g, 1.0 / rs)
    wall = np.hypot(gx, gy) > 1.0
    wall_dilation = ndi.binary_dilation(wall, iterations=2 * rs)
    spike = g - ndi.grey_opening(g, size=(3, 3))
    ys, xs = np.nonzero((spike > 0.5) & ~wall_dilation)
    cuts = []
    for py, px in zip(ys.tolist(), xs.tolist()):
        x, z = px / rs, py / rs
        if not in_d1(x, z):
            continue
        windows = []
        for cy in range(py - 1, py + 2):
            for cx in range(px - 1, px + 2):
                windows.append([
                    [float(xx / rs), float(yy / rs)]
                    for yy in range(cy - 1, cy + 2)
                    for xx in range(cx - 1, cx + 2)
                ])
        cuts.append({"kind": "R5sp", "point": [x, z], "windows": windows,
                     "spike_m": float(spike[py, px])})
    return cuts


def r8_gitter_cuts(data: dict, g: np.ndarray, gate: dict, rs: int) -> list[dict]:
    """Return exact least-squares residual-difference cuts for new D1 Gitter hits."""
    ny, nx = int(data["ny"]), int(data["nx"])
    fw = data["FW"]
    fs = int(fw["fs"])
    fw_width = nx * fs + 1
    vid = np.frombuffer(base64.b64decode(fw["vid"]), dtype=np.uint32)
    fine_h = np.frombuffer(base64.b64decode(fw["h"]), dtype=np.float32)
    if not np.all(vid[:-1] <= vid[1:]):
        raise RuntimeError("FW.vid ist nicht sortiert; Gitter-Schnitt braucht exakte FW-Zuordnung")

    def sample_h(xx: np.ndarray, yy: np.ndarray) -> np.ndarray:
        values = ndi.map_coordinates(g, [yy / fs * rs, xx / fs * rs], order=1)
        ids = yy.astype(np.int64) * fw_width + xx.astype(np.int64)
        positions = np.searchsorted(vid, ids)
        valid = positions < len(vid)
        matched = np.zeros(ids.shape, dtype=bool)
        matched[valid] = vid[positions[valid]] == ids[valid]
        values[matched] = fine_h[positions[matched]]
        return values

    dw = np.zeros((ny, nx), dtype=bool)
    for x, z in data["wege"]:
        dw[int(z), int(x)] = True
    dw |= np.frombuffer(base64.b64decode(data["WEGA"]), dtype=np.uint8).reshape(
        ny * rs + 1, nx * rs + 1,
    )[:-1:rs, :-1:rs] > 20
    ramps = [sample_path(route) for route in data["rampenwege"]]
    ramp_cells = np.zeros((ny, nx), dtype=bool)
    for p in ramps:
        ramp_cells[np.clip(p[:, 1].astype(int), 0, ny - 1),
                    np.clip(p[:, 0].astype(int), 0, nx - 1)] = True
    _ = dw & ~ndi.binary_dilation(ramp_cells, iterations=1)

    wm = np.zeros((ny * fs + 1, nx * fs + 1), dtype=bool)
    for p in ramps:
        wm[np.clip(np.rint(p[:, 1] * fs).astype(int), 0, ny * fs),
           np.clip(np.rint(p[:, 0] * fs).astype(int), 0, nx * fs)] = True
    wm = ndi.distance_transform_edt(~wm) / fs <= 1.5
    wm[:-1, :-1] |= np.kron(dw, np.ones((fs, fs), dtype=bool))

    cuts = []
    for item in gate.get("R8_D1_list", []):
        # r8_kreuzung.py rounds the displayed value to 3 decimals. A reported
        # 0.150 can therefore still be an official >0.15 hit before rounding.
        if float(item.get("gitter", 0.0)) < 0.15:
            continue
        x, z = float(item["x"]), float(item["z"])
        y0, x0 = int(round(z * fs)), int(round(x * fs))
        radius = 4 * fs
        ylo, yhi = max(0, y0 - radius), min(ny * fs, y0 + radius)
        xlo, xhi = max(0, x0 - radius), min(nx * fs, x0 + radius)
        yy, xx = np.mgrid[ylo:yhi + 1, xlo:xhi + 1]
        map_x, map_z = xx / fs, yy / fs
        di = np.hypot(map_x - x, map_z - z)
        local_wm = wm[ylo:yhi + 1, xlo:xhi + 1] & (di <= 4.0)
        m2 = local_wm & (di <= 2.0)
        if int(m2.sum()) <= 10:
            continue
        rows, cols = np.nonzero(m2)
        points = np.column_stack((map_x[m2], map_z[m2]))
        design = np.column_stack((points[:, 0] - x, points[:, 1] - z, np.ones(len(points))))
        heights = sample_h(xx[m2], yy[m2])
        pinv = np.linalg.pinv(design)
        residual = heights - design @ np.linalg.lstsq(design, heights, rcond=None)[0]
        grid_indices = np.full(m2.shape, -1, dtype=np.int64)
        grid_indices[m2] = np.arange(len(points))
        best = (0.0, None, None)
        for dy, dx in ((fs, 0), (0, fs)):
            for iy, ix in zip(rows.tolist(), cols.tolist()):
                jy, jx = iy + dy, ix + dx
                if jy >= m2.shape[0] or jx >= m2.shape[1] or not m2[jy, jx]:
                    continue
                ai, bi = int(grid_indices[iy, ix]), int(grid_indices[jy, jx])
                value = float(residual[ai] - residual[bi])
                if abs(value) > abs(best[0]):
                    weights = -((design[ai] - design[bi]) @ pinv)
                    weights[ai] += 1.0
                    weights[bi] -= 1.0
                    best = (value, ai, (bi, weights))
        if best[1] is None:
            continue
        value, ai, (bi, weights) = best
        cuts.append({
            "kind": "R8G", "center": [x, z], "checker_gitter_m": float(item["gitter"]),
            "pair": [points[ai].tolist(), points[bi].tolist()],
            "weights": [{"point": points[i].tolist(), "weight": float(w)}
                        for i, w in enumerate(weights) if abs(float(w)) > 1e-10],
        })
    return cuts


def r9w_cuts(data: dict, g: np.ndarray, gate: dict, rs: int) -> list[dict]:
    """Cut the weakest D1 R9w maxima until the global checker count can recover."""
    excess = max(0, int(gate.get("R9_by_rule", {}).get("R9w_wellen", 0)) - 280)
    if not excess:
        return []
    # r9_form.py reads G, independently of GB used by pruefe_regeln.py.
    gy, gx = np.gradient(g, 1.0 / rs)
    slope = np.hypot(gx, gy)
    land = np.frombuffer(base64.b64decode(data["WV"]), dtype=np.float32).reshape(g.shape) <= -900
    wall = slope > 1.0
    bp = ndi.gaussian_filter(g, rs * 0.25) - ndi.gaussian_filter(g, rs * 1.5)
    valid = ((slope > 0.15) & (slope < 0.8) & land
             & (ndi.distance_transform_edt(~wall) / rs >= 1.5)
             & (np.abs(bp) > 0.10))
    labels, n = ndi.label(valid)
    candidates = []
    # The wide Gaussian has radius 4*1.5 m. Keep the whole footprint in D1,
    # where route_field_row is the direct p3d17 transfer variable.
    margin = 6.0
    for k in range(1, n + 1):
        ys, xs = np.nonzero(labels == k)
        if len(xs) / (rs * rs) < 1.0:
            continue
        j = int(np.argmax(np.abs(bp[ys, xs])))
        py, px = int(ys[j]), int(xs[j])
        x, z = px / rs, py / rs
        if not (126.0 + margin <= x <= 168.0 - margin
                and 0.0 + margin <= z <= 43.0 - margin):
            continue
        candidates.append({"kind": "R9w", "point": [x, z],
                           "peak_m": float(abs(bp[py, px])),
                           "sign": 1 if bp[py, px] >= 0 else -1,
                           "component_center": [float(xs.mean() / rs), float(ys.mean() / rs)],
                           "pixels": int(len(xs))})
    candidates.sort(key=lambda cut: (cut["peak_m"], cut["point"][0], cut["point"][1]))
    return candidates[:excess]


def main() -> None:
    UNSUPPORTED_R5_NO_SADDLE.clear()
    ap = argparse.ArgumentParser()
    ap.add_argument("gate_json", type=Path)
    ap.add_argument("out_cuts", type=Path)
    ap.add_argument("--baseline", type=Path, default=ROOT / "codex_jobs/tools/p3d20_r3/official_gates/p3d17_reference_regeln_current_schema.json")
    ap.add_argument("--regression-reference", type=Path, default=ROOT / "codex_jobs/tools/p3d19_r3/gate_probe_ohne_regressionssperren.json")
    args = ap.parse_args()
    gate = json.loads(args.gate_json.read_text(encoding="utf-8"))
    relief_path = Path(gate["probe_relief"])
    data = json.loads(gzip.decompress(relief_path.read_bytes()))
    rs = int(data["rs"])
    g = np.frombuffer(base64.b64decode(data["GB"]), dtype=np.float32).reshape(data["ny"] * rs + 1, data["nx"] * rs + 1).astype(float)
    land = np.frombuffer(base64.b64decode(data["WV"]), dtype=np.float32).reshape(g.shape) <= -900
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    regression_baseline = json.loads(args.regression_reference.read_text(encoding="utf-8"))
    cuts: list[dict] = []

    current_g5 = g5_components(g, rs)
    old_g5 = [h for h in baseline.get("treffer", [])
              if h.get("feld") == "D1" and h.get("regel") == "G5_beule_klippe"]
    protected_g5 = greedy_protected(current_g5, old_g5, 2)
    g5_count = int(gate.get("rules_by_rule", {}).get("G5_beule_klippe", 0))
    g5_d1 = int(gate.get("D1_rules", {}).get("G5_beule_klippe", 0))
    need_g5 = max(0, g5_count - 69, g5_d1 - 2)
    extra_g5 = [i for i in range(len(current_g5)) if i not in protected_g5]
    extra_g5.sort(key=lambda i: (-current_g5[i]["peak"], current_g5[i]["x"], current_g5[i]["z"]))
    for i in extra_g5[:need_g5]:
        item = current_g5[i]
        for event in item["events"]:
            cuts.append({"kind": "G5", "point": event["point"],
                         "references": event["references"],
                         "component_center": [item["x"], item["z"]],
                         "peak_m": item["peak"]})

    current_r5 = r5_components(g, land, rs)
    old_r5 = [h for h in baseline.get("treffer", [])
              if h.get("feld") == "D1" and h.get("regel") == "R5_loch"]
    protected_r5 = greedy_protected(current_r5, old_r5, 5)
    r5_count = int(gate.get("rules_by_rule", {}).get("R5_loch", 0))
    r5_d1 = int(gate.get("D1_rules", {}).get("R5_loch", 0))
    need_r5 = max(0, r5_count - 22, r5_d1 - 5)
    extra_r5 = [i for i in range(len(current_r5)) if i not in protected_r5]
    extra_r5.sort(key=lambda i: (-current_r5[i]["depth"], current_r5[i]["x"], current_r5[i]["z"]))
    for i in extra_r5[:need_r5]:
        item = current_r5[i]
        cuts.append({"kind": "R5", "pit": item["pit"], "pits": item["pits"],
                     "saddle": item["saddle"],
                     "component_center": [item["x"], item["z"]], "depth_m": item["depth"],
                     "flood_level_m": item["fill"]})

    current_r8b = r8b_components(data, g, land, rs)
    protected_r8b: set[int] = set()
    if current_r8b:
        protected_r8b.add(min(range(len(current_r8b)),
                              key=lambda i: (current_r8b[i]["depth"],
                                             current_r8b[i]["x"], current_r8b[i]["z"])))
    r8b_d1 = int(gate.get("R9_by_tile", {}).get("D1", {}).get("R8b_delle", 0))
    need_r8b = max(0, r8b_d1 - 1)
    extra_r8b = [i for i in range(len(current_r8b)) if i not in protected_r8b]
    extra_r8b.sort(key=lambda i: (-current_r8b[i]["depth"],
                                  current_r8b[i]["x"], current_r8b[i]["z"]))
    for i in extra_r8b[:need_r8b]:
        item = current_r8b[i]
        cuts.append({"kind": "R8b", "pit": item["pit"], "pits": item["pits"],
                     "saddle": item["saddle"],
                     "component_center": [item["x"], item["z"]],
                     "depth_m": item["depth"], "flood_level_m": item["fill"]})

    current_g6 = g6_components(data, g, land, rs)
    old_g6 = [h for h in baseline.get("treffer", [])
              if h.get("feld") == "D1" and h.get("regel") == "G6_facette"]
    protected_g6 = greedy_protected(current_g6, old_g6, 3)
    g6_d1 = int(gate.get("D1_rules", {}).get("G6_facette", 0))
    need_g6 = max(0, g6_d1 - 3)
    extra_g6 = [i for i in range(len(current_g6)) if i not in protected_g6]
    extra_g6.sort(key=lambda i: (-current_g6[i]["peak_dn"], current_g6[i]["x"], current_g6[i]["z"]))
    for i in extra_g6[:need_g6]:
        item = current_g6[i]
        cuts.append({"kind": "G6", "point": item["point"],
                     "component_center": [item["x"], item["z"]], "peak_dn": item["peak_dn"],
                     "pixels": item["size"]})

    cuts.extend(r4_cuts(data, g, rs))
    current_spikes = r5_spike_cuts(g, rs)
    cuts.extend(current_spikes)
    current_r8g = r8_gitter_cuts(data, g, gate, rs)
    cuts.extend(current_r8g)
    # p3d29 deliberately derives no R9w height pin or equality band.
    current_r9w = []
    args.out_cuts.parent.mkdir(parents=True, exist_ok=True)
    args.out_cuts.write_text(json.dumps(cuts, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "candidate_G5_total_D1": [g5_count, g5_d1], "candidate_G5_components_D1": len(current_g5),
        "protected_G5": len(protected_g5), "new_G5_cuts": sum(c["kind"] == "G5" for c in cuts),
        "candidate_R5_total_D1": [r5_count, r5_d1], "candidate_R5_components_D1": len(current_r5),
        "protected_R5": len(protected_r5), "new_R5_cuts": sum(c["kind"] == "R5" for c in cuts),
        "candidate_R8b_D1": r8b_d1, "candidate_R8b_components_D1": len(current_r8b),
        "protected_R8b": len(protected_r8b), "new_R8b_cuts": sum(c["kind"] == "R8b" for c in cuts),
        "candidate_G6_D1": g6_d1, "candidate_G6_components_D1": len(current_g6),
        "protected_G6": len(protected_g6), "new_G6_cuts": sum(c["kind"] == "G6" for c in cuts),
        "new_R4_cuts": sum(c["kind"] == "R4" for c in cuts), "out": str(args.out_cuts),
        "new_R5_spitze_cuts": len(current_spikes), "new_R8_gitter_cuts": len(current_r8g),
        "new_R9w_event_cuts": 0,
        "R9w_policy": "no R9w event cuts, height pins, or equality locks",
        "unsupported_R5_without_saddle": UNSUPPORTED_R5_NO_SADDLE,
    }, indent=2))


if __name__ == "__main__":
    main()
