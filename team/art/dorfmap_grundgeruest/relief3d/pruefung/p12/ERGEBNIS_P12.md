# P12 – Normalen über Kachelnähte gemeinsam (56-Kachel-Viewer + index.html)

Branch `devui/dorfmap-p12`, Basis ist P11b-v2 (`devui/dorfmap-p11b-v2`, PR #23, 0316b65 auf d5b17e2). **Abhängigkeit:** erst nach #23 mergen, weil `bau_endstand.sh` aus P11b-v2 gebraucht wird.

## Ursache gemessen
`computeVertexNormals()` läuft je Kachel. Ein Randvertex sieht deshalb nur die Dreiecke seiner eigenen Kachel, und links und rechts der Naht entstehen verschiedene Normalen. Das ergibt bei gleicher Höhe eine harte Helligkeitslinie (QA P4c).

Messung: `pruefung/p12/naht_messung.mjs` misst den Winkel zwischen den Normalen beider Kacheln am selben Nahtpunkt, vorher und nachher. Ausgaben: `naht_messung_56.json` und `naht_messung_index.json`.

| Paket | Nahtpaare | Punkte | vorher max | vorher >1° / >5° | nachher max | nachher >1° / >5° |
|---|---:|---:|---:|---:|---:|---:|
| 56 Kacheln | 181 (inkl. Eckpunkte) | 8455 | 95,8° | 3019 / 1216 | 0,023° | 0 / 0 |
| index.html (D1/G1/D2) | 1 (D1\|D2) | 85 | 4,13° | 17 / 0 | 0,02° | 0 / 0 |

QA-Nähte:

| Naht | max | mittel | >5° | Ort | nachher |
|---|---:|---:|---:|---|---:|
| C4\|D4 (x = 126) | 36,4° | 6,6° | 38 | 126/150,5 | 0,02° |
| B6\|C6 (x = 84) | 27,2° | 2,5° | 13 | 84/224 | 0,02° |

Die Nähte sind kartenweit betroffen: 108 von 181 Nahtpaaren haben Punkte über 1°, 86 über 5°.

Die 10 stärksten Nähte (vorher max, mittel, Punkte >5°, Ort, nachher max):

| Naht | max | mittel | >5° | Ort | nachher |
|---|---:|---:|---:|---|---:|
| D6\|D7 | 95.794 | 12.453 | 32 | [160.5, 258] | 0.02 |
| A1\|A2 | 71.935 | 10.532 | 56 | [24, 43] | 0.022 |
| C5\|C6 | 67.758 | 5.992 | 29 | [90, 215] | 0.021 |
| B4\|C4 | 52.691 | 7.781 | 33 | [84, 134] | 0.019 |
| B1\|B2 | 48.232 | 9.919 | 43 | [58.5, 43] | 0.022 |
| E6\|E7 | 47.598 | 6.55 | 18 | [173, 258] | 0.019 |
| G3\|H3 | 45.617 | 4.394 | 16 | [294, 96.5] | 0.02 |
| D3\|D4 | 45.328 | 2.423 | 7 | [127.5, 129] | 0.019 |
| B5\|B6 | 44.405 | 4.072 | 19 | [83, 215] | 0.019 |
| F7\|G7 | 43.188 | 3.933 | 17 | [252, 266] | 0.019 |

## Umsetzung
`neu/naht_normalen.js` (`nahtNormalen`):
- Für die Randvertices aller Kacheln werden die flächengewichteten Dreiecksnormalen summiert, so wie three.js es macht. Schlüssel ist der Gitterpunkt; zusammengeführt wird nur bei gleicher Höhe (≤ 1e-4).
- Danach wird normiert und in die `normal`-Attribute zurückgeschrieben.
- Innere Vertices bleiben unverändert (geprüft).
- Positionen und Indizes bleiben unverändert.

Aufrufer:
- `pruefung/alle_kacheln/viewer_alle.js` (56 Kacheln, 16574 Randvertices).
- `neu/viewer.js` (index.html, D1/D2: 170 Randvertices; G1 hat keinen Nachbarn).

Schalter `?nahtnormalen=0`: alter Zustand, er dient den Vorher-Bildern. Die alten index.html-Normalen sind gleich `?nahtnormalen=0` (Hash geprüft).

## Bundle / Endbau
- Neu ist nur das Bundle in `index.html` und `neu/index.html` (neu/viewer.js über main.js@6e58af0, esbuild 0.24.2 gepinnt). Die Datenzeile NEU_GZ ist bytegleich.
- Bundle-sha256 (`pruefung/p12/bundle_sha.py`): alt `53dbc78c963dc0b682ba164658738d1854d545ab9fd9b047356da45b8db48a0a`, neu `21f9a79951bd4a6e8a2ba8ca73a5f6e17518933115b10c67302c00a574f6dab1`.
- index.html: `1819a14032aa38726b2991c3b73e079b0c560eb6efaafda58f5e1013fccee2be` (vorher 2a2e9aa7…).
- `bau_endstand.sh`: Bau 1 mit UEBERNEHMEN=1 weicht nur in index.html und neu/index.html ab. Bau 2 aus leerem Ordner liefert danach alle 20 Ausgaben bitgleich.

## Nachweise
- **Gate je Regel und Trefferliste** identisch zu P11b-v2: 374 / 33 / 325 / W1 0 / W1-56 0. Das Gate liest Geometrie und Daten; Normalen gehen nicht ein.
- **D2:** Geometrie bitgleich, Positionen surface/sides/bottom = ebeb46a1 / 6835acf2 / b33d5a64.
  - **Geändert sind nur die Normalen von terrain_surface_D2** (3bf24e5f → db48c52f), und zwar an den 85 Randvertices der Naht D1|D2.
  - Ebenso D1 surface (0b6eea17 → b1d637ae).
  - sides und bottom sowie G1 sind unverändert. Details: `d2_hashes.json`.
- **Nahbilder** liegen in `/workspace/p12_nahbilder/` (nicht eingecheckt): Ton und Farbe, `nosh=1`, ohne Kachelrand, je vorher (`?nahtnormalen=0`) und nachher. Sammelblätter in `vergleich/`, Differenzbilder `diff8x_ton_*`.
  - C4/D4 von Süden (z 140 und 150): Die harte senkrechte Helligkeitslinie am Hang bei x = 126 ist nachher weg.
  - B6/C6 (z 224, von Süden und Westen): Die Linie in der Mulde ist nachher weg.
  - Von Osten (Blick entlang der Naht) ist vorher wie nachher kaum ein Unterschied zu sehen, wie erwartet.
  - Die Differenzbilder zeigen Änderungen nur in schmalen Streifen entlang der Nähte.
  - D1|D2 in index.html (max 4°): im Bild unter einer Graustufe Unterschied.
- Konsolenfehler: keine. `window.__nahtNormalen` meldet 16574 (56 Kacheln) bzw. 170 (index.html) geänderte Randvertices.
