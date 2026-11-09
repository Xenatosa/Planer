# Ergebnis p3d10 – D1-Rampenprofile und Kreuzung

## Ergebnis in Kürze

Die Standardvariante `RELIEF_KREUZUNG_VAR=10` löst beide Rampen über ihre ganze Polylinie und berechnet eine gemeinsame ebene Kreuzungsfläche. Die MILP-Lösung ist optimal für die Minimierung der verletzten 4-m-Abschnitte: 6 Abschnitte bleiben über dem R3-Grenzwert. Der 2D-Transfer ins Mesh erfüllt den geforderten Achsabgleich jedoch nicht an allen Stationen. Die R3-Zahlen und die gemessene Kreuzungsstufe verfehlen die Ziele; mehrere Regeln und Bildmetriken regressieren. D2-Höhenfeld und Adapter-Meshbytes sind unverändert, der neu gerenderte D2-Screenshot ist aber nicht bytegleich zur Referenz. Der Auftrag ist damit **nicht vollständig erreicht**.

## Änderungen

- `neu/mesh.py`: Varianten 8, 9 und 10 für ganzheitliche Profile von `rampe_2`/`rampe_11`; Variante 5 bleibt Referenz. Standard ist 10 (Mischform mit Wandbegrenzung). Der volle Gewichtungsstreifen ist 1,81 m breit, gefolgt von einem 10-m-Höhenfade. Variante 8 lässt den wandseitigen Rampenabschnitt frei; 9 hält `rampe_11` ab Station 40 fest; 10 begrenzt dort die Abweichung zur p3d6-Fläche auf 0,25 m.
- `neu/README.md`: Beschreibung der Varianten und Verweis auf diesen Bericht.
- Neu gebaut: `index.html`, `neu/index.html`, `neu/build.json`; dazu Prüfbilder, Deltas und vollständige Profil-/Mesh-Abtasttabelle unter `pruefung/bilder_p3d10/`.
- Keine Schwellen, Tests, Prüfer, Quellzellen, Overlay oder Referenzdateien geändert.

## Regeln: p3d6 / p3d8 / p3d10

Messwerte stammen aus `neu_mesh_adapter.py`-Gate-Eingaben. Tabellenwerte je Kachel sind Trefferzahlen; Spalten „D1/G1/D2“ zeigen p3d8 → p3d10. p3d6 ist als unabhängige Referenz in der Gesamtspalte enthalten. `—` bedeutet null Treffer.

| Gruppe / Regel | Gesamt p3d6 / p3d8 / p3d10 | D1 p3d8→10 | G1 p3d8→10 | D2 p3d8→10 |
|---|---:|---:|---:|---:|
| Prüfe-Regeln / `R1_blind` | 24 / 24 / 24 | 2→2 | 1→1 | 0→0 |
| Prüfe-Regeln / `R2_getrennt` | 15 / 15 / 15 | 1→1 | 0→0 | 1→1 |
| Prüfe-Regeln / `R3_laengs_m` | 39 / 43 / 35 | 14→6 | 1→1 | 0→0 |
| Prüfe-Regeln / `R3_woelb_m` | 19 / 20 / 19 | 8→7 | 0→0 | 0→0 |
| Prüfe-Regeln / `R3_quer_pct` | 19 / 21 / 21 | 9→9 | 0→0 | 0→0 |
| Prüfe-Regeln / `R5_loch` | 17 / 17 / 17 | 0→0 | 0→0 | 0→0 |
| Prüfe-Regeln / `R6_wasser_schnee` | 4 / 4 / 4 | 0→0 | 3→3 | 0→0 |
| Prüfe-Regeln / `G2_spitze_oben` | 3 / 3 / 3 | 0→0 | 0→0 | 0→0 |
| Prüfe-Regeln / `G3_spitze_unten` | 3 / 3 / 3 | 0→0 | 0→0 | 0→0 |
| Prüfe-Regeln / `G2_spitze_oben_fein` | 8 / 8 / 8 | 0→0 | 0→0 | 0→0 |
| Prüfe-Regeln / `G3_spitze_unten_fein` | 2 / 2 / 2 | 0→0 | 0→0 | 0→0 |
| Prüfe-Regeln / `G5_beule_klippe` | 67 / 67 / 67 | 0→0 | 0→0 | 0→0 |
| Prüfe-Regeln / `G6_facette` | 216 / 216 / 218 | 0→2 | 3→3 | 0→0 |
| Prüfe-Regeln / `G7_wand_glatte_flaeche` | 1 / 1 / 1 | 0→0 | 0→0 | 0→0 |
| Prüfe-Regeln / `G8_fluss_nicht_bis_rand` | 1 / 1 / 1 | 0→0 | 0→0 | 0→0 |
| Prüfe-Regeln / `T1_fleckrand` | 94 / 94 / 94 | 0→0 | 3→3 | 7→7 |
| Prüfe-Regeln / `T2_textur_abgeschnitten_bildpruefung_offen` | 1 / 1 / 1 | 0→0 | 0→0 | 0→0 |
| Prüfe-Regeln / `T3_streifen_ringe_bildpruefung_offen` | 1 / 1 / 1 | 0→0 | 0→0 | 0→0 |
| Prüfe-Regeln / `T4_graue_flussstreifen_bildpruefung_offen` | 1 / 1 / 1 | 0→0 | 0→0 | 0→0 |
| Prüfe-Regeln / `T5_textur_vs_clay_bildpruefung_offen` | 1 / 1 / 1 | 0→0 | 0→0 | 0→0 |
| Prüfe-Regeln / `G7b_wandkontur_rauheit` | 1 / 1 / 1 | 0→0 | 0→0 | 0→0 |
| Prüfe-Regeln / `G7b_wandkontur_kantenschaerfe` | 1 / 1 / 1 | 0→0 | 0→0 | 0→0 |
| Prüfe-Regeln / `G7b_wandkontur_feld` | 25 / 25 / 25 | 1→1 | 0→0 | 0→0 |
| Prüfe-Regeln / `G11_baum_an_wand` | 0 / 0 / 2 | 0→2 | 0→0 | 0→0 |
| R8 / `R8_stufe` | 7 / 7 / 8 | 0→1 | 0→0 | 0→0 |
| R8 / `R8_gitter` | 8 / 8 / 9 | 0→1 | 0→0 | 0→0 |
| R8 / `R8_quer` | 4 / 4 / 5 | 0→1 | 0→0 | 0→0 |
| R8 / `R8a_wegende` | 20 / 20 / 21 | 0→1 | 0→0 | 0→0 |
| R9 / `R8b_delle` | 22 / 22 / 23 | 0→1 | 0→0 | 0→0 |
| R9 / `R9_saegezahn` | 34 / 34 / 34 | 1→1 | 1→1 | 0→0 |
| R9 / `R9w_wellen` | 280 / 280 / 283 | 21→21 | 12→12 | 0→0 |
| **regeln Summe** | **563 / 570 / 565** |  |  |  |
| **R8 Summe** | **39 / 39 / 43** |  |  |  |
| **R9 Summe** | **336 / 336 / 340** |  |  |  |

Adapter-Gesamtsummen: p3d6 `563 / 39 / 336`, p3d8 `570 / 39 / 336`, p3d10 `565 / 43 / 340` (Prüfe-Regeln / R8 / R9). Gegen p3d8 sinken die Prüfe-Regeln um 5, steigen R8 um 4 und R9 um 4. D2 bleibt bei Prüfe-Regeln `R2_getrennt=1`, `T1_fleckrand=7`; R8 und R9 haben in D2 jeweils 0 Treffer. Gegen p3d8 kommen in D2 keine Prüfe-Regel-, R8- oder R9-Treffer hinzu.

Der unveränderte Rohdaten-Prüflauf in diesem Worktree meldete `pruefe_regeln=570`, `r8=48` (Stufe 9, Gitter 10, Quer 5, Wegende 24) und `r9=334` (Delle 25, Sägezahn 34, Wellen 275). Der im Auftrag genannte Roh-Ausgangswert `596` stammt damit nicht aus dem aktuellen Basisstand `origin/art/dorfmap-p3d8 @ 123408b`; deshalb sind die Mesh-Vergleiche oben getrennt über die unveränderten Adapter-Snapshots p3d6/p3d8 ausgewiesen. Prüfer und Schwellen wurden nicht verändert.

### D1-Rampenregeln und Kreuzung

- D1 `R3_laengs_m`: 14 (p3d8) → 6. Ziel ≤6: erreicht.
- D1 `R3_quer_pct`: 9 → 9. Ziel ≤7: verfehlt um 2.
- D1 `R3_woelb_m`: 8 → 7. Ziel ≤7: erreicht.
- Kreuzung `152.5|28.5`: R8-Stufe `1.028 m` (gerundet 1.03), Ziel ≤0.116 m; R8-Gitter `0.037 m`, Ziel ≤0.02 m. R8 zählt D1 je eins für Stufe, Gitter, Quer und Wegende. Die MILP-Ebene ist kein Nachweis für die tatsächliche Meshhöhe an der Kreuzung.
- D1-Endpunkt `156.5|37.5`: R8-Stufe `0.119 m`, Gitter `0.236 m`, Quer `3.7`, R8a-Wegende `0.23 m`. Stufenziel ≤0.20 m ist erreicht; Gitter-/Wegendenverhalten nicht vollständig regressionsfrei.
- D1 R9: `R8b_delle=1` (neu gegenüber p3d8), `R9_saegezahn=1` (gleich), `R9w_wellen=21` (gleich). G1 R9 bleibt Sägezahn 1 / Wellen 12; D2 R9 bleibt 0.
- D1 `G7b_wandkontur_feld=1` bleibt auf dem p3d8-Wert. Die Klippe bei `140|35` bleibt laut Meshmessung bei `7.8840365 m`; R9w in D1 steigt nicht. Dennoch steigen D1 `G11_baum_an_wand` von 0 auf 2 und `G6_facette` von 0 auf 2.

## MILP-Profil und 2D-Übertragung

Der deterministische MILP-Lauf (`scipy.optimize.milp`/HiGHS) verwendete den R3-Gaussoperator des Prüfers und die 4-m-Abschnittseinteilung. Die gemeinsame Ebene um `152.5|28.5` hat Solverhöhe `5.040377 m`, maximale Abweichung `0.01 m` und Neigung `0 %`. Optimale Zielfunktion: 6 verletzte Abschnitte, Summe der absoluten Quellabweichungen `19.411416 m`, maximale Profilabweichung `0.539915 m`. Sechs verletzte Abschnitte sind:

| Rampe | Station von–bis | max. |lr| (m) | Grenzwert (m) |
|---|---:|---:|---:|
| rampe_2 | 20–23.75 | 0.755892 | 0.075 |
| rampe_2 | 44–47.75 | 0.100534 | 0.075 |
| rampe_2 | 48–49 | 0.112508 | 0.075 |
| rampe_11 | 36–39.75 | 0.540205 | 0.075 |
| rampe_11 | 40–43.75 | 0.390811 | 0.075 |
| rampe_11 | 44–47.5 | 0.266251 | 0.075 |

Die Abtastung des tatsächlichen Meshes enthält 388 Stationen, davon 359 in D1. Pflichtabgleich Achse `Mesh−Soll ≤0.02 m` ist **nicht** erfüllt: `rampe_2` hat 6 von 168 D1-Stationen über 0.02 m (Maximum `+0.100040 m` bei s=23.25); `rampe_11` hat 9 von 191 (Maximum `−0.047508 m` bei s=39.5). Einzelstationen stehen vollständig in [`profil_tabelle.csv`](bilder_p3d10/profil_tabelle.csv), mit s, x|z, Quellhöhe, p3d6, p3d8, Soll, Meshhöhe, Differenz und `lr_soll`. Das weist den Transferfehler im Mesh nach, unabhängig von der MILP-Profillösung.

Die beiden experimentellen MILP-Zusätze mit Quer-Faltbindungen (76 bzw. 27 Bindungen) waren infeasible und wurden verworfen; sie sind nicht Teil der endgültigen Variante. Ein lokales Fenster um die Kreuzung wurde nicht als Ersatz eingesetzt.

## Bilder und sichtbare Form

Alle geforderten p3d10-Screenshots liegen unter [`bilder_p3d10/nachher/`](bilder_p3d10/nachher/); die verwendeten Kameras sind gespeichert. Bildzahlen sind Sichtindikatoren und wurden mit den Bildern gegengeprüft.

| Ansicht | p3d6 | p3d8 | p3d10 |
|---|---:|---:|---:|
| D1 / kreuzung / facetten | 351 | 317 | 562 |
| D1 / kreuzung / kantenzaehne | 51 | 36 | 41 |
| D1 / kreuzung / normale_spruenge | 802 | 484 | 585 |
| D1 / kreuzung / normale_sprung_inseln | 117 | 57 | 140 |
| D1 / wandfuss_140_35 / facetten | 535 | 515 | 418 |
| D1 / wandfuss_140_35 / kantenzaehne | 1258 | 1255 | 1467 |
| D1 / wandfuss_140_35 / normale_spruenge | 3322 | 3503 | 3562 |
| D1 / wandfuss_140_35 / normale_sprung_inseln | 333 | 364 | 401 |
| D1 / wegende / facetten | 807 | 825 | 982 |
| D1 / wegende / kantenzaehne | 887 | 866 | 854 |
| D1 / wegende / normale_spruenge | 2137 | 2308 | 1839 |
| D1 / wegende / normale_sprung_inseln | 212 | 220 | 192 |
| D2 / draufsicht / facetten | 0 | 0 | 21 |
| D2 / draufsicht / kantenzaehne | 313 | 313 | 313 |
| D2 / draufsicht / normale_spruenge | 2275 | 2275 | 2275 |
| D2 / draufsicht / normale_sprung_inseln | 9 | 9 | 9 |
| G1 / wandfuss / facetten | 530 | 530 | 530 |
| G1 / wandfuss / kantenzaehne | 911 | 911 | 911 |
| G1 / wandfuss / normale_spruenge | 3393 | 3393 | 3393 |
| G1 / wandfuss / normale_sprung_inseln | 182 | 182 | 182 |

D1-Kreuzung zeigt gegenüber p3d8 deutlich mehr Terrassenfacetten (`317→562`; p3d6 `351`); Streiflicht zeigt die harte Stufe am Bandrand. Ziel Clay-Facetten ≤351 ist verfehlt. G1-Wandfußbild ist bytegleich zu p3d6/p3d8 (SHA256 `6a391991ecdee07c10383399b917bcc04b56efe8dfb85ae311b1510393cc6781`). D2-Meshhöhe ist bytegleich; der gerenderte D2-Draufsicht-Screenshot weicht aber von der Referenz ab: p3d10 SHA256 `558b76f28b8417786eb568b4f5cdf62639154fded1bad330179e40531bf3b8b0`, erwartet `e8db06e608ee2bb6c833c7ca4112a487b5671c5fc2141798c4efd2321350158a`; Differenz betraf 7,955 von 700,000 Pixeln, maximale Kanaldifferenz 25, mittlere absolute Kanaldifferenz 0.0366. Das ist als Bildabweichung offen, nicht als D2-Geometrieänderung ausgegeben.

Vergleichstabellen der fünf Kameras und des Streiflichts: [`delta_p3d6_p3d10.md`](bilder_p3d10/delta_p3d6_p3d10.md), [`delta_p3d8_p3d10.md`](bilder_p3d10/delta_p3d8_p3d10.md), [`delta_var0_p3d10.md`](bilder_p3d10/delta_var0_p3d10.md). Die automatischen Deltas melden p3d6→p3d10 22 Anstiege (3 Prüfe-Regeln, 4 R8, 3 R9, 12 Bildmetriken) und p3d8→p3d10 21 Anstiege (2 Prüfe-Regeln, 4 R8, 3 R9, 12 Bildmetriken). Damit sind die geforderten Null-/nur-Rückgangsbedingungen verfehlt.

## Build und Prüfungen

- Build: `RELIEF_NEU=1 python3 gen_relief.py && RELIEF_NEU=1 python3 baue_html.py`, danach deterministisch mit Standardvariante 10 wiederholt. D1 Höhenhash `2b3655e774fe0cb3035ba3f9967a29c1d8ff91ddda6860e3576663eade6f1b39`; G1 `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb`; D2 `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`.
- LOD1: 134,316 Dreiecke (88,728 Gelände + 45,588 Wände), unter 1.3 Mio. Lochscan/Raycast: 9 Meshes, 88,728 Dreiecke, 0 offene Innenkanten, 0 isolierte Punkte. `t42u`: Summe 0, alle Felder 0. `d2_gb_mesh_bytegleich=true`.
- `pytest -q neu/tests`: 23 bestanden, 8 fehlgeschlagen (p3d8 Referenz 26/5). Fehlgeschlagen: Kreuzungsstufe D1 (1.028 m statt ≤0.20), Wegende allgemein (21), D1-Sägezahnzahl (27), verwaschener Wandfuß (Kantenschärfe 2.24 statt ≥3), Wegende F1/C1 (F1 0.17; C1 kein Treffer), Schattenartefakt (0.307 statt ≤0.25), zwei Terrainmesh-Grenzprüfungen (maximale Quelldifferenz 4.012822 m statt ≤4 m; Maximum bei `128.5|37.5`).
- LOD1-Grenze, D2-Höhenhash, G1-Höhenhash, Klippenwert und t42u bestanden; die R3-Quergrenze, Kreuzungsstufe, Achsabweichung, Regressionsfreiheit, Clay-Facetten und pytest-Referenz sind verfehlt.

## Annahmen, Grenzen und offene Punkte

- Die MILP-Abschnittszahlen beziehen sich auf das Sollprofil auf Rampenpolylinien mit Prüferoperator/Abschnittsstart `j=0,16,32,…`; Meshwerte sind die separate bilineare Abtastung der endgültigen D1-Höhenfläche. Diese Ebenen sind nicht gleichzusetzen.
- Ein exakt ebenes Solverfeld bei der Kreuzung garantiert keine ebene Kreuzung im übertragenen Mesh. Die 1.028-m-R8-Stufe und der misslungene Achsabgleich zeigen die verbleibende 2D-Transfergrenze.
- Keine weiteren Varianten wurden nach der Auswahl von 10 als Standard aufgenommen. Zielwerte trotz drei Varianten nicht erreicht; ein nächster Schritt müsste die Projektion/Profileinbettung im Mesh lösen, ohne Wandfuß, R9w und Bildmetriken zu verschlechtern.
- Ausgabe erzeugt keine Kosten (0 EUR). Es wurden keine Secrets gelesen oder Nachrichten versandt.
