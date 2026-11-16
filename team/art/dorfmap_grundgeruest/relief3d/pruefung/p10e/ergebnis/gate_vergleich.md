# P10e Gate vorher (9ace686) / nachher (P10e) je Regel

Eigene Pfade (`/tmp/p10e/gate.sh` = export_gate.sh-Schritte, O17REF=/tmp/p10c/o17.json.gz; nie /tmp/gate_loch.json). Vorher = Worktree 9ace686 unverändert, W1 dort mit P10d-Skript gemessen.

## regeln: 397 → 397

| Regel | vorher | nachher | Δ |
|---|---|---|---|
| G2_spitze_oben | 3 | 3 | +0 |
| G2_spitze_oben_fein | 9 | 9 | +0 |
| G3_spitze_unten | 3 | 3 | +0 |
| G3_spitze_unten_fein | 2 | 2 | +0 |
| G5_beule_klippe | 63 | 63 | +0 |
| G6_facette | 205 | 205 | +0 |
| G7_wand_glatte_flaeche | 1 | 1 | +0 |
| G7b_wandkontur_feld | 25 | 25 | +0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | +0 |
| G7b_wandkontur_rauheit | 1 | 1 | +0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | +0 |
| R1_blind | 17 | 17 | +0 |
| R2_getrennt | 9 | 9 | +0 |
| R3_laengs_m | 20 | 20 | +0 |
| R3_quer_pct | 11 | 11 | +0 |
| R3_woelb_m | 10 | 10 | +0 |
| R5_loch | 8 | 8 | +0 |
| R6_wasser_schnee | 4 | 4 | +0 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | +0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | +0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | +0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | +0 |

## r8: 33 → 33

| Regel | vorher | nachher | Δ |
|---|---|---|---|
| R8_gitter | 7 | 7 | +0 |
| R8_quer | 3 | 3 | +0 |
| R8_stufe | 6 | 6 | +0 |
| R8a_wegende | 17 | 17 | +0 |

## r9: 325 → 325

| Regel | vorher | nachher | Δ |
|---|---|---|---|
| R8b_delle | 22 | 22 | +0 |
| R9_saegezahn | 34 | 34 | +0 |
| R9w_wellen | 269 | 269 | +0 |

## w1: 0 → 0

| Regel | vorher | nachher | Δ |
|---|---|---|---|
| W1a_ausserhalb_karte | 0 | 0 | +0 |
| W1b_ueber_krone | 0 | 0 | +0 |
| W1c_schwebend | 0 | 0 | +0 |
| W1d_quellabstand | 0 | 0 | +0 |

## W1 alle 56 Kacheln (neu im Gate)

| Teilprüfung | vorher (9ace686, alter wand.py) | nachher |
|---|---|---|
| W1a_ausserhalb_karte | 0 | 0 |
| W1b_ueber_krone | 1616 | 0 |
| W1c_schwebend | 0 | 0 |
| W1d_quellabstand | 0 | 0 |
| **Summe** | 1616 | 0 |

W1b vorher je Kachel: C6 387, G6 263, E6 210, D6 195, H6 154, F6 107, B4 61, B6 53, A3 47, A6 46, C1 27, G3 26, C7 16, A4 13, C5 9, H3 2

## Laufzeit Gate (nachher, `gate_nachher/zeiten.txt`)

```
zeit loch 3.01 regeln 3.36 r8r9 5.9 w1 0.93
zeit w1_56 18.05 gesamt 31.3
```
W1 alle 56 (Paket bauen ohne HTML + Prüfung) ≈ 18 s → unter 1 min, daher in `export_gate.sh` aufgenommen.

## Lochscan 56 Kacheln

R5_loch vorher 0 → nachher 0; Positivkontrolle C3: 3 (erwartet 3).

## index.html vorher (9ace686) / nachher – Gelände bitgleich

| Kachel | Teil | identisch | pos sha256 | idx sha256 |
|---|---|---|---|---|
| D1 | surface | True | 5a1fff67b0dfcb1d… | dcc175769e81696f… |
| D1 | sides | True | 48b61c1b6d1b589a… | d78766b08f5d4b72… |
| D1 | bottom | True | 110e2ff11c02fcd4… | b130fea93319b6db… |
| G1 | surface | True | afd6afad9d075459… | dcc175769e81696f… |
| G1 | sides | True | 99ddcb7db922b0f2… | d78766b08f5d4b72… |
| G1 | bottom | True | b6ed71c46935a0e2… | b130fea93319b6db… |
| D2 | surface | True | ebeb46a15c25bce0… | dcc175769e81696f… |
| D2 | sides | True | 6835acf26107fbe7… | d78766b08f5d4b72… |
| D2 | bottom | True | b33d5a64c686ce3f… | b130fea93319b6db… |

Wände: vorher D1 16544 / G1 25004 / D2 0 Dreiecke (ganz im Gelände), nachher alle 0. index.html außer der NEU_GZ-Zeile bytegleich (Bundle unverändert).

## Wandstatistik 56 Kacheln

| | vorher | nachher |
|---|---|---|
| dreiecke | 621068 | 0 |
| vertices | 525676 | 0 |
| ueber_0_1m | 72550 | 0 |
| nahe_gelaende_0_02m | 1773 | 0 |
| Kacheln mit Wandkörper | 35 | 0 |

Render-Beleg Viewer: pixel_abweichend_ohne_waende {'C6.png': 0, 'C6_nah_nord.png': 0, 'E6.png': 0, 'F6.png': 0, 'G6.png': 0, 'H6.png': 0, 'H6_nah_nord.png': 0}

