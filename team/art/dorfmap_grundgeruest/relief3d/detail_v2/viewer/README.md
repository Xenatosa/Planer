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
| `dummy/erzeuge_dummy.py` | Dummy-Mesh im Planformat aus dem alten Raster GB (nur zum Testen, wird **nicht** eingecheckt) |
| `nachweis/` | kleine Nachweisbilder (Clay 1,7 m / 5 m, Wire+Kachelrand 5 m) und Testergebnis |

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
| `?wire=1` | dicke Dreieckskanten (LineSegments2/LineMaterial, `?wirebreite=` px, Standard 1,6) ueber der Flaeche |
| `?kachelrand=1` | Kachelgrenzen gelb auf dem Gelaende (Hoehe per Bodenstrahl, +0,1 m) |
| `?modus=orbit` | im Orbit starten (Standard: Laufen) |
| `?start=x,z,blick` | Startpunkt Laufen (Standard Dorfkern 209,118, Blick 0 = Norden) |
| `?kacheln=E3,E4` | nur diese Kacheln laden |
| `?manual=1` | keine Renderschleife (nur `__test`-Aufrufe rendern) – fuer QA-Bilder |
| `?hud=0`, `?schatten=0`, `?auge=1.7`, `?fov=60`, `?parallel=6` | HUD aus, Schatten aus, Augenhoehe, Bildwinkel, parallele Downloads |
| `?sonnenhoehe=32&sonnenazimut=315&sonne=2.8&himmel=0.9` | Licht |

## Bedienung

- **Laufen** (Standard): Kamera 1,7 m ueber Grund. WASD/Pfeile, Shift = schnell (3 bzw. 7 m/s), Maus: Klick faengt den Zeiger (Pointer-Lock), sonst mit gedrueckter Taste ziehen.
  Touch: linke Bildhaelfte = Stick (laufen), rechte Haelfte = schauen.
- **Orbit**: Taste **O** oder Knopf oben rechts. OrbitControls, `minDistance` 0,3 m – **keine 25-m-Grenze** (die gilt nur im alten Viewer).
- Bodenkontakt: senkrechter Strahl auf das Mesh (`src/boden.js`, 2-m-Zellraster der Dreiecke, exakte Hoehe aus der Dreiecksebene).
  Mehrere Flaechen uebereinander (Bruecke): genommen wird die hoechste bis 0,6 m ueber dem aktuellen Boden (Stufe), sonst die hoechste.
  Wasser-Meshes zaehlen nicht als Boden. **[A]** Spaeter austauschbar gegen `queryPoint` aus P4 (`detail_v2/daten/query.mjs`).
- Schatten: DirectionalLight mit 2048er Schattenkarte, folgt der Kamera (Laufen: 12 m vor der Kamera, ±40 m; Orbit: Ziel, ±1,3·Abstand, 30–260 m), auf Texel gerastert.

## Test-API (`window.__test`)

| Aufruf | Ergebnis |
|---|---|
| `bereit` / `fehler` | `true` sobald alles geladen und das erste Bild gerendert ist (zusaetzlich `<html data-bereit="1">` und Konsole `[dv2] bereit {...}`) / Fehlertext |
| `ladezeit` | `{gesamt_ms, manifest_ms, kacheln_ms, bodenindex_ms, erstes_bild_ms}` (auch im HUD) |
| `kam(p, t)` | Orbit, Kamera auf `p=[x,y,z]`, Ziel `t`, rendert sofort; gibt `zustand()` |
| `lauf(x, z, blick, neigung=0)` | Laufmodus bei (x,z), 1,7 m ueber Grund, `blick` in Grad (0 = Norden/−z, 90 = Osten/+x), `neigung` in Grad; rendert sofort |
| `boden(x, z[, yMax])` | Bodenhoehe (Strahl), `null` ausserhalb |
| `zustand()` | `{modus, pos, boden, blick, abstand, minDistance, ueber_grund}` |
| `schritt(dt)` | Simulationsschritt dt s mit den gerade gedrueckten Tasten, dann rendern |
| `render()`, `frames`, `stopRender()` | rendern / Bildzaehler / Schleife anhalten |
| `schatten()`, `info()` | Schattenmitte/-groesse; Kacheln, Dreiecke, Bytes, Schalter, Ladezeit |

## Manifest (`detail_v2/mesh/manifest.json`) – was der Viewer annimmt **[A]**

Pflicht ist nur `kacheln` mit einer Datei je Kachel; alles andere ist optional (der Viewer ist tolerant).

```json
{
 "format": "dorfmap-detail-v2-mesh", "version": 1, "einheit_m": 1,
 "welt": {"x_m": 336, "z_m": 303},
 "kachelschema": {"spalten": "ABCDEFGH", "zeilen": 7,
   "schnitt_x": [0,42,84,126,168,210,252,294,336], "schnitt_z": [0,43,86,129,172,215,258,303]},
 "uv": {"TEXCOORD_0": "Welt-XZ in m", "TEXCOORD_1": "(x/336, z/303)"},
 "draco": false,
 "kacheln": [
  {"id": "A1", "datei": "A1.glb", "bounds": [0,0,42,43], "dreiecke": 3780, "vertices": 1936, "bytes": 116424, "sha256": "…"}
 ],
 "zusatz": [{"datei": "bruecke_e2.glb", "rolle": "bruecke"}],
 "dreiecke_gesamt": 203616
}
```

- `kacheln`: Liste **oder** Objekt `{ "A1": {...} }`. Dateiname aus `datei` | `file` | `glb` | `uri`, sonst `<id>.glb`; relativ zum Manifest.
- `bounds` = `[x0, z0, x1, z1]` in m (optional; nur fuer den Kachelrand, wenn `kachelschema.schnitt_x/z` fehlt).
- `zusatz` (optional): weitere .glb (z. B. Bruecken), `rolle` wie unten.
- `welt` fehlt → 336 × 303 m.
- **Koordinaten** **[A]**: glTF y oben, x = Ost 0…336, z = Sued 0…303 (wie Bildzeile des Rasters), Welt-Meter direkt in POSITION (keine Node-Verschiebung noetig, wird aber beachtet).
- **Rollen** je Mesh aus dem Node-/Mesh-Namen: `wasser*` → Wasser (halbtransparent, kein Boden), `bruecke*`, `wand*` → eigenes Material, sonst Gelaende. `rolle` im Manifest-Eintrag ueberschreibt.
- Attribute: POSITION, NORMAL (fehlt → `computeVertexNormals`), TEXCOORD_0/1 (vom Viewer nicht benutzt, keine Texturen), optional TEXCOORD_2 (P2, Wegband – ignoriert). Indizes uint16/uint32.
- **[F]** letzte Kachelzeile: 43·7 = 301 < 303 – der Dummy schneidet Zeile 7 bei 258…303 (45 m). Falls P2 anders schneidet, liest der Viewer `schnitt_z`/`bounds` aus dem Manifest.

## Dummy

`dummy/erzeuge_dummy.py --out <ordner> [--schritt 2] [--kacheln A1,B1]`: aus GB (0,5 m) mit Schrittweite `--schritt` (2 = 1 m: 56 Kacheln, 203 616 Dreiecke, 6,8 MB;
1 = 0,5 m: 814 464 Dreiecke, 26,5 MB). Normalen global aus dem Raster (nahtlos). Schreibt nie nach `detail_v2/mesh/`.

## Test

```sh
cd team/art/dorfmap_grundgeruest/relief3d
NODE_DIR=/tmp/dv2_viewer/node node detail_v2/viewer/test_viewer_v2.js       # MESH_DIR=<ordner mit manifest.json>, BILDER=<ausgabe>
```

Prueft (23 Punkte): alle Kacheln geladen, Dreiecke = Manifest, Budget, Ladezeit; Bodenstrahl = Raster an Gitterpunkten (nur Dummy), keine Loecher;
`lauf` 1,7 m; Tempo 3/7 m/s; Schatten folgt und wirkt; `kam` 5 m und 1 m; Clay-Bilder 1,7 m/5 m; Wire + Kachelrand; WASD live, Taste O, Mausrad < 25 m, Knopf;
Touch-Stick und Touch-Schauen; keine Konsolenfehler. Ohne `MESH_DIR` wird der Dummy unter `/tmp/dv2_viewer/dummy_mesh` erzeugt.

## Offene Punkte fuer das echte Mesh (P2) **[F]/[R]**

- **[R]** `?wire=1` baut Kanten aller Kacheln: bei 1,6 Mio. Dreiecken ≈ 2,4 Mio. Linien – fuer QA-Bilder mit `?kacheln=` eingrenzen.
- **[R]** Ladezeit wurde nur lokal (localhost, SwiftShader) gemessen; das echte Mesh ist bis ~2× so gross wie der dichte Dummy.
- **[F]** Wasser/Bruecken: eigene Meshes in der Kachel-.glb (Name `wasser_*`/`bruecke_*`) oder `zusatz`? Viewer kann beides.
- **[F]** Achsen/Ursprung wie oben angenommen (x Ost, z Sued, y oben, Ursprung Kartenecke NW).
