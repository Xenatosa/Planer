# Ergebnis L2

Stand: 16.11.2026 · Basis `[S] cc2a02b` · Branch `art/dorfmap-L2`

## Ergebnis

`[S]` **Ziel nicht erreicht.** Keine der 23 QA-Stellen ist im Nahbild sichtbar besser geworden. Die gate-sichere Standardvariante 2 verändert `GB` lokal um höchstens **0,0396 m**; bei allen Bildpaaren blieb die Zahl der Pixel mit mehr als 2 RGB-Stufen Abweichung bei 0 %. Der stärkere Kandidat wurde verworfen, weil er Gates verschlechterte. Der Bericht hält alle 23 offenen Stellen fest.

## Methode

`[S]` Neu: `relief_l2.py` und `pruefung/l2_stellen.json`. Ein kleiner Hook in `gen_relief.py` führt die Korrektur nach den üblichen Höhenoperationen aus. `RELIEF_L2=0` schaltet sie ab; der ausgeschaltete Build ist bytegleich zum Ausgangs-Relief (`5e8fdb51c3f3dff9ad2c03c32c7a39ee1a4f97a3bc0942d47a352b1d0b4f0e88`). Standard ist `RELIEF_L2=1`, Variante 2. `baue_html.py` respektiert `BUNDLE_OUT`, damit der vorgeschriebene Build `/tmp/w3/bundle_r.js` unberührt lässt.

`[S]` Die Standardmethode ist eine lokale symmetrische 1D-Mittelung entlang der angegebenen Linienachse mit 3 m Auslauf. Der Feldquellwert `G` bleibt bytegleich; nur das sichtbare Höhenfeld `GB` wird bearbeitet. Wand-/Klippenflächen, Straßen und Rampen plus 2,5 m, Wasser plus 2 m, Bauflächen sowie D2 werden ausgespart. Zusätzlich gibt es 1,5 m weichen Schutzabstand zu festen Bändern. Stellen liegen in Weltkoordinaten und sind deshalb nach einem P2-Merge neu anwendbar.

`[R]` Variante 1 (Median) verursachte in einem Versuch 40 offene Innenkanten und einen neuen G1-Lochtreffer; sie wurde verworfen. Variante 3 ohne das breite Renderband verursachte 44 offene Innenkanten, `pruefe_regeln` 571 statt 570 und `r9` 335 statt 334; ebenfalls verworfen. Bei Standardvariante 2 blieben die Gates unverändert, aber die Änderungen waren optisch zu klein. Stelle 19 ist im Standard zusätzlich mit Korrekturgrenze 0 m deaktiviert.

## 23 Stellen und Nahbilder

`[S]` Alle Paare zeigen dieselbe Kamera (Hauptviewer, Clay, 800×600). Die Messwerte stehen zusätzlich in [`l2_nahbild_messwerte.json`](l2_nahbild_messwerte.json). **Unverändert** bedeutet, dass die Form im Nahbild gleich erscheint.

| ID | Kachel | Koordinate x\|z (m) | Muster | Max. Korrektur GB (m) | Urteil | Bilder |
|---:|---|---|---|---:|---|---|
| 01 | C3 | 94\|97 | Saegezahn-Ring am Mulden-/Kraterrand | 0.0007 | **unveraendert** | [vorher](l2_nahbilder/01_C3_ring_vorher.jpg) / [nachher](l2_nahbilder/01_C3_ring_nachher.jpg) |
| 02 | C3 | 105-112\|112-118 | Saegezahn-Kamm auf Grat | 0.0000 | **unveraendert** | [vorher](l2_nahbilder/02_C3_gratkamm_vorher.jpg) / [nachher](l2_nahbilder/02_C3_gratkamm_nachher.jpg) |
| 03 | D1 | 145-158\|15-30 | Treppen- und Rippenrillen am Hang | 0.0000 | **unveraendert** | [vorher](l2_nahbilder/03_D1_rillen_vorher.jpg) / [nachher](l2_nahbilder/03_D1_rillen_nachher.jpg) |
| 04 | C3 | 114.8\|120.7 | Kamm auf linkem Grat | 0.0000 | **unveraendert** | [vorher](l2_nahbilder/04_C3_linker_grat_vorher.jpg) / [nachher](l2_nahbilder/04_C3_linker_grat_nachher.jpg) |
| 05 | D4 | 135\|139 | Zahnkante am Blockrand | 0.0009 | **unveraendert** | [vorher](l2_nahbilder/05_D4_zahnkante_vorher.jpg) / [nachher](l2_nahbilder/05_D4_zahnkante_nachher.jpg) |
| 06 | C4 | 112-121\|158-168 | Saegezahn auf kleinem Simsgrat | 0.0001 | **unveraendert** | [vorher](l2_nahbilder/06_C4_simsgrat_vorher.jpg) / [nachher](l2_nahbilder/06_C4_simsgrat_nachher.jpg) |
| 07 | D6 | 150-160\|226-229 | Trapeztafeln am Wandfuss | 0.0000 | **unveraendert** | [vorher](l2_nahbilder/07_D6_tafeln_vorher.jpg) / [nachher](l2_nahbilder/07_D6_tafeln_nachher.jpg) |
| 08 | B4 | 74-78\|145-149 | Zahnreihe an kleiner Stufe | 0.0000 | **unveraendert** | [vorher](l2_nahbilder/08_B4_zahnreihe_vorher.jpg) / [nachher](l2_nahbilder/08_B4_zahnreihe_nachher.jpg) |
| 09 | C5 | 104-112\|180-184 | Saegezahn-Kamm in Rinnen-/Gratlinie | 0.0000 | **unveraendert** | [vorher](l2_nahbilder/09_C5_kamm_vorher.jpg) / [nachher](l2_nahbilder/09_C5_kamm_nachher.jpg) |
| 10 | E7/F7 | 199-216\|273-276 | Gerade Stufenlinie im Flussbett | 0.0000 | **unveraendert** | [vorher](l2_nahbilder/10_E7_F7_stufen_vorher.jpg) / [nachher](l2_nahbilder/10_E7_F7_stufen_nachher.jpg) |
| 11 | C4/C5 | 84-95\|168-176 | Gezackte Gratkante | 0.0000 | **unveraendert** | [vorher](l2_nahbilder/11_C4_C5_gratkante_vorher.jpg) / [nachher](l2_nahbilder/11_C4_C5_gratkante_nachher.jpg) |
| 12 | D6 | 133-138\|231-236 | Saegezahnlinie am Hangrand | 0.0000 | **unveraendert** | [vorher](l2_nahbilder/12_D6_hangrand_vorher.jpg) / [nachher](l2_nahbilder/12_D6_hangrand_nachher.jpg) |
| 13 | G4 | 274\|133; 281\|139 | Kissenbloecke, Zickzack am Fuss | 0.0000 | **unveraendert** | [vorher](l2_nahbilder/13_G4_kissen_vorher.jpg) / [nachher](l2_nahbilder/13_G4_kissen_nachher.jpg) |
| 14 | E1 | 181\|20 | Splitter an Klippenecke | 0.0000 | **unveraendert** | [vorher](l2_nahbilder/14_E1_splitter_vorher.jpg) / [nachher](l2_nahbilder/14_E1_splitter_nachher.jpg) |
| 15 | C6 | 97\|221 | Trichter/Mulde am Wandfuss | 0.0000 | **unveraendert** | [vorher](l2_nahbilder/15_C6_trichter_vorher.jpg) / [nachher](l2_nahbilder/15_C6_trichter_nachher.jpg) |
| 16 | H6 | 315\|226 | Kammzaehne auf Wandkrone | 0.0001 | **unveraendert** | [vorher](l2_nahbilder/16_H6_kammkrone_vorher.jpg) / [nachher](l2_nahbilder/16_H6_kammkrone_nachher.jpg) |
| 17 | H3 | 316\|90 | Knubbel am Terrassenrand | 0.0000 | **unveraendert** | [vorher](l2_nahbilder/17_H3_terrassenrand_vorher.jpg) / [nachher](l2_nahbilder/17_H3_terrassenrand_nachher.jpg) |
| 18 | H2 | 322-330\|65-69 | Kammzaehne auf Grat und Randspitze | 0.0263 | **unveraendert** | [vorher](l2_nahbilder/18_H2_gratkamm_vorher.jpg) / [nachher](l2_nahbilder/18_H2_gratkamm_nachher.jpg) |
| 19 | G3 | 285\|108 | Spitzen/Knick am Ruecken | 0.0000 | **unveraendert** | [vorher](l2_nahbilder/19_G3_ruecken_vorher.jpg) / [nachher](l2_nahbilder/19_G3_ruecken_nachher.jpg) |
| 20 | E2 | 200\|55-60 | Zickzack an Bachuferkante | 0.0396 | **unveraendert** | [vorher](l2_nahbilder/20_E2_uferkante_vorher.jpg) / [nachher](l2_nahbilder/20_E2_uferkante_nachher.jpg) |
| 21 | F6 | Wandkrone; Naeherung 215\|224 | Kamm auf Wandkrone | 0.0000 | **unveraendert** | [vorher](l2_nahbilder/21_F6_kronenkamm_vorher.jpg) / [nachher](l2_nahbilder/21_F6_kronenkamm_nachher.jpg) |
| 22 | F1 | Wandkrone; Naeherung 212\|18 | Kamm auf Wandkrone | 0.0000 | **unveraendert** | [vorher](l2_nahbilder/22_F1_kronenkamm_vorher.jpg) / [nachher](l2_nahbilder/22_F1_kronenkamm_nachher.jpg) |
| 23 | G6 | 283\|226 | Kerbe/Kammkante an Krone | 0.0002 | **unveraendert** | [vorher](l2_nahbilder/23_G6_kerbe_vorher.jpg) / [nachher](l2_nahbilder/23_G6_kerbe_nachher.jpg) |

## Gates

`[S]` Ausgangszahlen laut Auftrag und endgültiger Nachher-Lauf:

### Prüfregeln

| Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| `G2_spitze_oben` | 3 | 3 | +0 |
| `G2_spitze_oben_fein` | 8 | 8 | +0 |
| `G3_spitze_unten` | 3 | 3 | +0 |
| `G3_spitze_unten_fein` | 2 | 2 | +0 |
| `G5_beule_klippe` | 68 | 68 | +0 |
| `G6_facette` | 220 | 220 | +0 |
| `G7_wand_glatte_flaeche` | 1 | 1 | +0 |
| `G7b_wandkontur_feld` | 24 | 24 | +0 |
| `G7b_wandkontur_kantenschaerfe` | 1 | 1 | +0 |
| `G7b_wandkontur_rauheit` | 1 | 1 | +0 |
| `G8_fluss_nicht_bis_rand` | 1 | 1 | +0 |
| `R1_blind` | 24 | 24 | +0 |
| `R2_getrennt` | 15 | 15 | +0 |
| `R3_laengs_m` | 35 | 35 | +0 |
| `R3_quer_pct` | 23 | 23 | +0 |
| `R3_woelb_m` | 22 | 22 | +0 |
| `R5_loch` | 17 | 17 | +0 |
| `R6_wasser_schnee` | 4 | 4 | +0 |
| `T1_fleckrand` | 94 | 94 | +0 |
| `T2_textur_abgeschnitten_bildpruefung_offen` | 1 | 1 | +0 |
| `T3_streifen_ringe_bildpruefung_offen` | 1 | 1 | +0 |
| `T4_graue_flussstreifen_bildpruefung_offen` | 1 | 1 | +0 |
| `T5_textur_vs_clay_bildpruefung_offen` | 1 | 1 | +0 |
| **Summe** | **570** | **570** | **+0** |

### R8 Kreuzungen

| Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| `R8_gitter` | 10 | 10 | +0 |
| `R8_quer` | 5 | 5 | +0 |
| `R8_stufe` | 9 | 9 | +0 |
| `R8a_wegende` | 24 | 24 | +0 |
| **Summe** | **48** | **48** | **+0** |

### R9 Form

| Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| `R8b_delle` | 25 | 25 | +0 |
| `R9_saegezahn` | 34 | 34 | +0 |
| `R9w_wellen` | 275 | 275 | +0 |
| **Summe** | **334** | **334** | **+0** |

`[S]` Die vollständigen Regeln × Kacheln (A1–H7), inklusive D1/G1/D2, stehen in [`L2_gate_vorher_nachher.json`](L2_gate_vorher_nachher.json). Die drei offiziellen Trefferlisten sind vor/nachher identisch. D2: Prüfregeln 8 → 8, R8 0 → 0, R9 0 → 0; keine neuen D2-Treffer.

### D1, G1 und D2

| Prüfer | Kachel | Vorher → Nachher | Aufteilung vorher / nachher |
|---|---|---:|---|
| Prüfregeln | D1 | 36 → 36 | G5_beule_klippe 1, G6_facette 5, R1_blind 2, R2_getrennt 1, R3_laengs_m 6, R3_quer_pct 11, R3_woelb_m 10 / G5_beule_klippe 1, G6_facette 5, R1_blind 2, R2_getrennt 1, R3_laengs_m 6, R3_quer_pct 11, R3_woelb_m 10 |
| Prüfregeln | G1 | 13 → 13 | G3_spitze_unten_fein 1, G6_facette 4, R1_blind 1, R3_laengs_m 1, R6_wasser_schnee 3, T1_fleckrand 3 / G3_spitze_unten_fein 1, G6_facette 4, R1_blind 1, R3_laengs_m 1, R6_wasser_schnee 3, T1_fleckrand 3 |
| Prüfregeln | D2 | 8 → 8 | R2_getrennt 1, T1_fleckrand 7 / R2_getrennt 1, T1_fleckrand 7 |
| R8 | D1 | 8 → 8 | R8_gitter 2, R8_quer 1, R8_stufe 2, R8a_wegende 3 / R8_gitter 2, R8_quer 1, R8_stufe 2, R8a_wegende 3 |
| R8 | G1 | 1 → 1 | R8a_wegende 1 / R8a_wegende 1 |
| R8 | D2 | 0 → 0 | — / — |
| R9 | D1 | 26 → 26 | R8b_delle 2, R9_saegezahn 1, R9w_wellen 23 / R8b_delle 2, R9_saegezahn 1, R9w_wellen 23 |
| R9 | G1 | 8 → 8 | R8b_delle 1, R9_saegezahn 1, R9w_wellen 6 / R8b_delle 1, R9_saegezahn 1, R9w_wellen 6 |
| R9 | D2 | 0 → 0 | — / — |

`[S]` Hauptviewer-Lochscan: 7 Meshes, 1.700.454 Dreiecke, 0 offene Innenkanten. Scan aller 56 Kacheln: 0 vorher und nachher; C3-Positivkontrolle findet 3 offene Kanten. Das All-Kachel-Mesh hat 809.088 Terrain- und 45.588 Wanddreiecke, zusammen 854.676. Die 97 Kachelnahtpaare sind exakt (maximale Nahtabweichung 0 m). `t42u`-Summe: **0**.

`[S]` D2-Höhenfeld `G` und `GB`, Form 87×85, ist bitgleich. `GB`-SHA-256 vorher/nachher: `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`. Das globale Quellfeld `G` blieb ebenfalls bytegleich (SHA-256 `056b84f4f57045a905cdb7676b4dec94b71552c5c34e7c0c484c2155011965ff` vorher/nachher); globales `GB` ändert sich nur durch L2. Das geschützte `neu/build.json` meldet für seinen LOD1-Paketstand 134.316 von 1.300.000 Dreiecken (unter dem Limit). Geschützte Eingabedateien blieben unverändert: `neu/zellen_relief.csv` `99d30e55…`, `neu/vektor.json` `aac6afff…`, `neu/felder.json` `e4e2ec8f…`.

`[S]` Trefferkartenvergleich: [`vergleich.png`](trefferkarte/l2/vergleich.png), [`vergleich.html`](trefferkarte/l2/vergleich.html), Zahlen [`trefferkarte.json`](trefferkarte/l2/trefferkarte.json). Ergebnis: alle Zellfamilien haben Δ=0.

## Annahmen, Grenzen und offene Punkte

- `[A]` Die sichtbaren Fehler sollen trotz unveränderter Grundrisse, Wege, Wasser- und Klippenkonturen entfernt werden. Da die Schutzmasken den größten Teil der Zielstellen überdecken, war der verfügbare Korrekturraum klein.
- `[S]` Der 56-Kachel-P10-Build verwendete `RELIEF_KREUZUNG_VAR=0`, weil die gespeicherte p3d17-Lösung den SHA des Reliefs vor L2 erwartet. Der Hauptviewer-Gate wurde mit seinem normalen Build geprüft. Die Kachelprototypen D1/G1 im Zusatzscan verwenden daher nicht die Standard-Kreuzungsvariante; dies ist eine Grenze des Zusatzscans.
- `[A]` Nach dem Merge des parallelen P2-Branches sind `python3 gen_relief.py`, `python3 baue_html.py`, Haupt-Gates, `t42u` und der 56-Kachel-Lochscan erneut auszuführen. Weltkoordinatenmasken brauchen keine Indexanpassung; durch P2 geänderte Wege/Rampen verändern jedoch die Schutzmasken.
- `[R]` Ring C3, Gratkamm C3, Rillen D1, Kamm C3 bei 114,8|120,7, Zahnkante D4 und alle weiteren QA-Punkte bleiben sichtbar bzw. unverändert. Für eine echte optische Korrektur braucht es einen genehmigten Weg, mindestens einzelne Schutzbänder zu lockern oder andere Geometrieparameter zu ändern.
