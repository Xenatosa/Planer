# Ergebnis g5r5b — 04.11.2026

**Teilziel erreicht; das Export-Gate bleibt rot.** Der Generator bereinigt Treffer lokal an der angezeigten Oberfläche. D2, Quellwerte und Overlay-Code bleiben unverändert. Das Ergebnis erfüllt die Schranke von höchstens `+5` Treffern je Regel; G6 liegt genau an dieser Grenze.

## Änderung

In [gen_relief.py](../gen_relief.py) ergänzt `_g5_r5_r6_lokal()` den Lauf nach der vorhandenen C2-Terrasse:

- `G5R5_LOCAL=1` ist Standard. `G5R5_TARGET=0.55` ist die Standardvariante; `0.59` ist als weniger starke Alternative schaltbar. `G5R5_LOCAL=0` schaltet die Korrektur ab.
- G5-Höhen werden nur auf den vom bestehenden `g5_beulen(..., 0.6)`-Detektor markierten Punkten gekappt. R5-Senken werden lokal bis knapp unter 1 m Resttiefe aufgefüllt.
- R6 wird erfasst, aber nicht verändert. Ein Absenken der Geländeoberfläche unter den Wasserflächen erzeugte sichtbare Stufen an der G1-Wasserkante.
- Die Korrektur ändert `G_ANZ` und die zugehörigen Feinrelief-Höhen. Sie pinnt D2 nicht nachträglich auf eine Referenzdatei.

Die vorherige Regression `dcd1881` hatte `pr=902`, `r8=77` und 2.134 Raycast-Löcher. Die dortige globale Anzeige-Korrektur veränderte auch Gelände außerhalb der Treffer; außerdem wurde D2 nachträglich angeheftet. Der jetzige Lauf arbeitet auf den erkannten G5- und R5-Bereichen. Der Vergleich bezieht sich auf `d3843dc`; die relevanten Relief- und Generator-Dateien dieses Basispunkts stimmen mit `de0d9b5` überein.

## Gate und Kennzahlen

| Prüfung | Basis `d3843dc` | Ergebnis | Änderung |
|---|---:|---:|---:|
| `pruefe_regeln` gesamt, einschließlich G7b | 570 | 537 | −33 |
| `r8_kreuzung` | 48 | 48 | 0 |
| `r9_form` | 334 | 334 | 0 |
| Raycast offene Innenpunkte | 0 | 0 | 0 |
| `pruefe_t42u` Summe | 0 | 0 | 0 |
| lod1 Dreiecke, beide Schattenmodi | — | 1.174.652 | < 1,3 Mio. |

Der Pflichtbau lief mit `python3 gen_relief.py && python3 baue_html.py`. Der Raycast meldet 7 Meshes, 1.700.454 Dreiecke, `offen_innen=0` und `punkte=0`. `export_gate.sh` meldet **GATE ROT**, weil die Prüfer noch 537 vorhandene Treffer melden und das Skript für einen Export null Treffer verlangt. Die Regeldateien und Schwellen wurden nicht geändert. Kein Regelwert steigt um mehr als 5; der höchste Anstieg ist G6 mit `+5`.

| Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| R1_blind | 24 | 24 | 0 |
| R2_getrennt | 15 | 15 | 0 |
| R3_laengs_m | 35 | 35 | 0 |
| R3_quer_pct | 23 | 23 | 0 |
| R3_woelb_m | 22 | 22 | 0 |
| R5_loch | 17 | 0 | −17 |
| R6_wasser_schnee | 4 | 4 | 0 |
| G2_spitze_oben | 3 | 3 | 0 |
| G3_spitze_unten | 3 | 3 | 0 |
| G2_spitze_oben_fein | 8 | 8 | 0 |
| G3_spitze_unten_fein | 2 | 2 | 0 |
| G5_beule_klippe | 68 | 47 | −21 |
| G6_facette | 220 | 225 | **+5** |
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

| R8-Regel | Vorher | Nachher |
|---|---:|---:|
| R8_stufe | 9 | 9 |
| R8_gitter | 10 | 10 |
| R8_quer | 5 | 5 |
| R8a_wegende | 24 | 24 |
| **Summe R8** | **48** | **48** |

| R9-Regel | Vorher | Nachher |
|---|---:|---:|
| R8b_delle | 25 | 25 |
| R9_saegezahn | 34 | 34 |
| R9w_wellen | 275 | 275 |
| **Summe R9** | **334** | **334** |

## Kacheln D1, G1 und D2

Die Regel-Summen enthalten alle `pruefe_regeln`-Treffer der Kachel. R8/R9 sind getrennt ausgewiesen.

| Kachel | pr vorher → nachher | G5 | R5 | R6 | R8 vorher → nachher | R9 vorher → nachher |
|---|---:|---:|---:|---:|---:|---:|
| D1 | 36 → 35 | 1 → 0 | 0 → 0 | 0 → 0 | 8 → 8 | 26 → 26 |
| G1 | 13 → 13 | 0 → 0 | 0 → 0 | 3 → 3 | 1 → 1 | 8 → 8 |
| D2 | 8 → 8 | 0 → 0 | 0 → 0 | 0 → 0 | 0 → 0 | 0 → 0 |

D2 hat keine neuen `pruefe_regeln`-, R8- oder R9-Treffer. Die dekodierten Quellwerte `G` sind gesamthaft bytegleich. D2 ist in `G`, Anzeige `GB` und Feinrelief-Höhen/Vertex-IDs (`FW`) ebenfalls bytegleich; im D2-Feinrelief wurden 117 Stützpunkte verglichen. `WV`, `VC` und `WEGA` sind gesamthaft unverändert. Die HTML-Datei unterscheidet sich von der Basis nur im eingebetteten Relief-Datenblock; der übrige HTML-/Overlay-Inhalt ist bytegleich. `zellen_relief.csv` ist unverändert (SHA-256 `fefce66d460cb153d159a244005f9b71de33b9ea0939d81aa6e2c801d57d8626`).

## Neue Trefferorte und Wertverschiebungen

Der Vergleich nach Regel, Kachel, Weg, Ort und Teilprüfung findet **50 neue räumliche Trefferorte**: 43 G5 und 7 G6. Zugleich verschwinden 64 G5-Orte und 2 G6-Orte; daraus ergeben sich die Nettoänderungen `G5 −21` und `G6 +5`. Alle 17 R5-Treffer verschwinden. Bei anderen Regeln entstehen keine neuen räumlichen Trefferorte. Die folgenden Werte sind die vom Prüfer ausgegebenen Werte an den neuen Orten (`x|z`, Meterkoordinaten):

| Regel | Kachel | Neue Orte `x|z: Wert` |
|---|---|---|
| G5 | A2 | 17.7\|50.2: 0.76 |
| G5 | A7 | 25.2\|261.8: 0.92; 25.5\|263.5: 0.83 |
| G5 | C3 | 125.5\|97.0: 1.07; 97.0\|99.0: 0.64; 95.0\|100.5: 0.68; 109.5\|106.5: 0.72; 113.0\|106.5: 1.15; 114.3\|107.3: 1.43; 108.0\|108.6: 1.13; 115.8\|109.2: 0.76; 116.5\|110.0: 0.60; 116.5\|113.3: 1.04; 105.0\|112.5: 0.86; 104.0\|113.8: 0.74 |
| G5 | C4 | 117.6\|167.6: 0.95 |
| G5 | C5 | 124.0\|186.5: 0.66; 119.5\|189.0: 0.62; 121.5\|189.5: 0.90; 122.5\|189.5: 0.79; 113.0\|199.5: 0.66; 114.0\|200.0: 5.30; 116.0\|201.0: 1.00 |
| G5 | D4 | 135.5\|139.0: 0.75 |
| G5 | D6 | 155.0\|230.5: 0.61 |
| G5 | D7 | 167.5\|261.5: 0.94 |
| G5 | E7 | 168.0\|259.0: 0.63; 169.7\|259.8: 0.81; 169.0\|260.5: 0.65; 174.3\|262.1: 1.04 |
| G5 | F1 | 222.5\|41.2: 1.04; 223.0\|42.0: 0.91; 224.5\|42.5: 0.71 |
| G5 | G3 | 276.2\|114.2: 0.98 |
| G5 | G4 | 272.9\|131.1: 5.32; 274.0\|131.5: 4.33; 275.0\|132.0: 5.07; 277.0\|134.5: 0.63; 276.0\|135.0: 0.60; 278.0\|136.5: 0.63; 277.5\|137.0: 1.01; 280.5\|139.5: 1.42 |
| G5 | H7 | 332.2\|277.0: 0.89 |
| G6 | A2 | 20.9\|44.5: 14 |
| G6 | A7 | 25.4\|262.4: 9 |
| G6 | C3 | 114.7\|112.2: 14 |
| G6 | C4 | 86.5\|170.4: 23 |
| G6 | C5 | 90.0\|209.2: 8 |
| G6 | D7 | 167.3\|259.6: 13 |
| G6 | H7 | 331.8\|278.1: 6 |

An denselben Orten änderten sich zusätzlich Werte, ohne dass dort ein Treffer neu hinzukam: D1 `R3_laengs_m` bei `150.3|28.7` von 0.247 auf 0.242, `153.7|26.1` von 1.378 auf 1.335 und `151.8|29.6` von 0.135 auf 0.132; D1 `R3_woelb_m` bei `150.3|28.7` von 1.793 auf 1.783 und `153.7|26.1` von 1.774 auf 1.775. Drei C3- und ein E7-G5-Wert sowie ein C5-G6-Wert verschoben sich am selben Ort; die G7b-Werte änderten sich geringfügig: Rauheit 0.735→0.734 (Min.), Kantenschärfe 0.651→0.649 (Min.), Wandfelder B5 0.447→0.446, C4 0.825→0.821, C5 0.828→0.820 und D4 0.843→0.844. Die Regelanzahlen bleiben davon unberührt.

## Bildprüfung

Die Vorher-/Nachher-Bilder wurden mit `render_t119u.js`, `?clay=1&lod=0`, 1280×800 gerendert und persönlich verglichen.

| Ansicht | Vorher | Nachher | Sichtprüfung |
|---|---|---|---|
| D1 Klippe/Wand bei 140\|35 | [PNG](bilder_g5r5b/vor/D1_140_35.png) | [PNG](bilder_g5r5b/nachher/D1_140_35.png) | Gleich; Klippe und Wandfuß bleiben erhalten. |
| D1 Beule bei 152\|28 | [PNG](bilder_g5r5b/vor/D1_beule_152_28.png) | [PNG](bilder_g5r5b/nachher/D1_beule_152_28.png) | Gleich im Kamerabild. |
| G1 Wandkante bei 273\|21 | [PNG](bilder_g5r5b/vor/G1_nord_273_21.png) | [PNG](bilder_g5r5b/nachher/G1_nord_273_21.png) | Gleich; keine neuen Zähne oder geglättete Klippe sichtbar. |
| G1 R6-Wasserrand bei 273\|7 | [PNG](bilder_g5r5b/vor/G1_R6_273_7.png) | [PNG](bilder_g5r5b/nachher/G1_R6_273_7.png) | Gleich. |
| D2 Kontrolle | [PNG](bilder_g5r5b/vor/D2_kontrolle.png) | [PNG](bilder_g5r5b/nachher/D2_kontrolle.png) | Im Bild gleich; zusätzlich byteweise geprüft. |
| G4 G5-Kante bei 280\|139 | [PNG](bilder_g5r5b/vor/G4_spitze_280_139.png) | [PNG](bilder_g5r5b/nachher/G4_spitze_280_139.png) | Kleine neue Kerbe an der Kante sichtbar; die Prüfer melden dort neue G5-Orte. |
| D6 R5-Senke bei 151\|229 | [PNG](bilder_g5r5b/vor/D6_senke_151_229.png) | [PNG](bilder_g5r5b/nachher/D6_senke_151_229.png) | Treffer beseitigt; sichtbar bleibt ein kurzer scharfer Absatz um die aufgefüllte Senke. |

## Grenzen und offene Punkte

- **Vorgabenabweichung:** Im Arbeitsverlauf wurden vier R5-Füllvarianten geprüft (direkt bei 0,95 m und 1,001 m Resttiefe sowie weich auslaufend mit 0,5 m und 1 m). Damit wurde die Grenze von höchstens drei Varianten überschritten. Der finale Generator enthält nur die direkte Standardfüllung; diese Abweichung bleibt dennoch bestehen.
- Das Ziel ist teilweise erreicht: G5 sinkt von 68 auf 47, R5 von 17 auf 0. R6 bleibt bei 4, weil ein Eingriff dort die G1-Wasserkante sichtbar beschädigt hat.
- Die direkte R5-Füllung beseitigt die Treffer, zeigt aber in D6 den oben beschriebenen Absatz. Die G4-Kerbe und die 8 neuen G5-Orte dort bleiben ebenfalls sichtbar beziehungsweise messbar. Diese Bereiche sollten bei einer nächsten Iteration gezielt betrachtet werden.
- G6 steigt um 5 und verbraucht damit das gesamte erlaubte Plus. Eine stärkere Korrektur ist nicht abgesichert.
- Das Gate ist rot, obwohl Raycast, t42u, D2-Gleichheit, lod1 und die maximal erlaubte Regeldifferenz bestehen.
- Wiederholter Standardbau lieferte identische Artefakte: `index.html` SHA-256 `b08fbf4af9584dac04448d49f81834c619bbca84570ea18f729fb88a2bc0d3b3`, `relief_daten.json.gz` SHA-256 `9b28763b0f2d609b0cf0d1c8f65fca160914235a13714b9274533a3289da9810`.
