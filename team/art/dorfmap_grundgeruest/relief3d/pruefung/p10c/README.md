# P10c – Einheitenfix Wandkörper (`neu/wand.py`)

Basis `art/dorfmap-fertig` @ 7944b33. Freigabe durch Dorfmap-Grundgerüst (Einheitenfehler bestätigt).

## Einheiten-Beleg
- `neu/vektor.py` schreibt Wände in **Metern**: `mittellinie_m` = `(Zelle + 0,5) · CELL_M`, `breite_min_m = CELL_M` (Z. 336–346).
  Maximum in `vektor.json`: x 402,69 / z 311,49 m = Karte 336 × 1,2 = 403,2 m.
- Das Geländemesh rechnet in **Zellen**: `mesh.TILE_BOUNDS` (D1 = 126–168 / 0–43), `tile_mesh`-Vertices D1 x 126,0–168,0;
  `mesh.py` teilt Weg-Mittellinien bereits durch `CELL_M` (Z. 477 `line /= CELL_M`).
- Höhe (y) ist in beiden Fällen Meter (Gelände y 0–14 m); nur x/z waren vertauscht.
- Andere Stellen geprüft: `neu/objekte.py` (Objekte aus `relief_daten.json.gz` liegen in Zellen, x max 335,7 ≤ 336 →
  kein Fehler, unverändert); `neu/viewer.js` zeichnet Wandvertices 1:1 (keine Umrechnung, unverändert);
  `mesh.py`-Wegprofile rechnen bereits korrekt. Betroffen war nur `neu/wand.py`.

## Fix (eine Einheit: Zellen)
`neu/wand.py`: `_centerline_cells()` = `mittellinie_m / CELL_M`; `_chunks` clippt in Zellen (Rand = Breite/CELL_M·1,05);
`build_wall_manifest` baut Körper mit `width / CELL_M` (Breite 1,2 m = 1 Zelle); gemeldete Breiten bleiben in Metern.
`pruefung/alle_kacheln/baue_alle_kacheln.py` (Wände für alle 56 Kacheln) folgt derselben Umrechnung.

## Artefakte neu eingesetzt
`neu/pipeline.py` lässt sich auf 7944b33 nicht ausführen (unabhängig vom Fix): seit a10fc1e (P3) passt
`relief_daten.json.gz` (sha bfed8424…) nicht mehr zur `source_relief_sha256` der p3d17-Rasterlösung (5e8fdb51…).
Daher `pruefung/p10c/waende_einsetzen.py`: liest `neu/relief_neu.json.gz`, baut nur `waende` (+ lod1-Wandzahl) mit
`build_wall_manifest(terrain_tiles=gespeicherte Kacheln)` neu, ersetzt in `index.html`/`neu/index.html` nur die
NEU_GZ-Zeile (Bundle bytegleich, wie P3 `html_payload_p3.py`). Kontrollen: Neu-Serialisierung bytegleich = True;
mit dem alten `wand.py` (git stash) sind D1/G1/D2-Wände hash-gleich zum Stand 7944b33; alle anderen Manifest-Schlüssel unverändert (assert).

| Kachel | Wand-Dreiecke vorher → nachher | mesh_sha256 vorher → nachher |
|---|---|---|
| D1 | 19920 → 16544 | `f6bf913146145b57` → `9a9290710ae39c86` |
| G1 | 25668 → 25004 | `7eb137e59af31eca` → `ed2ceab591366384` |
| D2 | 0 → 0 | `e3b0c44298fc1c14` → `e3b0c44298fc1c14` |

D2: Gelände (surface/sides/bottom) und Wände bitgleich (`ergebnis/hash_index_vorher_nachher.json`, Wand leer = sha256 des leeren Puffers `e3b0c442…`).
D2 bekommt jetzt auch ohne die Pipeline-Sonderregel keine Wandstücke mehr (vorher 2 unterdrückte Abschnitte, nachher 0).

## Wandstatistik (`ergebnis/wand_herkunft_*.json`, alle 56 Kacheln)
| | vorher | nachher |
|---|---|---|
| Wände ganz außerhalb der Karte (von 260) | 97 | 0 |
| Abstand Wandlinie → eigene Quellzellen, Median / Max (Zellen) | 53.38 / 82.69 | 0.23 / 0.26 |
| Kacheln mit Wandstücken / Stücke / kürzer 5 / Enden an Clipkante | 35 / 201 / 75 / 108 | 35 / 299 / 148 / 122 |
| Klippe ohne Wand (Klippenzellen) | H2 (122), B3 (1), G3 (366), H3 (633), A4 (17), G4 (407), B5 (126), E5 (64), H5 (596), A6 (239), B6 (208), G6 (788), H6 (507) | B2 (31), C2 (30), F2 (30), B3 (1) |
| Wand ohne Klippe (Stücke) | D2 (2), G2 (3), A7 (1), B7 (4), D7 (12), E7 (3), F7 (13), G7 (5), H7 (12) | – |
| Wandvertices über Gelände (+0,1 m) / gesamt | 102605 / 359574 | 73251 / 525676 |

Klippe ohne Wand nachher: B2/C2/F2 sind die Ränder des Nord-Bands (z 43–46); deren Wand-Mittellinie liegt in Reihe 1
und endet an der Clipkante (keine dieser Zellen ist Quellzelle einer Wand). B3: 1 Zelle.

## Befund Höhenbezug (`ergebnis/wand_hoehenbezug.json`, nicht geändert)
`vektor.py` nimmt `hoehe_oben_m` aus `zellen_relief.csv` `hoehe_m` (max 8,6 m); das sichtbare Gelände GB reicht von −20,4 bis 14,0 m.

| Familie | Wände | oben (Median) | oben − GB-Krone (Median) | oben unter Krone | oben > 8 m über GB-Fuß |
|---|---|---|---|---|---|
| Nord | 71 | 8.6 | -5.4 | 100% | 7% |
| Suedgrat | 68 | 0.0 | 0.89 | 7% | 83% |
| Krater | 37 | 0.0 | -9.34 | 100% | 0% |
| Ostgrat | 72 | 6.54 | -5.3 | 100% | 0% |
| unbenannt | 12 | 0.0 | 0.93 | 24% | 34% |

Folge: Nord/Ostgrat/Krater-Wände liegen jetzt an der richtigen Stelle, aber vollständig im Gelände (D1, G1 u. a.:
0 Vertices über Gelände, `ergebnis/wand_sichtbar.json`). Suedgrat/unbenannt reichen von der Krone bis zum
Canyonboden (bis ~16 m sichtbar, z. B. C6, D6, G6). Die Höhenprofile gehören in `vektor.py`/`vektor.json` (nicht Teil von P10c).

## Gate
Unverändert in allen Regeln (`ergebnis/gate_vergleich.md`), regeln 476, r8 48, r9 334, G5 68, G7 1, G7b 24+1+1.
Grund: Kein Prüfer sieht Wandkörper. `pruefe_regeln.py` bildet WAND aus der GB-Steilheit (Z. 9), G5/G7/G7b messen
das Höhenfeld, `loch_o18g.js` nur Ebene `gelaende`; `relief_daten.json.gz` ist unverändert. Der alte Fehler war
für das Gate daher unsichtbar und der Fix ebenso.

## Befehle (relief3d/)
```sh
python3 pruefung/p10c/waende_einsetzen.py --pruefen      # nur vergleichen
python3 pruefung/p10c/waende_einsetzen.py                # relief_neu.json.gz + index.html neu einsetzen
sh pruefung/p10c/gate_eigene_pfade.sh index.html /tmp/p10c/nachher
python3 pruefung/trefferkarte/trefferkarte.py --regeln /tmp/p10c/nachher/regeln_letzter_lauf.json --r8 /tmp/p10c/nachher/r8_letzter_lauf.json --r9 /tmp/p10c/nachher/r9_letzter_lauf.json --vorher /tmp/p10c/vorher --aus /tmp/p10c/trefferkarte
python3 pruefung/alle_kacheln/baue_alle_kacheln.py --out /tmp/p10c/alle_nachher   # ~7 min
KONTROLLE=C3 sh pruefung/alle_kacheln/lochscan_alle.sh /tmp/p10c/alle_nachher
python3 pruefung/alle_kacheln/wand_herkunft.py; python3 pruefung/p10c/wand_hoehenbezug.py
```
