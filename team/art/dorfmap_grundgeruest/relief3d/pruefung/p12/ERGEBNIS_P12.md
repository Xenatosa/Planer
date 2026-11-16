# P12-v3 – Normalen über Kachelnähte gemeinsam (56-Kachel-Viewer + index.html)

Branch `devui/dorfmap-p12-v3`, Basis `art/dorfmap-fertig` @ `a3eaefe` (P11b-v3, #27 gemergt). Ersetzt #24 (alter Stand auf P11b-v2).
Codeänderungen aus #24 übernommen (`neu/naht_normalen.js`, `neu/viewer.js`, `viewer_alle.js`, Messskripte); Daten **nicht** gemergt,
sondern mit `bau_endstand.sh` neu erzeugt.

Kosten: 0 € zusätzlich, Codex: nein (Dev UI selbst), Laufzeit: bau_endstand 395 s (Bau 2) / Arbeitszeit ca. 1 h

## Ursache
`computeVertexNormals()` läuft je Kachel; ein Randvertex sieht nur die Dreiecke seiner Kachel → zwei verschiedene Normalen am
selben Punkt bei gleicher Höhe → harte Helligkeitslinie auf der Naht (QA P4c).

## Umsetzung
`neu/naht_normalen.js` (`nahtNormalen`): für Randvertices aller Kacheln die flächengewichteten Dreiecksnormalen (wie three.js)
über alle Kacheln summieren, die denselben Gitterpunkt bei gleicher Höhe (≤ 1e-4) teilen, normieren, zurückschreiben.
Innenvertices, Positionen und Indizes unverändert (geprüft: 0 Innenkomponenten geändert).
Aufrufer: `pruefung/alle_kacheln/viewer_alle.js` (alle 56, 16574 Randvertices) und `neu/viewer.js` (index.html, D1|D2: 170).
`?nahtnormalen=0` = alter Stand (Vorher-Bilder).

## Messung (`pruefung/p12/naht_messung.mjs`, Stand a3eaefe)
| Paket | Nahtpaare | Punkte | vorher max | vorher >1° / >5° | nachher max | nachher >1° / >5° |
|---|---:|---:|---:|---:|---:|---:|
| 56 Kacheln | 181 | 8455 | 95,8° (D6\|D7) | 3003 / 1182 | 0,023° | 0 / 0 |
| index.html (D1\|D2) | 1 | 85 | 4,13° | 17 / 0 | 0,02° | 0 / 0 |

QA-Nähte: C4\|D4 (x=126) 36,4° → 0,02°; B6\|C6 (x=84) 27,2° → 0,02°. Kartenweit: 108 von 181 Nahtpaaren > 1°, 86 > 5°.
Details: `naht_messung_56.json`, `naht_messung_index.json`.

## Bundle / Endbau
- Neu ist nur das Viewer-Bundle in `index.html` und `neu/index.html` (main.js@6e58af0 + neu/viewer.js, esbuild 0.24.2).
  Teil vor und nach dem Bundle (Daten, NEU_GZ) bytegleich. Bundle-sha256 (`bundle_sha.py`):
  alt `53dbc78c…48a0a` → neu `21f9a79951bd4a6e8a2ba8ca73a5f6e17518933115b10c67302c00a574f6dab1` (= Bundle aus #24).
- Neue Soll-sha256: `index.html` = `neu/index.html` = `bb57def902fe2ad561be91623aad652d67b156733834bc08b6a4ceea399f73e0`
  (vorher 995a2764…). Alle übrigen 23 Ausgaben unverändert. Volle Liste: `sha256_bau2.txt`.
- Bau 1 (`UEBERNEHMEN=1`) wich nur in index.html/neu/index.html ab; Bau 2 aus leerem Ordner: 25/25 bitgleich (395 s).
- Bau-Toolchain: `bau/package.json` zusätzlich `playwright 1.65.1` (für den Gate-Lochscan, s. u.); esbuild 0.24.2 / three 0.170.0 unverändert.

## Gate (Lauf ohne NODE_PATH)
Je Regel **und** Trefferliste identisch zum Gate auf a3eaefe (gleicher Lauf mit index.html@a3eaefe):
regeln 372, r8 31, r9 325, W1 0, W1-56 0, G1_loch_offen 0 (Lochscan lief). `regeln_letzter_lauf.json` damit von 371 auf den
aktuellen Lauf 372 nachgezogen (Normalen gehen nicht ins Gate).

## export_gate.sh: Lochscan ohne NODE_PATH
Vorher scheiterte `loch_o18g.js` ohne NODE_PATH stumm (Ausgabe nach /dev/null, Treffer `G1_lochscan_fehlt`). Jetzt:
NODE_PATH standardmäßig `${NODE_BAU:-/tmp/relief3d_bau_node}/node_modules`; fehlt dort playwright → `GATE ABBRUCH` mit Anleitung, exit 2;
scheitert der Scan oder bleibt die Datei leer → `GATE ABBRUCH` mit Log-Auszug, exit 2. Prüfer und Schwellen unverändert.
Beleg: ohne NODE_PATH läuft das Gate (G1 0); mit `NODE_BAU=<leer>` bricht es sichtbar ab (exit 2). `test_export_gate_lochscan.sh` grün.

## D2
**D2: Positionen bitgleich, Nahtnormalen bewusst geändert (3bf24e5f → db48c52f)** (vom Eigner bestätigt).

Beleg Inneres pixelgleich (`pruefung/p12/d2_innen_bild.js`, Bilder in `pruefung/p12/ergebnis/` und `/workspace/p12_nahbilder/d2_innen_*`):
D2-Fläche abseits der Naht (Kamera 147/y+22/54 → Ziel 147/74, Naht z = 43 hinter der Kamera), index.html@a3eaefe vs. @d301315,
gleiche Kamera, 1024 × 768: **0 abweichende Pixel** mit Schatten und mit `nosh=1`. Positivkontrolle mit Blick auf die Naht D1|D2:
2558 abweichende Pixel (max. 1 Tonwert), d. h. der Vergleich erkennt die Nahtänderung.

Positionen surface/sides/bottom = `ebeb46a1` / `6835acf2` / `b33d5a64` (unverändert). **Geändert sind nur die Normalen von
terrain_surface_D2** (`3bf24e5f` → `db48c52f`, 85 Randvertices der Naht D1|D2), ebenso D1 surface (`77eafb20` → `50b32f1f`).
G1, sides, bottom unverändert. `?nahtnormalen=0` = Basis a3eaefe (Hash). Details `d2_hashes.json`.

## Nahbilder (`/workspace/p12_nahbilder/`, nicht eingecheckt)
Ton und Farbe, `nosh=1`, ohne Kachelrand, vorher (`?nahtnormalen=0`) / nachher; Vergleichsblätter und 8×-Differenzbilder in `vergleich/`.
- C4/D4 von Süden (z 140, 150): harte senkrechte Hell-dunkel-Kante am Hang bei x=126 nachher weg.
- B6/C6 (z 224): senkrechte Linie in der Mulde und die waagerechte Linie oben links (z-Naht) nachher weg.
- Blick entlang der Naht (Ost/West): kaum Unterschied, wie erwartet. Differenzen nur in schmalen Streifen an den Nähten.
