# Ergebnis Delle

Stand: 03.11.2026 · Branch `art/dorfmap-delle` · Vergleichsbasis `9d3f8fc`

## Ergebnis

`R8b_delle` ist kartenweit von 25 auf 0 Treffer gesunken. Die drei Prüfer melden jetzt `pruefe_regeln` 579, R8 53 und R9 305 Treffer. Kein einzelner Regelzähler steigt um mehr als 5; die größten Anstiege sind `R3_quer_pct` und `G11_objekt_schwebt_sinkt` mit je +5.

Das Export-Gate bleibt wegen der übrigen Treffer rot. Außerdem stehen das geforderte Zurücksetzen von `zellen_relief.csv` und `t42u=0` im Konflikt: Mit den beim Build erzeugten Zellspalten ist `t42u=0`; nach dem verlangten Zurücksetzen auf den unveränderten Stand von `9d3f8fc` meldet `pruefe_t42u.py` 3.879 Abweichungen. Die CSV blieb zurückgesetzt und unverändert.

## Änderung

`gen_relief.py` ergänzt am finalen abgeleiteten Höhenfeld eine deterministische Füllung für trockene, abflusslose Mulden. Sie nutzt dieselbe morphologische Senkenfüllung wie `r9_form.py`, hebt zusammenhängende Bereiche mit mehr als 0,30 m Fülltiefe an, wenn sie höchstens 6 m von einem Dorfweg oder Rampenpfad entfernt sind, und lässt Wasser sowie Wandbereiche aus. Die Zellquellen und das Wege-Overlay werden nur gelesen, nicht geändert.

Die Standardvariante ist `DELLENWEG=1`; `DELLENWEG=0` schaltet sie aus. Es wurden zwei Varianten verwendet. Im Build wurden 25 Muldenkomponenten mit 4.494 Gitterpunkten angehoben, maximal um 4,11 m. Die sichtbare Korrektur wird mit σ=0,6 Gitterpunkten in `GB` und Feinmesh übertragen. 55 Dekoobjekte erhielten denselben vertikalen Hub wie der sichtbare Boden unter ihnen; so bleiben ihre bisherigen Bodenabstände erhalten. Der maximale Objekt-Hub war 3,749 m.

Quellwerte, Overlay, `../referenz/*` und Kachel D2 wurden nicht verändert. `zellen_relief.csv` wurde nach dem Build auf den Branch-Stand zurückgesetzt.

## G1-Stufenmessung

Der tatsächliche G1-Treffer von `r9_form.py` lag bei `(278.5, 27.0)` und hatte vor der Änderung 0,423 m Fülltiefe. Die beiden im Auftrag genannten Näherungspunkte `(273.4, 21.2)` und `(262, 25)` messen in den Stufen-Snapshots jeweils 0,000 m; sie sind nicht der vom Prüfer gemeldete Tiefenpeak.

| Stufe am tatsächlichen Treffer `(278.5, 27.0)` | Fülltiefe |
|---|---:|
| Zellquellwert `h0` | 0,000 m |
| `H` nach Quellskalierung und Ebenenzuweisung | 0,000 m |
| `H` nach Wandzuweisung | 0,000 m |
| `H` nach Südgratfuß | 0,000 m |
| `H` nach Flusslückenschluss | 0,000 m |
| `H` nach Wasserglättung | 0,000 m |
| `H` nach Kratermodell | 0,000 m |
| `H` nach Flusskorrektur `fluss_k` | 0,000 m |
| `H` nach Rampen | 0,000 m |
| `H` nach Serpentinen | 0,000 m |
| `H` nach Ufer und Flussbett | 0,000 m |
| `G` nach Wandmodell | 0,781 m |
| `G` nach thermischer Erosion | 0,423 m |
| `G` nach hydraulischer Erosion | 0,423 m |
| `G` nach Rampenprojektion | 0,423 m |
| `G` nach Dellenkorrektur | 0,000 m |

Die Ursache liegt damit in der abgeleiteten Wandmodell-Stufe; thermische Erosion verringert die Fülltiefen danach auf den vom Prüfer gemeldeten Wert. In den unveränderten Zellquellwerten ist an dieser Stelle keine Mulde enthalten.

## Gruppierung der 25 ursprünglichen Treffer

| Erste Stufe mit Fülltiefe >0,30 m | Treffer | Felder |
|---|---:|---|
| Wandmodell (`G_wandmodell`) | 18 | G1: 1, F1: 1, E3: 12, E4: 4 |
| Rampen in `H` | 4 | D1: 2, D6: 2 |
| Wandzuweisung in `H` | 2 | C4: 1, C5: 1 |
| Rampenprojektion in `G` | 1 | C3: 1 |
| **Gesamt** | **25** | |

## Regelzähler je Regel

Vorherwerte stammen aus den drei unveränderten Prüfern mit Datenstand `9d3f8fc`; fehlende Regeln hatten 0 Treffer.

| Prüfer | Regel | Vorher | Nachher | Änderung |
|---|---|---:|---:|---:|
| `pruefe_regeln` | R1_blind | 24 | 24 | 0 |
| `pruefe_regeln` | R1_wand | 0 | 1 | +1 |
| `pruefe_regeln` | R2_getrennt | 15 | 15 | 0 |
| `pruefe_regeln` | R3_laengs_m | 35 | 37 | +2 |
| `pruefe_regeln` | R3_quer_pct | 23 | 28 | +5 |
| `pruefe_regeln` | R3_woelb_m | 22 | 26 | +4 |
| `pruefe_regeln` | R5_loch | 17 | 21 | +4 |
| `pruefe_regeln` | R6_wasser_schnee | 4 | 4 | 0 |
| `pruefe_regeln` | G2_spitze_oben | 3 | 3 | 0 |
| `pruefe_regeln` | G3_spitze_unten | 3 | 3 | 0 |
| `pruefe_regeln` | G2_spitze_oben_fein | 8 | 4 | −4 |
| `pruefe_regeln` | G3_spitze_unten_fein | 2 | 1 | −1 |
| `pruefe_regeln` | G5_beule_klippe | 66 | 68 | +2 |
| `pruefe_regeln` | G6_facette | 249 | 213 | −36 |
| `pruefe_regeln` | G7_wand_glatte_flaeche | 1 | 1 | 0 |
| `pruefe_regeln` | G7b_wandkontur_rauheit | 1 | 1 | 0 |
| `pruefe_regeln` | G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| `pruefe_regeln` | G7b_wandkontur_feld | 23 | 22 | −1 |
| `pruefe_regeln` | G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| `pruefe_regeln` | G11_objekt_schwebt_sinkt | 0 | 5 | +5 |
| `pruefe_regeln` | G11_baum_an_wand | 0 | 3 | +3 |
| `pruefe_regeln` | T1_fleckrand | 94 | 93 | −1 |
| `pruefe_regeln` | T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| `pruefe_regeln` | T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| `pruefe_regeln` | T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| `pruefe_regeln` | T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |
| **`pruefe_regeln` gesamt** | | **596** | **579** | **−17** |
| `r8_kreuzung` | R8_stufe | 9 | 11 | +2 |
| `r8_kreuzung` | R8_gitter | 10 | 12 | +2 |
| `r8_kreuzung` | R8_quer | 5 | 5 | 0 |
| `r8_kreuzung` | R8a_wegende | 24 | 25 | +1 |
| **R8 gesamt** | | **48** | **53** | **+5** |
| `r9_form` | R8b_delle | 25 | 0 | −25 |
| `r9_form` | R9_saegezahn | 34 | 34 | 0 |
| `r9_form` | R9w_wellen | 275 | 271 | −4 |
| **R9 gesamt** | | **334** | **305** | **−29** |

## Zähler je Kachel

`pruefe_regeln` zählt alle Treffer. R8/R9 sind die Summe ihrer jeweiligen Einzelregeln.

| Kachel | `pruefe_regeln` vorher → nachher | R8 vorher → nachher | R9 vorher → nachher |
|---|---:|---:|---:|
| D1 | 36 → 36 | 8 → 8 | 26 → 24 |
| G1 | 13 → 13 | 1 → 1 | 8 → 7 |
| D2 | 8 → 8 | 0 → 0 | 0 → 0 |

Die acht bestehenden `pruefe_regeln`-Treffer in D2 sind dieselben Einträge wie vorher; es kam dort keiner hinzu. R8 und R9 bleiben in D2 bei 0.

## D2-Nachweis

Bytevergleiche zwischen `9d3f8fc` und dem generierten Relief zeigen für D2 identische Höhenwerte:

| Feld | D2-Ausschnitt | SHA-256 | Vergleich |
|---|---:|---|---|
| `G` | 7.395 Werte | `325f6fe2f41178f7e9c4b2198881438bc5ac70649ac4a0ee9836b463e6e1408c` | bytegleich |
| Anzeigehöhen `GB` | 7.395 Werte | `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6` | bytegleich |
| `WV` | 7.395 Werte | `4b33ed17db72aa7b29472ef5b50f05196ea61eb7a11a7db3b7a8684eb8d3880a` | bytegleich |
| Feinmesh-Höhen | 17 Werte | `5f6e029e43d8964603baa9a5b1ff13fcc42d4a7f7551c069c1d4d56f17457dcb` | bytegleich |
| Feinmesh-Vertex-IDs | 17 Werte | `be2b34cc8db032aba9dade4a3a4f5f4ae042133d6af5878390c18142a05403a0` | bytegleich |

Alle 1.806 D2-Zellzeilen sind in allen Spalten wertgleich; der kanonische SHA-256 der extrahierten Zeilen ist `6965c81f72adb6c6e60f10affa26a0087525a5e21d29042a29beafccdc55b96f`. Die zurückgesetzte Gesamtdatei `zellen_relief.csv` ist bytegleich mit `9d3f8fc` (SHA-256 `fefce66d460cb153d159a244005f9b71de33b9ea0939d81aa6e2c801d57d8626`).

## Pflichtprüfungen

| Prüfung | Ergebnis |
|---|---|
| `python3 gen_relief.py && python3 baue_html.py` | erfolgreich |
| Raycast `loch_o18g.js`, RAND 0.6 | 2.140.988 Dreiecke, `offen_innen=0`, keine Punkte |
| `pruefe_regeln.py` mit aktuellem Raycast | 579 Treffer, Exit 1 wegen übriger Regeln |
| `r8_kreuzung.py` | 53 Treffer, Exit 1 |
| `r9_form.py` | 305 Treffer, `R8b_delle=0`, Exit 1 wegen R9/R9w |
| `sh pruefung/export_gate.sh` | ROT wegen der verbleibenden Treffer |
| LOD1, mit und ohne Schatten | 1.290.999 gerenderte Dreiecke, unter 1,3 Mio. um 9.001 |
| `pruefe_t42u.py` mit Zellspalten aus dem aktuellen Relief-Build | Summe 0 |
| `pruefe_t42u.py` nach dem geforderten CSV-Reset | Summe 3.879; 1.286 `hoehe_m`, 1.121 je `ecke_nw_m`/`ecke_so_m`, 164 je Wand-/Skin-Klasse und 23 `begehbar_auf_wand` |
| `zellen_relief.csv` nach dem Build | auf `9d3f8fc` zurückgesetzt |

## Annahmen, Grenzen und offene Punkte

- Die Wegnähe folgt dem R9-Prüfer: Dorfwegzellen plus 0,25-m-Abtastung der Rampenpfade, maximal 6 m Abstand. Korrekturmaske: trockenes Land, Fülltiefe >0,30 m, Wandbereiche ausgeschlossen.
- Die Trefferursache liegt nicht in den Zellquellwerten, sondern im abgeleiteten Wandmodell und in Rampen-/Wandübergängen. Die Reparatur läuft als deterministischer letzter abgeleiteter G-Schritt, weil die 25 Treffer aus vier unterschiedlichen Stufen stammen.
- Die ungeklärte Vorgabenkollision betrifft den t42u-Abgleich: Zurücksetzen der CSV auf den Branch-Stand lässt den Abgleich mit dem aktualisierten `G` fehlschlagen; die generierte Zellspalten-Datei besteht ihn. Beides zugleich ist mit dem aktuellen `pruefe_t42u.py` nicht erreichbar, ohne die CSV stehen zu lassen oder den Prüfer zu ändern. Beides wurde nicht getan.
- Das vollständige Export-Gate ist weiterhin rot. Ziel `R8b_delle=0` ist erreicht; übrige Regeln und die t42u-Abweichungen nach CSV-Reset bleiben offen.
