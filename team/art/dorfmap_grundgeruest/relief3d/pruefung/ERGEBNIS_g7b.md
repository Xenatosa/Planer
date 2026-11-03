# Ergebnis g7b – Wandkontur

## Ergebnis

Ziel nicht erreicht. Der Standard bleibt bei der unveränderten Rohkontur, da beide getesteten Konturvarianten die G7b-Messung kaum bewegten und deutliche Regressionen erzeugten. Die G7b-Treffer und `G7_wand_glatte_flaeche` bleiben auf dem Ausgangswert.

## Änderung und Varianten

`gen_relief.py` hat jetzt den Schalter `WANDKONTURV`: `0` ist Standard und lässt Reliefdaten unverändert; `1` und `2` sind deterministische Versuche mit signiertem Abstandsfeld und geglättetem Konturverlauf. Die Maskenänderung schützt Wasser, Wege, Brücken, Bauflächen und Rampen. Quellwerte, Overlaydatei und Wandflächen-Tesselierung bleiben unverändert.

| Variante | Konturänderung | `pruefe_regeln` | R8 | R9 | G7b Rauheit (Ist/O17) | G7b Kantenschärfe (Ist/O17) | G7b Feldtreffer | Befund |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `WANDKONTURV=0` (Standard) | 0 Zellen | 596 | 48 | 334 | 0,507 / 0,687 (0,737) | 1,303 / 1,992 (0,654) | 23 | keine Regression; Zielwerte offen |
| `WANDKONTURV=1` | 477 hinzu, 443 entfernt | 708 (+112) | 48 (+0) | 336 (+2) | 0,509 / 0,687 (0,741) | 1,303 / 1,992 (0,654) | 23 | verworfen; G6 +19, G11 +100 |
| `WANDKONTURV=2` | 874 hinzu, 761 entfernt | 722 (+126) | 48 (+0) | 338 (+4) | 0,505 / 0,687 (0,735) | 1,304 / 1,992 (0,654) | 23 | verworfen; G11 +127, T1 +6, R6_objekt_auf_weg +1 |

Die Klammerwerte sind das Verhältnis zum O17-Referenzwert; für beide G7b-Regeln gilt eine Mindestquote von 0,85. Keine getestete Variante erreichte sie. Die stärkere Variante verschlechterte die Rauheit leicht.

## Regelzahlen vorher/nachher

Ausgang ist der angegebene Stand `9d3f8fc`. Der Standardlauf reproduzierte ihn exakt. `G7_wand_glatt_gesamt` hatte vor und nachher keinen Treffer.

| Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| R1_wand | 0 | 0 | 0 |
| R1_wasser | 0 | 0 | 0 |
| R1_blind | 24 | 24 | 0 |
| R2_getrennt | 15 | 15 | 0 |
| R3_laengs_m | 35 | 35 | 0 |
| R3_quer_pct | 23 | 23 | 0 |
| R3_woelb_m | 22 | 22 | 0 |
| R4_rand | 0 | 0 | 0 |
| R4_schlucht | 0 | 0 | 0 |
| R5_loch | 17 | 17 | 0 |
| R5_spitze | 0 | 0 | 0 |
| R6_objekt_auf_weg | 0 | 0 | 0 |
| R6_wasser_schnee | 4 | 4 | 0 |
| R7_trennung | 0 | 0 | 0 |
| G1_lochscan_fehlt | 0 | 0 | 0 |
| G1_loch_offen | 0 | 0 | 0 |
| G2_spitze_oben | 3 | 3 | 0 |
| G3_spitze_unten | 3 | 3 | 0 |
| G2_spitze_oben_fein | 8 | 8 | 0 |
| G3_spitze_unten_fein | 2 | 2 | 0 |
| G4_delle_beule | 0 | 0 | 0 |
| G5_beule_klippe | 66 | 66 | 0 |
| G6_facette | 249 | 249 | 0 |
| G7_wand_glatt_gesamt | 0 | 0 | 0 |
| G7_wand_glatte_flaeche | 1 | 1 | 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| G8_fluss_flach | 0 | 0 | 0 |
| G11_objekt_schwebt_sinkt | 0 | 0 | 0 |
| G11_baum_an_wand | 0 | 0 | 0 |
| T1_harte_farbkante | 0 | 0 | 0 |
| T1_harte_farbkante_gerade | 0 | 0 | 0 |
| T1_fleckrand | 94 | 94 | 0 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |
| T6_wasser_in_schnee_farbe | 0 | 0 | 0 |
| T_VC_format | 0 | 0 | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | 0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| G7b_wandkontur_feld | 23 | 23 | 0 |
| **pruefe_regeln Summe** | **596** | **596** | **0** |
| R8_stufe | 9 | 9 | 0 |
| R8_gitter | 10 | 10 | 0 |
| R8_quer | 5 | 5 | 0 |
| R8a_wegende | 24 | 24 | 0 |
| **R8 Summe** | **48** | **48** | **0** |
| R8b_delle | 25 | 25 | 0 |
| R9_saegezahn | 34 | 34 | 0 |
| R9w_wellen | 275 | 275 | 0 |
| **R9 Summe** | **334** | **334** | **0** |

## D1, G1 und D2

Die Feldsummen und Einzelregeln sind vor und nach dem Standardlauf gleich. G7/G7b-Treffer in diesen drei Feldern: jeweils 0.

| Feld | pruefe_regeln vorher/nachher | R8 vorher/nachher | R9 vorher/nachher | Treffer in D2 neu |
|---|---:|---:|---:|---:|
| D1 | 36 / 36 | 8 / 8 | 26 / 26 | – |
| G1 | 13 / 13 | 1 / 1 | 8 / 8 | – |
| D2 | 8 / 8 | 0 / 0 | 0 / 0 | 0 |

Nichtnull-Regeln in `pruefe_regeln` je Feld:

| Regel | D1 | G1 | D2 |
|---|---:|---:|---:|
| R1_blind | 2 | 1 | 0 |
| R2_getrennt | 1 | 0 | 1 |
| R3_laengs_m | 6 | 1 | 0 |
| R3_quer_pct | 11 | 0 | 0 |
| R3_woelb_m | 10 | 0 | 0 |
| R6_wasser_schnee | 0 | 3 | 0 |
| G3_spitze_unten_fein | 0 | 1 | 0 |
| G5_beule_klippe | 1 | 0 | 0 |
| G6_facette | 5 | 4 | 0 |
| T1_fleckrand | 0 | 3 | 7 |

R8 in D1: `R8_stufe` 2, `R8_gitter` 2, `R8_quer` 1, `R8a_wegende` 3; G1: `R8a_wegende` 1; D2: 0. R9 in D1: `R8b_delle` 2, `R9_saegezahn` 1, `R9w_wellen` 23; G1: 1, 1, 6; D2: 0.

Die Display-Höhenscheiben `G` und `GB` von D2 sind bytegleich zum Vorher-Stand. Beide sind 87×85 Werte; SHA-256: `G` `325f6fe2f41178f7e9c4b2198881438bc5ac70649ac4a0ee9836b463e6e1408c`, `GB` `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`. Die 17 Feinbandpunkte in D2 sind ebenfalls unverändert.

## Pflichtprüfungen

- `python3 gen_relief.py && python3 baue_html.py`: erfolgreich und deterministisch. `relief_daten.json.gz` SHA-256: `208b06f8c1d95f9f3bf36d887314faf0579ea2ff709b3cbf5a17ecda9425d87d`; `index.html`: `93f0b8eb6cd986390e213e1a189bd7bda0e6e3bdd317ffeb9e28b909981da1ee`.
- `pruefe_t42u.py`: Summe 0.
- LOD1-Bildpass: 1.174.561 Dreiecke (<1,3 Mio.); zusätzlicher FBO-Pass: 829.241.
- Raycast (`RAND=0.6`): 7 Meshes, 0 offene Innenlöcher, 0 Punkte.
- `sh pruefung/export_gate.sh`: ROT, wie auf der gegebenen Ausgangsbasis zu erwarten; die verbliebenen 596/48/334 Treffer bleiben unverändert. Kein Prüfskript und kein Schwellenwert wurde geändert.
- `zellen_relief.csv` wurde nach dem Build auf Branch-Stand zurückgesetzt (SHA-256 `fefce66d460cb153d159a244005f9b71de33b9ea0939d81aa6e2c801d57d8626`). Die Overlaydatei und Zellquellen sind unverändert.

## Annahmen, Grenzen und offene Punkte

- Feldzuordnung: 42×43 m; D1 = x 126–168 m, z 0–43 m; G1 = x 252–294 m, z 0–43 m; D2 = x 126–168 m, z 43–86 m.
- Der Zufall der Konturversuche ist mit Seed 7107 festgelegt. Kosten: 0 EUR.
- Die G7b-Prüfung misst Rauheit und Laplace-Spitzen im Wandhöhenfeld. Die erlaubte 2D-Maskenverschiebung änderte diese Messwerte kaum; die Varianten erzeugten zugleich neue G6/G11- und R9-Treffer. Eine wirksame Korrektur muss die Wandoberfläche selbst adressieren und ist mit der parallelen K5b-Tesselierungsarbeit abzustimmen.
- Offen bleiben `G7_wand_glatte_flaeche` (1), G7b Rauheit (1), Kantenschärfe (1) und Feld (23). Der Standard hält die Ausgangswerte und D2 exakt ein, erreicht das Ziel aber nicht.
