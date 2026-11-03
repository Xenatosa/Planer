# Ergebnis TAG=weg2

Stand: 2026-11-03 · Branch: `art/dorfmap-weg2` · Vergleichsbasis: `9d3f8fc`

## Ergebnis

Das Ziel wurde teilweise erreicht. `R3_laengs_m` sank gegenüber dem Zwischenstand von 45 auf 39 und liegt damit bei +4 zur Basis 35 (Grenze +5 eingehalten; Ziel ≤40 erreicht, ≤35 nicht). `R8` sank von 48 auf 38, `R8a_wegende` von 24 auf 23. `R1_wand` und `R4_rand` stehen wieder bei 0. Keine einzelne Regel steigt um mehr als 5; die Summe der `pruefe_regeln`-Treffer steigt von 596 auf 604 (+8). `R9` bleibt bei 334. Die Gates melden weiterhin die unten bezifferten Resttreffer.

## Änderungen

- Die Wegmischung verwendet standardmäßig einen 8-m-Endauslauf, einen Knotenpad-Übergang von 0 bis 8 m und Endpads an `rampe_7` Anfang und `rampe_8` Ende. Die beiden problematischen Kreuzungspads D1 (`rampe_2×11`) und D6 (`rampe_3×5`) sind standardmäßig aus. Diese Schalter bleiben über `WEG2_ENDFADE`, `WEG2_NODEIN`, `WEG2_NODEOUT`, `WEG2_NODEPAD`, `WEG2_D1_NODEPAD`, `WEG2_D6_NODEPAD` und `WEG2_ENDPADS` einzeln konfigurierbar.
- Eine lokale Verlängerung des letzten Querschnitts von `rampe_8` (`WEG2_R1_FLANKE=8e`, abschaltbar mit `0`) beseitigt den letzten `R1_wand`-Treffer. Sie verändert 40 grobe und 310 feine Höhenwerte, maximal 2,755 m; dafür liegt `R8` bei 38 statt 35 ohne diesen Endfix.
- Der Randabgleich berücksichtigt nun auch die Rampenzellen. Damit sinkt `R4_rand` von 3 im Zwischenstand auf 0.
- Die bestehende Display-Dellenanhebung bleibt aktiv (`WEG2_DELLEN=1`, abschaltbar mit `0`). Ihre Abschaltung änderte `R3_laengs_m` nicht.
- Die D2-Anteile von `GB` und `FW` werden aus einer fest eingecheckten Momentaufnahme von `9d3f8fc` restauriert. Der Generator bricht ab, falls Raster oder D2-Vertexmenge abweichen. Die Rohhöhe `G` und das Overlay `WEGA` werden nicht verändert.
- `zellen_relief.csv` wurde nach dem Build auf den Branch-Stand zurückgesetzt. Prüfskripte und Schwellenwerte blieben unverändert.

## Regelzahlen

Die Tabelle vergleicht den Gate-Lauf mit Raycast-Scan an der Basis `9d3f8fc` und am finalen Standardlauf. Fehlende Regeln haben jeweils 0 Treffer.

| Regel | Vorher | Nachher | Delta |
|---|---:|---:|---:|
| R1_blind | 24 | 24 | 0 |
| R1_wand | 0 | 0 | 0 |
| R1_wasser | 0 | 0 | 0 |
| R2_getrennt | 15 | 15 | 0 |
| R3_laengs_m | 35 | 39 | +4 |
| R3_quer_pct | 23 | 26 | +3 |
| R3_woelb_m | 22 | 24 | +2 |
| R4_rand | 0 | 0 | 0 |
| R4_schlucht | 0 | 0 | 0 |
| R5_loch | 17 | 14 | -3 |
| R5_spitze | 0 | 0 | 0 |
| R6_wasser_schnee | 4 | 4 | 0 |
| R6_objekt_auf_weg | 0 | 0 | 0 |
| R7_trennung | 0 | 0 | 0 |
| G1_lochscan_fehlt | 0 | 0 | 0 |
| G2_spitze_oben | 3 | 3 | 0 |
| G3_spitze_unten | 3 | 3 | 0 |
| G2_spitze_oben_fein | 8 | 10 | +2 |
| G3_spitze_unten_fein | 2 | 4 | +2 |
| G5_beule_klippe | 66 | 68 | +2 |
| G6_facette | 249 | 245 | -4 |
| G7_wand_glatte_flaeche | 1 | 1 | 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | 0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| G7b_wandkontur_feld | 23 | 23 | 0 |
| T1_fleckrand | 94 | 94 | 0 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |
| **Gesamt** | **596** | **604** | **+8** |

| Regelgruppe | Vorher | Nachher | Delta |
|---|---:|---:|---:|
| R8_stufe | 9 | 5 | -4 |
| R8_gitter | 10 | 5 | -5 |
| R8_quer | 5 | 5 | 0 |
| R8a_wegende | 24 | 23 | -1 |
| **R8 + R8a** | **48** | **38** | **-10** |
| R8b_delle | 25 | 25 | 0 |
| R9_saegezahn | 34 | 34 | 0 |
| R9w_wellen | 275 | 275 | 0 |
| **R9 gesamt** | **334** | **334** | **0** |

## R3-Ursache und verbleibende Treffer

Die frühere Zunahme 35→45 (+10) wurde anhand der 4-m-Prüfsegmente zerlegt:

| Kachel / Rampe | Basis-Segmente | Zwischenstand-Segmente | Netto |
|---|---|---|---:|
| D1 `rampe_2`, Kreuzung X084 | 6 | 4–8 | +4 |
| D6 `rampe_3`, Kreuzung mit `rampe_5` | 13 | 12–15 | +3 |
| D6 `rampe_5` | 0 | 1–2 (Segment 0 entfällt) | +1 |
| D1 `rampe_11`, Endauslauf X084 | 0, 8, 9, 11 | 7–11 | +2 |
| **Summe** |  |  | **+10** |

Ablationen am Zwischenstand ergaben: Ohne Knotenpads fiel R3 von 45 auf 38, während R8 von 36 auf 41 stieg; ohne Endauslauf fiel R3 auf 43, aber R8 stieg auf 84 und R8a auf 26. Ohne Dellenanhebung blieb R3 bei 45. Die Effekte überlagern sich und sind daher nicht additiv. Das stützt Knotenpads und Endauslauf als Hauptursachen der Längsregression; die Dellenanhebung ist es nicht.

Im finalen Lauf bleiben 4 zusätzliche R3-Längssegmente gegenüber der Basis: `rampe_2` Segment 7 bei 154,3|28,2 (0,082 m), `rampe_7` Segment 2 bei 120,5|178,2 (0,088 m) und `rampe_11` Segmente 7 und 10 bei 155,6|22,6 (0,104 m) sowie 150,4|33,1 (0,083 m). Bei bestehenden Treffern änderten sich unter anderem `rampe_2` Segment 6 von 0,247 auf 0,613 m, `rampe_11` Segment 8 von 1,378 auf 0,564 m und Segment 9 von 0,135 auf 0,231 m. Die 4-m-Längsabweichungsregel zählt Segmente, nicht die Höhe der Überschreitung; daher bleibt die Zahl 39.

## D1, G1 und D2 je Prüflauf

| Prüfer / Kachel | D1 vorher → nachher | G1 vorher → nachher | D2 vorher → nachher |
|---|---:|---:|---:|
| `pruefe_regeln` gesamt | 36 → 39 | 13 → 13 | 8 → 8 |
| R8/R8a gesamt | 8 → 9 | 1 → 1 | 0 → 0 |
| R9 gesamt | 26 → 26 | 8 → 8 | 0 → 0 |

In D1 steigen bei `pruefe_regeln` die R3-Längstreffer 6→9 und G6 5→6; G5 sinkt 1→0, R3-Quer sinkt 11→10 und ein G7b-Feldtreffer kommt hinzu. G1 bleibt regelweise gleich. Die acht D2-Treffer sind exakt dieselben (`R2_getrennt` 1, `T1_fleckrand` 7); es kam kein Treffer hinzu.

Der D2-Bytevergleich gegen `9d3f8fc` ergab: Rohhöhe `G` 0 abweichende Werte, Displayhöhe `GB` 0, Feinvertexmenge 6.669/6.669 identisch und Fein-Höhen 0 abweichende Werte. Das Overlay `WEGA` ist global bytegleich. D2 bleibt auch in R8/R9 bei 0 Treffern.

## Verbleibende R8-/R8a-Treffer

Die fünf R8-Knoten haben jeweils Stufen-, Gitter- und Quertreffer (insgesamt je 5). Werte sind Stufe in m / Gitterabweichung in m / Querneigung in Prozent.

| Kachel / Ort | Knoten | Restwerte |
|---|---|---:|
| C3 125,3\|126,5 | `rampe_12` Selbstknoten | 0,95 / 1,38 / 141,4 |
| D1 152,5\|28,5 | `rampe_2×11` | 0,86 / 1,79 / 17,6 |
| D6 132,9\|232,4 | `rampe_3×5` | 0,21 / 0,20 / 15,2 |
| C4 89,5\|171,4 | `rampe_8` Ende | 2,59 / 1,89 / 9,2 |
| D1 156,5\|37,5 | `rampe_11` Ende | 0,45 / 0,51 / 11,5 |

Die 23 R8a-Endwerte (Kachel, Rampe, m) sind:

| Kachel | Ende | m | Kachel | Ende | m |
|---|---|---:|---|---|---:|
| B1 | rampe_0 Anfang | 0,16 | C2 | rampe_0 Ende | 0,13 |
| G1 | rampe_1 Anfang | 0,23 | F1 | rampe_1 Ende | 0,16 |
| D1 | rampe_2 Anfang | 0,21 | E1 | rampe_2 Ende | 0,30 |
| E6 | rampe_3 Anfang | 0,28 | C6 | rampe_3 Ende | 0,16 |
| H6 | rampe_4 Anfang | 0,23 | D6 | rampe_5 Anfang | 0,25 |
| C7 | rampe_5 Ende | 0,29 | C5 | rampe_6 Anfang | 0,26 |
| C5 | rampe_7 Anfang | 0,25 | D4 | rampe_7 Ende | 0,26 |
| C4 | rampe_8 Anfang | 0,11 | C4 | rampe_8 Ende | 0,12 |
| G3 | rampe_9 Ende | 0,16 | H5 | rampe_10 Anfang | 0,24 |
| H5 | rampe_10 Ende | 0,12 | D1 | rampe_11 Anfang | 0,14 |
| D1 | rampe_11 Ende | 0,45 | D4 | rampe_12 Anfang | 0,23 |
| C3 | rampe_12 Ende | 0,18 |  |  |  |

Die Grenzwerte für die übrigen R8-Treffer sind im unveränderten `r8_kreuzung.py` hinterlegt. R8/R8a ist verbessert, aber noch nicht fehlerfrei; die D1- und C3-Knoten bleiben die größten numerischen Überschreitungen.

## Prüfungen und Determinismus

| Prüfung | Ergebnis |
|---|---|
| `python3 gen_relief.py && python3 baue_html.py` | erfolgreich; zweimal wiederholt |
| Raycast Lochscan | 7 Meshes, 1.713.256 Dreiecke, 0 offene Innenkanten, 0 Testpunkte |
| `pruefe_regeln.py` mit Lochscan | 604 Treffer; Exit 1 wegen Resttreffern |
| `r8_kreuzung.py` | 38 Treffer; Exit 1 wegen Resttreffern |
| `r9_form.py` | 334 Treffer; Exit 1 wegen Resttreffern |
| `pruefe_t42u.py` | Summe 0; keine Abweichung |
| lod1 | 1.177.664 gerenderte Dreiecke (<1,3 Mio.) |
| `sh pruefung/export_gate.sh` | GATE ROT wegen der bezifferten Resttreffer; Schwellen unverändert |
| CSV nach Build | auf HEAD-Stand zurückgesetzt; SHA-256 `fefce66d460cb153d159a244005f9b71de33b9ea0939d81aa6e2c801d57d8626` |
| Wiederholbuild | Hashes identisch: `relief_daten.json.gz` `0a00ab66…65f3b797`, `index.html` `ac36bd57…728c4d2`, `relief_zaehlung.json` `80fc12b4…706162e` |

## Annahmen, Grenzen und offene Punkte

- D2 ist als die Displayvertices x=42…84 und z=43…86 definiert. Der Referenzabzug wird gegen den eingecheckten Reliefdatensatz von `9d3f8fc` geprüft; andere Rastergeometrien führen zum Abbruch.
- Die R3-Ablationen sind lokale Varianten desselben Generators, keine mathematisch unabhängige Zerlegung; Pads und Endausläufe beeinflussen einander.
- Der R1-Endfix erfüllt `R1_wand=0`, aber `R1_blind` bleibt bei 24 wie an der Basis. R8/R8a und R9 sind nicht vollständig beseitigt.
- Die `pruefe_regeln`-Gesamtsumme liegt +8, obwohl alle Einzelregeln höchstens +4 steigen. Export bleibt laut Pflicht-Gate gesperrt, bis die verbleibenden Treffer anderweitig akzeptiert oder behoben sind.
- `R9` wertet das unveränderte Rohfeld `G` aus; die Display-Dellenanhebung ändert `R8b_delle` deshalb nicht. Quellwerte und Prüfgrenzen wurden nicht angepasst.
