#!/usr/bin/env python3
"""P4 detail_v2 Datenschicht: flaeche.png, untergrund.png, begehbar.png (+ hoehe.png ab P2-Mesh).

GeoJSON-Schema (Entscheidung Grundgeruest 19.11.2026) [F]:
  FeatureCollection, Koordinaten in Viewer-Metern (1 Einheit = 1 Zelle = 1 m, Ursprung Weltecke wie UV1),
  Properties: klasse (int 0-5, s. legende.json flaeche.klassen), untergrund (Schnee/Wald/Boden/Sand), id.
Gerastert werden alle (Multi)Polygon-Features aus detail_v2/vektor/*.geojson:
  - flaeche.png: Feature mit Property klasse, Prioritaet Wasser > Bruecke > Weg > Ufer > Fels/Klippe > Grund,
    Pixelmitten-Regel; nicht abgedeckte Pixel = 0 (Grund).
  - untergrund.png: Features mit Property untergrund (zonen.geojson); fehlt sie ueberall -> 1-m-Fallback aus
    zellen_relief.csv (im Lauf ausgewiesen). Wo flaeche wasser/fels_klippe/bruecke ist -> 0 [A].
  - begehbar.png: vorerst nur aus der Flaeche (wasser, fels_klippe -> 0, sonst 1) [A]; Neigungsgrenze aus dem
    Mesh folgt mit P2 (Fr). Linien-/Punkt-Features (Mittellinien, Kanten) werden nicht gerastert.
  - hoehe.png: aus P2-Mesh (Fr), hier noch nicht implementiert.

Aufruf:
    python3 baue_masken.py --pruefe-quellen
    python3 baue_masken.py --selbsttest
    python3 baue_masken.py --out <ordner> [--vektor <ordner>] [--ohne-mesh]
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

import numpy as np

HIER = Path(__file__).resolve().parent
DV2 = HIER.parent                      # relief3d/detail_v2/
RELIEF = DV2.parent
NX, NY, PX_PRO_M = 336, 303, 10
W, H = NX * PX_PRO_M, NY * PX_PRO_M
RAND_TOL_M = 0.01

KLASSE = {"grund": 0, "weg": 1, "ufer": 2, "fels_klippe": 3, "wasser": 4, "bruecke": 5}
KLASSE_NAME = {v: k for k, v in KLASSE.items()}
PRIORITAET = ["wasser", "bruecke", "weg", "ufer", "fels_klippe", "grund"]   # hoechste zuerst
UNTERGRUND = {"schnee": 1, "wald": 2, "boden": 3, "sand": 4}
UNTERGRUND_ALT = {"SCHNEE": 1, "WALD": 2, "BODEN": 3, "SAND": 4}
OHNE_UNTERGRUND = (KLASSE["wasser"], KLASSE["fels_klippe"], KLASSE["bruecke"])
NICHT_BEGEHBAR = (KLASSE["wasser"], KLASSE["fels_klippe"])

QUELLEN = {
    "wege": "wege.geojson", "kreuzungen": "kreuzungen.geojson",          # P1a
    "wasser": "wasser.geojson", "ufer": "ufer.geojson",                  # P1b
    "zonen": "zonen.geojson", "kanten": "kanten.geojson", "grat": "grat.geojson",  # P1c
}
MESH_MANIFEST = DV2 / "mesh" / "manifest.json"                           # P2 (Fr)


def pruefe_quellen(vektor: Path, mesh: bool = True) -> list[str]:
    fehlt = []
    for k, n in QUELLEN.items():
        ok = (vektor / n).exists(); fehlt += [] if ok else [k]
        print(f"{'ok   ' if ok else 'FEHLT'} {k:14s} {vektor / n}")
    if mesh:
        ok = MESH_MANIFEST.exists(); fehlt += [] if ok else ["mesh_manifest"]
        print(f"{'ok   ' if ok else 'FEHLT'} {'mesh_manifest':14s} {MESH_MANIFEST}")
    return fehlt


def lies_features(pfad: Path) -> list[dict]:
    """FeatureCollection lesen und gegen das Schema pruefen. Rueckgabe: Polygon-Features
    {id, quelle, geom, klasse|None, untergrund|None}. Fehler -> ValueError mit Datei + id."""
    from shapely.geometry import shape
    d = json.loads(pfad.read_text(encoding="utf-8"))
    if d.get("type") != "FeatureCollection":
        raise ValueError(f"{pfad.name}: keine FeatureCollection")
    out = []
    for n, f in enumerate(d.get("features", [])):
        p = f.get("properties") or {}
        fid = p.get("id", f.get("id", f"#{n}"))
        g = f.get("geometry")
        if not g or g.get("type") not in ("Polygon", "MultiPolygon"):
            continue                                   # Linien/Punkte: nicht rastern
        geom = shape(g)
        if not geom.is_valid:
            raise ValueError(f"{pfad.name} id={fid}: Polygon ungueltig")
        x0, z0, x1, z1 = geom.bounds
        if x0 < -RAND_TOL_M or z0 < -RAND_TOL_M or x1 > NX + RAND_TOL_M or z1 > NY + RAND_TOL_M:
            raise ValueError(f"{pfad.name} id={fid}: ausserhalb 0-{NX}|0-{NY} m (bounds {geom.bounds}) - Einheit pruefen (1,2-m-Zellen?)")
        kl = p.get("klasse")
        if kl is not None:
            if isinstance(kl, bool) or not isinstance(kl, int) or kl not in KLASSE_NAME:
                raise ValueError(f"{pfad.name} id={fid}: klasse {kl!r} nicht 0-5")
        ug = p.get("untergrund")
        if ug is not None:
            if str(ug).lower() not in UNTERGRUND:
                raise ValueError(f"{pfad.name} id={fid}: untergrund {ug!r} nicht Schnee/Wald/Boden/Sand")
            ug = UNTERGRUND[str(ug).lower()]
        out.append({"id": fid, "quelle": pfad.name, "geom": geom, "klasse": kl, "untergrund": ug})
    return out


def pixelmitten(bbox_m):
    x0, z0, x1, z1 = bbox_m
    i0, j0 = max(0, int(np.floor(x0 * PX_PRO_M))), max(0, int(np.floor(z0 * PX_PRO_M)))
    i1, j1 = min(W, int(np.ceil(x1 * PX_PRO_M))), min(H, int(np.ceil(z1 * PX_PRO_M)))
    return i0, j0, (np.arange(i0, i1) + 0.5) / PX_PRO_M, (np.arange(j0, j1) + 0.5) / PX_PRO_M


def male(out: np.ndarray, geom, wert: int) -> int:
    import shapely
    if geom.is_empty:
        return 0
    shapely.prepare(geom)
    i0, j0, xs, zs = pixelmitten(geom.bounds)
    if xs.size == 0 or zs.size == 0:
        return 0
    X, Z = np.meshgrid(xs, zs)
    m = shapely.contains_xy(geom, X, Z)
    out[j0:j0 + m.shape[0], i0:i0 + m.shape[1]][m] = wert
    return int(m.sum())


def rastere_flaeche(features: list[dict]) -> np.ndarray:
    out = np.zeros((H, W), np.uint8)
    for kl in reversed(PRIORITAET):                    # niedrigste zuerst, hoechste zuletzt
        for f in features:
            if f["klasse"] == KLASSE[kl]:
                male(out, f["geom"], KLASSE[kl])
    return out


def untergrund_fallback_1m() -> np.ndarray:
    import csv
    z = np.zeros((NY, NX), np.uint8)
    with (RELIEF / "zellen_relief.csv").open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            z[int(r["cy"]), int(r["cx"])] = UNTERGRUND_ALT.get(r["untergrund"], 0)
    return np.kron(z, np.ones((PX_PRO_M, PX_PRO_M), np.uint8))


def rastere_untergrund(features: list[dict], flaeche: np.ndarray) -> tuple[np.ndarray, str]:
    ug = [f for f in features if f["untergrund"] is not None]
    if ug:
        out = np.zeros((H, W), np.uint8)
        for f in ug:
            male(out, f["geom"], f["untergrund"])
        quelle = f"Polygone ({len(ug)} Features)"
    else:
        out, quelle = untergrund_fallback_1m(), "FALLBACK 1 m zellen_relief.csv (keine untergrund-Polygone)"
    out[np.isin(flaeche, OHNE_UNTERGRUND)] = 0
    return out, quelle


def begehbar_aus_flaeche(flaeche: np.ndarray) -> np.ndarray:
    return (~np.isin(flaeche, NICHT_BEGEHBAR)).astype(np.uint8)


def schreibe_png(arr: np.ndarray, ziel: Path, bit: int) -> None:
    from PIL import Image
    if bit == 1:
        img = Image.fromarray((arr > 0).astype(np.uint8) * 255).convert("1")
    elif bit == 8:
        img = Image.fromarray(arr.astype(np.uint8), "L")
    else:
        img = Image.fromarray(arr.astype(np.uint16))
    img.save(ziel)
    chk = np.array(Image.open(ziel))
    soll = (arr > 0) if bit == 1 else arr
    assert (chk.astype(soll.dtype) == soll).all(), f"Rueckleseprobe {ziel.name} fehlgeschlagen"


def baue(vektor: Path, out: Path) -> dict:
    feats = []
    for n in sorted(vektor.glob("*.geojson")):
        feats += lies_features(n)
    if not any(f["klasse"] is not None for f in feats):
        raise ValueError("kein Polygon-Feature mit Property klasse gefunden")
    fl = rastere_flaeche(feats)
    ug, ug_quelle = rastere_untergrund(feats, fl)
    be = begehbar_aus_flaeche(fl)
    out.mkdir(parents=True, exist_ok=True)
    schreibe_png(fl, out / "flaeche.png", 8)
    schreibe_png(ug, out / "untergrund.png", 8)
    schreibe_png(be, out / "begehbar.png", 1)
    anteil = {KLASSE_NAME[k]: round(float((fl == k).mean()), 5) for k in KLASSE_NAME}
    return {"features": len(feats), "flaeche_anteil": anteil, "untergrund_quelle": ug_quelle,
            "begehbar_regel": "nur Flaeche (Neigung aus Mesh fehlt)"}


def selbsttest() -> None:
    fc = lambda feats: {"type": "FeatureCollection", "features": [
        {"type": "Feature", "properties": p, "geometry": {"type": "Polygon", "coordinates": [c]}} for p, c in feats]}
    box = lambda x0, z0, x1, z1: [[x0, z0], [x1, z0], [x1, z1], [x0, z1], [x0, z0]]
    with tempfile.TemporaryDirectory(prefix="dv2_daten_selbst_") as t:
        v = Path(t) / "vektor"; v.mkdir()
        (v / "zonen.geojson").write_text(json.dumps(fc([
            ({"id": "z1", "klasse": 0, "untergrund": "Schnee"}, box(0, 0, NX, NY)),
            ({"id": "z2", "klasse": 0, "untergrund": "Wald"}, box(50, 50, 60, 60)),
            ({"id": "f1", "klasse": 3}, box(10, 10, 20, 20))])))
        (v / "wege.geojson").write_text(json.dumps(fc([({"id": "w1", "klasse": 1}, box(15, 0, 16, 303))])))
        (v / "wasser.geojson").write_text(json.dumps(fc([({"id": "a1", "klasse": 4}, box(15.2, 12, 40, 18))])))
        (v / "linien.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": [
            {"type": "Feature", "properties": {"id": "l1"}, "geometry": {"type": "LineString", "coordinates": [[0, 0], [5, 5]]}}]}))
        info = baue(v, Path(t) / "out")
        from PIL import Image
        fl = np.array(Image.open(Path(t) / "out" / "flaeche.png"))
        ug = np.array(Image.open(Path(t) / "out" / "untergrund.png"))
        be = np.array(Image.open(Path(t) / "out" / "begehbar.png"))
        px = lambda a, x, z: a[int(z * 10), int(x * 10)]
        assert fl.shape == (H, W) and fl.dtype == np.uint8
        assert px(fl, 5, 5) == 0 and px(fl, 12, 12) == 3 and px(fl, 15.5, 5) == 1
        assert px(fl, 15.5, 15) == 4, "Wasser muss Weg ueberschreiben"
        assert px(fl, 15.15, 15) == 1 and px(fl, 15.25, 15) == 4   # Kante 15,2 m an Pixelmitten
        assert px(ug, 5, 5) == 1 and px(ug, 55, 55) == 2 and px(ug, 30, 15) == 0 and px(ug, 12, 12) == 0
        assert px(ug, 15.5, 5) == 1                                 # Weg behaelt Untergrund [A]
        assert bool(px(be, 5, 5)) and not bool(px(be, 30, 15)) and not bool(px(be, 12, 12))
        assert info["untergrund_quelle"].startswith("Polygone")
        # Schemafehler werden erkannt
        for p, msg in [({"id": "x", "klasse": 7}, "klasse"), ({"id": "y", "klasse": 0, "untergrund": "Eis"}, "untergrund")]:
            (v / "kaputt.geojson").write_text(json.dumps(fc([(p, box(1, 1, 2, 2))])))
            try:
                lies_features(v / "kaputt.geojson"); raise AssertionError(f"{msg}-Fehler nicht erkannt")
            except ValueError as e:
                assert msg in str(e)
        (v / "kaputt.geojson").write_text(json.dumps(fc([({"id": "e", "klasse": 0}, box(0, 0, 400, 10))])))
        try:
            lies_features(v / "kaputt.geojson"); raise AssertionError("Einheitenfehler nicht erkannt")
        except ValueError as e:
            assert "ausserhalb" in str(e)
    print("selbsttest ok")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pruefe-quellen", action="store_true")
    ap.add_argument("--selbsttest", action="store_true")
    ap.add_argument("--vektor", type=Path, default=DV2 / "vektor")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--ohne-mesh", action="store_true", help="flaeche/untergrund/begehbar ohne Mesh (kein hoehe.png)")
    a = ap.parse_args()
    if a.selbsttest:
        selbsttest(); return
    fehlt = pruefe_quellen(a.vektor, mesh=not a.ohne_mesh)
    if a.pruefe_quellen or not a.out:
        sys.exit(2 if fehlt else 0)
    if fehlt:
        print(f"Abbruch: Quellen fehlen {fehlt} (s. STATUS.md). Keine Masken erzeugt.", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(baue(a.vektor, a.out), ensure_ascii=False, indent=1))
    if not a.ohne_mesh:
        raise NotImplementedError("hoehe.png + Neigung fuer begehbar aus P2-Mesh: Fr nach P2")


if __name__ == "__main__":
    main()
