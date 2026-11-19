#!/usr/bin/env python3
"""P4 detail_v2 Datenschicht: flaeche.png, begehbar.png, untergrund.png, hoehe.png (Fr, aus Vektoren + Mesh).

Stand Do 19.11.2026: GERUEST. Quellenpruefung und Prioritaets-Rasterung (Pixelmitten) sind fertig und per
--selbsttest geprueft; die Zuordnung GeoJSON-Eigenschaft -> Klasse wird Fr an das echte Schema von P1a/b/c
angepasst (Schema heute unbekannt, nichts geraten). Ohne Quellen bricht das Skript mit Exit 2 ab.

Aufruf:
    python3 baue_masken.py --pruefe-quellen
    python3 baue_masken.py --selbsttest
    python3 baue_masken.py --out /tmp/dv2_daten/masken      # Fr, wenn Vektoren + Mesh da sind
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

HIER = Path(__file__).resolve().parent
DV2 = HIER.parent                      # relief3d/detail_v2/
NX, NY, PX_PRO_M = 336, 303, 10
W, H = NX * PX_PRO_M, NY * PX_PRO_M

# Klassen (legende.json) und Prioritaet Wasser > Bruecke > Weg > Ufer > Fels/Klippe > Grund [F ueber Plan]
KLASSE = {"grund": 0, "weg": 1, "ufer": 2, "fels_klippe": 3, "wasser": 4, "bruecke": 5}
PRIORITAET = ["wasser", "bruecke", "weg", "ufer", "fels_klippe", "grund"]

# Erwartete Quellen (Plan 3.1/9). Feldzuordnung wird Fr am echten Schema festgelegt.
QUELLEN = {
    "wege": DV2 / "vektor" / "wege.geojson",            # P1a
    "kreuzungen": DV2 / "vektor" / "kreuzungen.geojson",  # P1a
    "wasser": DV2 / "vektor" / "wasser.geojson",        # P1b
    "ufer": DV2 / "vektor" / "ufer.geojson",            # P1b
    "zonen": DV2 / "vektor" / "zonen.geojson",          # P1c (Flaechentyp-/Zonenpolygone inkl. untergrund?)
    "kanten": DV2 / "vektor" / "kanten.geojson",        # P1c (Klippen-Ober/Unterkante)
    "grat": DV2 / "vektor" / "grat.geojson",            # P1c (Grat-Kronen)
    "mesh_manifest": DV2 / "mesh" / "manifest.json",    # P2 (Fr)
}


def pruefe_quellen() -> list[str]:
    fehlt = [k for k, p in QUELLEN.items() if not p.exists()]
    for k, p in QUELLEN.items():
        print(f"{'ok   ' if p.exists() else 'FEHLT'} {k:14s} {p.relative_to(DV2.parent)}")
    return fehlt


def pixelmitten(bbox_m=None):
    """Weltkoordinaten der Pixelmitten (x, z), optional auf bbox [x0,z0,x1,z1] beschraenkt."""
    x0, z0, x1, z1 = bbox_m or (0, 0, NX, NY)
    i0, j0 = int(np.floor(x0 * PX_PRO_M)), int(np.floor(z0 * PX_PRO_M))
    i1, j1 = min(W, int(np.ceil(x1 * PX_PRO_M))), min(H, int(np.ceil(z1 * PX_PRO_M)))
    xs = (np.arange(i0, i1) + 0.5) / PX_PRO_M
    zs = (np.arange(j0, j1) + 0.5) / PX_PRO_M
    return i0, j0, xs, zs


def rastere_klassen(polys: dict[str, list]) -> np.ndarray:
    """polys: klasse -> Liste shapely-(Multi)Polygone in Viewer-Metern. Rasterung an Pixelmitten,
    hoehere Prioritaet ueberschreibt niedrigere. Ergebnis uint8 (H, W), Grund = 0."""
    import shapely
    out = np.zeros((H, W), np.uint8)
    for kl in reversed(PRIORITAET):          # niedrigste zuerst, hoechste zuletzt
        for g in polys.get(kl, []):
            if g.is_empty:
                continue
            shapely.prepare(g)
            i0, j0, xs, zs = pixelmitten(g.bounds)
            if xs.size == 0 or zs.size == 0:
                continue
            X, Z = np.meshgrid(xs, zs)
            m = shapely.contains_xy(g, X, Z)
            out[j0:j0 + m.shape[0], i0:i0 + m.shape[1]][m] = KLASSE[kl]
    return out


def selbsttest() -> None:
    from shapely.geometry import Polygon, box
    polys = {"grund": [box(0, 0, NX, NY)], "fels_klippe": [box(10, 10, 20, 20)],
             "weg": [box(15, 0, 16, 303)], "wasser": [Polygon([(15.2, 12), (40, 12), (40, 18), (15.2, 18)])]}
    r = rastere_klassen(polys)
    assert r.shape == (H, W) and r.dtype == np.uint8
    px = lambda x, z: r[int(z * 10), int(x * 10)]
    assert px(5, 5) == 0 and px(12, 12) == 3 and px(15.5, 5) == 1
    assert px(15.5, 15) == 4, "Wasser muss Weg ueberschreiben"
    assert px(15.15, 15) == 1 and px(15.25, 15) == 4   # Kante bei 15,2 m: Pixelmitte 15,15 vs 15,25
    print("selbsttest ok")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pruefe-quellen", action="store_true")
    ap.add_argument("--selbsttest", action="store_true")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    if a.selbsttest:
        selbsttest(); return
    fehlt = pruefe_quellen()
    if a.pruefe_quellen:
        sys.exit(2 if fehlt else 0)
    if fehlt:
        print(f"Abbruch: Quellen fehlen {fehlt} (s. STATUS.md). Keine Masken erzeugt.", file=sys.stderr)
        sys.exit(2)
    raise NotImplementedError("Fr: Feldzuordnung an das echte P1-Schema + Hoehenrasterung aus P2-Mesh (s. STATUS.md)")


if __name__ == "__main__":
    main()
