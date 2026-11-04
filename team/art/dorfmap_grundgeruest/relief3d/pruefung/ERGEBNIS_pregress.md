# Ergebnis pregress

## Zusammenfassung

Die Fabian-Beanstandungen sind als Negativreferenzen und sieben feste Regressionstests erfasst. Alle sieben Tests sind auf dem aktuellen Stand rot und messen damit die noch vorhandenen Beanstandungen. Der neue Python-Kern baut deterministische, indizierte Netze für D1, G1 und D2. Er ist mit `RELIEF_NEU=1` zuschaltbar; ohne Variable bleibt der bisherige Pfad Standard.

Der Prototyp behebt die Beanstandungen noch nicht: `main.js` liest `neu_mesh_tiles` derzeit nicht als Rendergeometrie. Das optionale Paket enthält daher die zusätzlichen Netze, während die Seite weiterhin die vorhandene Szene rendert. Rendereradapter und neue D1/G1-Geometrie sind offene Arbeiten.

## Aenderungen

- Neuer deterministischer Meshkern und optionaler Paketbau unter [`neu/mesh.py`](../neu/mesh.py) und [`neu/pipeline.py`](../neu/pipeline.py).
- `RELIEF_NEU=1` waehlt den neuen Paketbau in `gen_relief.py` und bindet das optionale Paket in `baue_html.py` ein. Ohne den Schalter bleibt der bisherige Ablauf aktiv.
- Drei Netze fuer D1, G1 und D2: jeweils 7.395 Vertices und 14.448 Dreiecke, insgesamt 43.344 Dreiecke.
- Fabian-Bilder als Kopien und mit Koordinate, Fehlerart und Beschreibung im [Index](../neu/referenz_neg/Index.csv). Automatische Beanstandungstests stehen in [`test_beanstandungen.py`](../neu/tests/test_beanstandungen.py); Kern- und Determinismustests in [`test_neu_kern.py`](../neu/tests/test_neu_kern.py).
- Der Standardlauf hat nur die abgeleitete CSV-Spalte `boden_anzeige_m` in 14.429 Zellen neu exportiert. Bei den neun geschuetzten Quellspalten gab es null geaenderte Werte. `relief_daten.json.gz`, Overlay und `../referenz/*` blieben unveraendert.

## Gates vorher und nachher

Vorher ist der tatsaechlich ausgecheckte Branchstand `7c0df80` (t134u); nachher ist der Stand nach den Aenderungen. Der vom Auftrag genannte historische Stand `9d3f8fc` hatte bei `pruefe_regeln` 596 Treffer. Auf dem hier bearbeiteten Branch waren es vor Beginn 570. R8 und R9 stimmen mit den angegebenen Ausgangswerten ueberein. Die Tabellen zeigen Branch-Vorher und Branch-Nachher; keine Regel hat zugenommen.

| Gate / Regel | Vorher | Nachher | Delta |
|---|---:|---:|---:|
| `pruefe_regeln` gesamt | 570 | 570 | 0 |
| R1_blind | 24 | 24 | 0 |
| R2_getrennt | 15 | 15 | 0 |
| R3_laengs_m | 35 | 35 | 0 |
| R3_quer_pct | 23 | 23 | 0 |
| R3_woelb_m | 22 | 22 | 0 |
| R5_loch | 17 | 17 | 0 |
| R6_wasser_schnee | 4 | 4 | 0 |
| G2_spitze_oben | 3 | 3 | 0 |
| G2_spitze_oben_fein | 8 | 8 | 0 |
| G3_spitze_unten | 3 | 3 | 0 |
| G3_spitze_unten_fein | 2 | 2 | 0 |
| G5_beule_klippe | 68 | 68 | 0 |
| G6_facette | 220 | 220 | 0 |
| G7_wand_glatte_flaeche | 1 | 1 | 0 |
| G7b_wandkontur_feld | 24 | 24 | 0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| T1_fleckrand | 94 | 94 | 0 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |
| R8 gesamt | 48 | 48 | 0 |
| R8_stufe | 9 | 9 | 0 |
| R8_gitter | 10 | 10 | 0 |
| R8_quer | 5 | 5 | 0 |
| R8a_wegende | 24 | 24 | 0 |
| R9 gesamt | 334 | 334 | 0 |
| R8b_delle | 25 | 25 | 0 |
| R9_saegezahn | 34 | 34 | 0 |
| R9w_wellen | 275 | 275 | 0 |
| t42u Abweichungssumme | 0 | 0 | 0 |
| Innere offene Meshkanten | 0 | 0 | 0 |

`pruefe_regeln` hatte vor G7b in seiner Diagnose 544 Treffer und danach 570 einschliesslich 26 G7b-Treffern. Die D2-Treffer in `pruefe_regeln` blieben bei 8 (R2_getrennt 1, T1_fleckrand 7); D2 hat in R8 und R9 jeweils 0 Treffer. Die Zahl der gerenderten Dreiecke der Gesamtseite im LOD1-Lauf betraegt 1.174.554 und liegt damit unter 1,3 Mio.

### Treffer je Kachel

Die Vorher- und Nachherwerte sind auch in jeder Kachel gleich.

| Kachel | `pruefe_regeln` | R8 | R9 |
|---|---:|---:|---:|
| D1 | 36 | 8 | 26 |
| G1 | 13 | 1 | 8 |
| D2 | 8 | 0 | 0 |

| Kachel | Regeln: Aufschluesselung | R8: Aufschluesselung | R9: Aufschluesselung |
|---|---|---|---|
| D1 | R1 2, R2 1, R3_laengs 6, R3_quer 11, R3_woelb 10, G5 1, G6 5 | Stufe 2, Gitter 2, Quer 1, Wegende 3 | Delle 2, Saegezahn 1, Wellen 23 |
| G1 | R1 1, R3_laengs 1, R6 3, G3_spitze_unten_fein 1, G6 4, T1 3 | Wegende 1 | Delle 1, Saegezahn 1, Wellen 6 |
| D2 | R2 1, T1 7 | keine | keine |

## Zellwerte und D2

Die Spalten `untergrund`, `hindernis_id`, `hindernis_art`, `wasser_eis`, `ebene`, `bauzone_bestand`, `bauzone_plan`, `begehbar` und `bebaubar` haben jeweils 0 Wertedifferenzen zum Beginn des Auftrags (SHA-256 pro Spalte vor/nach identisch). Die CSV-Neuausgabe aenderte ausschliesslich `boden_anzeige_m` in 14.429 Zellen.

Die originale `relief_daten.json.gz` blieb unangetastet. Der neue Loader verwendet `GB`, also das Feld, das der bestehende Viewer bei vorhandenem `GB` darstellt. Die D2-Vertices werden direkt aus dessen D2-Ausschnitt kopiert und nicht zurueckgeschrieben oder angepasst: 7.395 Hoehenwerte, SHA-256 `52516cbd116d8f4d460d2f3f70ec6e12f9a4909dd8b06e000da5042568969650`. Der Pakettest vergleicht diese Bytes mit dem D2-Quellausschnitt und vergleicht alle alten Paketfelder byte-/wertgleich; nur `neu_mesh_tiles` kommt hinzu. Ein Screenshot-Pixelvergleich wurde nicht abgeschlossen, daher ist die D2-Aussage auf die Zell-/Hoehenfeld- und Paketbytes begrenzt.

## Fabian-Regressionen

Alle sieben Tests wurden auf dem aktuellen Grundgeruest ausgefuehrt. Rot ist hier das gewollte Ergebnis, solange der jeweilige Fehler noch besteht.

| Test | Messwert | Feste Schwelle | Heute |
|---|---:|---:|---|
| Kreuzung D1/G1, maximale Stufe | 1,389 m | <= 0,20 m | rot |
| Wegende allgemein, R8a | 24 Treffer | 0 Treffer | rot |
| Delle G1 bei 278,5|27,0 | 0,42 m | <= 0,30 m | rot |
| Saegezahn D1, R9 | 41 Zahnelemente | 0 | rot |
| Verwaschene D1-Wand, Bildkante p90 | 2,24 Graustufen/Pixel | >= 3,00 | rot |
| Wegenden F1/C1 | F1 0,17 m; C1 0 explizite Messungen | F1 <= 0,10 m; C1 >= 1 | rot |
| Schattenartefakt, Bild-ROI Hochfrequenzrest | 0,307 | <= 0,25 Graustufen | rot |

Ausfuehrung: `PYTHONPATH=/tmp/pregress_pytest python3 -m pytest -q neu/tests/test_beanstandungen.py` ergab `7 failed`; die erwarteten Fehlermeldungen enthalten jeweils den Messwert. `PYTHONPATH=/tmp/pregress_pytest python3 -m pytest -q neu/tests/test_neu_kern.py` ergab `4 passed`. Pytest wurde fuer diese Ausfuehrung unter `/tmp/pregress_pytest` bereitgestellt.

## Befehle und Messgrenzen

Ausgefuehrt wurden der Standardbau `python3 gen_relief.py && python3 baue_html.py`, der opt-in Bau `RELIEF_NEU=1 python3 gen_relief.py && RELIEF_NEU=1 python3 baue_html.py`, die vier vorgegebenen Gates mit eigenen `/tmp/*_pregress` Dateien sowie `python3 pruefung/pruefe_t42u.py`. Der optionale Bau wurde danach nicht als Standard belassen; `index.html` wurde mit dem Standardpfad gebaut. LOD1 wurde auf dieser Standardseite mit `test_dreiecke_l1.js` gemessen.

Die neuen Kachelmeshes sind deterministische Rastertriangulierungen des bestehenden `GB`-Feldes. Sie sind noch kein neu berechnetes D1/G1-Oberflaechenmodell. Die Beanstandungstests verwenden die bestehenden R8/R9-Messungen beziehungsweise feste Bild-ROIs und zeigen den aktuellen Fehlerzustand; sie belegen keine Verbesserung. Der Schatten- und Wandtest sind an die vorliegenden Fabian-Renderbilder und deren Bildausschnitt gebunden. C1 hat im bestehenden R8-Auszug keine explizite Endpunktmessung, was der Test als fehlende Messabdeckung ebenfalls rot meldet.

Kosten: 0 EUR. Keine Prozesspools verwendet. Zellquellwerte, Overlay, D2-Quellfeld und `../referenz/*` wurden nicht editiert. Die CSV hat bereits im Ausgangsstand CRLF-Zeilenenden; diese wurden beibehalten. `git diff --check` markiert deshalb die CR-Zeichen am Ende geaenderter CSV-Zeilen als Whitespace, obwohl das Zeilenende dem Originalformat entspricht.
