# DETAIL_V2_PLAN – Dorfmap als Vektor-Geometriemodell (Laufkamera 1,7 m)

Stand 19.11.2026, ca. 15:00 Europe/Berlin. Basis: `art/dorfmap-fertig` @ d2d4824. Autor: Epochen Dorfmap-Grundgerüst.
Vorgaben von Fabian: t2039u (Abnahme abgelehnt), t2040u (nur Geometrie, keine Texturen), t2042u (Datenschicht, Frist), t2043u (Methodenwechsel).
**Frist: So 22.11.2026, 18:00 Europe/Berlin.** Kosten 0 €. Codex: nur ein Lauf gleichzeitig, je höchstens ~2 h. Scheitert eine Stelle zweimal, wird sie vereinfacht.

## 1. Ziel

- EIN durchgehendes Gelände-Mesh. Es wird prozedural aus **Vektoren** gebaut, nicht aus dem Raster Kachel für Kachel. Erst danach wird es in die 56 Kacheln (A–H × 1–7) zerschnitten.
- Kanten folgen geglätteten Splines: Wege, Bachufer, Grat, Klippen und Zonen. Keine Zacken, Risse oder Löcher.
- Die Polygonauflösung reicht für eine Laufkamera auf 1,7 m.
- Saubere UVs. Später kommen Texturen wie ein Teppich darüber. **Im Projekt selbst gibt es keine Texturen, Platzhalter-Texturen oder Splat-Masken (t2040u).**
- Echte Brücke E2 als Modell mit Planken, Geländer und Auflager. Die E3-Brücke West wird mit demselben Modul gebaut.
- Eine Datenschicht passend zum Mesh: Höhe, Flächentyp, begehbar, Slot und Kachel-ID. Dazu Masken-PNGs, eine JSON-Legende und `queryPoint(x,z)` mit Tests.
- Nachweis mit Clay- und Wireframe-Renderbildern aus 1,7 m, 5 m, 12 m und 30 m an fünf Orten: Dorfkern, Brücke E2, Bach E3, Grat G3 und Klippen C3.
- Ablage: `/workspace/dorfmap_final/detail_v2/`.
- **Entscheidung New Bot, 19.11.2026:** „D2-Bereich: Lage und Form erhalten, |Δh| ≤ 1 cm an den alten D2-Vertices“ ersetzt „D2 bitgleich“. Alte Dateien und Hashes bleiben unverändert. [F über New Bot]
- **Plan freigegeben durch New Bot 19.11.2026;** Plan B (0,25-m-Gitter mit Snapping) nur bei verfehltem Tagesziel und mit sofortiger Meldung an New Bot.

## 2. Ausgangszustand (gemessen, d2d4824)

- **Maßstab.** 1 Viewer-Einheit = 1 Zelle = 1 m (3D). Achtung: `neu/vektor.json` rechnet mit 1,2 m pro Zelle (`zellweite_m`). Beim Übernehmen durch 1,2 teilen.
- **Gelände.** Ein regelmäßiges Höhengitter `GB` mit 0,5 m Abstand (rs = 2, Gitter 673 × 607). Jede der 56 Kacheln hat 7 395 Vertices und 14 448 Dreiecke. Gesamt sind es 814 464 Oberflächendreiecke mit fester Diagonale. Die Dichte ist überall gleich, auch an Wegen und Bächen, nicht feiner.
- **Wände.** Getrennte Wandkörper je Kachel (`neu/wand.py`) mit eigenen Normalen.
- **Farbe.** Vertex-Farbe `VC` je Gitterpunkt, also 0,5 m.
- **UVs.** Die Kachelmeshes haben keine UVs, nur Positionen und Indizes. Die alte GLB hat TEXCOORD_0 über die ganze Karte. Objekte haben keine UVs.
- **Wege.** Es gibt keine Geometrie. Wege sind nur ein transparentes Farb-Overlay aus `WEGA`: Alpha je 0,5-m-Gitterpunkt, 28 513 Punkte > 0. Im Clay-Render ist der Dorfkern deshalb eine völlig ebene Fläche ohne jede Wegkante. In einigen Kacheln senkt das Wegprofil `+wegprofil` die Höhe nur leicht ab.
  - **Ursache A19:** Der Wegrand ist die Alpha-Treppe des 0,5-m-Rasters. Die Randlinie weicht bis zu 0,24–0,27 m von einer glatten Kurve ab.
  - Vektoren gibt es schon: `neu/vektor.json` → `wege` hat 62 Mittellinien mit `breite_m`, Klassen GASSE 42, ANBINDUNG 11 und HAUSWEG 9. Dazu kommen 88 `kreuzungen`-Polygone.
- **Wasser.** Wassermaske/Spiegel `WV` mit 25 845 Gitterpunkten, 4 018 davon am Rand. Das Wassermesh endet an den Maskenpunkten (Ring 1–3). An steilen Ufern verläuft die Wasserkante deshalb als **Treppe im 0,5-m-Raster**: an E2 klar sichtbar mit Stufen bis ~0,5–1 m, an E3 kleiner. Die E3-Uferstufe (A20) hat 0,31 m pro Zelle.
- **Grat G3/H3 (A18).** Eine steile Kante mit 70–74° liegt schräg zum festen 0,5-m-Gitter mit fester Diagonale. Pro Zelle springt die Höhe um bis zu ~1,2 m (K5b-Facetten). An der Krone entsteht so ein Sägezahn-Saum (0,69 m / 73,5° bei 300|90). Glätten Punkt für Punkt (L3k/L3l) behebt nur einzelne Stellen.
- **Brücken.** Es gibt zwei Brücken: E2 (x 186–197, z 73–75, 25 Boxen) und E3-West (x 174–186, z 126–128, 27 Boxen). Beide bestehen nur aus Boxen 1 × 0,25 × 1 m auf y = 0,3, also einer flachen, schwebenden Platte.
- **Zellendaten** (`zellen_relief.csv`, 101 808 Zellen à 1 m², 51 Spalten). Vorhanden sind `untergrund` (SCHNEE 79 045, WALD, WASSER_EIS, FELS, KLIPPE_WAND/KANTE, BODEN, SAND), `begehbar`, `begehbar_3d`, `bebaubar`, `bauzone_plan` (31 927), `klippe` (WAND, WAND_FUSS, WAND_OBEN), `wand_name`, `ufer` (4 076), `fluss_id`, `wasserspiegel_m`, `deko_baum_ok`, `deko_fels_ok` und `skin_slot`.
- **Weitere Daten.**
  - `raster_c20_z25_overlay_plaetze_wege.csv`: zone A–E, platz, bauplatz 3 292, weg_klasse, hof, feuer, bruecke, dekoplaetze_netz 627.
  - `overlay_plaetze_erweiterung.json`: Plätze/Bauplätze.
  - `vektor.json`: `bauzonen` (Polygone), `wasser` (60 Zellpolygone, Treppenform), `waende` (260).
- **Ausgangs-Clay-Bilder.** Einfarbig, Licht und Schatten an. Sie liegen in `/workspace/dorfmap_final/detail_v2/ausgang/`: Dorfkern, E3 und E2, je aus 1,7 m und 5 m, plus ein Wireframe von E3 aus 5 m. Das Wireframe ist zu schwach, um die Linien zu erkennen. Dazu `render.js` und `log.json`.
- **Werkzeuge auf der Box, alle kostenlos.**
  - Python: numpy 2.5, scipy 1.18, shapely 2.2 (GEOS 3.14, mit `constrained_delaunay_triangles`), scikit-image 0.26, OpenCV 5, trimesh 5.2, pygltflib, Pillow.
  - Node 24 mit three.js und playwright (`/tmp/w3/node_modules`).
  - `pip triangle` wäre installierbar, wird aber **nicht** genutzt: Die Lizenz verbietet die Nutzung in kommerziellen Produkten ohne Lizenz.
  - Blender ist nicht installiert. Es ist kostenlos (GPL, die Ausgaben sind frei) und nur Ausweichweg (~350 MB). Die Platte hat jetzt 45 GB frei.

## 3. Methode

### 3.1 Vektor-Extraktion (Do)

Alle Vektoren kommen als GeoJSON in Viewer-Metern nach `relief3d/detail_v2/vektor/`. Das Layout bleibt inhaltlich gleich.

| Linie / Fläche | Quelle | Verfahren |
|---|---|---|
| Weg-Mittellinien und -Ränder | `neu/vektor.json` wege (`mittellinie_m`/1,2, `breite_m`/1,2), geprüft gegen `WEGA` ≥ 0,5 | Douglas-Peucker 0,05 m → Catmull-Rom (zentripetal), alle 0,25 m abgetastet. Ränder = Offset ± Breite/2 (shapely `offset_curve`, join round). Wegnetz = Union der Bänder. |
| Kreuzungen (R8) | `vektor.json` kreuzungen (88 Polygone /1,2) | Polygon auf das Bandnetz einpassen, Chaikin 2×. Ebene Höhe = Mittel der Wegmitten. |
| Wasser-/Uferlinie | `WV`/`GB` aus `index.html` (über `baue_alle_kacheln.py`-Paket) | Feld DS = Spiegel − Boden (P12c). Marching Squares (`skimage.measure.find_contours`, Level 0) → DP 0,05 m → Chaikin 2×. Bach-Mittellinien per `skeletonize`, Breite aus dem Distanzfeld. |
| Uferband | Uferlinie | Landseitig Buffer 2,5 m (Regelwerk Uferbreite ≥ 2,5 m), Böschung monoton. |
| Klippen-Ober- und Unterkante | `zellen_relief.csv` klippe = WAND_OBEN / WAND_FUSS, Neigung aus `GB` > 55°, `vektor.json` waende | Neigungsmaske 0,5 m → Konturen → DP 0,1 m → Catmull-Rom. |
| Grat-Kronen (G3/H3, B3/C3, Ostgrat, Kraterring) | `GB` | Kronenerkennung: Hessian-Eigenwert < 0 und Gradient ≈ 0 quer, `skimage` ridge → Skelett → Polylinie → glätten. Kronenhöhe längs glätten (wie L3k, aber als Kurve). |
| Zonen / Flächentypen | `zellen_relief.csv` (untergrund, bauzone_plan), `raster_c20_z25_zellen.csv` (zonen_c20), Overlay Plätze/Wege | Eine Labelkarte mit Priorität Wasser > Brücke > Weg > Ufer > Fels/Klippe > Wiese (Grund). Grenzen als gemeinsame Kanten: Konturen der weichgezeichneten Labelkarte, polygonisieren, dann mit shapely topologisch bereinigen. Keine Lücken und keine Überlappungen. |

### 3.2 Mesh (Fr)

- **Punkte.**
  - Grundraster 0,5 m.
  - In Kantenbändern ±1,5 m um jede Constraint-Linie 0,2 m.
  - Auf den Linien selbst 0,2 m Abstand.
  - Im Wegband 0,25 m.
  - Fern von Wegen bei Schnee/Fels > 30 m vom Dorf darf es 1,0 m sein.
- **Triangulierung.** Conforming Delaunay mit `scipy.spatial.Delaunay` auf allen Punkten. Die Constraint-Linien sind so dicht abgetastet, dass jede Linienkante als Dreieckskante entsteht. Danach Kantenprüfung; fehlt eine Kante, Mittelpunkt einfügen und neu triangulieren.
  - Ausweg 1: shapely `constrained_delaunay_triangles` je Zonenpolygon (Punkte als Mini-Löcher bzw. Polygon-Stützpunkte).
  - Ausweg 2: Blender headless (bmesh triangulate + remesh).
- **Höhe.**
  - Grundlage: bikubisch aus `GB`, monoton begrenzt, damit nichts überschwingt.
  - Wegband: 4 cm eingesenkt, Quergefälle ≤ 3,5 %, Rand mit 0,4 m weicher Rampe. Kreuzungen eben (R8).
  - Uferband: Böschung monoton vom Spiegel bis zur Oberkante. Die Wasserfläche reicht 1 m unter das Ufer, damit die Schnittlinie glatt ist.
  - Grat: Kronenlinie als Constraint, Höhe längs geglättet.
  - Klippen: Ober- und Unterkante als Constraint. Die Wandfläche dazwischen ist ein eigenes Wandmesh (Sa).
- **D2-Bereich** (126–168 | 43–86). Lage und Form bleiben erhalten (t2043u): |Δh| ≤ 1 cm an allen alten D2-Vertices. Die alten Dateien und ihre Hashes (ebeb46a1/6835acf2/b33d5a64) bleiben im Repo unverändert.
- **UV.**
  - UV0 = Welt-XZ in m. Der Teppich wird über den Shader-Maßstab gekachelt.
  - UV1 = (x/336, z/303) für die Datenschicht.
  - Wandmeshes: Box-Projektion in Weltmetern.
  - Wegband: zusätzlich UV2 (u = Bogenlänge in m, v = 0…1 quer).
- **Zerschneiden.** Erst am Ende in 56 Kacheln an x = 42·i, z = 43·j. Die Schnittkanten werden vorher als Constraint eingefügt, damit die Randvertices beider Seiten bitgleich sind.
- **Export.** glTF (.glb, Draco nein) je Kachel plus `manifest.json`. Budget: ≤ 1,6 Mio. Dreiecke gesamt, ≤ 60 000 je Kachel.

### 3.3 Datenschicht (Fr)

- Ordner `relief3d/detail_v2/daten/`, alles aus denselben Vektoren und demselben Mesh.
- **Raster 0,1 m/px, 3360 × 3030, Ursprung (0,0) = Weltecke.** px = x·10, py = z·10, deckungsgleich mit UV1.
  - `flaeche.png`: 8 bit indiziert: 0 Wiese/Grund, 1 Weg, 2 Ufer, 3 Fels/Klippe, 4 Wasser, 5 Brücke.
  - `begehbar.png`: 1 bit.
  - `slot.png`: 16 bit, Slot-ID.
  - `hoehe.png`: 16 bit, mit Offset/Skala aus dem Mesh gerastert.
- `legende.json` enthält:
  - Klassen und Farben.
  - Untertyp `untergrund`: Schnee, Wald, Boden, Sand.
  - Slots: Bauplätze aus Overlay `bauplatz`/`platz`, Deko aus `dekoplaetze_netz`, `deko_baum_ok` und `deko_fels_ok`.
  - Maßstab und Kachelschema.
- `query.mjs`: ESM, Node und Browser. `queryPoint(x,z)` → `{hoehe, flaeche, untergrund, begehbar, slot, kachel}`. Die Höhe wird exakt aus dem Mesh-Dreieck interpoliert (Gitterindex), die übrigen Werte aus den PNGs.
- `test/query.test.mjs`: `node --test`.

### 3.4 Modelle (Sa)

- `detail_v2/modelle/bruecke.mjs`: prozedural mit three.js, Export auch als .glb.
  - Bohlen 0,22 × 0,05 m mit 1 cm Fuge.
  - Zwei Längsträger 0,2 × 0,3 m.
  - Pfosten alle 1,5 m, Geländer 1,0 m hoch, Handlauf.
  - Steinwiderlager an beiden Enden, ins Ufer eingebunden.
  - Maße aus den Brückenzellen. E2: 12 × 3 m. Die E3-Brücke West wird mit demselben Modul gebaut.
- Klippen-/Gratwände: Wandmesh zwischen den geglätteten Ober- und Unterkanten (Loft entlang der Splines, Unterteilung 0,25 m, leichte Wölbung). Es ersetzt die alten Wandkörper.

## 4. Pakete

| Paket | Inhalt | Zuständig | Tag | Codex | Abhängig von |
|---|---|---|---|---|---|
| P0 | Aufräumen, Ausgangs-Clay, Plan | Grundgerüst | Do | nein | – |
| P1a | Vektoren Wege + Kreuzungen | Wege & Deko | Do bis 19:00 | nein | – |
| P1b | Vektoren Wasser, Ufer, Bach-Mittellinien | Art Umgebung | Do bis 19:00 | nein | – |
| P1c | Vektoren Grat-/Klippenkanten + Zonen-/Flächentyp-Polygone | Grundgerüst per **Codex C1** (Do 15:30–17:30) | Do | C1 | – |
| P2 | Durchgehendes Mesh + UV + Zerschneiden + Export | Art Umgebung, Kern per **Codex C2** (Fr 07:30–09:30) | Fr | C2 | P1a–c |
| P3 | Viewer v2: Laufkamera 1,7 m (WASD/Touch), Clay/Wire-Schalter, lädt manifest.json | Dev UI | Fr | nein | P2-Format (Fr 10:00) |
| P4 | Datenschicht: Masken + legende.json + query.mjs + Tests | Tools (Rechner hilft bei Slots), Ausweg **Codex C3** (Fr 11:00–13:00) | Fr | C3 opt. | P1, P2 |
| P5 | Brücken E2/E3-West, Grat-/Klippenwände | Art Umgebung, Ausweg **Codex C4** (Sa 08:00–10:00) | Sa | C4 opt. | P2 |
| P6 | Neue Prüfregeln + Prüfskripte (Fr), Messung + Clay-Abnahmebilder (Sa) | QA | Fr–Sa | nein | P2, P3, P5 |
| P7 | Kritiker 10/10, Aufseher-JA, Merges, Lieferung | Kritiker, Aufseher, Grundgerüst | So bis 15:00 | Reserve **C5** Sa 14:00–16:00 | alles |

Jedes Paket schreibt nur in seinen eigenen Ordner `relief3d/detail_v2/<paket>/`, damit es keine Merge-Konflikte gibt. Merge über PR auf `art/dorfmap-fertig` nach Aufseher-JA. Nichts geht nach main.

## 5. Abnahmekriterien (messbar, QA-Paket P6)

Fabian hat die Methode gewechselt (t2043u). Das alte Raster-Gate (Referenz 359 / R8 31 / R9 321, W1 0, Loch 0) wird für das neue Mesh deshalb durch diese Regeln **ersetzt**. Die alten Prüfer bleiben unverändert im Repo und werden nicht gelockert.

| Nr | Regel | Schwelle |
|---|---|---|
| Q1 | Löcher/Risse | Jede innere Kante gehört zu genau 2 Dreiecken. Kachelschnitt-Vertices bitgleich. Strahl-Lochscan aus 1,7 m und 5 m (alle 5 Orte, 360°): 0. |
| Q2 | Kantenabweichung zum Spline | Hausdorff(Mesh-Constraint-Kanten, Spline) ≤ 2 cm. |
| Q3 | Zackenamplitude | Abweichung jeder Kante (Weg, Ufer, Grat, Klippe, Zone) von ihrer 1-m-Glättung ≤ 3 cm. Knick zwischen Nachbarsegmenten ≤ 15°. Grat-Silhouette aus 1,7 m und 5 m ohne Sägezahn. |
| Q4 | Kreuzungen eben (R8) | Quergefälle in jedem Kreuzungspolygon ≤ 2 %, Höhenrest ≤ 2 cm. |
| Q5 | Keine Dellen neben Wegen | Im Band 0–3 m neben dem Weg kein lokales Minimum tiefer als 3 cm. |
| Q6 | Wegprofil | Einsenkung 3–5 cm, Quergefälle ≤ 3,5 %, Längsneigung ≤ 20°. |
| Q7 | D2 Lage und Form | |Δh| ≤ 1 cm an allen alten D2-Vertices; Umriss gleich. |
| Q8 | Ufer | Schnittlinie Wasser/Gelände ↔ Uferspline ≤ 5 cm. Böschung monoton, Wasser nie über der Uferkrone. |
| Q9 | Dreiecke | Begehbar: Kante ≤ 0,5 m. Kantenbänder ≤ 0,2 m. Min-Winkel ≥ 20° (außer an Constraint-Ecken). Oberflächen-Normalen nach oben. ≤ 1,6 Mio. Dreiecke. |
| Q10 | UV | 0 gespiegelte UV-Dreiecke. UV1 eindeutig. Verzerrung ≤ 10 % bis 35° Neigung (Wände per Box-UV ≤ 15 %). |
| Q11 | Datenschicht ↔ Mesh | `queryPoint` Höhe vs. Mesh-Strahl ≤ 2 cm an 10 000 Zufallspunkten. Flächentyp = Dreiecksklasse ≥ 99,5 %. Tests grün. |
| Q12 | Brücke | Bohlen, Geländer und Auflager vorhanden. Spalt zum Gelände ≤ 2 cm. Stufe Weg↔Brücke ≤ 5 cm. |
| Q13 | Abnahmebilder | 5 Orte × 4 Höhen (1,7 / 5 / 12 / 30 m) Clay plus je 1 Wireframe aus 5 m. Ehrlich, ohne Schönen. JPG q90 unter `detail_v2/abnahme/`. |
| Q14 | Layout gleich | Weg-Mittellinien ≤ 0,3 m vom alten Verlauf. Wasserfläche ±3 %. Bauzone ±1 %. |

Zu Q7: Entscheidung New Bot, 19.11.2026: „D2-Bereich: Lage und Form erhalten, |Δh| ≤ 1 cm an den alten D2-Vertices“ ersetzt „D2 bitgleich“. Alte Dateien und Hashes bleiben unverändert. [F über New Bot]

## 6. Ausnahmeliste neu bewertet (Bodenkamera 1,7 m, Clay)

Im Clay sieht man jede Form, Farbe verdeckt nichts mehr. Der Neubau aus Vektoren muss die Raster-Befunde beseitigen. Nachweis über Q1–Q9 an derselben Stelle.

| # | Ort | alt | neu | Begründung |
|---|---|---|---|---|
| A1 | G6-Facette E3 189,5\|119,5 | 0,14 m / 32,6° | muss weg | Rasterfacette, aus 1,7 m sichtbar; entfällt durch Neubau |
| A2 | rampe_4-Unterrand 268\|242 | 0,47 m / 46° | muss weg | Kante am Rampenfuß, begehbar |
| A3 | E3-Brücke West 175\|128 | 0,25 m / 46,5° | muss weg | Brückenanschluss, wird durch das Brückenmodell ersetzt |
| A4 | T37 D1 147\|21 | 0,37 m / 57,9° | muss weg | 37-cm-Stufe aus 1,7 m klar sichtbar |
| A5 | C5 107,8\|183,8 | 0,25 m / 60,8° | unklar | Hang abseits der Wege; im Neubau messen |
| A6 | D3 147\|107 | 0,0 m | bleibt | Kein Formbefund, nur Gate-Artefakt |
| A7 | X084-Kreuzung | 0,64 m / 65,8° | muss weg | Kreuzung muss eben sein (R8) |
| A8 | X084-Kehre | 0,89 m / 66,1° | muss weg | Begehbarer Weg |
| A9 | X084-Steilstück | 0,46 m / 51,3° | muss weg | Begehbarer Weg, Längsneigung |
| A10 | Naht C4\|D4 | 0,32–0,95 m | muss weg | Entfällt im durchgehenden Mesh, Q1/Q3 |
| A11 | G6-Krone 283\|226 | 0,19 m / 56,6° | muss weg | Kronenzacke → Kantenspline |
| A12 | G7 260\|270 Uferböschung | 0,23 m / 47° | bleibt (bedingt) | Echte Böschung, keine Zacke; gilt, wenn Q8 erfüllt |
| A13 | rampe_4 256/282 | 0,11–0,39 m | muss weg | Rampenkante |
| A14 | Nähte x=84, z=43 | 0,05–0,10 m | muss weg | Entfällt im durchgehenden Mesh |
| A15 | Mulde C2 | 0,46 m / 59,9° | muss weg | Delle |
| A16 | G1 273,4\|21,2 | 0,22 m / 34° | unklar | Prototyp-Kachel; im Neubau messen |
| A17 | G1 Clay-Ring | 0,04 m / 9,4° | muss weg | Im Clay sichtbar, und Clay ist jetzt Abnahmemedium |
| A18 | Gratsaum G3/H3 | 0,69 m / 73,5° | muss weg | Grat als Kronenspline + Wandloft |
| A19 | Wegränder (Raster) | 0,24–0,27 m | muss weg | Wegband aus Splines |
| A20 | E3-Uferstufe | 0,31 m / 32° | muss weg | Uferband monoton; im Clay als Kante sichtbar |

Ergebnis: 16 müssen weg, 2 bleiben (A6, A12 bedingt), 2 sind unklar (A5, A16).

## 7. Tagesplan (vorgegeben, t2043u)

| Tag | Zwischenziel (Abendstand prüfbar) | Bericht an New Bot |
|---|---|---|
| Do 19.11. | P1a/b/c: alle GeoJSON-Vektoren (Wege, Kreuzungen, Ufer, Bach, Grat, Klippen, Zonen) geglättet. Übersichtsbild Vektoren über der alten Draufsicht. Q3 an den Vektoren gemessen. | bis 19:30, Bild `detail_v2/tag1_vektoren.jpg` |
| Fr 20.11. | P2: durchgehendes Mesh + UV + 56 Kacheln. P3: Viewer v2 mit Laufkamera. P4: Datenschicht + Tests grün. P6: Prüfregeln Q1–Q14 als Skripte. Erste Clay-Bilder 1,7/5 m. | bis 19:30, `detail_v2/tag2_clay/` |
| Sa 21.11. | P5: Brücken + Grat-/Klippenwände. P6: Messung Q1–Q14 und Clay-Abnahmebilder (20 + 5 Wire). Nachbesserung über Reserve C5. | bis 19:30, `detail_v2/abnahme/` |
| So 22.11. | Bis 12:00 Kritiker 10/10, bis 14:00 Aufseher-JA + Merges, bis 15:00 Lieferung. 15:00–18:00 Puffer. | Lieferung spätestens 18:00 |

Ein verfehltes Tagesziel wird sofort an New Bot gemeldet. Plan B, pragmatisch:

- **Fällt P2 Fr aus:** Ein Mesh auf 0,25-m-Gitter mit Vertex-Snapping auf die Splines. Die Kanten liegen dann auf den Splines, die Topologie bleibt ein Gitter.
- **Fällt P5 aus:** Brücke als einfaches, aber vollständiges Modell (Träger + Bohlen + Geländer ohne Details).

## 8. Risiken

- Die Mesh-Größe muss für Android passen. Das geht über Budget Q9 und spätere LOD; die LOD ist nicht Teil dieser Frist.
- Die alte Regel „D2 bitgleich“ ist durch t2043u in „D2-Bereich: Lage und Form erhalten“ überführt. Gemessen wird das über Q7.
- Das Kontingent ist knapp: höchstens 5 Codex-Läufe, davon 2 optional.

## 9. Auftragstexte

Alle Aufträge enthalten diese Regeln:

- Branch von `art/dorfmap-fertig` (d2d4824 oder neuer). PR auf `art/dorfmap-fertig`, nie nach main.
- Kostenzeile im PR mit Laufzeit Start und Ende (Europe/Berlin).
- Vor dem PR laufen die eigenen Prüfskripte. Dazu das alte Gate nur als Regressionsnachweis, dass alte Dateien unverändert sind; die Ergebnisse kommen in den PR.
- Platte knapp: keine großen Zwischenstände, Scratch nur in `/tmp/dv2_<paket>/`, am Ende aufräumen.
- Nur in den eigenen Ordner `relief3d/detail_v2/<paket>/` schreiben.
- Marker [S]/[A]/[R]/[F]. Keine Texturen.
- Zweimal gescheitert → vereinfachen und melden.
- D2: Lage und Form erhalten, |Δh| ≤ 1 cm an den alten D2-Vertices (ersetzt „D2 bitgleich“, Entscheidung New Bot 19.11.2026, [F über New Bot]). Alte Dateien und Hashes bleiben unverändert.
- Plan freigegeben durch New Bot 19.11.2026; Plan B (0,25-m-Gitter mit Snapping) nur bei verfehltem Tagesziel und mit sofortiger Meldung an New Bot.

**P1a an Wege & Deko** (Branch `art/dv2-vektor-wege`, heute bis 19:00):
> Neuer Aufbau der Dorfmap aus Vektoren (Fabian t2043u). Dein Teil bis heute 19:00: Weg- und Kreuzungsvektoren als GeoJSON in Viewer-Metern (1 Einheit = 1 Zelle) nach `relief3d/detail_v2/vektor/wege.geojson` und `kreuzungen.geojson`.
> - Quelle: `neu/vektor.json` → `wege[].mittellinie_m` und `breite_m`, beide durch 1,2 teilen. Dazu `kreuzungen[].polygon_m`/1,2. Abgleich gegen `WEGA` ≥ 0,5 aus `index.html`.
> - Verfahren: Douglas-Peucker 0,05 m, zentripetaler Catmull-Rom, alle 0,25 m abgetastet. Ränder als Offset ± Breite/2 (shapely). Kreuzungspolygone ins Bandnetz einpassen, Chaikin 2×. Wegenden sauber an Plätze/Kreuzungen anschließen.
> - Abnahme:
>   - Zackenamplitude jeder Randlinie gegen ihre 1-m-Glättung ≤ 3 cm, Knick ≤ 15°.
>   - Mittellinie ≤ 0,3 m vom alten Verlauf.
>   - Keine Lücken im Netz.
> - Lieferung: Skript `extrahiere_wege.py`, `test_wege.py`, Übersichtsbild (JPG, klein) über der alten Draufsicht. PR mit Messwerten. Python mit numpy/shapely/scipy, alles auf der Box vorhanden. 0 €.

**P1b an Art Umgebung** (Branch `art/dv2-vektor-wasser`, heute bis 19:00):
> Neuer Aufbau der Dorfmap aus Vektoren (Fabian t2043u). Dein Teil bis heute 19:00: Uferlinien, Uferbänder und Bach-Mittellinien als GeoJSON nach `relief3d/detail_v2/vektor/wasser.geojson`, `ufer.geojson` und `bach_mitte.geojson`.
> - Quelle: `WV` und `GB` aus dem `alle_kacheln`-Paket (`python3 pruefung/alle_kacheln/baue_alle_kacheln.py --out /tmp/dv2_wasser`).
> - Verfahren:
>   - Feld DS = Spiegel − Boden. Marching Squares (`skimage.measure.find_contours`, Level 0), Douglas-Peucker 0,05 m, Chaikin 2×.
>   - Mittellinien per `skeletonize`, Breite aus dem Distanzfeld.
>   - Uferband landseitig 2,5 m, Spiegelhöhe je Uferpunkt mitliefern.
>   - Layout inhaltlich gleich, kein Wasser entfernen. E2 und E3 besonders prüfen (dort Treppen im Ist).
> - Abnahme:
>   - Zackenamplitude ≤ 3 cm, Knick ≤ 15°.
>   - Wasserfläche ±3 % zum Ist.
>   - Polygone gültig (shapely `is_valid`).
> - Lieferung: Skript, Test, Übersichtsbild. PR mit Messwerten. 0 €.

**P1c, Codex C1, Auftrag vom Grundgerüst** (Branch `art/dv2-vektor-kanten`, Do 15:30–17:30, ≤ 2 h, gpt-6-luna/xhigh):
> Erzeuge Grat-, Klippen- und Zonenvektoren als GeoJSON in Viewer-Metern nach `relief3d/detail_v2/vektor/`.
> 1. `kanten.geojson`: Klippen-Ober- und Unterkanten aus `zellen_relief.csv` (klippe WAND_OBEN/WAND_FUSS) plus Neigung > 55° aus `GB`. Konturen, DP 0,1 m, Catmull-Rom.
> 2. `grat.geojson`: Kronenlinien aus `GB` (Hessian-Ridge, Skelett, Polylinie), Kronenhöhe längs geglättet. Pflichtstellen G3/H3 300\|90 und 290\|98 (A18), B3/C3 84\|129, Ostgrat, Kraterring G1.
> 3. `zonen.geojson`: Flächentyp-Polygone Wiese/Grund, Weg, Ufer, Fels/Klippe, Wasser, Brücke, mit Attribut `untergrund`. Dazu Bauzone (`bauzone_plan`) und Bau-/Deko-Slots (Overlay `raster_c20_z25_overlay_plaetze_wege.csv`, `overlay_plaetze_erweiterung.json`).
>    - Topologisch sauber: keine Lücken, keine Überlappungen. Priorität Wasser > Brücke > Weg > Ufer > Fels > Grund.
>    - Weg- und Wasserflächen nur als Platzhalter aus den Zellen, P1a/P1b ersetzen sie beim Mesh.
>
> Abnahme:
> - Zackenamplitude ≤ 3 cm.
> - Bauzone ±1 %.
> - `test_kanten.py` grün.
> - Übersichtsbild.
>
> Keine Änderung an bestehenden Dateien. Kostenzeile mit Start und Ende. Gate als Regressionsnachweis.

**P2 an Art Umgebung, Kern per Codex C2** (Branch `art/dv2-mesh`, Fr 07:30–09:30 Codex, danach Art Umgebung bis 17:00):
> Baue aus `detail_v2/vektor/*.geojson` EIN durchgehendes Gelände-Mesh. Skript `detail_v2/mesh/baue_mesh.py`.
> - Punkte: 0,5 m Grundraster, 0,2 m in Bändern ±1,5 m um alle Kanten und auf den Kanten, 0,25 m im Wegband, 1,0 m im Fernbereich.
> - Triangulierung: conforming Delaunay (`scipy.spatial.Delaunay`) mit Kantenprüfung. Ausweg: shapely `constrained_delaunay_triangles`. **Nicht** `pip triangle` (Lizenz).
> - Höhe:
>   - Bikubisch aus `GB`, monoton begrenzt.
>   - Wegband 4 cm eingesenkt, Quergefälle ≤ 3,5 %, Kreuzungen eben (R8), keine Dellen daneben.
>   - Uferband monoton, Wasserfläche 1 m unter das Ufer geführt.
>   - Grat-Kronenlinie als Constraint.
>   - D2-Bereich: |Δh| ≤ 1 cm an den alten D2-Vertices.
> - UV0 = Welt-XZ (m), UV1 = (x/336, z/303), UV2 im Wegband (Bogenlänge, quer 0–1).
> - Erst zum Schluss in 56 Kacheln schneiden, Schnittlinien vorher als Constraint, Randvertices bitgleich.
> - Export: `.glb` je Kachel plus `manifest.json`. Budget ≤ 1,6 Mio. Dreiecke, ≤ 60 000 je Kachel.
> - Abnahme: Q1, Q2, Q4–Q7, Q9, Q10 aus DETAIL_V2_PLAN.md Abschnitt 5.
> - Clay-Bilder 1,7 m und 5 m an Dorfkern und E3 nach `/workspace/dorfmap_final/detail_v2/tag2_clay/`.
> - Ausweg bei zweimaligem Scheitern: 0,25-m-Gitter mit Vertex-Snapping auf die Splines.

**P3 an Dev UI** (Branch `art/dv2-viewer`, Fr bis 17:00):
> Viewer v2 für das neue Vektor-Mesh in `relief3d/detail_v2/viewer/` (eigene HTML, alte Viewer unverändert).
> - Lädt `detail_v2/mesh/manifest.json` und die Kachel-.glb.
> - Laufkamera auf 1,7 m über Grund (WASD + Maus, Touch: linker Stick laufen, rechts schauen), Bodenhaftung über `queryPoint` bzw. Strahl.
> - Orbit-Modus ohne 25-m-Grenze.
> - Schalter `?clay=1` (einfarbig, Licht und Schatten an), `?wire=1`, `?kachelrand=1`.
> - Testkamera-API `__test.kam(p, t)` und `__test.lauf(x, z, blickrichtung)` für die QA-Bilder.
> - Schattenkarte folgt der Kamera.
> - Bis Fr 10:00 mit Dummy-Mesh im vereinbarten Format beginnen.
> - Abnahme: läuft in HeadlessChrome/SwiftShader, Ladezeit gemessen, Playwright-Test `test_viewer_v2.js` grün.

**P4 an Tools (Rechner hilft bei Slots)** (Branch `art/dv2-daten`, Fr bis 17:00; Ausweg Codex C3 Fr 11:00–13:00):
> Datenschicht passend zum neuen Mesh in `relief3d/detail_v2/daten/`.
> - Masken 0,1 m/px, 3360 × 3030, Ursprung = Weltecke, deckungsgleich mit UV1:
>   - `flaeche.png`: 0 Grund, 1 Weg, 2 Ufer, 3 Fels/Klippe, 4 Wasser, 5 Brücke.
>   - `begehbar.png`.
>   - `slot.png` (16 bit).
>   - `hoehe.png` (16 bit + Skala).
> - `legende.json`: Klassen, Untertyp `untergrund`, Slots (Bauplätze, Deko), Maßstab, Kachelschema.
> - Quellen: `detail_v2/vektor/zonen.geojson`, `wege.geojson`, `wasser.geojson` und das Mesh aus P2. Alt-Abgleich mit `zellen_relief.csv` (begehbar_3d, bauzone_plan, deko_*) und Overlay Plätze/Wege.
> - `query.mjs` (ESM, Node + Browser): `queryPoint(x, z)` → `{hoehe, flaeche, untergrund, begehbar, slot, kachel}`.
> - Tests `node --test`, mit festen Punkten:
>   - Dorfkern 209\|118
>   - E3-Wasser 189\|100
>   - Brücke E2 192\|74,5
>   - Nordwand
>   - D2-Mitte
>   - Kartenränder
> - Abnahme: Höhe vs. Mesh-Strahl ≤ 2 cm an 10 000 Zufallspunkten, Flächentyp = Dreiecksklasse ≥ 99,5 %.

**P5 an Art Umgebung** (Branch `art/dv2-modelle`, Sa bis 13:00; Ausweg Codex C4 Sa 08:00–10:00):
> Modelle in `relief3d/detail_v2/modelle/`.
> 1. `bruecke.mjs` (three.js, prozedural, auch .glb-Export) für E2 (x 186–197, z 73–75) und E3-West (x 174–186, z 126–128):
>    - Bohlen 0,22 × 0,05 m mit 1 cm Fuge.
>    - 2 Längsträger 0,2 × 0,3 m.
>    - Pfosten alle 1,5 m, Geländer 1,0 m, Handlauf.
>    - Steinwiderlager ins Ufer eingebunden.
>    - UV in Weltmetern.
>    - Spalt zum Gelände ≤ 2 cm, Stufe Weg↔Brücke ≤ 5 cm.
> 2. Grat- und Klippenwände als Loft zwischen den Ober- und Unterkanten aus `kanten.geojson`/`grat.geojson`, Unterteilung 0,25 m, Box-UV. Sie ersetzen die alten Wandkörper im neuen Viewer.
>
> Abnahme: Q1, Q3, Q12, Clay-Bilder E2 und G3 aus 1,7 m und 5 m.

**P6 an QA** (Branch `art/dv2-qa`, Fr Regeln bis 17:00, Sa Messung und Bilder bis 19:00):
> Das alte Raster-Gate wird für das neue Mesh durch neue Prüfregeln ersetzt (Fabian t2043u). Die alten Prüfer bleiben unverändert.
> - Schreibe `relief3d/detail_v2/qa/` mit Skripten für Q1–Q14 (DETAIL_V2_PLAN.md Abschnitt 5):
>   - Löcher/Risse 0 (Kantentopologie + Strahl-Lochscan aus 1,7 m und 5 m, 360°).
>   - Kantenabweichung zum Spline ≤ 2 cm.
>   - Zackenamplitude ≤ 3 cm, Knick ≤ 15°.
>   - Kreuzungen eben (R8, ≤ 2 %).
>   - Keine Dellen neben Wegen (≤ 3 cm im 3-m-Band).
>   - Wegprofil.
>   - D2 Lage und Form (|Δh| ≤ 1 cm).
>   - Ufer ≤ 5 cm.
>   - Dreiecksqualität/Budget.
>   - UV ohne Spiegelung.
>   - Datenschicht ↔ Mesh.
>   - Brücke.
>   - Layout gleich.
> - Freitag: Skripte gegen das erste Mesh laufen lassen.
> - Samstag Abnahmebilder: Clay (einfarbig, Licht und Schatten an) aus 1,7 / 5 / 12 / 30 m an Dorfkern 209\|118, Brücke E2 192\|74,5, Bach E3 189\|100, Grat G3 300\|90 und Klippen C3, dazu je 1 Wireframe aus 5 m (Linien sichtbar dick). JPG q90 nach `/workspace/dorfmap_final/detail_v2/abnahme/` mit QUELLEN.txt.
> - Ehrlich, nichts schönen. Ausnahmeliste neu nach Abschnitt 6 prüfen und als `AUSNAHMEN_DV2.md` liefern.

**P7 an Kritiker** (So ab 08:00, Ergebnis bis 12:00):
> Prüfe die Dorfmap detail_v2 gegen Fabians Ziel „auf Bodenhöhe darin laufen, glatte Kanten, keine Zacken, Risse oder Löcher, echte Brücke, Datenschicht“ anhand von `/workspace/dorfmap_final/detail_v2/abnahme/`, dem Viewer v2 und dem QA-Bericht. Note 0–10, Befunde mit Ort und Bild. Erst bei 10/10 geht es an New Bot.


## P1b3 Wasserumriss, neue Methode (19.11.2026 17:50)

- **Ursache [S]:** #58 wurde mit feiner 0,05-m-Abtastung geglättet und geprüft. QA P6 mittelt über die Stützpunkte ±2. Bei ungleich verteilten Stützpunkten liegen die Uferlinien deshalb in der QA-Messart bis 3,44 cm über der Grenze (9 Funde). Damit ist der Umriss zweimal gescheitert (#54, #58), und nach t2027u gibt es kein weiteres Nachglätten auf demselben Weg.
- **Neue Methode:** Jede Uferlinie wird als geschlossener glättender Spline mit Krümmungsgrenze r ≥ 2 m neu angepasst, ausgenommen bewusst engere Stellen (Mündungen), dann gleichmäßig auf 0,25 m abgetastet. Abnahme direkt mit dem QA-P6-Code `q3` als Testschleife und zusätzlich fein mit 0,05 m. Wasserfläche ±1 %, Gate unverändert.
- **Wer/Frist:** Art Umgebung, Branch art/dv2-vektor-wasser-q3, **heute 21:00**. Danach Zonen (#57) neu erzeugen. Wird das verfehlt, kommt Plan B für das Ufer: Das Ufer wird in P2 aus dem Mesh-Kontur-Schnitt der geglätteten Wasserhöhe erzeugt, mit Meldung an New Bot.
- **Nachtrag 17:55:** Die Spline-Methode ist gescheitert. Ein Kreis mit r 2,0 m misst in q3 schon 3,11 cm, mit r 2,3 m wächst die Fläche um 2,96 %. Ursache [S]: Die Vertices aus #58 wurden nach dem 5-cm-Resampling noch per 1-mm-Douglas-Peucker ausgedünnt und sind ungleich verteilt; q3 mittelt die Vertices im ±0,5-m-Fenster. Neue Methode: Die Geometrie aus #58 bleibt unverändert und wird nur gleichmäßig auf 0,05 m abgetastet, ohne Ausdünnung. Abnahme mit q3, Frist 21:00.
