# Ergebnis p3d18

**Ergebnis: Die korrigierte offizielle R3-Modellformulierung ist machbar und die minimale Modellstufe ist bewiesen. Variante 24 wurde gebaut. D1-R3 besteht; zwei numerisch kleine R8-Grenzen, mehrere Regressionen und die weiche Clay-/Streiflichtvorgabe sind verfehlt.**
Stand: 10.11.2026 · Worktree /workspace/wt_dorfmap_p3d18 · Branch art/dorfmap-p3d18 · Basis origin/art/dorfmap-p3d17 bei c3659e7 · Kosten **0 EUR**.

## Kalibrierung der offiziellen R3-Formel

Die unveränderte p3d17-Variante 22 wurde auf der Relief-Neu-Fläche nachgebildet. Der rekonstruierte D1-Raster ist bytegleich zum p3d17-Bericht, SHA-256 26b849f6384993d5029b58dc08f6c657406785e26939f7c172a0d8fafe1ace29. Der unveränderte offizielle Prüfer pruefung/pruefe_regeln.py wurde darauf erneut ausgeführt.

| D1-R3-Zähler | bisherige Modellindikatoren | offizieller p3d17-Bericht | offizielle Wiederholung |
|---|---:|---:|---:|
| längs | 6 | 6 | 6 |
| quer | 5 | 17 | 17 |
| Wölbung | 4 | 19 | 19 |

Die alte interne Ersatzformel zählte auf dem unveränderten p3d17-Mesh die Quer- und Wölbungsabschnitte deutlich zu niedrig. Die korrigierte Formulierung übernimmt die Prüferabtastung mit 0,25 Karten-Einheiten, 16 Punkten je Abschnitt, gaußgefiltertem Längsrest mit sigma 8, seitlichen Abständen ±1,5, Quergrenze 3,5 %, Wölbungsgrenze 0,08 m und einer Kappe von 20 % für jeden Querwert. Die Längsschwelle ist 0,08 m. Der Prüfer selbst und seine Schwellen blieben unverändert. Reproduktion: codex_jobs/tools/p3d18_r3/calibrate_p3d17.py.

## Machbarkeit und minimale Modellstufe

Die Machbarkeitsrechnung hielt Route, Ebenenkernradius r=2,00 m und alle harten Limits fest: Stufe ≤0,116 m, Gitter ≤0,020 m, R8-Querneigung ≤3 %, Achsauflagen ±0,02 m, D1-R3 6/7/7 und kein Einzelquerwert >20 %. HiGHS fand einen zulässigen ganzzahligen Punkt und bewies das Optimum der Machbarkeitszielfunktion.

| Machbarkeitspunkt | Modellwert | Grenze |
|---|---:|---:|
| Stufe am R8-Zentrum | 0,115153279 m | ≤0,116 m |
| R8-Gitter | 0,020000000000037 m | ≤0,020 m |
| R8-Quer | 2,999421748 % | ≤3 % |
| D1-R3 längs/quer/Wölbung | 4/0/4 | ≤6/≤7/≤7 |
| Ebenenkernneigung | 2,216100 % | r=2,00 m, ≤3 % |
| Achsstützen | 359 geprüft | ±0,02 m |
| Modellgröße | 7.858 Variablen, 10.136 Bedingungen | optimal |

Ergebnis Machbarkeit: **ja**. Danach wurde die Stufe separat minimiert. HiGHS meldete optimalen Status und MIP-Lücke 0,0 %; Incumbent 0,076068881583 m, duale Untergrenze 0,076068871583 m, Abstand rund 0,000000010 m. Der Modellpunkt zählt D1-R3 mit 6/7/7 und sagt R8-Gitter 0,020000000000032 m sowie R8-Quer 2,999999999999826 % voraus. Die tatsächliche Meshprüfung steht unten; sie findet beim Float32-Export minimale Grenzüberschreitungen.

## Variante 23, gemessener Transferfehler und Korrektur 24

Variante 23 wurde gebaut und mit dem unveränderten Neu-Mesh-Adapter geprüft. Der offizielle Prüfer zählte im D1-Mesh R3 längs/quer/Wölbung **7/20/21**, die größte Einzelquerung war 41,3 % bei rampe_11 am Prüfort 148.5|2.5. Zwölf von 359 Achsstützen wichen mehr als 0,02 m ab; Maximum 0,064167 m. Damit war der vorherige Modellpunkt kein Mesh-Machbarkeitsbeleg.

Die Diagnose fand zwei Modellierungsfehler: Der affine Transferintercept war nochmals mit 1−Deckung gewichtet, obwohl er bereits der feste Intercept der finalen Transferfunktion ist; außerdem lagen Achsbedingungen am Zielraster statt an der tatsächlich ausgegebenen, überblendeten Meshfläche. Variante 24 korrigiert diese Abbildung. Wegführung, Ebenenkernradius, Prüfer und Schwellen blieben unverändert. Die Variante-23-Einzelbefunde liegen in bilder_p3d18/variante23_diagnose/.

## Variante-24-Mesh und Zielprüfung

Der Build war RELIEF_NEU=1 RELIEF_KREUZUNG_VAR=24. Der Adapter patchte D1 und G1 in die offizielle Prüfeingabe; D2 blieb bytegleich.

| Messung | Ergebnis | Ziel / Bewertung |
|---|---:|---|
| D1-Meshhash | 9619da5083720eb43f736043452b28f87dd2f9aa946dc2cb453b5ed972d02c6c | neu, verschieden von p3d17 26b849f6… |
| G1-Meshhash | 38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb | unverändert |
| D2-Meshhash | 749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6 | unverändert; Adapter bestätigt bytegleich |
| LOD1-Dreiecke | 134.316 | Grenze <1,3 Mio. bestanden |
| maximale D1-Höhenänderung | 2,928332 m | test_gelaende_mesh-Grenze 4,0 m bestanden |
| Klippenhöhe bei 140|35 | 7,884036541 m | Soll 7,8840365 m |
| Vektor SHA-256 | aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e | unverändert |
| Zellquell-Differenzen | 0 | Zellquellwerte unverändert |

### R3 und R8 an D1

| Prüfung | p3d17 / Modell vor Build | Variante 24 Modell | Variante 24 tatsächlicher Mesh-Prüfer | Vorgabe |
|---|---:|---:|---:|---:|
| D1 R3 längs/quer/Wölbung | offiziell 6/17/19 | 6/7/7 | **6/5/6** | ≤6/≤7/≤7 |
| größter D1-Einzelquerwert | 20,002199 % in p3d17 | ≤20 % | **19,999708 %** | ≤20 % |
| R8-Stufe bei 152.5|28.5 | p3d17 0,080 m | 0,076068882 m | **0,076069355 m** | ≤0,116 m |
| R8-Gitter am Zielkreuz | p3d17 0,020 m | 0,020000000000032 m | **0,020000531 m** | ≤0,020 m |
| R8-Querneigung am Zielkreuz | p3d17 Grenze 3,0 % | 2,999999999999826 % | **3,000002241 %** | ≤3,0 % |
| Achsstützen | p3d17 max. Abweichung 0,000475 m | 359 innerhalb ±0,02 m | max. 0,020000000000032 m, 0 Stützen über 0,02 m laut Builddiagnostik | ±0,02 m |

D1-R3 besteht mit dem offiziellen Mesh-Prüfer. Der maximale Einzelquerwert bleibt um 0,000292 Prozentpunkte unter 20 %. Am R8-Zentrum sind Stufe und R3 erfüllt; Gitter überschreitet die verlangte 0,020-m-Grenze um 0,000000531 m und Querneigung die 3-%-Grenze um 0,000002241 Prozentpunkte. Der unveränderte R8-Prüfer rundet die Querneigung auf 3,0 % aus und meldet deshalb einen R8_quer-Treffer; die ungerundete Rechnung bestätigt, dass der harte Grenzwert knapp überschritten wird. Diese Werte werden als verfehlt berichtet, nicht als Rundungserfolg.

Am gesonderten D1-Endpunkt 156.5|37.5 misst R8 eine Stufe von **0,135 m** statt höchstens 0,054 m wie p3d11; ein R8a-Treffer liegt dort nicht vor. Bei der Zielkreuzung gibt es keinen R8a-Treffer, aber einen R8-Quertreffer. G1 und D2 haben null R8- und R8a-Treffer.

Die offiziellen D1-R3-Treffer mit Feinpunkt, Abschnittsstation, Soll- und Meshhöhe sowie nächster Station der jeweils anderen Rampe sind in [r3_d1_hits.csv](bilder_p3d18/nachher/r3_d1_hits.csv) dokumentiert. Der R8-Treffer und die ungerundeten Messwerte am Kreuzungszentrum stehen in [r8_d1_hits.csv](bilder_p3d18/nachher/r8_d1_hits.csv).

## Zahlen je Regel und Kachel

Die R1–R7/G-Regelsumme ist 596 für den p3d17-Ausgang und 577 im Variante-24-Mesh (−19). Vier bildabhängige T2–T5-Prüfvermerke sind in beiden Summen offen und wurden nicht als bestanden markiert. Die vollständige Einzelregelübersicht zeigt p3d17 → p3d18, Delta und D1/G1/D2 je Kachel:

| Regel | p3d17 | p3d18 | Δ | D1 p3d17→18 | G1 p3d17→18 | D2 p3d17→18 |
|---|---:|---:|---:|---:|---:|---:|
| G2_spitze_oben | 3 | 3 | +0 | 0→0 | 0→0 | 0→0 |
| G2_spitze_oben_fein | 8 | 8 | +0 | 0→0 | 0→0 | 0→0 |
| G3_spitze_unten | 4 | 5 | +1 | 1→2 | 0→0 | 0→0 |
| G3_spitze_unten_fein | 2 | 2 | +0 | 0→0 | 0→0 | 0→0 |
| G5_beule_klippe | 69 | 69 | +0 | 2→2 | 0→0 | 0→0 |
| G6_facette | 219 | 223 | +4 | 3→7 | 3→3 | 0→0 |
| G7_wand_glatte_flaeche | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| G7b_wandkontur_feld | 25 | 25 | +0 | 1→1 | 0→0 | 0→0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| G7b_wandkontur_rauheit | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| R1_blind | 24 | 24 | +0 | 2→2 | 1→1 | 0→0 |
| R2_getrennt | 15 | 15 | +0 | 1→1 | 0→0 | 1→1 |
| R3_laengs_m | 35 | 35 | +0 | 6→6 | 1→1 | 0→0 |
| R3_quer_pct | 29 | 17 | -12 | 17→5 | 0→0 | 0→0 |
| R3_woelb_m | 31 | 18 | -13 | 19→6 | 0→0 | 0→0 |
| R4_rand | 1 | 0 | -1 | 1→0 | 0→0 | 0→0 |
| R5_loch | 25 | 22 | -3 | 8→5 | 0→0 | 0→0 |
| R5_spitze | 0 | 5 | +5 | 0→5 | 0→0 | 0→0 |
| R6_wasser_schnee | 4 | 4 | +0 | 0→0 | 3→3 | 0→0 |
| T1_fleckrand | 94 | 94 | +0 | 0→0 | 3→3 | 7→7 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |

R8-Ausgangswerte 9d3f8fc: 48 gesamt (Stufe/Gitter/Quer/Wegende 9/10/5/24). p3d17 ergab 46, Variante 24 ergibt 40:

| Regel | Ausgang 9d3f8fc | p3d17 | p3d18 | D1 p3d17→18 | G1 p3d17→18 | D2 p3d17→18 |
|---|---:|---:|---:|---:|---:|---:|
| R8_gitter | 10 | 10 | 8 | 2→0 | 0→0 | 0→0 |
| R8_quer | 5 | 4 | 5 | 0→1 | 0→0 | 0→0 |
| R8_stufe | 9 | 9 | 7 | 2→0 | 0→0 | 0→0 |
| R8a_wegende | 24 | 23 | 20 | 3→0 | 0→0 | 0→0 |

R9-Ausgangswerte 9d3f8fc: 334 gesamt (Delle/Sägezahn/Wellen 25/34/275). p3d17 ergab 344, Variante 24 ergibt 341. Damit liegen R9 gesamt und R9w im Variante-24-Mesh **7 Treffer über dem ausdrücklich genannten Ausgangswert**; die +5-Grenze ist hier verfehlt, obwohl R9w gegenüber p3d17 um 5 sinkt:

| Regel | Ausgang 9d3f8fc | p3d17 | p3d18 | D1 p3d17→18 | G1 p3d17→18 | D2 p3d17→18 |
|---|---:|---:|---:|---:|---:|---:|
| R8b_delle | 25 | 23 | 25 | 1→3 | 0→0 | 0→0 |
| R9_saegezahn | 34 | 34 | 34 | 1→1 | 1→1 | 0→0 |
| R9w_wellen | 275 | 287 | 282 | 27→23 | 12→12 | 0→0 |

Für D2 kamen in pruefe_regeln keine Treffer neu hinzu. D2 ist außerdem in R8 und R9 weiterhin bei 0. Bei den übrigen p3d17→p3d18 Regelvergleichen ist der größte Zuwachs +5 bei R5_spitze; G6_facette steigt um 4. Der R9w-Gesamtanstieg von +7 gegenüber 9d3f8fc bleibt davon als ausdrückliche Ausnahme oberhalb der allgemeinen +5-Grenze stehen.

## Bildprüfung, Regressionen und Tests

Vorher-/Nachher-Bilder wurden bei derselben Auflösung 1000×700 selbst geprüft. Die sechs Pflichtbilder liegen unter [bilder_p3d18/nachher](bilder_p3d18/nachher); p3d17-Vergleichsbilder unter bilder_p3d17/nachher. D1-Kreuzung und Rampe-11-Streiflicht zeigen weiterhin sichtbare Faltungen und facettierte Übergänge; die Vorgabe einer weichen Fläche ohne Welle/Falte/Knick ist **nicht erreicht**. Die Clay-Bildindikatoren steigen p3d17→p3d18 in 13 Einträgen. D1-Kreuzung: Facetten 566→879, Kanten-Zähne 344→725, normale Sprünge 756→1471. D1-Wandfuß 140|35: Facetten 719→1020 und normale Sprünge 3597→4347. Diese Bildmetriken sind Proxys; die Bilder selbst sind gespeichert.

Die geforderten Vergleiche liefern keine Null-Anstiege:

| Vergleich | Gate-/Regelanstiege | Clay-Bildanstiege | Gesamt |
|---|---:|---:|---:|
| VAR0 → p3d18 | 11 | 25 | 36 |
| p3d6 → p3d18 | 8 | 21 | 29 |
| p3d8 → p3d18 | 8 | 18 | 26 |
| p3d16 → p3d18 | 7 | 18 | 25 |
| p3d17 → p3d18 | 5 | 13 | 18 |

Vollständige Delta-Berichte und JSONs liegen in bilder_p3d18/. Die D1-Werte verschlechtern sich gegenüber p3d8 bei G6_facette (0→7), R8b_delle (0→3) und R9w_wellen (21→23); Sägezahn bleibt bei 1. G1 und D2 bleiben meshgleich.

| Prüfung | Ergebnis |
|---|---:|
| Xvfb-Lochscan | 9 Meshes, 88.728 Geländedreiecke, 0 offene Innenkanten, 0 Punkte |
| pruefe_t42u.py | Summe 0; alle Abweichungsfelder 0 |
| pytest -q neu/tests/test_gelaende_mesh.py | 4 bestanden |
| pytest -q neu/tests | 26 bestanden, 5 fehlgeschlagen; Suite nicht grün |

Die fünf Suite-Fehler sind die unveränderten Prüfungen für allgemeine R8a-Wegenden, D1-Sägezahn, D1-Wandkantenschärfe, F1/C1-Wegende und Schattenbild-Hochfrequenz. Die Zielzahl ≥26/5 ist erreicht.

## Annahmen, Grenzen und offene Punkte

- Die Machbarkeit gilt für das linearisierte Transfermodell und wurde am tatsächlich exportierten Mesh nachgeprüft. Der Float32-Transfer überschreitet R8-Gitter und R8-Quer knapp; kein Grenzwert wurde angepasst.
- Die minimale Modellstufe ist unter den formulierten Modellbedingungen bewiesen. Wegen der gemessenen Meshabweichung ist sie kein Beleg, dass alle Endziele gleichzeitig im exportierten Mesh eingehalten sind.
- Die Achsstützen liegen bis auf 3,2×10⁻¹⁴ m numerische Differenz an der ±0,02-m-Grenze; Builddiagnostik zählt 0 Stützen außerhalb. Die R8-Abweichungen von 5,31×10⁻⁷ m und 2,24×10⁻⁶ Prozentpunkten sind ebenfalls klein, aber gegenüber den strikten Limits dennoch als Überschreitung gewertet.
- Die verlangte minimale Stufe ist 0,076068882 m; die Mesh-Grenzen, D1-Endpunkt, R9w-Ausgangsdelta, mehrere Delta-Nullziele und die Clay-/Streiflicht-Weichheit sind nicht erreicht. Es wurde keine weitere Variante erfunden.
- Zellquellwerte, Overlay, Wegführung und D2 blieben unverändert. Ebenenkernradius bleibt 2,00 m. Prüfer und Schwellen wurden nicht geändert. Laufzeitnachweis: /workspace/codex_jobs/log_p3d18.txt (gpt-6-luna, xhigh). Kosten: 0 EUR.
