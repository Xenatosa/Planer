# ERGEBNIS_fleck — Welle 5 (04.11.2026)

Branch: `art/dorfmap-fleck`

Basis: `origin/art/dorfmap-grundgeruest` bei `e7a5874`
Änderung: Textur-Mischung zur Verringerung von `T1_fleckrand`.

## Änderung und Ursache

Die Treffergruppen lagen überwiegend in der Schneemischung aus `GRAS` und `MOOS2`: Bei 81 von 94 Ausgangstreffern lagen die Messfenster innerhalb eines einzelnen `skin_slot`; 13 berührten mehrere Slots. `boden_anzeige_m` fließt nicht in die VC-Farbmischung ein. Die verursachende Stufe ist damit die binäre/spitze Mischung dieser beiden Schnee-Beimengungen, nicht der Zellquellwert oder die Höhenberechnung.

`gen_relief.py` filtert nun die GRAS- und MOOS2-Gewichte normiert mit einer Gaußmaske (Variante `FLECKVAR=1`, σ=0,75 m; Standard). Das gilt nur für Schnee-Landpunkte außerhalb eines 3-m-Schutzstreifens um D2. `FLECKVAR=0` schaltet den Eingriff ab. Die Ausgangsgewichte und Zellwerte bleiben unverändert; es ändern sich daraus erzeugte Vertexfarben. Als D2-Regression wird nach den bestehenden Textur-Nähschritten der ursprüngliche D2-VC-Ausschnitt aus `pruefung/d2_vc_basis_fleck.bin` zurückgesetzt.

## Regelwerte vor/nach

Alle Prüfer und Schwellen blieben unverändert. Bei `pruefe_regeln` sind die offenen Bildprüfungsmarker T2–T5 jeweils weiterhin als ein Treffer enthalten.

| Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| `G11_baum_an_wand` | 0 | 0 | +0 |
| `G11_objekt_schwebt_sinkt` | 0 | 0 | +0 |
| `G1_loch_offen` | 0 | 0 | +0 |
| `G1_lochscan_fehlt` | 0 | 0 | +0 |
| `G2_spitze_oben` | 3 | 3 | +0 |
| `G2_spitze_oben_fein` | 8 | 8 | +0 |
| `G3_spitze_unten` | 3 | 3 | +0 |
| `G3_spitze_unten_fein` | 2 | 2 | +0 |
| `G4_delle_beule` | 0 | 0 | +0 |
| `G5_beule_klippe` | 68 | 68 | +0 |
| `G6_facette` | 220 | 220 | +0 |
| `G7_wand_glatt_gesamt` | 0 | 0 | +0 |
| `G7_wand_glatte_flaeche` | 1 | 1 | +0 |
| `G7b_wandkontur_feld` | 24 | 24 | +0 |
| `G7b_wandkontur_kantenschaerfe` | 1 | 1 | +0 |
| `G7b_wandkontur_rauheit` | 1 | 1 | +0 |
| `G8_fluss_flach` | 0 | 0 | +0 |
| `G8_fluss_nicht_bis_rand` | 1 | 1 | +0 |
| `R1_blind` | 24 | 24 | +0 |
| `R1_wand` | 0 | 0 | +0 |
| `R1_wasser` | 0 | 0 | +0 |
| `R2_getrennt` | 15 | 15 | +0 |
| `R3_laengs_m` | 35 | 35 | +0 |
| `R3_quer_pct` | 23 | 23 | +0 |
| `R3_woelb_m` | 22 | 22 | +0 |
| `R4_rand` | 0 | 0 | +0 |
| `R4_schlucht` | 0 | 0 | +0 |
| `R5_loch` | 17 | 17 | +0 |
| `R5_spitze` | 0 | 0 | +0 |
| `R6_objekt_auf_weg` | 0 | 0 | +0 |
| `R6_wasser_schnee` | 4 | 4 | +0 |
| `R7_trennung` | 0 | 0 | +0 |
| `R8_gitter` | 10 | 10 | +0 |
| `R8_quer` | 5 | 5 | +0 |
| `R8_stufe` | 9 | 9 | +0 |
| `R8a_wegende` | 24 | 24 | +0 |
| `R8b_delle` | 25 | 25 | +0 |
| `R9_saegezahn` | 34 | 34 | +0 |
| `R9w_wellen` | 275 | 275 | +0 |
| `T1_fleckrand` | 94 | 25 | -69 |
| `T1_harte_farbkante` | 0 | 0 | +0 |
| `T1_harte_farbkante_gerade` | 0 | 0 | +0 |
| `T2_textur_abgeschnitten_bildpruefung_offen` | 1 | 1 | +0 |
| `T3_streifen_ringe_bildpruefung_offen` | 1 | 1 | +0 |
| `T4_graue_flussstreifen_bildpruefung_offen` | 1 | 1 | +0 |
| `T5_textur_vs_clay_bildpruefung_offen` | 1 | 1 | +0 |
| `T6_wasser_in_schnee_farbe` | 0 | 0 | +0 |
| `T_VC_format` | 0 | 0 | +0 |
| **pruefe_regeln Summe** | **570** | **501** | **-69** |
| **R8 Summe** | **48** | **48** | **+0** |
| **R9 Summe** | **334** | **334** | **+0** |
| **Alle drei Prüfer zusammen** | **952** | **883** | **-69** |

R8-Aufteilung: `R8_stufe` 9→9, `R8_gitter` 10→10, `R8_quer` 5→5, `R8a_wegende` 24→24. R9-Aufteilung: `R8b_delle` 25→25, `R9_saegezahn` 34→34, `R9w_wellen` 275→275.

## Kachelwerte (alle 56)

Je Kachel stehen die Trefferzahlen für `pruefe_regeln`, R8, R9 und darunter `T1_fleckrand`; Bildlinks führen zu den nicht-Clay-Vorher/Nachher-Texturvergleichen. Fokuskoordinaten sind x|z in Metern. `—` bedeutet: kein T1-Trefferzahlwechsel und daher kein Bildpaar erforderlich.

| Kachel | pruefe_regeln | R8 | R9 | T1_fleckrand | Fokus x\|z | Bild |
|---|---:|---:|---:|---:|---:|---|
| A1 | 11→11 | 0→0 | 2→2 | 0→0 | — | — |
| A2 | 9→9 | 0→0 | 7→7 | 0→0 | — | — |
| A3 | 1→1 | 0→0 | 0→0 | 1→1 | — | — |
| A4 | 0→0 | 0→0 | 0→0 | 0→0 | — | — |
| A5 | 0→0 | 0→0 | 0→0 | 0→0 | — | — |
| A6 | 0→0 | 0→0 | 5→5 | 0→0 | — | — |
| A7 | 3→3 | 0→0 | 3→3 | 0→0 | — | — |
| B1 | 4→4 | 1→1 | 3→3 | 0→0 | — | — |
| B2 | 1→1 | 0→0 | 7→7 | 0→0 | — | — |
| B3 | 13→10 | 0→0 | 7→7 | 5→2 | 72.6|95.4 | [Vergleich 01](nahbilder_fleck/vergleich_01.png) |
| B4 | 22→21 | 0→0 | 12→12 | 3→2 | 53.7|166.3 | [Vergleich 01](nahbilder_fleck/vergleich_01.png) |
| B5 | 15→14 | 0→0 | 11→11 | 1→0 | 62.1|185.6 | [Vergleich 01](nahbilder_fleck/vergleich_01.png) |
| B6 | 4→2 | 0→0 | 3→3 | 2→0 | 50.2|231.7 | [Vergleich 02](nahbilder_fleck/vergleich_02.png) |
| B7 | 1→1 | 0→0 | 1→1 | 0→0 | — | — |
| C1 | 7→7 | 0→0 | 5→5 | 0→0 | — | — |
| C2 | 7→5 | 1→1 | 4→4 | 2→0 | 89.7|82.8 | [Vergleich 02](nahbilder_fleck/vergleich_02.png) |
| C3 | 45→45 | 4→4 | 19→19 | 0→0 | — | — |
| C4 | 32→31 | 2→2 | 15→15 | 1→0 | 119.2|137.9 | [Vergleich 02](nahbilder_fleck/vergleich_02.png) |
| C5 | 48→47 | 5→5 | 12→12 | 1→0 | 92.6|186.8 | [Vergleich 03](nahbilder_fleck/vergleich_03.png) |
| C6 | 11→8 | 3→3 | 19→19 | 3→0 | 119.9|252.5 | [Vergleich 03](nahbilder_fleck/vergleich_03.png) |
| C7 | 4→2 | 0→0 | 3→3 | 2→0 | 115.2|258.7 | [Vergleich 03](nahbilder_fleck/vergleich_03.png) |
| D1 | 36→36 | 8→8 | 26→26 | 0→0 | — | — |
| D2 | 8→8 | 0→0 | 0→0 | 7→7 | — | — |
| D3 | 11→8 | 0→0 | 2→2 | 3→0 | 153.8|93.0 | [Vergleich 04](nahbilder_fleck/vergleich_04.png) |
| D4 | 23→23 | 2→2 | 7→7 | 0→0 | — | — |
| D5 | 4→4 | 0→0 | 11→11 | 0→0 | — | — |
| D6 | 16→16 | 4→4 | 12→12 | 0→0 | — | — |
| D7 | 1→1 | 0→0 | 0→0 | 0→0 | — | — |
| E1 | 13→11 | 1→1 | 8→8 | 2→0 | 205.6|39.7 | [Vergleich 04](nahbilder_fleck/vergleich_04.png) |
| E2 | 14→12 | 0→0 | 0→0 | 6→4 | 179.3|81.9 | [Vergleich 04](nahbilder_fleck/vergleich_04.png) |
| E3 | 9→6 | 0→0 | 12→12 | 3→0 | 179.8|86.0 | [Vergleich 05](nahbilder_fleck/vergleich_05.png) |
| E4 | 9→6 | 0→0 | 8→8 | 4→1 | 189.3|133.2 | [Vergleich 05](nahbilder_fleck/vergleich_05.png) |
| E5 | 1→1 | 0→0 | 1→1 | 0→0 | — | — |
| E6 | 5→4 | 1→1 | 5→5 | 1→0 | 172.4|234.3 | [Vergleich 05](nahbilder_fleck/vergleich_05.png) |
| E7 | 8→8 | 0→0 | 0→0 | 0→0 | — | — |
| F1 | 16→14 | 1→1 | 7→7 | 2→0 | 246.2|42.4 | [Vergleich 06](nahbilder_fleck/vergleich_06.png) |
| F2 | 6→2 | 0→0 | 3→3 | 4→0 | 251.5|52.9 | [Vergleich 06](nahbilder_fleck/vergleich_06.png) |
| F3 | 0→0 | 0→0 | 0→0 | 0→0 | — | — |
| F4 | 3→1 | 0→0 | 0→0 | 2→0 | 249.4|163.7 | [Vergleich 06](nahbilder_fleck/vergleich_06.png) |
| F5 | 14→6 | 0→0 | 0→0 | 9→1 | 249.7|179.9 | [Vergleich 07](nahbilder_fleck/vergleich_07.png) |
| F6 | 7→8 | 1→1 | 8→8 | 0→1 | 247.1|236.2 | [Vergleich 07](nahbilder_fleck/vergleich_07.png) |
| F7 | 4→4 | 0→0 | 0→0 | 0→0 | — | — |
| G1 | 13→11 | 1→1 | 8→8 | 3→1 | 260.4|41.6 | [Vergleich 07](nahbilder_fleck/vergleich_07.png) |
| G2 | 4→2 | 0→0 | 0→0 | 3→1 | 284.1|45.4 | [Vergleich 08](nahbilder_fleck/vergleich_08.png) |
| G3 | 14→10 | 3→3 | 11→11 | 4→0 | 274.5|87.3 | [Vergleich 08](nahbilder_fleck/vergleich_08.png) |
| G4 | 16→16 | 0→0 | 6→6 | 0→0 | — | — |
| G5 | 4→0 | 0→0 | 0→0 | 4→0 | 286.4|191.0 | [Vergleich 08](nahbilder_fleck/vergleich_08.png) |
| G6 | 11→10 | 0→0 | 8→8 | 1→0 | 258.2|251.6 | [Vergleich 09](nahbilder_fleck/vergleich_09.png) |
| G7 | 0→0 | 0→0 | 0→0 | 0→0 | — | — |
| H1 | 2→2 | 0→0 | 7→7 | 0→0 | — | — |
| H2 | 9→5 | 0→0 | 6→6 | 4→0 | 326.6|66.1 | [Vergleich 09](nahbilder_fleck/vergleich_09.png) |
| H3 | 4→3 | 0→0 | 9→9 | 1→0 | 312.2|96.0 | [Vergleich 09](nahbilder_fleck/vergleich_09.png) |
| H4 | 7→6 | 4→4 | 6→6 | 1→0 | 295.1|138.8 | [Vergleich 10](nahbilder_fleck/vergleich_10.png) |
| H5 | 19→16 | 5→5 | 12→12 | 4→1 | 296.7|178.5 | [Vergleich 10](nahbilder_fleck/vergleich_10.png) |
| H6 | 18→16 | 1→1 | 11→11 | 5→3 | 301.4|218.1 | [Vergleich 10](nahbilder_fleck/vergleich_10.png) |
| H7 | 1→1 | 0→0 | 2→2 | 0→0 | — | — |

### D1, G1 und D2

| Kachel | pruefe_regeln | R8 | R9 | T1_fleckrand |
|---|---:|---:|---:|---:|
| D1 | 36→36 | 8→8 | 26→26 | 0→0 |
| G1 | 13→11 | 1→1 | 8→8 | 3→1 |
| D2 | 8→8 | 0→0 | 0→0 | 7→7 |

## Nahbildbefunde

Vorher/Nachher sind jeweils mit Gelände-Textur gerendert; Clay war deaktiviert. Die zehn Vergleichsbilder enthalten die 30 Kacheln mit geänderter T1-Trefferzahl, drei Vorher/Nachher-Paare pro Bild. In den betrachteten Ausschnitten werden harte grünliche Fleckgrenzen weicher. An den Fokusorten war keine neue sichtbare Kante, Kerbe, Treppe/Zahn, Riss oder Absatz erkennbar. Das gilt auch für den einzelnen lokalen T1-Anstieg F6 (0→1 bei x|z=247,1|236,2); dort ist die Geländeform vor/nach gleich, die Änderung betrifft die Farb-/Mischmaske. Bestehende Fels-/Schneekanten bleiben in den Paaren bestehen.

## Regressionen und Prüfläufe

- `T1_fleckrand`: 94→25 (netto −69; Ziel ≤40 erreicht). Auf Kachelebene sinkt der Wert in 29 Kacheln und steigt in F6 um eins; D2 bleibt 7→7.
- Keine einzelne Regelklasse in `pruefe_regeln`, R8 oder R9 steigt. R8 bleibt 48, R9 bleibt 334. D2 bleibt in R8/R9 bei 0; seine Prüftrefferliste ist unverändert.
- Lochscan: 0 offene Innenlöcher. `t42u`: Summe 0.
- lod1-Raycaster: 1.174.554 gezeichnete Dreiecke (unter 1,3 Mio.); Ausgangsbasis im Scan: 1.700.454.
- JSON-Basisvergleich gegen `e7a5874`: `G`, `GB`, `WV` und `WEGA` sind bytegleich. Der D2-VC-Ausschnitt ist bytegleich (SHA-256 `b67dc7199dcd4fe28bb242295f928355a85fc84bee12e390e060c9e7cbbcf2bf`). In `FW` unterscheiden sich außerhalb D2 nur Farbbytes; die 17 gültigen D2-FW-Punkte (IDs, Höhe, Farbe und übrige FW-Daten) stimmen überein. `zellen_relief.csv` blieb gegenüber der Basis bytegleich.
- Der unveränderte Lochprüfer lief unter Xvfb mit headed Chromium/SwiftShader erfolgreich: `meshes=7`, `dreiecke=1700454`, `offen_innen=0`, `punkte=0`. Die angegebene reine Headless-Ausführung scheiterte in dieser Umgebung nach dem Start mit „WebGL ist in diesem Browser nicht verfügbar“ (Headless Chromium war mit `--use-gl=disabled` konfiguriert); für den erfolgreichen Lauf wurden Prüfer und Schwellen nicht geändert, nur Playwrights Browserstart über einen temporären Preload auf headed umgestellt.
- `pruefe_regeln.py` meldet wie vorgesehen Exit 1 wegen vorhandener Regelhits; die JSON-Ausgabe wurde für die Zahlen verwendet. R8/R9 liefen mit 48/334.

## Annahmen, Grenzen und offene Punkte

- Die Ursachengruppierung nach `skin_slot` ist eine räumliche Überlagerung der 94 T1-Messfenster. Sie zeigt die Häufigkeit innerhalb/eines Übergangs, ist keine unabhängige kausale Messung. `boden_anzeige_m` wird in der Farbgewichtung nicht verwendet; der direkte Eingriff ist deshalb auf GRAS/MOOS2-Mischgewichte begrenzt.
- Der Filter wirkt auf Vertexfarben; Vegetations-/Materialparameter, Zellquellwerte, Höhen und Overlay wurden nicht angepasst. Die D2-Farbregression wird explizit festgeschrieben, damit Folgeänderungen an der Textur-Nähstufe D2 nicht verändern.
- Die neue T1-Erkennung in F6 bleibt lokal bestehen, obwohl der Gesamttrefferwert deutlich sinkt. Der Bildvergleich zeigt an dieser Stelle keine neue sichtbare Strukturkante; eine automatische Regelabnahme ersetzt das nicht.
- Nicht verändert wurden die bestehenden T2–T5 Bildprüfungsmarker; sie bleiben je einmal offen.

## Bilddateien

`pruefung/nahbilder_fleck/vergleich_01.png` bis `vergleich_10.png` enthalten alle erforderlichen Paaransichten; die Links stehen zeilenweise in der Kacheltabelle.
