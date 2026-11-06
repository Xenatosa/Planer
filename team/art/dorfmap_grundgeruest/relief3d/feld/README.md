# Feld-3D-HTMLs (t82u)

Eine eigenständige HTML je Rasterfeld A1…H7 (8×7, raster_def.py). Szene = unveränderter Hauptviewer-Code (main.js, Handy-LOD lod=1), danach Ausschnitt Feld + 7 m Rand (Rand abgedunkelt).

- Bau: `cd relief3d && python3 feld/baue_feld_html.py /workspace/dorfmap_felder_3d [FELD ...]` → dorfmap_3d_feld_XX.html (2,0–3,5 MB).
- Daten: G/GB/VC/Feinband/Zellspalten außerhalb Feld+7 m+15 m Sicherheit auf 0 (nur Dateigröße). WV und WEGA bleiben ungekürzt (Wasser-/Wegebau wirkt über den Ausschnitt hinaus; mit Kürzung wich H7-Wasser ab). ALT-Welt und ihre Bodentextur entfallen.
- `FELD_VOLL=1` baut mit ungekürzten Daten (Prüfmodus, ~11,8 MB).
- Bedienung: 1 Finger drehen, 2 Finger zoomen/schieben; Buttons Clay/Textur, Umriss, Wege, Start. Hochformat: Startkamera weiter weg.
- Tests: `test_feld.js` (Ladezeit, JS-Fehler, Dreiecke, Screenshot), `vergleich_geometrie.js/.py` (Mesh-Dump gekürzt vs. ungekürzt), `vergleich_bild.js` (Feld vs. index.html?lod=1, gleiche Kamera), `test_bedienung.js` (Touch-Emulation 390×844).
- Bekannt: Schatten von Objekten außerhalb fehlen; Zäune/Randteile nach Dreieck-Schwerpunkt geschnitten; ferne Hintergrundobjekte (Wasserscheibe, Bergspitzen außerhalb der Karte) bleiben sichtbar; Ladezeit headless 4–9 s (Viewer baut erst die ganze Szene, dann Ausschnitt).
