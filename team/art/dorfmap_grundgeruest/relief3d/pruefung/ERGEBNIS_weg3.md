# Ergebnis weg3

Stand: 03.11.2026
Worktree: `/workspace/wt_dorfmap_weg3`
Branch: `art/dorfmap-weg3`, Basis `d3843dc` (`art/dorfmap-grundgeruest` zum angegebenen Ausgangsstand)

## Ergebnis

Das Wegziel ist **nicht erreicht**. Der sichere Standard lässt Wegmischung, Dellenanhebung und Flankenfortsetzung ausgeschaltet. Damit sind die erzeugten Reliefdaten bytegleich zum Basisstand; kein Gate-Zähler verschiebt sich. R8 bleibt 48, R8a_wegende bleibt 24 und R3_laengs bleibt 35.

Der beste getestete Wegmix senkte R8 auf 35, aber G6_facette stieg von 220 auf 230 (+10) und verletzt damit die erlaubte Zunahme von höchstens +5. R8a_wegende sank dabei nur von 24 auf 23. Dieser Mix ist deshalb **nicht Standard**. Es wurden drei Wegmix-Parameterkombinationen geprüft; alle drei verletzten die G6-Grenze.

## Änderungen und Schalter

In `gen_relief.py` liegen die einzeln übernommenen Funktionen `_weg_mischung`, `_weg_dellen_anheben` und `_weg2_r1_flanke` aus `fc8d651`, ergänzt um Messungen für D1-Klippe, D1/G1-Wandmasken und D2. Die Mischung läuft nach der C2-Stufe, damit nachfolgende globale Geländefilter D2 nicht erneut verändern. D2 wird nicht nachträglich aus einer Referenz wiederhergestellt.

Alle drei Schritte sind über Umgebungsvariablen schaltbar und im Standard aus:

| Schritt | Schalter | Standard | geprüfter Effekt |
|---|---|---:|---|
| Wegmischung/Knotenpads/Endauslauf | `WEGMISCH` | `0` | Bester Mix: R8 35, aber G6 +10; verworfen |
| Dellenanhebung | `WEG2_DELLEN` | `0` | Zusammen mit Flanke und ohne Mix: neue Treffer, kein R8-Gewinn |
| Rampenflanke am Ende 8 | `WEG2_R1_FLANKE` | `0` | Zusammen mit Dellenanhebung und ohne Mix: drei neue R8-Treffer |

Die deaktivierte Standardausgabe wurde frisch mit `python3 gen_relief.py && python3 baue_html.py` gebaut. `zellen_relief.csv` wurde danach auf den Basisstand zurückgesetzt; SHA-256 vorher/nachher: `fefce66d460cb153d159a244005f9b71de33b9ea0939d81aa6e2c801d57d8626`.

## Regeln: Basis und finaler Standard

Die Zahlen im finalen Standard entsprechen exakt `d3843dc`. `Δ` ist final minus Basis.

| Regel | Basis | Final | Δ |
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
| G5_beule_klippe | 68 | 68 | 0 |
| G6_facette | 220 | 220 | 0 |
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
| **pruefe_regeln Summe** | **570** | **570** | **0** |

| Gate-Regel | Basis | Final | Δ |
|---|---:|---:|---:|
| R8_stufe | 9 | 9 | 0 |
| R8_gitter | 10 | 10 | 0 |
| R8_quer | 5 | 5 | 0 |
| R8a_wegende | 24 | 24 | 0 |
| **R8 Summe** | **48** | **48** | **0** |
| R8b_delle | 25 | 25 | 0 |
| R9_saegezahn | 34 | 34 | 0 |
| R9w_wellen | 275 | 275 | 0 |
| **R9 Summe** | **334** | **334** | **0** |

## D1, G1 und D2: finale Treffer je Kachel

| Prüfung / Kachel | Basis | Final | Aufteilung im finalen Standard |
|---|---:|---:|---|
| pruefe_regeln / D1 | 36 | 36 | R1 2, R2 1, R3 längs 6, R3 quer 11, R3 Wölbung 10, G5 1, G6 5 |
| pruefe_regeln / G1 | 13 | 13 | R1 1, R3 längs 1, R6 3, G3 fein 1, G6 4, T1 3 |
| pruefe_regeln / D2 | 8 | 8 | R2 1, T1 7; kein neuer Treffer |
| R8 / D1 | 8 | 8 | Stufe 2, Gitter 2, quer 1, Wegende 3 |
| R8 / G1 | 1 | 1 | Wegende 1 |
| R8 / D2 | 0 | 0 | – |
| R9 / D1 | 26 | 26 | Delle 2, Sägezahn 1, Wellen 23 |
| R9 / G1 | 8 | 8 | Delle 1, Sägezahn 1, Wellen 6 |
| R9 / D2 | 0 | 0 | – |

Im finalen Standard gibt es **keine neuen Treffer und keine Ortsverschiebungen** gegenüber der Basis. Die drei finalen Checker-JSONs sind bytegleich zu den gespeicherten Basis-JSONs.

## Verworfen: Wegmix mit `WEGMISCH=1`

Die drei getesteten Nachlaufvarianten nutzten Wandfade/Kern `6/4,5 m`, `6/2,5 m` und `8/4,5 m`; der letzte Satz entspricht den gespeicherten Bildern `versuch_wegmischung/`. Alle ließen D2 unverändert, aber G6 stieg jeweils um mehr als 5:

| Wandfade / Kern | pruefe_regeln | G6 | R8 (Stufe/Gitter/quer/Wegende) | R9 |
|---|---:|---:|---:|---:|
| 6 / 4,5 m | 578 | 229 (+9) | 35 (4/4/4/23) | 334 |
| 6 / 2,5 m | 593 | 239 (+19) | 36 (4/4/4/24) | 334 |
| 8 / 4,5 m | 580 | 230 (+10) | 35 (4/4/4/23) | 334 |

Beim letzten Versuch waren gegenüber der Basis 74 `pruefe_regeln`-Treffer neu und 64 entfallen; D2 erhielt keinen neuen Treffer. R8 fügte zwei Treffer hinzu und entfernte 15; R9 blieb unverändert. R8a sank nur um einen Treffer. Die neuen Treffer außerhalb D2 sind hier mit Prüferwerten aufgeführt:

| Regel | Neue Treffer: Kachel (x, z) = Wert |
|---|---|
| G2_spitze_oben_fein | C4 (94.0, 171.2)=0.59; C4 (93.8, 171.8)=0.47 |
| G3_spitze_unten_fein | C4 (94.2, 171.0)=0.49; C4 (94.0, 171.5)=0.68 |
| G5_beule_klippe | C5 (114.0,182.0)=0.61; C5 (113.5,182.5)=0.61; C5 (123.0,185.1)=0.91; C5 (124.0,188.2)=0.86; C5 (121.0,188.9)=0.92; C5 (112.0,199.0)=0.61; C5 (112.3,199.8)=1.75; D4 (127.3,147.7)=1.41; G4 (273.5,131.0)=0.67; G4 (274.9,133.3)=4.44; G4 (281.0,139.0)=2.92 |
| G6_facette | B1 (61.7,37.2)=31; C1 (123.0,31.9)=19; C3 (122.4,115.6)=9; C3 (120.4,117.7)=8; C3 (118.0,125.8)=6; C4 (96.4,132.5)=7; C4 (95.1,140.1)=9; C4 (94.5,144.4)=11; C4 (93.4,156.4)=47; C4 (124.2,158.7)=6; C4 (94.9,160.2)=9; C4 (96.3,164.7)=12; C4 (86.8,165.8)=36; C4 (93.5,169.2)=8; C4 (92.6,170.5)=14; C5 (96.2,172.6)=12; C5 (123.9,178.6)=19; C5 (84.8,179.1)=10; C5 (115.4,181.7)=14; C5 (86.8,186.3)=6; C5 (110.2,186.6)=8; C6 (111.0,226.8)=6; D1 (145.0,2.5)=7; D1 (150.4,6.2)=6; D1 (141.8,10.0)=6; D1 (140.6,13.9)=7; D1 (159.2,21.2)=9; D3 (133.3,116.9)=10; D4 (133.5,131.8)=10; D6 (134.8,235.5)=6; E1 (178.0,25.8)=6; G1 (277.3,21.4)=17; G3 (272.8,116.0)=8; G3 (274.8,118.7)=9; G3 (281.0,125.8)=16; G3 (275.2,128.0)=12; G4 (286.4,131.9)=7; H5 (315.0,187.5)=11; H5 (313.7,195.3)=8; H5 (312.5,203.2)=6; H5 (316.4,210.8)=21; H6 (314.2,216.1)=6; H6 (294.7,226.9)=6 |
| G7b_wandkontur_feld | D1 (147,21)=0.813 |
| R3_laengs_m | D1 (154.3,28.2)=0.098 |
| R3_quer_pct | C5 (87.6,180.1)=4.2; C5 (109.2,190.5)=12.2; C5 (112.8,192.3)=15.2 |
| R3_woelb_m | C5 (109.2,190.5)=0.199; C5 (112.8,192.3)=0.247 |
| R5_loch | C4 (96.5,158.5)=1.6; C4 (85.0,171.0)=1.36; C5 (86.0,174.5)=1.27; C5 (86.5,175.0)=1.24; C5 (91.5,175.5)=1.36; C5 (90.0,176.0)=1.29 |
| T1_fleckrand | C7 (114.5,258.5)=9; G6 (258.1,251.5)=11; H4 (296.0,138.9)=9 |
| R8_quer | D1 (156.5,37.5)=16.4, `rampe_11_ende` |
| R8a_wegende | C7 (100.0,269.1)=0.22, `rampe_5_ende` |

Bei Wegmix wurden in der gezielten Änderungsmessung an D1-Klippe 344 Grobpunkte (max. 0,982881 m) und 1.314 Feinpunkte (max. 1,000065 m) verändert. In der D1-Wandmaske waren es 982 Grobpunkte (max. 2,179296 m) und 3.820 Feinpunkte (max. 2,049816 m); in der G1-Wandmaske 423 Grob- (max. 1,077631 m) und 1.723 Feinpunkte (max. 1,069213 m). **D2: null** geänderte Grobpunkte, Feinpunkte oder neue Feinvertices. Die Kernpriorität setzt die Wandmaske innerhalb des Straßenkerns teilweise wieder frei; damit erfüllt dieser Versuch die gewünschte Wandmaskenbegrenzung nicht vollständig.

Die Bilder des Mixversuchs zeigen die D1-Klippe weiterhin als steile Kante, aber mehr Unruhe an der D1-Wandfläche/-kante. G1 ist dort nahezu unverändert. Diese Sichtprüfung und der G6-Anstieg bestätigen, den Mix nicht als Standard zu setzen.

## Weitere verworfene Kombination: Dellenanhebung und Flanke ohne Mix

Mit `WEG2_DELLEN=1 WEG2_R1_FLANKE=8e WEGMISCH=0` stieg `pruefe_regeln` von 570 auf 576; R8 stieg von 48 auf 51, R9 blieb 334. Die neuen Treffer lagen außerhalb D2:

| Regel | Neue Treffer: Kachel (x, z) = Wert |
|---|---|
| G2_spitze_oben_fein | C4 (88.5,171.5)=1.69; C4 (91.0,171.5)=0.87 |
| G3_spitze_unten_fein | C4 (88.8,171.2)=1.00; C4 (88.2,171.8)=1.09; C5 (90.5,172.2)=1.37 |
| G5_beule_klippe | C5 (123.0,185.1)=0.92; C5 (124.0,188.2)=0.88 |
| G6_facette | C4 (96.3,164.5)=14; C5 (91.6,172.6)=7 |
| R3_quer_pct | C4 (89.8,167.4)=3.7; C4 (89.5,171.4)=3.8 |
| R5_loch | C4 (96.5,158.5)=1.6 |
| R8_gitter | C4 (89.5,171.4)=2.71 |
| R8_quer | C4 (89.5,171.4)=9.5 |
| R8_stufe | C4 (89.5,171.4)=2.72 |

Die Messfunktion für Dellenanhebung und Flanke meldete an D1-Klippe, D1/G1-Wandmasken und D2 jeweils 0 Änderungen. Dellenanhebung änderte außerhalb dieser Masken 400 Grobpunkte, maximal 1,178 m; die Flanke änderte 29 Grob- und 147 Feinpunkte, maximal 2,7135 m. Wegen der zusätzlichen Treffer und des schlechteren R8 sind beide Schritte im Standard deaktiviert.

## D2, Zellwerte und Regressionsschutz

Der finale `G`-Quellblock und `WEGA` sind bytegleich zur Basis. Für D2 ist der `GB`-Ausschnitt mit Form `(87, 85)` bytegleich; SHA-256 beider Seiten: `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`. Im Feinmesh sind alle 17 D2-Vertex-IDs und Höhen bytegleich. Der Mixversuch hatte dieselben D2-Werte; es gab keine D2-Treffer neu.

`index.html` und `relief_daten.json.gz` sind im finalen Standard ebenfalls bytegleich zur Basis (`b723acdf…` bzw. `5e8fdb51…`). Die Zell-CSV blieb unverändert. Overlay, `../referenz/*`, Prüfer und Schwellenwerte wurden nicht geändert.

## Pflichtprüfungen und Bilder

| Prüfung | Ergebnis finaler Standard |
|---|---|
| `python3 gen_relief.py && python3 baue_html.py` | Erfolgreich; Ausgabe deterministisch bytegleich zur Basis |
| Raycast `loch_o18g.js` | `offen_innen=0`, `punkte=0` |
| `pruefe_regeln.py` | 570 (Basis 570), maximale Regeländerung 0 |
| `r8_kreuzung.py` | 48 (Basis 48) |
| `r9_form.py` | 334 (Basis 334) |
| `pruefe_t42u.py` | Summe 0 |
| lod1 `test_budget.js` | 1.174.554 gerenderte Dreiecke, unter 1,3 Mio. |
| D2 GB/FW | Bytegleich; keine neuen D2-Treffer |

Die drei Nahbilder wurden mit `render_t119u.js`, Ton (`?clay=1&lod=0`), 1280×800 und derselben Kamera gerendert und selbst angesehen. Vorher und finaler Standard sind pixelidentisch:

| Motiv | Vorher | Finaler Standard | verworfener Mix |
|---|---|---|---|
| D1-Klippe bei 140\|35 | [Bild](o18/weg3/vorher/D1_klippe_140_35.png) | [Bild](o18/weg3/nachher/D1_klippe_140_35.png) | [Bild](o18/weg3/versuch_wegmischung/D1_klippe_140_35.png) |
| D1-Wand bei 152\|29 | [Bild](o18/weg3/vorher/D1_wand_152_29.png) | [Bild](o18/weg3/nachher/D1_wand_152_29.png) | [Bild](o18/weg3/versuch_wegmischung/D1_wand_152_29.png) |
| G1-Wand bei 273\|21 | [Bild](o18/weg3/vorher/G1_wand_273_21.png) | [Bild](o18/weg3/nachher/G1_wand_273_21.png) | [Bild](o18/weg3/versuch_wegmischung/G1_wand_273_21.png) |

Der Standard bewahrt Klippe und Wandkanten unverändert, weil keine Höhenänderung aktiv ist. Der optionale Mix wurde wegen der dokumentierten Regelzunahme und zusätzlicher D1-Wandunruhe verworfen.

Die Kommandos der Gate-Skripte wurden direkt mit separaten `/tmp/*_weg3`-Ausgaben ausgeführt. `export_gate.sh` wurde nicht aufgerufen: es ignoriert den übergebenen `LOCHSCAN`-Pfad, verwendet fest `/tmp/gate_loch.json` und schreibt seine Ergebnisdateien in den Worktree. Prüfer und Schwellen blieben unverändert.

## Annahmen und offene Punkte

- Die offiziellen Zell-/Wegprüfer bleiben die maßgebliche Messung; die Höhenänderungsmessungen sind zusätzliche Ursachenmessungen.
- Die Wandmaske stammt aus `_wand_maske()`. Beim optionalen Mix überstimmt der Straßenkern sie teilweise; eine sichere Wandbegrenzung ist offen.
- Offen bleiben das Ziel R8 ≤ 38 und eine deutliche Senkung von R8a_wegende. Der finale Standard erreicht diese Ziele nicht.
- Es wurden höchstens drei Wegmix-Parameterkombinationen getestet. Keine davon erfüllt gleichzeitig die R8-Ziele und die G6-Grenze.
