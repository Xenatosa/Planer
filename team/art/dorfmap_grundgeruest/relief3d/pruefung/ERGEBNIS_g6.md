# Ergebnis G6 (TAG g6)

Stand: Basis-Commit `d3843dc` (`art/dorfmap-grundgeruest`), Branch `art/dorfmap-g6`. Ausgabe erzeugt am 03.11.2026 mit dem Standard `FALTVWD=2.0`.

## Ergebnis

- `G6_facette`: **220 → 195** (−25 Treffer, −11,4 %). Die Senkung ist real, aber 195 Treffer bleiben; eine konkrete Zielzahl unterhalb davon war nicht vorgegeben.
- `pruefe_regeln.py`: **570 → 543** (−27); größte Regelzunahme `G11_objekt_schwebt_sinkt` **0 → 3**. Keine Regel steigt um mehr als 5.
- R8: **48 → 48**; R9: **334 → 334**. Raycast: **0** offene Innenkanten. t42u: **Summe 0**.
- lod1: **1.174.554** gerenderte Dreiecke, unter 1,3 Mio. `export_gate.sh` meldet weiterhin `GATE ROT`, weil es bei jedem noch vorhandenen Treffer rot bleibt; der Basisstand hatte bereits 570 Prüftreffer. Die Schwellen wurden nicht geändert.
- D2: G, GB und die Feinbanddaten im D2-Bereich sind bytegleich zum Artefakt von `d3843dc`; keine neuen Prüftreffer in D2.

## Änderung

`gen_relief.py` behält die vorhandene Grobmaske in `_falten_glatt` bei und ergänzt eine Maske aus der tatsächlich sichtbaren Grob-/Feinband-Mischfläche. Die zusätzliche Glättung wirkt auf Hangflächen mit Normalensprüngen; Wandabstand, Wege, Wasser und Rampenenden bleiben ausgespart. `FALTVWD` steuert den Wandabstand der neuen Feinmaske: Standard 2,0 m, getestete Alternative 3,0 m. Die neue Maske wird in einem 2-m-Saum um D2 ausgeschaltet. Die alte Grobwirkung in D2 bleibt unverändert, weil sie zum Basisresultat gehört.

Im nachgelagerten `_hangwellen_glatt` wird nach der Distanztransformation das berechnete Gewicht im D2-Feld auf null gesetzt. Die Auswahlmaske allein sperrte D2 nicht, da die Distanztransformation auch innerhalb ausgeschlossener Zellen positive Gewichte liefert. Das behebt den Übergriff an der Naht an seiner verursachenden Stufe.

`pruefung/export_gate.sh` akzeptiert `TAG` und `LOCHSCAN`, damit alle Prüfausgaben in eigene `/tmp/*_g6.json`-Dateien gehen. Prüfer und Schwellenwerte blieben unangetastet. `relief_daten.json.gz` und das eingebettete Relief in `index.html` stammen aus dem finalen Neubau. `zellen_relief.csv`, Overlay und `../referenz/*` sind unverändert.

## Werte je Regel

| Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| `G11_objekt_schwebt_sinkt` | 0 | 3 | +3 |
| `G2_spitze_oben` | 3 | 3 | +0 |
| `G2_spitze_oben_fein` | 8 | 4 | -4 |
| `G3_spitze_unten` | 3 | 3 | +0 |
| `G3_spitze_unten_fein` | 2 | 1 | -1 |
| `G5_beule_klippe` | 68 | 68 | +0 |
| `G6_facette` | 220 | 195 | -25 |
| `G7_wand_glatte_flaeche` | 1 | 1 | +0 |
| `G7b_wandkontur_feld` | 24 | 24 | +0 |
| `G7b_wandkontur_kantenschaerfe` | 1 | 1 | +0 |
| `G7b_wandkontur_rauheit` | 1 | 1 | +0 |
| `G8_fluss_nicht_bis_rand` | 1 | 1 | +0 |
| `R1_blind` | 24 | 24 | +0 |
| `R2_getrennt` | 15 | 15 | +0 |
| `R3_laengs_m` | 35 | 35 | +0 |
| `R3_quer_pct` | 23 | 23 | +0 |
| `R3_woelb_m` | 22 | 22 | +0 |
| `R5_loch` | 17 | 17 | +0 |
| `R6_wasser_schnee` | 4 | 4 | +0 |
| `T1_fleckrand` | 94 | 94 | +0 |
| `T2_textur_abgeschnitten_bildpruefung_offen` | 1 | 1 | +0 |
| `T3_streifen_ringe_bildpruefung_offen` | 1 | 1 | +0 |
| `T4_graue_flussstreifen_bildpruefung_offen` | 1 | 1 | +0 |
| `T5_textur_vs_clay_bildpruefung_offen` | 1 | 1 | +0 |
| **Summe** | **570** | **543** | **-27** |

G7b-Einzelwerte aus dem finalen Lauf: Rauheit `[0,505; 0,687]`, Kantenschärfe `[1,298; 1,992]`; Treffer `G7b_wandkontur_feld=24`, `..._rauheit=1`, `..._kantenschaerfe=1` (jeweils unverändert zur Basis).

## R8 und R9

| Regel | R8 vorher | R8 nachher | R9 vorher | R9 nachher |
|---|---:|---:|---:|---:|
| `R8_gitter` | 10 | 10 | — | — |
| `R8_quer` | 5 | 5 | — | — |
| `R8_stufe` | 9 | 9 | — | — |
| `R8a_wegende` | 24 | 24 | — | — |
| `R8b_delle` | — | — | 25 | 25 |
| `R9_saegezahn` | — | — | 34 | 34 |
| `R9w_wellen` | — | — | 275 | 275 |
| **Summe** | **48** | **48** | **334** | **334** |

## Kacheln D1, G1 und D2

### pruefe_regeln

| Kachel | Treffer vorher → nachher | Regelweise: vorher → nachher |
|---|---:|---|
| D1 | 36 → 35 | `G5_beule_klippe` 1→1, `G6_facette` 5→4, `R1_blind` 2→2, `R2_getrennt` 1→1, `R3_laengs_m` 6→6, `R3_quer_pct` 11→11, `R3_woelb_m` 10→10 |
| G1 | 13 → 13 | `G3_spitze_unten_fein` 1→1, `G6_facette` 4→4, `R1_blind` 1→1, `R3_laengs_m` 1→1, `R6_wasser_schnee` 3→3, `T1_fleckrand` 3→3 |
| D2 | 8 → 8 | `R2_getrennt` 1→1, `T1_fleckrand` 7→7 |

### r8

| Kachel | Treffer vorher → nachher | Regelweise: vorher → nachher |
|---|---:|---|
| D1 | 8 → 8 | `R8_gitter` 2→2, `R8_quer` 1→1, `R8_stufe` 2→2, `R8a_wegende` 3→3 |
| G1 | 1 → 1 | `R8a_wegende` 1→1 |
| D2 | 0 → 0 | — |

### r9

| Kachel | Treffer vorher → nachher | Regelweise: vorher → nachher |
|---|---:|---|
| D1 | 26 → 26 | `R8b_delle` 2→2, `R9_saegezahn` 1→1, `R9w_wellen` 23→23 |
| G1 | 8 → 8 | `R8b_delle` 1→1, `R9_saegezahn` 1→1, `R9w_wellen` 6→6 |
| D2 | 0 → 0 | — |

D2-Prüfergebnis: pruefe_regeln **8 → 8** (R2=1, T1=7), R8 **0 → 0**, R9 **0 → 0**. Die Trefferidentität nach Regel/Feld/Koordinate enthält in D2 keine neuen und keine entfernten Treffer.

## Neue Trefferkoordinaten außerhalb D2

Verglichen wurden `regel`, `feld`, `x` und `z` (Koordinaten auf 0,1 m); `wert` wurde nicht zur Identität gezählt. Damit werden geänderte Werte am selben Punkt nicht als neue Koordinate ausgegeben. Es gibt **105 neue Koordinaten** (102 G6 und 3 G11) und **132 entfernte** (127 G6, 4 G2 fein, 1 G3 fein). R8 und R9 haben keine neuen oder entfernten Treffer.

Neue G11-Treffer (Feld, x|z, wert):
- `C5`, `104.2|211.0`, `0.81` (baeume).
- `E1`, `205.6|40.3`, `-0.78` (steine).
- `G3`, `286.2|103.5`, `0.63` (baeume).

Neue G6-Koordinaten (pro Feld `x|z:wert`):
- `A1`: 13.2|32.7:12, 16.5|32.4:9
- `A2`: 38.7|55.9:27
- `B1`: 61.8|37.0:29
- `B3`: 63.1|125.0:10, 65.8|111.2:9, 69.5|107.4:12, 78.2|127.9:10, 80.6|123.3:7, 82.2|118.6:6
- `B4`: 47.5|159.8:11, 64.7|157.5:38, 74.5|137.0:11, 75.7|171.5:11, 77.2|133.8:6, 78.1|131.3:6, 82.2|158.7:9, 82.2|161.8:6
- `B5`: 52.4|176.6:11, 58.2|176.2:6, 64.9|203.2:6, 69.5|214.0:7, 74.1|205.8:8, 75.1|208.0:11, 79.1|194.9:27, 79.1|210.7:13, 81.8|181.3:29, 82.0|177.9:11
- `B6`: 70.8|215.0:7
- `C1`: 97.2|32.0:13, 101.6|32.4:11
- `C2`: 85.2|85.5:6
- `C3`: 85.2|105.5:11, 85.2|111.8:8, 94.1|95.0:28, 113.2|116.8:6, 120.0|98.0:10, 122.4|100.1:14, 123.3|113.1:11
- `C4`: 112.8|170.3:6, 120.1|156.1:7, 123.4|140.9:6
- `C5`: 85.4|200.8:6, 86.7|203.7:14, 93.1|208.8:14, 93.4|172.5:12, 101.9|176.6:9, 110.4|186.9:8, 112.3|175.1:11, 122.5|203.0:9
- `C6`: 93.2|223.1:8, 93.2|227.4:8, 118.3|220.7:9
- `D1`: 144.4|20.8:22, 165.4|15.4:10
- `D3`: 134.0|115.8:6
- `D6`: 127.2|222.1:13, 138.3|242.3:6, 139.6|224.5:7, 147.0|244.4:6, 153.2|245.4:7, 154.4|222.1:6, 163.2|245.1:7
- `E1`: 188.0|30.2:6, 202.0|41.4:6, 206.5|32.4:20
- `F1`: 250.7|20.4:9
- `F2`: 212.0|43.6:11
- `F6`: 225.2|244.2:6, 231.2|238.8:8
- `G1`: 277.6|21.6:17
- `G3`: 268.5|125.2:6, 273.5|103.0:7, 277.1|98.0:25, 289.2|102.8:19
- `G4`: 266.5|129.8:8, 266.8|135.5:12, 289.0|155.0:16
- `G6`: 256.6|239.4:7, 259.8|227.3:10, 279.8|244.0:6, 291.2|236.4:6
- `H1`: 304.1|40.4:8, 304.9|32.0:6, 316.9|33.4:10
- `H2`: 300.3|84.9:10, 334.6|73.2:14
- `H3`: 317.6|86.0:10
- `H4`: 294.9|157.2:12
- `H5`: 301.3|179.0:9, 305.3|203.9:7, 306.0|194.0:16, 308.2|176.8:6, 308.2|207.1:6, 314.0|184.8:6, 324.1|202.1:7
- `H6`: 305.7|235.1:14, 312.4|224.2:7, 314.3|216.4:11, 335.2|245.8:6
- `H7`: 319.0|277.4:6, 334.4|277.6:8

Entfernte Treffer: `G6_facette` 127 Koordinaten, `G2_spitze_oben_fein` 4, `G3_spitze_unten_fein` 1. Damit sinkt G6 netto um 25 trotz der oben aufgeführten neuen G6-Koordinaten.

## D2-Bytevergleich

Verglichen wurde mit `d3843dc:team/art/dorfmap_grundgeruest/relief3d/relief_daten.json.gz`. Die Kachelformel ergibt D2-Zellen x=126–167, z=43–85; die dazugehörigen Randknoten wurden eingeschlossen.

| Daten | Vergleich | Ergebnis |
|---|---|---|
| `G` und `GB` | Float32-Knotenbereich D2 einschließlich Kachelrand | bytegleich, 0 Abweichungen |
| Feinband-IDs | 17 Vertices in D2 | bytegleich |
| Feinband-Höhen `h` | dieselben 17 Vertices | bytegleich |
| Feinband-Kanäle `c`, `t`, `s` | dieselben 17 Vertices | bytegleich |
| Feinband-Bandzellen | D2-Zellen | bytegleich, 0 Einträge |
| `zellen_relief.csv` | Git-Arbeitsbaum gegen Basis | unverändert |

## Bildprüfung Ton

Vorher stammt direkt aus dem eingecheckten HTML von `d3843dc`; Nachher aus dem finalen Build. Alle Bilder wurden mit denselben sechs Kameras bei `?clay=1&lod=0`, 1280×800 gerendert. D1 ist byteidentisch. G1 unterscheidet sich in 34.858 von 1.024.000 Pixeln (maximale Kanalabweichung 16); im direkten Vergleich bleiben Wandkante und Klippenkontur erhalten, ohne neue Zähne oder sichtbar weggeglättete Wand.

| Kachel / Ausschnitt | Vorher | Nachher |
|---|---|---|
| D1 – Klippe/Wand | [PNG](o18/g6_vor/D1_ton.png) | [PNG](o18/g6_nach/D1_ton.png) |
| G1 – Wandkante | [PNG](o18/g6_vor/G1o_ton.png) | [PNG](o18/g6_nach/G1o_ton.png) |
| D2 | [PNG](o18/g6_vor/D2_ton.png) | [PNG](o18/g6_nach/D2_ton.png) |
| C2 | [PNG](o18/g6_vor/C2_ton.png) | [PNG](o18/g6_nach/C2_ton.png) |
| B3 – G6-Fläche | [PNG](o18/g6_vor/B3_g6.png) | [PNG](o18/g6_nach/B3_g6.png) |
| H3 – Hang/Kante | [PNG](o18/g6_vor/H3_g6.png) | [PNG](o18/g6_nach/H3_g6.png) |

## Varianten, Annahmen und Grenzen

- Getestete Variante 1 (temporärer Feinmasken-only Versuch, 3 m Wandabstand): verworfen; G6 220→273 (+53), G5 +14, R5 +7, G11 +9. Diese Versuchsfassung ist nicht im Ergebnis enthalten.
- Variante 2: alte Grobmaske plus sichtbare Feinmaske, `FALTVWD=3`; G6=214 (−6), Gesamt=563, G11 +1.
- Variante 3 und Standard: gleiche Maskenkombination, `FALTVWD=2`; G6=195 (−25), Gesamt=543, G11 +3. Das ist der beste getestete Stand.
- Annahme: G6 soll an der sichtbaren Mischfläche gemessen werden; die Ergänzung verwendet feinbandbasierte Höhen auf dem Grobraster, ohne die bisherige Grobmaske auszutauschen. Wegband und Overlay wurden nicht verändert.
- Grenzen/offene Punkte: 195 G6-Treffer bleiben. Die Gesamtzahl sinkt, aber 102 G6-Koordinaten treten neu auf, während 127 alte G6-Koordinaten entfallen; die Verschiebungen sind oben vollständig mit Feld, Ort und Prüfwert aufgeführt. Ob −25 die gewünschte Zieltiefe erreicht, ist mangels konkreter Sollzahl offen. `export_gate.sh` bleibt rot, solange die vorhandenen Regeltreffer nicht auf null gebracht sind.
- Keine externen Dienste oder kostenpflichtigen Ressourcen verwendet; Ergebnis deterministisch gerendert/geprüft. Keine Quellwerte, kein Overlay, keine Referenzdateien und keine Prüfschwellen geändert.

## Gate-Protokoll

```text
HTML=index.html OUT=/tmp/gate_loch_g6.json RAND=0.6 NODE_PATH=/tmp/w3/node_modules node pruefung/loch_o18g.js
meshes=7, dreiecke=1.700.454, offen_innen=0
TAG=g6 LOCHSCAN=/tmp/gate_loch_g6.json sh pruefung/export_gate.sh
pruefe_regeln=543 (vor G7b-Ausgabe 517); export_gate: GATE ROT wegen nicht-null Treffer
r8=48; r9=334; pruefung_t42u summe=0; lod1=1.174.554 Dreiecke
```
