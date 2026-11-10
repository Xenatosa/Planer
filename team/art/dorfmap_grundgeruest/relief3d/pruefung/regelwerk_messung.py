#!/usr/bin/env python3
"""Read-only Ist-Messungen fuer REGELWERK_LANDSCHAFT_VOLLSTAENDIG.md.

Liest relief_daten.json.gz und zellen_relief.csv. Es werden weder Eingaben noch
andere Dateien geaendert. Ausgabe ist JSON nach stdout oder in eine optionale
Ausgabedatei.

Aufruf im relief3d-Ordner:
  python3 pruefung/regelwerk_messung.py
  python3 pruefung/regelwerk_messung.py relief_daten.json.gz /tmp/regelwerk.json
"""
from __future__ import annotations

import argparse
import base64
import csv
import gzip
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi


ELEMENTS = (
    "Landschaft", "Plateau", "Hang", "Gebirge", "Klippe_Wand",
    "Wandkrone", "Wandfuss", "Weg_Rampe", "Dorfweg", "Kreuzung",
    "Gabelung", "Kehre", "Wegende", "Bach_Fluss", "See", "Ufer", "Felsen",
    "Felsbloecke", "Findlinge", "Steine", "Geroell", "Deko",
    "Baeume", "Gebaeude", "Weg_Hang", "Weg_Wand", "Hang_Wand",
    "Ufer_Land", "Plateau_Hang", "Kachelnaht",
)


def read_cells(path: Path, nx: int, ny: int) -> dict[str, np.ndarray]:
    names = ("ebene", "klippe", "wand_name", "fluss_id", "ufer", "wasser_eis")
    a = {k: np.full((ny, nx), "", dtype=object) for k in names}
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            x, z = int(row["cx"]), int(row["cy"])
            for k in names:
                a[k][z, x] = row.get(k, "")
    if any(np.any(v == "") for v in (a["ebene"],)):
        raise ValueError(f"Unvollstaendige Zellkarte: {path}")
    return a


def decode_grid(data: dict, key: str, shape: tuple[int, int]) -> np.ndarray:
    return np.frombuffer(base64.b64decode(data[key]), dtype=np.float32).reshape(shape).astype(float)


def distribution(values: np.ndarray, mask: np.ndarray) -> dict:
    v = np.asarray(values)[np.asarray(mask, dtype=bool)]
    v = v[np.isfinite(v)]
    if not len(v):
        return {"n": 0, "p5": None, "median": None, "p95": None}
    p5, med, p95 = np.percentile(v, [5, 50, 95])
    return {"n": int(v.size), "p5": round(float(p5), 4), "median": round(float(med), 4), "p95": round(float(p95), 4)}


def tile_of(x: float, z: float) -> str:
    ix = int(np.clip(math.floor(x / 42), 0, 7))
    iz = int(np.clip(math.floor(z / 43), 0, 6))
    return "ABCDEFGH"[ix] + str(iz + 1)


def mark_points(tile_sets: dict[str, set[str]], element: str, points) -> None:
    for x, z in points:
        if math.isfinite(float(x)) and math.isfinite(float(z)):
            tile_sets[tile_of(float(x), float(z))].add(element)


def point_line(points: list, spacing: float = 0.5) -> np.ndarray:
    """Densify polylines at a fixed physical interval, preserving endpoints."""
    out = []
    for line in points:
        p = np.asarray(line, dtype=float)
        if len(p) == 1:
            out.append(p[0])
            continue
        for a, b in zip(p[:-1], p[1:]):
            length = float(np.linalg.norm(b - a))
            n = max(1, int(math.ceil(length / spacing)))
            out.extend(a + (b - a) * (j / n) for j in range(n))
        out.append(p[-1])
    return np.asarray(out, dtype=float).reshape((-1, 2)) if out else np.empty((0, 2))


def cell_points(mask: np.ndarray) -> np.ndarray:
    z, x = np.nonzero(mask)
    return np.column_stack((x + 0.5, z + 0.5))


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("relief", nargs="?", type=Path, default=base / "relief_daten.json.gz")
    ap.add_argument("out", nargs="?", type=Path)
    ap.add_argument("--zellen", type=Path, default=base / "zellen_relief.csv")
    args = ap.parse_args()

    with gzip.open(args.relief, "rt", encoding="utf-8") as f:
        d = json.load(f)
    nx, ny, rs = int(d["nx"]), int(d["ny"]), int(d["rs"])
    gx, gy = nx * rs + 1, ny * rs + 1
    shape = (gy, gx)
    g = decode_grid(d, "GB", shape)  # angezeigtes Endrelief
    wv = decode_grid(d, "WV", shape)
    land = wv <= -900
    dz, dx = np.gradient(g, 1 / rs)
    grad = np.hypot(dx, dz)
    slope_deg = np.degrees(np.arctan(grad))
    rough1 = np.abs(g - ndi.gaussian_filter(g, sigma=2 * rs, mode="nearest"))
    # Principal-curvature approximation; radius is reported only where |k| >= 0.02 1/m.
    gxx = ndi.gaussian_filter(g, sigma=rs, order=(0, 2), mode="nearest")
    gzz = ndi.gaussian_filter(g, sigma=rs, order=(2, 0), mode="nearest")
    gxz = ndi.gaussian_filter(g, sigma=rs, order=(1, 1), mode="nearest")
    disc = np.sqrt(np.maximum(0, ((gxx - gzz) / 2) ** 2 + gxz ** 2))
    kappa = np.maximum(np.abs((gxx + gzz) / 2 + disc), np.abs((gxx + gzz) / 2 - disc)) / np.sqrt(1 + grad ** 2)
    radius = np.divide(1, kappa, out=np.full_like(kappa, np.nan), where=kappa >= 0.02)

    c = read_cells(args.zellen, nx, ny)
    # Project 1-m cell labels onto the 0.5-m relief grid by the containing cell.
    zi = np.minimum(np.arange(gy) // rs, ny - 1)
    xi = np.minimum(np.arange(gx) // rs, nx - 1)
    labels = {k: v[zi[:, None], xi[None, :]] for k, v in c.items()}
    plateau_raw = np.isin(labels["ebene"], ["PLATEAU_NORD", "OSTPLATEAU"]) & (labels["klippe"] == "")
    plateau_interior = plateau_raw & (ndi.distance_transform_edt(plateau_raw, sampling=1 / rs) >= 4.0)
    tile_sets = defaultdict(set)
    for tile_z in range(7):
        for tile_x in range(8):
            tile_sets["ABCDEFGH"[tile_x] + str(tile_z + 1)].add("Landschaft")

    cell_masks = {
        "Plateau": np.isin(c["ebene"], ["PLATEAU_NORD", "OSTPLATEAU"]) & (c["klippe"] == ""),
        "Hang": c["ebene"] == "HANG",
        "Gebirge": (c["wand_name"] != "") | np.isin(c["ebene"], ["KRATERRAND", "KRATER", "GIPFEL", "SIMS"]),
        "Klippe_Wand": (c["klippe"] == "WAND") | (c["ebene"] == "WAND"),
        "Wandkrone": c["klippe"] == "WAND_OBEN",
        "Wandfuss": c["klippe"] == "WAND_FUSS",
        "Bach_Fluss": np.char.find(c["fluss_id"].astype(str), "BACH") >= 0,
        "See": c["fluss_id"] == "SEE",
        "Ufer": c["ufer"] == "1",
    }
    for element, mask in cell_masks.items():
        mark_points(tile_sets, element, cell_points(mask))

    masks = {
        "Landschaft": land,
        "Plateau": plateau_interior,
        "Hang": labels["ebene"] == "HANG",
        "Gebirge": (labels["wand_name"] != "") | np.isin(labels["ebene"], ["KRATERRAND", "KRATER", "GIPFEL", "SIMS"]),
        "Klippe_Wand": (labels["klippe"] == "WAND") | (labels["ebene"] == "WAND"),
        "Wandkrone": labels["klippe"] == "WAND_OBEN",
        "Wandfuss": labels["klippe"] == "WAND_FUSS",
        "Bach_Fluss": np.char.find(labels["fluss_id"].astype(str), "BACH") >= 0,
        "See": labels["fluss_id"] == "SEE",
        "Ufer": (labels["ufer"] == "1") | ((ndi.binary_dilation(wv > -900, iterations=1)) & land),
    }

    # Current masks/cell counts are kept separate from the fine-grid metric samples.
    source_cells = {}
    for name in ("Plateau", "Hang", "Gebirge", "Klippe_Wand", "Wandkrone", "Wandfuss", "Bach_Fluss", "See", "Ufer"):
        source_cells[name] = int(np.count_nonzero({
            "Plateau": np.isin(c["ebene"], ["PLATEAU_NORD", "OSTPLATEAU"]) & (c["klippe"] == ""),
            "Hang": c["ebene"] == "HANG",
            "Gebirge": (c["wand_name"] != "") | np.isin(c["ebene"], ["KRATERRAND", "KRATER", "GIPFEL", "SIMS"]),
            "Klippe_Wand": (c["klippe"] == "WAND") | (c["ebene"] == "WAND"),
            "Wandkrone": c["klippe"] == "WAND_OBEN",
            "Wandfuss": c["klippe"] == "WAND_FUSS",
            "Bach_Fluss": np.char.find(c["fluss_id"].astype(str), "BACH") >= 0,
            "See": c["fluss_id"] == "SEE",
            "Ufer": c["ufer"] == "1",
        }[name]))

    stats = {}
    for name, mask in masks.items():
        m = mask & land
        stats[name] = {
            "source_cells_1m": source_cells.get(name),
            "slope_deg": distribution(slope_deg, m),
            "rough1m_m": distribution(rough1, m),
            "curvature_radius_m": distribution(radius, m & np.isfinite(radius)),
            "height_m": distribution(g, m),
        }
    stats["Landschaft"].update({
        "slope_deg": distribution(slope_deg, land),
        "rough1m_m": distribution(rough1, land),
        "curvature_radius_m": distribution(radius, land & np.isfinite(radius)),
        "height_m": distribution(g, land),
    })
    water = wv > -900
    depth = wv - g
    stream_water = water & (np.char.find(labels["fluss_id"].astype(str), "BACH") >= 0)
    lake_water = water & (labels["fluss_id"] == "SEE")
    stats["Bach_Fluss"] = {
        "source_cells_1m": source_cells["Bach_Fluss"],
        "water_depth_m": distribution(depth, stream_water),
        "bed_slope_deg": distribution(slope_deg, stream_water),
        "bed_rough1m_m": distribution(rough1, stream_water),
        "slope_deg": distribution(slope_deg, masks["Bach_Fluss"] & land),
        "rough1m_m": distribution(rough1, masks["Bach_Fluss"] & land),
        "curvature_radius_m": distribution(radius, masks["Bach_Fluss"] & land & np.isfinite(radius)),
        "height_m": distribution(g, masks["Bach_Fluss"] & land),
    }
    stats["See"] = {
        "source_cells_1m": source_cells["See"],
        "water_depth_m": distribution(depth, lake_water),
        "bed_slope_deg": distribution(slope_deg, lake_water),
        "bed_rough1m_m": distribution(rough1, lake_water),
        "slope_deg": distribution(slope_deg, masks["See"] & land),
        "rough1m_m": distribution(rough1, masks["See"] & land),
        "curvature_radius_m": distribution(radius, masks["See"] & land & np.isfinite(radius)),
        "height_m": distribution(g, masks["See"] & land),
    }

    # Road and object geometry comes directly from the serialized viewer inputs.
    ramp_lines = d.get("rampenwege", [])
    ramps = point_line(ramp_lines)
    village = np.asarray(d.get("wege", []), dtype=float).reshape((-1, 2))
    ramp_grid = np.zeros((ny, nx), dtype=bool)
    if len(ramps):
        ix = np.clip(np.floor(ramps[:, 0]).astype(int), 0, nx - 1)
        iz = np.clip(np.floor(ramps[:, 1]).astype(int), 0, ny - 1)
        ramp_grid[iz, ix] = True
    road_grid = np.zeros((ny, nx), dtype=bool)
    if len(village):
        ix = np.clip(village[:, 0].astype(int), 0, nx - 1)
        iz = np.clip(village[:, 1].astype(int), 0, ny - 1)
        road_grid[iz, ix] = True
    mark_points(tile_sets, "Weg_Rampe", ramps)
    mark_points(tile_sets, "Dorfweg", village + 0.5)
    road = ramp_grid | road_grid
    # Four-neighbour degree marks village-road junction cells. Curves use a
    # reproducible heading-change threshold over a 2-m chord on each polyline.
    junc = np.zeros_like(road_grid)
    forks = np.zeros_like(road_grid)
    for y, x in zip(*np.nonzero(road_grid)):
        deg = sum(0 <= y + dy < ny and 0 <= x + dx < nx and road_grid[y + dy, x + dx]
                  for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)))
        if deg >= 4:
            junc[y, x] = True
        elif deg == 3:
            forks[y, x] = True
    mark_points(tile_sets, "Kreuzung", cell_points(junc))
    mark_points(tile_sets, "Gabelung", cell_points(forks))
    ends = []
    hairpins = []
    for line in ramp_lines:
        p = np.asarray(line, dtype=float)
        if len(p):
            ends.extend([p[0], p[-1]])
        for i in range(2, len(p) - 2):
            a = p[i] - p[i - 2]
            b = p[i + 2] - p[i]
            den = np.linalg.norm(a) * np.linalg.norm(b)
            if den and math.degrees(math.acos(float(np.clip(np.dot(a, b) / den, -1, 1)))) >= 90:
                hairpins.append(p[i])
    mark_points(tile_sets, "Wegende", ends)
    mark_points(tile_sets, "Kehre", hairpins)

    # Intersections between distinct ramp centerlines; deduplicated to 1-m squares.
    from scipy.spatial import cKDTree
    intersections = []
    for i, line_a in enumerate(ramp_lines):
        pa = point_line([line_a])
        if not len(pa):
            continue
        for line_b in ramp_lines[i + 1:]:
            pb = point_line([line_b])
            if not len(pb):
                continue
            dd, jj = cKDTree(pb).query(pa, distance_upper_bound=1.5)
            hit = np.isfinite(dd)
            if np.any(hit):
                intersections.extend((pa[hit] + pb[jj[hit]]) / 2)
    if intersections:
        unique = sorted({(round(float(x)), round(float(z))) for x, z in intersections})
        mark_points(tile_sets, "Kreuzung", unique)

    # Class transitions from source cell labels; each cell and object is assigned
    # using the same x//42, z//43 convention as the O18 gate scripts.
    def mark_boundary(element: str, mask: np.ndarray) -> None:
        mark_points(tile_sets, element, cell_points(mask))

    # Explicit class adjacency, with the boundary attributed to both cells.
    def adjacent(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        m = np.zeros((ny, nx), dtype=bool)
        for dy, dx0 in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            shifted = np.zeros_like(b)
            ys = slice(max(0, dy), min(ny, ny + dy))
            xs = slice(max(0, dx0), min(nx, nx + dx0))
            srcy = slice(max(0, -dy), min(ny, ny - dy))
            srcx = slice(max(0, -dx0), min(nx, nx - dx0))
            shifted[ys, xs] = b[srcy, srcx]
            m |= a & shifted
            shifted_a = np.zeros_like(a)
            shifted_a[ys, xs] = a[srcy, srcx]
            m |= b & shifted_a
        return m

    plateau = np.isin(c["ebene"], ["PLATEAU_NORD", "OSTPLATEAU"]) & (c["klippe"] == "")
    hang = c["ebene"] == "HANG"
    wand = (c["klippe"] == "WAND") | (c["ebene"] == "WAND")
    mark_boundary("Plateau_Hang", adjacent(plateau, hang))
    mark_boundary("Hang_Wand", adjacent(hang, wand))
    # Way to terrain transition zones (within 2 m of the route/corridor).
    dist_road = ndi.distance_transform_edt(~road_grid)
    mark_boundary("Weg_Hang", (dist_road <= 2) & (c["ebene"] == "HANG"))
    mark_boundary("Weg_Wand", (dist_road <= 2) & ((c["klippe"] == "WAND") | (c["ebene"] == "WAND")))
    mark_boundary("Ufer_Land", (c["ufer"] == "1") | ((ndi.binary_dilation(c["wasser_eis"] == "1") & (c["wasser_eis"] == "0"))))
    # All 56 tiles participate in at least one internal tile seam.
    for tile in tile_sets:
        tile_sets[tile].add("Kachelnaht")

    def object_stats(key: str, size_index: int, height_index: int | None = None) -> dict:
        objs = d.get(key, [])
        sizes = np.asarray([float(o[size_index]) for o in objs], dtype=float)
        result = {"count": len(objs), "size_parameter_m": distribution(sizes, np.ones(len(sizes), dtype=bool))}
        if height_index is not None:
            heights = np.asarray([float(o[height_index]) for o in objs], dtype=float)
            result["height_parameter_m"] = distribution(heights, np.ones(len(heights), dtype=bool))
        return result

    object_measurements = {
        "Baeume": object_stats("baeume", 3),
        "Felsen": object_stats("felsen", 3),
        "Felsbloecke": {"count": len(d.get("felsbloecke", [])), "size_parameter_m": distribution(np.array([]), np.array([], dtype=bool))},
        "Findlinge": object_stats("findlinge", 3),
        "Steine": object_stats("steine", 3),
        "Geroell": object_stats("geroell", 3),
        "Deko": object_stats("gras", 3),
        "Gebaeude": {
            "count": len(d.get("haeuser", [])),
            "width_m": distribution(np.asarray([h["b"] for h in d.get("haeuser", [])], dtype=float), np.ones(len(d.get("haeuser", [])), bool)),
            "depth_m": distribution(np.asarray([h["t"] for h in d.get("haeuser", [])], dtype=float), np.ones(len(d.get("haeuser", [])), bool)),
            "height_parameter_m": distribution(np.asarray([h["h"] for h in d.get("haeuser", [])], dtype=float), np.ones(len(d.get("haeuser", [])), bool)),
        },
    }
    obj_key_to_element = {"baeume": "Baeume", "felsen": "Felsen", "felsbloecke": "Felsbloecke", "findlinge": "Findlinge", "steine": "Steine", "geroell": "Geroell", "gras": "Deko", "haeuser": "Gebaeude"}
    for key, element in obj_key_to_element.items():
        for o in d.get(key, []):
            mark_points(tile_sets, element, [(float(o[0]), float(o[2]))] if key != "haeuser" else [(float(o["x"]), float(o["z"]))])

    # Quantify rendered road/shore metrics on the end relief.
    def point_metric(points: np.ndarray) -> dict:
        if not len(points):
            empty = np.array([])
            return {"slope_deg": distribution(empty, empty), "rough1m_m": distribution(empty, empty), "curvature_radius_m": distribution(empty, empty), "height_m": distribution(empty, empty)}
        coords = np.vstack((np.clip(points[:, 1] * rs, 0, gy - 1), np.clip(points[:, 0] * rs, 0, gx - 1)))
        return {"slope_deg": distribution(ndi.map_coordinates(slope_deg, coords, order=1), np.ones(len(points), bool)),
                "rough1m_m": distribution(ndi.map_coordinates(rough1, coords, order=1), np.ones(len(points), bool)),
                "curvature_radius_m": distribution(ndi.map_coordinates(radius, coords, order=1), np.ones(len(points), bool)),
                "height_m": distribution(ndi.map_coordinates(g, coords, order=1), np.ones(len(points), bool))}
    stats["Weg_Rampe"] = {"count": len(ramp_lines), "sample_points_0_5m": len(ramps), **point_metric(ramps)}
    stats["Dorfweg"] = {"count_cells": int(road_grid.sum()), **point_metric(village + 0.5)}
    stats["Wegende"] = {"count_endpoints": len(ends), **point_metric(np.asarray(ends, dtype=float).reshape((-1, 2)))}
    stats["Ufer"] = {**stats.get("Ufer", {}), "water_edge_slope_deg": distribution(slope_deg, masks["Ufer"] & land),
                     "rough1m_m": distribution(rough1, masks["Ufer"] & land),
                     "curvature_radius_m": distribution(radius, masks["Ufer"] & land & np.isfinite(radius))}

    def transition_steps(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        steps = []
        for dy, dx0 in ((1, 0), (0, 1)):
            aa = a.copy()
            bb = b.copy()
            if dy:
                m = aa[:-1, :] & bb[1:, :]
                y0, x0 = np.nonzero(m)
                if len(y0):
                    p0 = np.vstack(((y0 + 0.5) * rs, (x0 + 0.5) * rs))
                    p1 = np.vstack(((y0 + 1.5) * rs, (x0 + 0.5) * rs))
                    steps.extend(np.abs(ndi.map_coordinates(g, p0, order=1) - ndi.map_coordinates(g, p1, order=1)))
                m = bb[:-1, :] & aa[1:, :]
                y0, x0 = np.nonzero(m)
                if len(y0):
                    p0 = np.vstack(((y0 + 0.5) * rs, (x0 + 0.5) * rs))
                    p1 = np.vstack(((y0 + 1.5) * rs, (x0 + 0.5) * rs))
                    steps.extend(np.abs(ndi.map_coordinates(g, p0, order=1) - ndi.map_coordinates(g, p1, order=1)))
            else:
                m = aa[:, :-1] & bb[:, 1:]
                y0, x0 = np.nonzero(m)
                if len(y0):
                    p0 = np.vstack(((y0 + 0.5) * rs, (x0 + 0.5) * rs))
                    p1 = np.vstack(((y0 + 0.5) * rs, (x0 + 1.5) * rs))
                    steps.extend(np.abs(ndi.map_coordinates(g, p0, order=1) - ndi.map_coordinates(g, p1, order=1)))
                m = bb[:, :-1] & aa[:, 1:]
                y0, x0 = np.nonzero(m)
                if len(y0):
                    p0 = np.vstack(((y0 + 0.5) * rs, (x0 + 0.5) * rs))
                    p1 = np.vstack(((y0 + 0.5) * rs, (x0 + 1.5) * rs))
                    steps.extend(np.abs(ndi.map_coordinates(g, p0, order=1) - ndi.map_coordinates(g, p1, order=1)))
        return np.asarray(steps, dtype=float)

    plateau_cells = np.isin(c["ebene"], ["PLATEAU_NORD", "OSTPLATEAU"]) & (c["klippe"] == "")
    hang_cells = c["ebene"] == "HANG"
    wall_cells = (c["klippe"] == "WAND") | (c["ebene"] == "WAND")
    water_cells = c["wasser_eis"] == "1"
    land_cells = ~water_cells
    ph_step = transition_steps(plateau_cells, hang_cells)
    hw_step = transition_steps(hang_cells, wall_cells)
    ul_step = transition_steps(water_cells, land_cells)
    transitions = {
        "Plateau_Hang_step_m": distribution(ph_step, np.ones(len(ph_step), bool)),
        "Hang_Wand_step_m": distribution(hw_step, np.ones(len(hw_step), bool)),
        "Ufer_Land_step_m": distribution(ul_step, np.ones(len(ul_step), bool)),
    }
    # A global mesh shares exact seam vertices. Measure the slope-gradient change
    # from the 0.5-m cells immediately before and after each internal tile line.
    seam_changes = []
    for x_cell in range(42, nx, 42):
        i = x_cell * rs
        left = (g[:, i] - g[:, i - 1]) * rs
        right = (g[:, i + 1] - g[:, i]) * rs
        seam_changes.extend(np.abs(np.degrees(np.arctan(left)) - np.degrees(np.arctan(right))))
    for z_cell in range(43, ny, 43):
        j = z_cell * rs
        north = (g[j, :] - g[j - 1, :]) * rs
        south = (g[j + 1, :] - g[j, :]) * rs
        seam_changes.extend(np.abs(np.degrees(np.arctan(north)) - np.degrees(np.arctan(south))))
    transitions["Kachelnaht_slope_delta_deg"] = distribution(np.asarray(seam_changes), np.ones(len(seam_changes), bool))

    # Map dimensions in the shared coordinate system, plus per-tile inventory.
    tiles = {}
    for iz in range(7):
        for ix in range(8):
            name = "ABCDEFGH"[ix] + str(iz + 1)
            tiles[name] = {"elements": sorted(tile_sets[name], key=ELEMENTS.index)}
    result = {
        "input": {"relief": str(args.relief), "zellen": str(args.zellen), "relief_field": "GB (sichtbares Endrelief)",
                  "nx": nx, "ny": ny, "rs": rs, "tile_formula": "ABCDEFGH[x//42] + str(z//43+1)"},
        "measure_definitions": {"slope_deg": "atan(|gradient(GB)|), spacing 1/rs m",
                                "rough1m_m": "abs(GB - Gaussian(GB, sigma=1 m))",
                                "curvature_radius_m": "1/max(abs(principal curvature)); only |curvature| >= 0.02 1/m",
                                "Plateau metric domain": "interior of PLATEAU_NORD/OSTPLATEAU, at least 4 m from class edge, outside klippe-tagged cells",
                                "water_depth_m": "WV - GB on WV > -900",
                                "object_size_parameter_m": "serialized object parameter at index 3; not a full mesh bounding-box measurement"},
        "stats": stats,
        "transitions": transitions,
        "objects": object_measurements,
        "tiles": tiles,
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)
    if args.out:
        args.out.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
