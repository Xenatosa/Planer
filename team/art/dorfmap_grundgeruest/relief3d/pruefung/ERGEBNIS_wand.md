# Ergebnis Wandstreifen (TAG `wand`)

Stand: 2026-11-03 · Referenz: Branch-Ausgang `9d3f8fc`

## Ergebnis

Die gewählte Standardvariante glättet das Feinband mit σ=1,0 m und erweitert es auf trockene Steilzonen. R9s sinkt kartenweit von 47 auf 36 Treffer. D1 sinkt von 1 auf 0; G1 bleibt bei 1. Das Ziel ist **teilweise erreicht**. Die verlangten Rückgänge von `G5_beule_klippe`, `G6_facette` und dem bestehenden `R9_saegezahn` wurden mit dieser Variante nicht erreicht.

## Messung der Streifenursache

Die Messung verwendet `GB` als gerenderte Groboberfläche, ergänzt um die gespeicherten `FW`-Höhen. Beide Oberflächen werden mit dem Dreiecks-Split des Viewers auf 0,25 m abgetastet. Der neue Detektor berechnet die periodische Änderung der Normalenrichtung auf trockenen Flächen mit Neigung >1. Als Treffer gelten RMS-Winkelabweichung >10°, Periode 0,25 bis <2 m, mindestens 64 Stichprobenpaare und Korrelation ≥0,53.

| Kachel | Oberfläche vor Änderung | Periode | Winkelabweichung | Korrelation | Bandrand p95 / max. Höhenversatz |
|---|---|---:|---:|---:|---:|
| D1 | GB-Raster-Gegenprobe, beste Richtung | 0,35 m | 29,1° | 0,851 | 0 / 0 m |
| D1 | tatsächliches GB+FW-Netz | 0,25 m | 40,1° | 0,715 | 0 / 0 m |
| G1 | GB-Raster-Gegenprobe, beste Richtung | 0,25 m | 14,7° | 0,880 | 0 / 0 m |
| G1 | tatsächliches GB+FW-Netz | 0,25 m | 27,2° | 0,767 | 0 / 0 m |

Die Raster-Gegenprobe ist bereits periodisch; das gerenderte Netz verstärkt die Abweichung. Ein Höhenversatz an der Grob/Fein-Naht wurde in D1 und G1 nicht gemessen (p95 und Maximum 0 m). Die Messung spricht deshalb für periodische Höhen-/Rasterfacetten und gegen eine T-Naht als Ursache. Sie trennt Rasterdiagonale und Höhenfeld nicht vollständig voneinander.

## Änderung

- `gen_relief.py` ergänzt nach den vorhandenen Reliefschritten eine optionale Feinband-Erweiterung und normierte Gaußglättung der Feinbandhöhen. Standard: `WANDSTREIFEN=1`, `WANDSTREIFEN_SIG=1.0`, `WANDSTREIFEN_FELDER=*`, `WANDSTREIFEN_GROBSIG=0`.
- Wasser und Wege bleiben ausgenommen. Die Bandrandhöhen werden anschließend wieder exakt an die Groboberfläche gepinnt.
- D2 und ein Zellrand darum sind von der neuen Erweiterung und Glättungsmaske ausgenommen. D2 ist unveränderte Regressionsbasis.
- `pruefung/r9_wandstreifen.py` ergänzt R9s mit Ergebnissen pro Kachel sowie Raster-Gegenprobe, Feinband-Innenmessung und Nahtmessung.
- `main.js`, Wegbandlogik und Schattenlogik wurden nicht geändert.

Feinbandzellen: 26.919 → 44.660 (+17.741); gespeicherte Feinbandpunkte: 439.895 → 729.557 (+289.662). D2 enthält vor und nachher keine Feinbandzellen; die 17 Feinbandpunkte im D2-Ausschnitt stimmen bitgenau überein. Der maximale absolute Höhenunterschied durch die Glättung beträgt 7,545 m.

## Regeln vor/nachher

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
| G2_spitze_oben_fein | 8 | 7 | -1 |
| G3_spitze_unten_fein | 2 | 2 | 0 |
| G5_beule_klippe | 66 | 66 | 0 |
| G6_facette | 249 | 251 | +2 |
| G7_wand_glatte_flaeche | 1 | 1 | 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| G11_objekt_schwebt_sinkt | 0 | 5 | +5 |
| T1_fleckrand | 94 | 94 | 0 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | 0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| G7b_wandkontur_feld | 23 | 23 | 0 |

`pruefe_regeln` gesamt: 596 → 602 (+6). Kein einzelner Prüfschlüssel steigt um mehr als +5; `G11_objekt_schwebt_sinkt` liegt genau an der erlaubten Grenze. `G5` sinkt nicht, `G6` steigt um 2. Der bestehende `R9_saegezahn` bleibt bei 34.

| Prüflauf / Regel | Vorher | Nachher | D1 vorher → nachher | G1 vorher → nachher | D2 vorher → nachher |
|---|---:|---:|---:|---:|---:|
| `pruefe_regeln` | 596 | 602 | 36 → 37 | 13 → 14 | 8 → 8 |
| R8 gesamt | 48 | 49 | 8 → 8 | 1 → 1 | 0 → 0 |
| R9 gesamt | 334 | 334 | 26 → 26 | 8 → 8 | 0 → 0 |
| R9s_wandstreifen | 47 | 36 | 1 → 0 | 1 → 1 | 0 → 0 |

R8-Regeln: `R8_stufe` 9→10, `R8_gitter` 10→10, `R8_quer` 5→4, `R8a_wegende` 24→25. R9-Regeln: `R8b_delle` 25→25, `R9_saegezahn` 34→34, `R9w_wellen` 275→275. Die zusätzlichen `pruefe_regeln`-Treffer in D1 und G1 sind je ein `G6_facette`; D2 erhält keinen neuen Treffer.

R9s-Winkelmessung nach Änderung: D1 0,25 m / 31,1° / Korrelation 0,510 (kein Treffer); G1 0,25 m / 20,4° / 0,649 (Treffer). Der Raster-Gegenprobe-Zähler bleibt bei 47; der tatsächliche Netz-Zähler sinkt von 47 auf 36. Die Nahtmessung hat kartenweit p95=0 m und Maximum=0 m.

## Weitere Prüfungen

- Lochscan: 7 Meshes, 2.140.988 Geländedreiecke, 0 offene Innenkanten im Karteninneren, 0 Punkte.
- Lod1: 1.291.157 gerenderte Dreiecke (<1,3 Mio.).
- `index.html`: 16.483.334 → 19.688.490 Byte (+19,44 %, unter +30 %).
- `pruefe_t42u.py`: Summe 0; alle Teilabweichungen 0.
- Eingabe-/Quellfelder `G`, `WV`, `WEGA`, Zellspalten und Reihenfolge sind gegenüber dem Vorher-Export identisch. `zellen_relief.csv` ist unverändert. `GB` und `FW` im D2-Ausschnitt sind identisch.

## Varianten, Annahmen und Grenzen

- Eine optionale Grobglättung mit σ=0,5 m bzw. 1,0 m senkte in den Explorationsläufen G5/G6, erhöhte aber `G7b_wandkontur_feld` um 7 bzw. 9 und wurde verworfen. Sie ist nicht Standard.
- Die Korrelationsschwelle 0,53 und Mindeststichprobe 64 sind Messannahmen, weil „periodisch“ keine numerische Korrelation vorgibt. Der Detektor prüft vier Rasterrichtungen und nicht die lokale Wandkante als kontinuierliche Tangente; unregelmäßige oder schräg verlaufende Streifen können daher über- oder unterzählt werden.
- Die Glättung reduziert die gemessene Periodizität, beseitigt aber die Winkelabweichungen nicht überall. G1 bleibt R9s-Treffer. Eine Vorher/Nachher-Bildaufnahme wurde nicht erstellt; die visuelle Wirkung ist daher nicht unabhängig bewertet.
- `G11` steigt um 5 und `G6` um 2. Die Ursache dieser neuen Treffer ist offen. Das verlangte gemeinsame Ziel ist somit nicht vollständig erreicht.
