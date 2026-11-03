# Ergebnis Wellen2

Stand: 03.11.2026 · Worktree `/workspace/wt_dorfmap_wellen2` · Branch `art/dorfmap-wellen2`
Vergleichsbasis: `d3843dc` (`art/dorfmap-grundgeruest`-Basis-Gate: 570 / 48 / 334; Loch 0; T42 0).

## Ergebnis und Diagnose

Die 0,25–1,5-m-Wellen entstehen in den abgeleiteten Höhenfeldern, nicht in den Zellquellwerten. In `../_alt/modell3d_t36u/zellen_eigenschaften.csv`, Feld `hoehe_m`, wurden die 4-nachbarschaftlichen Paare innerhalb jeder Kachel gezählt. D1 und G1 enthalten je 3.527 Paare und D2 ebenfalls 3.527; in keiner Kachel gibt es ein Paar mit einer Höhendifferenz von 0,25 bis 1,5 m. Die Quellwerte reichen in D1/G1 von 0 bis 8,6 m, in D2 von −0,44 bis 0 m.

Der unveränderte R9w-Messlauf über die Stufen von `gen_relief.py` zeigt, wann die Wellen auftreten:

| G-Stufe | R9w gesamt | D1 | G1 | D2 |
|---|---:|---:|---:|---:|
| `g_wandmodell` | 243 | 14 | 7 | 0 |
| `g_thermal` | 224 | 14 | 5 | 0 |
| `g_erosion` (nach hydraulischer Erosion) | 235 | 11 | 5 | 0 |
| `g_rampen` | 275 | 23 | 6 | 0 |
| endgültiges `G` | 253 | 23 | 6 | 0 |

Das Wandmodell erzeugt bereits R9w-Komponenten. Die Erosionsstufen verändern deren Zahl; die Rampenüberblendung erhöht sie anschließend von 235 auf 275. Die nachgelagerte, auf 5 cm begrenzte Korrektur senkt den Endwert auf 253. D1 und G1 bleiben bei R9w unverändert; der Rückgang entsteht in anderen Kacheln.

## Änderung

`gen_relief.py` glättet nach der Rampenüberblendung ausschließlich das abgeleitete `G`: Gauß-Sigma 0,75 m, maximal 0,05 m Versatz. Die Standardvariante ist `GWELLEN=0.05`; `GWELLEN=0` schaltet sie aus. 52.434 G-Ecken ändern sich, der maximale Versatz beträgt 0,05 m, der RMS-Versatz über das Feld 0,0089 m. Aktiv ist der Filter nur auf Land mit 0,15–0,8 Hangneigung, mindestens 1,5 m von steilen Wänden und mindestens 1 m von Straßen/Rampen entfernt. Eine zusätzliche Wanddreiecksmaske schützt Wandkanten; der D2-Ausschnitt samt 5-m-Umfeld bleibt unangetastet. Overlay und Zellquellwerte werden nur gelesen.

Nach der letzten Feinbandänderung werden 77 Objekt-Höhen außerhalb D2 an die vom Regelprüfer abgefragte finale `FW`-Höhe angeglichen. Dafür wird dieselbe bilineare Interpolation wie in `pruefe_regeln.py` verwendet; Objektpositionen in der Ebene und Zellwerte werden nicht geändert. Dies hält die Höhenprüfung an der tatsächlich sichtbaren Fläche ausgerichtet.

Eine stärkere 0,25-m-Variante wurde in einer früheren Messrunde verworfen: sie überschritt G6/G11 deutlich. Sie ist im endgültigen Code nicht mehr schaltbar. Übrig sind nur „aus“ und der bestandene 5-cm-Standard.

## Regeln: vorher und nachher

Die Tabelle zeigt alle Klassen aus dem Basis-Gate `d3843dc` und dem Abschlusslauf mit dem Raycast-Scan `/tmp/gate_loch_wellen2.json`. Keine Klasse steigt um mehr als 3; die erlaubte Obergrenze +5 wird eingehalten.

| Prüfer | Regel | Basis | Wellen2 | Δ |
|---|---|---:|---:|---:|
| pruefe_regeln | G2_spitze_oben | 3 | 3 | +0 |
| pruefe_regeln | G2_spitze_oben_fein | 8 | 7 | -1 |
| pruefe_regeln | G3_spitze_unten | 3 | 3 | +0 |
| pruefe_regeln | G3_spitze_unten_fein | 2 | 2 | +0 |
| pruefe_regeln | G5_beule_klippe | 68 | 71 | +3 |
| pruefe_regeln | G6_facette | 220 | 218 | -2 |
| pruefe_regeln | G7_wand_glatte_flaeche | 1 | 1 | +0 |
| pruefe_regeln | G7b_wandkontur_feld | 24 | 23 | -1 |
| pruefe_regeln | G7b_wandkontur_kantenschaerfe | 1 | 1 | +0 |
| pruefe_regeln | G7b_wandkontur_rauheit | 1 | 1 | +0 |
| pruefe_regeln | G8_fluss_nicht_bis_rand | 1 | 1 | +0 |
| pruefe_regeln | R1_blind | 24 | 24 | +0 |
| pruefe_regeln | R2_getrennt | 15 | 15 | +0 |
| pruefe_regeln | R3_laengs_m | 35 | 36 | +1 |
| pruefe_regeln | R3_quer_pct | 23 | 23 | +0 |
| pruefe_regeln | R3_woelb_m | 22 | 22 | +0 |
| pruefe_regeln | R5_loch | 17 | 16 | -1 |
| pruefe_regeln | R6_wasser_schnee | 4 | 4 | +0 |
| pruefe_regeln | T1_fleckrand | 94 | 93 | -1 |
| pruefe_regeln | T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | +0 |
| pruefe_regeln | T3_streifen_ringe_bildpruefung_offen | 1 | 1 | +0 |
| pruefe_regeln | T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | +0 |
| pruefe_regeln | T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | +0 |
| r8_kreuzung | R8_gitter | 10 | 10 | +0 |
| r8_kreuzung | R8_quer | 5 | 5 | +0 |
| r8_kreuzung | R8_stufe | 9 | 9 | +0 |
| r8_kreuzung | R8a_wegende | 24 | 24 | +0 |
| r9_form | R8b_delle | 25 | 24 | -1 |
| r9_form | R9_saegezahn | 34 | 34 | +0 |
| r9_form | R9w_wellen | 275 | 253 | -22 |

## Kacheln D1, G1 und D2

Je Eintrag stehen Trefferzahlen `Basis→Wellen2`; die Detailspalte nennt die Werte je Regel.

| Prüfer | Kachel | Summe | Regelwerte |
|---|---|---:|---|
| pruefe_regeln | D1 | 36→33 | G5_beule_klippe 1→1; G6_facette 5→2; R1_blind 2→2; R2_getrennt 1→1; R3_laengs_m 6→6; R3_quer_pct 11→11; R3_woelb_m 10→10 |
| pruefe_regeln | G1 | 13→16 | G3_spitze_unten_fein 1→1; G6_facette 4→7; R1_blind 1→1; R3_laengs_m 1→1; R6_wasser_schnee 3→3; T1_fleckrand 3→3 |
| pruefe_regeln | D2 | 8→8 | R2_getrennt 1→1; T1_fleckrand 7→7 |
| r8_kreuzung | D1 | 8→8 | R8_gitter 2→2; R8_quer 1→1; R8_stufe 2→2; R8a_wegende 3→3 |
| r8_kreuzung | G1 | 1→1 | R8a_wegende 1→1 |
| r8_kreuzung | D2 | 0→0 | – |
| r9_form | D1 | 26→26 | R8b_delle 2→2; R9_saegezahn 1→1; R9w_wellen 23→23 |
| r9_form | G1 | 8→8 | R8b_delle 1→1; R9_saegezahn 1→1; R9w_wellen 6→6 |
| r9_form | D2 | 0→0 | – |

D2 hat in keinem Prüfer neue Treffer. Die vorhandenen 8 `pruefe_regeln`-Treffer (R2: 1, T1: 7) sind unverändert; R8 und R9 bleiben bei 0. D1/G1 haben bei R8 und R9 keine geänderten Trefferzahlen. In `pruefe_regeln` sinkt G6 in D1 von 5 auf 2, steigt in G1 von 4 auf 7 und sinkt insgesamt von 220 auf 218.

## Zusätzliche beziehungsweise weiter verlagerte Trefferorte

Für die Ortszuordnung wurden Treffer zuerst nach exakt gleicher Position und danach per nächstem Treffer derselben Regel und Kachel im Radius 2 m gepaart. Die folgende Liste enthält aktuelle Treffer ohne solches Basispaar. Das umfasst neue Komponenten und Komponenten, deren Schwerpunkt weiter als 2 m gewandert ist; die offiziellen Prüfer selbst wurden nicht geändert. Werte stammen unverändert aus den Prüferausgaben. Es gibt keine solchen D2-Treffer.

### `pruefe_regeln.py`

| Regel | Kachel | Anzahl ohne Basispaar | Ort `x|z` (m) = Wert |
|---|---|---:|---|
| G2_spitze_oben_fein | H2 | 2 | 303.8|85.2 = 0.5; 305.8|85.8 = 0.46 |
| G5_beule_klippe | C3 | 2 | 97.5|98.5 = 0.64; 99.0|102.5 = 0.64 |
| G5_beule_klippe | C4 | 1 | 118.0|167.0 = 1.18 |
| G5_beule_klippe | D4 | 1 | 126.8|143.1 = 0.77 |
| G5_beule_klippe | F2 | 1 | 224.0|43.0 = 0.75 |
| G5_beule_klippe | G4 | 1 | 282.0|140.0 = 1.57 |
| G6_facette | B2 | 1 | 49.1|47.2 = 14 |
| G6_facette | B3 | 1 | 80.7|120.5 = 154 |
| G6_facette | B4 | 10 | 54.0|135.2 = 8; 58.6|140.8 = 6; 71.4|141.9 = 9; 79.1|149.9 = 14; 78.4|154.3 = 12; 82.0|160.5 = 64; 75.2|160.1 = 7; 74.3|162.4 = 7; 76.3|164.9 = 11; 82.0|170.2 = 8 |
| G6_facette | B6 | 1 | 70.7|215.3 = 10 |
| G6_facette | C1 | 1 | 122.3|42.2 = 10 |
| G6_facette | C3 | 3 | 118.6|94.1 = 24; 122.9|110.3 = 6; 90.2|112.5 = 10 |
| G6_facette | C4 | 6 | 120.6|132.8 = 8; 95.4|137.3 = 14; 117.1|136.6 = 17; 120.4|146.7 = 7; 125.3|150.1 = 9; 119.6|151.4 = 8 |
| G6_facette | C5 | 9 | 122.1|183.4 = 7; 110.2|186.8 = 10; 123.1|202.0 = 9; 86.4|206.9 = 15; 101.5|209.1 = 25; 94.9|209.1 = 8; 93.5|210.2 = 6; 84.0|210.8 = 6; 92.5|211.2 = 7 |
| G6_facette | C6 | 3 | 117.5|220.9 = 6; 123.7|221.9 = 8; 103.4|223.7 = 8 |
| G6_facette | D1 | 1 | 141.2|22.4 = 7 |
| G6_facette | D3 | 2 | 133.0|95.0 = 11; 132.0|99.2 = 6 |
| G6_facette | D4 | 1 | 129.7|135.9 = 9 |
| G6_facette | D5 | 1 | 143.0|173.5 = 7 |
| G6_facette | D6 | 2 | 127.6|222.4 = 10; 167.1|224.7 = 6 |
| G6_facette | E1 | 2 | 204.8|30.6 = 6; 203.0|40.6 = 12 |
| G6_facette | E6 | 2 | 203.1|230.7 = 16; 201.4|235.0 = 41 |
| G6_facette | F1 | 3 | 232.1|26.9 = 6; 228.4|27.8 = 15; 212.2|31.4 = 7 |
| G6_facette | F6 | 2 | 243.2|225.1 = 15; 218.8|255.9 = 7 |
| G6_facette | G1 | 3 | 284.0|22.1 = 8; 283.2|23.9 = 16; 274.2|29.9 = 6 |
| G6_facette | G4 | 3 | 289.4|153.2 = 21; 286.1|162.4 = 15; 291.7|165.8 = 9 |
| G6_facette | G6 | 3 | 269.5|227.6 = 6; 273.2|229.2 = 9; 268.2|238.2 = 6 |
| G6_facette | H1 | 5 | 299.0|31.4 = 11; 304.3|32.4 = 7; 310.5|32.3 = 8; 311.8|33.1 = 6; 317.6|41.1 = 7 |
| G6_facette | H2 | 3 | 321.6|68.6 = 7; 329.4|76.4 = 9; 300.9|84.4 = 9 |
| G6_facette | H3 | 1 | 312.3|92.6 = 7 |
| G6_facette | H5 | 4 | 307.8|174.8 = 6; 302.4|182.7 = 37; 306.8|195.8 = 6; 304.9|199.8 = 6 |
| G6_facette | H6 | 3 | 323.6|237.4 = 31; 326.2|240.3 = 6; 308.7|241.4 = 8 |
| R3_laengs_m | C5 | 1 | 120.5|178.2 = 0.08 |
| T1_fleckrand | B1 | 1 | 53.9|40.4 = 8 |

### `r9_form.py`

| Regel | Kachel | Anzahl ohne Basispaar | Ort `x|z` (m) = Wert |
|---|---|---:|---|
| R9w_wellen | B2 | 3 | 75.8|48.2 = 0.49; 81.8|48.4 = 0.55; 59.8|50.0 = 0.12 |
| R9w_wellen | B3 | 2 | 80.0|98.4 = 0.13; 71.9|113.7 = 0.38 |
| R9w_wellen | B4 | 3 | 57.5|132.0 = 0.42; 51.4|140.4 = 0.11; 54.5|146.8 = 0.11 |
| R9w_wellen | B5 | 1 | 79.4|193.6 = 0.59 |
| R9w_wellen | B6 | 1 | 79.2|222.2 = 0.18 |
| R9w_wellen | C4 | 1 | 110.0|143.9 = 0.67 |
| R9w_wellen | C5 | 4 | 119.2|179.2 = 0.97; 94.1|190.0 = 0.35; 87.1|190.9 = 0.36; 96.3|198.2 = 0.62 |
| R9w_wellen | C6 | 1 | 113.4|216.8 = 0.69 |
| R9w_wellen | D1 | 3 | 149.3|3.2 = 0.16; 146.7|11.6 = 0.4; 151.5|6.3 = 0.2 |
| R9w_wellen | D4 | 1 | 156.6|170.5 = 0.25 |
| R9w_wellen | D6 | 2 | 128.2|241.0 = 0.37; 128.9|248.9 = 0.29 |
| R9w_wellen | E1 | 1 | 178.1|32.9 = 0.19 |
| R9w_wellen | E5 | 1 | 169.2|184.5 = 0.29 |
| R9w_wellen | F6 | 1 | 210.1|246.1 = 0.16 |
| R9w_wellen | G6 | 1 | 277.5|245.2 = 0.29 |
| R9w_wellen | H1 | 1 | 301.9|39.7 = 0.63 |
| R9w_wellen | H2 | 2 | 327.5|74.5 = 0.4; 316.7|85.7 = 0.58 |
| R9w_wellen | H4 | 3 | 296.9|158.2 = 0.25; 299.8|163.8 = 0.48; 303.5|168.4 = 0.41 |
| R9w_wellen | H5 | 1 | 303.4|183.5 = 0.62 |
| R9w_wellen | H6 | 1 | 324.8|255.5 = 0.41 |

`r8_kreuzung.py` hat keine zusätzlichen Trefferorte. Die Positionslisten sind bewusst vollständig für die oben beschriebene 2-m-Zuordnung; sie erklären, warum unveränderte Gesamtsummen einzelne Ortsverschiebungen verdecken können.

## D2-Bytevergleich

| Ausschnitt | Bytegleich zu `d3843dc` | SHA-256 |
|---|---|---|
| `G` D2, Form 87×85 | ja | `325f6fe2f41178f7e9c4b2198881438bc5ac70649ac4a0ee9836b463e6e1408c` |
| `GB` Anzeige D2, Form 87×85 | ja | `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6` |
| D2-Zeilen in `zellen_relief.csv` (1.806 Zeilen) | ja | `6965c81f72adb6c6e60f10affa26a0087525a5e21d29042a29beafccdc55b96f` |
| komplette zurückgesetzte `zellen_relief.csv` | ja | `fefce66d460cb153d159a244005f9b71de33b9ea0939d81aa6e2c801d57d8626` |
| D2-`FW`-IDs und Höhen (17 Feinbandpunkte) | ja | IDs und Höhen bytegleich; Höhen-SHA `5f6e029e43d8964603baa9a5b1ff13fcc42d4a7f7551c069c1d4d56f17457dcb` |

Der HTML-Container als Ganzes ändert sich wegen der Änderungen außerhalb D2. Der darin enthaltene D2-Anzeigeausschnitt `GB` ist bytegleich. Die Zell-CSV wurde nach dem Build wie vorgegeben auf den Basisstand zurückgesetzt; T42 wurde davor auf der frisch erzeugten CSV geprüft.

## Pflicht-Gates

| Gate | Ergebnis |
|---|---|
| `python3 gen_relief.py && python3 baue_html.py` | erfolgreich; deterministischer Abschlussbuild |
| Raycast `loch_o18g.js`, `RAND=0.6` | 7 Meshes; 1.698.596 Dreiecke in dieser LOD0-Szene; `offen_innen=0`, `punkte=0` |
| `pruefe_regeln.py` mit eigenem Raycast-Scan | 568 Treffer; Basis 570; keine Klasse über +5 |
| `r8_kreuzung.py` | 48 Treffer; Basis 48 |
| `r9_form.py` | 311 Treffer; Basis 334; davon R9w 253 statt 275 |
| `pruefe_t42u.py` auf der frisch generierten CSV | Summe 0; GLB: 33.476 Wand- und 780.988 Bodendreiecke |
| `test_dreiecke_l1.js` | 1.172.821 gerenderte LOD1-Dreiecke, mit und ohne Schatten; unter 1,3 Mio. |
| `LOCHSCAN=/tmp/gate_loch_wellen2.json sh pruefung/export_gate.sh` | Exit 1 / `GATE ROT`, weil das Skript bei vorhandenen Regel-Treffern rot liefert. Der direkte Regelprüfer wurde zusätzlich explizit mit dem getaggten Scan ausgeführt; `export_gate.sh` setzt intern fest `/tmp/gate_loch.json`. |

## Tonbilder und Sichtprüfung

Gerendert mit `NODE_PATH=/tmp/w3/node_modules`, `?clay=1&lod=0`, 1280×800. Auf den Vorher/Nachher-Nahbildern bleibt die D1-Klippe bei 140|35 sichtbar und durchgehend; die steile G1-Wandkante bleibt erhalten. Ich sehe keine neu erzeugten Zähne oder eine weggeg­lättete Klippe. Die Bilder zeigen auch die kleinen Oberflächenänderungen in der Umgebung.

| Kachel / Blick | Vorher | Nachher |
|---|---|---|
| D1, Klippe 140|35 | [PNG](bilder_wellen2/vor/D1_klippe_140_35.png) | [PNG](bilder_wellen2/nach/D1_klippe_140_35.png) |
| G1, Wandkante 272.5|26.5 | [PNG](bilder_wellen2/vor/G1_wandkante_272_30.png) | [PNG](bilder_wellen2/nach/G1_wandkante_272_30.png) |

## Annahmen, Grenzen und offene Punkte

- Der Quelltest zählt orthogonale Nachbarpaare innerhalb der jeweiligen Kachel und verwendet das Eingangsfeld `hoehe_m`; diagonale Paare und Unterschiede außerhalb 0,25–1,5 m sind nicht Teil dieser Aussage.
- Die 2-m-Paarung dient nur dazu, Ortsverschiebungen im Ergebnisbericht nachvollziehbar zu machen; sie ändert keine Schwelle oder Regel.
- R9w verbessert sich um 22 Treffer, bleibt mit 253 aber deutlich über 0. D1/G1 selbst sinken bei R9w nicht; dort bleiben 23 beziehungsweise 6 Treffer. Das Ziel ist daher teilweise, nicht vollständig erreicht.
- G6 sinkt global um 2, obwohl sich viele G6-Schwerpunkte verlagern; die zusätzlichen Orte sind in der Liste aufgeführt. G1 steigt dabei um 3, unter der zulässigen +5-Grenze.
- `export_gate.sh` bleibt rot, da es auf null Treffer besteht. Das ist kein grünes Gate; die unabhängigen Klassen- und Schwellenbedingungen sind erfüllt.
- `zellen_relief.csv` ist nach dem Abschlussbuild zurückgesetzt. Zellquellwerte, Overlay, Prüfer und Schwellen wurden nicht verändert. Kosten: 0 EUR.
