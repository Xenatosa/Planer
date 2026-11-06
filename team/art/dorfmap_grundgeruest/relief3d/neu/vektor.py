"""Vektorisierte Landschaftselemente aus den unveraenderten Zellquellen."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi
from shapely.geometry import MultiPoint, Polygon, box
from shapely.ops import unary_union
from skimage.morphology import skeletonize

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "raster_c20_z25_zellen.csv"
OVERLAY = ROOT.parent / "raster_c20_z25_overlay_plaetze_wege.csv"
OUT = ROOT / "neu"
NX, NY = 336, 303
TILE_W, TILE_H = 42, 43
CELL_M = 1.2
PROTOTYPE_TILES = ("D1", "G1", "D2")
TILE_COLS = "ABCDEFGH"


def tile_name(x: int, y: int) -> str:
    return f"{TILE_COLS[min(7, x // TILE_W)]}{min(6, y // TILE_H) + 1}"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _curves(nodes: set[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    """Zerlegt ein Zellnetz in deterministische Trails, die jede Kante abdecken."""
    if not nodes:
        return []
    adj: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for x, y in nodes:
        adj[(x, y)] = sorted(
            (x + dx, y + dy)
            for dy in (-1, 0, 1)
            for dx in (-1, 0, 1)
            if (dx or dy) and (x + dx, y + dy) in nodes
        )
    edges = {tuple(sorted((a, b))) for a, ns in adj.items() for b in ns}
    used: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    trails: list[list[tuple[int, int]]] = []
    starts = sorted(p for p in nodes if len(adj[p]) != 2)
    for start in starts:
        if not adj[start]:
            trails.append([start])
            continue
        for nxt in adj[start]:
            edge = tuple(sorted((start, nxt)))
            if edge in used:
                continue
            path = [start, nxt]
            used.add(edge)
            prev, cur = start, nxt
            while True:
                choices = [p for p in adj[cur] if p != prev and tuple(sorted((cur, p))) not in used]
                if not choices:
                    break
                nxt2 = choices[0]
                used.add(tuple(sorted((cur, nxt2))))
                path.append(nxt2)
                prev, cur = cur, nxt2
            trails.append(path)
    for a, b in sorted(edges):
        if (a, b) in used:
            continue
        path = [a, b]
        used.add((a, b))
        prev, cur = a, b
        while True:
            choices = [p for p in adj[cur] if p != prev and tuple(sorted((cur, p))) not in used]
            if not choices:
                break
            nxt = choices[0]
            used.add(tuple(sorted((cur, nxt))))
            path.append(nxt)
            prev, cur = cur, nxt
        trails.append(path)
    return trails


def _spline(cells: list[tuple[int, int]], spacing_m: float = 0.30) -> list[list[float]]:
    points = np.asarray([[(x + 0.5) * CELL_M, (y + 0.5) * CELL_M] for x, y in cells], dtype=np.float64)
    if len(points) == 1:
        return [[round(float(points[0, 0]), 4), round(float(points[0, 1]), 4)]]
    out: list[np.ndarray] = []
    for i in range(len(points) - 1):
        p0 = points[max(0, i - 1)]
        p1, p2 = points[i], points[i + 1]
        p3 = points[min(len(points) - 1, i + 2)]
        steps = max(1, int(np.ceil(np.linalg.norm(p2 - p1) / spacing_m)))
        t = np.linspace(0.0, 1.0, steps, endpoint=False)[:, None]
        q = 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t**2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t**3)
        out.extend(q)
    out.append(points[-1])
    return [[round(float(x), 4), round(float(y), 4)] for x, y in out]


def _extend_spline(points: list[list[float]], start: bool, end: bool, length_m: float = 4.0) -> list[list[float]]:
    p = np.asarray(points, dtype=np.float64)
    if len(p) < 2:
        return points
    if start:
        d = p[0] - p[1]
        n = float(np.linalg.norm(d))
        if n > 1e-9:
            ext = np.linspace(length_m, 0.0, int(np.ceil(length_m / 0.30)) + 1)[:-1, None]
            p = np.concatenate([p[0] + ext * (d / n), p], axis=0)
    if end and len(p) >= 2:
        d = p[-1] - p[-2]
        n = float(np.linalg.norm(d))
        if n > 1e-9:
            ext = np.linspace(0.0, length_m, int(np.ceil(length_m / 0.30)) + 1)[1:, None]
            p = np.concatenate([p, p[-1] + ext * (d / n)], axis=0)
    return [[round(float(x), 4), round(float(y), 4)] for x, y in p]


def _road_profile(points: list[list[float]], height: np.ndarray) -> list[float]:
    p = np.asarray(points, dtype=np.float64)
    coords = [p[:, 1] / CELL_M - 0.5, p[:, 0] / CELL_M - 0.5]
    values = ndi.map_coordinates(height, coords, order=1, mode="nearest")
    return [round(float(v), 3) for v in values]


def _polygon_rings(geom, simplify_m: float = 0.12) -> list[list[list[float]]]:
    geom = geom.simplify(simplify_m, preserve_topology=True)
    parts = [geom] if isinstance(geom, Polygon) else list(getattr(geom, "geoms", ()))
    result = []
    for part in parts:
        if not isinstance(part, Polygon) or part.area <= 0:
            continue
        coords = [[round(float(x), 3), round(float(y), 3)] for x, y in part.exterior.coords]
        result.append(coords)
    return result


def _polygon_holes(geom, simplify_m: float = 0.12) -> list[list[list[list[float]]]]:
    geom = geom.simplify(simplify_m, preserve_topology=True)
    parts = [geom] if isinstance(geom, Polygon) else list(getattr(geom, "geoms", ()))
    return [
        [[[round(float(x), 3), round(float(y), 3)] for x, y in ring.coords] for ring in part.interiors]
        for part in parts if isinstance(part, Polygon)
    ]


def _mask_polygons(mask: np.ndarray, heights: np.ndarray | None = None) -> list[dict]:
    labels, count = ndi.label(mask, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.uint8))
    features = []
    for component in range(1, count + 1):
        yy, xx = np.nonzero(labels == component)
        if not len(xx):
            continue
        geom = unary_union([box(x * CELL_M, y * CELL_M, (x + 1) * CELL_M, (y + 1) * CELL_M) for y, x in zip(yy, xx)])
        rings = _polygon_rings(geom)
        h = round(float(np.median(heights[yy, xx])), 3) if heights is not None else None
        features.append({"polygon_m": rings, "innenringe_m": _polygon_holes(geom), "z_m": h,
                         "cells": int(len(xx)), "area_m2": round(float(geom.area), 3)})
    return features


def _draw_debug(rows: list[dict[str, str]], overlay_by_cell: dict[tuple[int, int], dict[str, str]], data: dict) -> None:
    from PIL import Image, ImageDraw

    scale = 12
    palette = {
        "SCHNEE": (207, 216, 219), "WASSER_EIS": (79, 150, 194), "KLIPPE_WAND": (86, 88, 91),
        "KLIPPE_KANTE": (126, 124, 116), "WALD": (81, 120, 80), "FELS": (152, 142, 121),
        "BODEN": (149, 139, 109), "SCHATTEN": (117, 122, 123),
    }
    by_coord = {(int(r["cx"]), int(r["cy"])): r for r in rows}
    road_cells = {(x, y) for y in range(NY) for x in range(NX) if overlay_by_cell.get((x, y), {}).get("weg_id")}
    cross_cells = {(int(v["cx"]), int(v["cy"])) for cross in data["kreuzungen"] for v in cross["quellzellen"]}
    water_cells = {(x, y) for y in range(NY) for x in range(NX) if by_coord[(x, y)]["wasser_eis"] == "1"}
    for tile in PROTOTYPE_TILES:
        col = TILE_COLS.index(tile[0]); row = int(tile[1:]) - 1
        x0, y0, x1, y1 = col * TILE_W, row * TILE_H, (col + 1) * TILE_W, (row + 1) * TILE_H
        image = Image.new("RGB", (TILE_W * scale, TILE_H * scale), (235, 234, 228))
        draw = ImageDraw.Draw(image)
        for y in range(y0, min(y1, NY)):
            for x in range(x0, min(x1, NX)):
                color = palette.get(by_coord[(x, y)]["untergrund"], (170, 170, 165))
                rect = ( (x - x0) * scale, (y - y0) * scale, (x - x0 + 1) * scale - 1, (y - y0 + 1) * scale - 1 )
                draw.rectangle(rect, fill=color)
                if (x, y) in road_cells:
                    draw.rectangle(rect, fill=(184, 65, 57))
                if (x, y) in cross_cells:
                    draw.rectangle(rect, fill=(244, 193, 67))
                if by_coord[(x, y)]["wasser_eis"] == "1":
                    draw.rectangle(rect, fill=(71, 154, 209))
                if by_coord[(x, y)]["bauzone_bestand"] == "1" or by_coord[(x, y)]["bauzone_plan"] == "1":
                    draw.rectangle(rect, outline=(82, 156, 97), width=1)
        draw.rectangle((0, 0, TILE_W * scale - 1, TILE_H * scale - 1), outline=(28, 31, 35), width=2)
        image.save(OUT / f"debug_{tile}.png", optimize=False)


def build() -> dict:
    rows = _rows(SOURCE)
    overlays = _rows(OVERLAY)
    if len(rows) != NX * NY:
        raise ValueError(f"Unerwartete Zellzahl: {len(rows)} statt {NX * NY}")
    source_grid = {(int(r["cx"]), int(r["cy"])): r for r in rows}
    if len(source_grid) != len(rows):
        raise ValueError("Zellkoordinaten sind nicht eindeutig")
    height = np.zeros((NY, NX), dtype=np.float32)
    water = np.zeros((NY, NX), dtype=bool)
    wall = np.zeros((NY, NX), dtype=bool)
    wall_name = np.empty((NY, NX), dtype=object)
    zone_existing = np.zeros((NY, NX), dtype=bool)
    zone_planned = np.zeros((NY, NX), dtype=bool)
    for r in rows:
        x, y = int(r["cx"]), int(r["cy"])
        height[y, x] = float(r["hoehe_m"])
        water[y, x] = r["wasser_eis"] == "1"
        wall[y, x] = r["untergrund"] in ("KLIPPE_WAND", "KLIPPE_KANTE")
        wall_name[y, x] = r["wand_name"]
        zone_existing[y, x] = r["bauzone_bestand"] == "1"
        zone_planned[y, x] = r["bauzone_plan"] == "1"

    ov_by_cell: dict[tuple[int, int], dict[str, str]] = {}
    roads: dict[str, list[dict[str, str]]] = defaultdict(list)
    road_mask = np.zeros((NY, NX), dtype=bool)
    road_id_grid: dict[tuple[int, int], str] = {}
    place_mask = np.zeros((NY, NX), dtype=bool)
    place_id_grid: dict[tuple[int, int], str] = {}
    for o in overlays:
        x, y = int(o["cx"]), int(o["cy"])
        ov_by_cell[(x, y)] = o
        if o["platz"]:
            place_mask[y, x] = True
            place_id_grid[(x, y)] = o["platz"]
        wid = o["weg_id"]
        if wid:
            roads[wid].append(o)
            road_mask[y, x] = True
            road_id_grid[(x, y)] = wid

    road_vectors = []
    road_cell_ids: set[int] = set()
    for wid in sorted(roads):
        cells = {(int(o["cx"]), int(o["cy"])) for o in roads[wid]}
        road_cell_ids.update(y * NX + x for x, y in cells)
        classes = Counter(o["weg_klasse"] for o in roads[wid])
        road_class = sorted(classes.items(), key=lambda item: (-item[1], item[0]))[0][0]
        # Rasterbreiten aus der Zellmaske: Gasse meist drei Zellen, Anbindung
        # zwei bis drei, Hausweg eine bis zwei. Die Werte decken die Quellzellen.
        width = {"GASSE": 3.6, "ANBINDUNG": 3.2, "HAUSWEG": 2.4}.get(road_class, 2.4)
        id_mask = np.zeros((NY, NX), dtype=bool)
        for x, y in cells:
            id_mask[y, x] = True
        center_cells = {(int(x), int(y)) for y, x in zip(*np.nonzero(skeletonize(id_mask)))}
        for part_index, trail in enumerate(_curves(center_cells)):
            def degree(point):
                x, y = point
                return sum((x + dx, y + dy) in center_cells for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dx or dy)
            start_terminal, end_terminal = degree(trail[0]) <= 1, degree(trail[-1]) <= 1
            centerline = _extend_spline(_spline(trail), start_terminal, end_terminal)
            endpoints = []
            if start_terminal:
                endpoints.append({"zell_id": trail[0][1] * NX + trail[0][0], "kachel": tile_name(*trail[0]), "auslauf_m": 4.0, "ziel": "gelaende"})
            if end_terminal and (len(trail) > 1 or not start_terminal):
                endpoints.append({"zell_id": trail[-1][1] * NX + trail[-1][0], "kachel": tile_name(*trail[-1]), "auslauf_m": 4.0, "ziel": "gelaende"})
            road_vectors.append({
                "id": wid, "teil": part_index, "klasse": road_class, "breite_m": width,
                "mittellinie_m": centerline, "laengsprofil_m": _road_profile(centerline, height),
                "quellzellen": [y * NX + x for x, y in trail], "zellzahl": len(set(trail)),
                "wegenden": endpoints,
            })

    # Ein Kreuzungscluster gehoert genau zu einer gemeinsamen, ebenen Flaeche.
    crossing_seed = np.zeros((NY, NX), dtype=bool)
    for (x, y), wid in sorted(road_id_grid.items()):
        nearby = {road_id_grid[(xx, yy)] for yy in range(max(0, y - 1), min(NY, y + 2))
                  for xx in range(max(0, x - 1), min(NX, x + 2)) if (xx, yy) in road_id_grid}
        touches_place = bool(place_mask[max(0, y - 2):min(NY, y + 3), max(0, x - 2):min(NX, x + 3)].any())
        if len(nearby) >= 2 or touches_place:
            crossing_seed[y, x] = True
    crossing_labels, crossing_count = ndi.label(crossing_seed, structure=np.ones((3, 3), dtype=np.uint8))
    intersections = []
    crossing_mask = np.zeros((NY, NX), dtype=bool)
    for cid in range(1, crossing_count + 1):
        yy, xx = np.nonzero(crossing_labels == cid)
        near = np.zeros((NY, NX), dtype=bool)
        for y, x in zip(yy, xx):
            ys, xs = slice(max(0, y - 2), min(NY, y + 3)), slice(max(0, x - 2), min(NX, x + 3))
            near[ys, xs] |= road_mask[ys, xs] | place_mask[ys, xs]
        py, px = np.nonzero(near)
        if not len(px):
            continue
        points = [((x + 0.5) * CELL_M, (y + 0.5) * CELL_M) for y, x in zip(py, px)]
        geom = MultiPoint(points).convex_hull.buffer(0.15, join_style="mitre")
        rings = _polygon_rings(geom, simplify_m=0.05)
        if not rings:
            continue
        cx, cy = float(np.mean(px)), float(np.mean(py))
        zflat = round(float(np.median(height[py, px])), 3)
        ids = sorted({road_id_grid[(int(x), int(y))] for x, y in zip(px, py) if (int(x), int(y)) in road_id_grid})
        places = sorted({place_id_grid[(int(x), int(y))] for x, y in zip(px, py) if (int(x), int(y)) in place_id_grid})
        source_cells = sorted(int(y * NX + x) for y, x in zip(py, px))
        crossing_mask[py, px] = True
        intersections.append({
            "id": f"K{len(intersections) + 1:03d}", "weg_ids": ids, "platz_ids": places,
            "art": "weg_platz" if places and len(ids) < 2 else "weg_kreuzung",
            "polygon_m": rings[0], "hoehe_m": zflat, "uebergang_m": 2.4,
            "quellzellen": [{"cx": int(x), "cy": int(y)} for y, x in zip(py, px)],
            "zentrum_m": [round((cx + 0.5) * CELL_M, 3), round((cy + 0.5) * CELL_M, 3)],
        })

    # Waende werden ueber die gesamte Karte aus dem Band skeletonisiert und mit Profil abgelegt.
    wall_vectors = []
    for name in ("Nord", "Suedgrat", "Krater", "Ostgrat", "unbenannt"):
        mask = wall & ((wall_name == "") if name == "unbenannt" else (wall_name == name))
        skel = skeletonize(mask)
        for i, trail in enumerate(_curves({(int(x), int(y)) for y, x in zip(*np.nonzero(skel))})):
            tops, bottoms = [], []
            for x, y in trail:
                y0, y1 = max(0, y - 5), min(NY, y + 6)
                x0, x1 = max(0, x - 5), min(NX, x + 6)
                nearby_h = height[y0:y1, x0:x1]
                top = float(np.max(nearby_h))
                cliff = float(source_grid[(x, y)]["klippe_hoehe_m"] or 0)
                bottoms.append(round(top - max(4.0, cliff), 3))
                tops.append(round(top, 3))
            centerline = _spline(trail)
            node_points = np.asarray([[(x + 0.5) * CELL_M, (y + 0.5) * CELL_M] for x, y in trail], dtype=np.float64)
            line_points = np.asarray(centerline, dtype=np.float64)
            node_dist = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(node_points, axis=0), axis=1))]
            line_dist = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(line_points, axis=0), axis=1))]
            top_profile = np.interp(line_dist, node_dist, tops)
            bottom_profile = np.interp(line_dist, node_dist, bottoms)
            wall_vectors.append({
                "name": name, "teil": i, "mittellinie_m": centerline,
                "hoehe_oben_m": [round(float(v), 3) for v in top_profile],
                "hoehe_unten_m": [round(float(v), 3) for v in bottom_profile],
                "breite_min_m": CELL_M, "quellzellen": [y * NX + x for x, y in trail],
            })

    water_vectors = _mask_polygons(water, height)
    water_total = int(water.sum())
    zones = {
        "bestand": _mask_polygons(zone_existing),
        "plan": _mask_polygons(zone_planned),
    }

    data = {
        "schema": "dorfmap-vektor-1", "karte": {"nx": NX, "ny": NY, "zellweite_m": CELL_M,
                  "kacheln": {"spalten": 8, "zeilen": 7, "breite_zellen": TILE_W, "hoehe_zellen": TILE_H}},
        "prototype_kacheln": list(PROTOTYPE_TILES),
        "quellen": {"zellen_sha256": _sha(SOURCE), "overlay_sha256": _sha(OVERLAY),
                    "zellzahl": len(rows), "wegzellzahl": len(road_cell_ids), "wasserzellzahl": water_total},
        "wege": road_vectors, "kreuzungen": intersections,
        "waende": wall_vectors, "wasser": water_vectors, "bauzonen": zones,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "vektor.json"
    out.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    _draw_debug(rows, ov_by_cell, data)
    return {"daten": data, "hoehe": height, "wegmaske": road_mask, "kreuzungsmaske": crossing_mask,
            "wandmaske": wall, "wassermaske": water, "bauzone_bestand": zone_existing,
            "bauzone_plan": zone_planned, "quellzeilen": rows}


if __name__ == "__main__":
    result = build()
    d = result["daten"]
    print(json.dumps({"wege": len(d["wege"]), "kreuzungen": len(d["kreuzungen"]), "waende": len(d["waende"]),
                      "wasserflaechen": len(d["wasser"]), "bauzonen_bestand": len(d["bauzonen"]["bestand"]),
                      "bauzonen_plan": len(d["bauzonen"]["plan"]), "prototyp": d["prototype_kacheln"]}, ensure_ascii=False))
