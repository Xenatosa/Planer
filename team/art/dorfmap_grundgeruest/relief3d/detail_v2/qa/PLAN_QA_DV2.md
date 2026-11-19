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

## 2. Formatannahmen (offen, bis P2/P3/P4/P5 liefern – dann nur `konfig.json`/`welt.py` anpassen)

| Eingabe | Annahme |
|---|---|
| Mesh | `detail_v2/mesh/manifest.json` = `{format, einheit:"m", welt:[336,303], kacheln:[{id, datei, bounds:[x0,z0,x1,z1], dreiecke}]}`; je Kachel eine `.glb` in **Weltkoordinaten** (Knoten ohne Transform), y oben, 1 Einheit = 1 m. |
| Dreiecksklasse | Je Klasse ein Primitive im Mesh `gelaende`, Klasse in `extras.klasse` (Name oder Code 0–5 wie `flaeche.png`) oder Meshname `gelaende_<klasse>`. Fehlt sie: `grund`. |
| Wasser / Wände | Mesh `wasser*` bzw. `wand*` in der Kachel-GLB; Wand-Lofts alternativ `modelle/wand*.glb`. |
| UV | `TEXCOORD_0` = Welt-XZ (m), `TEXCOORD_1` = (x/336, z/303), `TEXCOORD_2` nur Weg. |
| Vektoren | `vektor/*.geojson` in Viewer-Metern (x, z). `wege.geojson`: Mittellinien `art:"mitte"` mit `id`, `breite_m` (optional `teil`), Ränder `art:"rand"`. `kreuzungen.geojson` Polygone. `wasser.geojson` Polygone mit `spiegel_m`. `ufer.geojson` Uferlinien `art:"uferlinie"`. `kanten.geojson`, `grat.geojson` Linien. `zonen.geojson` Polygone, Bauzone über `bauzone:true`. |
| Brücken | `modelle/bruecke_E2.glb`, `modelle/bruecke_E3W.glb`, Teile über Knoten-/Meshnamen: `bohle`, `traeger`, `pfosten`, `gelaender`/`handlauf`, `widerlager`/`auflager`. |
| Datenschicht | `daten/query.mjs` exportiert `queryPoint(x,z)` und optional `lade|laden|init(datenOrdner)`; Tests `daten/test/*.test.mjs`. |
| Abnahmebilder | `<ort>_clay_<h>m.jpg` mit h ∈ {1,7; 5; 12; 30} und `<ort>_wire_5m.jpg`, Orte `dorfkern 209|118`, `bruecke_e2 192|74,5`, `bach_e3 189|100`, `grat_g3 300|90`, `klippen_c3 105|110` (C3-Punkt angenommen), dazu `QUELLEN.txt`. Diese Bilder macht P6 am Sa selbst. |

## 3. Regeln: Eingabe, Messmethode, Schwelle, Ausgabe

| Regel | Eingabe | Messmethode | Schwelle (Plan Abschn. 5) |
|---|---|---|---|
| Q1 Geschlossen | Mesh `gelaende`+`wand` aller Kacheln | Verschweißen über float32-bitgleiche Positionen; Kantenzählung: keine Kante > 2 Dreiecke, Randkanten nur auf dem Außenrand der Manifest-Kacheln; Naht: Vertexmengen beider Kacheln je Schnittlinie bitgleich; Strahlscan an den 5 Orten aus 1,7 m und 5 m, 360 × 1°, 14 Neigungen (Bodentreffer 1–60 m), Schritt 5 cm, Loch = unbedeckter Kartenpunkt, an dem der Strahl unter die zuletzt gesehene Geländehöhe fällt | 0 Mehrfachkanten, 0 Innenrandkanten, 0 Nahtabweichungen, 0 Strahllöcher |
| Q2 Constraint-Treue | Constraint-Linien (konfig `constraint_quellen`), Mesh | Linie alle 5 cm abgetastet → nächste parallele Mesh-Kante (≤ 0,1 m, < 20°); zurück: Kanten mit beiden Enden ≤ 0,1 m → Abstand zur Linie; Maximum beider = Hausdorff (fehlende Kante = 9,99) | ≤ 2 cm |
| Q3 Glätte | Ränder Weg/Ufer/Kante/Grat/Zone | Stützpunkt vs. gleitende 1-m-Mittelung (an Enden symmetrisch verkürzt), Knick zwischen Nachbarsegmenten; Punkte in Kreuzungspolygonen ausgenommen (Annahme, siehe Frage 6). Grat-Silhouette: Sa per Bild (Q13) | ≤ 3 cm, ≤ 15° |
| Q4 Kreuzungen | `kreuzungen.geojson`, Mesh | Ebenen-Fit über Mesh-Vertices + 0,1-m-Abtastung im Polygon | Gefälle ≤ 2 %, Rest ≤ 2 cm |
| Q5 Dellen | Weg-Mittellinien + Breite, Mesh | 0,1-m-Höhenraster im Band 0–3 m neben dem Weg (ohne Wasser); lokale Minima (0,7-m-Fenster); Tiefe = tiefster Punkt eines 1-m-Rings minus Minimum | ≤ 3 cm |
| Q6 Wegprofil | Mittellinien, Mesh | Stationen alle 1 m: Einsenkung = Mittel der Schultern bei ±(b/2 + 0,7 m) minus Mitte; Quergefälle = Geradenfit über die Breite; Längsneigung aus Mittenhöhe. Kreuzungen (+1,5 m), Enden, Wasser (+1 m) ausgenommen | 3–5 cm, ≤ 3,5 %, ≤ 20° |
| Q7 D2 | `referenz/d2_alt.npz` (7 395 alte D2-Vertices), Mesh | Neue Geländehöhe an jedem alten Vertex (Dreiecksinterpolation); alle abgedeckt; Kachel D2 = 126–168 \| 43–86 (Umriss). Lage/Form: eine verschobene Form erzeugt Δh an den alten Vertices (Selbsttest: 0,6 m Wegversatz → 3,7 cm) | \|Δh\| ≤ 1 cm (neue D2-Regel, s. o.) |
| Q8 Ufer | `wasser.geojson` (`spiegel_m`), `ufer.geojson`, Mesh | Exakte Nullkontur (Gelände − Spiegel) aus den Dreiecken vs. Uferlinie, beidseitig; Profile alle 10 cm, 0–2,5 m landeinwärts, enden am Wegband; monoton (1 mm Toleranz); Krone > Spiegel | ≤ 5 cm, monoton, Wasser nie über Krone |
| Q9 Netzqualität | Mesh, Constraint-Linien, Mittellinien | Kantenlänge im Grundriss je Dreieck; Band = Schwerpunkt ≤ 1,5 m von Constraint-Linie; fern = > 30 m von Wegen; Min-Winkel im Grundriss außer Dreiecken an Constraint-Ecken (Linienenden, Knicke > 10°, Schnittpunkte Linie×Linie und Linie×Kachelrand); Normale y > 0; Budgets | Kante ≤ Abstand × √2 (+1 %): Band 0,2, begehbar 0,5, fern 1,0 m (Annahme, Frage 4); Winkel ≥ 20°; ≤ 1,6 Mio. gesamt, ≤ 60 000 je Kachel |
| Q10 UV | Mesh UV0/UV1, Wände | Spiegelung = Vorzeichen UV-Fläche vs. XZ-Fläche; UV1 = (x/336, z/303) ± 1e-5; Verzerrung = \|1 − Fläche_UV0 / Fläche_3D\| bis 35° Neigung; Wände Box-UV | 0 gespiegelt, UV1 exakt, ≤ 10 % (wörtlich, Frage 5), Wände ≤ 15 % |
| Q11 Datenschicht | `daten/query.mjs`, PNGs, Mesh | Node-Harness: 10 000 Zufallspunkte (Seed 611) in den Kacheln, Brückenfußabdrücke + 1 m ausgenommen; Höhe vs. Mesh; Flächentyp vs. Dreiecksklasse (bzw. Wasser, wenn Wassermesh über Gelände); alle 6 Felder; `node --test daten/test/*.test.mjs` | ≤ 2 cm, ≥ 99,5 %, Tests grün |
| Q12 Brücken | `modelle/bruecke_*.glb`, Mesh | Teile über Namen; Spalt = Auflager-Unterkante − Gelände; Stufe = Deckoberkante am Ende vs. Gelände 15 cm davor; Geländer 1,0 ± 0,1 m | Bohlen, Träger, Pfosten, Geländer, Auflager; Spalt ≤ 2 cm; Stufe ≤ 5 cm |
| Q13 Abnahmebilder | `--abnahme` Ordner | 5 Orte × 4 Höhen Clay + 5 × Wire 5 m; JPEG; Qualität aus Quantisierungstabelle ± 2; jeder Name in `QUELLEN.txt` | 25 JPG q90 + QUELLEN.txt |
| Q14 Layout | `referenz/referenz_alt.json`, Vektoren | Hausdorff je Weg-ID (`id[/teil]`) alt vs. neu; Wasserfläche = Vereinigung `wasser.geojson`; Bauzone = Vereinigung Bauzonen-Polygone | ≤ 0,3 m; ±3 %; ±1 % |

## 4. Stand Do 19.11. (Selbsttest)

Alle 14 Regeln als Skript fertig und selbstgetestet: Der saubere Dummy besteht alle 14, jede der 16 Fehlervarianten reißt ihre Regel. Dazu Exit 2 bei fehlenden Eingaben, Exit 1 bei Fehler und 3 Kurven-Einheitstests (Kreis glatt, Zickzack und 90°-Ecke erkannt). Details: `selbsttest/ERGEBNIS_SELBSTTEST.md`.

Skalierungstest: Das alte Mesh (56 Kacheln, 814 464 Dreiecke) wurde ins angenommene Format umgeschrieben. Q1 läuft in 24 s (1,22 Mio. Kanten, 0 Löcher, 50 400 Strahlen), Q7 ergibt Δh 0 (alt = alt).
Q10 wörtlich: 47 754 Dreiecke > 10 % Verzerrung. Das belegt den Widerspruch in Frage 5.

Grenzen des Dummys: Constraint-Linien liegen achsparallel auf dem 0,2-m-Raster, gekrümmte Linien sind nur über die Einheitstests abgedeckt. Q10-Wände sind ohne Dummy, weil P5 sie erst Sa liefert.

## 5. Tagesziele

| Tag | Ziel | Fertig wenn |
|---|---|---|
| Do 19.11. bis 23:59 | Plan, alle 14 Skripte, Runner, Alt-Referenz, Dummy und Selbsttest. Draft-PR. | Selbsttest BESTANDEN ✔ |
| Fr 20.11. bis 17:00 | Formatabgleich mit P2 (Mesh/Manifest), P3 (Viewer-API), P4 (query.mjs, Legende), P1 (GeoJSON-Attribute); `konfig.json`/`welt.py` anpassen, Selbsttest erneut. Erster Lauf gegen das erste echte Mesh (~10–12 Uhr), Bericht-JSON und Befundliste an Grundgerüst und P2. | Lauf ohne Prüfer-Ausnahme, jede Regel ok/fehler mit Ort |
| Sa 21.11. bis 19:00 | Messung Q1–Q14 auf dem Abgabestand; Clay-Bilder 1,7/5/12/30 m an den 5 Orten und je 1 Wire aus 5 m mit dicken Linien über die Viewer-Testkamera-API (`__test.kam`), JPG q90 nach `/workspace/dorfmap_final/detail_v2/abnahme/` mit QUELLEN.txt (ehrlich); Grat-Silhouette Q3 per Bild; `AUSNAHMEN_DV2.md` nach Abschnitt 6 (16 „muss weg“, A6 bleibt, A12 bedingt an Q8, A5/A16 klären). | Q13 ok, Bericht mit Befunden |
| So 22.11. bis 18:00 | Nachprüfung nach Nachbesserung, Endbericht | Gesamt-JSON Exit 0 oder ehrliche Ausnahmeliste |

## 6. Risiken

1. **Formatabweichung** von P2/P4 (Klassen, Manifest, Wasser/Wände): Annahmen sind zentral in `konfig.json`/`welt.py` gekapselt, Anpassung ≤ 1 h. Selbsttest danach neu.
2. **Schwellen-Widersprüche im Plan** (Q9-Kantenlänge, Q10-Verzerrung, Q3-Knick an Weg-Einmündungen) führen zu Fehlalarmen auf korrektem Mesh. Deshalb Klärung bis Fr 10:00 (Fragen 4–6).
3. **Wasser-Referenz** für ±3 % ist mehrdeutig: DS > 0 ergibt 6 338 m², WV-Punkte 6 461 m², WASSER_EIS-Zellen 6 912 m², vektor.json 6 695 m². Die Spanne beträgt 9 %. Standard: DS > 0 (wie P1b-Verfahren).
4. **Laufzeit:** Auf 0,8 Mio. Dreiecken dauern alle Regeln < 1 min. Bei 1,6 Mio. erwartet ~2–3 min, unkritisch.
5. **Erstes Mesh verspätet** (Fr ~10–12 Uhr): Dann Lauf am Teilstand (Manifest mit den vorhandenen Kacheln; Q1 wertet Ränder nur am Außenrand der vorhandenen Kacheln).

## 7. Offene Fragen an Grundgerüst

1. Mesh-Format/Manifest-Schema, Klassenkodierung je Dreieck, Ort von Wasser- und Wandmesh (Annahme Abschn. 2) – bitte von P2 bestätigen oder Schema nennen.
2. Pfad und Uhrzeit des ersten echten Mesh (Annahme `relief3d/detail_v2/mesh/` auf `art/dv2-mesh`, Fr ~10–12 Uhr).
3. `query.mjs`: Init-Funktion und Pfad der Tests; GeoJSON-Attribute (`art` mitte/rand/uferlinie, `spiegel_m`, Bauzone-Attribut `bauzone` vs. `bauzone_plan`).
4. Q9: „Kante ≤ 0,2 m / ≤ 0,5 m“ ist bei Punktabstand 0,2/0,5 m mit Delaunay nicht erfüllbar (Diagonale 0,28/0,71 m). Umgesetzt als Punktabstand × √2 (+1 %) im Grundriss. Der Fernbereich 1,0 m (Plan 3.2) ist ausgenommen. Bitte bestätigen.
5. Q10: „Verzerrung ≤ 10 % bis 35°“ widerspricht UV0 = Welt-XZ, denn 1/cos 35° = 1,22, also schon ab 25,8° über 10 %. Am alten Mesh sind das 47 754 Dreiecke. Gemeint sind entweder ≤ 25° oder ≤ 22 % bis 35° oder Triplanar ab 25°. Bitte entscheiden. Bis dahin wird wörtlich gemessen und gemeldet.
6. Q3: Weg-Einmündungen ergeben als Union der Bänder 90°-Ecken. Annahme: Punkte innerhalb Kreuzungspolygonen sind vom Knick ausgenommen (P1a passt Kreuzungen ein). Bitte bestätigen.
7. Wasser-Referenz für Q14 (siehe Risiko 3): DS > 0 auf dem 0,5-m-Raster?
8. Der Ort „Klippen C3“ hat keine Koordinate im Plan. Annahme 105|110.
