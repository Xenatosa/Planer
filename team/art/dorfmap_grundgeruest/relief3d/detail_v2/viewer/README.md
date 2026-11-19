# Viewer v2 (Detail v2, P3)

Eigener Viewer fuer das Vektor-Mesh aus `detail_v2/mesh/` (DETAIL_V2_PLAN.md, Abschnitt 3.2 + Abschnitt 9 „P3 an Dev UI“).
Alte Viewer (`index.html`, `main.js`, `neu/`) und alle alten Dateien sind unveraendert. Keine Texturen.

Marker: **[S]** gesetzt/gemessen · **[A]** Annahme · **[R]** Risiko · **[F]** offene Frage.

## Dateien

| Datei | Zweck |
|---|---|
| `index.html` | Seite (laedt `viewer_v2.js`) |
| `src/main.js`, `src/boden.js` | Quelle: Laden, Kamera/Steuerung, Clay/Wire/Kachelrand, Test-API; Bodenstrahl |
| `viewer_v2.js` | gebautes Bundle (esbuild 0.24.2, three 0.170.0, IIFE, ~0,6 MB) |
| `bau_viewer.sh` | baut das Bundle; `NODE_DIR` = Ordner fuer `npm ci` von `relief3d/bau/package*.json` (Standard `/tmp/dv2_viewer/node`) |
| `test_viewer_v2.js` | Playwright-Test (HeadlessChrome/SwiftShader, eigener HTTP-Server) |
| `dummy/erzeuge_dummy.py` | Dummy-Mesh im verbindlichen Format aus dem alten Raster GB (nur zum Testen, wird **nicht** eingecheckt) |
| `nachweis/` | kleine Nachweisbilder (Clay 1,7 m / 5 m, Wire+Kachelrand 5 m, Klassen 5 m Bruecke E2) und Testergebnis |

## Starten

`fetch` ueber `file://` geht nicht, also per HTTP aus `relief3d/`:

```sh
cd team/art/dorfmap_grundgeruest/relief3d
python3 -m http.server 8080
# echtes Mesh (P2):  http://localhost:8080/detail_v2/viewer/            (Standard ?mesh=../mesh/manifest.json)
# Dummy:             python3 detail_v2/viewer/dummy/erzeuge_dummy.py --out detail_v2/viewer/dummy/mesh   (nicht committen)
#                    http://localhost:8080/detail_v2/viewer/?mesh=dummy/mesh/manifest.json
```

## URL-Schalter

| Schalter | Wirkung |
|---|---|
| `?mesh=<url>` | Manifest-URL (relativ zur Seite), Standard `../mesh/manifest.json` |
| `?clay=1` | einfarbig grau, Licht + Schatten |
| `?klassen=1` | Debug-Einfaerbung nach `_FLAECHE` (Farben wie `detail_v2/daten/legende.json`), Legende im HUD; keine Texturen |
| `?wire=1` | dicke Dreieckskanten (LineSegments2/LineMaterial, `?wirebreite=` px, Standard 1,6) ueber der Flaeche |
| `?kachelrand=1` | Kachelgrenzen gelb auf dem Gelaende (aus den `bbox`, Hoehe per Bodenstrahl, +0,1 m) |
| `?query=1` bzw. `?query=<ordner-url>` | optional `queryPoint` aus `detail_v2/daten/query.mjs` (P4) einhaengen (`1` = `../daten/`) |
| `?modus=orbit` | im Orbit starten (Standard: Laufen) |
| `?start=x,z,blick` | Startpunkt Laufen (Standard Dorfkern 209,118, Blick 0 = Norden) |
| `?kacheln=E3,E4` | nur diese Kacheln laden (Modelle immer) |
| `?manual=1` | keine Renderschleife (nur `__test`-Aufrufe rendern) – fuer QA-Bilder |
| `?hud=0`, `?schatten=0`, `?auge=1.7`, `?fov=60`, `?parallel=6` | HUD aus, Schatten aus, Augenhoehe, Bildwinkel, parallele Downloads |
| `?sonnenhoehe=32&sonnenazimut=315&sonne=2.8&himmel=0.9` | Licht |

Ohne Schalter: neutrales Material mit leicht getoenten Vertexfarben je Klasse (Wasser blaeulich, Weg braeunlich).

## Bedienung

- **Laufen** (Standard): Kamera 1,7 m ueber Grund. WASD/Pfeile, Shift = schnell (3 bzw. 7 m/s), Maus: Klick faengt den Zeiger (Pointer-Lock), sonst mit gedrueckter Taste ziehen.
  Touch: linke Bildhaelfte = Stick (laufen), rechte Haelfte = schauen. HUD zeigt Bodenhoehe, Klasse, Neigung, begehbar/gesperrt.
- **Orbit**: Taste **O** oder Knopf oben rechts. OrbitControls, `minDistance` 0,3 m – **keine 25-m-Grenze** (die gilt nur im alten Viewer).
- Schatten: DirectionalLight mit 2048er Schattenkarte, folgt der Kamera (Laufen: 12 m vor der Kamera, ±40 m; Orbit: Ziel, ±1,3·Abstand, 30–260 m), auf Texel gerastert.

## Bodenhaftung und Begehbarkeit (verbindlich, Grundgeruest 19.11.2026)

- **Strahl** (`src/boden.js`): senkrecht auf alle geladenen Meshes (Kacheln **und** `modelle`), 2-m-Zellraster, Hoehe exakt aus der Dreiecksebene,
  Klasse aus `_FLAECHE` des getroffenen Dreiecks, Neigung aus der Dreiecksnormale. Gleiches Verfahren wie `baueMeshIndex` in `query.mjs`.
- Mehrere Flaechen uebereinander: genommen wird die **hoechste bis 0,6 m ueber dem aktuellen Boden** (Stufe), sonst die hoechste.
  Daher trifft der Strahl auf der Bruecke das **Deck vor dem Wasser**; unter einer hohen Bruecke (> 0,6 m) bleibt man unten. **[A]**
- **Begehbar** = Klasse ∉ {3 fels_klippe, 4 wasser} **und** Neigung ≤ 35°; Klasse 5 (Bruecke) immer begehbar.
  Mesh ohne `_FLAECHE` (Altformat): nur die Neigungsregel; Modell ohne `_FLAECHE`: Klasse aus `modelle[].klasse`.
  Gemischtes Dreieck (Verstoss gegen klassenrein): Klasse `null`, nur Neigungsregel, gezaehlt in `info().klassen.gemischt`. **[A]**
- Bewegung in 0,25-m-Teilschritten; ein gesperrter Teilschritt wird verworfen, an der Grenze wird entlang der freien Achse gerutscht.
  Steht man (z. B. per `__test.lauf`) schon auf Gesperrtem, darf man heraus. `__test.lauf` selbst setzt ohne Regel (QA-Bilder ueberall).
- **queryPoint (P4)**: mit `?query=` wird `query.mjs` per `import()` geladen (`ladeDatenschicht(basis, {})`, nur lesen). Liefert
  `queryPoint(x,z).begehbar` einen Wahrheitswert (Maske `begehbar.png` vorhanden), gilt dieser statt der Mesh-Regel – ausser auf dem
  Brueckendeck (Klasse 5 aus dem Modell). Die **Hoehe kommt immer aus dem Strahl**. Fehlen die Masken (Stand Do: nur `slot.png`), bleibt die Mesh-Regel;
  fehlende Masken erzeugen 404-Meldungen in der Konsole. `__test.treffer()` sagt mit `quelle` (`mesh`/`queryPoint`), was entschieden hat.

## Test-API (`window.__test`)

| Aufruf | Ergebnis |
|---|---|
| `bereit` / `fehler` | `true` sobald alles geladen und das erste Bild gerendert ist (zusaetzlich `<html data-bereit="1">` und Konsole `[dv2] bereit {...}`) / Fehlertext |
| `ladezeit` | `{gesamt_ms, manifest_ms, kacheln_ms, bodenindex_ms, query_ms, erstes_bild_ms}` (auch im HUD) |
| `kam(p, t)` | Orbit, Kamera auf `p=[x,y,z]`, Ziel `t`, rendert sofort; gibt `zustand()` |
| `lauf(x, z, blick, neigung=0)` | Laufmodus bei (x,z), 1,7 m ueber Grund (oberste Flaeche), `blick` in Grad (0 = Norden/−z, 90 = Osten/+x); rendert sofort |
| `treffer(x, z[, yMax])` | `{y, klasse, klassenname, neigung, begehbar, quelle, netz, kachel}` oder `null` |
| `boden(x, z[, yMax])` | nur Hoehe |
| `zustand()` | `{modus, pos, boden, blick, abstand, minDistance, klasse, begehbar, ueber_grund}` |
| `schritt(dt)` | Simulationsschritt dt s mit den gerade gedrueckten Tasten (inkl. Begehbarkeit), dann rendern |
| `gesperrt()` | Zaehler verworfener/gerutschter Teilschritte |
| `render()`, `frames`, `stopRender()` | rendern / Bildzaehler / Schleife anhalten |
| `schatten()`, `info()` | Schattenmitte/-groesse; Kacheln, Modelle, Dreiecke, Bytes, Klassenzaehlung, Format-Abweichungen, queryPoint-Quellen |

## Manifest (`detail_v2/mesh/manifest.json`) – verbindlich (Grundgeruest 19.11.2026)

```json
{
 "version": 1, "einheit": "m", "ursprung": "weltecke",
 "karte": {"breite": 336, "tiefe": 303},
 "klassen": {"0": "grund", "1": "weg", "2": "ufer", "3": "fels_klippe", "4": "wasser", "5": "bruecke"},
 "attribute": {"flaeche": "_FLAECHE"},
 "uv": {"TEXCOORD_0": "welt_xz_m", "TEXCOORD_1": "karte_norm", "TEXCOORD_2": "wegband"},
 "kacheln": [
  {"id": "A1", "glb": "kacheln/A1.glb", "bbox": [0, 0, 42, 43], "dreiecke": 3780, "klassen_anteil": {"grund": 0.93, "ufer": 0.07}}
 ],
 "modelle": [{"id": "bruecke_E2", "glb": "modelle/bruecke_E2.glb", "klasse": 5}]
}
```

- **Hauptweg** ist genau dieses Format; `glb` relativ zum Manifest; `bbox = [x0, z0, x1, z1]` in m (Schnitt x = 42·i, z = 43·j, Zeile 7 bis 303).
  `modelle` werden wie Kacheln geladen, gerendert und vom Strahl getroffen.
- Der Viewer prueft das Format beim Laden (`info().formatWarnungen`, Konsolen-Warnung, HUD), laedt aber trotzdem.
- `_FLAECHE`: Vertex-Attribut SCALAR (u8/u16/u32/float, gerundet), Klasse 0–5, Dreiecke klassenrein. GLTFLoader legt es als `geometry.attributes._flaeche` ab.
- `klassen_anteil` **[A]**: Anteil der Dreiecke je Klassenname (Summe 1), nur aufgefuehrte Klassen > 0. Der Viewer liest es nicht.
- **[A]** Achsen: glTF y oben, x = Ost 0…336, z = Sued 0…303, Ursprung Weltecke (0,0), Welt-Meter direkt in POSITION (Node-Transform wird beachtet).
- Toleranz fuer Altfelder (bleibt): `kacheln` als Objekt, `datei`/`file`/`uri` statt `glb`, `bounds` statt `bbox`, `welt.x_m/z_m` statt `karte`,
  `zusatz[]` mit `rolle` statt `modelle`, Meshes ohne `_FLAECHE` (Klasse aus Namen `wasser*`/`bruecke*`).

## Dummy

`dummy/erzeuge_dummy.py --out <ordner> [--schritt 2] [--kacheln A1,B1]` schreibt `manifest.json`, `kacheln/*.glb`, `modelle/bruecke_E2.glb`
im verbindlichen Format aus dem alten Raster (`relief_daten.json.gz`): Hoehe GB, `_FLAECHE` aus WV (Wasser), WEGA ≥ 100 (Weg),
2 m Saum um Wasser (Ufer), Neigung > 40° (Fels/Klippe), sonst Grund; Prioritaet Wasser > Bruecke > Weg > Ufer > Fels > Grund, Dreiecke klassenrein
(Vertices an Klassengrenzen doppelt). TEXCOORD_0/1 ja, TEXCOORD_2 nein. Wasser liegt im Dummy auf Bachbett-Hoehe (kein eigener Spiegel) **[A]**.
`bruecke_E2`: Quader x 186–198, z 73–76, Deck y 0,30, 0,25 m dick, Klasse 5 (aus den Planken in `relief_daten`).
Schritt 2 = 1 m: 56 Kacheln, 203 616 + 12 Dreiecke, 7,3 MB; Schritt 1 = 0,5 m: 814 464 + 12 Dreiecke, 27,9 MB. Schreibt nie nach `detail_v2/mesh/`.

## Test-API (`window.__test`)

| Aufruf | Ergebnis |
|---|---|
| `bereit` / `fehler` | `true` sobald alles geladen und das erste Bild gerendert ist (zusaetzlich `<html data-bereit="1">` und Konsole `[dv2] bereit {...}`) / Fehlertext |
| `ladezeit` | `{gesamt_ms, manifest_ms, kacheln_ms, bodenindex_ms, query_ms, erstes_bild_ms}` (auch im HUD) |
| `kam(p, t)` | Orbit, Kamera auf `p=[x,y,z]`, Ziel `t`, rendert sofort; gibt `zustand()` |
| `lauf(x, z, blick, neigung=0)` | Laufmodus bei (x,z), 1,7 m ueber Grund (oberste Flaeche), `blick` in Grad (0 = Norden/−z, 90 = Osten/+x); rendert sofort |
| `treffer(x, z[, yMax])` | `{y, klasse, klassenname, neigung, begehbar, quelle, netz, kachel}` oder `null` |
| `boden(x, z[, yMax])` | nur Hoehe |
| `zustand()` | `{modus, pos, boden, blick, abstand, minDistance, klasse, begehbar, ueber_grund}` |
| `schritt(dt)` | Simulationsschritt dt s mit den gerade gedrueckten Tasten (inkl. Begehbarkeit), dann rendern |
| `gesperrt()` | Zaehler verworfener/gerutschter Teilschritte |
| `render()`, `frames`, `stopRender()` | rendern / Bildzaehler / Schleife anhalten |
| `schatten()`, `info()` | Schattenmitte/-groesse; Kacheln, Modelle, Dreiecke, Bytes, Klassenzaehlung, Format-Abweichungen, queryPoint-Quellen |

## Manifest (`detail_v2/mesh/manifest.json`) – verbindlich (Grundgeruest 19.11.2026)

```json
{
 "version": 1, "einheit": "m", "ursprung": "weltecke",
 "karte": {"breite": 336, "tiefe": 303},
 "klassen": {"0": "grund", "1": "weg", "2": "ufer", "3": "fels_klippe", "4": "wasser", "5": "bruecke"},
 "attribute": {"flaeche": "_FLAECHE"},
 "uv": {"TEXCOORD_0": "welt_xz_m", "TEXCOORD_1": "karte_norm", "TEXCOORD_2": "wegband"},
 "kacheln": [
  {"id": "A1", "glb": "kacheln/A1.glb", "bbox": [0, 0, 42, 43], "dreiecke": 3780, "klassen_anteil": {"grund": 0.93, "ufer": 0.07}}
 ],
 "modelle": [{"id": "bruecke_E2", "glb": "modelle/bruecke_E2.glb", "klasse": 5}]
}
```

- **Hauptweg** ist genau dieses Format; `glb` relativ zum Manifest; `bbox = [x0, z0, x1, z1]` in m (Schnitt x = 42·i, z = 43·j, Zeile 7 bis 303).
  `modelle` werden wie Kacheln geladen, gerendert und vom Strahl getroffen.
- Der Viewer prueft das Format beim Laden (`info().formatWarnungen`, Konsolen-Warnung, HUD), laedt aber trotzdem.
- `_FLAECHE`: Vertex-Attribut SCALAR (u8/u16/u32/float, gerundet), Klasse 0–5, Dreiecke klassenrein. GLTFLoader legt es als `geometry.attributes._flaeche` ab.
- `klassen_anteil` **[A]**: Anteil der Dreiecke je Klassenname (Summe 1), nur aufgefuehrte Klassen > 0. Der Viewer liest es nicht.
- **[A]** Achsen: glTF y oben, x = Ost 0…336, z = Sued 0…303, Ursprung Weltecke (0,0), Welt-Meter direkt in POSITION (Node-Transform wird beachtet).
- Toleranz fuer Altfelder (bleibt): `kacheln` als Objekt, `datei`/`file`/`uri` statt `glb`, `bounds` statt `bbox`, `welt.x_m/z_m` statt `karte`,
  `zusatz[]` mit `rolle` statt `modelle`, Meshes ohne `_FLAECHE` (Klasse aus Namen `wasser*`/`bruecke*`).

## Dummy

`dummy/erzeuge_dummy.py --out <ordner> [--schritt 2] [--kacheln A1,B1]`: aus GB (0,5 m) mit Schrittweite `--schritt` (2 = 1 m: 56 Kacheln, 203 616 Dreiecke, 6,8 MB;
1 = 0,5 m: 814 464 Dreiecke, 26,5 MB). Normalen global aus dem Raster (nahtlos). Schreibt nie nach `detail_v2/mesh/`.

## Test

```sh
cd team/art/dorfmap_grundgeruest/relief3d
NODE_DIR=/tmp/dv2_viewer/node node detail_v2/viewer/test_viewer_v2.js
#   MESH_DIR=<ordner mit manifest.json>  BILDER=<ausgabe>  DATEN_DIR=<ordner mit query.mjs aus P4> (optional, sonst queryPoint-Test uebersprungen)
```

Prueft (36 Punkte mit `DATEN_DIR`, sonst 35):
- Laden: alle Kacheln + Modelle, Dreiecke = Manifest, Budget, Ladezeit.
- **Format**: Manifest-Felder genau wie verbindlich, `glb`-Pfade, `bbox` = Schnitt; glb ohne Draco/Transform, POSITION in bbox,
  TEXCOORD_0 = Welt-XZ, TEXCOORD_1 = (x/336, z/303); `_FLAECHE` u8 0–5, klassenrein, `klassen_anteil` stimmt; Viewer-Formatpruefung ohne Abweichung.
- **_FLAECHE im Viewer**: Dreiecke je Klasse = glb, 0 gemischt; Strahl (Hoehe + Klasse) = Brute-Force aus den glb an 62 Punkten.
- Bodenstrahl = Raster an Gitterpunkten (Dummy), keine Loecher; `lauf` 1,7 m; Tempo 3/7 m/s.
- **Begehbarkeit**: Laeufer haelt vor Wasser (Klasse 4), Fels (Klasse 3) und einem steilen Dreieck (> 35°), bleibt dabei auf begehbarem Boden.
- **Bruecke**: Strahl trifft Deck (Klasse 5, y 0,30) vor Wasser darunter; Laeufer quert den Bach ueber das Deck (1,7 m ueber Deck); 3 m daneben stoppt ihn das Wasser.
- Schatten folgt und wirkt; `kam` 5 m und 1 m; Clay-Bilder 1,7 m/5 m; Wire + Kachelrand; `?klassen=1` (Wasser blau, Bruecke/Weg braun);
  optional queryPoint eingehaengt; WASD live, Taste O, Mausrad < 25 m, Knopf; Touch-Stick und Touch-Schauen; keine Konsolenfehler.

## Offene Punkte fuer das echte Mesh (P2) **[F]/[R]**

- **[F]** `klassen_anteil`: Anteil nach Dreiecksanzahl (so im Dummy) oder nach Flaeche? Viewer liest es nicht, nur der Test vergleicht.
- **[F]** Wasser: eigener Spiegel als Klasse-4-Dreiecke im Kachel-Mesh (Plan: 1 m unter Ufer) – der Viewer nimmt immer die oberste Flaeche bis 0,6 m Stufe;
  ein Spiegel ueber dem Bett ist dann der Treffer (gesperrt), wie gewuenscht.
- **[F]** Bruecken hoeher als 0,6 m ueber dem Ufer brauchen eine Rampe im Modell oder im Gelaende, sonst kommt man nicht hinauf.
- **[R]** `?wire=1` baut Kanten aller Kacheln: bei 1,6 Mio. Dreiecken ≈ 2,4 Mio. Linien – fuer QA-Bilder mit `?kacheln=` eingrenzen.
- **[R]** Ladezeit nur lokal (localhost, SwiftShader) gemessen; das echte Mesh ist bis ~2× so gross wie der dichte Dummy.
- **[F]** queryPoint: sobald `begehbar.png` (P4, Fr) liegt, entscheidet dessen Maske; Abweichungen Maske ↔ `_FLAECHE` zeigt `treffer().quelle`.
