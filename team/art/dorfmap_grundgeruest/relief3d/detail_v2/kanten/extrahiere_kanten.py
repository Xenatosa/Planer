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
from skimage.graph import route_through_array
from skimage.measure import find_contours
from skimage.morphology import skeletonize

import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
import zonen_konstruktiv as zk  # noqa: E402


HERE = Path(__file__).resolve().parent
RELIEF = HERE.parents[1]
ROOT = RELIEF.parents[0]
CELLS = RELIEF / "neu" / "zellen_relief.csv"
OVERLAY = ROOT / "raster_c20_z25_overlay_plaetze_wege.csv"
EXTENSION = ROOT / "overlay_plaetze_erweiterung.json"
RELIEF_GZ = RELIEF / "relief_daten.json.gz"
TARGETS = ((300.0, 90.0, "G3H3"), (290.0, 98.0, "G3H3"), (84.0, 129.0, "B3C3"))
SURFACE_PRIORITY = ("wasser", "bruecke", "weg", "ufer", "fels", "grund")
CLASS_CODES = {"grund": 0, "weg": 1, "ufer": 2, "fels": 3, "wasser": 4, "bruecke": 5}
SMOOTH_COVERAGE_STATUS = []
VEKTOR_QUELLE = RELIEF / "detail_v2" / "vektor"
QUELLE_FLAECHENTYP = {
    "wasser": "wasser.geojson (P1b2 #58)",
    "bruecke": "Platzhalter P5: Komponenten Wegnetz x Uferband (ohne Wasser), die E2 x186-197 z73-75 bzw. E3-West x174-186 z126-128 schneiden",
    "weg": "wege.geojson rolle=netz (P1a2 #59), Schliessen r=1,6 m",
    "ufer": "ufer.geojson typ=uferband vereinigt mit Wasser, Schliessen r=1,6 m, minus Wasser",
    "fels": "zellen_relief.csv FELS/KLIPPE_*: SDF 0,1 m, Gauss sigma 1 m, Kontur 0, Oeffnen/Schliessen r=2 m, Ringglaettung adaptiv",
    "grund": "Rest des Rechtecks 0..336 x 0..303",
}


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
                chaikin_n: int = 0, lowpass_m: float = 1.2) -> LineString | None:
    """DP-simplify, sample every 5 cm, Gaussian-smooth and re-sample evenly.

    Open endpoints remain fixed. Closed rings use cyclic filtering. Shared
    coverage boundaries are passed as whole arcs between graph junctions, so
    the fixed endpoints are common to all adjacent faces.
    """
    if line.length < 0.75:
        return None
    simplified = line.simplify(dp, preserve_topology=True)
    if simplified.geom_type != "LineString" or len(simplified.coords) < 3:
        simplified = line
    path = LineString(simplified.coords)
    p0 = np.asarray(path.coords[0], dtype=float)
    p1 = np.asarray(path.coords[-1], dtype=float)
    closed = np.linalg.norm(p0 - p1) < 1e-7
    length = path.length
    if closed:
        p = np.asarray(path.coords[:-1], dtype=float)
        n = max(8, int(math.ceil(length / 0.05)))
        s = np.arange(n, dtype=float) * (length / n)
        p = np.asarray([path.interpolate(float(v)).coords[0] for v in s])
        p = ndi.gaussian_filter1d(p, sigma=max(lowpass_m / 0.05, 1.0), axis=0, mode="wrap")
        filtered = LineString(np.vstack((p, p[:1])))
        nout = max(8, int(math.ceil(filtered.length / min(step, 0.25))))
        so = np.arange(nout, dtype=float) * (filtered.length / nout)
        out = np.asarray([filtered.interpolate(float(v)).coords[0] for v in so])
        out = np.vstack((out, out[:1]))
    else:
        n = max(2, int(math.ceil(length / 0.05)))
        s = np.linspace(0.0, length, n + 1)
        p = np.asarray([path.interpolate(float(v)).coords[0] for v in s])
        p = ndi.gaussian_filter1d(p, sigma=max(lowpass_m / 0.05, 1.0), axis=0, mode="nearest")
        p[0], p[-1] = p0, p1
        filtered = LineString(p)
        nout = max(1, int(math.ceil(filtered.length / min(step, 0.25))))
        so = np.linspace(0.0, filtered.length, nout + 1)
        out = np.asarray([filtered.interpolate(float(v)).coords[0] for v in so])
    p = round_xy(out)
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
    raw_counts = Counter(types.ravel().tolist())
    # Reassign isolated 1-3 cell specks before smoothing. The surface classes
    # are area-calibrated back to their unmodified source counts below, so this
    # removes sub-cell islands without making small classes disappear globally.
    from scipy.ndimage import label as cc_label
    slivers = 0
    priority = {name: i for i, name in enumerate(SURFACE_PRIORITY)}
    for source_type in sorted(raw_counts):
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
    return types, substrates, codes, labels, slivers, raw_counts


def feature_from_polygon(poly, props):
    if not poly.is_valid:
        poly = make_valid(poly)
    return feature(poly, props)


def majority_at_geometry(geom, types, substrates):
    ny, nx = types.shape
    x0, y0, x1, y1 = geom.bounds
    ix0, iy0 = max(0, int(math.floor(x0))), max(0, int(math.floor(y0)))
    ix1, iy1 = min(nx, int(math.ceil(x1))), min(ny, int(math.ceil(y1)))
    if ix1 > ix0 and iy1 > iy0:
        xs, ys = np.arange(ix0, ix1) + 0.5, np.arange(iy0, iy1) + 0.5
        xx, yy = np.meshgrid(xs, ys)
        inside = contains_xy(geom, xx, yy)
        if inside.any():
            t = Counter(types[iy0:iy1, ix0:ix1][inside].tolist())
            u = Counter(substrates[iy0:iy1, ix0:ix1][inside].tolist())
            typ = min(t, key=lambda v: (-t[v], v))
            under = min(u, key=lambda v: (-u[v], v))
            return typ, under
    rp = geom.representative_point()
    x, y = min(nx - 1, max(0, int(rp.x))), min(ny - 1, max(0, int(rp.y)))
    return str(types[y, x]), str(substrates[y, x])


def classify_coverage(polys, originals):
    labels = sorted(originals, key=str)
    geoms = [originals[k] for k in labels]
    tree = STRtree(geoms)
    result = defaultdict(list)
    for poly in polys:
        candidates = tree.query(poly)
        best, area = None, -1.0
        for idx in candidates:
            idx = int(idx)
            overlap = poly.intersection(geoms[idx]).area
            if overlap > area + 1e-9 or (abs(overlap - area) <= 1e-9 and (best is None or str(labels[idx]) < str(labels[best]))):
                best, area = idx, overlap
        if best is not None:
            result[labels[best]].append(poly)
    return {k: unary_union(v) for k, v in result.items()}


def build_zone_features(cells, cell_rows, overlay_rows, nx, ny):
    types, substrates, codes, labels, slivers, raw_type_counts = surface_layer(cells, cell_rows, overlay_rows)
    # Nacharbeit 19.11. (Methodenwechsel, t2027u): keine Zellpolygonisierung mehr.
    # Flaechentyp konstruktiv aus den gemergten glatten Vektoren + SDF-Fels,
    # Untergrund per Multi-Label-Glaettung mit partitionserhaltender Bogenglaettung.
    surf, _raw = zk.flaechentyp_partition(VEKTOR_QUELLE, substrates)
    surf = zk.knoten_neu(surf)
    surf = zk.boegen_bereinigen(surf)
    out = []
    type_area = Counter()
    surface_polys = []
    for typ in SURFACE_PRIORITY:
        surface_polys.extend((typ, p) for p in zk.polys(surf.get(typ)))
    for typ, poly in sorted(surface_polys, key=lambda v: (SURFACE_PRIORITY.index(v[0]), round(v[1].bounds[1], 5), round(v[1].bounds[0], 5), round(v[1].area, 5))):
        x0, y0, x1, y1 = poly.bounds
        ix0, iy0 = max(0, int(math.floor(x0))), max(0, int(math.floor(y0)))
        ix1, iy1 = min(nx, int(math.ceil(x1))), min(ny, int(math.ceil(y1)))
        xs, ys = np.arange(ix0, ix1) + 0.5, np.arange(iy0, iy1) + 0.5
        counts = Counter()
        if len(xs) and len(ys):
            xx, yy = np.meshgrid(xs, ys)
            inside = contains_xy(poly, xx, yy)
            counts = Counter(substrates[iy0:iy1, ix0:ix1][inside].tolist())
        if not counts:
            rp = poly.representative_point(); x = max(0, min(nx - 1, int(rp.x))); y = max(0, min(ny - 1, int(rp.y)))
            counts[str(substrates[y, x])] = 1
        under = sorted(counts.items(), key=lambda v: (-v[1], v[0]))[0][0]
        type_area[typ] += poly.area
        out.append(feature_from_polygon(poly, {"layer": "flaechentyp", "typ": typ, "klasse": CLASS_CODES[typ], "untergrund": under,
                                               "quelle": QUELLE_FLAECHENTYP[typ]}))
    under_regions, _assigned, under_info = zk.untergrund_partition_v2(substrates)
    under_by_label = under_regions
    under_labels = sorted(under_regions)
    for under in under_labels:
        for poly in sorted(zk.polys(under_regions[under]), key=lambda p: (round(p.bounds[1], 5), round(p.bounds[0], 5), round(p.area, 5))):
            typ, _ = majority_at_geometry(poly, types, substrates)
            out.append(feature_from_polygon(poly, {"layer": "untergrund", "typ": under,
                                                   "klasse": CLASS_CODES[typ], "untergrund": under,
                                                   "quelle": "zellen_relief.csv: untergrund (Wasser/Fels -> naechster Untergrund), "
                                                             "Indikator 0,1 m Gauss sigma %.2f m, argmax, Inseln < %.0f m2 -> Nachbar, "
                                                             "Bogenglaettung adaptiv" % (zk.UNTER_SIGMA_M, zk.UNTER_INSEL_M2)}))

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
        typ, under = majority_at_geometry(poly, types, substrates)
        out.append(feature_from_polygon(poly, {"layer": "bauzone_plan", "typ": "bauzone", "klasse": CLASS_CODES[typ],
                                               "untergrund": under, "quelle": "zellen_relief.csv"}))

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
            main_type, under = majority_at_geometry(geom, types, substrates)
            out.append(feature(geom, {"layer": "slot", "typ": typ, "klasse": CLASS_CODES[main_type], "untergrund": under,
                                      "id": f"{typ}_{i:04d}", "quelle": "raster_c20_z25_overlay_plaetze_wege.csv"}))
    expansion = json.loads(EXTENSION.read_text(encoding="utf-8"))
    for item in expansion.get("plaetze", []):
        x, y = float(item["cx"]) + 0.5, float(item["cy"]) + 0.5
        px, py = int(item["cx"]), int(item["cy"])
        px, py = min(nx - 1, max(0, px)), min(ny - 1, max(0, py))
        main_type, under = str(types[py, px]), str(substrates[py, px])
        out.append(feature(Point(x, y), {"layer": "slot", "typ": "slot_bau", "klasse": CLASS_CODES[main_type], "untergrund": under,
                                         "id": f"{item['stand']}_{item['id']}",
                                         "quelle": "overlay_plaetze_erweiterung.json", "stand": item["stand"],
                                         "gebiet": item.get("gebiet", "")}))
    seen_ids = set()
    for i, f in enumerate(out):
        props = f["properties"]
        if "klasse" not in props or "untergrund" not in props:
            typ, under = majority_at_geometry(shape(f["geometry"]), types, substrates)
            props.setdefault("klasse", CLASS_CODES[typ]); props.setdefault("untergrund", under)
        ident = str(props.get("id") or f"{props.get('layer', 'feature')}_{i:05d}")
        candidate = ident
        suffix = 1
        while candidate in seen_ids:
            suffix += 1
            candidate = f"{ident}_{suffix}"
        props["id"] = candidate
        seen_ids.add(candidate)
    type_counts = raw_type_counts
    return out, {"type_area": dict(sorted(type_area.items())), "type_cells": dict(sorted(type_counts.items())),
                 "substrate_area": {k: float(v.area) for k, v in under_by_label.items()},
                 "bauzone_cells": int(target_area), "bauzone_area": float(bz_area),
                 "bauzone_delta_pct": (bz_area / target_area - 1) * 100 if target_area else 0,
                 "zone_feature_count": len([f for f in out if f["properties"].get("layer") == "flaechentyp"]),
                 "bauzone_feature_count": len([f for f in out if f["properties"].get("typ") == "bauzone"]),
                 "slot_feature_count": len([f for f in out if f["properties"].get("layer") == "slot"]),
                 "surface_features": len([f for f in out if f["properties"].get("layer") == "flaechentyp"]),
                 "untergrund_info": under_info,
                 "untergrund_inseln_entfallen": list(zk.BOGEN_INSELN_ENTFALLEN),
                 "bruecken_schnitt": list(zk.BRUECKEN_SCHNITT),
                 "fels_ringe_entfallen": list(zk.RING_DROPPED)}


def line_feature(line: LineString, props: dict, get_height) -> dict:
    # Fixed-distance emission is done after all smoothing, since filtering changes
    # the original Catmull-Rom parameter spacing.
    closed = np.linalg.norm(np.asarray(line.coords[0]) - np.asarray(line.coords[-1])) < 1e-7
    step = 0.10
    distances = np.linspace(0.0, line.length, max(1, int(math.ceil(line.length / step))) + 1)
    coords = np.array([line.interpolate(float(s)).coords[0] for s in distances])
    if closed and len(coords) > 1:
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
        source_mask = np.zeros((ny, nx), dtype=bool)
        for idx, row in cell_rows.items():
            if row["wand_name"] == name and row["klippe"] in ("WAND", "KANTE") and row["untergrund"] in ("KLIPPE_WAND", "KLIPPE_KANTE"):
                source_mask[idx // nx, idx % nx] = True
        if not source_mask.any():
            continue
        ys, xs = np.where(source_mask)
        vals = get_height(np.column_stack((xs + 0.5, ys + 0.5)))
        mid = float(np.median(vals))
        # Nacharbeit: dieselbe SDF-Glaettung wie die Felsflaeche statt 7-m-Opening
        # (Kontur 0 des Gauss-geglaetteten SDF, Oeffnen/Schliessen r=2 m,
        # adaptive Ringglaettung); Komponenten < 4 m2 und Linien < 3 m entfallen.
        region = zk.sdf_smooth_region(source_mask, zk.FELS_SIGMA_M, zk.MIN_AREA, clip=False)
        region = zk.schliessen(zk.oeffnen(region, zk.FELS_OEFFNEN_M), zk.FELS_SCHLIESSEN_M)
        region = zk.ringe_glaetten(region, zk.FELS_RING_SIGMA_M)
        rings = []
        for poly in zk.polys(region):
            if poly.area < zk.MIN_AREA:
                omitted_short += 1
                continue
            rings.append(LineString(poly.exterior.coords))
            rings.extend(LineString(r.coords) for r in poly.interiors)
        if not rings:
            omitted_short += 1
            continue
        for ring in rings:
            for raw in linestring_parts(line_merge(ring.intersection(box(0, 0, nx, ny)))):
                if raw.length < 3.0:
                    omitted_short += 1
                    continue
                p = np.asarray(raw.coords)
                hp = get_height(p)
                typ = "klippe_oben" if float(np.median(hp)) >= mid else "klippe_unten"
                feat = line_feature(raw, {"typ": typ, "wand_name": name,
                                          "quelle": "zellen_relief.csv: KLIPPE_WAND/KANTE + GB; SDF sigma 1 m, r=2 m, Ringglaettung"}, get_height)
                features.append(feat); q3_lines.append(LineString(feat["geometry"]["coordinates"]))

    # GB slope mask, sampled from the viewer field at 0.5 m. A fixed 2.5 m
    # binary opening/closing removes sub-cell notches and loops before the
    # contour is traced; the resulting contour is then Gaussian-smoothed.
    h = ndi.gaussian_filter(gb.astype(float), sigma=0.7, mode="nearest")
    dz, dx = np.gradient(h, 1 / rs, 1 / rs)
    slope = np.degrees(np.arctan(np.hypot(dx, dz)))
    slope = ndi.gaussian_filter(slope, sigma=0.55, mode="nearest")
    radius = int(round(2.5 * rs))
    yy, xx = np.ogrid[-radius:radius + 1, -radius:radius + 1]
    disk = xx * xx + yy * yy <= radius * radius
    steep_mask = ndi.binary_closing(ndi.binary_opening(slope > 55.0, structure=disk), structure=disk)
    for raw in contour_node_mask(steep_mask, rs):
        smooth = smooth_line(raw, dp=0.1, step=0.20, chaikin_n=1, lowpass_m=1.5)
        if smooth is None:
            continue
        candidates = []
        if smooth.is_ring:
            rounded = Polygon(smooth.coords).buffer(-2.5, quad_segs=12).buffer(2.5, quad_segs=12)
            for poly in polygon_parts(rounded):
                candidates.append(LineString(poly.exterior.coords))
                candidates.extend(LineString(r.coords) for r in poly.interiors)
        else:
            candidates.append(smooth)
        for line in candidates:
            if line.length < 3.0:
                omitted_short += 1
                continue
            features.append(line_feature(line, {"typ": "steil55", "quelle": "GB Neigung > 55 Grad; Masken-Oeffnung 2.5 m"}, get_height))
            q3_lines.append(line)
    return features, q3_lines, omitted_short


def build_grats(cell_rows, nx, ny, rs, gb, get_height):
    paths = hessian_ridges(gb, rs)
    candidates = []
    for path in paths:
        if len(path) < 3:
            continue
        line = LineString(path)
        # Closed skeleton loops in this field are detector artifacts, not
        # through-going crown lines. Drop them with all sub-3 m fragments.
        if line.length >= 3.0 and not line.is_ring:
            candidates.append(line)
    output = []
    # A short skeleton segment can be a bridge between two longer branches.
    # Do not emit it on its own, but retain it while tracing a single connected
    # G3/H3 route through the graph.
    route_paths = [LineString(p) for p in paths if len(p) >= 3 and not LineString(p).is_ring]
    mask = np.zeros_like(gb, dtype=bool)
    for line in route_paths:
        q = np.rint(np.asarray(line.coords) * rs).astype(int)
        good = (q[:, 0] >= 0) & (q[:, 0] < mask.shape[1]) & (q[:, 1] >= 0) & (q[:, 1] < mask.shape[0])
        mask[q[good, 1], q[good, 0]] = True
    components, _ = ndi.label(mask, structure=np.ones((3, 3), dtype=np.uint8))
    yy, xx = np.where(mask)
    points = np.asarray([(x / rs, y / rs) for y, x in zip(yy, xx)])

    def snap(point):
        d2 = np.sum((points - np.asarray(point)) ** 2, axis=1)
        k = int(np.argmin(d2))
        return int(yy[k]), int(xx[k]), float(math.sqrt(d2[k]))

    # G3/H3 is one graph route between the two nearest valid Hessian skeleton
    # nodes. The Fabian coordinates are measurements only; the line is never
    # translated or seeded at a non-ridge control point.
    g3_targets = [t for t in TARGETS if t[2] == "G3H3"]
    if len(g3_targets) == 2:
        a, b = g3_targets
        ay, ax, ad = snap(a[:2]); by, bx, bd = snap(b[:2])
        if components[ay, ax] == components[by, bx] and components[ay, ax] > 0:
            cost = np.where(mask, 1.0, 1e8)
            route, _ = route_through_array(cost, (ay, ax), (by, bx), fully_connected=True, geometric=True)
            raw = LineString([(x / rs, y / rs) for y, x in route])
            line = smooth_line(raw, dp=0.05, step=0.20, lowpass_m=1.2)
            line = smooth_line(line, dp=0.05, step=0.10, lowpass_m=1.2) if line is not None else None
            if line is not None and line.length >= 3.0:
                distances = {f"{int(x)}|{int(z)}": round(float(line.distance(Point(x, z))), 4)
                             for x, z, _ in g3_targets}
                output.append(line_feature(line, {"name": "G3H3", "typ": "grat",
                                                   "anker_abstaende_m": distances,
                                                   "quelle": "GB Hessian-Ridge-Skelett, kuerzester Pfad im zusammenhaengenden Ridge-Netz"}, get_height))

    # B3/C3 uses the nearest remaining real Hessian path. Its actual offset is
    # stored and reported when the field has no crown within the 1 m target.
    bx, bz, _ = next(t for t in TARGETS if t[2] == "B3C3")
    bp = Point(bx, bz)
    bbase = min(candidates, key=lambda l: (l.distance(bp), -l.length)) if candidates else None
    if bbase is not None:
        line = smooth_line(bbase, dp=0.05, step=0.20, lowpass_m=1.2)
        line = smooth_line(line, dp=0.05, step=0.10, lowpass_m=1.2) if line is not None else None
        if line is not None and line.length >= 3.0:
            output.append(line_feature(line, {"name": "B3C3", "typ": "grat",
                                               "anker_abstaende_m": {"84|129": round(float(line.distance(bp)), 4)},
                                               "quelle": "GB Hessian-Ridge-Skelett; naechster tatsaechlicher Pfad"}, get_height))

    # Keep one longest through-going crown per named field window; discard the
    # short branch fragments and closed skeleton loops above.
    windows = {"Ostgrat": (270, 75, 336, 205), "Kraterring_G1": (252, 0, 294, 43)}
    for name, bounds in windows.items():
        clip = box(*bounds)
        named = [l for l in candidates if l.intersection(clip).length >= 2.0]
        if not named:
            continue
        base = min(named, key=lambda l: (-l.length, tuple(round(v, 4) for v in l.coords[0])))
        line = smooth_line(base, dp=0.05, step=0.20, lowpass_m=1.2)
        line = smooth_line(line, dp=0.05, step=0.10, lowpass_m=1.2) if line is not None else None
        if line is not None and line.length >= 3.0:
            output.append(line_feature(line, {"name": name, "typ": "grat",
                                               "quelle": "GB Hessian-Ridge -> Skelett -> durchgehende Polylinie"}, get_height))
    lines = [LineString(f["geometry"]["coordinates"]) for f in output]
    return output, lines, {"hessian_skeleton_paths": len(paths), "hessian_lines_candidate": len(candidates),
                           "closed_loops_dropped": sum(LineString(p).is_ring for p in paths if len(p) >= 3),
                           "grat_features": len(output)}


def build(out_dir: Path):
    SMOOTH_COVERAGE_STATUS.clear()
    for log in (zk.RING_LOG, zk.RING_DROPPED, zk.BOGEN_LOG, zk.BOGEN_INSELN_ENTFALLEN):
        log.clear()
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
