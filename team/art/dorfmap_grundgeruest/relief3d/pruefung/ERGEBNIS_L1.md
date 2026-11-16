# Ergebnis L1

**[S] Basis:** `07f10ac7b5142852928ccae0ba751553b4e49275` (`origin/art/dorfmap-fertig`). **Branch:** `art/dorfmap-L1`. **Standard:** `RELIEF_L1_VAR=2`.

## Ergebnis und Methode

- **[S]** Der unveränderte Stand wurde vor dem Eingriff geprüft: `pruefe_regeln` 570, R8 48, R9 334. Der finale Build mit Variante 2 ergibt erneut 570 / 48 / 334. Keine Regel und keine Kachel steigt; R5 bleibt 17. Lochscan: 0 offene Innenlöcher, 0 Punkte. D2 hat keine neuen Treffer; dort sind `pruefe_regeln` 8, R8 0, R9 0.
- **[R]** Ein globaler, deterministischer Gauß-Tiefpass wird einmal auf das sichtbare Höhenfeld `GB` angewandt. Variante 2 verwendet σ=1,00 m, Blend 0,80 und eine Korrekturbegrenzung von 0,50 m. Die Korrektur wird in Wand-/Klippenbändern, Wasser samt 2-m-Uferzone, Wegen und Rampen samt 3,5-m-Zone sowie Kachelrändern (1 m) ausgeblendet; D2 samt Randpunkten bleibt vollständig gesperrt. Quellfeld `G` und Overlay-Daten werden nicht nachbearbeitet.
- **[R]** Variante 2 änderte 134.454 Grobnetzpunkte; maximale Korrektur 0,119159 m, RMS 0,009268 m. Kein gespeicherter Feinmesh-Höhenpunkt änderte sich. Der Lauf ist eine weiche globale Glättung, keine gezielte Entfernung einzelner Facetten oder Spitzen.
- **[A]** Die Gates belegen Sicherheit im Sinne der vorgegebenen Treffergrenzen, aber keine deutliche optische Verbesserung: Alle Regeln und Kacheln haben in Variante 2 dieselben Trefferzahlen wie vorher. Beim internen Kartenvergleich war kein klar sichtbarer Gesamteffekt erkennbar. Das Sichtbarkeitsziel ist damit **nicht nachgewiesen**.

## Varianten

| Variante | σ / Blend / Korrekturgrenze | Geänderte Grobpunkte | max / RMS Korrektur | Gate-Ergebnis |
|---|---:|---:|---:|---|
| 0 | unverändert | 0 | 0 / 0 m | bytegleich zur Eingabe |
| 1 | 0,75 m / 0,75 / 0,35 m | 121.605 | 0,077485 / 0,005261 m | 570 / 48 / 334, keine Regel- oder Kachelzunahme |
| **2 (Standard)** | **1,00 m / 0,80 / 0,50 m** | **134.454** | **0,119159 / 0,009268 m** | **570 / 48 / 334, keine Regel- oder Kachelzunahme** |
| 3 | 2,00 m / 0,90 / 0,90 m | 153.812 | 0,372039 / 0,034852 m | verworfen: G6 220→221 (neuer Treffer C2, 3→4); Gesamtsumme 571 |

**[R]** Variante 2 ist die stärkste gerechnete Glättung, die alle Regel-/Kachelgrenzen einhält. Variante 1 brachte ebenfalls keine Trefferreduktion. Variante 3 bleibt abschaltbar, ist nicht Standard.

## Treffer je Regel: vorher → Standard 2

| Prüfung | Regel | Vorher | Nachher |
|---|---|---:|---:|
| Regeln | R1_blind | 24 | 24 |
| Regeln | R2_getrennt | 15 | 15 |
| Regeln | R3_laengs_m | 35 | 35 |
| Regeln | R3_quer_pct | 23 | 23 |
| Regeln | R3_woelb_m | 22 | 22 |
| Regeln | R5_loch | 17 | 17 |
| Regeln | R6_wasser_schnee | 4 | 4 |
| Regeln | G2_spitze_oben | 3 | 3 |
| Regeln | G3_spitze_unten | 3 | 3 |
| Regeln | G2_spitze_oben_fein | 8 | 8 |
| Regeln | G3_spitze_unten_fein | 2 | 2 |
| Regeln | G5_beule_klippe | 68 | 68 |
| Regeln | G6_facette | 220 | 220 |
| Regeln | G7_wand_glatte_flaeche | 1 | 1 |
| Regeln | G8_fluss_nicht_bis_rand | 1 | 1 |
| Regeln | T1_fleckrand | 94 | 94 |
| Regeln | T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 |
| Regeln | T3_streifen_ringe_bildpruefung_offen | 1 | 1 |
| Regeln | T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 |
| Regeln | T5_textur_vs_clay_bildpruefung_offen | 1 | 1 |
| Regeln | G7b_wandkontur_rauheit | 1 | 1 |
| Regeln | G7b_wandkontur_kantenschaerfe | 1 | 1 |
| Regeln | G7b_wandkontur_feld | 24 | 24 |
| Regeln | **Summe** | **570** | **570** |
| R8 | R8_stufe | 9 | 9 |
| R8 | R8_gitter | 10 | 10 |
| R8 | R8_quer | 5 | 5 |
| R8 | R8a_wegende | 24 | 24 |
| R8 | **Summe** | **48** | **48** |
| R9 | R8b_delle | 25 | 25 |
| R9 | R9_saegezahn | 34 | 34 |
| R9 | R9w_wellen | 275 | 275 |
| R9 | **Summe** | **334** | **334** |

**[R] Kacheln mit größter Verbesserung:** keine zählbare Verbesserung. In D1, G1 und allen übrigen Kacheln blieben die Treffer je Regel gleich. Die geänderten Höhenpunkte sind keine belegte Fehlerreduktion.

## D1 / G1 / D2 je Kachel

| Kachel | Regeln vorher→nachher | R8 vorher→nachher | R9 vorher→nachher | Summe vorher→nachher |
|---|---:|---:|---:|---:|
| D1 | 36→36 | 8→8 | 26→26 | 70→70 |
| G1 | 13→13 | 1→1 | 8→8 | 22→22 |
| D2 | 8→8 | 0→0 | 0→0 | 8→8 |

**[R]** D2-Grobhöhen wurden aus dem finalen `relief_daten.json.gz` bitweise mit dem Basisstand verglichen: identisch. Auch der D2-Hash aus `neu/build.json` bleibt `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`.

## Zehn auffälligste Reststellen in Variante 2

| Regel | Kachel | x\|z (m) | Wert | Schwelle |
|---|---|---:|---:|---:|
| G5_beule_klippe | G4 | 274,3\|132,8 | 4,44 m | >0,60 m |
| G6_facette | B3 | 79,0\|126,2 | 103 Zellen | zusammenhängend ≥6 Zellen |
| G2_spitze_oben_fein | B4 | 72,8\|142,2 | 0,59 m | >0,45 m |
| G3_spitze_unten_fein | H2 | 306,5\|85,5 | 0,54 m | >0,45 m |
| R5_loch | D6 | 151,5\|228,5 | 2,57 m | >1,00 m |
| R3_quer_pct | D1 | 151,8\|29,6 | 99,3 % | >3,5 % |
| R3_woelb_m | D1 | 150,3\|28,7 | 1,793 m | >0,08 m |
| R3_laengs_m | D1 | 153,7\|26,1 | 1,378 m | >0,08 m |
| R8_quer | C3 | 125,3\|126,5 | 141,4 % | >3,0 % |
| R9_saegezahn | C3 | 123,5\|93,5 | 133 Zacken | ≥3 Zacken |

## Unveränderte Eingaben, Prüfung und Grenzen

- **[S] Geschützte Eingaben (SHA-256):** `neu/zellen_relief.csv` `99d30e55310453725aa1c9613900b5203f430f75f19745244fe3ebd650fc93fa`; `neu/vektor.json` `aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e`; `neu/felder.json` `e4e2ec8f5f4b7b7bb825f8fdda6c0400b5525e9c8c31153f7d9b10d4185e3435`. Die unveränderten Quellfelder `G`, `WV`, `WEGA`, `wege` und `rampenwege` stimmen ebenfalls byte-/wertgleich mit dem Basisbuild überein. Overlay, Prüfer und `../referenz/*` wurden nicht geändert.
- **[R] Prüfungen:** Lochscan mit `NODE_PATH` gesetzt: 0 offene Innenlöcher. `pruefe_regeln`: 570; R8: 48; R9: 334. `pruefe_t42u.py`: Summe 0. Gerenderte LOD1-Dreiecke: 1.174.582 (<1,3 Mio.).
- **[A] Grenzen/offene Punkte:** Die Höhenkorrektur ist klein und die gespeicherten Feinmesh-Höhen blieben unverändert. Die Gates messen keine sichere visuelle Verbesserung; mehrere große Resttreffer (oben) bestehen weiter. Der Test schützt Trefferzahlen und D2, er ersetzt keine Nahbild-Sichtprüfung.
- **[A] Vorschlag L2:** keinen stärkeren Gauß-Lauf anschließen. Einen kantenbewussten globalen Filter (bilateral/anisotrop) mit denselben Sperrbändern als eigene Variante prüfen und mit gezielten Nahbildern der obigen Reststellen bewerten; nur bei sichtbarer Verbesserung übernehmen. D2, Quellfelder und Prüfer dabei unverändert halten.
- **[R] Laufzeit:** rund 48 Minuten vom Start um 07:18 CET bis zum finalen Gate-/LOD1-Lauf. Es wurden keine kostenpflichtigen Dienste verwendet (0 EUR).
