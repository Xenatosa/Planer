#!/usr/bin/env python3
"""P10: Markdown zum Vertex-Hash-Vergleich (hash_vergleich.json) und Mesh-Hashes aller Kacheln.
Aufruf: python3 pruefung/alle_kacheln/hash_bericht.py /tmp/p10/hash_vergleich.json /tmp/p10/alle_kacheln_build.json OUT.md"""
import json, sys
from pathlib import Path

hv = json.loads(Path(sys.argv[1]).read_text())
bi = json.loads(Path(sys.argv[2]).read_text())
L = ["# P10 Vertex-Hash-Vergleich D1/G1/D2: index.html vs. alle_kacheln.html", "",
     f"Referenz: `{hv['referenz']}` (Kacheln {', '.join(hv['referenz_kacheln'])}) · Neu: `{hv['neu']}` ({len(hv['neu_kacheln'])} Kacheln)", "",
     "Verglichen im gerenderten Three.js-Szenengraph (Ebene `gelaende`): SHA-256 der Weltkoordinaten (Float32, matrixWorld angewendet) "
     "und der Indizes je Mesh (Oberfläche, Seiten, Boden).", "",
     f"**Ergebnis: {'alle identisch' if hv['alle_identisch'] else 'NICHT identisch'}**", "",
     "| Kachel | Teil | identisch | Vertices | pos_sha256 (Ref) | pos_sha256 (Neu) | idx identisch | Farbe identisch |",
     "|---|---|---|---|---|---|---|---|"]
for t, x in hv["vergleich"].items():
    for art, v in x["teile"].items():
        L.append(f"| {t} | {art} | {'ja' if v['identisch'] else 'NEIN'} | {v['vertices']} | `{(v['ref_pos_sha256'] or '-')[:16]}…` | "
                 f"`{(v['neu_pos_sha256'] or '-')[:16]}…` | {'ja' if v['ref_idx_sha256'] == v['neu_idx_sha256'] else 'NEIN'} | {'ja' if v['farbe_identisch'] else 'nein'} |")
L += ["", "Zusätzlich im Build (Python): `neu.mesh.build_manifest()` erzeugt D1/G1/D2 erneut aus `relief_daten.json.gz`; "
      f"Kontrolle mit `neu.mesh.tile_mesh()`: {bi['prototyp_mit_tile_mesh_identisch']}.", "",
      f"Nahtprüfung (gemeinsame Randvertices benachbarter Kacheln): {bi['naht']['paare']} Paare, max. Höhendifferenz {bi['naht']['max_abs_m']} m.", "",
      "## Mesh-Hashes aller 56 Kacheln (Paket)", "", "| Kachel | Verfahren | surface_mode | Dreiecke | mesh_sha256 |", "|---|---|---|---|---|"]
for t, it in bi["kacheln_info"].items():
    L.append(f"| {t} | {it.get('verfahren','')} | {it['surface_mode']} | {it['triangles']} | `{it['mesh_sha256'][:16]}…` |")
Path(sys.argv[3]).write_text("\n".join(L) + "\n")
print(sys.argv[3])
