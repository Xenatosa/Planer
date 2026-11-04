# Ergebnis Wellen3

Stand: 04.11.2026 · Worktree `/workspace/wt_dorfmap_wellen3` · Branch `art/dorfmap-wellen3`  
Vergleichsbasis: `e7a5874` (`pruefe_regeln` 570, R8 48, R9 334; Loch 0; t42u 0; LOD1 1.700.454 Dreiecke im Raycast-Scan).

## Ergebnis

**Nicht mergefähig nach dem strengen Kriterium.** Die beste gemessene Variante senkt R9w von 275 auf 249, beseitigt die Wellen2-Anstiege in `R3_laengs_m` und `G5_beule_klippe` und hält D2 bytegleich. Sie verfehlt aber R9w ≤240, erhöht `G6_facette` um 14 und `G3_spitze_unten_fein` um 1. In den Ton-Nahbildern sind bei H3 und E6 außerdem neue, klar sichtbare Formen zu sehen. Kein Merge empfohlen.

Der Gesamtzähler sinkt von 952 auf 935. Die Nettoverbesserung reicht nicht für das Welle-5-Kriterium, weil einzelne Klassen steigen dürfen gar nicht.

## Änderung und Ursachenmessung

`gen_relief.py` glättet weiterhin ausschließlich das abgeleitete Grobnetz `G`; Zellquellwerte, Overlay, Prüfer und Schwellen wurden nicht geändert. Standard ist `GWELLEN=0.12`; schaltbar sind `GWELLEN=0` (aus) und `GWELLEN=0.05`. Der Filter nutzt Sigma 0,75 m, maximal 0,12 m Versatz, einen 2-m-Abstand zu natürlichen Rampen, eine Maske der G5-Kandidatenspur und den bestehenden D2-Schutzbereich. Der Lauf änderte 44.443 G-Ecken; RMS-Versatz über das Feld 0,0112 m.

Die Wellen2-Zunahmen sind überwiegend kleine, getrennte Schwellenkomponenten, nicht eine starke zusammenhängende Welle. Acht R9w-Komponenten ohne Basispaar im 2-m-Abgleich wurden gefunden; ihre Spitzenwerte lagen bei 0,16–0,40 m. Zusammen mit gleichzeitig verschwundenen oder verschmolzenen Komponenten erklären sie die lokalen Zähleränderungen: H2 hatte Komponenten bei 327,5|74,5 und 316,7|85,7; F6 bei 210,1|246,1; D4 bei 156,6|170,5; E5 bei 169,2|184,5; B6 bei 79,2|222,2; D6 bei 128,2|241,0 und 128,9|248,9. Vier Schwerpunkte lagen 1,0–1,8 m von der steilen Wandmaske entfernt; die zwei D6-Schwerpunkte lagen bei 2,12 m. Die D4- und E5-Komponenten lagen weiter von der Wand entfernt. Die bearbeiteten G-Ecken lagen je nach Komponente 0,14–0,71 m von der Komponente entfernt. Das passt zu einer Änderung der Bandpass-Schwelle und der Komponententrennung; eine reine Rampenerklärung trifft nicht auf alle sechs Kacheln zu.

| R9w-Kachel | Basis `e7a5874` | Wellen2 | Wellen3, `GWELLEN=0.12` |
|---|---:|---:|---:|
| H2 | 5 | 6 | 6 |
| F6 | 7 | 8 | 9 |
| D4 | 6 | 7 | 8 |
| E5 | 1 | 2 | 2 |
| B6 | 2 | 3 | 4 |
| D6 | 9 | 11 | 13 |

Der zusätzliche Wellen2-Treffer `R3_laengs_m` lag bei 120,5|178,2 auf `rampe_7` (Wert 0,080 m); der nächste Basistreffer lag bei 118,8|181,8, rund 4,0 m entfernt. Im Wellen2-Rohnetz lag die nächste geänderte G-Ecke 1,02 m vom neuen Treffer. Das bestätigt Empfindlichkeit am Rampenprofil. Der 2-m-Rampenschutz beseitigt den zusätzlichen R3-Treffer in Wellen3.

`G5_beule_klippe` stieg in Wellen2 um drei Komponenten. Die zusätzlichen Schwerpunkte waren F2 224,0|43,0, C3 99,0|102,5 und D4 126,8|143,1. Die Wellen2-Änderung des sichtbaren `GB` lag am Schwerpunkt F2 bei +0,290 m und D4 bei +0,573 m, obwohl die Änderung im Rohnetz an diesen einzelnen Abfragepunkten 0 m betrug; nächste geänderte G-Ecken lagen 1,0–1,2 m entfernt. Das spricht für eine nachgelagerte Wand-/Klippenklassifikation, die auf kleine Nachbaränderungen empfindlich reagiert. Die G5-Kandidatenspur als Sperrmaske bringt die Gesamtklasse in Wellen3 auf den Basiswert 68 zurück.

Die Schutzmasken beheben die R3- und G5-Anstiege, aber nicht die sechs R9w-Kachelzunahmen. Bei H2 ist die Wellen2-Zunahme in Wellen3 weg; F6, D4, B6 und D6 verschlechtern sich gegenüber Wellen2 weiter. Eine stärkere Maximaldämpfung senkt zwar den R9w-Gesamtwert, verursacht aber zusätzliche Facetten und sichtbare Formänderungen.

## Regelklassen vorher/nachher

| Prüfer | Regel | Basis | Wellen3 | Δ |
|---|---|---:|---:|---:|
| regeln | `R1_blind` | 24 | 24 | +0 |
| regeln | `R2_getrennt` | 15 | 15 | +0 |
| regeln | `R3_laengs_m` | 35 | 35 | +0 |
| regeln | `R3_quer_pct` | 23 | 23 | +0 |
| regeln | `R3_woelb_m` | 22 | 22 | +0 |
| regeln | `R5_loch` | 17 | 17 | +0 |
| regeln | `R6_wasser_schnee` | 4 | 4 | +0 |
| regeln | `G2_spitze_oben` | 3 | 3 | +0 |
| regeln | `G3_spitze_unten` | 3 | 3 | +0 |
| regeln | `G2_spitze_oben_fein` | 8 | 7 | -1 |
| regeln | `G3_spitze_unten_fein` | 2 | 3 | +1 |
| regeln | `G5_beule_klippe` | 68 | 68 | +0 |
| regeln | `G6_facette` | 220 | 234 | +14 |
| regeln | `G7_wand_glatte_flaeche` | 1 | 1 | +0 |
| regeln | `G8_fluss_nicht_bis_rand` | 1 | 1 | +0 |
| regeln | `T1_fleckrand` | 94 | 91 | -3 |
| regeln | `T2_textur_abgeschnitten_bildpruefung_offen` | 1 | 1 | +0 |
| regeln | `T3_streifen_ringe_bildpruefung_offen` | 1 | 1 | +0 |
| regeln | `T4_graue_flussstreifen_bildpruefung_offen` | 1 | 1 | +0 |
| regeln | `T5_textur_vs_clay_bildpruefung_offen` | 1 | 1 | +0 |
| regeln | `G7b_wandkontur_rauheit` | 1 | 1 | +0 |
| regeln | `G7b_wandkontur_kantenschaerfe` | 1 | 1 | +0 |
| regeln | `G7b_wandkontur_feld` | 24 | 23 | -1 |
| r8 | `R8_stufe` | 9 | 9 | +0 |
| r8 | `R8_gitter` | 10 | 10 | +0 |
| r8 | `R8_quer` | 5 | 5 | +0 |
| r8 | `R8a_wegende` | 24 | 24 | +0 |
| r9 | `R8b_delle` | 25 | 24 | -1 |
| r9 | `R9_saegezahn` | 34 | 34 | +0 |
| r9 | `R9w_wellen` | 275 | 249 | -26 |

## Kacheln D1, G1 und D2

| Prüfer | Kachel | Treffer Basis→Wellen3 | Regeln Basis→Wellen3 |
|---|---|---:|---|
| regeln | D1 | 36→37 | R1_blind 2→2; R2_getrennt 1→1; R3_laengs_m 6→6; R3_quer_pct 11→11; R3_woelb_m 10→10; G5_beule_klippe 1→1; G6_facette 5→6 |
| r8 | D1 | 8→8 | R8_stufe 2→2; R8_gitter 2→2; R8_quer 1→1; R8a_wegende 3→3 |
| r9 | D1 | 26→25 | R8b_delle 2→2; R9_saegezahn 1→1; R9w_wellen 23→22 |
| regeln | G1 | 13→14 | R1_blind 1→1; R3_laengs_m 1→1; R6_wasser_schnee 3→3; G3_spitze_unten_fein 1→1; G6_facette 4→5; T1_fleckrand 3→3 |
| r8 | G1 | 1→1 | R8a_wegende 1→1 |
| r9 | G1 | 8→8 | R8b_delle 1→1; R9_saegezahn 1→1; R9w_wellen 6→6 |
| regeln | D2 | 8→8 | R2_getrennt 1→1; T1_fleckrand 7→7 |
| r8 | D2 | 0→0 | – |
| r9 | D2 | 0→0 | – |

D2 hat keine neuen Prüfer-Treffer: `pruefe_regeln` bleibt bei 8 (R2: 1, T1: 7), R8 und R9 bleiben bei 0.

## Alle 56 Kacheln

Je Zelle stehen Trefferzahlen `Basis→Wellen3` für `pruefe_regeln`, R8 und R9. Kacheln ohne Treffer sind vollständig aufgeführt.

| Kachel | `pruefe_regeln` | R8 | R9 |
|---|---:|---:|---:|
| A1 | 11→12 | 0→0 | 2→2 |
| B1 | 4→4 | 1→1 | 3→3 |
| C1 | 7→7 | 0→0 | 5→5 |
| D1 | 36→37 | 8→8 | 26→25 |
| E1 | 13→13 | 1→1 | 8→8 |
| F1 | 16→17 | 1→1 | 7→8 |
| G1 | 13→14 | 1→1 | 8→8 |
| H1 | 2→6 | 0→0 | 7→5 |
| A2 | 9→9 | 0→0 | 7→6 |
| B2 | 1→2 | 0→0 | 7→7 |
| C2 | 7→6 | 1→1 | 4→3 |
| D2 | 8→8 | 0→0 | 0→0 |
| E2 | 14→13 | 0→0 | 0→0 |
| F2 | 6→5 | 0→0 | 3→3 |
| G2 | 4→4 | 0→0 | 0→0 |
| H2 | 9→13 | 0→0 | 6→6 |
| A3 | 1→1 | 0→0 | 0→0 |
| B3 | 13→13 | 0→0 | 7→7 |
| C3 | 45→42 | 4→4 | 19→18 |
| D3 | 11→11 | 0→0 | 2→2 |
| E3 | 9→9 | 0→0 | 12→12 |
| F3 | 0→0 | 0→0 | 0→0 |
| G3 | 14→15 | 3→3 | 11→9 |
| H3 | 4→3 | 0→0 | 9→7 |
| A4 | 0→0 | 0→0 | 0→0 |
| B4 | 22→23 | 0→0 | 12→10 |
| C4 | 32→29 | 2→2 | 15→11 |
| D4 | 23→22 | 2→2 | 7→8 |
| E4 | 9→9 | 0→0 | 8→7 |
| F4 | 3→3 | 0→0 | 0→0 |
| G4 | 16→17 | 0→0 | 6→6 |
| H4 | 7→7 | 4→4 | 6→5 |
| A5 | 0→0 | 0→0 | 0→0 |
| B5 | 15→13 | 0→0 | 11→9 |
| C5 | 48→50 | 5→5 | 12→10 |
| D5 | 4→5 | 0→0 | 11→9 |
| E5 | 1→1 | 0→0 | 1→2 |
| F5 | 14→14 | 0→0 | 0→0 |
| G5 | 4→4 | 0→0 | 0→0 |
| H5 | 19→21 | 5→5 | 12→11 |
| A6 | 0→0 | 0→0 | 5→4 |
| B6 | 4→3 | 0→0 | 3→4 |
| C6 | 11→9 | 3→3 | 19→19 |
| D6 | 16→18 | 4→4 | 12→13 |
| E6 | 5→9 | 1→1 | 5→5 |
| F6 | 7→7 | 1→1 | 8→9 |
| G6 | 11→11 | 0→0 | 8→8 |
| H6 | 18→17 | 1→1 | 11→6 |
| A7 | 3→3 | 0→0 | 3→1 |
| B7 | 1→1 | 0→0 | 1→1 |
| C7 | 4→4 | 0→0 | 3→3 |
| D7 | 1→1 | 0→0 | 0→0 |
| E7 | 8→8 | 0→0 | 0→0 |
| F7 | 4→4 | 0→0 | 0→0 |
| G7 | 0→0 | 0→0 | 0→0 |
| H7 | 1→1 | 0→0 | 2→2 |

Insgesamt ändern sich Trefferzahlen in 33 Kacheln: A1, D1, F1, G1, H1, A2, B2, C2, E2, F2, H2, C3, G3, H3, B4, C4, D4, E4, G4, H4, B5, C5, D5, E5, H5, A6, B6, C6, D6, E6, F6, H6, A7.

## Ton-Nahbilder und Sichtprüfung

Render: `?clay=1&lod=0`, 1280×800; für jede geänderte Kachel dieselbe Kamera vorher/nachher. Kameras stehen in [wellen3_cams.json](wellen3_cams.json). Die 33 Vorher-/Nachher-Paare wurden visuell angesehen.

| Kachel | Vorher | Nachher |
|---|---|---|
| A1 | [vorher](bilder_wellen3/vor/A1.png) | [nachher](bilder_wellen3/nach/A1.png) |
| D1 | [vorher](bilder_wellen3/vor/D1.png) | [nachher](bilder_wellen3/nach/D1.png) |
| F1 | [vorher](bilder_wellen3/vor/F1.png) | [nachher](bilder_wellen3/nach/F1.png) |
| G1 | [vorher](bilder_wellen3/vor/G1.png) | [nachher](bilder_wellen3/nach/G1.png) |
| H1 | [vorher](bilder_wellen3/vor/H1.png) | [nachher](bilder_wellen3/nach/H1.png) |
| A2 | [vorher](bilder_wellen3/vor/A2.png) | [nachher](bilder_wellen3/nach/A2.png) |
| B2 | [vorher](bilder_wellen3/vor/B2.png) | [nachher](bilder_wellen3/nach/B2.png) |
| C2 | [vorher](bilder_wellen3/vor/C2.png) | [nachher](bilder_wellen3/nach/C2.png) |
| E2 | [vorher](bilder_wellen3/vor/E2.png) | [nachher](bilder_wellen3/nach/E2.png) |
| F2 | [vorher](bilder_wellen3/vor/F2.png) | [nachher](bilder_wellen3/nach/F2.png) |
| H2 | [vorher](bilder_wellen3/vor/H2.png) | [nachher](bilder_wellen3/nach/H2.png) |
| C3 | [vorher](bilder_wellen3/vor/C3.png) | [nachher](bilder_wellen3/nach/C3.png) |
| G3 | [vorher](bilder_wellen3/vor/G3.png) | [nachher](bilder_wellen3/nach/G3.png) |
| H3 | [vorher](bilder_wellen3/vor/H3.png) | [nachher](bilder_wellen3/nach/H3.png) |
| B4 | [vorher](bilder_wellen3/vor/B4.png) | [nachher](bilder_wellen3/nach/B4.png) |
| C4 | [vorher](bilder_wellen3/vor/C4.png) | [nachher](bilder_wellen3/nach/C4.png) |
| D4 | [vorher](bilder_wellen3/vor/D4.png) | [nachher](bilder_wellen3/nach/D4.png) |
| E4 | [vorher](bilder_wellen3/vor/E4.png) | [nachher](bilder_wellen3/nach/E4.png) |
| G4 | [vorher](bilder_wellen3/vor/G4.png) | [nachher](bilder_wellen3/nach/G4.png) |
| H4 | [vorher](bilder_wellen3/vor/H4.png) | [nachher](bilder_wellen3/nach/H4.png) |
| B5 | [vorher](bilder_wellen3/vor/B5.png) | [nachher](bilder_wellen3/nach/B5.png) |
| C5 | [vorher](bilder_wellen3/vor/C5.png) | [nachher](bilder_wellen3/nach/C5.png) |
| D5 | [vorher](bilder_wellen3/vor/D5.png) | [nachher](bilder_wellen3/nach/D5.png) |
| E5 | [vorher](bilder_wellen3/vor/E5.png) | [nachher](bilder_wellen3/nach/E5.png) |
| H5 | [vorher](bilder_wellen3/vor/H5.png) | [nachher](bilder_wellen3/nach/H5.png) |
| A6 | [vorher](bilder_wellen3/vor/A6.png) | [nachher](bilder_wellen3/nach/A6.png) |
| B6 | [vorher](bilder_wellen3/vor/B6.png) | [nachher](bilder_wellen3/nach/B6.png) |
| C6 | [vorher](bilder_wellen3/vor/C6.png) | [nachher](bilder_wellen3/nach/C6.png) |
| D6 | [vorher](bilder_wellen3/vor/D6.png) | [nachher](bilder_wellen3/nach/D6.png) |
| E6 | [vorher](bilder_wellen3/vor/E6.png) | [nachher](bilder_wellen3/nach/E6.png) |
| F6 | [vorher](bilder_wellen3/vor/F6.png) | [nachher](bilder_wellen3/nach/F6.png) |
| H6 | [vorher](bilder_wellen3/vor/H6.png) | [nachher](bilder_wellen3/nach/H6.png) |
| A7 | [vorher](bilder_wellen3/vor/A7.png) | [nachher](bilder_wellen3/nach/A7.png) |

Sichtbare Befunde, jeweils am Kameraziel `x|z`:

- **H3, 303,12|96,44:** Nachher erscheint eine große steile Wandfläche, wo vorher eine deutlich niedrigere, gerundete Rückenform lag. Neue sichtbare Kante/Flanke; klarer Ausschlussgrund.
- **E6, 199,20|237,95:** Nachher hat der Rücken eine neue gezackte, stufenartige Kontur. Klarer Ausschlussgrund.
- **A1, 27,00|32,93:** Nachher erscheint ein stärker ausgeprägter runder Buckel mit sichtbarer Schulter.
- **F1, 230,60|29,20:** Die Rücken-/Wandkante wirkt nachher deutlich unruhiger und stärker gezahnt.

Die übrigen Ansichten zeigen überwiegend kleine Formverschiebungen ohne klar neue Risse. Das ändert die Ausschlussbefunde in H3 und E6 nicht.

## Gates und D2-Regression

| Prüfung | Ergebnis |
|---|---|
| `python3 gen_relief.py && python3 baue_html.py` mit `GWELLEN=0.12` | erfolgreich |
| Lochscan (`RAND=0.6`) | `offen_innen=0`, `punkte=0`; 1.698.750 Dreiecke im Raycast-Scan |
| `pruefe_regeln.py` | 580 Treffer; Basis 570; strikt nicht bestanden |
| `r8_kreuzung.py` | 48; Basis 48 |
| `r9_form.py` | 307; Basis 334; R9w 249 statt 275 |
| `pruefe_t42u.py` | Summe 0; keine Abweichungen |
| LOD1 `test_dreiecke_l1.js` | 1.173.147 gerenderte Dreiecke; unter 1,3 Mio. |
| D2 `G`, `GB`, Feinband und CSV-Zeilen | bytegleich |

D2-SHA-256: `G` `325f6fe2f41178f7e9c4b2198881438bc5ac70649ac4a0ee9836b463e6e1408c`; `GB` `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`; 17 Feinbandpunkte samt Höhen gleich (SHA-256 IDs+Höhen `6bcf7ea4440fc0db34582eb436d724a6e321eb41e23d8c8ef2ab404244084a14`); 1.806 D2-CSV-Zeilen bytegleich (SHA-256 `1ceca847caeab1e6a4a2d2ab95fd27f88a214e98adadc13ffad3610e948cec7a`).

## Annahmen, Grenzen und offene Punkte

- Verglichen wird der committed Ergebnisstand `e7a5874`, nicht nur der ältere Stand aus dem Wellen2-Arbeitsbericht.
- R9w-Messorte sind Schwerpunkte zusammenhängender Komponenten; sie müssen nicht selbst auf einem geänderten G-Eckpunkt liegen. Abstände zu geänderten G-Ecken wurden auf den Komponentenflächen gemessen.
- Die Wellen3-Schutzmasken sichern die beobachteten Rampen- und G5-Fälle in diesem Build, lösen aber die R9w-Zunahmen in vier der sechs genannten Kacheln nicht. R9w 249 liegt neun über dem Ziel.
- G6 steigt um 14 und G3-Spitze-fein um 1; die sichtbaren H3-/E6-Änderungen verletzen ebenfalls das Merge-Kriterium. Es ist daher kein mergefähiges Ergebnis.
- Die T2–T5-Bildprüfungsmarker bleiben wie in der Basis je 1 offen; ihre Prüfschwellen wurden nicht geändert.
- Zellquellwerte, Overlay, Referenzverzeichnis und Prüfer/Schwellen blieben unverändert. Kosten: 0 EUR.
