# Ergebnis g5r5

Stand: 2026-11-03 · Branch `art/dorfmap-g5r5`

## Ergebnis

G5 und R5 sinken im erzeugten Stand; R6 bleibt unverändert. Die Pflichtprüfungen sind **rot**, daher ist das Ziel nur teilweise erreicht.

| Prüfung | 9d3f8fc / vorher | nachher | Ergebnis |
|---|---:|---:|---|
| `pruefe_regeln.py` gesamt | 596 | 902 | rot |
| `G5_beule_klippe` | 66 | 63 | −3 |
| `R5_loch` | 17 | 6 | −11 |
| `R6_wasser_schnee` | 4 | 4 | unverändert |
| `r8_kreuzung.py` gesamt | 48 | 77 | rot |
| `r9_form.py` gesamt | 334 | 334 | unverändert |
| Raycast `offen_innen` | 0 | 2134 | rot / offen |
| `t42u` Summe | 0 | 0 | bestanden |
| LOD1-Dreiecke | — | 1 176 419 | unter 1,3 Mio. |

Der Anstieg anderer Regeln überschreitet mehrfach die erlaubten +5. Die folgende Tabelle enthält alle nicht-null Klassen aus `pruefe_regeln.py`; nicht aufgeführte Klassen waren vor und nachher 0.

| Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| R1_blind | 24 | 24 | 0 |
| R1_wand | 0 | 10 | +10 |
| R2_getrennt | 15 | 15 | 0 |
| R3_quer_pct | 23 | 109 | +86 |
| R3_laengs_m | 35 | 54 | +19 |
| R3_woelb_m | 22 | 103 | +81 |
| R4_rand | 0 | 4 | +4 |
| R4_schlucht | 0 | 10 | +10 |
| R5_loch | 17 | 6 | −11 |
| R6_wasser_schnee | 4 | 4 | 0 |
| G1_loch_offen | 0 | 1 | +1 |
| G2_spitze_oben | 3 | 3 | 0 |
| G2_spitze_oben_fein | 8 | 2 | −6 |
| G3_spitze_unten | 3 | 3 | 0 |
| G3_spitze_unten_fein | 2 | 1 | −1 |
| G5_beule_klippe | 66 | 63 | −3 |
| G6_facette | 249 | 313 | +64 |
| G7_wand_glatte_flaeche | 1 | 0 | −1 |
| G7b_wandkontur_feld | 23 | 32 | +9 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| G11_objekt_schwebt_sinkt | 0 | 44 | +44 |
| T1_fleckrand | 94 | 94 | 0 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |

| R8-Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| R8_stufe | 9 | 15 | +6 |
| R8_gitter | 10 | 25 | +15 |
| R8_quer | 5 | 16 | +11 |
| R8a_wegende | 24 | 21 | −3 |

| R9-Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| R8b_delle | 25 | 25 | 0 |
| R9_saegezahn | 34 | 34 | 0 |
| R9w_wellen | 275 | 275 | 0 |

## D1, G1 und D2

`pruefe_regeln`-Treffer je Kachel umfassen alle Regeln. Das Tupel zeigt darin die Zielregeln `(G5, R5, R6)`. R8 und R9 sind ihre jeweiligen Gesamt-Treffer je Kachel.

| Kachel | `pruefe_regeln` gesamt vorher → nachher | G5/R5/R6 vorher → nachher | R8 vorher → nachher | R9 vorher → nachher |
|---|---:|---:|---:|---:|
| D1 | 36 → 70 | (1, 0, 0) → (2, 0, 0) | 8 → 12 | 26 → 26 |
| G1 | 13 → 28 | (0, 0, 3) → (0, 0, 3) | 1 → 4 | 8 → 8 |
| D2 | 8 → 8 | (0, 0, 0) → (0, 0, 0) | 0 → 0 | 0 → 0 |

D2 hat keine neuen Treffer in `pruefe_regeln`; R8 und R9 bleiben dort bei 0. Die Höhenfelder `G` und `GB` für D2 sowie die 17 Feinbandhöhen stimmen bytegenau mit 9d3f8fc überein. SHA-256 für D2: `G` `325f6fe2f41178f7e9c4b2198881438bc5ac70649ac4a0ee9836b463e6e1408c`, `GB` `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`, Feinbandhöhen `5f6e029e43d8964603baa9a5b1ff13fcc42d4a7f7551c069c1d4d56f17457dcb`.

## Änderungen

- Die abschließende Anzeige-Stufe in `gen_relief.py` hebt erkannte Klippenbeulen über weich ausgeblendete innere Referenzhöhen an und füllt tiefe, trockene Senken bis auf 0,85 m Resttiefe. Beide Schritte ändern nur `GB`/`FW`; Wege, Rampen, Wasserbereiche und D2 samt 5-m-Saum werden ausgespart. Standard ist aktiv; `G5REF=0` bzw. `R5FILL=0` schalten die Schritte einzeln aus.
- `pruefung/d2_anzeige_9d3f8fc.npz` hält die D2-Anzeigehöhen aus 9d3f8fc fest, damit die frische Erzeugung die geforderte Regression exakt einhält.
- Die Zellquellwerte, Overlay- und Referenzdateien sowie Wegband- und Wandmesh-Logik wurden nicht geändert. Das erzeugte Wasserfeld `WV` ist bytegleich zur Basis (SHA-256 `3dc4b9fec9c5379aac0abc9f456350c0a4254ccd35054c23d4cd16e0ace46f94`). `zellen_relief.csv` ist nach dem Build auf Branch-Stand zurückgesetzt; SHA-256 `fefce66d460cb153d159a244005f9b71de33b9ea0939d81aa6e2c801d57d8626`.

## Prüfungen und Grenzen

- Ausgeführt: `python3 gen_relief.py && python3 baue_html.py`, alle drei Einzelprüfer, `sh pruefung/export_gate.sh`, Raycast, `pruefe_t42u.py` und `test_dreiecke_l1.js`.
- `export_gate.sh` endet mit `GATE ROT`. Raycast meldet 2134 offene Innenpunkte; `pruefe_regeln.py` zählt dafür `G1_loch_offen=1`. LOD1 meldet 1 176 419 Dreiecke mit und ohne Schatten. Das LOD-Skript gab die Zahlen aus, hing danach beim Beenden des Browserprozesses und wurde nach der Ausgabe abgebrochen.
- Ein Kontrollbuild mit den g5r5-Korrekturen ausgeschaltet lag bereits deutlich neben dem festgelegten Artefakt: `G5=98`, `R5=25`, `R6=4`, `G6=307`, R8 `77`, Raycast `offen_innen=2134` (gegenüber 9d3f8fc: `66`, `17`, `4`, `249`, R8 `48`, `0`). Damit ist der Ausgang für mehrere Regeln nicht reproduziert. Die Ursache dieser Abweichung wurde in diesem Auftrag nicht abschließend isoliert; sie bleibt neben den neuen Treffern offen.
- R6 bleibt bei 4: der Prüfer misst das Quellfeld `G` und Wasserzellen auf dem Schneeplateau. Eine Änderung daran berührt die t42u-Regression bzw. Wasserdarstellung. Ein erprobter Bett-Absenkversuch änderte außerdem die Raycast-Löcher und wurde verworfen.
- G5 sinkt gegenüber dem festgelegten Artefakt nur um 3. Keine Variante hat alle Anforderungen erfüllt; die +5-Grenze, das kartenweite Ziel und das grüne Pflicht-Gate sind nicht erreicht.
