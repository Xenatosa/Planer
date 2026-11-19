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
| Wasser / Wände | Geländemesh geschlossen inkl. Bachbett: Klasse 4 = Bett-Dreiecke unter dem Spiegel, mit dem Ufer verbunden. Wasseroberfläche = eigenes Modell in `modelle[]` (`klasse:4`, Spiegel aus `spiegel_m`), nicht Teil von Q1 (Abschn. 8, Runde 2). Wände/Grat ab Sa als `modelle[]`. |
| Vektoren | `vektor/*.geojson` in Viewer-Metern, Unterscheidung über `typ` (ersatzweise `art`). Real aus #54: `wasser.geojson` (`typ:"wasser"`, `spiegel_m_median`, `flaeche_m2`), `ufer.geojson` (`typ:"uferlinie"`, `seite`, `gewaesser`, `spiegel_m` je Punkt, `geschlossen`; `typ:"uferband"`), `bach_mitte.geojson`. Real aus #56: `wege.geojson` über `rolle` = `mittellinie` / `rand_links` / `rand_rechts` (LineString), `band` (Polygon), `netz` (MultiPolygon, Vereinigung); `klasse` = GASSE / ANBINDUNG / HAUSWEG; dazu `id`, `breite`, `teil`. `kreuzungen.geojson`: `art` = `weg_kreuzung` (38) / `weg_platz` (50), `id`, `weg_ids`, `platz_ids`, `flaeche`. Noch angenommen bis P1c (heute bis 19:00): `zonen.geojson` mit `klasse`/`untergrund`/`id`, Bauzone über `bauzone_plan`. |
| Datenschicht | Echte Module aus `daten/`: `manifest.mjs` `ladeMesh(manifest)` → `gelaende`, `query.mjs` `ladeDatenschicht(daten, {gelaende})` → `queryPoint`, `quellen()`, `pruefeDreiecksklasse()`; Tests `daten/test/*.test.mjs`. |
| Abnahmebilder | `<ort>_clay_<h>m.jpg` (h 1,7/5/12/30) und `<ort>_wire_5m.jpg`, Orte `dorfkern 209|118`, `bruecke_e2 192|74,5`, `bach_e3 189|100`, `grat_g3 300|90`, `klippen_c3 104|115` (Kraterwand), dazu `QUELLEN.txt`. |

## 3. Regeln: Eingabe, Messmethode, Schwelle, Ausgabe

| Regel | Eingabe | Messmethode | Schwelle (Plan Abschn. 5) |
|---|---|---|---|
| Q1 Geschlossen | Mesh aller Kacheln, Manifest | Manifest-Schema; Klassenreinheit; Verschweißen nach Position (0,1 mm, Klassengrenz-Duplikate = verbunden); Kantenzählung: keine Kante > 2 Dreiecke, Randkanten nur auf dem Außenrand der Manifest-Kacheln; Naht: Vertexmengen beider Kacheln je Schnittlinie bitgleich; Strahlscan an den 5 Orten aus 1,7 m und 5 m, 360 × 1°, 14 Neigungen (Bodentreffer 1–60 m), Schritt 5 cm, Loch = unbedeckter Kartenpunkt, an dem der Strahl unter die zuletzt gesehene Geländehöhe fällt. Geländemesh inkl. Bett (Klasse 4); Wasserspiegel-Modell zählt nicht (verdeckt kein Loch), Brückenmodelle schon | 0 Mehrfachkanten, 0 Innenrandkanten, 0 Nahtabweichungen, 0 Strahllöcher |
| Q2 Constraint-Treue | Constraint-Linien (konfig `constraint_quellen`), Mesh | Linie alle 5 cm abgetastet → nächste parallele Mesh-Kante (≤ 0,1 m, < 20°); zurück: Kanten mit beiden Enden ≤ 0,1 m → Abstand zur Linie; Maximum beider = Hausdorff (fehlende Kante = 9,99) | ≤ 2 cm |
| Q3 Glätte | Wegränder, Uferlinien, `bach_mitte`, Kanten, Grat, Zonen (`layer=flaechentyp`) und die Mesh-Kantenzüge dazu (Mesh-Vertices ≤ 2 cm an der Linie, nach Bogenlänge geordnet) | Runde 3: jede Linie zuerst gleichmäßig auf 0,05 m nach Bogenlänge neu abgetastet (lineare Interpolation, Endpunkte bleiben), dann gleitendes 1-m-Mittel (an Enden symmetrisch verkürzt); Abweichung = Abstand Abtastpunkt → gemittelte Linie. Knick = Winkel zwischen den Abtastsegmenten vor und nach dem Punkt (eine Segmentlücke); in Kreuzungspolygonen vom Knick ausgenommen (R8/Q4 gilt dort). Zonenringe `flaechentyp` und `untergrund` (F11 Runde 4, F13 Runde 5): ausgenommen nur Abschnitte auf dem Kartenrand (inkl. Ecken) und ± 0,5 m Bogenlänge um Stoßpunkte mit ≥ 3 Zonen, der Kartenrand zählt als Zone „außerhalb“; Brücken-Stoßpunkte hart; Stoßpunktliste in der Ausgabe. Logikschichten `bauzone_plan` und `slot` nie in Q3. Grat-Silhouette: Sa per Bild (Q13) | ≤ 3 cm hart für alle Linien, ≤ 15° |
| Q4 Kreuzungen | `kreuzungen.geojson` (`art` weg_kreuzung + weg_platz, beide geprüft, Zählung je `art`), Mesh | Ebenen-Fit über Mesh-Vertices + 0,1-m-Abtastung im Polygon | Gefälle ≤ 2 %, Rest ≤ 2 cm |
| Q5 Dellen | Wegfläche `rolle=netz` (ersatzweise Mittellinie + `breite`), Mesh | 0,1-m-Höhenraster im Band 0–3 m neben der Wegfläche (ohne Wasser); lokale Minima (0,7-m-Fenster); Tiefe = tiefster Punkt eines 1-m-Rings minus Minimum | ≤ 3 cm |
| Q6 Wegprofil | Mittellinien, Mesh | Stationen alle 1 m: Einsenkung = Mittel der Schultern bei ±(b/2 + 0,7 m) minus Mitte; Quergefälle = Geradenfit über die Breite; Längsneigung aus Mittenhöhe. Kreuzungen (+1,5 m), Enden, Wasser (+1 m) ausgenommen | 3–5 cm, ≤ 3,5 %, ≤ 20° |
| Q7 D2 | `referenz/d2_alt.npz` (7 395 alte D2-Vertices), Mesh | Neue Geländehöhe an jedem alten Vertex (Dreiecksinterpolation); alle abgedeckt; Kachel D2 = 126–168 \| 43–86 (Umriss). Lage/Form: eine verschobene Form erzeugt Δh an den alten Vertices (Selbsttest: 0,6 m Wegversatz → 3,7 cm) | \|Δh\| ≤ 1 cm (neue D2-Regel, s. o.) |
| Q8 Ufer | `ufer.geojson` (`spiegel_m` je Punkt), `wasser.geojson`, Geländemesh inkl. Bett, Spiegelmodell (`modelle[]` klasse 4) | (a) Spalt: Rand des Spiegelmodells alle 5 cm, Gelände dort ≥ Spiegel − 2 mm (Kante steckt im Ufer, von oben kein Spalt); Überlappung = waagerechter Abstand eines Spiegelrandpunkts im Ufer zur Wasserlinie ≤ 10 cm (Runde 3); (b) Schnitt: je Uferstation (10 cm) Vorzeichenwechsel Gelände − Spiegel entlang der Normalen (−2 m Wasser bis +2,5 m Land), sonst „Spiegel unter Uferkante ohne Schnitt“; (c) exakte Kontur Gelände = Spiegelmodell vs. Uferlinie beidseitig; (d) Profile 0–2,5 m landeinwärts monoton (1 mm), enden am Wegband; Krone > `spiegel_m`. Kartenrand ausgenommen; Spiegel vs. `spiegel_m` nur Bericht | Spalt 0, Überlappung ≤ 10 cm, Schnitt an jeder Station, ≤ 5 cm, monoton, Wasser nie über Krone |
| Q9 Netzqualität | Mesh, Constraint-Linien, Mittellinien | Kantenlänge im Grundriss je Dreieck; Band = Schwerpunkt ≤ 1,5 m von Constraint-Linie; fern = > 30 m von Wegen; Min-Winkel im Grundriss außer Dreiecken an Constraint-Ecken (Linienenden, Knicke > 10°, Schnittpunkte Linie×Linie und Linie×Kachelrand); Normale y > 0; Budgets | Kante ≤ Punktabstand × √2 (+1 %): Band 0,2 → 0,286, Wegband 0,25 → 0,357, sonst 0,5 → 0,714, fern 1,0 → 1,428 m, alle Klassen gemessen (Entscheidung 4); Winkel ≥ 20°; ≤ 1,6 Mio. gesamt, ≤ 60 000 je Kachel |
| Q10 UV | Mesh UV0/UV1/UV2 | Überall: 0 Spiegelungen, 0 NaN, 0 Sprünge an positionsgleichen Ecken (> 1 mm), UV1 = (x/336, z/303) ± 1e-5. UV0-Verzerrung \|1 − A_UV0/A_3D\| nur Neigung ≤ 25° und Klasse ≠ 3; Triplanar-Zone (Klasse 3 oder > 25°) nur Stetigkeit. UV2 (Klasse 1): \|∇u\| = 1 ± 10 %, Scherung cos ≤ 0,1, \|∇v\| ± 10 % zum Median im 2-m-Umkreis; Kurvenradius der nächsten Mittellinie (Umkreisradius über ±1 m, Minimum im ±1,5-m-Fenster) < 10 m → nur kennzeichnen (`uv2_enge_kurve_*`), nicht blockierend | 0 / 0 / 0, ≤ 10 % (Entscheidung 5); UV2 blockierend erst ab r ≥ 10 m (Runde 2) |
| Q11 Datenschicht | `daten/manifest.mjs` + `query.mjs` (echt), PNGs, Mesh | Node-Harness über `ladeMesh` + `ladeDatenschicht`: 10 000 Zufallspunkte (Seed 611) in den Kacheln, Brückenfußabdrücke + 1 m ausgenommen; Höhe vs. sichtbare Oberfläche (Gelände, über Wasser der Spiegel, wo er über dem Bett liegt); Flächentyp vs. `_FLAECHE`-Klasse (über Wasser `wasser`); zusätzlich P4-`pruefeDreiecksklasse`; alle 6 Felder; `node --test daten/test/*.test.mjs` | ≤ 2 cm, ≥ 99,5 %, Tests grün |
| Q12 Brücken | `modelle/bruecke_*.glb`, Mesh | Teile über Namen; Spalt = Auflager-Unterkante − Gelände; Stufe = Deckoberkante am Ende vs. Gelände 15 cm davor; Geländer 1,0 ± 0,1 m | Bohlen, Träger, Pfosten, Geländer, Auflager; Spalt ≤ 2 cm; Stufe ≤ 5 cm |
| Q13 Abnahmebilder | `--abnahme` Ordner | 5 Orte × 4 Höhen Clay + 5 × Wire 5 m; JPEG; Qualität aus Quantisierungstabelle ± 2; jeder Name in `QUELLEN.txt` | 25 JPG q90 + QUELLEN.txt |
| Q14 Layout | `referenz/referenz_alt.json`, Vektoren (`rolle=mittellinie`), Mesh, Spiegelmodell | Hausdorff je Weg-ID (`id/teil`) alt vs. neu; Wasser **maßgeblich = sichtbare Spiegelmodell-Fläche** (0,1-m-Zellen, in denen der Spiegel über dem Gelände liegt) vs. Fläche aus `wasser.geojson` (`typ=wasser`, Vereinigung), zur Laufzeit berechnet (konfig `q14_wasser_referenz`, Stand aa78160: 6 630,17 m²); Spiegelmodell gesamt und Klasse-4-Bett nur Bericht; Ausnahmen nur laut konfig `q14_ausnahmen` (A-DV2-02, F12); Bauzone ab #61 als Zellschicht: Zellsumme = 31 893 und Zellmenge deckungsgleich mit `neu/zellen_relief.csv` (`bauzone_plan` = 1), Abweichungen mit Zellen; ohne `zellen` Rückfall Fläche `layer=bauzone_plan` vs. 31 927 m², fehlt die Datei → „Eingabe fehlt“, Status `offen` (nicht bestanden); alte Wasserquellen nur im Bericht | ≤ 0,3 m; ±3 %; ±1 % |

## 4. Stand Do 19.11. (Selbsttest)

Alle 14 Regeln als Skript fertig und selbstgetestet. Stand 19.11. Runde 6: 67 Fälle BESTANDEN (111 s); neu: Q3_bruecke (offen P5), Q3_bruecke_p5 (P5-Regel an → ok), Q3_bruecke_p5_laengs, Q3_wegende (Ausnahme A-DV2-01), Q3_wegende_weit, Q3_wegende_gross (beide hart). Stand Runde 5: Der saubere Dummy besteht alle 14 Regeln, jede der 26 Fehlervarianten reißt ihre Regel (neu: Q14_zelle_fehlt). Dazu kommen 5 Sonderfälle (enge Kurve nur gekennzeichnet, fehlende Zonen = offen, Q14-Ausnahme = ok mit Ausnahme-Befund, Bauzone im Zellformat = ok, Logikschichten nicht in Q3), Exit 2/1, die Q14-Referenz aus der Datei, 5 Q3-Einheitstests (Kreis 0,25 vs. 0,05 m, DP = dicht, Delle, Zickzack, Ecke), 4 F11-Tests (Kartenrand, Stoßfenster, Knick knapp außerhalb, Brückenecke) und 2 F13-Tests (Kartenrand-Stoß im Fenster, mit Brücke hart). Ergebnis: 61 Fälle, 105 s. Details: `selbsttest/ERGEBNIS_SELBSTTEST.md`.

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

1. **Zonen-Attribute** (P1c bis 19:00): `zonen.geojson` mit `klasse`/`untergrund`/`id`, Bauzone über `bauzone_plan` angenommen (Q14 akzeptiert Property `bauzone_plan` = true oder `klasse`/`id`/`typ` = `bauzone_plan`); Abweichung = nur `konfig.json`/Q14-Filter.
2. **Datenschicht über dem Spiegelmodell:** `query.mjs` `baueGelaende` behandelt jedes Modell als Deck (`deckAn`), also auch den Wasserspiegel. Wo der Spiegel unter dem Ufer steckt (Überlappung), liefert `queryPoint` die Spiegelhöhe *unter* dem Gelände und Fläche `wasser`. Q11 vergleicht mit der sichtbaren Oberfläche und meldet das ab 2 cm. Bei kleiner Überlappung (Dummy 5 cm → 1,3 cm) unkritisch, bei großer ein echter Befund für P4 → Frage an Grundgerüst/P4 (Abschn. 8, Runde 2).
3. **Q10-UV2 in engen Kurven** (< 10 m): nur gekennzeichnet; ok nur, solange auf dem Clay-Bild nichts sichtbar ist → Sa an den Orten mit `uv2_enge_kurve_*` gezielt prüfen.
4. **Laufzeit:** Auf 0,8 Mio. Dreiecken dauern alle Regeln < 1 min. Bei 1,6 Mio. erwartet ~2–3 min, unkritisch.
5. **Erstes Mesh verspätet** (Fr ~10–12 Uhr): Dann Lauf am Teilstand (Manifest mit den vorhandenen Kacheln; Q1 wertet Ränder nur am Außenrand der vorhandenen Kacheln).

## 7. Offene Fragen an Grundgerüst

Runden 1–3 beantwortet (Abschnitt 8); F9 bestätigt (sichtbarer Spiegel), F10 erledigt (`queryPoint` nimmt den Spiegel nur über dem Gelände, Tools baut das). `zonen.geojson` ist da (#57). F11 (Zonenringe in Q3) und F12 (ausgelassene Weg-Teilstücke in Q14) entschieden, siehe Abschnitt 8 Runde 4. Fragen aus Runde 2 (erledigt):

- **F9 Q14-Wasser:** Ist mit „Spiegelmodell-Fläche“ die *sichtbare* Fläche gemeint (Spiegel über dem Gelände, so umgesetzt) oder die Grundrissfläche des ganzen Modells inkl. des Teils, der im Ufer steckt? Die ganze Fläche wächst mit der Überlappung (Dummy: 5 cm Überlappung = +2,4 %) und kippt dann leicht über ±3 %.
- **F10 Datenschicht über Wasser:** Soll `queryPoint` über Wasser die Spiegelhöhe liefern (so macht es `query.mjs` heute für jedes Modell) und im Überlappungsstreifen das Gelände? Heute kommt dort die Spiegelhöhe unter dem Gelände (Risiko 2).

## 8. Entscheidungen Grundgerüst 19.11.2026 (verbindlich, eingearbeitet 19.11. ab 15:16 MEZ)

1. **Format:** wie Abschnitt 2 (manifest version 1, `_FLAECHE`, klassenreine Dreiecke, duplizierte Grenzvertices, 3 UV-Sets, `modelle[]`; Wasser Klasse 4 im Geländemesh; Wände/Grat Sa als `modelle[]`; Kacheln 42 × 43 m, Zeile 7 bis z = 303). Q1 wertet positionsgleiche Duplikate als verbunden (Schweißen nach Position mit Toleranz). Selbsttest: Duplikat-Naht kein Loch, echte Naht-Lücke (1 cm) wird gefunden.
2. **Mesh** kommt auf `art/dv2-mesh`, `relief3d/detail_v2/mesh/`; Grundgerüst meldet.
3. **query.mjs:** Kopf auf `art/dorfmap-fertig` (`baueMeshIndex`, `quellen()`), Q11 nutzt `ladeMesh` + `ladeDatenschicht`. GeoJSON aus #54: `ufer.geojson {id, typ, seite, gewaesser, spiegel_m, breite_m, geschlossen, flaeche_m2}`, `bach_mitte.geojson {id, typ, gewaesser, breite_m, spiegel_m}`; Unterscheidung über `typ`. Bauzone heißt `bauzone_plan`.
4. **Q9:** Kante ≤ Punktabstand × √2 (+1 %), Fernbereich wird mitgemessen (≤ 1,42 m), nicht ausgenommen.
5. **Q10:** UV0 gilt für Neigung ≤ 25° mit ≤ 10 %. Klasse 3 und Neigung > 25° = Triplanar-Zone: nur UV-Stetigkeit (keine Sprünge/Flips, keine NaN). UV2 im Wegband ≤ 10 % Verzerrung.
6. **Q3:** Kreuzungspolygone vom Knick-Grenzwert ausgenommen; R8 (eben) gilt dort weiter (Q4).
7. **Q14:** Referenz `wasser.geojson` aus #54 (6547,84 m²), Mesh-Wasserfläche (Klasse 4) ± 3 %. Alte Quellen (DS > 0 6 338, WV-Punkte 6 461,25, WASSER_EIS 6 912, vektor.json 6 695 m²) nur im Bericht.
8. **C3** = Kraterwand, Abnahmepunkt 104|115.

**Runde 2 (Grundgerüst 19.11.2026, eingearbeitet 19.11. 15:31–15:48 MEZ), Antworten wörtlich zusammengefasst:**

- (a) `wege.geojson` (#56): Unterscheidung über `rolle` = `mittellinie` / `rand_links` / `rand_rechts` (LineString), `band` (Polygon), `netz` (MultiPolygon, Vereinigung); `klasse` = GASSE / ANBINDUNG / HAUSWEG; weiter `id`, `breite`, `teil`. `kreuzungen.geojson`: `art` = `weg_kreuzung` (38) / `weg_platz` (50), `id`, `weg_ids`, `platz_ids`, `flaeche`. Zonen (P1c) kommen heute bis 19:00 mit `klasse`/`untergrund`/`id`; Name bleibt `bauzone_plan`. Bis dahin Annahme lassen; Q14-Bauzone toleriert die fehlende Datei mit der Meldung „Eingabe fehlt“, nicht als bestanden.
  → konfig: Constraints/Q3 = `rolle` ∈ {rand_links, rand_rechts}; Mittellinien `rolle=mittellinie`, Breite `breite`; Wegfläche (Q5) `rolle=netz`; Kreuzungen `art` ∈ {weg_kreuzung, weg_platz}. Q14 Status `offen` + Befund „Eingabe fehlt: zonen.geojson (P1c)“.
- (b) Geländemesh geschlossen inkl. Bachbett unter Wasser (Klasse 4 = Bett-Dreiecke, mit dem Ufer verbunden) → Q1 auf dem Geländemesh inkl. Bett. Wasseroberfläche = eigenes Modell in `modelle[]` (Spiegel aus `spiegel_m`), **nicht** Teil von Q1. Q8 prüft den Anschluss Spiegel/Ufer: von oben kein Spalt sichtbar, Spiegel schneidet das Ufer. Q14-Wasser: Spiegelmodell-Fläche und Klasse-4-Fläche, beide berichten; Referenz 6547,84 m² ± 3 %; **maßgeblich: Spiegelmodell, da sichtbar**.
  → `welt.py`: Wassermodelle = `modelle[]` mit `klasse 4` (oder id `wasser*`), aus Q1-Strahlscan und Brückenlogik heraus. Q8 neu (Spalt, Schnitt, Kontur, Profile). Q14: sichtbare Spiegelfläche maßgeblich (Frage F9). Q11 vergleicht mit der sichtbaren Oberfläche (Frage F10).
- (c) UV2 ≤ 10 % gilt ab Kurvenradius 10 m; darunter kennzeichnen und als Zahl berichten, nicht blockierend (nur ok, solange auf dem Clay-Bild nichts sichtbar ist).
  → Q10: `uv2_enge_kurve_dreiecke`, `uv2_enge_kurve_ueber_10pct_gekennzeichnet`, `uv2_enge_kurve_max_abw`, `kurvenradius_min_m`, `enge_kurven_orte`.

Selbsttest Runde 2: **47 Fälle BESTANDEN** (78 s). Neu: Dummy mit geschlossenem Bett (Klasse 4, 0,27 m unter dem Spiegel) und separatem Spiegelmodell `wasser_W01` (5 cm im Ufer), `wege.geojson`/`kreuzungen.geojson` im #56-Schema (mittellinie/rand_links/rand_rechts/band/netz, `art=weg_kreuzung`). Neue Fälle:
- Q1_bett: Loch im Bett unter dem Spiegel wird gefunden; der Spiegel verdeckt nichts.
- Q8_spalt: Spalt Spiegel/Ufer gefunden (Spiegelkante 15 cm vor dem Ufer, 3,7 cm über dem Bett).
- Q8_ohne_schnitt: Spiegel 0,4 m tief, unter der Uferkante ohne Schnitt gefunden (1 702/1 702 Stationen).
- Q10_kurve: enge S-Kurve (r ≈ 5 m) mit 15 % UV2-Stauchung → Status ok, 280 Dreiecke gekennzeichnet.
- Q14_wasser: sichtbare Spiegelfläche +9,5 % gefunden.
- Q14_ohne_zonen: Status `offen` mit „Eingabe fehlt“.
- Sauber: Spalt 0; sichtbare Spiegelfläche = Bett Klasse 4 = Referenz (361,2 m²).

**Gegenprobe echtes `wege.geojson`/`kreuzungen.geojson` (#56) + altes Mesh** (d2d4824 im neuen Format, 814 464 Dreiecke; Q2–Q6/Q9 in 55 s). Alle sechs reißen erwartungsgemäß, weil das alte Mesh die neuen Linien nicht kennt. Die Zahlen sind die Basis für Fr:
- Q2: 221 Linien (122 Wegränder, 88 Kreuzungsumrisse, 11 Uferlinien), davon 210 ohne passende Mesh-Kante (9,99).
- Q3 (reine Vektorprüfung, unabhängig vom Mesh): 133 Linien, 13 über Schwelle. Wege: G003_anb 3,45 cm und G903a 3,12 cm (knapp über 3 cm, Knick < 15°). Uferlinien #54: 11 Linien mit 6,6–13,6 cm Abweichung von der 1-m-Mittelung, Knick ≤ 10,5° → Hinweis an P1a/P1b.
- Q4: 88 Kreuzungen (38 weg_kreuzung, 50 weg_platz), 22 nicht eben (Rest bis 0,94 m, Gefälle bis 23,6 %).
- Q5: 442 770 Kandidaten, 1 Delle 6,05 cm bei 324|38,5.
- Q6: 1 455 m Mittellinie, davon 254 Stationen außerhalb Kreuzung/Ende/Wasser gewertet und 252 mit Befund (altes Mesh nicht eingesenkt: Einsenkung −0,09 bis 1,99 m, quer bis 49 %).
- Q9: 111 688 Kanten zu lang (altes 0,5-m-Raster, 0,707 m gegen 0,286 m im Band).

**Runde 3 (Entscheidung QA, Vorschlag Grundgerüst übernommen, eingearbeitet 19.11. 18:08–18:22 MEZ, Basis 38fa7ec + Merge aa78160 mit #57–#60):**

1. **q3-Methode abtastunabhängig.** Jede Linie (Wege, Ufer, Bach, Kanten, Grat, Zonen und die Mesh-Kantenzüge, alle gleich) wird vor dem Mitteln gleichmäßig auf 0,05 m nach Bogenlänge neu abgetastet. Das geschieht per linearer Interpolation entlang der Polylinie, die Endpunkte bleiben. Danach folgt das gleitende 1-m-Mittel. Die Abweichung ≤ 3 cm ist hart für alle Linien, ohne Sonderschwelle. Kreuzungspolygone bleiben vom Knick-Limit ausgenommen, R8 gilt dort weiter (Q4). In konfig.json stehen `q3_abtastung_m` 0,05 und `q3_fenster_m` 1,0.
   - **Begründung:** Das alte Verfahren mittelte über die Stützpunkte. Dichte Stützpunkte zogen das Mittel zur Kurve, wenige zogen es weg. Gemessen wurde also die Punktverteilung und nicht die Form: Kreis r 2 m alt 1,05 cm bei 0,25 m gegen 1,87 cm bei 0,05 m. Die neue Messung misst die Form: 2,53 gegen 2,29 cm. Der Rest von 2,4 mm ist echte Form, denn das 0,25-m-Polygon liegt mit 3,9 mm Sehnenpfeil innen. DP-Stützpunkte (0,14–1,14 m) und dichte Punkte (0,01 m) liefern 1,85 gegen 1,82 cm. **Kein Lockern:** Die Schwelle bleibt 3 cm für alle Linien, Mesh-Kantenzüge werden genauso gemessen. Echte Dellen werden weiter gefunden: 5 cm → 4,01 cm dicht und DP, Zickzack 4,54 cm / 53°, Ecke 90°.
   - **Knick:** wird jetzt auf der Neuabtastung gemessen (Sehne vor/nach dem Punkt mit einer Segmentlücke). Ein Stützpunktknick zählt so voll, ein glatter Bogen r 1,6 m ergibt etwa 5–7° (vorher 3–4° auf dichten Stützpunkten). Die Grenze bleibt 15°.
2. **Q8 neu: Überlappung** des Spiegels ins Ufer/Gelände ≤ 10 cm. P2 begrenzt die Überlappung; `queryPoint` nimmt den Spiegel nur dort, wo er über dem Gelände liegt (Tools baut das). Kein Spalt bleibt Pflicht.
3. **Q14 dateibasiert:** Die Referenzfläche ist keine feste Zahl mehr. konfig `q14_wasser_referenz` = `wasser.geojson` (`typ=wasser`), die Fläche wird zur Laufzeit berechnet (Stand aa78160: 6 630,17 m², ± 3 %). **F9 bestätigt:** Q14 misst den sichtbaren Teil des Spiegels. Bauzone ab #57 über `layer=bauzone_plan` (25 Polygone, 31 893 m² gegen 31 927 m² = −0,11 %).

Selbsttest Runde 3: **50 Fälle BESTANDEN** (neu: Q8_ueberlappung 0,3 m gefunden; Q3 (a)/(b)/(c); Q14-Referenz aus Datei 6 630,17 m²).

Gegenprobe echte Vektoren auf art/dorfmap-fertig (aa78160, nach #58/#60; wasser/ufer 0,05 m abgetastet), q3 alt → neu (Abweichung max, Knick max):

| Linie | alt | neu |
|---|---|---|
| Ufer (11 Linien) | 2,01–2,90 cm, ≤ 4,0° | 2,01–2,90 cm, ≤ 7,4° |
| G003_anb (rand_links / rand_rechts) | 2,63 / 2,24 cm | 2,07 / 1,75 cm |
| G903a (rand_links / rand_rechts) | 0,51 / 0,89 cm | 1,60 / 2,12 cm |
| bach_mitte (23 Linien) | ≤ 2,70 cm | ≤ 2,70 cm |
| Wege 122, Kanten 20, Grat 4 | 0 über Schwelle | 0 über Schwelle |
| Zonen `flaechentyp` (97 Ringe) | 49 über Schwelle | 39 über Schwelle, bis 26 cm, Knick bis 179° |

Die Zonen-Treffer liegen an echten Ecken der Flächentyp-Ringe: Kartenrand, Einmündungen Weg/Platz, Brückenrechteck. Siehe Frage F11.

**F11 (neu):** Die Flächentyp-Ringe aus `zonen.geojson` (#57) haben notwendige Ecken: Kartenrand, T-Stöße Zone|Zone, Brückenrechteck. Mit „≤ 3 cm hart für alle Linien“ reißt Q3 dort (39 von 97 Ringen). Soll Q3 die Zonenringe prüfen, aber Kartenrand und Stoßpunkte (Knoten mit ≥ 3 Zonen) ausnehmen? Oder reißt es zu Recht (P1c rundet aus)? → **entschieden in Runde 4** (unten).
**F12 (neu):** Q14 meldet 4 alte Weg-Teilstücke als fehlend (G002_anb/0, G008/2, G010/2, G014/1). P1a hat genau diese in `wege.geojson` `meta.ausgelassen` begründet weggelassen (Teilstück < 0,5 m, Skelettrest). Sollen begründet ausgelassene Teile in Q14 als Ausnahme zählen? → **entschieden in Runde 4** (unten).

**Runde 4 (Entscheidung Grundgerüst F11/F12, eingearbeitet 19.11. ab 18:22 MEZ, Basis 33d0d86):**

1. **F11 – Q3 Zonenringe (`layer=flaechentyp`).** Ausgenommen sind **nur** (1) Abschnitte, die auf dem Kartenrand liegen, inklusive der 4 Kartenecken (Abtastpunkt ≤ `q3_zonen.kartenrand_tol_m` = 0,01 m vom Rand 0…336 × 0…303 m), und (2) ein Fenster von ± 0,5 m Bogenlänge (`q3_zonen.stoss_fenster_m`) um Stoßpunkte, an denen ≥ 3 Zonen zusammenstoßen. Ausgenommen heißt: Abweichung und Knick zählen dort nicht. **Brückenrechteck-Ecken bleiben hart** (Platzhalter, wird in P5 ersetzt): Stoßpunkte mit einer Zone vom Typ in `q3_zonen.hart_typen` = [`bruecke`] bekommen kein Fenster. Alles andere bleibt hart (≤ 3 cm, ≤ 15°).
   - **Stoßpunkte:** Ringstützpunkte, an denen ≥ 3 verschiedene Zonen-Polygone innerhalb `q3_zonen.stoss_tol_m` = 0,01 m liegen; Kandidaten < 5 cm zu einem Punkt zusammengefasst. Die Liste (x, z, Zonen-IDs, Typen, ausgenommen/hart) steht in `werte.zonen_stosspunkte` und wird von `pruefe_alle.py` ausgegeben. Jeder Rest-Befund trägt eine Gruppe: `kartenrand_nah` (≤ 1 m am Rand, aber nicht darauf), `bruecke` (Brückenzone oder ≤ 1 m um harten Stoßpunkt), `stoss_nah` (≤ 1 m um Stoßpunkt, außerhalb des Fensters), `sonst`.
   - **Pflicht:** Sichtprüfung bei 1,7 m in P6 an den Stoßpunkten. Ein sichtbar zackiger Stoßpunkt ist ein Befund.
   - **Selbsttest:** Kartenrand-Abschnitt und Kartenecke ausgenommen; Stoßpunkt-Fenster ausgenommen; Buckel 5 cm bei 0,65 m Bogenlänge vom Stoßpunkt gefunden (4,3 cm / 53°); Brückenecke bleibt hart (90° gefunden).
   - **Gegenprobe** auf den aktuellen Zonen (art/dorfmap-fertig aa78160, vor P1c2): 33 Stoßpunkte, davon 21 mit Fenster und 12 hart (alle an den beiden Brücken bei 175–190 | 73–130). Von 39 der 97 Ringe über Schwelle bleiben **35**. Nach Gruppe (Ort des größten Ausschlags): `kartenrand_nah` 20, `bruecke` 12, `stoss_nah` 1, `sonst` 2. Über alle Abtastpunkte über Schwelle: `sonst` 4 387, `bruecke` 433, `kartenrand_nah` 250, `stoss_nah` 124; 11 Ringe haben `sonst`-Punkte. `kartenrand_nah` sind die Stellen, an denen eine Zonengrenze auf den Kartenrand trifft (2 Zonen + Rand): kein Abschnitt auf dem Rand und kein Stoß von ≥ 3 Zonen, bleiben nach der Entscheidung also hart. Die Zonen erzeugt P1c2 neu; die Gegenprobe wird am neuen Stand wiederholt.
2. **F12 – Q14 ausgelassene Weg-Teilstücke.** Neue Ausnahme **A-DV2-02** in `AUSNAHMEN_DV2.md`: G002_anb/0 (256,5 | 131,5), G008/2 (301,5 | 186,5), G010/2 (180,5 | 75,5), G014/1 (186,5 | 127,5). Jedes Stück ist ein einzelner Stützpunkt, Länge je 0,00 m. Drei liegen in Kreuzungen (K082; K023/K025; K040), G002_anb/0 liegt 5,70 m neben der nächsten Kreuzung, alle vier im Wegnetz. Quelle ist `meta.verfahren.ausgelassen` von P1a. **Bedingung:** gilt nur, wenn in P6 bei 1,7 m keine sichtbare Lücke im Wegnetz entsteht, sonst müssen die vier wieder rein. Q14 führt sie über konfig `q14_ausnahmen` als Befund mit `ausnahme: A-DV2-02` (nicht blockierend, `werte.wege_ausnahme`); alle anderen fehlenden oder abweichenden Wege bleiben hart. Selbsttest: `Q14_ausnahme` (gelistetes Stück fehlt → ok mit Ausnahme-Befund), `Q14_fehlt` (nicht gelistetes Stück fehlt → fehler). Gegenprobe aa78160: `wege_fehlend` 0, 4 Ausnahmen, Hausdorff max 0,249 m.
3. Zeitangabe Runde 3 korrigiert (Ende 18:22 statt 18:23).

Selbsttest Runde 4: **56 Fälle BESTANDEN** (95–100 s).

**Runde 5 (Entscheidung Grundgerüst, eingearbeitet 19.11. ab 18:39 MEZ, Basis 748bafe; Zonen aus #61 `art/dv2-zonen2` @ 5dabe976, nicht gemergt, nur gelesen):**

1. **Q14 Bauzone im Zellformat.** Ab #61 ist die Bauzone in `zonen.geojson` eine Punkt-Logikschicht: 25 Komponenten (`layer=bauzone_plan`, Geometrie Point) mit `zellen` [[cx, cy], …] und `flaeche_m2`, zusammen 31 893 Zellen; Slots sind gleich aufgebaut. Q14 erkennt das Format an `properties.zellen`. Geprüft wird: Zellsumme = Soll (konfig `bauzone.zellen_soll` = 31 893), keine Zelle doppelt, `flaeche_m2` = Zellzahl je Komponente und Zellmenge deckungsgleich mit `bauzone.zellen_csv` = `../neu/zellen_relief.csv` (Spalten `cx`, `cy`, `bauzone_plan` ≠ 0). Abweichungen werden mit Anzahl und bis zu 20 Zellen genannt (fehlend / zusätzlich). Fehlt die CSV → Status `offen` („Eingabe fehlt“). Ohne `zellen` bleibt die alte Flächenvariante als Rückfall (± 1 % gegen 31 927 m²).
2. **Bauzone und Slots nie in Q3.** Q3 prüft nur sichtbare Geometrie: Flächentyp, Untergrund, Kanten, Grat und alle Linien. konfig `q3_ausschluss.layer` = [`bauzone_plan`, `slot`] gilt für jede Q3-Quelle (auch ohne Layer-Filter). Neu als Q3-Quelle: `zonen.geojson` `layer=untergrund`, mit denselben Zonenring-Regeln wie `flaechentyp` (Stoßpunkte je Layer).
3. **F13 – Kartenrand-Stoß.** Wo 2 Zonen auf den Kartenrand treffen, ist das ein Stoßpunkt (Zone, Zone, außerhalb): Es gilt das ± 0,5-m-Fenster, der Punkt steht in der Stoßpunktliste (`kartenrand: true`, Zonen inkl. `ausserhalb`) und gehört zur Sichtprüfung bei 1,7 m. Brücken-Stoßpunkte bleiben hart.
4. **Selbsttest:** `Q14_zellen` (2 Komponenten + Slot-Punkt, deckungsgleich → ok), `Q14_zelle_fehlt` (1 Zelle fehlt → fehler mit Zelle), `Q3_logik` (zackige Slot-/Bauzonen-Polygone, Q3-Quelle ohne Filter → ausgeschlossen, ok), F13 (Kartenrand-Stoß im Fenster ausgenommen; mit Brücke hart). **61 Fälle BESTANDEN** (105 s).
5. **Gegenprobe Zonen 5dabe976** (übrige Vektoren aa78160), Details in `gegenprobe/R5_zonen_5dabe976.md`:
   - Stoßpunkte 117 (flaechentyp 61, untergrund 56), mit Fenster 105, hart 12 (Brücken), am Kartenrand (F13) 48.
   - Q3-Rest: 17 Ringe (alle `flaechentyp`, `untergrund` 0). Nach Gruppe (Ort des größten Ausschlags): `bruecke` 13, `sonst` 3, `stoss_nah` 1, `kartenrand_nah` 0. Abschnitte über Schwelle: `sonst` 98, `bruecke` 40, `stoss_nah` 13.
   - **Abweichung von der Erwartung (0 „sonst“, 0 Brückenecken):** Die 40 Brückenabschnitte sind die Rechteck-Ecken der Brücken bei 175–190 | 73–130 (bis 24,2 cm / 141°; Ringe flaechentyp_00007/08/09 Brücke, 00010/00012 Weg, 00015–00018 Ufer, 00052/54/55/56 Grund). Alle 98 `sonst`-Abschnitte liegen ≤ 3 m an einem Mittellinien-Ende (Median 1,3 m), also an runden Wegenden (Kandidat A-DV2-01): 3,0–4,8 cm, Knick ≤ 11°, Ringe 00010/11/12 (Weg), 00015/18 (Ufer), 00037 (Fels), 00052/54/56/58 (Grund).
   - Q14 Bauzone: 25 Komponenten, 31 893 Zellen, 0 doppelt, deckungsgleich mit `neu/zellen_relief.csv` (0 fehlend, 0 zusätzlich).

**Runde 6 (Entscheidung Grundgerüst, eingearbeitet 19.11. ab 18:48 MEZ, Basis a60ea22 + Merge origin/art/dorfmap-fertig bf9f62d mit #61):**

1. **F14 – Brücken bis P5 offen.** Die Q3-Abschnitte der Gruppe `bruecke` (Brückenrechteck = Platzhalter) zählen bis P5 als **offener Befund „P5“**: Befund mit `offen: P5`, Q3-Status `offen`, wenn sonst nichts reißt. Das ist weder eine Ausnahme noch ok. `werte.bruecke_offen_p5` listet die Ringe. Nach P5 wird neu gemessen.
   - **P5-Regel vorbereitet** (konfig `q3_bruecke_p5`, `aktiv: false` bis das Brückenmodell da ist): Die Deckenden sind echte Baukanten. Die 4 Ecken je Brücke (kleinstes gedrehtes Rechteck der Brückenfläche, Quelle `datei`/`filter`, nach P5 auf das Modell umstellbar) sind im Fenster ± 0,5 m frei, wie Kreuzungspolygone. Längsseiten und alles andere bleiben hart, und mit `aktiv` gibt es keinen P5-Status mehr. `befreit` = [`knick`, `abw`]: Im Eckfenster sind Knick **und** Abweichung frei, weil eine 90-Grad-Ecke sonst über die Abweichung (≈ 18 cm) weiter reißt. Soll nur der Knick frei sein, genügt `befreit: ["knick"]` (Rückfrage an Grundgerüst).
2. **F15 – Wegenden unter A-DV2-01.** Die 98 Abschnitte (3,0–4,8 cm, ≤ 3 m vor Wegende) stehen in `AUSNAHMEN_DV2.md` unter A-DV2-01, je Ring zusammengefasst mit Verweis auf `gegenprobe/R5_zonen_5dabe976.md`. Bedingung: Sichtprüfung bei 1,7 m; sind sie sichtbar, bekommen die Wegenden im Mesh (P2) eine andere Endgeometrie. Q3 führt sie eng begrenzt als Ausnahme (konfig `q3_wegenden`): nur Gruppe `sonst`, und nur der ganze Abschnitt (zusammenhängend, gleiche Gruppe, 1 Abtastpunkt Lücke erlaubt), wenn er vollständig ≤ 3,0 m vor einem Mittellinien-Ende liegt UND die Abweichung ≤ 4,8 cm UND der Knick ≤ 15° ist. Alles andere bleibt hart. `werte.wegenden_ausnahme` zählt Abschnitte je Ring.
3. **stoss_nah (13 Abschnitte, 6 Ringe):** Alle liegen **außerhalb** des ± 0,5-m-Fensters (kürzester Bogenabstand zum Stoßpunkt 0,502–0,851 m; jeder Abschnitt beginnt direkt hinter der Fenstergrenze). Die Fensterlogik ist korrekt: Im Selbsttest F11/F13 hinterlässt eine 90-Grad-Ecke außerhalb des Fensters keinen Rest. Alle 13 liegen 0,96–1,48 m vor einem Wegende: Dort beginnt die runde Wegend-Kurve direkt am Stoßpunkt. **Befund für P1c.** Sie bleiben hart (nicht unter F15, weil nur die Gruppe `sonst` freigegeben ist). Liste: `gegenprobe/R6_zonen_bf9f62d.md`.
4. **Gegenprobe gemergter Stand bf9f62d** (Zonen = 5dabe976). Q3-Zonenringe (Vektor) nach Gruppe:

   | Gruppe | Ringe | Abschnitte | Behandlung |
   |---|---|---|---|
   | `bruecke` | 13 | 40 | offen P5 |
   | `sonst` (Wegenden) | 10 | 98 | Ausnahme A-DV2-01, 0 Rest |
   | `stoss_nah` | 6 | 13 | hart, Befund P1c |
   | `kartenrand_nah` | 0 | 0 | – |

   Weitere Ergebnisse:
   - 117 Stoßpunkte.
   - Q14-Bauzone deckungsgleich.
   - Q3 gesamt am alten Mesh `fehler`: Wege-Mesh-Kantenzüge und die stoss_nah-Abschnitte.
5. **Selbsttest Runde 6: 67 Fälle BESTANDEN** (111 s).
   - `Q3_bruecke`: Rechteck → offen P5.
   - `Q3_bruecke_p5`: P5-Regel an → 4 Deckecken frei, ok.
   - `Q3_bruecke_p5_laengs`: Delle auf der Längsseite → fehler.
   - `Q3_wegende`: ~4,1 cm, 2 m vor Wegende → Ausnahme, ok.
   - `Q3_wegende_weit`: > 3 m → fehler.
   - `Q3_wegende_gross`: ~7 cm → fehler.

**D2-Regel** (Entscheidung New Bot 19.11.2026 über Grundgerüst) unverändert: |Δh| ≤ 1 cm an den alten D2-Vertices, Lage und Form erhalten.

**Gegenprobe altes Mesh im neuen Format** (56 Kacheln, 814 464 Dreiecke, Klasse 0, ohne UV2, `vektor/` aus #54, echte `daten/`-Module), 24,9 s gesamt:
- Q1 ok (21 s, 0 Löcher, 8 329 Duplikate verschweißt, Manifest ok inkl. Zeile 7 bis 303).
- Q7 ok (Δh 0).
- Q10 ok mit der neuen Regel (vorher wörtlich 47 754 Verstöße).
- Q11: Höhe über die echte Datenschicht 0,4 mm; Fläche/Tests fehlen noch (kein `flaeche.png`, keine Tests in diesem Abzug) → fehler wie erwartet.
- Q8 fehler wie erwartet: altes Ufer ist Treppe (bis 10,3 m Abstand, 1 531 nicht monotone Profile).
- Q9/Q14 offen (keine `wege.geojson`).
