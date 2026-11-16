# P13 – Haarlinien an Grat-/Hangsilhouetten (Kritiker P8, Befund S1)

> Nachtrag 16./17.11. (Basis 9d04f67, index.html über Pipeline, P13b D3) siehe unten.

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

---

# Nachtrag (Basis jetzt art/dorfmap-fertig @ 9d04f67, L3k #46 per Merge-Commit geholt)
Kosten Nachtrag: 0 € zusätzlich, Codex: nein (Dev UI selbst), Laufzeit: 23:36–00:10 MEZ, bau_endstand 2 Läufe (Übernahme + leerer Ordner) je ca. 8,5 min

## (2) index.html (D1/G1/D2): FrontSide
- Geändert: **`neu/viewer.js`** (+6/−1). Für index.html ruft `main.js` (Zeile 19, `RELIEF_NEU_VIEWER`) `renderNeuCore` aus `neu/viewer.js` auf. Dort sitzt das Gelände-Material der Kacheln D1/G1/D2. `main.js` selbst bleibt unverändert: bau_endstand baut es gepinnt aus 6e58af0, und sein eigenes Grobnetz-Material liegt im Legacy-Pfad hinter dem Return. Gleiche Lösung wie im 56-Kachel-Viewer: `FrontSide` + `shadowSide = DoubleSide`, **`?silh=0`** = alter Stand.
- Bundle/index.html **über die Pipeline** erzeugt: `UEBERNEHMEN=1 sh bau_endstand.sh` (esbuild 0.24.2 / three 0.170.0 aus /tmp/relief3d_bau_node, Schritt 4 baue_html, dann alle Schritte bis 20 L3k). In diesem Lauf waren 41 Ausgaben gleich, nur index.html und neu/index.html abweichend.
- **Neues Soll** (`nachtrag/soll_sha_index.json`): index.html und neu/index.html `f356c5a3dc2326be75d3a4bd136192dc98598192166b7f92e7d137ca188bac08` (9d04f67) → `69bbf5caa1886ec47418d8abb84be367dee10573e1f4591a24667b79b093a2df`. Das Soll ist der Repo-Stand; bau_endstand.sh selbst ist unverändert.
- bau_endstand.sh aus leerem Ordner: **ENDBAU BITGLEICH, 43/43** zum neuen Soll (522 s, `nachtrag/sha256_bau_p13_nachtrag.txt`).
- D2 und D1/G1 in index.html: Positionen und Indizes basis = P13 = P13 silh=0 (`nachtrag/idx_d2.json`). D2 im 56-Viewer: Positionen ebeb46a1/6835acf2/b33d5a64, Nahtnormalen 52eb1840, gleich wie 9d04f67 (`nachtrag/d2_hashes_9d04f67.json`).
- Bilder index.html, 12 Viertel-Kameras (30 m/35°) + 3 Übersichten (60 m): `?silh=0` ist 15 von 15 bytegleich mit index.html@9d04f67. Geänderte Pixel je Bild 0–74, Silhouetten-Dunkelpixel unter den geänderten **242 → 3**. Der Gesamtzähler sinkt nur 5051 → 4814, weil er in index.html von Häusern, Bäumen und Objektkanten dominiert wird (`nachtrag/zaehlung_index.json`). D1/G1/D2 haben weniger Grate, daher ist der Effekt dort kleiner als in B4/C4.
- 56-Kachel-Viewer auf 9d04f67 nachgemessen: `?silh=0` 15/15 bytegleich zur Basis, dunkle Linienpixel **4025 → 353** (`nachtrag/zaehlung_9d04f67.json`), weiterhin 0 Dreiecke nach unten und 0 offene Innenkanten.
- Gate 359/31/321, W1 0/0, Lochscan auf neuem index.html ok, Loch 0. Konsole ohne Fehler. P12c-Schalter `?wfeld=0`/`?wrand=0` wirken, ohne Fehler.

## (1) P13b: D3-Bachufer oben rechts → Ursache in den Daten, nicht geändert
- Ort: Die Stelle im Bild D3_U oben rechts ist der **E3-Kanal (L3i/L3j) bei x≈188, z≈97**. Die dunkle Linie ist 1 px breit und liegt am nahen Ufer, Bildpixel ~686|178.
- Der Dunkelpunkt-Zähler findet dort schon im Kritiker-Rohbild 0 Punkte (Ausschnitt 640–960×0–220), ebenso bei silh=0 und P13. Die 31 Rest-Pixel in D3_U sind Kanten der beiden Brücken; mit `ohne=wege` verschwinden sie.
- Luminanz-Transekt quer zum Bach (`nachtrag/p13b_d3_bachufer.json`), Wert in der Linie gegen das Schneeufer daneben:

  | Variante | Linie | Ufer daneben |
  |---|---|---|
  | normal | 119 | 165 |
  | ohne Wasser | 118 | 165 |
  | Wasser opak | Linie verdeckt | |
  | clay | 115 | 118 |
  | clay ohne Wasser | 114 | 118 |
  | silh=0 | wie normal | |
  | wfeld=0 | 124 | |
  | wrand=0 | 129 | |

  Rückseiten magenta: 0. Wasser FrontSide/BackSide: keine Wirkung.
- Raycast und Daten (z = 97,5): Die letzte nasse Ecke x=188,0 liegt bei GB −1,549 unter dem Spiegel WV −1,300, also **0,25 m tief direkt an der Uferlinie**. Die trockene Nachbarecke 187,5 liegt bei −1,238, nur 6 cm über dem Spiegel. Das ist eine Stufe von 0,31 m auf 0,5 m. Die Bett-VC ist dunkel (R 146/141) bis an die Wasserlinie, der Schnee daneben hat R 171/186.
- **Ursache: Daten** (Kanalprofil mit Uferstufe plus dunkle Bett-VC bis zur Wasserlinie). Die nahe Bachwand wird streifend gesehen und zeigt die dunkle Bettfarbe als 1-px-Linie; ohne VC ist sie kaum noch da. Der Wasserrand-Alpha aus P12c legt sie nur frei; Material, Seitenwahl, Z-Fighting und Tiefenblende sind es nicht.
- Vorschlag für Art Umgebung: Bett zur Wasserlinie auslaufen lassen (Tiefe an der letzten nassen Ecke gegen 0) oder die Bett-VC an den Uferecken aufhellen.

## Bilder Nachtrag
`/workspace/p13_nahbilder/nachtrag/`:
- `index_vorher/`, `index_nachher/`, `index_vergleich/` (Ausschnitte ×4.5)
- `alle56_9d04f67_vorher/`, `alle56_9d04f67_nachher/`
- `p13b_d3/`: D3_U-Varianten base/ow/owe/wf0/wr0/wb/wfr/wbk/web/mag/s0/clay/clayow, `d3_montage.png`, `d3_zoom*.png`, `d3_rest.png` (Brückenkanten), `D3_U_transekt_x4.png`
