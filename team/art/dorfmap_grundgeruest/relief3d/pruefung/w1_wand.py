#!/usr/bin/env python3
"""W1 Wandkoerper (P10d). Prueft die GERENDERTEN Wandkoerper gegen das gerenderte Gelaende.

Aufruf (relief3d/):  python3 pruefung/w1_wand.py [QUELLE] [AUSGABE.json]
  QUELLE  index.html (Standard; liest window.NEU_GZ wie der Viewer), neu/relief_neu.json.gz
          oder ein 56-Kachel-Paket alle_kacheln.json.gz (pruefung/alle_kacheln/baue_alle_kacheln.py)
  AUSGABE Standard pruefung/w1_letzter_lauf.json
Exit 1 bei mindestens einem Treffer (wie pruefe_regeln.py / r8 / r9). Liest nur.

Teilpruefungen (Schwellen [A], Begruendung in REGELN_VERPFLICHTEND.md, Abschnitt W1):
  W1a_ausserhalb_karte  Wandvertex ausserhalb 0..nx / 0..ny Zellen (Karte 336 x 303).
  W1b_ueber_krone       Wandvertex mehr als 0,5 m ueber der lokalen Gelaendekrone = hoechster
                        Gelaendepunkt im Kreis von 1,5 Zellen um den Vertex (frei stehende Wand).
  W1c_schwebend         Unterkante (tiefster Vertex je x|z-Saeule des Koerpers) mehr als 0,5 m ueber dem
                        Gelaende direkt darunter (Gelaendefuss an dieser Stelle) -> Wand schwebt.
  W1d_quellabstand      Wandvertex weiter als 1 Zelle + halbe Wandbreite (+0,02 Kappenzugabe) vom
                        naechsten Quellzellen-Quadrat (vektor.json waende[].quellzellen) -> Wandlinie
                        mehr als 1 Zelle neben ihren Quellzellen (z. B. Einheitenfehler wie vor P10c).
Gelaende: Kachel-Meshes aus der Quelle (Raster 0,5 Zellen, Dreiecke wie neu/mesh.tile_mesh), wo keine
vorliegen GB aus relief_daten.json.gz. Ein Treffer = eine Zelle (floor x|z) je Teilpruefung und Kachel.
"""
import base64
import gzip
import json
import re
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import maximum_filter
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[1]
SCHWELLE_KRONE_M = 0.5      # [A]
SCHWELLE_SCHWEBEN_M = 0.5   # [A]
KRONE_RADIUS_ZELLEN = 1.5   # [A]
QUELL_ABSTAND_ZELLEN = 1.0  # [A]
CELL_M = 1.2


def lade_quelle(pfad: Path):
    roh = pfad.read_bytes()
    if pfad.suffix == ".html":
        m = re.search(rb'window\.NEU_GZ="([^"]+)"', roh)
        if not m:
            raise SystemExit(f"{pfad}: window.NEU_GZ nicht gefunden")
        roh = base64.b64decode(m.group(1))
    d = json.loads(gzip.decompress(roh))
    if "neu_mesh_tiles" in d:
        man = d["neu_mesh_tiles"]
        return man["tiles"], man["waende"]["tiles"], "relief_neu"
    if "alle_kacheln" in d:
        a = d["alle_kacheln"]
        return a["tiles"], a["waende"]["tiles"], "alle_kacheln"
    raise SystemExit(f"{pfad}: unbekanntes Format")


def gelaende_raster():
    d = json.loads(gzip.decompress((ROOT / "relief_daten.json.gz").read_bytes()))
    rs, nx, ny = int(d["rs"]), int(d["nx"]), int(d["ny"])
    gb = np.frombuffer(base64.b64decode(d["GB"]), "<f4").reshape(ny * rs + 1, nx * rs + 1).astype(np.float64)
    return gb.copy(), rs, nx, ny


def feld(x, z):
    return "ABCDEFGH"[int(np.clip(x // 42, 0, 7))] + str(int(np.clip(z // 43, 0, 6)) + 1)


def sample(G, rs, x, z):
    """Gelaendehoehe wie die gerenderten Dreiecke (Diagonale a-d, vgl. neu/wand._sample_grid)."""
    u = np.clip(x * rs, 0, G.shape[1] - 1.001)
    v = np.clip(z * rs, 0, G.shape[0] - 1.001)
    ix, iz = np.floor(u).astype(np.int64), np.floor(v).astype(np.int64)
    du, dv = u - ix, v - iz
    a, b, c, d = G[iz, ix], G[iz, ix + 1], G[iz + 1, ix], G[iz + 1, ix + 1]
    return np.where(du <= dv, a * (1 - dv) + c * (dv - du) + d * du, a * (1 - du) + b * (du - dv) + d * dv)


def main():
    quelle = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "index.html"
    ausgabe = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "pruefung" / "w1_letzter_lauf.json"
    tiles, wand_tiles, fmt = lade_quelle(quelle)
    G, rs, nx, ny = gelaende_raster()
    gesetzt = 0
    for t, item in tiles.items():
        if not item.get("vertices_xyz_f32"):
            continue
        P = np.frombuffer(base64.b64decode(item["vertices_xyz_f32"]), "<f4").reshape(-1, 3)
        ix, iz = np.rint(P[:, 0] * rs).astype(int), np.rint(P[:, 2] * rs).astype(int)
        ok = (ix >= 0) & (ix < G.shape[1]) & (iz >= 0) & (iz < G.shape[0])
        G[iz[ok], ix[ok]] = P[ok, 1]
        gesetzt += int(ok.sum())
    r = int(np.ceil(KRONE_RADIUS_ZELLEN * rs))
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    Gmax = maximum_filter(G, footprint=(xx ** 2 + yy ** 2) <= (KRONE_RADIUS_ZELLEN * rs) ** 2 + 1e-9, mode="nearest")

    vek = json.loads((ROOT / "neu" / "vektor.json").read_text(encoding="utf-8"))
    q = np.unique(np.concatenate([np.asarray(w["quellzellen"], int) for w in vek["waende"]]))
    QC = np.stack([q % nx + 0.5, q // nx + 0.5], 1)
    qtree = cKDTree(QC)
    halbe_breite = max(float(w["breite_min_m"]) for w in vek["waende"]) / CELL_M * 0.5
    grenze_d = QUELL_ABSTAND_ZELLEN + halbe_breite + 0.02

    treffer, stat = [], {}
    regeln = ("W1a_ausserhalb_karte", "W1b_ueber_krone", "W1c_schwebend", "W1d_quellabstand")
    for t, w in sorted(wand_tiles.items()):
        if not w.get("vertices"):
            continue
        P = np.frombuffer(base64.b64decode(w["vertices_xyz_f32"]), "<f4").reshape(-1, 3).astype(np.float64)
        x, y, z = P[:, 0], P[:, 1], P[:, 2]
        st = {"vertices": len(P)}
        befunde = {}
        # a) ausserhalb der Karte
        m_a = (x < 0) | (x > nx) | (z < 0) | (z > ny)
        befunde["W1a_ausserhalb_karte"] = (m_a, np.zeros(len(P)))
        # b) ueber lokaler Krone (konservativ: Maximum der 4 umliegenden Rasterpunkte des Max-Filters)
        u = np.clip(x * rs, 0, G.shape[1] - 1.001); v = np.clip(z * rs, 0, G.shape[0] - 1.001)
        i0, j0 = np.floor(u).astype(int), np.floor(v).astype(int)
        krone = np.maximum.reduce([Gmax[j0, i0], Gmax[j0, i0 + 1], Gmax[j0 + 1, i0], Gmax[j0 + 1, i0 + 1]])
        ueber = y - krone
        befunde["W1b_ueber_krone"] = ((ueber > SCHWELLE_KRONE_M) & ~m_a, ueber)
        # c) schwebend: tiefster Vertex je x|z-Saeule ueber dem Gelaende darunter
        key = np.round(P[:, [0, 2]], 4)
        _, inv = np.unique(key, axis=0, return_inverse=True)
        inv = inv.ravel()
        unten = np.full(inv.max() + 1, np.inf); np.minimum.at(unten, inv, y)
        ist_unten = y <= unten[inv] + 1e-6
        luecke = y - sample(G, rs, x, z)
        befunde["W1c_schwebend"] = (ist_unten & (luecke > SCHWELLE_SCHWEBEN_M) & ~m_a, luecke)
        # d) Abstand zu Quellzellen-Quadraten
        dist, nn = qtree.query(np.column_stack((x, z)), k=min(4, len(QC)))
        box = np.maximum(np.abs(np.column_stack((x, z))[:, None, :] - QC[nn]) - 0.5, 0.0)
        dbox = np.linalg.norm(box, axis=2).min(axis=1)
        befunde["W1d_quellabstand"] = (dbox > grenze_d, dbox)
        st["max_ueber_krone_m"] = round(float(ueber.max()), 3)
        st["max_luecke_unterkante_m"] = round(float(luecke[ist_unten].max()), 3) if ist_unten.any() else None
        st["max_quellabstand_zellen"] = round(float(dbox.max()), 3)
        st["vertices_ueber_gelaende_0_1m"] = int((luecke > 0.1).sum())
        for regel in regeln:
            m, wert = befunde[regel]
            st[regel + "_vertices"] = int(m.sum())
            if not m.any():
                continue
            zellen = {}
            for xi, zi, wv in zip(x[m], z[m], wert[m]):
                k = (int(np.floor(xi)), int(np.floor(zi)))
                zellen[k] = max(zellen.get(k, -np.inf), float(wv))
            for (cx, cz), wv in sorted(zellen.items()):
                treffer.append({"regel": regel, "feld": t, "x": cx, "z": cz, "wert": round(wv, 3),
                                "zellfeld": feld(cx, cz)})
        stat[t] = st
    je_regel = {r_: sum(1 for h in treffer if h["regel"] == r_) for r_ in regeln}
    je_feld = {}
    for h in treffer:
        je_feld.setdefault(h["feld"], {}).setdefault(h["regel"], 0)
        je_feld[h["feld"]][h["regel"]] += 1
    out = {"summe": len(treffer), "je_regel": je_regel, "je_feld": je_feld,
           "quelle": str(quelle), "format": fmt, "gelaende_vertices_aus_quelle": gesetzt,
           "schwellen_A": {"krone_m": SCHWELLE_KRONE_M, "krone_radius_zellen": KRONE_RADIUS_ZELLEN,
                           "schweben_m": SCHWELLE_SCHWEBEN_M, "quellabstand_zellen": QUELL_ABSTAND_ZELLEN,
                           "quellabstand_vertex_grenze_zellen": round(grenze_d, 3)},
           "je_kachel": stat, "treffer": treffer}
    ausgabe.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"summe": out["summe"], "je_regel": je_regel}))
    sys.exit(1 if treffer else 0)


if __name__ == "__main__":
    main()
