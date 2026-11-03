# Ergebnis K10 – Rampenrillen

Stand: `art/dorfmap-rillen`, Ausgang `9d3f8fc`; Generatorlauf am 03.11.2026.

## Ergebnis

Die gemessene hochfrequente Quer-Restwelligkeit sinkt auf allen 13 im Relief enthaltenen Rampen. Ihr Median über die Rampen sinkt von 0,95 cm auf 0,60 cm (−37 %). Das ist eine messbare Minderung; eine vollständige visuelle Beseitigung der Rillen ist damit nicht belegt. Besonders die Kehre C3 und einzelne D1-Übergangsstellen behalten erhöhte Restwerte.

## Änderung und Varianten

`gen_relief.py` filtert Höhenwerte ausschließlich im Feinband innerhalb von 2,5 m zur Rampenmittellinie. Der Gaußfilter wirkt quer zur lokalen Rampenachse; die Mittellinie und das Grobnetz `G_ANZ` bleiben unverändert. Die Änderung wird mit einem weichen Gewicht auf die Feinbandhöhen angewandt. Anschließend werden die 18.414 Feinband-Randpunkte wieder exakt an das Grobnetz gebunden.

Varianten über `RILLEN_Q`:

- `0`: aus
- `0.50`: Filter-Sigma 0,50 m; `G6_facette` steigt um 4
- `0.75`: Filter-Sigma 0,75 m; Standard, stärkste gemessene Minderung; `G6_facette` steigt um 5

Beide aktiven Varianten hielten die Grenze von höchstens +5 je Regel ein. Die stärkere Variante ist Standard. Sie bearbeitete 45.808 Feinbandpunkte; an 41.258 änderte sich die Höhe um mehr als 1 mm. Die größte Einzeländerung beträgt 1,0625 m und liegt seitlich im steilen Feinband. Die nachfolgende Nahtkorrektur setzte die Randhöhen wieder exakt auf das Grobnetz; ihre größte Korrektur vor dem Zurücksetzen betrug 0,068 m.

## Ursachenmessung

Das Grobnetz hat 0,5-m-Abstand, das Feinband 0,25 m. Im Handy-LOD `?lod=1` werden sie mit 1,0 m beziehungsweise 0,5 m abgetastet. Gemessen wurden Querstreifen von ±2 m zur Rampe, alle 0,25 m entlang der Mittellinie. Für die Quer-Restwelligkeit wurde zunächst der lineare Querfall abgezogen, danach der Anteil unter 0,5 m Quer-Skala herausgefiltert; angegeben ist der Median des RMS je Rampenstation. Die Fein/Grob-RMS-Spalte misst die Höhenabweichung beider Raster auf denselben abgedeckten Feinbandpunkten im Handy-LOD. Sie enthält auch natürliche Wandform und ist daher kein reines Maß der Rillentiefe.

| Rampe | Kachel | Länge m | Feinband-Abdeckung | Quer-Restwelligkeit RMS, cm vorher → nachher | Fein/Grob-RMS, cm vorher → nachher |
|---:|:---:|---:|---:|---:|---:|
| 0 | C1 | 54,0 | 99,9 % | 1,01 → 0,48 | 1,43 → 1,28 |
| 1 | F1 | 49,0 | 100,0 % | 0,96 → 0,45 | 1,51 → 1,22 |
| 2 | D1 | 49,0 | 99,5 % | 1,06 → 0,60 | 14,52 → 12,64 |
| 3 | D6 | 77,0 | 99,7 % | 0,62 → 0,35 | 2,17 → 2,01 |
| 4 | G6 | 56,0 | 85,4 % | 0,94 → 0,79 | 2,50 → 2,30 |
| 5 | C6 | 52,0 | 42,2 % | 0,63 → 0,56 | 1,74 → 1,27 |
| 6 | C5 | 41,0 | 98,1 % | 0,58 → 0,57 | 1,50 → 1,25 |
| 7 | D4 | 43,0 | 96,8 % | 0,57 → 0,54 | 1,49 → 1,36 |
| 8 | C4 | 36,0 | 97,6 % | 0,95 → 0,71 | 54,17 → 54,16 |
| 9 | G4 | 43,0 | 75,2 % | 1,08 → 0,86 | 2,00 → 1,69 |
| 10 | H5 | 24,0 | 97,5 % | 0,82 → 0,66 | 1,21 → 1,02 |
| 11 | D1 | 47,5 | 90,1 % | 1,38 → 1,31 | 14,41 → 13,15 |
| 12 | C3 | 37,2 | 100,0 % | 6,49 → 4,29 | 14,13 → 13,49 |

Die mittlere Fein/Grob-RMS je Rampe sinkt von 2,00 cm auf 1,69 cm. Die großen Restwerte in C4, D1 und C3 liegen in steiler oder stark wechselnder Wandform; der Filter ändert diese Bereiche nur wenig. Die Endwerte bestätigen daher die Rasterabweichung als einen Anteil, aber nicht als alleinige Ursache sämtlicher sichtbarer Linien.

## Regeln und Regressionen

Ausgangswerte entsprechen den vorgegebenen Werten von `9d3f8fc`. Nicht aufgeführte Trefferzahlen ändern sich nicht.

| Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| R1_blind | 24 | 24 | 0 |
| R2_getrennt | 15 | 15 | 0 |
| R3_laengs_m | 35 | 35 | 0 |
| R3_quer_pct | 23 | 23 | 0 |
| R3_woelb_m | 22 | 22 | 0 |
| R5_loch | 17 | 17 | 0 |
| R6_wasser_schnee | 4 | 4 | 0 |
| G2_spitze_oben | 3 | 3 | 0 |
| G3_spitze_unten | 3 | 3 | 0 |
| G2_spitze_oben_fein | 8 | 8 | 0 |
| G3_spitze_unten_fein | 2 | 2 | 0 |
| G5_beule_klippe | 66 | 66 | 0 |
| G6_facette | 249 | 254 | **+5** |
| G7_wand_glatte_flaeche | 1 | 1 | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | 0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| G7b_wandkontur_feld | 23 | 23 | 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| T1_fleckrand | 94 | 94 | 0 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |
| **pruefe_regeln Summe** | **596** | **601** | **+5** |
| R8_stufe | 9 | 9 | 0 |
| R8_gitter | 10 | 10 | 0 |
| R8_quer | 5 | 5 | 0 |
| R8a_wegende | 24 | 24 | 0 |
| **R8 Summe** | **48** | **48** | **0** |
| R8b_delle | 25 | 25 | 0 |
| R9_saegezahn | 34 | 34 | 0 |
| R9w_wellen | 275 | 275 | 0 |
| **R9 Summe** | **334** | **334** | **0** |

Kachelzahlen für D1, G1 und D2; jeweils vorher → nachher:

| Prüfung | D1 | G1 | D2 |
|---|---:|---:|---:|
| `pruefe_regeln` Summe | 36 → 36 | 13 → 13 | 8 → 8 |
| R8 Summe | 8 → 8 | 1 → 1 | 0 → 0 |
| R9 Summe | 26 → 26 | 8 → 8 | 0 → 0 |

Einzelregeln je Kachel, ebenfalls vorher → nachher:

| Regel | D1 | G1 | D2 |
|---|---:|---:|---:|
| R1_blind | 2 → 2 | 1 → 1 | 0 → 0 |
| R2_getrennt | 1 → 1 | 0 → 0 | 1 → 1 |
| R3_laengs_m | 6 → 6 | 1 → 1 | 0 → 0 |
| R3_quer_pct | 11 → 11 | 0 → 0 | 0 → 0 |
| R3_woelb_m | 10 → 10 | 0 → 0 | 0 → 0 |
| G3_spitze_unten_fein | 0 → 0 | 1 → 1 | 0 → 0 |
| G5_beule_klippe | 1 → 1 | 0 → 0 | 0 → 0 |
| G6_facette | 5 → 5 | 4 → 4 | 0 → 0 |
| R6_wasser_schnee | 0 → 0 | 3 → 3 | 0 → 0 |
| T1_fleckrand | 0 → 0 | 3 → 3 | 7 → 7 |
| R8_stufe | 2 → 2 | 0 → 0 | 0 → 0 |
| R8_gitter | 2 → 2 | 0 → 0 | 0 → 0 |
| R8_quer | 1 → 1 | 0 → 0 | 0 → 0 |
| R8a_wegende | 3 → 3 | 1 → 1 | 0 → 0 |
| R8b_delle | 2 → 2 | 1 → 1 | 0 → 0 |
| R9_saegezahn | 1 → 1 | 1 → 1 | 0 → 0 |
| R9w_wellen | 23 → 23 | 6 → 6 | 0 → 0 |

D1 hat damit weiterhin R1 2, R2 1, R3 längs 6, R3 quer 11, R3 Wölbung 10, G5 1, G6 5, R8 8 und R9 26 Treffer. G1 hat R1 1, R3 längs 1, G3 fein 1, G6 4, R6 3, T1 3, R8 1 und R9 8. D2 hat R2 1 und T1 7 Treffer; **kein Treffer kam in D2 neu hinzu**. Die fünf zusätzlichen G6-Treffer sind Nettozuwächse außerhalb von D1, G1 und D2.

## Pflichtprüfungen

| Prüfung | Ergebnis |
|---|---|
| `python3 gen_relief.py && python3 baue_html.py` | Erfolgreich; zwei identische Läufe. SHA-256 `relief_daten.json.gz`: `518f3980a44efbc48c9da81ed1b8b9b3a2c7c55730591e60a3350e4c46d1efe1`; `index.html`: `7049bef662da85bfa32c5e1cd5c49f6cc4f7d09a6c30174e808b8cf223500766` |
| `pruefe_t42u.py` | Summe 0 |
| Handy-LOD `?lod=1`, 390×844 | 1.174.326 sichtbare Dreiecke einschließlich instanzierter Objekte; Grenzwert <1,3 Mio. erfüllt |
| Raycast `loch_o18g.js`, RAND=0.6 | 0 offene Innenkanten, 0 Punkte; Desktop-Szene 1.700.454 Dreiecke |
| D2 Anzeigehöhen gegen `9d3f8fc` | Bytegleich: Grobnetz-SHA-256 `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`; 17 Feinbandhöhen und ihre Vertex-IDs ebenfalls bytegleich |
| `sh pruefung/export_gate.sh` | Exit 1 / rot wegen vorhandener Regel-Treffer. Absolute Summen sind 601/48/334; gegenüber dem Ausgang steigen nur `G6_facette` und die Regelsumme um +5. |
| `zellen_relief.csv` | Nach beiden Builds unverändert zum Branch-Stand |

## Annahmen, Grenzen und offene Punkte

- Die Kachelzuordnung je Rampe verwendet den Schwerpunkt ihrer gespeicherten Mittellinie.
- Der Querfilter verändert Höhen im Feinband seitlich der Rampe, nicht die Weg-Höhenmischung oder das Overlay. Eine maximale Seitenänderung von 1,0625 m tritt in steilem Feinband auf.
- R3 längs, quer und Wölbung bleiben bei 35/23/22 Treffern. G6 steigt um den erlaubten Höchstwert +5.
- Die Kennzahl prüft Geometrie, nicht Schatten, Beleuchtung oder Textur. Ein Bildvergleich der Rampen vor/nachher bleibt offen. Die visuelle Zielerreichung ist deshalb teilweise und nicht vollständig bestätigt.
- Der C3-Quer-RMS-Median bleibt bei 4,29 cm; D1-Rampe 11 hat noch 10,81 cm Quer-RMS am 95. Perzentil. Weitere Glättung ist wegen des G6-Budgets und der großen Seitenänderungen nicht belegt.
