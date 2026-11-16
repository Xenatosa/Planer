#!/usr/bin/env python3
"""P10b: Was ist je Kachel dargestellt (aus dem Browser, darstellung.json) und was liegt in den Daten
(Kennzahlen aus alle_kacheln_build.json)? Schreibt Markdown.
Aufruf: python3 pruefung/alle_kacheln/darstellung_bericht.py /tmp/p10b/nahbilder/darstellung.json /tmp/p10b/alle_kacheln_build.json OUT.md"""
import json, sys
from pathlib import Path

d = json.loads(Path(sys.argv[1]).read_text())
b = json.loads(Path(sys.argv[2]).read_text())
k = b["kennzahlen"]
L = ["# P10b Darstellung je Kachel", "",
     "Spalten links = im Viewer gezeichnet (Dreiecke je Ebene, aus `__test.darstellung()`), rechts = Quelldaten:",
     "`WEGA>0` / `WV>-900` = Vertices des 0,5-m-Gitters in `relief_daten.json.gz`; `vektor` = Wege-Mittellinien / Wasserpolygone / Wand-Abschnitte",
     "aus `neu/vektor.json`, die die Kachel schneiden; `Klippe` = Zellen mit `klippe` WAND/KANTE in `raster_c20_z25_zellen.csv`;",
     "`Profil` = von `neu.mesh.terrain_heights()` geänderte Geländevertices.", "",
     "| Kachel | Gelände | Wand | Wege | Wasser | Brücken | WEGA>0 | WV>-900 | vektor Wege | vektor Wasser | vektor Wand | Klippe WAND | Klippe KANTE | Profil |",
     "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
summe = {x: 0 for x in ("wand_dreiecke", "wege_dreiecke", "wasser_dreiecke", "bruecken")}
for t in [f"{c}{r}" for r in range(1, 8) for c in "ABCDEFGH"]:
    x, y = d.get(t, {}), k[t]
    for s in summe:
        summe[s] += x.get(s, 0)
    L.append(f"| {t} | {x.get('gelaende_dreiecke', '-')} | {x.get('wand_dreiecke', 0)} | {x.get('wege_dreiecke', 0)} | {x.get('wasser_dreiecke', 0)} | {x.get('bruecken', 0)} | "
             f"{y['wega_vertices']} | {y['wv_vertices']} | {y['vektor_wege']} | {y['vektor_wasser']} | {y['wand_chunks']} | {y['klippe_WAND_zellen']} | {y['klippe_KANTE_zellen']} | {y['wegprofil_vertices']} |")
n = lambda key: sum(1 for t in d.values() if t.get(key, 0) > 0)
L += ["", f"Kacheln mit Wandkörper: {n('wand_dreiecke')} ({summe['wand_dreiecke']} Dreiecke) · mit Wege-Overlay: {n('wege_dreiecke')} ({summe['wege_dreiecke']}) · "
      f"mit Wasser: {n('wasser_dreiecke')} ({summe['wasser_dreiecke']}) · Brücken: {summe['bruecken']}", "",
      f"Kacheln mit Klippenzellen (WAND oder KANTE): {sum(1 for y in k.values() if y['klippe_WAND_zellen'] + y['klippe_KANTE_zellen'] > 0)} · "
      f"mit vektor.json-Wandabschnitten: {sum(1 for y in k.values() if y['wand_chunks'] > 0)}", "",
      "Klippen ohne Wandkörper (Klippenzellen > 0, aber keine Wand-Dreiecke): " +
      (", ".join(f"{t} ({k[t]['klippe_WAND_zellen']}+{k[t]['klippe_KANTE_zellen']})" for t in k if k[t]['klippe_WAND_zellen'] + k[t]['klippe_KANTE_zellen'] > 0 and d.get(t, {}).get('wand_dreiecke', 0) == 0) or "keine"),
      "", "Wandkörper ohne Klippenzellen: " +
      (", ".join(t for t in k if k[t]['klippe_WAND_zellen'] + k[t]['klippe_KANTE_zellen'] == 0 and d.get(t, {}).get('wand_dreiecke', 0) > 0) or "keine"),
      "", f"D2: vektor.json hat {k['D2']['wand_chunks']} Wandabschnitte; die Pipeline (`neu/wand.py`) lässt D2 bewusst wandfrei "
      f"(unterdrückt: {b.get('waende_d2_unterdrueckt')}); sichtbar mit `?d2wand=1`."]
Path(sys.argv[3]).write_text("\n".join(L) + "\n")
print(sys.argv[3])
