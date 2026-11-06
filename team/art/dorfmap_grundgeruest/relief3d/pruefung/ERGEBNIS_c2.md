# Ergebnis C2 – Terrassenhang

Stand: 03.11.2026 · Branch `art/dorfmap-c2` · Vergleichsbasis `9d3f8fc`

## Ergebnis

Der sichtbare Nordhang in C2 ist lokal geglättet. Der gemessene Anteil stufenartiger Hangprofile sank von 5,199 % auf 2,362 %. Das C2-Gesamtgate hat das Soll 0 nicht erreicht: `pruefe_regeln` steht in C2 bei 7 Treffern, R8 bei 1 und R9 bei 4. Die unveränderte Rampenüberlagerung verursacht am Endpunkt (118,9; 43,3) weiterhin `R1_blind` und `R8a_wegende`. R9 meldet weiter drei Hangwellen und einen Sägezahn in C2.

## Änderung

`gen_relief.py` glättet mit `C2TERR=1` (Standard, σ=1 m) das trockene Gelände im C2-Nordhangband `x=84..126`, `z=43..56`. Straßen und Wasser bleiben ausgespart. Ein 3-m-Smoothstep an den Kachelrändern sowie ein 2,5-m-Fade am Bandrand halten die Übergänge weich. Das sichtbare Grobhöhenfeld `GB` und die Höhen des Feinmesh erhalten dieselbe interpolierte Korrektur.

`C2TERR=0` schaltet die Änderung aus. Das quellgebundene Höhenfeld `G`, die Zellwerte, das Straßen-/Rampenoverlay und `zellen_relief.csv` bleiben unverändert. Im finalen Build änderten sich 2.074 `GB`-Vertices und 4.765 Feinmesh-Höhen; die maximale Höhenänderung beträgt 1,221 m.

## Terrassenmessung C2

Die Hangmaske folgt dem vorhandenen O18-Diagnoseansatz: 5-m-Mittelneigung zwischen 0,35 und 1,2; ein Stufenprofil liegt vor, wenn die lokale Neigung kleiner als 35 % dieses Mittelwerts ist. Der 0,5-m-Nachbarschritt wird zwischen Hangpunkten gemessen. Kantenschärfe ist das P95 des Betrags des diskreten Laplaceoperators; Flächengleichmaß ist die Standardabweichung von `GB − Gauss(GB, σ=2 m)` im Hang.

| Messwert | Vorher | Nachher |
|---|---:|---:|
| Stufenprofile, Anteil der Hangpunkte | 5,199 % | 2,362 % |
| Höhenänderung benachbarter 0,5-m-Punkte, P95 | 0,530 m | 0,511 m |
| Höhenänderung benachbarter 0,5-m-Punkte, Maximum | 1,201 m | 0,835 m |
| Kantenschärfe, Laplace-P95 | 2,333 m⁻¹ | 1,664 m⁻¹ |
| Hochpass-Streuung im Hang, σ=2 m | 0,453 m | 0,426 m |
| Punkte in der Hangmaske | 1.231 | 1.270 |

Die Stichprobenmaske ändert sich durch die Glättung. Die Messwerte zeigen eine Verbesserung, belegen aber nicht alle Sollwerte aus LF02/LF03/TR05. Insbesondere ist R9w in C2 nicht auf 0 gefallen.

## Gate-Zähler je Regel

| Prüfer | Regel | Vorher | Nachher | Änderung |
|---|---|---:|---:|---:|
| `pruefe_regeln` | R1_blind | 24 | 24 | 0 |
| `pruefe_regeln` | R2_getrennt | 15 | 15 | 0 |
| `pruefe_regeln` | R3_laengs_m | 35 | 35 | 0 |
| `pruefe_regeln` | R3_quer_pct | 23 | 23 | 0 |
| `pruefe_regeln` | R3_woelb_m | 22 | 22 | 0 |
| `pruefe_regeln` | R5_loch | 17 | 17 | 0 |
| `pruefe_regeln` | R6_wasser_schnee | 4 | 4 | 0 |
| `pruefe_regeln` | G2_spitze_oben | 3 | 3 | 0 |
| `pruefe_regeln` | G2_spitze_oben_fein | 8 | 8 | 0 |
| `pruefe_regeln` | G3_spitze_unten | 3 | 3 | 0 |
| `pruefe_regeln` | G3_spitze_unten_fein | 2 | 2 | 0 |
| `pruefe_regeln` | G5_beule_klippe | 66 | 65 | −1 |
| `pruefe_regeln` | G6_facette | 249 | 248 | −1 |
| `pruefe_regeln` | G7_wand_glatte_flaeche | 1 | 1 | 0 |
| `pruefe_regeln` | G7b_wandkontur_rauheit | 1 | 1 | 0 |
| `pruefe_regeln` | G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| `pruefe_regeln` | G7b_wandkontur_feld | 23 | 24 | +1 |
| `pruefe_regeln` | G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| `pruefe_regeln` | T1_fleckrand | 94 | 94 | 0 |
| `pruefe_regeln` | T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| `pruefe_regeln` | T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| `pruefe_regeln` | T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| `pruefe_regeln` | T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |
| `r8_kreuzung` | R8_stufe | 9 | 9 | 0 |
| `r8_kreuzung` | R8_gitter | 10 | 10 | 0 |
| `r8_kreuzung` | R8_quer | 5 | 5 | 0 |
| `r8_kreuzung` | R8a_wegende | 24 | 24 | 0 |
| `r9_form` | R8b_delle | 25 | 25 | 0 |
| `r9_form` | R9_saegezahn | 34 | 34 | 0 |
| `r9_form` | R9w_wellen | 275 | 275 | 0 |

Die Gesamtsummen sind `pruefe_regeln` 596→595, R8 48→48 und R9 334→334. Keine Regel steigt um mehr als 1.

## Zähler je Kachel

Werte sind `vorher → nachher`; `pruefe_regeln` / R8 / R9 werden getrennt gezählt.

| Kachel | `pruefe_regeln` | R8 | R9 |
|---|---:|---:|---:|
| B2 | 3 → 3 | 0 → 0 | 7 → 7 |
| C1 | 6 → 6 | 0 → 0 | 5 → 5 |
| C2 | 8 → 7 | 1 → 1 | 4 → 4 |
| C3 | 42 → 42 | 4 → 4 | 19 → 19 |
| D2 | 8 → 8 | 0 → 0 | 0 → 0 |
| D1 | 36 → 36 | 8 → 8 | 26 → 26 |
| G1 | 13 → 13 | 1 → 1 | 8 → 8 |

In C2 gingen `G5_beule_klippe` (1→0) und ein `G6_facette`-Treffer (4→3) zurück. Ein `G7b_wandkontur_feld` kam hinzu (0→1); `R1_blind` (1), `T1_fleckrand` (2), R8a (1) und R9 (4) bleiben. Für D2 kam in `pruefe_regeln` kein Treffer hinzu; die dortigen 8 bestehenden Treffer sind dieselben Einträge wie vorher.

## Naht und D2-Nachweis

`G`, `GB`, `WV` und alle 17 Feinmesh-Höhen in D2 sind bytegleich zum Stand `9d3f8fc`. SHA-256 der D2-Ausschnitte: `G` `325f6fe2f41178f7e9c4b2198881438bc5ac70649ac4a0ee9836b463e6e1408c`; `GB` `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`; Feinmesh-Höhen `5f6e029e43d8964603baa9a5b1ff13fcc42d4a7f7551c069c1d4d56f17457dcb`. Das globale `G`, `WV`, `WEGA`, `wege` und `rampenwege` sind ebenfalls bytegleich beziehungsweise inhaltlich unverändert.

| Naht | maximale Höhenänderung am Rand | maximale Änderung des 0,5-m-Querschritts |
|---|---:|---:|
| B2/C2 | 0 m | 0 m |
| C2/D2 | 0 m | 0,00046 m |
| C1/C2 | 0 m | 0 m |
| C2/C3 | 0 m | 0 m |

## Pflichtprüfungen

| Prüfung | Ergebnis |
|---|---|
| `python3 gen_relief.py && python3 baue_html.py` | erfolgreich |
| `sh pruefung/export_gate.sh` | ROT: bestehende Treffer; Zähler 595 / 48 / 334 |
| Raycast `loch_o18g.js` | 0 offene Innenpunkte; 1.700.454 Dreiecke gesamt |
| t42u (`pruefe_t42u.py`) | Summe 0 |
| LOD1 (`test_dreiecke_l1.js`) | 1.174.328 Dreiecke, unter 1,3 Mio. |
| `zellen_relief.csv` nach Build | auf Branch-Stand zurückgesetzt |

## Annahmen, Grenzen und offene Punkte

- PLAN_O18_NEU.md führt C2-Terrassen als ungemessen. Mangels eigener Terrassenmaske ist das Nordhangband `z=43..56` die angenommene Mess- und Bearbeitungsfläche; die ganze Kachel wurde nicht geglättet.
- Das vollständige Ziel „C2 im Gate 0“ ist nicht erreicht. Das Overlay bleibt unverändert und verursacht am Rampenende die Treffer `R1_blind` und `R8a_wegende`. Zusätzlich bleiben in C2 G6-, T1-, R9- und R9w-Treffer.
- `r9_form.py` wertet `G` aus. `G` bleibt wegen des geforderten t42u-Abgleichs quellgleich; die sichtbare Glättung liegt in `GB` und Feinmesh. Der R9-Zähler kann die sichtbare Korrektur daher nicht abbilden.
- Die Messwerte sind lokale Formindikatoren, keine vollständige Prüfung aller LF02/LF03/TR05-Sollwerte. Die Regelwerksanforderung R9w=0 ist für C2 weiterhin offen.
- Für einen echten C2-Gatewert 0 müssten zumindest Overlay-Wegende und weitere bestehende Form-/Texturtreffer neu eingeordnet oder bearbeitet werden. Diese Änderung hat sie nicht verändert.
