#!/usr/bin/env python3
"""Build the detail_v2 terrain with Shewchuk Triangle constrained Delaunay.

Each tile is an independent PSLG. Shared tile borders use an identical 0.2 m
float32 vertex sequence; Triangle may refine interior constraints but cannot
split those border segments. The 1.6M triangle limit is a hard budget.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import struct
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree
import triangle as triangle_cdt
from shapely import contains_xy, covers, distance, get_coordinates, line_interpolate_point, line_locate_point, line_merge, linestrings, points, unary_union
from shapely.geometry import GeometryCollection, LineString, MultiLineString, MultiPolygon, Point, Polygon, box
from shapely.ops import triangulate
from shapely.strtree import STRtree

HERE = Path(__file__).resolve().parent
RELIEF = HERE.parents[1]
sys.path.insert(0, str(RELIEF))
from neu.mesh import load_relief

NX, NZ = 336, 303
LETTERS = "ABCDEFGH"
CLASSES = {0: "grund", 1: "weg", 2: "ufer", 3: "fels_klippe", 4: "wasser", 5: "bruecke"}
RANK = {0: 0, 3: 1, 2: 2, 1: 3, 5: 4, 4: 5}
MAX_TRIANGLES = 1_600_000
MAX_TILE_TRIANGLES = 60_000
MAX_TILE_POINTS = 13_550
EPS = 1e-6


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def line_parts(g):
    if g is None or g.is_empty:
        return
    if g.geom_type == "LineString":
        yield g
    elif g.geom_type in ("MultiLineString", "GeometryCollection"):
        for q in g.geoms:
            yield from line_parts(q)
    elif g.geom_type == "Polygon":
        yield g.exterior
        for ring in g.interiors:
            yield ring
    elif g.geom_type == "MultiPolygon":
        for q in g.geoms:
            yield from line_parts(q)


def polygon_parts(g):
    if g is None or g.is_empty:
        return
    if g.geom_type == "Polygon":
        yield g
    elif g.geom_type in ("MultiPolygon", "GeometryCollection"):
        for q in g.geoms:
            yield from polygon_parts(q)


def tile_bounds(i: int, j: int):
    return (42 * i, 43 * j, 42 * (i + 1), NZ if j == 6 else 43 * (j + 1))


def grid_points(b, step):
    x0, z0, x1, z1 = b
    ia, ib = math.ceil((x0 - 1e-8) / step), math.floor((x1 + 1e-8) / step)
    ja, jb = math.ceil((z0 - 1e-8) / step), math.floor((z1 + 1e-8) / step)
    xs = np.arange(ia, ib + 1, dtype=np.float64) * step
    zs = np.arange(ja, jb + 1, dtype=np.float64) * step
    xx, zz = np.meshgrid(xs, zs)
    return np.column_stack((xx.ravel(), zz.ravel())).astype(np.float32)


def interp_height(field, xz):
    ix = np.clip(xz[:, 0].astype(np.float64) * 2.0, 0, field.shape[1] - 1.000001)
    iz = np.clip(xz[:, 1].astype(np.float64) * 2.0, 0, field.shape[0] - 1.000001)
    coords = np.vstack((iz, ix))
    h = ndimage.map_coordinates(field, coords, order=3, mode="nearest", prefilter=True)
    # Bound bicubic values by the surrounding 4x4 source samples.
    x0, z0 = np.floor(ix).astype(int), np.floor(iz).astype(int)
    lo = np.full(len(ix), np.inf); hi = np.full(len(ix), -np.inf)
    for dz in (-1, 0, 1, 2):
        rz = np.clip(z0 + dz, 0, field.shape[0] - 1)
        for dx in (-1, 0, 1, 2):
            rx = np.clip(x0 + dx, 0, field.shape[1] - 1)
            v = field[rz, rx]
            lo = np.minimum(lo, v); hi = np.maximum(hi, v)
    return np.minimum(np.maximum(h, lo), hi).astype(np.float64)


def load_inputs():
    vdir = HERE.parent / "vektor"
    vec = {n: read_json(vdir / f"{n}.geojson")["features"] for n in
           ("wege", "kreuzungen", "ufer", "kanten", "grat", "zonen", "wasser")}
    constraints = []
    for f in vec["wege"]:
        if (f.get("properties") or {}).get("rolle") in ("rand_links", "rand_rechts"):
            constraints.append(LineString(f["geometry"]["coordinates"]))
    for f in vec["kreuzungen"]:
        constraints.extend(line_parts(Polygon(f["geometry"]["coordinates"][0], f["geometry"]["coordinates"][1:])))
    for f in vec["ufer"]:
        p = f.get("properties") or {}
        if p.get("typ") == "uferlinie":
            g = f["geometry"]
            if g["type"] == "LineString": constraints.append(LineString(g["coordinates"]))
            elif g["type"] == "MultiLineString": constraints.extend(LineString(q) for q in g["coordinates"])
    for f in vec["kanten"] + vec["grat"]:
        if f.get("geometry", {}).get("type") == "LineString":
            constraints.append(LineString(f["geometry"]["coordinates"]))
    classes = []
    for f in vec["zonen"]:
        p = f.get("properties") or {}
        if p.get("layer") != "flaechentyp" or f.get("geometry", {}).get("type") not in ("Polygon", "MultiPolygon"):
            continue
        g = Polygon(f["geometry"]["coordinates"][0], f["geometry"]["coordinates"][1:]) if f["geometry"]["type"] == "Polygon" else MultiPolygon([Polygon(q[0], q[1:]) for q in f["geometry"]["coordinates"]])
        if not g.is_valid:
            g = g.buffer(0)
        cl = int(p.get("klasse", 0))
        classes.append((g, cl, p.get("untergrund"), p.get("id")))
        constraints.extend(line_parts(g.boundary))
    roads = []
    for f in vec["wege"]:
        p = f.get("properties") or {}
        if p.get("rolle") == "netz":
            roads.append(Polygon(f["geometry"]["coordinates"][0], f["geometry"]["coordinates"][1:]) if f["geometry"]["type"] == "Polygon" else MultiPolygon([Polygon(q[0], q[1:]) for q in f["geometry"]["coordinates"]]))
    # Keep road polygons separate; each tile unions only its spatial subset.
    # Keep the source network un-noded globally. A single full-map unary_union
    # exceeded the available process memory; each tile is noded after spatial
    # filtering in cdt_tile().
    constraint_lines = [g for g in constraints if g is not None and not g.is_empty and g.length >= 0.02]
    constraint_geom = GeometryCollection()
    constraint_tree = STRtree(constraint_lines) if constraint_lines else None
    constraint_vertex_tree = None  # Built from the noded, tile-local PSLG below.
    with (RELIEF / "zellen_relief.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    under = np.full((NZ, NX), "", dtype=object)
    walk = np.zeros((NZ, NX), dtype=np.uint8)
    cliff = np.full((NZ, NX), "", dtype=object)
    for r in rows:
        x, z = int(r["cx"]), int(r["cy"])
        if 0 <= x < NX and 0 <= z < NZ:
            under[z, x] = r.get("untergrund", "")
            walk[z, x] = int(float(r.get("begehbar", 0) or 0))
            cliff[z, x] = r.get("klippe", "")
    return vec, classes, roads, constraint_geom, constraint_lines, constraint_tree, constraint_vertex_tree, under, walk, cliff


def grid_tile(b, step, constraint_geom, constraint_tree, field):
    """Build a world-aligned quad lattice; snap nearby vertices onto constraints."""
    x0, z0, x1, z1 = b
    xs = np.arange(round(x0 / step), round(x1 / step) + 1, dtype=np.float64) * step
    zs = np.arange(round(z0 / step), round(z1 / step) + 1, dtype=np.float64) * step
    xx, zz = np.meshgrid(xs, zs)
    original = np.column_stack((xx.ravel(), zz.ravel())).astype(np.float32)
    p = original.copy()
    nx = len(xs)
    boundary = ((np.abs(p[:, 0] - x0) < 1e-6) | (np.abs(p[:, 0] - x1) < 1e-6) |
                (np.abs(p[:, 1] - z0) < 1e-6) | (np.abs(p[:, 1] - z1) < 1e-6))
    snapped = np.zeros(len(p), dtype=bool)
    if constraint_tree is not None and not constraint_geom.is_empty:
        q = points(p[:, 0], p[:, 1])
        nearest_ids = constraint_tree.nearest(q)
        lines = np.asarray(constraint_tree.geometries, dtype=object)[nearest_ids]
        station = line_locate_point(lines, q)
        nearest = get_coordinates(line_interpolate_point(lines, station)).reshape(-1, 2)
        distance = np.linalg.norm(nearest - p.astype(np.float64), axis=1)
        within = ((nearest[:, 0] >= x0) & (nearest[:, 0] <= x1) &
                  (nearest[:, 1] >= z0) & (nearest[:, 1] <= z1))
        sel = (distance <= 0.1250001) & ~boundary & within
        occupied = set()
        original_keys = {tuple(v) for v in original}
        for k in np.flatnonzero(sel):
            candidate = tuple(np.asarray(nearest[k], dtype=np.float32))
            if candidate in occupied or (candidate in original_keys and candidate != tuple(original[k])):
                continue
            occupied.add(candidate)
            p[k] = candidate
            snapped[k] = True
    # Tile border vertices are never displaced; their float32 bit patterns
    # therefore agree on both sides of every independently built seam.
    p[boundary] = original[boundary]
    ids = np.arange(len(p), dtype=np.int32).reshape(len(zs), len(xs))
    quads = np.column_stack((ids[:-1, :-1].ravel(), ids[:-1, 1:].ravel(),
                             ids[1:, 1:].ravel(), ids[1:, :-1].ravel()))
    # Snapping can fold a quad at a sharp crossing. Revert the snapped corners
    # of every non-convex cell so no inverted or collapsed triangles survive.
    for _ in range(2):
        xy = p[quads].astype(np.float64)
        edges = np.roll(xy, -1, axis=1) - xy
        turns = edges[:, :, 0] * np.roll(edges, -1, axis=1)[:, :, 1] - edges[:, :, 1] * np.roll(edges, -1, axis=1)[:, :, 0]
        bad_cells = np.flatnonzero(np.any(turns <= 1e-8, axis=1))
        if not len(bad_cells):
            break
        affected = np.unique(quads[bad_cells].ravel())
        affected = affected[snapped[affected]]
        if not len(affected):
            break
        p[affected] = original[affected]
        snapped[affected] = False

    # At a 0.5 m tile, insert 0.25 m points on every tile edge. A neighbor at
    # 0.25 m then has the identical border vertex sequence (T-junction-free).
    extra_points, extra_cells = [], []
    if step > 0.25:
        for xx0 in np.arange(x0, x1 + 0.125, 0.25, dtype=np.float32):
            extra_points.append((float(xx0), float(z0)))
            extra_points.append((float(xx0), float(z1)))
        for zz0 in np.arange(z0 + 0.25, z1, 0.25, dtype=np.float32):
            extra_points.append((float(x0), float(zz0)))
            extra_points.append((float(x1), float(zz0)))
        # These boundary points are used to split coarse boundary-cell sides.
        all_points = np.vstack((p, np.asarray(extra_points, dtype=np.float32)))
        unique, inverse = np.unique(all_points, axis=0, return_inverse=True)
        remap = inverse[:len(p)].astype(np.int32)
        p = unique
        quad_grid = np.arange(len(original), dtype=np.int32).reshape(len(zs), len(xs))
        quad_grid = remap[quad_grid]
        boundary_map = {}
        for old_id, coord in enumerate(extra_points, start=len(original)):
            boundary_map[tuple(np.asarray(coord, dtype=np.float32))] = int(inverse[old_id])
        quads = np.column_stack((quad_grid[:-1, :-1].ravel(), quad_grid[:-1, 1:].ravel(),
                                 quad_grid[1:, 1:].ravel(), quad_grid[1:, :-1].ravel()))
        for qi, qd in enumerate(quads):
            ring = [int(v) for v in qd]
            expanded = []
            for aa, bb in zip(ring, ring[1:] + ring[:1]):
                expanded.append(aa)
                pa, pb = p[aa], p[bb]
                if (abs(float(pa[0]) - float(pb[0])) < 1e-6 and
                    (abs(float(pa[0]) - x0) < 1e-6 or abs(float(pa[0]) - x1) < 1e-6) and
                    abs(float(pa[1]) - float(pb[1])) > 0.25 + 1e-6):
                    mid = (float(pa[0]), (float(pa[1]) + float(pb[1])) * 0.5)
                    expanded.append(boundary_map.get(mid, -1))
                elif (abs(float(pa[1]) - float(pb[1])) < 1e-6 and
                    (abs(float(pa[1]) - z0) < 1e-6 or abs(float(pa[1]) - z1) < 1e-6) and
                    abs(float(pa[0]) - float(pb[0])) > 0.25 + 1e-6):
                    mid = ((float(pa[0]) + float(pb[0])) * 0.5, float(pa[1]))
                    expanded.append(boundary_map.get(mid, -1))
            expanded = [v for v in expanded if v >= 0]
            if len(expanded) > 4:
                extra_cells.append((qi, expanded))

    # Height-based diagonal selection, except when one diagonal crosses a
    # source constraint and the other does not.
    h = interp_height(field, p)
    if step > 0.25:
        # Keep unsplit quads and transition polygons in one triangle list.
        split_by_q = {qi: ring for qi, ring in extra_cells}
    else:
        split_by_q = {}
    tris = []
    # Add one center vertex per transition polygon and fan it to its boundary.
    for qi, ring in sorted(split_by_q.items()):
        center = p[np.asarray(ring, dtype=np.int32)].mean(axis=0).astype(np.float32)
        center_id = len(p)
        p = np.vstack((p, center))
        h = np.append(h, interp_height(field, center.reshape(1, 2))[0])
        for aa, bb in zip(ring, ring[1:] + ring[:1]):
            tris.append((aa, bb, center_id))
    if len(quads):
        regular_ids = np.asarray([qi for qi in range(len(quads)) if qi not in split_by_q], dtype=np.int32)
        q = quads[regular_ids]
        d0 = linestrings(p[q[:, [0, 2]]].astype(np.float64))
        d1 = linestrings(p[q[:, [1, 3]]].astype(np.float64))
        cross0 = np.zeros(len(d0), dtype=bool)
        cross1 = np.zeros(len(d1), dtype=bool)
        if constraint_tree is not None:
            pairs0 = constraint_tree.query(d0, predicate="crosses")
            pairs1 = constraint_tree.query(d1, predicate="crosses")
            if pairs0.size:
                cross0[pairs0[0]] = True
            if pairs1.size:
                cross1[pairs1[0]] = True
        dh0 = np.abs(h[q[:, 0]] - h[q[:, 2]])
        dh1 = np.abs(h[q[:, 1]] - h[q[:, 3]])
        choose1 = cross0 & ~cross1
        choose1 |= ((~cross0 & ~cross1) | (cross0 & cross1)) & (dh1 < dh0)
        t0a = np.column_stack((q[:, 0], q[:, 1], q[:, 2]))
        t0b = np.column_stack((q[:, 0], q[:, 2], q[:, 3]))
        t1a = np.column_stack((q[:, 0], q[:, 1], q[:, 3]))
        t1b = np.column_stack((q[:, 1], q[:, 2], q[:, 3]))
        aa = np.where(choose1[:, None], t1a, t0a)
        bb = np.where(choose1[:, None], t1b, t0b)
        tris.extend(aa.tolist())
        tris.extend(bb.tolist())
    t = np.asarray(tris, dtype=np.int32)
    t[:, [1, 2]] = t[:, [2, 1]]
    return p, t, {"raster_m": step, "grid_vertices": len(p), "snapped_vertices": int(snapped.sum()),
                  "quads": len(quads), "diagonal_constraint_avoided": None,
                  "reparatur_runden": 0, "fehlende_constraint_kanten": None,
                  "eingefuegte_mittelpunkte": 0}


def _line_parts_local(g):
    if g is None or g.is_empty:
        return
    if g.geom_type == "LineString":
        yield g
    elif g.geom_type in ("MultiLineString", "GeometryCollection", "MultiPolygon", "Polygon"):
        for part in g.geoms if hasattr(g, "geoms") else ():
            yield from _line_parts_local(part)


def _tile_border_pslg(b):
    """Create bit-identical tile boundary samples at world multiples of 0.2 m."""
    x0, z0, x1, z1 = b
    # Integer lattice indices avoid cumulative floating point drift. Endpoints
    # are explicitly replaced by exact tile coordinates (303 is not 0.2*n).
    xs = (np.arange(round(x0 * 5), round(x1 * 5) + 1, dtype=np.float64) / 5.0).astype(np.float32)
    zs = (np.arange(round(z0 * 5), round(z1 * 5) + 1, dtype=np.float64) / 5.0).astype(np.float32)
    xs[0], xs[-1] = np.float32(x0), np.float32(x1)
    zs[0], zs[-1] = np.float32(z0), np.float32(z1)
    coords = np.vstack((np.column_stack((xs, np.full(len(xs), z0, np.float32))),
                        np.column_stack((np.full(len(zs) - 1, x1, np.float32), zs[1:])),
                        np.column_stack((xs[-2::-1], np.full(len(xs) - 1, z1, np.float32))),
                        np.column_stack((np.full(len(zs) - 2, x0, np.float32), zs[-2:0:-1]))))
    return coords.astype(np.float64)


def cdt_tile(b, constraint_geom, constraint_tree, roads_union, centerline_tree, quality_angle):
    """Build a noded, tile-clipped PSLG and refine its CDT against local Q9 sizes."""
    tile = box(*b)
    border = _tile_border_pslg(b)
    border_lines = [LineString([border[i], border[(i + 1) % len(border)]]) for i in range(len(border))]

    # Spatially filter first, then node only this tile's local constraint
    # network. A full-map union of the dense P1 vectors exceeds the memory cap.
    query_tile = tile.buffer(1.51)
    if constraint_tree is not None:
        candidate_ids = constraint_tree.query(query_tile)
        candidates = np.asarray(constraint_tree.geometries, dtype=object)[candidate_ids]
        nearby = unary_union([g.intersection(query_tile) for g in candidates if g.intersects(query_tile)])
    else:
        nearby = GeometryCollection()
    local_constraints = nearby.intersection(tile)

    linework = list(border_lines)
    linework.extend(_line_parts_local(local_constraints))
    noded = unary_union(linework)

    vertices = []
    segments = set()
    index = {}
    def vertex_id(xy):
        key = (round(float(xy[0]), 7), round(float(xy[1]), 7))
        idx = index.get(key)
        if idx is None:
            idx = len(vertices)
            index[key] = idx
            vertices.append(key)
        return idx

    # Dedupe noded coordinates by a 5 cm tolerance only when they are duplicate
    # endpoints from different source paths. Consecutive curve samples remain
    # intact so their polyline geometry does not move.
    for line in _line_parts_local(noded):
        coords = list(line.coords)
        if len(coords) < 2:
            continue
        kept = [coords[0]]
        for xy in coords[1:]:
            if math.hypot(float(xy[0]) - float(kept[-1][0]), float(xy[1]) - float(kept[-1][1])) >= 0.02:
                kept.append(xy)
        if len(kept) < 2:
            continue
        ids = [vertex_id(xy) for xy in kept]
        for a, c in zip(ids, ids[1:]):
            if a != c and math.dist(vertices[a], vertices[c]) >= 0.02:
                segments.add((min(a, c), max(a, c)))

    # Ensure fixed border positions survive exact-key deduplication.
    for xy in border:
        vertex_id(xy)
    pslg = {"vertices": np.asarray(vertices, dtype=np.float64),
            "segments": np.asarray(sorted(segments), dtype=np.int32)}
    print(f"CDT {b}: PSLG {len(vertices):,} vertices / {len(segments):,} segments", flush=True)
    first = triangle_cdt.triangulate(pslg, f"pq{quality_angle}YS60000")
    if "triangles" not in first or not len(first["triangles"]):
        raise RuntimeError(f"CDT leer auf {b}")

    v0 = np.asarray(first["vertices"], dtype=np.float64)
    t0 = np.asarray(first["triangles"], dtype=np.int32)
    print(f"CDT {b}: initial {len(v0):,} vertices / {len(t0):,} triangles", flush=True)
    cent = v0[t0].mean(axis=1)
    qcent = points(cent[:, 0], cent[:, 1])
    dcon = np.asarray(nearby.distance(qcent), dtype=np.float64)
    if centerline_tree is not None:
        road_ids = centerline_tree.nearest(qcent)
        nearest_roads = np.asarray(centerline_tree.geometries, dtype=object)[road_ids]
        droad = np.asarray(distance(nearest_roads, qcent), dtype=np.float64)
    else:
        droad = np.full(len(t0), np.inf)
    in_road = np.asarray(covers(roads_union, qcent), dtype=bool) if not roads_union.is_empty else np.zeros(len(t0), bool)
    far = droad > 30.0
    max_area = np.where(dcon <= 1.500001, 0.005,
                        np.where(in_road, 0.012,
                                 np.where(far, 0.40, 0.11))).astype(np.float64)
    refinement_input = {"vertices": v0, "triangles": t0,
                        "segments": np.asarray(first.get("segments", pslg["segments"]), dtype=np.int32),
                        "triangle_max_area": max_area}
    refined = triangle_cdt.triangulate(refinement_input, f"rq{quality_angle}aYS60000")
    if "triangles" not in refined or not len(refined["triangles"]):
        raise RuntimeError(f"CDT-Nachverfeinerung leer auf {b}")
    p = np.asarray(refined["vertices"], dtype=np.float32)
    t = np.asarray(refined["triangles"], dtype=np.int32)
    # Triangle outputs CCW in x,z; the viewer and all QA use y-up normals.
    t[:, [1, 2]] = t[:, [2, 1]]
    info = {"verfahren": "triangle/Shewchuk CDT + r-area refinement",
            "quality_angle_deg": quality_angle,
            "pslg_vertices": int(len(vertices)), "pslg_segments": int(len(segments)),
            "cdt_triangles": int(len(t0)), "cdt_vertices": int(len(v0)),
            "refined_vertices": int(len(p)), "refined_triangles": int(len(t)),
            "border_step_m": 0.2, "max_area_m2": {"constraint_band": 0.005, "road": 0.012,
                                                      "walkable": 0.11, "remote": 0.40}}
    local_lines = list(_line_parts_local(noded))
    local_xy = [np.asarray(g.coords, dtype=np.float32) for g in local_lines if len(g.coords) > 1]
    local_vertices = np.unique(np.concatenate(local_xy), axis=0) if local_xy else np.empty((0, 2), np.float32)
    local_tree = cKDTree(local_vertices.astype(np.float64)) if len(local_vertices) else None
    return p, t, info, local_tree


def terrain_heights(p, field, roads, road_union, vec, water_geoms, water_levels):
    h = interp_height(field, p)
    # Road band depression with a 0.4 m smooth return. D2 remains tied to GB.
    if not road_union.is_empty:
        mask = contains_xy(road_union, p[:, 0], p[:, 1])
        mask &= ~((p[:, 0] >= 126 - 1e-7) & (p[:, 0] <= 168 + 1e-7) &
                  (p[:, 1] >= 43 - 1e-7) & (p[:, 1] <= 86 + 1e-7))
        if mask.any():
            road_boundary = road_union.boundary
            d = np.asarray(road_boundary.distance(points(p[mask, 0], p[mask, 1])), dtype=np.float64)
            u = np.clip(d / 0.4, 0, 1)
            s = u * u * (3 - 2 * u)
            h[mask] -= 0.04 * s
    # Monotone water bed and 2.5 m landward bank, keyed from each source lake.
    q = points(p[:, 0], p[:, 1])
    d2 = ((p[:, 0] >= 126 - 1e-7) & (p[:, 0] <= 168 + 1e-7) &
          (p[:, 1] >= 43 - 1e-7) & (p[:, 1] <= 86 + 1e-7))
    for geom, level in zip(water_geoms, water_levels):
        if geom.is_empty:
            continue
        dwater = np.asarray(geom.distance(q), dtype=np.float64)
        near = (dwater <= 2.5) & ~d2
        if not near.any():
            continue
        ids = np.flatnonzero(near)
        qnear = q[ids]
        d = np.asarray(geom.boundary.distance(qnear), dtype=np.float64)
        inside = np.asarray(covers(geom, qnear), dtype=bool)
        s = np.clip(d / np.where(inside, 3.0, 2.5), 0, 1)
        s = s * s * (3 - 2 * s)
        target = np.where(inside, level - 1.0, h[ids])
        h[ids] = level + (target - level) * s
    return h


def slope_degrees(p3, t):
    a, b, c = p3[t[:, 0]], p3[t[:, 1]], p3[t[:, 2]]
    n = np.cross(b - a, c - a)
    ln = np.linalg.norm(n, axis=1)
    ny = np.abs(n[:, 1]) / np.maximum(ln, 1e-30)
    return np.degrees(np.arccos(np.clip(ny, 0, 1))), n / np.maximum(ln[:, None], 1e-30)


def glb_write(path: Path, name: str, primitives):
    blob = bytearray()
    views, accessors = [], []

    def put(arr, typ, ct, target, minmax=False):
        arr = np.ascontiguousarray(arr)
        while len(blob) % 4:
            blob.append(0)
        start = len(blob)
        blob.extend(arr.tobytes())
        views.append({"buffer": 0, "byteOffset": start, "byteLength": arr.nbytes, "target": target})
        acc = {"bufferView": len(views) - 1, "componentType": ct, "count": int(arr.shape[0]), "type": typ}
        if minmax:
            acc["min"], acc["max"] = arr.min(axis=0).tolist(), arr.max(axis=0).tolist()
        accessors.append(acc)
        return len(accessors) - 1

    prims = []
    for pr in primitives:
        pos = pr["pos"].astype(np.float32)
        if not len(pos):
            continue
        attrs = {"POSITION": put(pos, "VEC3", 5126, 34962, True),
                 "NORMAL": put(pr["normal"].astype(np.float32), "VEC3", 5126, 34962),
                 "TEXCOORD_0": put(pr["uv0"].astype(np.float32), "VEC2", 5126, 34962),
                 "TEXCOORD_1": put(pr["uv1"].astype(np.float32), "VEC2", 5126, 34962),
                 "TEXCOORD_2": put(pr["uv2"].astype(np.float32), "VEC2", 5126, 34962),
                 "_FLAECHE": put(pr["flaeche"].astype(np.uint8).reshape(-1, 1), "SCALAR", 5121, 34962)}
        prims.append({"attributes": attrs, "mode": 4, "extras": {"klasse": int(pr["klasse"])}})
    while len(blob) % 4:
        blob.append(0)
    js = {"asset": {"version": "2.0", "generator": "detail_v2 P2 regular snapped grid"}, "scene": 0,
          "scenes": [{"nodes": [0]}], "nodes": [{"mesh": 0, "name": name}],
          "meshes": [{"name": name, "primitives": prims}], "buffers": [{"byteLength": len(blob)}],
          "bufferViews": views, "accessors": accessors}
    j = json.dumps(js, separators=(",", ":")).encode("utf-8")
    j += b" " * (-len(j) % 4)
    total = 12 + 8 + len(j) + 8 + len(blob)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, total))
        f.write(struct.pack("<I4s", len(j), b"JSON")); f.write(j)
        f.write(struct.pack("<I4s", len(blob), b"BIN\x00")); f.write(blob)


def pack_primitives(pos_tri, normals, uv2_tri, classes):
    prims = []
    # Nonindexed triangles make class boundaries explicit and duplicate every
    # shared vertex that carries different _FLAECHE values.
    for cl in range(6):
        ix = np.flatnonzero(classes == cl)
        if not len(ix):
            continue
        p = pos_tri[ix].reshape(-1, 3).astype(np.float32)
        n = np.repeat(normals[ix], 3, axis=0).astype(np.float32)
        uv0 = p[:, [0, 2]].copy()
        uv1 = np.column_stack((p[:, 0] / NX, p[:, 2] / NZ)).astype(np.float32)
        u2 = uv2_tri[ix].reshape(-1, 2).astype(np.float32) if cl == 1 else np.zeros((len(p), 2), np.float32)
        fl = np.full(len(p), cl, np.uint8)
        prims.append({"klasse": cl, "pos": p, "normal": n, "uv0": uv0, "uv1": uv1, "uv2": u2, "flaeche": fl})
    return prims


def way_uv(pos_tri, line_geoms, widths):
    pts = pos_tri[:, :, [0, 2]].reshape(-1, 2)
    if not len(pts) or not line_geoms:
        return np.zeros((len(pos_tri), 3, 2), np.float32)
    tree = STRtree(line_geoms)
    q = points(pts[:, 0], pts[:, 1])
    ids = tree.nearest(q)
    lines = np.asarray(line_geoms, dtype=object)[ids]
    station = np.asarray(line_locate_point(lines, q), dtype=np.float64)
    nearest = get_coordinates(line_interpolate_point(lines, station))
    lengths = np.asarray([g.length for g in lines], dtype=np.float64)
    aa = get_coordinates(line_interpolate_point(lines, np.maximum(0, station - 0.02)))
    bb = get_coordinates(line_interpolate_point(lines, np.minimum(lengths, station + 0.02)))
    tang = bb - aa
    tang /= np.maximum(np.linalg.norm(tang, axis=1)[:, None], 1e-12)
    delta = pts - nearest
    signed = tang[:, 0] * delta[:, 1] - tang[:, 1] * delta[:, 0]
    # Use the source road width associated with the nearest centerline.
    v = np.clip(0.5 + signed / np.maximum(np.asarray(widths)[ids], 0.1), 0, 1)
    out = np.column_stack((station, v)).astype(np.float32)
    return out.reshape(-1, 3, 2)


def triangle_quality(p3, t, centroid, constraint_vertex_tree, road_union):
    xy = p3[t][:, :, [0, 2]]
    e = np.stack((np.linalg.norm(xy[:, 1] - xy[:, 0], axis=1), np.linalg.norm(xy[:, 2] - xy[:, 1], axis=1), np.linalg.norm(xy[:, 0] - xy[:, 2], axis=1)), axis=1)
    lengths = np.sort(e, axis=1)
    # min angle from the cosine rule
    a, b, c = e[:, 0], e[:, 1], e[:, 2]
    angles = np.column_stack((np.arccos(np.clip((b*b+c*c-a*a)/(2*b*c+1e-20), -1, 1)),
                              np.arccos(np.clip((a*a+c*c-b*b)/(2*a*c+1e-20), -1, 1)),
                              np.arccos(np.clip((a*a+b*b-c*c)/(2*a*b+1e-20), -1, 1))))
    near, _ = constraint_vertex_tree.query(centroid, k=1, workers=1)
    in_band = near <= 1.55
    in_road = contains_xy(road_union, centroid[:, 0], centroid[:, 1]) if not road_union.is_empty else np.zeros(len(t), bool)
    return {"min_angle_deg": float(np.degrees(angles.min())), "max_edge_m": float(e.max()),
            "band_max_edge_m": float(e[in_band].max()) if in_band.any() else 0.0,
            "road_max_edge_m": float(e[in_road].max()) if in_road.any() else 0.0,
            "upward_normals": True}


def build(args):
    t0 = time.time()
    vec, classes, roads, constraint_geom, constraint_lines, constraint_tree, _, under, walk, cliff = load_inputs()
    roads_tree = STRtree(roads) if roads else None
    source = load_relief(RELIEF / "relief_daten.json.gz")
    rs = int(source.data["rs"])
    field = source.heights
    water_geoms, water_levels = [], []
    for f in vec["wasser"]:
        p = f.get("properties") or {}
        geom = Polygon(f["geometry"]["coordinates"][0], f["geometry"]["coordinates"][1:]) if f["geometry"]["type"] == "Polygon" else MultiPolygon([Polygon(q[0], q[1:]) for q in f["geometry"]["coordinates"]])
        water_geoms.append(geom)
        water_levels.append(float(p.get("spiegel_m_median", -100.0)))
    shore = [(g, y) for g, y in zip(water_geoms, water_levels)]
    line_geoms, widths = [], []
    for f in vec["wege"]:
        p = f.get("properties") or {}
        if p.get("rolle") == "mittellinie":
            line_geoms.append(LineString(f["geometry"]["coordinates"]))
            widths.append(float(p.get("breite", 3.0)))
    centerline_tree = STRtree(line_geoms) if line_geoms else None
    (HERE / "kacheln").mkdir(parents=True, exist_ok=True)
    (HERE / "modelle").mkdir(parents=True, exist_ok=True)
    manifest_tiles_by_id = {}
    diagnostics = {"method": "triangle Shewchuk CDT, tile-local PSLG", "tiles": {},
                   "height": {}, "constraints": {}, "csv_walkability": {}, "time_s": {}}
    report_path, manifest_path = HERE / "build_report.json", HERE / "manifest.json"
    if args.kacheln and report_path.exists() and manifest_path.exists():
        try:
            prev_report, prev_manifest = read_json(report_path), read_json(manifest_path)
            if prev_report.get("method") == diagnostics["method"]:
                diagnostics["tiles"].update(prev_report.get("tiles", {}))
                manifest_tiles_by_id.update({x["id"]: x for x in prev_manifest.get("kacheln", [])})
        except (OSError, ValueError, KeyError):
            pass
    total_area_by_class = np.zeros(6, dtype=np.float64)
    tile_ids = args.kacheln.split(",") if args.kacheln else [f"{LETTERS[i]}{j+1}" for j in range(7) for i in range(8)]
    total_tri = 0
    village = Point(209.0, 118.0)
    for kid in tile_ids:
        i, j = LETTERS.index(kid[0]), int(kid[1]) - 1
        b = tile_bounds(i, j)
        tile_poly = box(*b)
        if roads_tree is not None:
            road_ids = roads_tree.query(tile_poly)
            local_roads = np.asarray(roads_tree.geometries, dtype=object)[road_ids]
            road_union = unary_union([g.intersection(tile_poly) for g in local_roads if g.intersects(tile_poly)])
        else:
            road_union = GeometryCollection()
        # E2 has a sharp, noded bridge/shore constraint junction. q30 exhausted
        # memory and q28 exceeded the tile budget, so use the authorized q25
        # acute-corner fallback for this tile only. Other tiles remain q30.
        quality_angle = 25 if kid == "E2" else 30
        p, t, repair, constraint_vertex_tree = cdt_tile(b, constraint_geom, constraint_tree, road_union, centerline_tree, quality_angle)
        # Remove any numerical spill outside the exact tile rectangle.
        cent = p[t].mean(axis=1)
        inside = ((cent[:, 0] >= b[0]-EPS) & (cent[:, 0] <= b[2]+EPS) &
                  (cent[:, 1] >= b[1]-EPS) & (cent[:, 1] <= b[3]+EPS))
        t, cent = t[inside], cent[inside]
        h = terrain_heights(p, field, roads, road_union, vec, water_geoms, water_levels)
        p3 = np.column_stack((p[:, 0], h, p[:, 1]))
        pos_tri = p3[t]
        grades, normals = slope_degrees(p3, t)
        # Point-in-polygon assignment uses source priority Water > Bridge > Road > Shore > Rock > Ground.
        centers = points(cent[:, 0], cent[:, 1])
        local_geoms, local_meta = [], []
        tile_poly = box(*b)
        for geom, cl, sub, zid in classes:
            if geom.intersects(tile_poly):
                local_geoms.append(geom)
                local_meta.append((geom, cl, sub, zid))
        cls = np.zeros(len(t), dtype=np.uint8)
        rank = np.zeros(len(t), dtype=np.uint8)
        if local_geoms:
            tree = STRtree(local_geoms)
            pairs = tree.query(centers)
            if pairs.size:
                ti, gi = pairs
                hit = covers(np.asarray(local_geoms, dtype=object)[gi], centers[ti])
                for gg, tt in zip(gi[hit], ti[hit]):
                    cc = local_meta[int(gg)][1]
                    if RANK[cc] > rank[tt]:
                        cls[tt], rank[tt] = cc, RANK[cc]
        cx = np.clip(np.floor(cent[:, 0]).astype(int), 0, NX-1)
        cz = np.clip(np.floor(cent[:, 1]).astype(int), 0, NZ-1)
        # Begehbare Felszellen only become rock above 35 degrees; KLIPPE_WAND is fixed class 3.
        wall = under[cz, cx] == "KLIPPE_WAND"
        rock_cell = np.isin(under[cz, cx], ("FELS", "KLIPPE_KANTE", "KLIPPE_WAND"))
        walkable_rock = rock_cell & walk[cz, cx].astype(bool) & np.isin(cls, (0, 3)) & ~wall
        cls[walkable_rock & (grades > 35.0)] = 3
        cls[walkable_rock & (grades <= 35.0)] = 0
        cls[wall & np.isin(cls, (0, 3))] = 3
        # Mirror bed stays class 4; bridge deck is prepared as class 5 surface.
        area = 0.5 * np.abs((pos_tri[:, 1, 0] - pos_tri[:, 0, 0]) * (pos_tri[:, 2, 2] - pos_tri[:, 0, 2]) -
                           (pos_tri[:, 1, 2] - pos_tri[:, 0, 2]) * (pos_tri[:, 2, 0] - pos_tri[:, 0, 0]))
        tile_area_by_class = np.asarray([float(area[cls == cl].sum()) for cl in range(6)], dtype=np.float64)
        uv2 = np.zeros((len(t), 3, 2), dtype=np.float32)
        road_tri = cls == 1
        if road_tri.any():
            uv2[road_tri] = way_uv(pos_tri[road_tri], line_geoms, widths)
        prims = pack_primitives(pos_tri, normals, uv2, cls)
        out_file = HERE / "kacheln" / f"{kid}.glb"
        glb_write(out_file, f"gelaende_{kid}", prims)
        nt = len(t)
        total_tri += nt
        if nt > MAX_TILE_TRIANGLES:
            raise RuntimeError(f"{kid}: Dreiecksbudget ueberschritten: {nt}")
        frac = {CLASSES[c]: float(area[cls == c].sum() / max(float(area.sum()), 1e-30)) for c in range(6) if np.any(cls == c)}
        manifest_tiles_by_id[kid] = {"id": kid, "glb": f"kacheln/{kid}.glb", "bbox": list(b), "dreiecke": nt,
                                     "klassen_anteil": frac}
        q = triangle_quality(p3, t, cent, constraint_vertex_tree, road_union)
        diagnostics["tiles"][kid] = {**repair, **q, "dreiecke": nt, "vertices": len(p),
                                     "missing_constraint_fraction": None,
                                     "klassen_flaeche_m2": tile_area_by_class.tolist()}
        print(f"{kid}: CDT {repair['pslg_segments']:,} Segmente, {nt:,} Dreiecke, "
              f"{len(p):,} Punkte", flush=True)
        del p, t, pos_tri, grades, normals, prims, uv2, h, p3, area, cls, cent, q
        import gc
        gc.collect()
        try:
            import ctypes
            ctypes.CDLL("libc.so.6").malloc_trim(0)
        except Exception:
            pass
    # Every lake/stream area is exported as an independent class-4 surface model.
    model_entries = []
    try:
        from shapely import constrained_delaunay_triangles
        cdt = constrained_delaunay_triangles
    except ImportError:
        cdt = None
    for f in vec["wasser"]:
        prop = f.get("properties") or {}
        wid = str(prop.get("id", f"W{len(model_entries)+1:02d}"))
        geom = Polygon(f["geometry"]["coordinates"][0], f["geometry"]["coordinates"][1:]) if f["geometry"]["type"] == "Polygon" else MultiPolygon([Polygon(q[0], q[1:]) for q in f["geometry"]["coordinates"]])
        triangles = []
        if cdt:
            tri_geom = cdt(geom)
            triangles = [g for g in polygon_parts(tri_geom) if len(g.exterior.coords) == 4 and g.area > 1e-10]
        else:
            for poly in polygon_parts(geom):
                triangles.extend(q for q in triangulate(poly) if poly.covers(q.representative_point()))
        if not triangles:
            raise RuntimeError(f"Wasseroberflaeche {wid}: constrained triangulation leer")
        tri_xz = np.asarray([[list(g.exterior.coords)[k][:2] for k in range(3)] for g in triangles], dtype=np.float32)
        # force clockwise XZ winding so normals point upward
        signed = (tri_xz[:,1,0]-tri_xz[:,0,0])*(tri_xz[:,2,1]-tri_xz[:,0,1])-(tri_xz[:,1,1]-tri_xz[:,0,1])*(tri_xz[:,2,0]-tri_xz[:,0,0])
        flp = signed > 0
        tri_xz[flp, 1], tri_xz[flp, 2] = tri_xz[flp, 2].copy(), tri_xz[flp, 1].copy()
        level = float(prop.get("spiegel_m_median", -100.0))
        pos = np.column_stack((tri_xz.reshape(-1,2)[:,0], np.full(len(triangles)*3, level), tri_xz.reshape(-1,2)[:,1])).astype(np.float32)
        n = np.zeros_like(pos); n[:,1] = 1
        uv0 = pos[:,[0,2]].copy(); uv1 = np.column_stack((pos[:,0]/NX,pos[:,2]/NZ)).astype(np.float32)
        uv2 = np.zeros((len(pos),2),np.float32); cls4 = np.full(len(pos),4,np.uint8)
        glb_write(HERE/"modelle"/f"wasser_{wid}.glb", f"wasser_{wid}", [{"klasse":4,"pos":pos,"normal":n,"uv0":uv0,"uv1":uv1,"uv2":uv2,"flaeche":cls4}])
        model_entries.append({"id":f"wasser_{wid}","glb":f"modelle/wasser_{wid}.glb","klasse":4,"spiegel_m":level})
    manifest_tiles = [manifest_tiles_by_id[k] for k in sorted(manifest_tiles_by_id,
                       key=lambda x: (int(x[1:]), LETTERS.index(x[0])))]
    total_tri = sum(int(x["dreiecke"]) for x in manifest_tiles)
    diagnostics["tiles"] = {k: diagnostics["tiles"][k] for k in sorted(diagnostics["tiles"],
                             key=lambda x: (int(x[1:]), LETTERS.index(x[0])))}
    total_area_by_class[:] = 0
    for td in diagnostics["tiles"].values():
        total_area_by_class += np.asarray(td.get("klassen_flaeche_m2", [0] * 6), dtype=np.float64)
    total_areas = float(total_area_by_class.sum())
    manifest = {"version":1,"einheit":"m","ursprung":"weltecke","karte":{"breite":336,"tiefe":303},
      "klassen":{str(k):v for k,v in CLASSES.items()},"attribute":{"flaeche":"_FLAECHE"},
      "uv":{"TEXCOORD_0":"welt_xz_m","TEXCOORD_1":"karte_norm","TEXCOORD_2":"wegband"},
      "kacheln":manifest_tiles,"modelle":model_entries}
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    diagnostics["dreiecke_gesamt"] = total_tri
    diagnostics["max_dreiecke_kachel"] = max((x["dreiecke"] for x in manifest_tiles), default=0)
    diagnostics["klassen_flaeche_m2"] = {CLASSES[i]: float(total_area_by_class[i]) for i in range(6)}
    diagnostics["kartenflaeche_m2"] = total_areas
    diagnostics["d2_ref_max_dh_m"] = d2_delta(HERE, field)
    diagnostics["quelle_gb_shape"] = list(field.shape)
    diagnostics["dateien"] = {"kacheln":len(manifest_tiles),"wassermodelle":len(model_entries)}
    diagnostics["time_s"] = {"gesamt":round(time.time()-t0,2)}
    report_path.write_text(json.dumps(diagnostics,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if total_tri > MAX_TRIANGLES:
        raise RuntimeError(f"Gesamt-Dreiecksbudget ueberschritten: {total_tri}")
    print(json.dumps({"tiles":len(manifest_tiles),"triangles":total_tri,"max_tile":diagnostics["max_dreiecke_kachel"],
                      "water_models":len(model_entries),"seconds":diagnostics["time_s"]["gesamt"]},ensure_ascii=False))


def d2_delta(here, field):
    ref = Path("/tmp/qa_ec77356/team/art/dorfmap_grundgeruest/relief3d/detail_v2/qa/referenz/d2_alt.npz")
    if not ref.exists():
        return None
    xyz = np.load(ref, allow_pickle=False)["xyz"].astype(np.float64)
    got = interp_height(field, xyz[:,[0,2]])
    return float(np.max(np.abs(got - xyz[:,1])))


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--kacheln",default=""); a=ap.parse_args()
    build(a)


if __name__ == "__main__":
    main()
