# Ergebnis R3

## Ergebnis

Die Änderung senkt `pruefe_regeln` von 570 auf 569 Treffer. `r8` bleibt bei 48 und `r9` bei 334; keine Regel steigt. Der geforderte Gesamtzustand ist **nicht erreicht**: Die Rampenbefunde R3 bleiben unverändert, dazu bleiben 24 echte blinde Rampenenden und 15 echte getrennte Wegkomponenten bestehen. Diese Topologie liegt im geschützten Overlay.

## Änderung

`gen_relief.py` nimmt jetzt mit `FALTRAMPEN` einen schaltbaren Schutzstreifen um Rampen aus dem abschließenden Hang-Faltschliff. Standard ist `FALTRAMPEN=1.5` m; erlaubt sind `0`, `1.5` und `3.5`. Das verhindert, dass der nachfolgende Hangschliff die bereits geformten Rampenprofile wieder verändert. Die übrigen Profil- und Endanschlussroutinen bleiben unverändert.

Der Standardlauf beseitigt einen `G6_facette`-Treffer. Er reduziert keine R3-Zähler. `pruefung/export_gate.sh` schreibt seine Prüfergebnisse nun mit `TAG` in eigene `/tmp`-Dateien und verwendet `LOCHSCAN`, damit der geforderte r3-Lauf keine gemeinsam verwendeten Ergebnisdateien überschreibt. Prüfer, Schwellen und Quellwerte wurden nicht geändert. Es wurde keine Wegmischung aus Branch `weg3` verwendet.

Zwei geprüfte Alternativen wurden verworfen: `FALTRAMPEN=3.5` ließ R3 unverändert und erhöhte `G6_facette` um 20. `RAMPENBAND=0` erhöhte `R3_quer` um 9, `G5_beule_klippe` um 8 und `G6_facette` um 8. Der Standard `FALTRAMPEN=1.5` ist von diesen Varianten der beste geprüfte Stand.

## Prüfergebnisse je Regel

| Prüfer / Regel | Vorher | Nachher | Änderung |
|---|---:|---:|---:|
| `pruefe_regeln` gesamt | 570 | 569 | -1 |
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
| G5_beule_klippe | 68 | 68 | 0 |
| G6_facette | 220 | 219 | -1 |
| G7_wand_glatte_flaeche | 1 | 1 | 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| T1_fleckrand | 94 | 94 | 0 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | 0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| G7b_wandkontur_feld | 24 | 24 | 0 |
| `r8` gesamt | 48 | 48 | 0 |
| R8_stufe | 9 | 9 | 0 |
| R8_gitter | 10 | 10 | 0 |
| R8_quer | 5 | 5 | 0 |
| R8a_wegende | 24 | 24 | 0 |
| `r9` gesamt | 334 | 334 | 0 |
| R8b_delle | 25 | 25 | 0 |
| R9_saegezahn | 34 | 34 | 0 |
| R9w_wellen | 275 | 275 | 0 |

Die `pruefe_regeln`-Summen enthalten auch die 26 G7b-Teiltreffer (Rauheit 1, Kantenschärfe 1, Feld 24). Keine einzelne Regel steigt, also bleibt jede innerhalb der Grenze von höchstens +5.

## Treffer je Kachel

Die R3-, R8- und R9-Angaben sind nach dem unveränderten Prüfer gruppiert. Für `pruefe_regeln` sind die aufgeführten Trefferarten die vollständige Aufteilung in D1, G1 und D2.

| Prüfer / Regel | D1 vorher → nachher | G1 vorher → nachher | D2 vorher → nachher |
|---|---:|---:|---:|
| `pruefe_regeln` gesamt | 36 → 35 | 13 → 13 | 8 → 8 |
| R1_blind | 2 → 2 | 1 → 1 | 0 → 0 |
| R2_getrennt | 1 → 1 | 0 → 0 | 1 → 1 |
| R3_laengs_m | 6 → 6 | 1 → 1 | 0 → 0 |
| R3_quer_pct | 11 → 11 | 0 → 0 | 0 → 0 |
| R3_woelb_m | 10 → 10 | 0 → 0 | 0 → 0 |
| G5_beule_klippe | 1 → 0 | 0 → 0 | 0 → 0 |
| G6_facette | 5 → 5 | 4 → 4 | 0 → 0 |
| R6_wasser_schnee | 0 → 0 | 3 → 3 | 0 → 0 |
| G3_spitze_unten_fein | 0 → 0 | 1 → 1 | 0 → 0 |
| T1_fleckrand | 0 → 0 | 3 → 3 | 7 → 7 |
| `r8` gesamt | 8 → 8 | 1 → 1 | 0 → 0 |
| R8_stufe | 2 → 2 | 0 → 0 | 0 → 0 |
| R8_gitter | 2 → 2 | 0 → 0 | 0 → 0 |
| R8_quer | 1 → 1 | 0 → 0 | 0 → 0 |
| R8a_wegende | 3 → 3 | 1 → 1 | 0 → 0 |
| `r9` gesamt | 26 → 26 | 8 → 8 | 0 → 0 |
| R8b_delle | 2 → 2 | 1 → 1 | 0 → 0 |
| R9_saegezahn | 1 → 1 | 1 → 1 | 0 → 0 |
| R9w_wellen | 23 → 23 | 6 → 6 | 0 → 0 |

Der D1-G5-Treffer bei `152.5|28.5` ist im Nachherlauf nicht mehr vorhanden; die globale Zahl `G5_beule_klippe` bleibt 68. Die Gesamtänderung von `pruefe_regeln` stammt aus einem weniger gezählten G6-Treffer außerhalb der hier einzeln ausgewiesenen D1/G1/D2-Änderung.

## Ursachenbewertung der Rampenbefunde

| Regel | Treffer | Einschätzung aus Geometrie-/Profilprüfung |
|---|---:|---|
| R1_blind | 24 | Alle 24 gemeldeten Enden sind echte blinde Enden: im 5×5-Nachbarschaftstest liegt kein anderer Wegabschnitt. Von 26 insgesamt geprüften Enden verbindet sich eines in 1,02 m mit einem anderen Abschnitt; eines liegt am Kartenrand bei z=2,5 m und ist ausgenommen. Die 24 gemeldeten Fälle würden eine Änderung am gesperrten Overlay benötigen. |
| R2_getrennt | 15 | Alle 15 Komponenten sind tatsächlich getrennt. Zellgrößen: 27, 38, 40, 43, 52, 58, 59, 59, 60, 74, 94, 116, 151, 1227 und 1588. Der Abstand zur Hauptkomponente beträgt 5,39–106,67 m. Verbinden würde eine Änderung der geschützten Wege-/Rampengeometrie erfordern. |
| R3_laengs_m | 35 | 23 Treffer liegen in den ersten oder letzten 4-m-Profilabschnitten und sind Randartefakte der `nearest`-Glättungsmessung. 12 mittlere Abschnitte zeigen echte Längsprofilabweichungen. Größter gemessener Ausschlag: 1,378 m bei rampe_11 nahe `153,7|26,1`. |
| R3_quer_pct | 23 | 3 Querschnitte liegen innerhalb 0,5 m eines anderen/nicht lokalen Rampenabschnitts; 4 Treffer liegen in Endabschnitten. Diese 7 sind als Messmehrdeutigkeit/Randartefakt klassifiziert. Die übrigen 16 sind echte Querprofilabweichungen. |
| R3_woelb_m | 22 | 3 Treffer liegen an nahen, nicht lokalen Rampenabschnitten; 4 in Endabschnitten. Diese 7 sind als Messmehrdeutigkeit/Randartefakt klassifiziert. Die übrigen 15 sind echte Wölbungsabweichungen. |

Die Ursachenbewertung ändert keine Zähler und keine Schwellen. Die echten R3-Abweichungen wurden mit diesem Stand nicht behoben; die Profiländerung per Rampenschutz änderte ihre Anzahl nicht. Die R1-/R2-Treffer bleiben wegen des unveränderlichen Overlay-Auftrags bestehen.

## Pflicht-Gates und Regression

- Build im Ordner `relief3d`: `python3 gen_relief.py && python3 baue_html.py` erfolgreich; `zellen_relief.csv` danach auf Branch-Stand zurückgesetzt und unverändert.
- Raycast: `meshes=7`, `dreiecke=1.700.454`, `offen_innen=0`; Lochprüfung 0.
- `export_gate.sh` mit `TAG=r3` und dem r3-Lochscan ausgeführt. Ergebnis `GATE ROT`, da die bestehenden Treffer weiter vorhanden sind; die Zähler erfüllen jedoch die Grenze „keine Regel über +5“.
- t42u: Summe 0, alle geprüften Zellwertdifferenzen 0.
- lod1: 1.174.554 gezeichnete Dreiecke, unter 1,3 Mio.
- D2 Zell- und Anzeigefelder wurden direkt gegen die Branch-Basis verglichen: `G`, `GB` und Feinband `vid/h/c/t/s` im D2-Ausschnitt sind bytegleich. Die D2-Treffer bleiben ebenfalls identisch: pruefe_regeln 8→8 ohne neue Treffer, r8 0→0, r9 0→0.
- D1-Klippenform bei ungefähr `140|35` und D1/G1-Wandkanten wurden in Vorher-/Nachher-Rendern betrachtet; die Klippe und Wandformen bleiben sichtbar, ohne neue Zacken oder eine geglättete Klippenkante. C3/D3 und D6 wurden ebenfalls verglichen.

Renderings stammen von `render_t119u.js index.html OUTDIR cams.json '?clay=1&lod=0' 1280 800` mit `NODE_PATH=/tmp/w3/node_modules`. Die Kameraeinstellungen stammen aus den passenden `cams.json`-Kameradaten.

| Ansicht | Vorher | Nachher |
|---|---|---|
| D1 Klippe | [D1_klippe_vor.png](bilder_r3_vor/D1_klippe_vor.png) | [D1_klippe_nach.png](bilder_r3_nach/D1_klippe_nach.png) |
| D1 Rampe | [D1_rampe_vor.png](bilder_r3_vor/D1_rampe_vor.png) | [D1_rampe_nach.png](bilder_r3_nach/D1_rampe_nach.png) |
| G1 Wandkante | [G1_wand_vor.png](bilder_r3_vor/G1_wand_vor.png) | [G1_wand_nach.png](bilder_r3_nach/G1_wand_nach.png) |
| C3/D3 Serpentine | [C3_D3_serp_vor.png](bilder_r3_vor/C3_D3_serp_vor.png) | [C3_D3_serp_nach.png](bilder_r3_nach/C3_D3_serp_nach.png) |
| D6 Rampe | [D6_rampe_vor.png](bilder_r3_vor/D6_rampe_vor.png) | [D6_rampe_nach.png](bilder_r3_nach/D6_rampe_nach.png) |

## Annahmen und offene Punkte

- Die Kachelprüfung ordnet D2 räumlich dem Ausschnitt x=126..168 m, z=43..86 m zu. Gemeinsame Grenzpunkte sind im Bytevergleich enthalten.
- Als R3-Artefakte gelten nur die durch Messlage erklärten Endabschnitte bzw. nahen, nicht lokalen Rampenkreuzungen. Der übrige R3-Bestand ist als echter Formfehler gewertet.
- Der Raycast-Nullwert schließt offene Innenlöcher aus, bewertet aber weder Rampenprofile noch die fachliche Richtigkeit der Wegeanschlüsse.
- Offen bleibt eine separate Ursachenbehebung für die 12 echten Längs-, 16 echten Quer- und 15 echten Wölbungsabweichungen. Dafür ist ein weiterer Rampenprofil-/Endanschlussversuch nötig, der D1-Wand- und Klippenform sowie alle Zählergrenzen erneut einhält. Die 24 R1- und 15 R2-Fälle können unter dem unveränderten Overlay nicht topologisch beseitigt werden.
