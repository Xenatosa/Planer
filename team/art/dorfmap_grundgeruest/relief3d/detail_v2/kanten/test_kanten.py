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


FRAME = box(0, 0, 336, 303).boundary


def shared_boundary_arcs(features, layer):
    """Gemeinsame Grenzboegen zwischen Knoten. Der Kartenrahmen wird mit
    verknotet, damit Boegen am Rand enden (Randuebergang = Tripelpunkt mit dem
    Aussenraum); Rahmenstuecke selbst sind keine Labelgrenze und entfallen."""
    geoms = [shape(f["geometry"]) for f in features if f["properties"].get("layer") == layer]
    noded = unary_union([g.boundary for g in geoms] + [FRAME])
    fb = FRAME.buffer(1e-7)
    return [line for line in line_parts(line_merge(noded)) if line.length > 1e-6 and not fb.contains(line)]


def glaettung_abw(pl, fenster=1.0, geschlossen=False):
    """Woertlich aus QA P6 (origin/art/dv2-qa 38fa7ec, detail_v2/qa/dv2qa/geom.py):
    Stuetzpunkt vs. gleitendes Mittel der Stuetzpunkte innerhalb +-fenster/2
    Bogenlaenge (Abstand zur geglaetteten Linie) und Knick zwischen Nachbarsegmenten."""
    from shapely import LineString as _LS, points, distance
    pl = np.asarray(pl, float)
    if geschlossen and np.allclose(pl[0], pl[-1]): pl = pl[:-1]
    n = len(pl)
    if n < 3: return np.zeros(n), np.zeros(max(n - 2, 0))
    seg = np.hypot(*np.diff(np.vstack([pl, pl[:1]]) if geschlossen else pl, axis=0).T)
    s = np.r_[0, np.cumsum(seg)][:n]
    L = s[-1] + (seg[-1] if geschlossen else 0)
    g = np.empty_like(pl)
    for i in range(n):
        if geschlossen:
            dd = np.abs(s - s[i]); dd = np.minimum(dd, L - dd); m = dd <= fenster / 2
        else:
            hw = min(fenster / 2, s[i], s[-1] - s[i])
            m = (s >= s[i] - hw - 1e-9) & (s <= s[i] + hw + 1e-9)
        g[i] = pl[m].mean(0)
    gl = _LS(np.vstack([g, g[:1]]) if geschlossen else g)
    abw = distance(points(pl), gl)
    if not geschlossen:
        abw[0] = abw[-1] = 0
    P = np.vstack([pl[-1:], pl, pl[:1]]) if geschlossen else pl
    v1 = P[1:-1] - P[:-2]; v2 = P[2:] - P[1:-1]
    c = (v1 * v2).sum(1) / (np.hypot(*v1.T) * np.hypot(*v2.T) + 1e-15)
    knick = np.degrees(np.arccos(np.clip(c, -1, 1)))
    return abw, knick


def qa_verstoesse(lines, grenze_m=0.03, grenze_grad=15.0):
    """QA-Messart je Linie; liefert (max_abw, max_knick, [(x, z, abw, knick)])."""
    worst_a = worst_k = 0.0
    bad = []
    for line in lines:
        p = np.asarray(line.coords, float)
        closed = len(p) > 2 and np.allclose(p[0], p[-1])
        abw, knick = glaettung_abw(p, 1.0, closed)
        inner = p[:-1] if closed else p
        kp = inner if closed else inner[1:-1]
        if len(abw):
            worst_a = max(worst_a, float(abw.max()))
        if len(knick):
            worst_k = max(worst_k, float(knick.max()))
        for i in np.where(abw > grenze_m)[0]:
            bad.append((round(float(inner[i, 0]), 2), round(float(inner[i, 1]), 2), "abw", round(float(abw[i]), 4)))
        for i in np.where(knick > grenze_grad)[0]:
            bad.append((round(float(kp[i, 0]), 2), round(float(kp[i, 1]), 2), "knick", round(float(knick[i]), 2)))
    return worst_a, worst_k, bad


def fein_verstoesse(lines, endpoint_guard=0.0, grenze_m=0.03, grenze_grad=15.0):
    """5-cm-Abtastung, 21-Punkt-Mittel (1 m), Ortsliste aller Verstoesse."""
    bad = []
    for line in lines:
        p = np.asarray(line.coords, dtype=float)
        seg = np.linalg.norm(np.diff(p, axis=0), axis=1)
        arc = np.r_[0.0, np.cumsum(seg)]
        total = float(arc[-1])
        closed = np.linalg.norm(p[0] - p[-1]) < 1e-7
        if total >= 1.0:
            step = 0.05
            s = (np.arange(int(np.ceil(total / step))) * (total / int(np.ceil(total / step)))) if closed \
                else np.linspace(0.0, total, max(2, int(np.ceil(total / step)) + 1))
            xy = np.column_stack((np.interp(s, arc, p[:, 0]), np.interp(s, arc, p[:, 1])))
            if closed:
                padded = np.vstack((xy[-10:], xy, xy[:10]))
                mean = np.column_stack([np.convolve(padded[:, k], np.ones(21) / 21, mode="valid") for k in range(2)])
                center, valid = xy, np.ones(len(s), bool)
            elif len(xy) > 21:
                mean = np.column_stack([np.convolve(xy[:, k], np.ones(21) / 21, mode="valid") for k in range(2)])
                center, cs = xy[10:-10], s[10:-10]
                valid = (cs >= endpoint_guard) & (cs <= total - endpoint_guard)
            else:
                center = mean = np.zeros((0, 2)); valid = np.zeros(0, bool)
            amp = np.linalg.norm(center - mean, axis=1)
            for i in np.where((amp > grenze_m) & valid)[0]:
                bad.append((round(float(center[i, 0]), 2), round(float(center[i, 1]), 2), "fein", round(float(amp[i]), 4)))
        q = p[:-1] if closed else p
        if len(q) >= 3:
            v0 = (q - np.roll(q, 1, axis=0)) if closed else q[1:-1] - q[:-2]
            v1 = (np.roll(q, -1, axis=0) - q) if closed else q[2:] - q[1:-1]
            pts = q if closed else q[1:-1]
            n0, n1 = np.linalg.norm(v0, axis=1), np.linalg.norm(v1, axis=1)
            ok = (n0 > 1e-8) & (n1 > 1e-8)
            ang = np.zeros(len(pts))
            ang[ok] = np.degrees(np.arccos(np.clip(np.sum(v0[ok] * v1[ok], axis=1) / (n0[ok] * n1[ok]), -1, 1)))
            for i in np.where(ang > grenze_grad)[0]:
                bad.append((round(float(pts[i, 0]), 2), round(float(pts[i, 1]), 2), "knick", round(float(ang[i]), 2)))
    return bad


def wegende_zonen():
    """Kreisscheiben um die Enden aller Weg-Mittellinien (wege.geojson, P1a2):
    Radius halbe Breite + 0,75 m. Ein Wegende mit runder Kappe bei < 3,2 m Wegbreite
    kann die 3-cm-Grenze geometrisch nicht halten (Kreis r < 1,6 m)."""
    feats = json.loads((VECTOR / "wege.geojson").read_text(encoding="utf-8"))["features"]
    zones = []
    for f in feats:
        p = f["properties"]
        if p.get("rolle") != "mittellinie":
            continue
        g = shape(f["geometry"])
        for end, xy in (("anfang", g.coords[0]), ("ende", g.coords[-1])):
            zones.append((f"{p['id']}#{p.get('teil', 0)}:{end}", Point(xy).buffer(float(p.get("breite", 3.0)) / 2 + 0.75)))
    return zones


def quelle_wegende(bad, features):
    """Ordnet Flaechentyp-Verstoesse einem Wegende zu, wenn der Ort auf dem Wegrand
    liegt und in einer Wegende-Zone; Rueckgabe (zugeordnet: {wegende}, uebrig: [...])."""
    weg = unary_union([shape(f["geometry"]) for f in features
                       if f["properties"].get("layer") == "flaechentyp" and f["properties"].get("typ") in ("weg", "bruecke")])
    zones = wegende_zonen()
    hits, rest = set(), []
    for b in bad:
        pt = Point(b[0], b[1])
        names = [n for n, z in zones if z.covers(pt)]
        if names and weg.boundary.distance(pt) <= 0.05:
            hits.add(sorted(names)[0])
        else:
            rest.append(b)
    return hits, rest


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
            # Ring: gleichmaessige Teilung (Naht ohne Restschritt, sonst
            # tangentialer Fensterversatz bis 1,7 cm als Scheinzacke).
            s = (np.arange(int(np.ceil(total / step))) * (total / int(np.ceil(total / step)))) if closed \
                else np.linspace(0.0, total, max(2, int(np.ceil(total / step)) + 1))
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


BRUECKEN_RECHTECKE = {"E2": box(186, 73, 197, 75), "E3-West": box(174, 126, 186, 128)}


def quell_flaechen():
    """Referenzflaechen direkt aus den Quellvektoren (detail_v2/vektor)."""
    rect = box(0, 0, 336, 303)
    def load(name):
        return json.loads((VECTOR / name).read_text(encoding="utf-8"))["features"]
    wasser = unary_union([shape(f["geometry"]) for f in load("wasser.geojson")]).intersection(rect)
    baender = unary_union([g for f in load("ufer.geojson") if f["properties"].get("typ") == "uferband"
                           for g in polygon_parts(shape(f["geometry"]))]).intersection(rect)
    netz = unary_union([shape(f["geometry"]) for f in load("wege.geojson")
                        if f["properties"].get("rolle") == "netz"]).intersection(rect)
    kandidat = netz.intersection(baender).difference(wasser)
    bruecke = unary_union([g for g in polygon_parts(kandidat)
                           if any(g.intersects(r) for r in BRUECKEN_RECHTECKE.values())])
    rechtecke = unary_union(list(BRUECKEN_RECHTECKE.values())).difference(wasser)
    return {"wasser": wasser, "ufer": baender.difference(wasser), "bruecke": bruecke,
            "weg": netz, "bruecke_rechtecke": rechtecke}


def flaechen_abweichungen():
    features = read("zonen.geojson")
    areas = Counter()
    for f in features:
        if f["properties"].get("layer") == "flaechentyp":
            areas[f["properties"]["typ"]] += shape(f["geometry"]).area
    ref = quell_flaechen()
    out = {typ: (areas[typ], ref[typ].area, areas[typ] / ref[typ].area - 1)
           for typ in ("wasser", "ufer", "bruecke", "weg")}
    out["bruecke_vs_rechtecke"] = (areas["bruecke"], ref["bruecke_rechtecke"].area,
                                   areas["bruecke"] / ref["bruecke_rechtecke"].area - 1)
    _, bauzone_cells = source_type_counts()
    bz = [shape(f["geometry"]) for f in features if f["properties"].get("layer") == "bauzone_plan"]
    out["bauzone"] = (unary_union(bz).area, float(bauzone_cells), unary_union(bz).area / bauzone_cells - 1)
    return out


def test_surface_and_bauzone_area_tolerances():
    dev = flaechen_abweichungen()
    print("FLAECHEN", {k: (round(a, 2), round(r, 2), round(100 * d, 3)) for k, (a, r, d) in dev.items()})
    # Wasser/Ufer/Bruecke +-3 % gegen die Vektorquelle, Bauzone +-1 % gegen 31 893 Zellen.
    for typ in ("wasser", "ufer", "bruecke"):
        assert abs(dev[typ][2]) <= 0.03, (typ, dev[typ])
    assert abs(dev["bauzone"][2]) <= 0.01, dev["bauzone"]


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
    with tempfile.TemporaryDirectory(prefix="dv2_kanten_determinismus_") as td:
        root = Path(td)
        outputs = []
        for i in (1, 2):
            out = root / f"run{i}"
            subprocess.run([sys.executable, str(GENERATOR), "--out", str(out)], check=True, capture_output=True, text=True)
            outputs.append({n: digest(out / n) for n in NAMES})
        assert outputs[0] == outputs[1]
        assert outputs[0] == {n: digest(VECTOR / n) for n in NAMES}


# Bekannte Quellen (vom Generator NICHT veraendert, Regel "Quellboegen nicht selbst aendern"):
# 1) Wegenden mit runder Kappe (wege.geojson, P1a2): bei < 3,2 m Breite geometrisch
#    nicht 3-cm-faehig. Einzeln aufgezaehlt; die Menge wird exakt verglichen.
BEKANNTE_WEGENDEN_LISTE = [
    'G001#0:ende',
    'G001_anb#0:ende',
    'G002#0:anfang',
    'G002#0:ende',
    'G003#0:anfang',
    'G003#0:ende',
    'G003_anb#0:anfang',
    'G003_anb#0:ende',
    'G004#1:ende',
    'G004_anb#0:anfang',
    'G004_anb#0:ende',
    'G005#1:ende',
    'G006#0:anfang',
    'G006#0:ende',
    'G006_anb#0:ende',
    'G007#0:anfang',
    'G007#1:anfang',
    'G008#1:ende',
    'G008_anb#0:anfang',
    'G008_anb#0:ende',
    'G009#1:anfang',
    'G009#1:ende',
    'G010#0:anfang',
    'G011#0:ende',
    'G011#1:anfang',
    'G012#0:anfang',
    'G012#0:ende',
    'G013#0:ende',
    'G014#0:ende',
    'G015#0:ende',
    'G015#1:ende',
    'G016#1:ende',
    'G017#0:ende',
    'G018_anb#0:ende',
    'G019_anb#0:anfang',
    'G902a#0:ende',
    'G903b#0:anfang',
    'G903b#0:ende',
    'haus_A11#0:anfang',
    'haus_A11#0:ende',
    'haus_A25#0:anfang',
    'haus_A25#0:ende',
    'haus_A31D#0:anfang',
    'haus_B28#0:anfang',
    'haus_B29D#0:anfang',
    'haus_B29D#0:ende',
    'haus_D02#0:anfang',
    'haus_D02#0:ende',
    'haus_D08#0:anfang',
    'haus_E04D#0:anfang',
    'haus_E07#0:anfang',
    'haus_E07#0:ende',
]  # 52 Wegenden (wege.geojson @ #59)
# 2) Wasserumriss (wasser.geojson, P1b2): die Uferlinien der Quelle verletzen die
#    QA-Messart selbst (max ~3,4 cm); Verstoesse <= 2 cm neben dem Quellumriss.
WASSER_TOLERANZ_M = 0.02


def q3_beide(lines, guard=0.0):
    qa_a, qa_k, qa_bad = qa_verstoesse(lines)
    fein = fein_verstoesse(lines, guard)
    f_a, f_k = q3_metrics(lines, guard)
    return {"qa": (qa_a, qa_k), "fein": (f_a, f_k), "verstoesse": qa_bad + fein}


def flaechentyp_zuordnung(bad, features):
    wegenden, rest = quelle_wegende(bad, features)
    wb = unary_union([shape(f["geometry"]).boundary
                      for f in json.loads((VECTOR / "wasser.geojson").read_text(encoding="utf-8"))["features"]])
    wasser = [b for b in rest if wb.distance(Point(b[0], b[1])) <= WASSER_TOLERANZ_M]
    uebrig = [b for b in rest if wb.distance(Point(b[0], b[1])) > WASSER_TOLERANZ_M]
    return wegenden, wasser, uebrig


def test_q3_both_metrics_hard_3cm_15deg():
    """Q3 nach beiden Messarten (QA-P6 glaettung_abw auf Stuetzpunkten und feine
    0,05-m-Abtastung) hart gegen 3,0 cm / 15 Grad. Ausnahmen nur echte Tripelpunkte und
    Kartenecken (Bogenenden) sowie die einzeln aufgezaehlten bekannten Quellen."""
    features = read("zonen.geojson")
    layers = {
        "kanten": ([shape(f["geometry"]) for f in read("kanten.geojson")], 0.0),
        "grat": ([shape(f["geometry"]) for f in read("grat.geojson")], 0.0),
        "untergrund": (shared_boundary_arcs(features, "untergrund"), 0.5),
        "flaechentyp": (shared_boundary_arcs(features, "flaechentyp"), 0.5),
    }
    res = {k: q3_beide(v, g) for k, (v, g) in layers.items()}
    for k, r in res.items():
        print("Q3", k, "QA %.2f cm %.1f deg" % (100 * r["qa"][0], r["qa"][1]),
              "fein %.2f cm %.1f deg" % (100 * r["fein"][0], r["fein"][1]), "verstoesse", len(r["verstoesse"]))
    for k in ("kanten", "grat", "untergrund"):
        assert not res[k]["verstoesse"], (k, res[k]["verstoesse"][:20])
        assert res[k]["qa"][0] <= 0.03 and res[k]["fein"][0] <= 0.03, (k, res[k])
        assert res[k]["qa"][1] <= 15.0 and res[k]["fein"][1] <= 15.0, (k, res[k])
    wegenden, wasser, uebrig = flaechentyp_zuordnung(res["flaechentyp"]["verstoesse"], features)
    print("Q3 flaechentyp bekannte Quelle Wegenden", len(wegenden), sorted(wegenden))
    print("Q3 flaechentyp bekannte Quelle Wasserumriss", len(wasser),
          "max %.2f cm" % (100 * max([b[3] for b in wasser if b[2] != "knick"], default=0)))
    assert not uebrig, ("flaechentyp Q3 ausserhalb Tripelpunkte/bekannter Quellen", uebrig)
    assert sorted(wegenden) == BEKANNTE_WEGENDEN_LISTE, sorted(set(wegenden) ^ set(BEKANNTE_WEGENDEN_LISTE))
    # P1c2: Mit #60 (Wasser/Ufer gleichmaessig 0,05 m) ist die Ausnahme Wasserumriss entfallen.
    assert not wasser, ("Wasserumriss-Verstoesse (seit #60 nicht mehr erlaubt)", wasser[:10])


def fein_ring_q3(coords):
    """Verbindliche QA-q3-Messart (ab 19.11. 18:08): Linie nach Bogenlaenge auf 0,05 m
    abtasten, gleitendes 1-m-Mittel (21 Punkte, Ring zyklisch); Knick an Stuetzpunkten.
    Rueckgabe Liste (x, z, wert, art) der Verstoesse > 3 cm bzw. > 15 Grad."""
    p = np.asarray(coords, float)
    if np.allclose(p[0], p[-1]):
        p = p[:-1]
    q = np.vstack([p, p[:1]])
    seg = np.linalg.norm(np.diff(q, axis=0), axis=1)
    s = np.r_[0, np.cumsum(seg)]
    n = max(int(np.ceil(s[-1] / 0.05)), 3)
    ss = np.arange(n) * (s[-1] / n)
    xy = np.column_stack([np.interp(ss, s, q[:, 0]), np.interp(ss, s, q[:, 1])])
    pad = np.vstack([xy[-10:], xy, xy[:10]])
    m = np.column_stack([np.convolve(pad[:, k], np.ones(21) / 21, "valid") for k in range(2)])
    a = np.linalg.norm(xy - m, axis=1)
    v1 = p - np.roll(p, 1, 0)
    v2 = np.roll(p, -1, 0) - p
    n1, n2 = np.linalg.norm(v1, axis=1), np.linalg.norm(v2, axis=1)
    ok = (n1 > 1e-9) & (n2 > 1e-9)
    k = np.where(ok, np.degrees(np.arccos(np.clip((v1 * v2).sum(1) / np.where(ok, n1 * n2, 1), -1, 1))), 0)
    return ([(xy[i, 0], xy[i, 1], a[i], "abw") for i in np.where(a > 0.03)[0]]
            + [(p[i, 0], p[i, 1], k[i], "knick") for i in np.where(k > 15.0)[0]])


def zonen_q3_gruppen():
    """Jeden q3-Fund (feine Messart) auf allen Polygonringen von zonen.geojson einer
    Gruppe zuordnen: a Tripelpunkt (>= 3 Zonen, Abstand <= 0,75 m), b Wegende
    (A-DV2-01, Wegende-Zone), c Kartenrand (<= 0,75 m), d Sonstiges."""
    features = read("zonen.geojson")
    trip = {}
    for layer in ("flaechentyp", "untergrund"):
        ex, _ = output_tripoints(features, layer)
        trip[layer] = [tuple(e[:2]) for e in ex]
    zones = wegende_zonen()
    funde = []
    for f in features:
        pr = f["properties"]
        for poly in polygon_parts(shape(f["geometry"])):
            for ring in [poly.exterior, *poly.interiors]:
                for x, z, v, art in fein_ring_q3(ring.coords):
                    pt = Point(x, z)
                    if FRAME.distance(pt) <= 0.75:
                        g = "c"
                    elif trip.get(pr["layer"]) and min((x - a) ** 2 + (z - b) ** 2 for a, b in trip[pr["layer"]]) <= 0.75 ** 2:
                        g = "a"
                    elif any(zz.covers(pt) for _, zz in zones):
                        g = "b"
                    else:
                        g = "d"
                    funde.append((pr["id"], pr["layer"], round(x, 2), round(z, 2), art, round(float(v), 4), g))
    return funde


def test_zonen_q3_fein_alle_ringe_nur_gruppen_a_b_c():
    funde = zonen_q3_gruppen()
    zus = Counter((f[1], f[6]) for f in funde)
    mx = {}
    for f in funde:
        if f[4] == "abw":
            mx[(f[1], f[6])] = max(mx.get((f[1], f[6]), 0), f[5])
    print("ZONEN_Q3_FEIN", dict(zus), {k: round(100 * v, 2) for k, v in mx.items()})
    sonst = [f for f in funde if f[6] == "d"]
    assert not sonst, ("q3-Funde Gruppe d (Sonstiges)", sonst[:20])
    # Bauzone und Slots: keine Funde (Bauzone glatt, Slots als Punkte)
    assert not [f for f in funde if f[1] in ("bauzone_plan", "slot")]


def test_zone_exceptions_are_only_true_tripoints_and_four_corners():
    features = read("zonen.geojson")
    surface_exceptions, surface_rejected = output_tripoints(features, "flaechentyp")
    substrate_exceptions, substrate_rejected = output_tripoints(features, "untergrund")
    # The returned sorted lists are the individually enumerated allowed points:
    # true 3+ label junctions, outer-border transitions, and four map corners.
    assert len(surface_exceptions) >= 4 and len(substrate_exceptions) >= 4
    assert not surface_rejected, ("flaechentyp non-tripoint endpoints", surface_rejected)
    assert not substrate_rejected, ("untergrund non-tripoint endpoints", substrate_rejected)
