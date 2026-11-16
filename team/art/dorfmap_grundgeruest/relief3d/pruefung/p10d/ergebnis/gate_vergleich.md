# P10d Gate vorher (d181fa6) / nachher (P10d) je Regel

Gelaufen mit `pruefung/p10d/gate_eigene_pfade.sh index.html <ordner>` (= export_gate.sh mit eigenen Pfaden, O17REF=/tmp/p10c/o17.json.gz, nicht /tmp/gate_loch.json).

## regeln: 476 → 476

| Regel | vorher | nachher | Δ |
|---|---|---|---|
| G2_spitze_oben | 3 | 3 | +0 |
| G2_spitze_oben_fein | 8 | 8 | +0 |
| G3_spitze_unten | 3 | 3 | +0 |
| G3_spitze_unten_fein | 2 | 2 | +0 |
| G5_beule_klippe | 68 | 68 | +0 |
| G6_facette | 220 | 220 | +0 |
| G7_wand_glatte_flaeche | 1 | 1 | +0 |
| G7b_wandkontur_feld | 24 | 24 | +0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | +0 |
| G7b_wandkontur_rauheit | 1 | 1 | +0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | +0 |
| R1_blind | 24 | 24 | +0 |
| R2_getrennt | 15 | 15 | +0 |
| R3_laengs_m | 35 | 35 | +0 |
| R3_quer_pct | 23 | 23 | +0 |
| R3_woelb_m | 22 | 22 | +0 |
| R5_loch | 17 | 17 | +0 |
| R6_wasser_schnee | 4 | 4 | +0 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | +0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | +0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | +0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | +0 |

## r8: 48 → 48

| Regel | vorher | nachher | Δ |
|---|---|---|---|
| R8_gitter | 10 | 10 | +0 |
| R8_quer | 5 | 5 | +0 |
| R8_stufe | 9 | 9 | +0 |
| R8a_wegende | 24 | 24 | +0 |

## r9: 334 → 334

| Regel | vorher | nachher | Δ |
|---|---|---|---|
| R8b_delle | 25 | 25 | +0 |
| R9_saegezahn | 34 | 34 | +0 |
| R9w_wellen | 275 | 275 | +0 |

## w1: 0 → 0

| Regel | vorher | nachher | Δ |
|---|---|---|---|
| W1a_ausserhalb_karte | 0 | 0 | +0 |
| W1b_ueber_krone | 0 | 0 | +0 |
| W1c_schwebend | 0 | 0 | +0 |
| W1d_quellabstand | 0 | 0 | +0 |

Hervorgehoben: G5_beule_klippe 68 → 68, G7_wand_glatte_flaeche 1 → 1, G7b 24+1+1 → 24+1+1 (unverändert; diese Prüfer messen das Höhenfeld, nicht die Wandkörper).

## W1 (neu) je Teilprüfung – index.html (D1/G1/D2) und alle 56 Kacheln

| Teilprüfung | index.html vorher | index.html nachher | 56 Kacheln vorher | 56 Kacheln nachher | Positivkontrolle 7944b33 (vor P10c) |
|---|---|---|---|---|---|
| W1a_ausserhalb_karte | 0 | 0 | 0 | 0 | 0 |
| W1b_ueber_krone | 0 | 0 | 1621 | 0 | 140 |
| W1c_schwebend | 0 | 0 | 0 | 0 | 0 |
| W1d_quellabstand | 0 | 0 | 0 | 0 | 461 |
| **Summe** | 0 | 0 | 1621 | 0 | 601 |

Treffer = Zellen je Teilprüfung und Kachel. W1 vorher in index.html = 0, weil die D1/G1-Wände nach P10c vollständig im Gelände lagen (unsichtbar).

### W1 56 Kacheln vorher je Kachel (nur W1b, alle anderen Teilprüfungen 0)

| Kachel | W1b vorher | max. über Krone vorher (m) | W1b nachher |
|---|---|---|---|
| C6 | 387 | 15.676 | 0 |
| G6 | 263 | 15.837 | 0 |
| E6 | 210 | 15.282 | 0 |
| D6 | 195 | 16.105 | 0 |
| H6 | 154 | 16.033 | 0 |
| F6 | 107 | 18.205 | 0 |
| B4 | 61 | 7.863 | 0 |
| B6 | 53 | 15.223 | 0 |
| A3 | 47 | 7.899 | 0 |
| A6 | 46 | 13.46 | 0 |
| C1 | 27 | 3.378 | 0 |
| G3 | 26 | 2.488 | 0 |
| C7 | 16 | 15.648 | 0 |
| A4 | 13 | 7.924 | 0 |
| C5 | 9 | 2.278 | 0 |
| C3 | 5 | 5.423 | 0 |
| H3 | 2 | 0.682 | 0 |

## Wandstatistik 56 Kacheln (`wand_statistik.json`)

| | vorher | nachher |
|---|---|---|
| dreiecke | 621068 | 48452 |
| vertices | 525676 | 42124 |
| ueber_0_1m | 73244 | 15418 |
| nahe_gelaende_0_02m | 1772 | 146 |
| Kacheln mit Wandkörper | 35 | 11 |
| max. Wand über Gelände (m) | 18.95 | 1.0 |

## Lochscan 56 Kacheln

R5_loch vorher 0 → nachher 0; Positivkontrolle C3 (1 Dreieck entfernt): 3 Treffer (erwartet 3).

## D2 bitgleich (index.html vorher/nachher, Browser-Hash Weltkoordinaten)

- surface: True pos ebeb46a15c25bce0… idx dcc175769e81696f…
- sides: True pos 6835acf26107fbe7… idx d78766b08f5d4b72…
- bottom: True pos b33d5a64c686ce3f… idx b130fea93319b6db…
- Wände D2: leer vorher/nachher (mesh_sha256 e3b0c442… = leerer Puffer)
