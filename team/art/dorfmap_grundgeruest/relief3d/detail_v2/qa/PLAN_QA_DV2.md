# PLAN_QA_DV2 – Prüfregeln Q1–Q14 für detail_v2 (P6, Epochen QA)

Quelle der Regeln: `DETAIL_V2_PLAN.md` Abschnitte 3, 5, 6, 9 (Branch `art/dv2-plan` @ 8f4ad55, noch nicht in `art/dorfmap-fertig`). Nur gelesen, nichts daran geändert. Alte Prüfer (`pruefung/…`) bleiben unverändert.

**D2-Regel (geändert):** „D2-Bereich: Lage und Form erhalten, |Δh| ≤ 1 cm an den alten D2-Vertices“ ersetzt „D2 bitgleich“. Quelle: Entscheidung New Bot vom 19.11.2026, über Grundgerüst an P6 (Steering 19.11. 14:47 MEZ). Alte Dateien und Hashes bleiben unverändert (`d2` height_sha256 749d3c4b… steht nur als Herkunft in `referenz/referenz_alt.json`).

## 1. Ansatz

Ein Runner, ein Aufruf, ein JSON, ein Exit-Code:

```
python3 detail_v2/qa/pruefe_alle.py --wurzel relief3d/detail_v2 \
    [--referenz detail_v2/qa/referenz] [--abnahme /workspace/dorfmap_final/detail_v2/abnahme] \
    [--nur Q1,Q7] [--konfig detail_v2/qa/konfig.json] --out bericht.json
```

- Exit **0** = alle geprüften Regeln ok, **1** = mindestens eine Regel `fehler`, **2** = kein Fehler, aber mindestens eine Regel `offen` (Eingabe fehlt).
- JSON `dv2-qa-1`: `{regeln: {Qn: {regel, status ok|fehler|offen, werte{…}, befunde_anzahl, befunde[≤40 mit x|z], notiz, dauer_s}}, gesamt, zaehlung, dauer_s}`.
- Code: `dv2qa/glb.py` (eigener GLB-Leser/-Schreiber, nur numpy), `dv2qa/welt.py` (Datensatz laden, Kacheln verschweißen über float32-bitgleiche Positionen), `dv2qa/geom.py` (Punktortung XZ, baryzentrische Höhe, Polylinien), `dv2qa/regeln_a|b|c.py` (Q1–Q5, Q6–Q10, Q11–Q14). Schwellen und Formatannahmen nur in `konfig.json`.
- `baue_referenz.py` baut die Alt-Referenz aus dem Repo-Ist (d2d4824): `referenz/d2_alt.npz` (7 395 alte D2-Vertices aus `alle_kacheln`), `referenz/referenz_alt.json` (62 Weg-Mittellinien aus `neu/vektor.json` ÷ 1,2, Wasser, Bauzone 31 927 m²).
- Selbsttest: `selbsttest/baue_dummy.py` (Dummy im Plan-Format, 4 Kacheln D2/E2/D3/E3) und `selbsttest/selbsttest.py` (sauber muss alle 14 bestehen, je Regel eine Fehlervariante muss reißen). Scratch nur `/tmp/dv2_qa/`. Ergebnis: `selbsttest/ERGEBNIS_SELBSTTEST.md`.

## 2. Format (verbindlich seit 19.11., siehe Abschnitt 8)

| Eingabe | Format |
|---|---|
| Mesh | `detail_v2/mesh/manifest.json` = `{version:1, einheit:"m", ursprung:"weltecke", karte:{breite:336,tiefe:303}, klassen:{0 grund,1 weg,2 ufer,3 fels_klippe,4 wasser,5 bruecke}, attribute:{flaeche:"_FLAECHE"}, uv:{TEXCOORD_0 welt_xz_m, TEXCOORD_1 karte_norm, TEXCOORD_2 wegband}, kacheln:[{id, glb:"kacheln/A1.glb", bbox, dreiecke, klassen_anteil}], modelle:[{id:"bruecke_E2", glb:"modelle/bruecke_E2.glb", klasse:5}]}`. GLB in Welt-Metern ohne Node-Transform, y oben. Kacheln 42 × 43 m, Zeile 7 bis z = 303 (`kachelGrenzen()`). |
| Dreiecksklasse | Vertex-Attribut `_FLAECHE` (0–5), Dreiecke klassenrein, Vertices an Klassengrenzen dupliziert. QA verschweißt nach Position (Toleranz 0,1 mm), gemischte Dreiecke = Fehler (Q1). |
| Wasser / Wände | Wasser = Klasse 4 im Geländemesh. Wände/Grat ab Sa als `modelle[]`. |
| Vektoren | `vektor/*.geojson` in Viewer-Metern, Unterscheidung über `typ` (ersatzweise `art`). Real aus #54: `wasser.geojson` (`typ:"wasser"`, `spiegel_m_median`, `flaeche_m2`), `ufer.geojson` (`typ:"uferlinie"`, `seite`, `gewaesser`, `spiegel_m` je Punkt, `geschlossen`; `typ:"uferband"`), `bach_mitte.geojson`. Noch angenommen bis P1a/P1c: `wege.geojson` `typ:"mitte"` (`id`, `breite_m`) / `typ:"rand"`, `kreuzungen.geojson` Polygone, `zonen.geojson` Bauzone über `bauzone_plan`. |
| Datenschicht | Echte Module aus `daten/`: `manifest.mjs` `ladeMesh(manifest)` → `gelaende`, `query.mjs` `ladeDatenschicht(daten, {gelaende})` → `queryPoint`, `quellen()`, `pruefeDreiecksklasse()`; Tests `daten/test/*.test.mjs`. |
| Abnahmebilder | `<ort>_clay_<h>m.jpg` (h 1,7/5/12/30) und `<ort>_wire_5m.jpg`, Orte `dorfkern 209|118`, `bruecke_e2 192|74,5`, `bach_e3 189|100`, `grat_g3 300|90`, `klippen_c3 104|115` (Kraterwand), dazu `QUELLEN.txt`. |

## 3. Regeln: Eingabe, Messmethode, Schwelle, Ausgabe

| Regel | Eingabe | Messmethode | Schwelle (Plan Abschn. 5) |
|---|---|---|---|
| Q1 Geschlossen | Mesh aller Kacheln, Manifest | Manifest-Schema; Klassenreinheit; Verschweißen nach Position (0,1 mm, Klassengrenz-Duplikate = verbunden); Kantenzählung: keine Kante > 2 Dreiecke, Randkanten nur auf dem Außenrand der Manifest-Kacheln; Naht: Vertexmengen beider Kacheln je Schnittlinie bitgleich; Strahlscan an den 5 Orten aus 1,7 m und 5 m, 360 × 1°, 14 Neigungen (Bodentreffer 1–60 m), Schritt 5 cm, Loch = unbedeckter Kartenpunkt, an dem der Strahl unter die zuletzt gesehene Geländehöhe fällt | 0 Mehrfachkanten, 0 Innenrandkanten, 0 Nahtabweichungen, 0 Strahllöcher |
| Q2 Constraint-Treue | Constraint-Linien (konfig `constraint_quellen`), Mesh | Linie alle 5 cm abgetastet → nächste parallele Mesh-Kante (≤ 0,1 m, < 20°); zurück: Kanten mit beiden Enden ≤ 0,1 m → Abstand zur Linie; Maximum beider = Hausdorff (fehlende Kante = 9,99) | ≤ 2 cm |
| Q3 Glätte | Ränder Weg/Ufer/Kante/Grat/Zone | Stützpunkt vs. gleitende 1-m-Mittelung (an Enden symmetrisch verkürzt), Knick zwischen Nachbarsegmenten; Punkte in Kreuzungspolygonen ausgenommen (Annahme, siehe Frage 6). Grat-Silhouette: Sa per Bild (Q13) | ≤ 3 cm, ≤ 15° |
| Q4 Kreuzungen | `kreuzungen.geojson`, Mesh | Ebenen-Fit über Mesh-Vertices + 0,1-m-Abtastung im Polygon | Gefälle ≤ 2 %, Rest ≤ 2 cm |
| Q5 Dellen | Weg-Mittellinien + Breite, Mesh | 0,1-m-Höhenraster im Band 0–3 m neben dem Weg (ohne Wasser); lokale Minima (0,7-m-Fenster); Tiefe = tiefster Punkt eines 1-m-Rings minus Minimum | ≤ 3 cm |
| Q6 Wegprofil | Mittellinien, Mesh | Stationen alle 1 m: Einsenkung = Mittel der Schultern bei ±(b/2 + 0,7 m) minus Mitte; Quergefälle = Geradenfit über die Breite; Längsneigung aus Mittenhöhe. Kreuzungen (+1,5 m), Enden, Wasser (+1 m) ausgenommen | 3–5 cm, ≤ 3,5 %, ≤ 20° |
| Q7 D2 | `referenz/d2_alt.npz` (7 395 alte D2-Vertices), Mesh | Neue Geländehöhe an jedem alten Vertex (Dreiecksinterpolation); alle abgedeckt; Kachel D2 = 126–168 \| 43–86 (Umriss). Lage/Form: eine verschobene Form erzeugt Δh an den alten Vertices (Selbsttest: 0,6 m Wegversatz → 3,7 cm) | \|Δh\| ≤ 1 cm (neue D2-Regel, s. o.) |
| Q8 Ufer | `ufer.geojson` (`spiegel_m` je Punkt), `wasser.geojson`, Mesh | Schnittlinie = Kanten Klasse 4 \| Land plus exakte Kontur der Land-Dreiecke auf dem lokalen Spiegel vs. Uferlinie, beidseitig; Profile alle 10 cm, 0–2,5 m landeinwärts, enden am Wegband; monoton (1 mm Toleranz); Krone > Spiegel | ≤ 5 cm, monoton, Wasser nie über Krone |
| Q9 Netzqualität | Mesh, Constraint-Linien, Mittellinien | Kantenlänge im Grundriss je Dreieck; Band = Schwerpunkt ≤ 1,5 m von Constraint-Linie; fern = > 30 m von Wegen; Min-Winkel im Grundriss außer Dreiecken an Constraint-Ecken (Linienenden, Knicke > 10°, Schnittpunkte Linie×Linie und Linie×Kachelrand); Normale y > 0; Budgets | Kante ≤ Punktabstand × √2 (+1 %): Band 0,2 → 0,286, Wegband 0,25 → 0,357, sonst 0,5 → 0,714, fern 1,0 → 1,428 m, alle Klassen gemessen (Entscheidung 4); Winkel ≥ 20°; ≤ 1,6 Mio. gesamt, ≤ 60 000 je Kachel |
| Q10 UV | Mesh UV0/UV1/UV2 | Überall: 0 Spiegelungen, 0 NaN, 0 Sprünge an positionsgleichen Ecken (> 1 mm), UV1 = (x/336, z/303) ± 1e-5. UV0-Verzerrung \|1 − A_UV0/A_3D\| nur Neigung ≤ 25° und Klasse ≠ 3; Triplanar-Zone (Klasse 3 oder > 25°) nur Stetigkeit. UV2 (Klasse 1): \|∇u\| = 1 ± 10 %, Scherung cos ≤ 0,1, \|∇v\| ± 10 % zum Median im 2-m-Umkreis | 0 / 0 / 0, ≤ 10 % (Entscheidung 5) |
| Q11 Datenschicht | `daten/manifest.mjs` + `query.mjs` (echt), PNGs, Mesh | Node-Harness über `ladeMesh` + `ladeDatenschicht`: 10 000 Zufallspunkte (Seed 611) in den Kacheln, Brückenfußabdrücke + 1 m ausgenommen; Höhe vs. Mesh; Flächentyp vs. `_FLAECHE`-Klasse; zusätzlich P4-`pruefeDreiecksklasse`; alle 6 Felder; `node --test daten/test/*.test.mjs` | ≤ 2 cm, ≥ 99,5 %, Tests grün |
| Q12 Brücken | `modelle/bruecke_*.glb`, Mesh | Teile über Namen; Spalt = Auflager-Unterkante − Gelände; Stufe = Deckoberkante am Ende vs. Gelände 15 cm davor; Geländer 1,0 ± 0,1 m | Bohlen, Träger, Pfosten, Geländer, Auflager; Spalt ≤ 2 cm; Stufe ≤ 5 cm |
| Q13 Abnahmebilder | `--abnahme` Ordner | 5 Orte × 4 Höhen Clay + 5 × Wire 5 m; JPEG; Qualität aus Quantisierungstabelle ± 2; jeder Name in `QUELLEN.txt` | 25 JPG q90 + QUELLEN.txt |
| Q14 Layout | `referenz/referenz_alt.json`, Vektoren, Mesh | Hausdorff je Weg-ID (`id[/teil]`) alt vs. neu; Wasser = Mesh-Fläche Klasse 4 (Grundriss) vs. 6547,84 m² (`wasser.geojson` #54); Bauzone = `zonen.geojson` `bauzone_plan` vs. 31 927 m²; alte Wasserquellen nur im Bericht | ≤ 0,3 m; ±3 %; ±1 % |

## 4. Stand Do 19.11. (Selbsttest)

Alle 14 Regeln als Skript fertig und selbstgetestet. Stand 19.11. 15:26 MEZ nach Abschnitt 8: Dummy im verbindlichen Format; der saubere Dummy besteht alle 14, jede der 20 Fehlervarianten reißt ihre Regel (41 Fälle, 59 s). Dazu Exit 2 bei fehlenden Eingaben, Exit 1 bei Fehler und 3 Kurven-Einheitstests (Kreis glatt, Zickzack und 90°-Ecke erkannt). Details: `selbsttest/ERGEBNIS_SELBSTTEST.md`.

Skalierung und Gegenprobe am alten Mesh im verbindlichen Format: siehe Abschnitt 8 (Q1 21 s, Gesamt 25 s für 7 Regeln auf 0,81 Mio. Dreiecken).

Grenzen des Dummys: Constraint-Linien liegen achsparallel auf dem 0,2-m-Raster, gekrümmte Linien sind nur über die Einheitstests abgedeckt. Wände/Grat (`modelle[]`, P5) sind ohne Dummy, weil sie erst Sa kommen. Fehlervariante Q11-Höhe entfällt: Die echte Datenschicht liest die Höhe aus demselben Mesh.

## 5. Tagesziele

| Tag | Ziel | Fertig wenn |
|---|---|---|
| Do 19.11. bis 23:59 | Plan, alle 14 Skripte, Runner, Alt-Referenz, Dummy und Selbsttest. Draft-PR. | Selbsttest BESTANDEN ✔ |
| Fr 20.11. bis 17:00 | Formatabgleich mit P2 (Mesh/Manifest), P3 (Viewer-API), P4 (query.mjs, Legende), P1 (GeoJSON-Attribute); `konfig.json`/`welt.py` anpassen, Selbsttest erneut. Erster Lauf gegen das erste echte Mesh (~10–12 Uhr), Bericht-JSON und Befundliste an Grundgerüst und P2. | Lauf ohne Prüfer-Ausnahme, jede Regel ok/fehler mit Ort |
| Sa 21.11. bis 19:00 | Messung Q1–Q14 auf dem Abgabestand; Clay-Bilder 1,7/5/12/30 m an den 5 Orten und je 1 Wire aus 5 m mit dicken Linien über die Viewer-Testkamera-API (`__test.kam`), JPG q90 nach `/workspace/dorfmap_final/detail_v2/abnahme/` mit QUELLEN.txt (ehrlich); Grat-Silhouette Q3 per Bild; `AUSNAHMEN_DV2.md` nach Abschnitt 6 (16 „muss weg“, A6 bleibt, A12 bedingt an Q8, A5/A16 klären). | Q13 ok, Bericht mit Befunden |
| So 22.11. bis 18:00 | Nachprüfung nach Nachbesserung, Endbericht | Gesamt-JSON Exit 0 oder ehrliche Ausnahmeliste |

## 6. Risiken

1. **Weg-/Zonen-Attribute** (P1a/P1c noch nicht geliefert): `typ:"mitte"/"rand"`, `bauzone_plan` angenommen; Abweichung = nur `konfig.json`.
2. **Wasser-Variante im Mesh:** Dummy und Q1 setzen Wasser als flache Klasse-4-Fläche, verbunden mit dem Ufer, voraus. Führt P2 die Wasserfläche 1 m *unter* das Ufer (überlappend, nicht verbunden), meldet Q1 deren Ränder als Innenrandkanten → dann mit Grundgerüst klären (Fehlalarm vs. echter Riss).
3. **Q10-UV2** misst |∇u| = 1 ± 10 % auch in Kurven; am Außenrand enger Kurven (R < ~10 m) ist das geometrisch > 10 %. Treffer dort kennzeichnen statt wegdefinieren.
4. **Laufzeit:** Auf 0,8 Mio. Dreiecken dauern alle Regeln < 1 min. Bei 1,6 Mio. erwartet ~2–3 min, unkritisch.
5. **Erstes Mesh verspätet** (Fr ~10–12 Uhr): Dann Lauf am Teilstand (Manifest mit den vorhandenen Kacheln; Q1 wertet Ränder nur am Außenrand der vorhandenen Kacheln).

## 7. Offene Fragen an Grundgerüst

Alle acht Fragen vom Do sind beantwortet (Abschnitt 8). Offen sind nur noch Lieferungen: `wege.geojson`/`kreuzungen.geojson` (P1a) und `zonen.geojson` (P1c) mit den angenommenen Attributen `typ:"mitte"/"rand"` bzw. `bauzone_plan`. Bis dahin sind Q2–Q6, Q9 und Q14 auf echten Daten `offen`. Das Mesh (P2) kommt auf `art/dv2-mesh`, Grundgerüst meldet.

## 8. Entscheidungen Grundgerüst 19.11.2026 (verbindlich, eingearbeitet 19.11. ab 15:16 MEZ)

1. **Format:** wie Abschnitt 2 (manifest version 1, `_FLAECHE`, klassenreine Dreiecke, duplizierte Grenzvertices, 3 UV-Sets, `modelle[]`; Wasser Klasse 4 im Geländemesh; Wände/Grat Sa als `modelle[]`; Kacheln 42 × 43 m, Zeile 7 bis z = 303). Q1 wertet positionsgleiche Duplikate als verbunden (Schweißen nach Position mit Toleranz). Selbsttest: Duplikat-Naht kein Loch, echte Naht-Lücke (1 cm) wird gefunden.
2. **Mesh** kommt auf `art/dv2-mesh`, `relief3d/detail_v2/mesh/`; Grundgerüst meldet.
3. **query.mjs:** Kopf auf `art/dorfmap-fertig` (`baueMeshIndex`, `quellen()`), Q11 nutzt `ladeMesh` + `ladeDatenschicht`. GeoJSON aus #54: `ufer.geojson {id, typ, seite, gewaesser, spiegel_m, breite_m, geschlossen, flaeche_m2}`, `bach_mitte.geojson {id, typ, gewaesser, breite_m, spiegel_m}`; Unterscheidung über `typ`. Bauzone heißt `bauzone_plan`.
4. **Q9:** Kante ≤ Punktabstand × √2 (+1 %), Fernbereich wird mitgemessen (≤ 1,42 m), nicht ausgenommen.
5. **Q10:** UV0 gilt für Neigung ≤ 25° mit ≤ 10 %. Klasse 3 und Neigung > 25° = Triplanar-Zone: nur UV-Stetigkeit (keine Sprünge/Flips, keine NaN). UV2 im Wegband ≤ 10 % Verzerrung.
6. **Q3:** Kreuzungspolygone vom Knick-Grenzwert ausgenommen; R8 (eben) gilt dort weiter (Q4).
7. **Q14:** Referenz `wasser.geojson` aus #54 (6547,84 m²), Mesh-Wasserfläche (Klasse 4) ± 3 %. Alte Quellen (DS > 0 6 338, WV-Punkte 6 461,25, WASSER_EIS 6 912, vektor.json 6 695 m²) nur im Bericht.
8. **C3** = Kraterwand, Abnahmepunkt 104|115.

**D2-Regel** (Entscheidung New Bot 19.11.2026 über Grundgerüst) unverändert: |Δh| ≤ 1 cm an den alten D2-Vertices, Lage und Form erhalten.

**Gegenprobe altes Mesh im neuen Format** (56 Kacheln, 814 464 Dreiecke, Klasse 0, ohne UV2, `vektor/` aus #54, echte `daten/`-Module), 24,9 s gesamt:
- Q1 ok (21 s, 0 Löcher, 8 329 Duplikate verschweißt, Manifest ok inkl. Zeile 7 bis 303).
- Q7 ok (Δh 0).
- Q10 ok mit der neuen Regel (vorher wörtlich 47 754 Verstöße).
- Q11: Höhe über die echte Datenschicht 0,4 mm; Fläche/Tests fehlen noch (kein `flaeche.png`, keine Tests in diesem Abzug) → fehler wie erwartet.
- Q8 fehler wie erwartet: altes Ufer ist Treppe (bis 10,3 m Abstand, 1 531 nicht monotone Profile).
- Q9/Q14 offen (keine `wege.geojson`).
