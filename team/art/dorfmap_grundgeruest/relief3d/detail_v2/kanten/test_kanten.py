from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import numpy as np
from shapely.geometry import LineString, Point, box, shape
from shapely import line_merge, unary_union
from shapely.strtree import STRtree

HERE = Path(__file__).resolve().parent
RELIEF = HERE.parents[1]
ROOT = RELIEF.parents[0]
VECTOR = RELIEF / "detail_v2" / "vektor"
GENERATOR = HERE / "extrahiere_kanten.py"
TARGETS = ((300.0, 90.0, "G3H3"), (290.0, 98.0, "G3H3"), (84.0, 129.0, "B3C3"))
NAMES = ("kanten.geojson", "grat.geojson", "zonen.geojson")
CLASS_CODES = {"grund": 0, "weg": 1, "ufer": 2, "fels": 3, "wasser": 4, "bruecke": 5}
MAP_CORNERS = {(0.0, 0.0), (336.0, 0.0), (336.0, 303.0), (0.0, 303.0)}

sys.path.insert(0, str(HERE))
import extrahiere_kanten as ek  # noqa: E402


def read(name):
    obj = json.loads((VECTOR / name).read_text(encoding="utf-8"))
    assert obj["type"] == "FeatureCollection"
    assert isinstance(obj["features"], list)
    return obj["features"]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def polygon_parts(geom):
    if geom.geom_type == "Polygon":
        return [geom]
    if geom.geom_type in ("MultiPolygon", "GeometryCollection"):
        return [p for g in geom.geoms for p in polygon_parts(g)]
    return []


def line_parts(geom):
    if geom.geom_type == "LineString":
        return [geom]
    if geom.geom_type in ("MultiLineString", "GeometryCollection"):
        return [line for g in geom.geoms for line in line_parts(g)]
    return []


def shared_boundary_arcs(features, layer):
    geoms = [shape(f["geometry"]) for f in features if f["properties"].get("layer") == layer]
    noded = unary_union([g.boundary for g in geoms])
    return [line for line in line_parts(line_merge(noded)) if line.length > 0.1]


def q3_metrics(lines, endpoint_guard=0.0):
    """Measure 1 m moving-average deviation and every interior turn.

    For coverage arcs, the 1 m window must lie inside one graph edge; the
    endpoint guard is exactly half the window. Arc endpoints are checked
    separately as source tripoints/map corners below.
    """
    max_amp = max_angle = 0.0
    for line in lines:
        p = np.asarray(line.coords, dtype=float)
        seg = np.linalg.norm(np.diff(p, axis=0), axis=1)
        arc = np.r_[0.0, np.cumsum(seg)]
        total = float(arc[-1])
        closed = np.linalg.norm(p[0] - p[-1]) < 1e-7
        if total >= 1.0:
            step = 0.05
            s = np.arange(0.0, total, step) if closed else np.linspace(0.0, total, max(2, int(np.ceil(total / step)) + 1))
            xy = np.column_stack((np.interp(s, arc, p[:, 0]), np.interp(s, arc, p[:, 1])))
            nwin = 21
            half = nwin // 2
            if closed:
                padded = np.vstack((xy[-half:], xy, xy[:half]))
                mean = np.column_stack([np.convolve(padded[:, k], np.ones(nwin) / nwin, mode="valid") for k in range(2)])
                center, center_s = xy, s
                valid = np.ones(len(s), dtype=bool)
            else:
                mean = np.column_stack([np.convolve(xy[:, k], np.ones(nwin) / nwin, mode="valid") for k in range(2)])
                center, center_s = xy[half:-half], s[half:-half]
                valid = (center_s >= endpoint_guard) & (center_s <= total - endpoint_guard)
            amp = np.linalg.norm(center - mean, axis=1)
            max_amp = max(max_amp, float(amp[valid].max(initial=0.0)))
        if closed:
            p = p[:-1]
        if len(p) >= 3:
            v0, v1 = p[1:-1] - p[:-2], p[2:] - p[1:-1]
            n0, n1 = np.linalg.norm(v0, axis=1), np.linalg.norm(v1, axis=1)
            valid = (n0 > 1e-8) & (n1 > 1e-8)
            dot = np.sum(v0[valid] * v1[valid], axis=1) / (n0[valid] * n1[valid])
            if len(dot):
                max_angle = max(max_angle, float(np.degrees(np.arccos(np.clip(dot, -1.0, 1.0))).max()))
    return max_amp, max_angle


def source_grids():
    nx, ny, rs, gb, cells, cell_rows, overlays = ek.read_inputs()
    types, substrates, *_ = ek.surface_layer(cells, cell_rows, overlays)
    return types, substrates


def source_tripoints(grid):
    ny, nx = grid.shape
    pts = set(MAP_CORNERS)
    for y in range(ny + 1):
        for x in range(nx + 1):
            vals = [str(grid[yy, xx]) for yy in (y - 1, y) for xx in (x - 1, x)
                    if 0 <= yy < ny and 0 <= xx < nx]
            if len(set(vals)) >= 3:
                pts.add((float(x), float(y)))
            elif (x in (0, nx) or y in (0, ny)) and len(vals) == 2 and vals[0] != vals[1]:
                # The outside of the viewer rectangle is the third zone at a
                # border transition, so these are genuine boundary tripoints.
                pts.add((float(x), float(y)))
    return pts


def output_tripoints(features, layer):
    key = "typ" if layer == "flaechentyp" else "untergrund"
    selected = [f for f in features if f["properties"].get("layer") == layer]
    geoms = [shape(f["geometry"]) for f in selected]
    labels = [f["properties"][key] for f in selected]
    tree = STRtree(geoms)
    arcs = shared_boundary_arcs(features, layer)
    endpoints = set()
    for line in arcs:
        if not line.is_ring:
            endpoints.add(tuple(round(float(v), 3) for v in line.coords[0]))
            endpoints.add(tuple(round(float(v), 3) for v in line.coords[-1]))
    allowed, rejected = [], []
    for xy in sorted(endpoints):
        point = Point(xy)
        at_point = set()
        for idx in tree.query(point.buffer(0.05)):
            i = int(idx)
            if geoms[i].boundary.distance(point) <= 0.05:
                at_point.add(labels[i])
        on_border = xy[0] in (0.0, 336.0) or xy[1] in (0.0, 303.0)
        if xy in MAP_CORNERS or len(at_point) >= 3 or (on_border and len(at_point) >= 2):
            allowed.append(xy)
        else:
            rejected.append((xy, tuple(sorted(at_point))))
    return allowed, rejected


def source_type_counts():
    overlay = {}
    with (ROOT / "raster_c20_z25_overlay_plaetze_wege.csv").open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            overlay[(int(r["cx"]), int(r["cy"]))] = r
    counts = Counter()
    bauzone = 0
    with (RELIEF / "neu" / "zellen_relief.csv").open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            x, y = int(r["cx"]), int(r["cy"])
            ov = overlay.get((x, y), {})
            under = r["untergrund"]
            typ = "fels" if under in ("FELS", "KLIPPE_WAND", "KLIPPE_KANTE") else "grund"
            if r["ufer"] == "1": typ = "ufer"
            if ov.get("weg_klasse"): typ = "weg"
            if ov.get("bruecke") == "1": typ = "bruecke"
            if r["wasser_eis"] == "1" or under == "WASSER_EIS": typ = "wasser"
            counts[typ] += 1
            bauzone += int(r["bauzone_plan"] or 0)
    return counts, bauzone


def test_geojson_files_and_feature_contract():
    all_features = {name: read(name) for name in NAMES}
    for name, features in all_features.items():
        assert features, name
        for f in features:
            assert f["type"] == "Feature"
            assert f["geometry"] is not None
            g = shape(f["geometry"])
            assert not g.is_empty
            if g.geom_type in ("Polygon", "MultiPolygon"):
                assert g.is_valid, (name, f.get("properties"))
    for f in all_features["kanten.geojson"] + all_features["grat.geojson"]:
        g = shape(f["geometry"])
        assert g.geom_type == "LineString"
        assert g.length >= 3.0
        if f in all_features["grat.geojson"]:
            assert not g.is_ring
        p = f["properties"]
        assert len(p["hoehen_m"]) == len(g.coords)
        assert np.isfinite(p["hoehen_m"]).all()
        assert max(np.linalg.norm(np.diff(np.asarray(g.coords), axis=0), axis=1)) <= 0.25 + 1e-6
    zone_features = all_features["zonen.geojson"]
    ids = []
    for f in zone_features:
        p = f["properties"]
        ids.append(p["id"])
        assert type(p["klasse"]) is int and 0 <= p["klasse"] <= 5
        assert isinstance(p["untergrund"], str) and p["untergrund"]
        if p["layer"] == "flaechentyp":
            assert p["typ"] in CLASS_CODES
            assert p["klasse"] == CLASS_CODES[p["typ"]]
        elif p["layer"] == "untergrund":
            assert p["typ"] == p["untergrund"]
            assert shape(f["geometry"]).geom_type in ("Polygon", "MultiPolygon")
        elif p["layer"] == "slot":
            assert p.get("typ") in {"slot_bau", "slot_deko"}
            assert p.get("quelle")
        elif p["layer"] == "bauzone_plan":
            assert p["typ"] == "bauzone"
        else:
            raise AssertionError(f"unbekannte zonen-Ebene: {p['layer']}")
    assert len(ids) == len(set(ids)), "id muss innerhalb der FeatureCollection eindeutig sein"


def assert_partition(features, layer):
    geoms = [shape(f["geometry"]) for f in features if f["properties"].get("layer") == layer]
    assert geoms, layer
    assert all(g.is_valid for g in geoms)
    tree = STRtree(geoms)
    for i, geom in enumerate(geoms):
        for j in tree.query(geom):
            j = int(j)
            if j <= i:
                continue
            assert geom.intersection(geoms[j]).area <= 1e-8, (layer, i, j)
    union = unary_union(geoms)
    rect = box(0, 0, 336, 303)
    assert abs(union.symmetric_difference(rect).area) / rect.area < 1e-6, layer
    assert union.is_valid


def test_surface_and_substrate_partitions_are_topologically_exact():
    features = read("zonen.geojson")
    assert_partition(features, "flaechentyp")
    assert_partition(features, "untergrund")


def test_surface_and_bauzone_area_tolerances():
    features = read("zonen.geojson")
    surfaces = [f for f in features if f["properties"].get("layer") == "flaechentyp"]
    source_counts, bauzone_cells = source_type_counts()
    areas = Counter()
    for f in surfaces:
        areas[f["properties"]["typ"]] += shape(f["geometry"]).area
    for typ, cells in source_counts.items():
        delta = areas[typ] / cells - 1
        assert abs(delta) <= 0.03, (typ, areas[typ], cells, delta)
    bz = [shape(f["geometry"]) for f in features if f["properties"].get("layer") == "bauzone_plan"]
    assert bz
    delta = unary_union(bz).area / bauzone_cells - 1
    assert abs(delta) <= 0.01, delta


def test_real_grat_anchor_distances_and_continuity():
    lines = [(f["properties"]["name"], f["properties"], shape(f["geometry"])) for f in read("grat.geojson")]
    for x, z, name in TARGETS:
        matching = [(p, g) for n, p, g in lines if n == name]
        assert matching, f"keine echte Ridge fuer {name}"
        props, geom = min(matching, key=lambda pg: pg[1].distance(Point(x, z)))
        actual = geom.distance(Point(x, z))
        reported = props.get("anker_abstaende_m", {}).get(f"{int(x)}|{int(z)}")
        assert reported is not None
        assert abs(actual - reported) <= 0.002, (name, x, z, actual, reported)
    g3 = [g for n, _, g in lines if n == "G3H3"]
    assert len(g3) == 1 and not g3[0].is_ring and g3[0].length >= 3.0
    assert all("Hessian-Ridge" in p.get("quelle", "") for _, p, _ in lines)


def test_deterministic_sha256_second_run():
    scratch = Path("/tmp/dv2_kanten")
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="determinismus_", dir=scratch) as td:
        root = Path(td)
        outputs = []
        for i in (1, 2):
            out = root / f"run{i}"
            subprocess.run([sys.executable, str(GENERATOR), "--out", str(out)], check=True, capture_output=True, text=True)
            outputs.append({n: digest(out / n) for n in NAMES})
        assert outputs[0] == outputs[1]
        assert outputs[0] == {n: digest(VECTOR / n) for n in NAMES}


def test_q3_hard_3cm_and_15_degrees_with_only_zone_junction_exceptions():
    edge_lines = [shape(f["geometry"]) for f in read("kanten.geojson")]
    ridge_lines = [shape(f["geometry"]) for f in read("grat.geojson")]
    q3_edges = q3_metrics(edge_lines)
    q3_ridges = q3_metrics(ridge_lines)
    features = read("zonen.geojson")
    surface_arcs = shared_boundary_arcs(features, "flaechentyp")
    substrate_arcs = shared_boundary_arcs(features, "untergrund")
    q3_surface = q3_metrics(surface_arcs, endpoint_guard=0.5)
    q3_substrate = q3_metrics(substrate_arcs, endpoint_guard=0.5)
    for label, metrics in (("kanten", q3_edges), ("grat", q3_ridges),
                           ("flaechentyp", q3_surface), ("untergrund", q3_substrate)):
        assert metrics[0] <= 0.03, (label, "1-m deviation", metrics)
        assert metrics[1] <= 15.0, (label, "turn angle", metrics)


def test_zone_exceptions_are_only_true_tripoints_and_four_corners():
    features = read("zonen.geojson")
    surface_exceptions, surface_rejected = output_tripoints(features, "flaechentyp")
    substrate_exceptions, substrate_rejected = output_tripoints(features, "untergrund")
    # The returned sorted lists are the individually enumerated allowed points:
    # true 3+ label junctions, outer-border transitions, and four map corners.
    assert len(surface_exceptions) >= 4 and len(substrate_exceptions) >= 4
    assert not surface_rejected, ("flaechentyp non-tripoint endpoints", surface_rejected)
    assert not substrate_rejected, ("untergrund non-tripoint endpoints", substrate_rejected)
