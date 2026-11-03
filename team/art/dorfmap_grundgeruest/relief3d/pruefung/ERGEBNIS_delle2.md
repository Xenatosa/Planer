# Ergebnis Delle2

> Aktueller Stand: siehe den ergänzenden Abschnitt „Nachauftrag delle2b“ am Ende. Die folgenden ursprünglichen Zahlen dokumentieren Commit `a0a618b`, der nicht gemergt wird.

Stand: 03.11.2026 · Branch `art/dorfmap-delle2` · Basis `art/dorfmap-grundgeruest` (`d3843dc`) · Referenzwerte aus dem unveränderten Lauf: `570 / 48 / 334`

## Ergebnis

`R8b_delle` ist von 25 auf 0 Treffer gesunken. Die Gesamtbilanz fällt von 952 auf 929. Das Ziel `R8 <= 48` wurde knapp verfehlt: R8 steht bei 51 (+3). Kein einzelner Regelzähler steigt um mehr als 5; der größte Anstieg beträgt +4. D2 blieb in allen drei Prüfern unverändert, und es kam dort kein neuer `pruefe_regeln`-Treffer hinzu.

`t42u` meldet 0 Abweichungen. Der Raycast meldet 0 offene Innenkanten und 0 Punkte. LOD1 rendert 407.365 Dreiecke und liegt unter 1,3 Mio. `export_gate.sh` ist wegen der verbleibenden Regelverstöße rot; ein Export-Gate ist damit nicht erreicht.

## Änderung und Varianten

`gen_relief.py` füllt als letzten abgeleiteten G-Schritt trockene, abflusslose Mulden im Höhenfeld `G`, wenn deren Fülltiefe über 0,30 m liegt und sie höchstens 6 m von einem Dorfweg oder Rampenweg entfernt sind. Wandflächen bleiben ausgeschlossen. Die ausgewählte Standardvariante lässt 0,29 m Resttiefe stehen, damit die R8b-Schwelle unterschritten wird und Rampenanschlüsse weniger stark verschoben werden. Die Korrektur wird mit Gauß-σ 0,6 auf Anzeigehöhe `GB` und Feinmesh übertragen; 54 betroffene Dekorationsobjekte erhalten den zugehörigen Höhenhub.

| `DELLENWEG` | Ausführung | `pruefe_regeln` | R8 | R9 | Summe | `R8b_delle` |
|---:|---|---:|---:|---:|---:|---:|
| 0 | aus; Basis | 570 | 48 | 334 | 952 | 25 |
| 1 | bis zur Überlaufhöhe füllen | 576 | 52 | 305 | 933 | 0 |
| **2** | **0,29 m Resttiefe; Standard** | **574** | **51** | **304** | **929** | **0** |
| 3 | Variante 2 plus 1-m-Schutz an Rampenenden | 577 | 51 | 307 | 935 | 3 |

Variante 2 bearbeitete 25 Komponenten und 4.494 Gitterpunkte in einem Durchlauf. Der maximale tatsächliche Höhenhub beträgt 3,82 m; der größte Objekt-Hub beträgt 3,464 m. Variante 3 hielt zwar R8 gleich, ließ aber drei R8b-Treffer stehen. Es wurden drei aktive Varianten geprüft; `DELLENWEG=0` schaltet die Änderung aus.

## Trefferzahlen je Regel

| Prüfer | Regel | Vorher | Nachher | Δ |
|---|---|---:|---:|---:|
| `pruefe_regeln` | R1_blind | 24 | 24 | 0 |
| `pruefe_regeln` | R1_wand | 0 | 1 | +1 |
| `pruefe_regeln` | R2_getrennt | 15 | 15 | 0 |
| `pruefe_regeln` | R3_laengs_m | 35 | 38 | +3 |
| `pruefe_regeln` | R3_quer_pct | 23 | 27 | +4 |
| `pruefe_regeln` | R3_woelb_m | 22 | 25 | +3 |
| `pruefe_regeln` | R5_loch | 17 | 17 | 0 |
| `pruefe_regeln` | R6_wasser_schnee | 4 | 4 | 0 |
| `pruefe_regeln` | G2_spitze_oben | 3 | 3 | 0 |
| `pruefe_regeln` | G3_spitze_unten | 3 | 3 | 0 |
| `pruefe_regeln` | G2_spitze_oben_fein | 8 | 7 | −1 |
| `pruefe_regeln` | G3_spitze_unten_fein | 2 | 2 | 0 |
| `pruefe_regeln` | G5_beule_klippe | 68 | 68 | 0 |
| `pruefe_regeln` | G6_facette | 220 | 214 | −6 |
| `pruefe_regeln` | G7_wand_glatte_flaeche | 1 | 1 | 0 |
| `pruefe_regeln` | G7b_wandkontur_rauheit | 1 | 1 | 0 |
| `pruefe_regeln` | G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| `pruefe_regeln` | G7b_wandkontur_feld | 24 | 22 | −2 |
| `pruefe_regeln` | G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| `pruefe_regeln` | G11_baum_an_wand | 0 | 3 | +3 |
| `pruefe_regeln` | T1_fleckrand | 94 | 93 | −1 |
| `pruefe_regeln` | T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| `pruefe_regeln` | T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| `pruefe_regeln` | T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| `pruefe_regeln` | T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |
| **`pruefe_regeln` gesamt** | | **570** | **574** | **+4** |
| R8 | R8_stufe | 9 | 10 | +1 |
| R8 | R8_gitter | 10 | 11 | +1 |
| R8 | R8_quer | 5 | 6 | +1 |
| R8 | R8a_wegende | 24 | 24 | 0 |
| **R8 gesamt** | | **48** | **51** | **+3** |
| R9 | R8b_delle | 25 | 0 | −25 |
| R9 | R9_saegezahn | 34 | 34 | 0 |
| R9 | R9w_wellen | 275 | 270 | −5 |
| **R9 gesamt** | | **334** | **304** | **−30** |
| **Gesamtbilanz** | | **952** | **929** | **−23** |

## Zahlen je Kachel

`pruefe_regeln` zählt Einträge. R8 und R9 sind jeweils Summen ihrer Einzelregeln.

| Kachel | `pruefe_regeln` Vorher → Nachher | R8 Vorher → Nachher | R9 Vorher → Nachher |
|---|---:|---:|---:|
| D1 | 36 → 36 | 8 → 8 | 26 → 24 |
| G1 | 13 → 13 | 1 → 1 | 8 → 7 |
| D2 | 8 → 8 | 0 → 0 | 0 → 0 |

Der Vergleich der D2-Treffer-IDs ergab 0 neue und 0 weggefallene `pruefe_regeln`-Treffer. R8 und R9 bleiben dort bei 0.

## CSV- und D2-Nachweis

Der Vergleich umfasst alle 101.808 Zeilen von `zellen_relief.csv`. Im vorhandenen CSV-Schema heißen die Hindernisfelder `hindernis_id` und `hindernis_art`; `bauzone` ist in `bauzone_bestand` und `bauzone_plan` aufgeteilt.

| Quellfeld laut Auftrag | Tatsächliche CSV-Spalten | Abweichende Werte Vorher/Nachher |
|---|---|---:|
| untergrund | untergrund | 0 |
| hindernis | hindernis_id, hindernis_art | 0 |
| wasser_eis | wasser_eis | 0 |
| ebene | ebene | 0 |
| bauzone | bauzone_bestand, bauzone_plan | 0 |
| begehbar | begehbar | 0 |
| bebaubar | bebaubar | 0 |

Die abgeleiteten Spalten blieben im Export und wurden neu erzeugt. Geänderte Zellen: `hoehe_m` 1.271, `neigung_grad` 1.044, `klippe` 348, `klippe_hoehe_m` 710, `klippe_hoehe_quelle` 188, `begehbar_3d` 126, `deko_baum_ok` 140, jede der vier Eckspalten 1.121, `skin_slot` 160 und `boden_anzeige_m` 15.697. `pruefe_t42u.py` meldet für alle neun Abgleichfelder 0 Abweichungen, Summe 0.

Der gesamte D2-CSV-Ausschnitt hat 1.806 Zeilen und stimmt in allen Spalten überein. Im Relief-JSON sind die D2-Ausschnitte von `G`, `GB`, `WV`, `WEGA` und `VC` bytegleich; ebenso die 17 Feinmesh-Vertex-IDs samt Höhen. Die D2-Objektlisten (7 Häuser, 5 Felsen, 2 Steine und 63 Grasobjekte; übrige geprüfte Objektarten 0) stimmen überein. Der Clay-Render `D2_regression.png` ist vor/nach bytegleich, SHA-256 `abfc64360156b0e2f1f7148423df3f6685ddacab14c503c2535ee818f128f2a9`. Es wurde kein D2-Ergebnis aus einer Referenz zurückkopiert.

Die explizite CSV-Entscheidung wurde angewendet: Quellspalten bytegleich halten und abgeleitete Spalten mit der G-Änderung neu erzeugen und committen. Deshalb wurde die erzeugte CSV nicht nachträglich vollständig auf den Basisstand zurückgesetzt; ein solcher Reset würde die neu abgeleiteten Spalten verwerfen.

## Tonbilder vorher/nachher

Alle Bilder wurden mit `render_t119u.js`, `?clay=1&lod=0`, 1280×800 und derselben Kameraliste `bilder/delle2/k_cams.json` erzeugt. D1-Klippe bei ungefähr 140|35 und die Wandkanten in D1/G1 bleiben sichtbar; in diesen Ansichten sind keine neuen Zähne und keine weggeglättete Klippe erkennbar. Das D2-Paar ist bytegleich.

| Kachel / Kamera | Vorher | Nachher |
|---|---|---|
| D1, Klippe | [D1_klippe](bilder/delle2/vor/D1_klippe.png) | [D1_klippe](bilder/delle2/nachher/D1_klippe.png) |
| D1, Mulde | [D1_mulde](bilder/delle2/vor/D1_mulde.png) | [D1_mulde](bilder/delle2/nachher/D1_mulde.png) |
| G1, Mulde | [G1_mulde](bilder/delle2/vor/G1_mulde.png) | [G1_mulde](bilder/delle2/nachher/G1_mulde.png) |
| G1, Wandkante | [G1_wand](bilder/delle2/vor/G1_wand.png) | [G1_wand](bilder/delle2/nachher/G1_wand.png) |
| F1 | [F1_mulde](bilder/delle2/vor/F1_mulde.png) | [F1_mulde](bilder/delle2/nachher/F1_mulde.png) |
| C3 | [C3_mulde](bilder/delle2/vor/C3_mulde.png) | [C3_mulde](bilder/delle2/nachher/C3_mulde.png) |
| C4 | [C4_mulde](bilder/delle2/vor/C4_mulde.png) | [C4_mulde](bilder/delle2/nachher/C4_mulde.png) |
| C5 | [C5_mulde](bilder/delle2/vor/C5_mulde.png) | [C5_mulde](bilder/delle2/nachher/C5_mulde.png) |
| D6 | [D6_mulde](bilder/delle2/vor/D6_mulde.png) | [D6_mulde](bilder/delle2/nachher/D6_mulde.png) |
| E3 | [E3_mulde](bilder/delle2/vor/E3_mulde.png) | [E3_mulde](bilder/delle2/nachher/E3_mulde.png) |
| E4 | [E4_mulde](bilder/delle2/vor/E4_mulde.png) | [E4_mulde](bilder/delle2/nachher/E4_mulde.png) |
| D2 Kontrolle | [D2_regression](bilder/delle2/vor/D2_regression.png) | [D2_regression](bilder/delle2/nachher/D2_regression.png) |

## Prüfungen

| Prüfung | Ergebnis |
|---|---|
| `python3 gen_relief.py && python3 baue_html.py` | erfolgreich; Standard `DELLENWEG=2`, `WANDSTREIFEN=0` |
| Raycast `loch_o18g.js`, `RAND=0.6` | 1.700.454 Dreiecke im Raycast-Szenenbestand, `offen_innen=0`, `punkte=0` |
| `pruefe_regeln.py` mit Raycast-JSON | 574 Treffer; keine Regel steigt um mehr als 5 |
| `r8_kreuzung.py` | 51 Treffer; Ziel ≤48 verfehlt |
| `r9_form.py` | 304 Treffer; `R8b_delle=0` |
| `pruefe_t42u.py` | Summe 0 |
| Browser LOD1, 390×844, `?clay=1&lod=1` | 407.365 gerenderte Dreiecke (<1,3 Mio.) |
| `LOCHSCAN=/tmp/gate_loch_delle2.json sh pruefung/export_gate.sh` | **GATE ROT**, wegen verbleibender Regelverstöße |

## Annahmen, Grenzen und offene Punkte

- Die Distanz von 6 m folgt der R9-Wegnähe; die Füllung nutzt morphologische Senkenfüllung vom Kartenrand. Wasser und Wandbereiche sind ausgeschlossen. Die Resttiefe von 0,29 m liegt 0,01 m unter der R8b-Schwelle.
- Der reale CSV-Quellbestand hat ein abweichendes Spaltenschema für Hindernisse und Bauzonen; die oben genannten Spaltenpaare sind der direkte Feldvergleich. Es gab 0 Quellwertabweichungen.
- `R8b_delle=0`, `t42u=0`, D2-Regressionsdaten bytegleich, Lochscan ohne offene Innenkanten, LOD1 unter Budget und Gesamtbilanz 929 sind erreicht. Das Ziel `R8<=48` bleibt mit 51 offen; das Export-Gate bleibt rot.
- Overlay, Zellquellen außerhalb der abgeleiteten CSV-Spalten und `../referenz/*` wurden nicht geändert. Die Bildprüfung deckt die genannten Clay-Kameras ab; sie ersetzt keine Freigabe des roten Export-Gates.

## Nachauftrag delle2b · 04.11.2026

Dieser Abschnitt ersetzt für den Branch den vorherigen Standard `DELLENWEG=2`. Commit `a0a618b` bleibt als Verlauf auf `art/dorfmap-delle2`; die breite Füllung wird mit der neuen Standardvariante zurückgenommen. Basis ist `art/dorfmap-grundgeruest` bei `d3843dc`.

### Änderung und Ursache

`DELLENWEG=4` ist jetzt Standard und bleibt über die Umgebungsvariable schaltbar. Es füllt nur trockene Wegsenken mit höchstens 1,0 m maximaler Fülltiefe und höchstens 50 m² zusammenhängender Fläche. 0,29 m Resttiefe bleiben stehen. Komponenten in C4, C5 und D6 sowie in einem 2-m-Rand um diese Kacheln werden vollständig ausgelassen. Dadurch werden 21 flache Komponenten an 94 G-Gitterpunkten angehoben; der maximale Hub beträgt 0,49 m. Drei Dekorationsobjekte werden mit maximal 0,136 m Höhenänderung nachgeführt.

Die großen Becken wurden auf den unveränderten Basisdaten und den Zwischenstufen des G-Aufbaus vermessen:

| Ort / Messung | Quellwerte und abgeleitete Zwischenstufen |
|---|---|
| C4, Fenster x=95–120/z=143–173 | 806 Quellzellen, alle `hoehe_m=0,0`; 762 tragen `ebene=KRATER`, 44 `ebene=WAND`. Der Quellwert ist dort kein abgesenktes Höhenbecken. Die Höhenableitung setzt die Kraterzellen auf 1,0 m. Am R8b-Punkt 106,5\|145,5 liegt G bei 1,0 m. Bereits `g_wandmodell` hat dort 2,899 m Fülltiefe und 4.254 Punkte in der Komponente; nach Erosion sind es 2,703 m/4.583 Punkte, nach Rampenprofil 4,11 m/4.396 Punkte (rund 1.099 m²). Das Becken entsteht somit im abgeleiteten Krater-/Wandmodell und wird im Rampenschritt vertieft. |
| D6, Fenster x=142–160/z=220–238 | 361 Quellzellen: 337 `KLIPPE_WAND`/`WAND` mit `hoehe_m=0,0`, 24 `TAL_SUED` mit `hoehe_m=-7,6`. Am Punkt 150,5\|228 ist die Quellzelle `KLIPPE_WAND`, `wand_name=Suedgrat`, `hoehe_m=0,0`. Der abgeleitete G-Punkt ist `-11,389 m`/3,893 m Fülltiefe in `g_wandmodell`, `-11,797 m`/4,256 m nach Erosion und `-11,277 m`/4,091 m nach dem Rampenschritt. Der zweite R8b-Punkt 155,5\|228,5 hat 1,86 m Tiefe. |

Die Tiefen in C4 und D6 liegen also nicht als entsprechende negative `hoehe_m`-Dellen in den Quellzellen vor; sie entstehen in der abgeleiteten Krater-/Wand-/Rampenform. Die Korrektur sitzt deshalb in der abschließenden Dellen-Füllstufe: Sie unterscheidet kleine Wegdellen von großen oder tiefen Geländebecken. Die Flächen C4/C5/D6 selbst bleiben unverändert. Ihre G-, GB-, WV-, WEGA- und VC-Ausschnitte sind jeweils bytegleich zur Basis.

### Prüfergebnisse je Regel

| Prüfer | Regel | Vorher | Nachher | Δ |
|---|---|---:|---:|---:|
| `pruefe_regeln` | R1_blind | 24 | 24 | 0 |
| `pruefe_regeln` | R1_wand | 0 | 0 | 0 |
| `pruefe_regeln` | R2_getrennt | 15 | 15 | 0 |
| `pruefe_regeln` | R3_laengs_m | 35 | 35 | 0 |
| `pruefe_regeln` | R3_quer_pct | 23 | 23 | 0 |
| `pruefe_regeln` | R3_woelb_m | 22 | 22 | 0 |
| `pruefe_regeln` | R5_loch | 17 | 17 | 0 |
| `pruefe_regeln` | R6_wasser_schnee | 4 | 4 | 0 |
| `pruefe_regeln` | G2_spitze_oben | 3 | 3 | 0 |
| `pruefe_regeln` | G3_spitze_unten | 3 | 3 | 0 |
| `pruefe_regeln` | G2_spitze_oben_fein | 8 | 8 | 0 |
| `pruefe_regeln` | G3_spitze_unten_fein | 2 | 2 | 0 |
| `pruefe_regeln` | G5_beule_klippe | 68 | 68 | 0 |
| `pruefe_regeln` | G6_facette | 220 | 221 | +1 |
| `pruefe_regeln` | G7_wand_glatte_flaeche | 1 | 1 | 0 |
| `pruefe_regeln` | G7b_wandkontur_rauheit | 1 | 1 | 0 |
| `pruefe_regeln` | G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| `pruefe_regeln` | G7b_wandkontur_feld | 24 | 24 | 0 |
| `pruefe_regeln` | G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| `pruefe_regeln` | G11_baum_an_wand | 0 | 0 | 0 |
| `pruefe_regeln` | T1_fleckrand | 94 | 94 | 0 |
| `pruefe_regeln` | T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| `pruefe_regeln` | T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| `pruefe_regeln` | T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| `pruefe_regeln` | T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |
| **`pruefe_regeln` gesamt** | | **570** | **571** | **+1** |
| R8 | R8_stufe | 9 | 9 | 0 |
| R8 | R8_gitter | 10 | 10 | 0 |
| R8 | R8_quer | 5 | 5 | 0 |
| R8 | R8a_wegende | 24 | 24 | 0 |
| **R8 gesamt** | | **48** | **48** | **0** |
| R9 | R8b_delle | 25 | 4 | −21 |
| R9 | R9_saegezahn | 34 | 34 | 0 |
| R9 | R9w_wellen | 275 | 275 | 0 |
| **R9 gesamt** | | **334** | **313** | **−21** |
| **Gesamtbilanz** | | **952** | **932** | **−20** |

Keine Regel steigt um mehr als 1. Der Vergleich der `pruefe_regeln`-Treffer-IDs einschließlich Ort und Wert enthält 9 hinzugekommene und 8 weggefallene Einträge; es gibt keine neuen D2-Treffer. Die hinzugekommenen Einträge liegen außerhalb C4/C5/D6:

| Regel | Kachel / x\|z | Wert |
|---|---|---:|
| R3_laengs_m | F1 / 231,8\|35,4 | 0,109 |
| R3_laengs_m | F1 / 228,0\|36,7 | 0,082 |
| R3_laengs_m | D3 / 127,7\|119,8 | 0,137 |
| R3_laengs_m | C3 / 123,7\|119,6 | 0,146 |
| G6_facette | C3 / 120,0\|119,0 | 13 |
| G6_facette | E3 / 182,9\|120,5 | 10 |
| G6_facette | E3 / 178,7\|126,9 | 17 |
| G6_facette | E4 / 181,2\|130,5 | 6 |
| G7b_wandkontur_feld | C3 / 105\|107 | 0,557 |

Die R3-Zähler bleiben gleich: vier Messwerte haben sich an denselben Rampenproben verändert. Drei G6-Markierungen liegen geringfügig versetzt zu weggefallenen Markierungen in E3/E4; dadurch steigt G6 netto um 1. R9w bleibt bei 275; drei geänderte Wellenmarker liegen in F1 (249,7\|28,0; 0,56), D1 (152,3\|23,7; 0,92) und C3 (124,1\|102,4; 0,61). In C4/C5/D6 gibt es bei keinem der drei Prüfer neue Treffer oder geänderte Trefferzahlen.

### Zahlen je Kachel

| Kachel | `pruefe_regeln` vorher → nachher | R8 vorher → nachher | R9 vorher → nachher |
|---|---:|---:|---:|
| D1 | 36 → 36 | 8 → 8 | 26 → 24 |
| G1 | 13 → 13 | 1 → 1 | 8 → 7 |
| D2 | 8 → 8 | 0 → 0 | 0 → 0 |
| C4 | 32 → 32 | 2 → 2 | 15 → 15 |
| C5 | 48 → 48 | 5 → 5 | 12 → 12 |
| D6 | 16 → 16 | 4 → 4 | 12 → 12 |

Die 4 verbliebenen R8b-Treffer sind unverändert: C4 106,5\|145,5 (4,11 m), C5 108,5\|185,5 (0,31 m), D6 150,5\|228,0 (4,09 m) und D6 155,5\|228,5 (1,86 m). Die 21 flachen Treffer außerhalb der geschützten Kacheln wurden beseitigt.

### CSV, D2 und geschützte Kacheln

Alle 101.808 CSV-Zeilen wurden gegen `d3843dc` verglichen. Für jede Quellspalte gibt es 0 abweichende Werte und identische SHA-256-Werte der Zellwertfolgen: `untergrund`, `hindernis_id`, `hindernis_art`, `wasser_eis`, `ebene`, `bauzone_bestand`, `bauzone_plan`, `begehbar`, `bebaubar`. Das Schema teilt `hindernis` und `bauzone` wie oben beschrieben auf.

Neu erzeugte abgeleitete CSV-Werte gegenüber der Basis: `hoehe_m` 60, `neigung_grad` 44, `klippe` 1, `klippe_hoehe_m` 29, `begehbar_3d` 2, `deko_baum_ok` 1, jede Eckspalte 23, `skin_slot` 1 und `boden_anzeige_m` 14.485 Zellen. `pruefe_t42u.py` meldet Summe 0.

Der D2-CSV-Ausschnitt mit 1.806 Zellen ist in allen Spalten bytegleich. Die D2-Ausschnitte von G, GB, WV, WEGA und VC sowie 17 Feinmesh-Vertex-IDs samt Höhen sind bytegleich; ebenso die D2-Objektlisten (7 Häuser, 5 Felsen, 2 Steine, 63 Grasobjekte, übrige geprüfte Arten 0). Es gibt keine neuen D2-Regeltreffer. Die korrigierte D2-Kamera rendert vor/nach bytegleich.

### Tonbilder

Die neue Kameraliste liegt in [k_cams.json](bilder/delle2b/k_cams.json). Für D2 wurde die Kamera auf Position `[140,28,82]` mit Ziel `[127,0,69]` gesetzt; sie steht sichtbar über dem Gelände und zeigt jetzt Terrain statt des leeren grauen Frames. Vorherbilder außer D2 stammen aus dem unveränderten Basislauf; das D2-Vorherbild wurde mit der korrigierten Kamera auf dem vorherigen D2-bytegleichen Build gerendert. Die C4-, C5-, D6- und D2-Bildpaare sind jeweils bytegleich. D1-Klippe bei 140\|35 sowie die Wandkanten D1/G1 sind im direkten Vorher/Nachher-Vergleich sichtbar erhalten; neue Zähne oder eine weggeglättete Klippe sind in diesen Ansichten nicht zu sehen.

| Kachel / Kamera | Vorher | Nachher |
|---|---|---|
| D1, Klippe | [D1_klippe](bilder/delle2b/vor/D1_klippe.png) | [D1_klippe](bilder/delle2b/nachher/D1_klippe.png) |
| D1, Mulde | [D1_mulde](bilder/delle2b/vor/D1_mulde.png) | [D1_mulde](bilder/delle2b/nachher/D1_mulde.png) |
| G1, Mulde | [G1_mulde](bilder/delle2b/vor/G1_mulde.png) | [G1_mulde](bilder/delle2b/nachher/G1_mulde.png) |
| G1, Wandkante | [G1_wand](bilder/delle2b/vor/G1_wand.png) | [G1_wand](bilder/delle2b/nachher/G1_wand.png) |
| C3 | [C3_mulde](bilder/delle2b/vor/C3_mulde.png) | [C3_mulde](bilder/delle2b/nachher/C3_mulde.png) |
| E3 | [E3_mulde](bilder/delle2b/vor/E3_mulde.png) | [E3_mulde](bilder/delle2b/nachher/E3_mulde.png) |
| E4 | [E4_mulde](bilder/delle2b/vor/E4_mulde.png) | [E4_mulde](bilder/delle2b/nachher/E4_mulde.png) |
| F1 | [F1_mulde](bilder/delle2b/vor/F1_mulde.png) | [F1_mulde](bilder/delle2b/nachher/F1_mulde.png) |
| C4, Becken | [C4_mulde](bilder/delle2b/vor/C4_mulde.png) | [C4_mulde](bilder/delle2b/nachher/C4_mulde.png) |
| C5 | [C5_mulde](bilder/delle2b/vor/C5_mulde.png) | [C5_mulde](bilder/delle2b/nachher/C5_mulde.png) |
| D6, Becken | [D6_mulde](bilder/delle2b/vor/D6_mulde.png) | [D6_mulde](bilder/delle2b/nachher/D6_mulde.png) |
| D2 Kontrolle | [D2_regression](bilder/delle2b/vor/D2_regression.png) | [D2_regression](bilder/delle2b/nachher/D2_regression.png) |

### Pflichtprüfungen und Grenzen

| Prüfung | Ergebnis |
|---|---|
| `DELLENWEG=4 python3 gen_relief.py && python3 baue_html.py` | erfolgreich; `WANDSTREIFEN=0`; 21 Komponenten/94 Punkte, maximal 0,49 m Hub |
| Raycast `loch_o18g.js`, `RAND=0.6` | 1.700.454 Dreiecke, `offen_innen=0`, `punkte=0` |
| `pruefe_regeln.py` mit `/tmp/gate_loch_delle2b.json` | 571 Treffer (+1); keine Regel über +5, keine neuen D2-Treffer |
| `r8_kreuzung.py` | 48 Treffer; Ziel erreicht |
| `r9_form.py` | 313 Treffer; `R8b_delle` 25→4 |
| `pruefe_t42u.py` | Summe 0 |
| LOD1, 390×844, `?clay=1&lod=1` | 407.365 gerenderte Dreiecke (<1,3 Mio.) |
| `LOCHSCAN=/tmp/gate_loch_delle2b.json sh pruefung/export_gate.sh` | **GATE ROT**, da 571 `pruefe_regeln`-Treffer bestehen |

`export_gate.sh` setzt intern fest `LOCHSCAN=/tmp/gate_loch.json` und übersteuert damit den übergebenen Dateinamen. Diese vorhandene Datei meldete `offen_innen=0`; der direkte Prüflauf oben verwendete die eigene tag-spezifische Raycast-Datei. Prüfer und Schwellen wurden nicht geändert.

Die Ziele `R8<=48`, `R8b` deutlich reduziert, keine neuen Treffer oder Tonbildänderungen in C4/C5/D6, D2 bytegleich, `t42u=0` und LOD1-Budget sind erreicht. `R8b_delle=4` bleibt bewusst in den unveränderten C4/C5/D6-Flächen; das Export-Gate ist wegen der sonstigen Kartenregeln weiter rot. Die 1,0-m-/50-m²-Grenzen und der 2-m-Kachelschutz sind Implementierungsannahmen; eine Neubeurteilung ist nötig, falls Rastermaß oder Kachelgrenzen geändert werden.
