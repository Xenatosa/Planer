# Ergebnis TAG=weg

Stand: 2026-11-03 · Branch: `art/dorfmap-weg`

## Ergebnis

Das Ziel wurde teilweise erreicht. Die gewichtete Wegprofil-Mischung senkt R8 von 48 auf 36 Treffer. R8, R8a und R8b sind weiterhin nicht null. Die harte Regressionsgrenze wird bei `R3_laengs_m` verletzt: 45 statt 35 Treffer (+10; zulässig wären höchstens +5). D2 bleibt in R8 und R9 bei null Treffern; in `pruefe_regeln` kam in D2 kein Treffer hinzu.

## Änderungen

- `_weg_mischung()` mischt die Profile aller Rampen bis 6,1 m mit `1/(d^4 + WEGMISCH_EPS)`. Standard ist `WEGMISCH_EPS=0.01`; Grob- und Feinband verwenden dieselbe Zielfläche.
- Kreuzungen, Kehren, Anschlüsse und Wegenden werden aus der R8-Knotenlogik gebildet und mit einer gemeinsamen Höhe `Hc` versehen. Die ebene Kernfläche hat 2,5 m Radius; außerhalb folgt die tanh-Böschung mit dem Parameter 0,7. Die Smoothstep-Armkorrektur ist über `WEGMISCH_GLATT=1` einschaltbar. Standard bleibt sie aus, weil beide geprüften Läufe mit Armkorrektur `R3_laengs_m` stärker verschlechterten.
- Wegenden erhalten ein mindestens 4 m langes Smoothstep-Profil und eine runde Feinbandkappe bis 6 m. `WEGMISCH=0` schaltet weiterhin die alte `_weg_eben()`-Nearest-Logik ein.
- `_weg_dellen_anheben()` hebt Display-Mulden über 0,30 m im 6-m-Wegbereich bis auf 0,28 m Resttiefe an. Der Rohwert `G` wird dabei nicht verändert.
- Die beim Build umgeschriebene `zellen_relief.csv` wurde auf den Branch-Stand zurückgesetzt. Quellwerte `G` und Overlay `WEGA` im Reliefdatensatz sind bytegleich zum Branch-Stand. Prüfskripte, `main.js`, Wandlogik und Texturen wurden nicht geändert.

## Regelzahlen: vorher und nachher

Quelle „vorher“: die im Branch liegenden Baseline-Berichte aus Stand `9d3f8fc`. „Nachher“: finaler Standardlauf.

| Regel | Vorher | Nachher | Delta |
|---|---:|---:|---:|
| R1_blind | 24 | 24 | 0 |
| R1_wand | 0 | 2 | +2 |
| R2_getrennt | 15 | 15 | 0 |
| R3_laengs_m | 35 | 45 | **+10** |
| R3_quer_pct | 23 | 23 | 0 |
| R3_woelb_m | 22 | 18 | -4 |
| R4_rand | 0 | 3 | +3 |
| R5_loch | 17 | 13 | -4 |
| R6_wasser_schnee | 4 | 4 | 0 |
| G2_spitze_oben | 3 | 3 | 0 |
| G3_spitze_unten | 3 | 4 | +1 |
| G2_spitze_oben_fein | 8 | 8 | 0 |
| G3_spitze_unten_fein | 2 | 2 | 0 |
| G5_beule_klippe | 66 | 68 | +2 |
| G6_facette | 249 | 251 | +2 |
| G7_wand_glatte_flaeche | 1 | 1 | 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| T1_fleckrand | 94 | 94 | 0 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | 0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| G7b_wandkontur_feld | 23 | 24 | +1 |
| **Gesamt** | **596** | **609** | **+13** |

### R8/R8a/R8b

| Regel | Vorher | Nachher | Delta |
|---|---:|---:|---:|
| R8_stufe | 9 | 3 | -6 |
| R8_gitter | 10 | 8 | -2 |
| R8_quer | 5 | 2 | -3 |
| R8a_wegende | 24 | 23 | -1 |
| **R8 gesamt** | **48** | **36** | **-12** |
| R8b_delle | 25 | 25 | 0 |
| R9_saegezahn | 34 | 34 | 0 |
| R9w_wellen | 275 | 275 | 0 |
| **R9 gesamt** | **334** | **334** | **0** |

## D1, G1 und D2

| Kachel | `pruefe_regeln` vorher → nachher | R8: Stufe / Gitter / Quer / Ende | R9: Delle / Sägezahn / Wellen |
|---|---:|---:|---:|
| D1 | 36 → 42 (+6) | 2 / 2 / 1 / 3 = 8 | 2 / 1 / 23 = 26 |
| G1 | 13 → 14 (+1) | 0 / 1 / 0 / 1 = 2 | 1 / 1 / 6 = 8 |
| D2 | 8 → 8 (0) | 0 / 0 / 0 / 0 = 0 | 0 / 0 / 0 = 0 |

Die acht vorhandenen `pruefe_regeln`-Treffer in D2 sind dieselben wie vorher; es gibt keinen neuen D2-Treffer. D2 bleibt bei null R8- und R9-Treffern. **Die D2-Displaygeometrie ist dennoch nicht unverändert:** Gegenüber dem eingecheckten Reliefdatensatz änderten sich 90 GB-Werte (max. 0,00391 m); unter 32.958 gemeinsamen Feinband-Vertices änderten sich 1.898 Höhen (max. 0,41212 m), zusätzlich kamen 1.508 Feinband-Vertices hinzu. Damit ist die strikte D2-Geometrie-Invariante nicht erfüllt, obwohl die genannten D2-Gatebedingungen erfüllt sind.

Am D1-Knoten `rampe_2x11` bei 152,5|28,5 fiel die gemessene R8-Stufe von 1,39 m auf 0,235 m je 0,25 m. Das Gittermaß liegt dort bei 0,046 m und ist unter der Schwelle; die Stufe bleibt knapp über 0,20 m. Am Ende von `rampe_11` verbleiben 0,45 m Stufe, 0,50 m Gitterabweichung, 11,3 % Querneigung und ein R8a-Wert von 0,45 m. In G1 verbleiben am Ende von `rampe_1` 0,17 m Gitterabweichung und 0,26 m bei R8a. Die Kehre C3 hat weiterhin 0,95 m Stufe, 1,38 m Gitterabweichung und 141,4 % Querneigung.

## Varianten

| Lauf | Einstellungen | `pruefe_regeln` gesamt | R3 längs | R8: Stufe / Gitter / Quer / Ende |
|---|---|---:|---:|---:|
| 1 | `GEF=0.08`, Armkorrektur an; vor Ergänzung der Endkappen | 616 | 49 | 6 / 14 / 3 / 24 = 47 |
| 2 | `GEF=0.04`, Armkorrektur an, Endkappen | 617 | 52 | 2 / 8 / 2 / 23 = 35 |
| 3 (Standard) | `GEF=0.08`, Armkorrektur aus, Endkappen | 609 | 45 | 3 / 8 / 2 / 23 = 36 |

Der dritte Lauf ist Standard, weil er die wenigsten Gesamt-Regeltreffer der drei Läufe hatte und R3 längs am wenigsten erhöhte. Keine Variante erfüllt die Grenze `+5` für R3 längs.

## Prüfungen des finalen Standardlaufs

- `python3 gen_relief.py && python3 baue_html.py`: erfolgreich.
- Lochprüfung: 7 Meshes, 1.713.256 Dreiecke, 0 offene Innenkanten, 0 Prüfpunkte.
- `pruefe_regeln`: 609 Treffer insgesamt; Exit 1 wegen vorhandener Regel-Treffer. Davon sind 583 vor dem zusätzlichen G7b-Teilbericht und 609 nach G7b.
- `r8_kreuzung.py`: 36 Treffer; Exit 1 wegen vorhandener R8/R8a-Treffer.
- `r9_form.py`: 334 Treffer; Exit 1 wegen vorhandener R8b/R9-Treffer.
- `pruefe_t42u.py`: Summe 0, auch nach Wiederherstellung der CSV.
- Lod1: 1.177.664 gerenderte Dreiecke, unter 1,3 Mio.
- Determinismus: zwei aufeinanderfolgende Standardbuilds erzeugten identische SHA-256-Werte für `relief_daten.json.gz` (`a3e3c609…10fe`) und `index.html` (`fdfbfe46…f7f3`).

## Annahmen, Grenzen und offene Punkte

- `r9_form.py` ermittelt R8b aus dem unveränderten Rohfeld `G`, nicht aus `GB` oder `FW`. Die gemessene G1-Delle bei 278,5|27,0 bleibt daher bei 0,423 m und 5,6 m Wegabstand. Der Display-Auffüller fand in G1 keine passende Mulde (`G1_mulden=0`); die R8b-Zahl änderte sich nicht. Eine Behebung im von R9 geprüften Feld würde den ausdrücklich geschützten Zellquellwert verändern.
- Die Knotenbildung der neuen Funktion lieferte 7 Knoten für gemeinsame Hc-Pads; der Gate-Scanner bewertet 31 Knoten. Nicht alle Gate-Knoten werden damit von der neuen Ebenenbehandlung erfasst.
- Die Smoothstep-Armangleichung ist im finalen Standard ausgeschaltet, weil sie in den geprüften Einstellungen R3 längs stärker erhöhte. Mit dem Standard sind gewichtete Profile, Knotenpads und Endausläufe aktiv, aber die geforderte Armangleichung ist nicht vollständig erfüllt.
- R8/R8a sind verbessert, aber nicht null. R8b und die beiden R9-Formregeln blieben unverändert. Die Karte erfüllt das Ziel „R8, R8a und R8b kartenweit 0“ nicht.
