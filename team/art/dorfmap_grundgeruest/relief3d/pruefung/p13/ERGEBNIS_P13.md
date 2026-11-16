# P13 – Haarlinien an Grat-/Hangsilhouetten (Kritiker P8, Befund S1)

Basis: art/dorfmap-fertig @ cc33fd1. Geändert: nur `pruefung/alle_kacheln/viewer_alle.js` (+7/−1), neu `pruefung/p13/`.
Kosten: 0 € zusätzlich, Codex: nein (Dev UI selbst), Laufzeit: bau_endstand 500 s / Arbeitszeit ca. 30 min

## Ursache (gemessen)
Die gepunktete dunkle 1-px-Linie besteht aus **Rückseiten des Geländes**. Das Oberflächenmaterial ist `side: DoubleSide`. An jeder Silhouette (Grat oder Hangkante, hinter der das Gelände abfällt) stoßen nach vorn und nach hinten gewandte Dreiecke mit gleicher Tiefe an derselben Kante zusammen. Einzelne Kantenpixel gewinnt dabei die Rückseite. Bei DoubleSide wird ihre Normale umgedreht, sie ist also nach unten beleuchtet und erscheint dunkel.

Belege (Kritiker-Kameras nachgestellt, 960×680 nativ PNG, SwiftShader, nosh=1):
- **Rückseite magenta** (FrontSide-Original plus BackSide-Kopie in Magenta): 94–98 % der dunklen Linienpixel liegen genau auf Magenta-Pixeln. B4_Q2: 543 von 558, B4_Q4: 485/512, C4_U: 341/380, G3_U: 146/153, H2_U: 58/59; D3_U: 76/107, der Rest dort ist der Bachrand. Siehe `rueckseite_beleg.json` und die Bilder unter `diagnose/`.
- **Nur FrontSide**: dunkle Pixel 558 → 17 (B4_Q2), 512 → 32, 380 → 49, 153 → 7, 59 → 5.
- **T-Stöße/Rasterlücken ausgeschlossen**: alle 56 Oberflächen, 814 464 Dreiecke, davon 0 nach unten gerichtet. 19 104 offene Kanten, 0 davon außerhalb des Kachelrands, also keine T-Stöße im Netz. Die Nähte sind laut Build mit max_abs 0,0 m geschlossen. Mit Clear-Farbe Rot gibt es 0 rote Pixel im Gelände, auch ohne Seiten/Boden. Rot erscheint nur im Himmel am Bildrand von G3_U/H2_U, und zwar identisch mit und ohne Seiten/Boden. Siehe `diagnose.json`.
- **Kein reines SwiftShader-/AA-Artefakt**: MSAA ist aktiv (antialias true, 4 Samples), die Linie entsteht trotzdem. Mit 2× Auflösung (DPR 2, wie ein Handy) bleibt sie als 1-Geräte-px-Linie (B4_Q2: 1384 dunkle px bei 2×, FrontSide 15). Erst ein Verkleinern auf 1× mittelt sie weg (13). Der Mechanismus ist Tiefengleichstand von Vorder- und Rückseite an der Kante und hängt nicht vom Renderer ab. Auf echter GPU ist er daher wahrscheinlich ebenfalls sichtbar, je nach Rasterregeln eventuell schwächer. Auf einem Gerät **nicht geprüft**.

## Behebung (nur Viewer)
`terrainMaterial.side = FrontSide`. Dazu `shadowSide = DoubleSide`, damit die Schattenkarte gleich bleibt. Seiten/Boden/Wände/Wasser bleiben unverändert. Schalter: **`?silh=0`** = alter Stand. Er ist bytegleich zu cc33fd1: 15 von 15 PNGs dateigleich mit dem Basis-Viewer. P12c-Schalter `?wfeld=0` und `?wrand=0` wirken weiter (Bild ändert sich, keine Konsolenfehler). `main.js`/`index.html` sind nicht angefasst: Eine Änderung dort würde `index.html` und damit bau_endstand ändern.

## Messwerte
- Dunkle Linienpixel (Luminanz < Median 5×5 − 30 bei Median > 120), 15 Kritiker-Kameras: **Summe 4041 → 360 (−91 %)**. Je Bild in `zaehlung.json`, z. B. B4_Q2 558 → 17, B4_Q4 512 → 33, C4_Q1 451 → 33, C4_U 380 → 49, G3_Q2 250 → 0, H3_U 208 → 4, G3_U 153 → 7, H2_U 59 → 5, C5_U 332 → 68, D3_U 107 → 31.
- Geänderte Pixel je Bild 214–1872, deckungsgleich mit den Magenta-Rückseitenpixeln (B4_Q2: 1832 geändert, 1829 magenta). Sonst ändert sich nichts am Bild.
- Mit Schatten (ohne nosh) identisch: B4_Q2 556 → 17, G3_U 162 → 15, H2_U 59 → 5, gleiche Zahl geänderter Pixel (`zaehlung_schatten.json`).
- Gate 359/31/321 = Soll, W1 0/0, Lochscan ok, Loch 0 (`gate_lauf.json`).
- D2: Positionen ebeb46a1/6835acf2/b33d5a64 und Normalen 52eb1840/98f2e596/18aaf4e1, identisch Basis = P13 = P13 mit silh=0 (`d2_hashes.json`).
- vektor.json, zellen_relief.csv, felder.json, gen_relief.py, index.html, neu/index.html unverändert.
- bau_endstand.sh: ENDBAU BITGLEICH – 41/41 Dateien gleich zum Basis-Soll cc33fd1 (`sha256_bau_p13.txt`).
- Konsole: keine Fehler/Warnungen (alle Läufe).

## Bildbefunde (ehrlich)
- B4 (Grat 76|140–84|129), C4, B5, C5, H3/H4, G3-Grat, H2-Randgrat: Die gepunktete Bleistiftkontur ist weg, aus 30 m und in der Übersicht. Die Silhouetten sind jetzt glatte Kanten aus Hell gegen Hell.
- Was bleibt: Die Silhouettenkanten zeigen normale Treppchen der MSAA-Kantenglättung. An einzelnen Stellen (C5_U links oben, C4_U, B5_U) liegt ein weicher, leicht olivgrauer Saum, wo der Hang streifend zur Kamera steht. Das ist Schattierung, keine Pixelpunkte. Die verbleibenden 4–68 Zählerpixel je Bild sind Einzelpunkte an steilen Kanten, Textur-/VC-Flecken und die Tile-Randlinie in den U-Bildern.
- **D3-Bachufer rechts oben: nicht behoben.** Die dunkle Randlinie am Bach ist vorher und nachher gleich. Sie ist ein Wasser-/Bettrand und gehört nicht zum Rückseiten-Befund S1 (dort 76 von 107 dunklen Pixeln Rückseiten an der Hangkante links unten, die sind weg).
- main.js (index.html, Prototyp D1/G1/D2) hat dasselbe DoubleSide. Dort ist es nicht geändert, weil das bau_endstand ändern würde. Ein eigener Auftrag wäre nötig, falls diese Ansicht relevant ist.

## Bilder
`/workspace/p13_nahbilder/`: `vorher/` (?silh=0), `nachher/`, `vergleich/` (Ausschnitte ×3 vorher|nachher, `*_nachher_rest_markiert.png` mit verbleibenden Zählerpixeln rot, `D3_U_bachufer_rechtsoben_x2.png`), `sh_vorher/` und `sh_nachher/` (mit Schatten), `diagnose/` (Rückseite magenta, nur FrontSide, B4_Q2-Ausschnitte).

## Werkzeug
`werkzeug/render_p13.js` (Kritiker-Kameras, MODE=magenta|front|nofund nur mit Diagnose-Build `window.__dbg`), `zaehl.py`, `vgl.py`, `d2h.js`. Der Diagnose-Build wurde nur temporär erzeugt und ist nicht im Commit.
