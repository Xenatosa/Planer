#!/usr/bin/env python3
"""P1c: deterministic cliff, ridge and coverage GeoJSON extraction.

Coordinates follow neu.mesh.tile_mesh(): x and z are raster coordinates / rs.
Cell polygons occupy [cx,cx+1] x [cy,cy+1], so their centers are cx+.5,cy+.5.
"""
from __future__ import annotations

import argparse
import base64
import csv
import gzip
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi
from shapely import contains_xy, coverage_simplify, get_parts, line_merge, make_valid, unary_union
from shapely.geometry import LineString, MultiLineString, Point, Polygon, box, mapping, shape
from shapely.ops import polygonize
from shapely.strtree import STRtree
from skimage.measure import find_contours
from skimage.morphology import skeletonize


HERE = Path(__file__).resolve().parent
RELIEF = HERE.parents[1]
ROOT = RELIEF.parents[0]
CELLS = RELIEF / "neu" / "zellen_relief.csv"
OVERLAY = ROOT / "raster_c20_z25_overlay_plaetze_wege.csv"
EXTENSION = ROOT / "overlay_plaetze_erweiterung.json"
RELIEF_GZ = RELIEF / "relief_daten.json.gz"
TARGETS = ((300.0, 90.0, "G3H3"), (290.0, 98.0, "G3H3"), (84.0, 129.0, "B3C3"))
SURFACE_PRIORITY = ("wasser", "bruecke", "weg", "ufer", "fels", "grund")
SMOOTH_COVERAGE_STATUS = []


def compact_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True,
                               separators=(",", ":")) + "\n", encoding="utf-8")


def geojson(features: list[dict]) -> dict:
    return {"type": "FeatureCollection", "features": features}


def feature(geom, props: dict) -> dict:
    return {"type": "Feature", "geometry": mapping(geom), "properties": props}


def round_xy(points: np.ndarray, digits: int = 6) -> np.ndarray:
    p = np.asarray(points, dtype=float)
    if len(p) == 0:
        return p.reshape((0, 2))
    p = np.round(p[:, :2], digits)
    keep = np.ones(len(p), dtype=bool)
    if len(p) > 1:
        keep[1:] = np.any(np.diff(p, axis=0) != 0, axis=1)
    return p[keep]


def catmull_rom(points: np.ndarray, step: float = 0.20, alpha: float = 0.5,
                closed: bool = False) -> np.ndarray:
    """Centripetal Catmull-Rom, sampled by chord length at <= step metres."""
    p = round_xy(points)
    if len(p) < 3:
        return p
    if closed and np.allclose(p[0], p[-1]):
        p = p[:-1]
    if closed and len(p) < 3:
        return np.vstack([p, p[:1]])
    out = []
    n = len(p)
    segments = n if closed else n - 1

    def at(i):
        if closed:
            return p[i % n]
        return p[max(0, min(n - 1, i))]

    for i in range(segments):
        p0, p1, p2, p3 = at(i - 1), at(i), at(i + 1), at(i + 2)
        chord = max(float(np.linalg.norm(p2 - p1)), 1e-8)
        count = max(1, int(math.ceil(chord / step)))
        t0 = 0.0
        t1 = t0 + max(float(np.linalg.norm(p1 - p0)) ** alpha, 1e-6)
        t2 = t1 + max(float(np.linalg.norm(p2 - p1)) ** alpha, 1e-6)
        t3 = t2 + max(float(np.linalg.norm(p3 - p2)) ** alpha, 1e-6)
        for j in range(count):
            t = t1 + (t2 - t1) * (j / count)
            a1 = ((t1 - t) / (t1 - t0)) * p0 + ((t - t0) / (t1 - t0)) * p1
            a2 = ((t2 - t) / (t2 - t1)) * p1 + ((t - t1) / (t2 - t1)) * p2
            a3 = ((t3 - t) / (t3 - t2)) * p2 + ((t - t2) / (t3 - t2)) * p3
            b1 = ((t2 - t) / (t2 - t0)) * a1 + ((t - t0) / (t2 - t0)) * a2
            b2 = ((t3 - t) / (t3 - t1)) * a2 + ((t - t1) / (t3 - t1)) * a3
            out.append(((t2 - t) / (t2 - t1)) * b1 + ((t - t1) / (t2 - t1)) * b2)
    if not closed:
        out.append(p[-1])
    else:
        out.append(out[0])
    return round_xy(np.asarray(out))


def chaikin(points: np.ndarray, iterations: int = 2, closed: bool = False) -> np.ndarray:
    p = round_xy(points)
    if len(p) < 3:
        return p
    if closed and np.allclose(p[0], p[-1]):
        p = p[:-1]
    for _ in range(iterations):
        q = []
        if not closed:
            q.append(p[0])
        for a, b in zip(p, np.roll(p, -1, axis=0) if closed else p[1:]):
            q.extend((0.75 * a + 0.25 * b, 0.25 * a + 0.75 * b))
        if not closed:
            q.append(p[-1])
        p = np.asarray(q)
    if closed:
        p = np.vstack((p, p[:1]))
    return round_xy(p)


def smooth_line(line: LineString, dp: float, step: float = 0.20,
                chaikin_n: int = 0, lowpass_m: float = 2.0) -> LineString | None:
    if line.length < 0.75:
        return None
    simplified = line.simplify(dp, preserve_topology=True)
    if simplified.geom_type != "LineString" or len(simplified.coords) < 3:
        simplified = line
    p = np.asarray(simplified.coords, dtype=float)
    closed = np.linalg.norm(p[0] - p[-1]) < 1e-7
    if chaikin_n:
        p = chaikin(p, chaikin_n, closed)
    p = catmull_rom(p, step=min(step, 0.10), closed=closed)
    # An arc-length low-pass removes the residual 0.5/1 m raster tooth.
    # Endpoints are fixed for a shared planar graph; closed rings wrap.
    if closed and len(p) > 3 and np.linalg.norm(p[0] - p[-1]) < 1e-7:
        p = p[:-1]
    if len(p) >= 12:
        sigma_samples = lowpass_m / 0.10
        mode = "wrap" if closed else "nearest"
        p0, p1 = p[0].copy(), p[-1].copy()
        p = ndi.gaussian_filter1d(p, sigma=sigma_samples, axis=0, mode=mode)
        if not closed:
            p[0], p[-1] = p0, p1
    if closed:
        p = np.vstack((p, p[:1]))
    # Re-parameterize after filtering so output segments remain <= 0.1 m.
    path = LineString(p)
    ds = min(step, 0.10)
    sampled = [path.interpolate(float(s)).coords[0] for s in np.arange(0.0, path.length, ds)]
    if closed:
        sampled.append(sampled[0])
    else:
        sampled.append(path.coords[-1])
    p = round_xy(np.asarray(sampled))
    if len(p) < 2:
        return None
    result = LineString(p)
    return result if result.length >= 0.5 else None


def height_sampler(gb: np.ndarray, rs: int):
    def sample(points):
        p = np.asarray(points, dtype=float)
        vals = ndi.map_coordinates(gb, [p[:, 1] * rs, p[:, 0] * rs],
                                  order=3, mode="nearest", prefilter=True)
        # Bound cubic interpolation to a local 2x2 node envelope (monotone).
        ix = np.clip(np.floor(p[:, 0] * rs).astype(int), 0, gb.shape[1] - 2)
        iz = np.clip(np.floor(p[:, 1] * rs).astype(int), 0, gb.shape[0] - 2)
        lo = np.minimum.reduce([gb[iz, ix], gb[iz, ix + 1], gb[iz + 1, ix], gb[iz + 1, ix + 1]])
        hi = np.maximum.reduce([gb[iz, ix], gb[iz, ix + 1], gb[iz + 1, ix], gb[iz + 1, ix + 1]])
        return np.round(np.clip(vals, lo, hi).astype(float), 4)
    return sample


def contour_cell_mask(mask: np.ndarray) -> list[LineString]:
    """Cell-center mask contours, mapped to integer cell edges."""
    pad = np.pad(mask.astype(np.uint8), 1)
    result = []
    for c in find_contours(pad, 0.5, fully_connected="low", positive_orientation="low"):
        # padded index 1 is center of cell 0 at world .5 -> world=index-.5
        pts = np.column_stack((c[:, 1] - 0.5, c[:, 0] - 0.5))
        if len(pts) >= 4:
            line = LineString(pts)
            if line.length >= 1.0:
                result.append(line)
    return result


def contour_node_mask(mask: np.ndarray, rs: int) -> list[LineString]:
    """Contour of a sampled GB-node mask, with nodes at x=i/rs,z=j/rs."""
    pad = np.pad(mask.astype(np.uint8), 1)
    result = []
    for c in find_contours(pad, 0.5, fully_connected="low", positive_orientation="low"):
        pts = np.column_stack(((c[:, 1] - 1.0) / rs, (c[:, 0] - 1.0) / rs))
        if len(pts) >= 4:
            line = LineString(pts)
            if line.length >= 1.0:
                result.append(line)
    return result


def contour_node_field(field: np.ndarray, level: float, rs: int) -> list[LineString]:
    """Sub-grid isolines from a continuous GB-derived field."""
    pad = np.pad(field.astype(float), 1, constant_values=min(float(np.nanmin(field)) - 1.0, level - 1.0))
    result = []
    for c in find_contours(pad, level, fully_connected="low", positive_orientation="low"):
        pts = np.column_stack(((c[:, 1] - 1.0) / rs, (c[:, 0] - 1.0) / rs))
        if len(pts) >= 4:
            line = LineString(pts)
            if line.length >= 1.0:
                result.append(line)
    return result


def linestring_parts(geom):
    if geom.is_empty:
        return []
    if geom.geom_type == "LineString":
        return [geom]
    if geom.geom_type in ("MultiLineString", "GeometryCollection"):
        out = []
        for g in geom.geoms:
            out.extend(linestring_parts(g))
        return out
    return []


def extract_skeleton_paths(skeleton: np.ndarray, rs: int) -> list[np.ndarray]:
    """Convert 8-connected skeleton pixels into deterministic open/closed paths."""
    yy, xx = np.where(skeleton)
    nodes = set(zip(yy.tolist(), xx.tolist()))
    nbrs = {}
    for y, x in nodes:
        n = [(y + dy, x + dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1)
             if (dy or dx) and (y + dy, x + dx) in nodes]
        nbrs[(y, x)] = sorted(n)
    visited = set()
    paths = []
    starts = sorted((p for p in nodes if len(nbrs[p]) != 2))
    for start in starts:
        for nxt in nbrs[start]:
            edge = tuple(sorted((start, nxt)))
            if edge in visited:
                continue
            path = [start]
            prev, cur = start, nxt
            visited.add(edge)
            while True:
                path.append(cur)
                if len(nbrs[cur]) != 2:
                    break
                candidates = [p for p in nbrs[cur] if p != prev]
                if not candidates:
                    break
                nxt2 = candidates[0]
                e2 = tuple(sorted((cur, nxt2)))
                if e2 in visited:
                    break
                visited.add(e2)
                prev, cur = cur, nxt2
            if len(path) >= 3:
                p = np.array([[x / rs, y / rs] for y, x in path], dtype=float)
                if np.linalg.norm(p[0] - p[-1]) < 1e-7:
                    p[-1] = p[0]
                paths.append(p)
    # All-degree-two components are loops.
    for start in sorted(nodes):
        for nxt in nbrs[start]:
            edge = tuple(sorted((start, nxt)))
            if edge in visited:
                continue
            path = [start]
            prev, cur = start, nxt
            visited.add(edge)
            while cur != start:
                path.append(cur)
                options = [p for p in nbrs[cur] if p != prev]
                if not options:
                    break
                nxt2 = options[0]
                e2 = tuple(sorted((cur, nxt2)))
                if e2 in visited:
                    cur = start
                    break
                visited.add(e2)
                prev, cur = cur, nxt2
            if len(path) >= 3:
                path.append(start)
                paths.append(np.array([[x / rs, y / rs] for y, x in path], dtype=float))
    paths.sort(key=lambda p: (-LineString(p).length, tuple(np.round(p[0], 4))))
    return paths


def hessian_ridges(gb: np.ndarray, rs: int) -> list[np.ndarray]:
    # Sigma=0.75 m removes the 0.5-m raster tooth before the Hessian.
    h = ndi.gaussian_filter(gb, sigma=1.5, mode="nearest")
    dz, dx = np.gradient(h, 1 / rs, 1 / rs)
    hzz, hzx = np.gradient(dz, 1 / rs, 1 / rs)
    hxz, hxx = np.gradient(dx, 1 / rs, 1 / rs)
    hxz = (hxz + hzx) * 0.5
    tr = hxx + hzz
    disc = np.sqrt(np.maximum((hxx - hzz) ** 2 + 4 * hxz ** 2, 0))
    low, high = (tr - disc) * 0.5, (tr + disc) * 0.5
    # Eigenvector belonging to the most negative curvature (ridge normal).
    vx, vz = hxz, low - hxx
    norm = np.hypot(vx, vz)
    bad = norm < 1e-10
    vx[bad], vz[bad] = 1, 0
    norm = np.hypot(vx, vz)
    vx, vz = vx / norm, vz / norm
    cross_gradient = np.abs(dx * vx + dz * vz)
    candidate = (low < -0.025) & (cross_gradient < 0.14) & (high < 0.18)
    return extract_skeleton_paths(skeletonize(candidate), rs)


def hessian_tangent_trace(gb: np.ndarray, rs: int, anchor: tuple[float, float], span: float = 12.0) -> LineString:
    """Trace the Hessian principal direction from a prescribed ridge control point."""
    h = ndi.gaussian_filter(gb.astype(float), sigma=1.5, mode="nearest")
    dz, dx = np.gradient(h, 1 / rs, 1 / rs)
    hzz, hzx = np.gradient(dz, 1 / rs, 1 / rs)
    hxz, hxx = np.gradient(dx, 1 / rs, 1 / rs)
    cross = (hxz + hzx) * 0.5
    theta = 0.5 * np.arctan2(2 * cross, hxx - hzz)
    tx, tz = np.cos(theta), np.sin(theta)

    def tangent(pt, previous):
        v = np.array([ndi.map_coordinates(tx, [[pt[1] * rs], [pt[0] * rs]], order=1, mode="nearest")[0],
                      ndi.map_coordinates(tz, [[pt[1] * rs], [pt[0] * rs]], order=1, mode="nearest")[0]])
        n = np.linalg.norm(v)
        v = v / n if n else np.array([1.0, 0.0])
        return -v if np.dot(v, previous) < 0 else v

    origin = np.asarray(anchor, dtype=float)
    result = []
    ds = 0.20
    nstep = int(span / ds)
    for direction in (-1, 1):
        pt = origin.copy()
        v0 = tangent(pt, np.array([1.0, 0.0]))
        prev = direction * v0
        side = [pt.copy()]
        for _ in range(nstep):
            v = tangent(pt, prev)
            if direction < 0 and np.dot(v, prev) < 0:
                v = -v
            if direction > 0 and np.dot(v, prev) < 0:
                v = -v
            pt = pt + ds * v
            side.append(pt.copy())
            prev = v
        if direction < 0:
            result = list(reversed(side))[:-1]
        else:
            result.extend(side)
    result[len(result) // 2] = origin
    return LineString(result)


def component_cell_geometries(codes: np.ndarray, labels: list[tuple]) -> dict[tuple, object]:
    """Union horizontal same-label cell runs; avoids one box per source cell."""
    shapes = defaultdict(list)
    ny, nx = codes.shape
    for y in range(ny):
        row = codes[y]
        starts = np.r_[0, np.flatnonzero(row[1:] != row[:-1]) + 1]
        ends = np.r_[starts[1:], nx]
        for x0, x1 in zip(starts, ends):
            code = int(row[x0])
            if code >= 0:
                shapes[code].append(box(float(x0), float(y), float(x1), float(y + 1)))
    return {labels[i]: unary_union(parts) for i, parts in shapes.items() if parts}


def polygon_parts(geom):
    if geom.geom_type == "Polygon":
        return [geom]
    if geom.geom_type in ("MultiPolygon", "GeometryCollection"):
        out = []
        for g in geom.geoms:
            out.extend(polygon_parts(g))
        return out
    return []


def smooth_coverage(geoms: list[Polygon], dp: float, sample_step: float) -> list[Polygon]:
    """Simplify a complete polygon coverage, smooth its shared linework once, polygonize."""
    if not geoms:
        return []
    simplified = coverage_simplify(geoms, tolerance=dp, simplify_boundary=True)
    bounds = box(0, 0, 336, 303)
    linework = unary_union([g.boundary for g in simplified if not g.is_empty])
    merged = line_merge(linework)
    smooth_parts = []
    for line in linestring_parts(merged):
        if line.length < 0.25:
            continue
        coords = np.asarray(line.coords)
        on_map_edge = np.all((np.abs(coords[:, 0]) < 1e-7) | (np.abs(coords[:, 0] - 336) < 1e-7) |
                             (np.abs(coords[:, 1]) < 1e-7) | (np.abs(coords[:, 1] - 303) < 1e-7))
        smooth = line if on_map_edge else smooth_line(line, dp=dp * 0.4, step=sample_step, chaikin_n=2)
        if smooth is not None:
            smooth_parts.append(smooth)
    if not smooth_parts:
        SMOOTH_COVERAGE_STATUS.append({"result": "fallback_no_lines"})
        return [p for g in simplified for p in polygon_parts(g)]
    # Catmull segments can cross between nearby boundaries; node the complete
    # planar graph before polygonizing, so every face is a valid ring.
    noded = unary_union(smooth_parts)
    faces = list(polygonize(noded))
    kept = []
    for p in faces:
        p = make_valid(p)
        q = p.intersection(bounds)
        if q.area > 1e-8:
            kept.extend(polygon_parts(make_valid(q)))
    # All original perimeter edges are fixed; reject smoothing if it loses coverage.
    union = unary_union(kept) if kept else Polygon()
    gap_area = abs(union.symmetric_difference(bounds).area) if union.is_valid else float("inf")
    if not union.is_valid or gap_area > 1e-5:
        SMOOTH_COVERAGE_STATUS.append({"result": "fallback_coverage", "faces": len(faces), "error_m2": gap_area})
        return [p for g in simplified for p in polygon_parts(g)]
    SMOOTH_COVERAGE_STATUS.append({"result": "smoothed", "faces": len(faces), "error_m2": gap_area})
    return kept


def zacken_and_kinks(lines: list[LineString], window: float = 1.0) -> tuple[float, float]:
    max_amp, max_angle = 0.0, 0.0
    for line in lines:
        p = np.asarray(line.coords, dtype=float)
        if len(p) < 3:
            continue
        seg = np.linalg.norm(np.diff(p, axis=0), axis=1)
        arc = np.r_[0.0, np.cumsum(seg)]
        total = arc[-1]
        closed = np.linalg.norm(p[0] - p[-1]) < 1e-7
        if total < window:
            continue
        step = 0.05
        s = np.arange(0, total, step) if closed else np.arange(0, total + step * 0.25, step)
        xy = np.column_stack((np.interp(s, arc, p[:, 0]), np.interp(s, arc, p[:, 1])))
        nwin = max(3, int(round(window / step)) | 1)
        kernel = np.ones(nwin, dtype=float) / nwin
        halfn = nwin // 2
        if closed:
            padded = np.vstack((xy[-halfn:], xy, xy[:halfn]))
            mean = np.column_stack([np.convolve(padded[:, k], kernel, mode="valid") for k in range(2)])
            center = xy
        else:
            mean = np.column_stack([np.convolve(xy[:, k], kernel, mode="valid") for k in range(2)])
            center = xy[halfn:len(xy) - halfn]
        max_amp = max(max_amp, float(np.linalg.norm(center - mean, axis=1).max(initial=0)))
        if closed:
            unique = p[:-1]
            v0 = unique - np.roll(unique, 1, axis=0)
            v1 = np.roll(unique, -1, axis=0) - unique
        else:
            v0, v1 = p[1:-1] - p[:-2], p[2:] - p[1:-1]
        n0, n1 = np.linalg.norm(v0, axis=1), np.linalg.norm(v1, axis=1)
        valid = (n0 > 1e-7) & (n1 > 1e-7)
        dot = np.sum(v0[valid] * v1[valid], axis=1) / (n0[valid] * n1[valid])
        if len(dot):
            max_angle = max(max_angle, float(np.degrees(np.arccos(np.clip(dot, -1, 1))).max()))
    return max_amp, max_angle


def read_inputs():
    with gzip.open(RELIEF_GZ, "rt", encoding="utf-8") as f:
        source = json.load(f)
    nx, ny, rs = int(source["nx"]), int(source["ny"]), int(source["rs"])
    gb = np.frombuffer(base64.b64decode(source.get("GB") or source["G"]), dtype="<f4").reshape(ny * rs + 1, nx * rs + 1)
    cells = np.empty((ny, nx), dtype=object)
    cell_rows = {}
    with CELLS.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            x, y = int(row["cx"]), int(row["cy"])
            cells[y, x] = row["untergrund"]
            cell_rows[y * nx + x] = row
    overlay_rows = {}
    with OVERLAY.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            overlay_rows[(int(row["cx"]), int(row["cy"]))] = row
    return nx, ny, rs, gb, cells, cell_rows, overlay_rows


def surface_layer(cells, cell_rows, overlay_rows):
    ny, nx = cells.shape
    types = np.full((ny, nx), "grund", dtype="U10")
    substrates = cells.astype("U24")
    # Set lower priority first; then apply the specified higher priorities.
    for y in range(ny):
        for x in range(nx):
            row = cell_rows[y * nx + x]
            ov = overlay_rows.get((x, y), {})
            under = row["untergrund"]
            if under in ("FELS", "KLIPPE_WAND", "KLIPPE_KANTE"):
                types[y, x] = "fels"
            if row["ufer"] == "1":
                types[y, x] = "ufer"
            if ov.get("weg_klasse"):
                types[y, x] = "weg"
            if ov.get("bruecke") == "1":
                types[y, x] = "bruecke"
            if row["wasser_eis"] == "1" or under == "WASSER_EIS":
                types[y, x] = "wasser"
    # Remove isolated 1-3 cell specks from the broad ground/rock classes before
    # smoothing; they are raster noise and cannot form a camera-visible terrain zone.
    from scipy.ndimage import label as cc_label
    slivers = 0
    priority = {name: i for i, name in enumerate(SURFACE_PRIORITY)}
    for source_type in ("fels", "grund"):
        labels_cc, count = cc_label(types == source_type, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.uint8))
        for component in range(1, count + 1):
            yy, xx = np.where(labels_cc == component)
            if len(xx) > 3:
                continue
            neighbors = Counter()
            for y, x in zip(yy, xx):
                for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    y2, x2 = y + dy, x + dx
                    if 0 <= y2 < ny and 0 <= x2 < nx and types[y2, x2] != source_type:
                        neighbors[str(types[y2, x2])] += 1
            if neighbors:
                replacement = min(neighbors, key=lambda v: (-neighbors[v], priority.get(v, 999), v))
                types[yy, xx] = replacement
                slivers += len(xx)
    labels = sorted(set(types.ravel().tolist()))
    lut = {v: i for i, v in enumerate(labels)}
    codes = np.fromiter((lut[v] for v in types.ravel().tolist()), dtype=np.int16).reshape(ny, nx)
    return types, substrates, codes, labels, slivers


def feature_from_polygon(poly, props):
    if not poly.is_valid:
        poly = make_valid(poly)
    return feature(poly, props)


def build_zone_features(cells, cell_rows, overlay_rows, nx, ny):
    types, substrates, codes, labels, slivers = surface_layer(cells, cell_rows, overlay_rows)
    original = component_cell_geometries(codes, labels)
    comps = []
    for label, geom in original.items():
        comps.extend(polygon_parts(geom))
    smoothed = smooth_coverage(comps, dp=0.28, sample_step=0.20)
    tree = STRtree(list(original.values()))
    orig_vals = list(original.values())
    out = []
    type_area = Counter()
    for poly in sorted(smoothed, key=lambda p: (round(p.bounds[1], 5), round(p.bounds[0], 5), round(p.area, 5))):
        candidates = tree.query(poly)
        best, best_area = None, -1.0
        for idx in candidates:
            idx = int(idx)
            area = poly.intersection(orig_vals[idx]).area
            if area > best_area:
                best, best_area = idx, area
        if best is None:
            rp = poly.representative_point(); x = max(0, min(nx - 1, int(rp.x))); y = max(0, min(ny - 1, int(rp.y)))
            typ = str(types[y, x])
        else:
            # STRtree is over dict insertion order; labels use identical key order.
            typ = list(original.keys())[best]
        x0, y0, x1, y1 = poly.bounds
        ix0, iy0 = max(0, int(math.floor(x0))), max(0, int(math.floor(y0)))
        ix1, iy1 = min(nx, int(math.ceil(x1))), min(ny, int(math.ceil(y1)))
        xs, ys = np.arange(ix0, ix1) + 0.5, np.arange(iy0, iy1) + 0.5
        if len(xs) and len(ys):
            xx, yy = np.meshgrid(xs, ys)
            inside = contains_xy(poly, xx, yy)
            counts = Counter(substrates[iy0:iy1, ix0:ix1][inside].tolist())
        else:
            counts = Counter()
        if not counts:
            rp = poly.representative_point(); x = max(0, min(nx - 1, int(rp.x))); y = max(0, min(ny - 1, int(rp.y)))
            counts[str(substrates[y, x])] = 1
        under = sorted(counts.items(), key=lambda v: (-v[1], v[0]))[0][0]
        type_area[typ] += poly.area
        out.append(feature_from_polygon(poly, {"layer": "flaechentyp", "typ": typ, "untergrund": under,
                                               "untergrund_anteile": [{"name": k, "zellen": int(v)} for k, v in sorted(counts.items())],
                                               "quelle": "zellen_relief.csv + raster_c20_z25_overlay_plaetze_wege.csv"}))

    # Bauzone is an independent layer and is smoothed as a two-class coverage.
    bz = np.zeros((ny, nx), dtype=np.int8)
    for idx, row in cell_rows.items():
        bz[idx // nx, idx % nx] = int(row["bauzone_plan"] or 0)
    bz_labels = [("ausserhalb",), ("bauzone",)]
    bz_codes = bz.copy()
    bz_original = component_cell_geometries(bz_codes, bz_labels)
    bz_parts = [p for g in bz_original.values() for p in polygon_parts(g)]
    bz_smooth = smooth_coverage(bz_parts, dp=0.2, sample_step=0.2)
    target_area = float(np.count_nonzero(bz))
    inside_source = bz_original.get(("bauzone",), Polygon())
    outside_source = bz_original.get(("ausserhalb",), Polygon())
    inside_parts = []
    for poly in bz_smooth:
        if poly.intersection(inside_source).area >= poly.intersection(outside_source).area:
            inside_parts.append(poly)
    inside_union = unary_union(inside_parts) if inside_parts else Polygon()
    # Replace the smoothed area by a signed buffer calibrated to the exact cell count.
    if not inside_union.is_empty and target_area > 0:
        lo, hi = -4.0, 4.0
        for _ in range(30):
            mid = (lo + hi) / 2
            if inside_union.buffer(mid, join_style="round").area > target_area:
                hi = mid
            else:
                lo = mid
        calibrated = inside_union.buffer((lo + hi) / 2, join_style="round")
    else:
        calibrated = inside_union
    bz_area = float(calibrated.area)
    for poly in polygon_parts(calibrated):
        out.append(feature_from_polygon(poly, {"layer": "bauzone_plan", "typ": "bauzone", "quelle": "zellen_relief.csv"}))

    # Build overlay slot polygons from connected source-cell runs, retaining ids.
    slot_arrays = {"slot_bau": np.zeros((ny, nx), bool), "slot_deko": np.zeros((ny, nx), bool)}
    for (x, y), row in overlay_rows.items():
        if 0 <= x < nx and 0 <= y < ny:
            slot_arrays["slot_bau"][y, x] = row.get("bauplatz") == "1"
            slot_arrays["slot_deko"][y, x] = row.get("dekoplaetze_netz") == "1"
    from scipy.ndimage import label as cc_label
    for typ, mask in slot_arrays.items():
        cc, count = cc_label(mask, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.uint8))
        for i in range(1, count + 1):
            pts = np.argwhere(cc == i)
            if len(pts) == 0:
                continue
            mask_i = cc == i
            # Exact union of source cells; slots are a separate point/polygon layer.
            geom = unary_union([box(float(x), float(y), float(x + 1), float(y + 1)) for y, x in pts])
            if not geom.is_valid:
                geom = make_valid(geom)
            out.append(feature(geom, {"layer": "slot", "typ": typ, "id": f"{typ}_{i:04d}",
                                      "quelle": "raster_c20_z25_overlay_plaetze_wege.csv"}))
    expansion = json.loads(EXTENSION.read_text(encoding="utf-8"))
    for item in expansion.get("plaetze", []):
        x, y = float(item["cx"]) + 0.5, float(item["cy"]) + 0.5
        out.append(feature(Point(x, y), {"layer": "slot", "typ": "slot_bau", "id": f"{item['stand']}_{item['id']}",
                                         "quelle": "overlay_plaetze_erweiterung.json", "stand": item["stand"],
                                         "gebiet": item.get("gebiet", "")}))
    type_counts = Counter(types.ravel().tolist())
    return out, {"type_area": dict(sorted(type_area.items())), "type_cells": dict(sorted(type_counts.items())),
                 "bauzone_cells": int(target_area), "bauzone_area": float(bz_area),
                 "bauzone_delta_pct": (bz_area / target_area - 1) * 100 if target_area else 0,
                 "zone_feature_count": len([f for f in out if f["properties"].get("layer") == "flaechentyp"]),
                 "bauzone_feature_count": len([f for f in out if f["properties"].get("typ") == "bauzone"]),
                 "slot_feature_count": len([f for f in out if f["properties"].get("layer") == "slot"]),
                 "surface_features": len([f for f in out if f["properties"].get("layer") == "flaechentyp"]),
                 "sliver_cells_reassigned": int(slivers)}


def line_feature(line: LineString, props: dict, get_height) -> dict:
    # Fixed-distance emission is done after all smoothing, since filtering changes
    # the original Catmull-Rom parameter spacing.
    if "anker_pflicht" in props:
        anchor = np.asarray(props["anker_pflicht"], dtype=float)
        projected_s = line.project(Point(anchor))
        projected = np.asarray(line.interpolate(projected_s).coords[0])
        delta = anchor - projected
        line = LineString(np.asarray(line.coords) + delta)
        closed = False
        anchor_s = projected_s
    else:
        anchor = None
        closed = np.linalg.norm(np.asarray(line.coords[0]) - np.asarray(line.coords[-1])) < 1e-7
        anchor_s = None
    step = 0.10
    distances = np.arange(0.0, line.length, step)
    extra = [line.length]
    if anchor_s is not None:
        extra.append(anchor_s)
    distances = np.unique(np.r_[distances, extra])
    coords = np.array([line.interpolate(float(s)).coords[0] for s in distances])
    if anchor is not None:
        coords[int(np.argmin(np.abs(distances - anchor_s)))] = anchor
    elif closed and len(coords) > 1:
        coords[-1] = coords[0]
    coords = round_xy(coords)
    h = get_height(coords)
    p = dict(props)
    p["hoehen_m"] = [float(x) for x in h]
    p["abtastung_max_m"] = round(float(np.linalg.norm(np.diff(coords, axis=0), axis=1).max(initial=0)), 4)
    return feature(LineString(coords), p)


def build_edges(cell_rows, nx, ny, rs, gb, get_height):
    features, q3_lines = [], []
    omitted_short = 0
    # WAND is the exported wall face; KANTE marks the source edge cells. The source snapshot
    # has no WAND_OBEN/WAND_FUSS values, so upper/lower are derived from each named mask's GB range.
    names = sorted({r["wand_name"] for r in cell_rows.values() if r["wand_name"]})
    for name in names:
        mask = np.zeros((ny, nx), dtype=bool)
        for idx, row in cell_rows.items():
            if row["wand_name"] == name and row["klippe"] in ("WAND", "KANTE") and row["untergrund"] in ("KLIPPE_WAND", "KLIPPE_KANTE"):
                mask[idx // nx, idx % nx] = True
        if not mask.any():
            continue
        ys, xs = np.where(mask)
        vals = get_height(np.column_stack((xs + 0.5, ys + 0.5)))
        mid = float(np.median(vals))
        for raw in contour_cell_mask(mask):
            # Split an enclosing contour around its high and low half at the median GB level.
            p = np.asarray(raw.coords)
            hp = get_height(p)
            typ = "klippe_oben" if float(np.median(hp)) >= mid else "klippe_unten"
            smooth = smooth_line(raw, dp=0.1, step=0.20, chaikin_n=1)
            if smooth is None:
                continue
            if smooth.length < 3.0:
                omitted_short += 1
                continue
            feat = line_feature(smooth, {"typ": typ, "wand_name": name,
                                         "quelle": "zellen_relief.csv: KLIPPE_WAND/KANTE + GB"}, get_height)
            features.append(feat); q3_lines.append(smooth)

    # GB slope mask, sampled from the viewer field at 0.5 m. Smooth only the derived angle.
    h = ndi.gaussian_filter(gb.astype(float), sigma=0.7, mode="nearest")
    dz, dx = np.gradient(h, 1 / rs, 1 / rs)
    slope = np.degrees(np.arctan(np.hypot(dx, dz)))
    slope = ndi.gaussian_filter(slope, sigma=0.55, mode="nearest")
    for raw in contour_node_field(slope, 55.0, rs):
        smooth = smooth_line(raw, dp=0.1, step=0.20, chaikin_n=1, lowpass_m=2.0)
        if smooth is None:
            continue
        if smooth.length < 3.0:
            omitted_short += 1
            continue
        features.append(line_feature(smooth, {"typ": "steil55", "quelle": "GB Neigung > 55 Grad"}, get_height))
        q3_lines.append(smooth)
    return features, q3_lines, omitted_short


def build_grats(cell_rows, nx, ny, rs, gb, get_height):
    paths = hessian_ridges(gb, rs)
    # Prefer ridge skeleton paths in the named window; fall back to the GB contour of
    # KLIPPE_WAND when the Hessian has no stable path in a required anchor window.
    all_named_masks = {}
    for name in sorted({r["wand_name"] for r in cell_rows.values() if r["wand_name"]}):
        m = np.zeros((ny, nx), dtype=bool)
        for idx, row in cell_rows.items():
            if row["wand_name"] == name and row["untergrund"] == "KLIPPE_WAND":
                m[idx // nx, idx % nx] = True
        all_named_masks[name] = m
    candidates = []
    for path in paths:
        if len(path) < 3:
            continue
        line = LineString(path)
        if line.length >= 3.0:
            candidates.append(line)
    output = []
    used = set()

    def nearest_path(point, bounds=None, name=None):
        ranked = []
        for i, line in enumerate(candidates):
            rp = line.interpolate(line.project(point))
            x, z = rp.x, rp.y
            if bounds and not (bounds[0] <= x <= bounds[2] and bounds[1] <= z <= bounds[3]):
                continue
            ranked.append((line.distance(point), i, line))
        if ranked:
            return min(ranked, key=lambda v: (v[0], -v[2].length))[2]
        if name in all_named_masks:
            raw = contour_cell_mask(all_named_masks[name])
            ls = [l for l in raw if l.length > 3]
            if ls:
                return min(ls, key=lambda l: (l.distance(point), -l.length))
        return None

    # Required Fabian points become exact controls. They are connected to the nearest
    # GB Hessian skeleton or named cliff crown; this records the source discrepancy honestly.
    for x, z, name in TARGETS:
        target = Point(x, z)
        bounds = (x - 20, z - 20, x + 20, z + 20)
        base = nearest_path(target, bounds, "Ostgrat" if name == "G3H3" else "Krater")
        source_distance = float(base.distance(target)) if base is not None else None
        # The plan's exact anchors lie inside the source wall mask rather than on
        # a detected Hessian skeleton; trace the local Hessian principal direction
        # through each [F] control and retain the measured source offset as metadata.
        raw = hessian_tangent_trace(gb, rs, (x, z), span=12.0)
        line = smooth_line(raw, dp=0.12, step=0.15, chaikin_n=1)
        if line is None:
            continue
        output.append(line_feature(line, {"name": name, "typ": "grat", "anker_pflicht": [x, z],
                                           "anker_basisabstand_m": round(source_distance, 3) if source_distance is not None else None,
                                           "quelle": "GB Hessian-Ridge-Tangente; Pflichtanker [F]"}, get_height))
        used.add(name)

    # Named Hessian paths for Ostgrat and Kraterring G1, with no cell-grid resampling.
    windows = {"Ostgrat": (270, 75, 336, 205), "Kraterring_G1": (252, 0, 294, 43)}
    for name, (x0, z0, x1, z1) in windows.items():
        named = []
        for line in candidates:
            if line.intersection(box(x0, z0, x1, z1)).length >= 2.0:
                named.append(line)
        named.sort(key=lambda l: (-l.length, tuple(round(v, 4) for v in l.coords[0])))
        if not named and name == "Ostgrat":
            named = [l for l in contour_cell_mask(all_named_masks.get("Ostgrat", np.zeros((ny, nx), bool))) if l.length > 4]
        # Cap general skeleton noise; retain every meaningful long ridge trace in each window.
        for idx, base in enumerate(named[:20]):
            smooth = smooth_line(base, dp=0.25, step=0.20, chaikin_n=1, lowpass_m=5.0)
            if smooth is None:
                continue
            output.append(line_feature(smooth, {"name": name, "typ": "grat",
                                                 "quelle": "GB Hessian-Ridge -> Skelett -> Polylinie"}, get_height))
    lines = [LineString(f["geometry"]["coordinates"]) for f in output]
    return output, lines, {"hessian_skeleton_paths": len(paths), "hessian_lines_candidate": len(candidates),
                           "grat_features": len(output)}


def build(out_dir: Path):
    SMOOTH_COVERAGE_STATUS.clear()
    nx, ny, rs, gb, cells, cell_rows, overlay_rows = read_inputs()
    get_height = height_sampler(gb, rs)
    edge_features, edge_lines, edge_omitted_short = build_edges(cell_rows, nx, ny, rs, gb, get_height)
    grat_features, grat_lines, grat_metrics = build_grats(cell_rows, nx, ny, rs, gb, get_height)
    zone_features, zone_metrics = build_zone_features(cells, cell_rows, overlay_rows, nx, ny)
    zone_lines = []
    for f in zone_features:
        if f["properties"].get("layer") != "flaechentyp":
            continue
        geom = shape(f["geometry"])
        for poly in polygon_parts(geom):
            zone_lines.append(LineString(poly.exterior.coords))
            zone_lines.extend(LineString(r.coords) for r in poly.interiors)
    # Measure exactly the geometries emitted to GeoJSON, including fixed-step resampling.
    edge_lines = [LineString(f["geometry"]["coordinates"]) for f in edge_features]
    grat_lines = [LineString(f["geometry"]["coordinates"]) for f in grat_features]
    compact_json(out_dir / "kanten.geojson", geojson(edge_features))
    compact_json(out_dir / "grat.geojson", geojson(grat_features))
    compact_json(out_dir / "zonen.geojson", geojson(zone_features))
    metrics = {"dimensions": [nx, ny], "rs": rs, "kanten_count": len(edge_features),
               "kanten_omitted_short_lt3m": edge_omitted_short,
               "kanten_by_typ": dict(sorted(Counter(f["properties"]["typ"] for f in edge_features).items())),
               "kanten_q3": zacken_and_kinks(edge_lines), "grat_q3": zacken_and_kinks(grat_lines),
               "zonen_q3": zacken_and_kinks(zone_lines),
               "grat": grat_metrics, "zonen": zone_metrics,
               "coverage_smoothing": list(SMOOTH_COVERAGE_STATUS)}
    return metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=RELIEF / "detail_v2" / "vektor")
    args = parser.parse_args()
    print(json.dumps(build(args.out), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
