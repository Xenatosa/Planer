# Ergebnis Delle2

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
