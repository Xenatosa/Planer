# Ergebnis p3d2

**Branch:** `art/dorfmap-p3d2` · **Basis:** `576080b` · **Standard:** `RELIEF_NEU=1`, `RELIEF_GELAENDE_VAR=2`

**Modell/Reasoning effort:** `gpt-6-luna / xhigh` · **Kosten:** 0 EUR

## Ergebnis

Das neue sichtbare Mesh ist wirksam: die D1-Kreuzungsstufe am R8-Punkt sinkt von **1,746 m auf 0,087 m**. Die D1/G1-R8a-Summen sinken von **0,59 m auf 0,56 m**. Der Lauf erfüllt die Gesamtziele **nicht**: im Neu-Mesh-Clay-Delta steigen 21 Bildmetriken und 5 Regel/Kachelwerte; D1 hat weiter 49 R9-Sägezahnelemente, R9w steigt global um 4. Keine Schwelle wurde gelockert.

## Ursache-Fix-Tabelle

| Belegte Ursache | Umsetzung in p3d2 | Ergebnis / Grenze |
|---|---|---|
| `neu/mesh.py` multiplizierte nach den Profilen das Gewicht mit `0.02`; die Höhenänderung blieb pixelklein. | Den pauschalen Faktor entfernt. Variante 2 baut lokale Rampenprofile und gemeinsame Ebenen an erkannten Rampenkreuzungen. | D1 max. abs(Δ) 3,311 m, G1 0,243 m. D2 0,000 m. |
| Legacy-Gates lasen `G/GB` statt `neu_mesh_tiles`. | `pruefung/neu_mesh_adapter.py` überträgt die sichtbaren D1/G1-Meshhöhen in unveränderte Gate-Eingabefelder `G`, `GB` und bilinear in passende `FW`-Stützstellen. Die Gate-Skripte und Schwellen bleiben unverändert. Die Tests laden den Kandidaten aus `neu/relief_neu.json.gz`. | Die Zahlen unten vergleichen Neu-Mesh Variante 0 mit dem gebauten Neu-Mesh Variante 2; die unveränderten Legacy-Zahlen werden getrennt ausgewiesen. |
| Wand-Abstandsschutz und Kachelrand-Fade hielten Profile von Wandfüßen fern. | Rampen-/Kreuzungsgewichte dürfen im Wandfußbereich anbinden; der 3-m-Kachelrand-Fade bleibt. Ein lokaler 1-m-Schutzring erhält die D1-Klippenform bei (140,35). | Der Höhenwert bei D1 (140,35) bleibt exakt 7,884 m. G1/D1-Wandanschlüsse haben Sichtbilder, aber noch keine eigene numerische Nahtschwelle. G7b steigt um 1; R9w steigt um 4. |
| Die volle Variante 1 hatte Clay-Anstiege; globales Minimalgewicht war nachweislich ungeeignet. | Variante 2 ist die Standardvariante: Endprofile nur in Rampen-Endzonen, σ=4 m, Halbbreite 1,8 m, Auslauf 8 m; Kreuzungsrand 4,5–9,5 m. Variante 1 bleibt über `RELIEF_GELAENDE_VAR=1` schaltbar; Variante 0 ist die Kontrolle. | Variante 2 besteht das Clay-Delta weiterhin nicht: 21 Bildmetriken und 5 Regel/Kachelwerte steigen. |

## Build und Mesh-Baseline

Der Legacy-Standardpfad ohne Selector erzeugt nicht den gewünschten Viewer. Für den freizugebenden Build wurde der vorhandene Selector verwendet:

```sh
RELIEF_NEU=1 python3 gen_relief.py
RELIEF_NEU=1 python3 baue_html.py
```

Der erzeugte `index.html` enthält `RELIEF_NEU_VIEWER=1`. Der vorgeschriebene Lochscan auf diesem Einstieg meldet **9 Terrainmeshes, 88.728 Dreiecke, 0 offene Innenkanten**. LOD1 hat **168.600 Dreiecke** bei 0,5-m-Abtastung (Limit 1,3 Mio.).

| Kachel | Variante-0 max. abs(Δ) zu GB | Variante-2 max. abs(Δ) zu GB | mittlere abs(Δ) | geänderte Vertices (>0,00001 m) | Höhen-SHA-256 |
|---|---:|---:|---:|---:|---|
| D1 | 0,000 m | 3,311102 m | 0,061450 m | 1.487 | `6293d3b0d9a73438f66aad2d6e04fb2b2377f497ba866a8fcd9827cb94d8d899` |
| G1 | 0,000 m | 0,242815 m | 0,002408 m | 567 | `4c72cac22813f8c388489377364627dc598e3d7f6d7eca7f38aef565eedc8ca4` |
| D2 | 0,000 m | 0,000000 m | 0,000000 m | 0 | `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6` |

D2 wurde für die Meshkachel gegen das sichtbare GB-Feld byteweise geprüft. Der Adaptertest prüft außerdem die D2-Slices von `G`, `GB` und `FW` auf Bytegleichheit. Der D1-Kontrollpunkt (140,35) ist im Quellfeld und im erzeugten Mesh bytegleich.

### Vorgeschriebene Legacy-Gates auf dem Branch-Quellfeld

| Aufruf | Ergebnis |
|---|---|
| Lochscan mit Neu-Viewer | 0 offene Innenkanten |
| `pruefe_regeln.py relief_daten.json.gz` | 570 Treffer, Exit 1 |
| `r8_kreuzung.py relief_daten.json.gz` | 48 (Stufe 9, Gitter 10, Quer 5, Wegende 24), Exit 1 |
| `r9_form.py relief_daten.json.gz` | 334 (Delle 25, Sägezahn 34, Wellen 275), Exit 1 |

Der angegebene Vergleichswert für `pruefe_regeln` (596 am Stand `9d3f8fc`) ließ sich auf der verlangten Basis `576080b` nicht reproduzieren; die lokale Quellenmessung ergab 570. R8=48 und R9=334 entsprechen den genannten Ausgangszahlen. Diese unveränderten GB-Zahlen sind **kein** Beleg für das neue Mesh.

## Neu-Mesh-Gates: Variante 0 → gebaute Variante 2

Die folgenden unveränderten Prüfskripte liefen auf Adapterkopien, in denen D1/G1 aus dem Mesh und D2 unverändert sind. `pruefe_regeln` erhielt denselben Lochscan. D2-Zahlen sind vor/nach identisch; kein neuer D2-Treffer kam hinzu.

### `pruefe_regeln`

| Regel | Gesamt vorher → nachher (Δ) | D1 | G1 | D2 |
|---|---:|---:|---:|---:|
| G11_objekt_schwebt_sinkt | 4 → 4 (+0) | 2 → 2 | 2 → 2 | 0 → 0 |
| G2_spitze_oben | 3 → 3 (+0) | 0 → 0 | 0 → 0 | 0 → 0 |
| G2_spitze_oben_fein | 8 → 8 (+0) | 0 → 0 | 0 → 0 | 0 → 0 |
| G3_spitze_unten | 3 → 3 (+0) | 0 → 0 | 0 → 0 | 0 → 0 |
| G3_spitze_unten_fein | 1 → 1 (+0) | 0 → 0 | 0 → 0 | 0 → 0 |
| G5_beule_klippe | 68 → 67 (-1) | 1 → 0 | 0 → 0 | 0 → 0 |
| G6_facette | 216 → 215 (-1) | 1 → 0 | 2 → 2 | 0 → 0 |
| G7_wand_glatte_flaeche | 1 → 1 (+0) | 0 → 0 | 0 → 0 | 0 → 0 |
| G7b_wandkontur_feld | 24 → 25 (+1) | 0 → 1 | 0 → 0 | 0 → 0 |
| G7b_wandkontur_kantenschaerfe | 1 → 1 (+0) | 0 → 0 | 0 → 0 | 0 → 0 |
| G7b_wandkontur_rauheit | 1 → 1 (+0) | 0 → 0 | 0 → 0 | 0 → 0 |
| G8_fluss_nicht_bis_rand | 1 → 1 (+0) | 0 → 0 | 0 → 0 | 0 → 0 |
| R1_blind | 24 → 24 (+0) | 2 → 2 | 1 → 1 | 0 → 0 |
| R2_getrennt | 15 → 15 (+0) | 1 → 1 | 0 → 0 | 1 → 1 |
| R3_laengs_m | 35 → 40 (+5) | 6 → 11 | 1 → 1 | 0 → 0 |
| R3_quer_pct | 23 → 19 (-4) | 11 → 7 | 0 → 0 | 0 → 0 |
| R3_woelb_m | 22 → 21 (-1) | 10 → 9 | 0 → 0 | 0 → 0 |
| R5_loch | 17 → 17 (+0) | 0 → 0 | 0 → 0 | 0 → 0 |
| R6_wasser_schnee | 4 → 4 (+0) | 0 → 0 | 3 → 3 | 0 → 0 |
| T1_fleckrand | 94 → 94 (+0) | 0 → 0 | 3 → 3 | 7 → 7 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 → 1 (+0) | 0 → 0 | 0 → 0 | 0 → 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 → 1 (+0) | 0 → 0 | 0 → 0 | 0 → 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 → 1 (+0) | 0 → 0 | 0 → 0 | 0 → 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 → 1 (+0) | 0 → 0 | 0 → 0 | 0 → 0 |
| **Summe** | **569 → 568 (-1)** | — | — | — |

Größte Regelzunahme ist `R3_laengs_m` mit +5 (35→40); `G7b_wandkontur_feld` steigt um 1. Alle übrigen Regel-Deltas liegen zwischen −4 und 0.

### `r8_kreuzung.py`

| Regel | Gesamt vorher → nachher (Δ) | D1 | G1 | D2 |
|---|---:|---:|---:|---:|
| R8_gitter | 9 → 8 (-1) | 1 → 0 | 0 → 0 | 0 → 0 |
| R8_quer | 5 → 4 (-1) | 1 → 0 | 0 → 0 | 0 → 0 |
| R8_stufe | 8 → 8 (+0) | 1 → 1 | 0 → 0 | 0 → 0 |
| R8a_wegende | 23 → 23 (+0) | 2 → 2 | 1 → 1 | 0 → 0 |
| **Summe** | **45 → 43 (-2)** | **5 → 3** | **1 → 1** | **0 → 0** |

D1 `rampe_2x11` bei (152,5; 28,5): Stufe **1,746→0,087 m**, Gitter **2,353→0,000 m**. G1 `rampe_1_anfang` bei (273,4; 21,2): Stufe **0,046→0,044 m**. R8a D1/G1-Hits bleiben 3; ihre Wertsumme sinkt **0,59→0,56 m**. Offener Randfall: D1 `rampe_11_ende` hat nach Variante 2 eine Stufe von **0,299 m** (vorher 0,064 m).

### `r9_form.py`

| Regel | Gesamt vorher → nachher (Δ) | D1 | G1 | D2 |
|---|---:|---:|---:|---:|
| R8b_delle | 23 → 22 (-1) | 1 → 0 | 0 → 0 | 0 → 0 |
| R9_saegezahn | 34 → 34 (+0) | 1 → 1 | 1 → 1 | 0 → 0 |
| R9w_wellen | 281 → 285 (+4) | 21 → 23 | 13 → 14 | 0 → 0 |
| **Summe** | **338 → 341 (+3)** | **23 → 24** | **14 → 15** | **0 → 0** |

Der D1-Sägezahn bleibt als Treffer bestehen (Wert 49; Ziel 0). `R9w_wellen` steigt um 4 global (281→285), darunter D1 +2 und G1 +1. D2 bleibt trefferfrei.

## Clay-Delta Variante 0 → Variante 2

Gemessen wurden 126 Kennzahlen aus 18 Clay-Ansichten (D1/G1/D2 × 6 Kameras × 7 Metriken), jeweils Neu-Mesh gegen Neu-Mesh-Kontrolle. Die Variante-0-Kontrolle und Variante 2 nutzten denselben aktuellen Core-Viewer sowie identische Wandmeshes; nur das Geländemesh unterschied sich. **26 positive Deltas insgesamt:** 21 Bildmetriken steigen, 34 sinken, 71 bleiben unverändert; außerdem steigen 5 Regel/Kachel-Zähler (R3 D1 +5, G7b D1 +1, R9w D1 +2, G1 +1, F1 +1). Das Delta-Prüfprogramm endet mit Exit 1. Beispiele: D1-Draufsicht Facetten +31, D1-Wegende Facetten +115, G1-Wandfuß Facetten +33. Eine D2-Wegende-Metrik steigt um 46, obwohl D2 selbst bytegleich ist; der Bildzähler ist ein szenenweiter Kamerawert und kein D2-Höhenfeldvergleich. Die D2-Meshbytes sind separat exakt geprüft.

## Pflichtbilder (Clay, unter Xvfb, selbst angesehen)

| Ansicht | Datei |
|---|---|
| D1-Kreuzungsfläche | [D1_kreuzung.png](bilder_p3d2/D1_kreuzung.png) |
| D1-Wandfuß, exakt (140,35) | [D1_wandfuss_140_35.png](bilder_p3d2/D1_wandfuss_140_35.png) |
| G1-Wandanschluss | [G1_wandanschluss.png](bilder_p3d2/G1_wandanschluss.png) |
| D2-Draufsicht | [D2_draufsicht.png](bilder_p3d2/D2_draufsicht.png) |
| Wegende D1 | [D1_wegende.png](bilder_p3d2/D1_wegende.png) |

Die Bilder zeigen den geplanten lokalen D1-Kreuzungsübergang und den erhaltenen D1-Klippenpunkt. Der G1-Wandanschluss ist sichtbar, aber die Bilder ersetzen keine eigene numerische Wandfuß-/Nahtschwelle. D2 ist die flache, unveränderte Quellfläche. Die Clay-Bildmetriken bleiben trotz dieser visuellen Ansichten rot.

## Tests und offene Punkte

- Gezielte Suite: **9 passed, 3 failed**. Rote Prüfungen: D1 `R9_saegezahn=49` (Grenze 0); feste Negativreferenz `wand_D1_ton.png` Kantenschärfe 2,24 (Grenze 3,00); feste Schattenreferenz Hochfrequenz 0,307 (Grenze 0,25). Die zwei Bildprüfungen verwenden unveränderte Dateien aus `neu/referenz_neg/`, keine aktuellen Kandidatenbilder. Schwellen blieben unverändert.
- Gesamtes `pytest neu/tests -q` stoppt bei Collection mit drei bestehenden Importfehlern: `neu.baue_html.build` fehlt, `neu.gen_relief.SOURCE_COLUMNS` und `neu.gen_relief.build` fehlen in zwei alten Testmodulen.
- `pruefe_t42u.py`: Summe **0** (im temporären Prüfverzeichnis ausgeführt).
- Keine Zellquellspalten oder Overlaydaten geändert. Der Mesh-Adapter ist eine Eingabebrücke für die alten Prüfskripte; sie sind dadurch nicht in native Mesh-Prüfer umgeschrieben.
- Offen: Clay-Delta-Anstiege beheben; D1-Sägezahn (49), R9w/G7b und D1-Endstufe 0,299 m untersuchen; Wandfußanschlüsse mit einer direkten Nahtmetrik absichern; die drei veralteten Testimporte bereinigen.
