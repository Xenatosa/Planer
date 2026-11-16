# P10/P10b – 3D-Mesh, Lochscan und Nahbilder für alle 56 Kacheln (A–H × 1–7)

Basis: P10 `art/dorfmap-fertig` @ `038528c`, P10b @ `dc8c174`. Nur neue Dateien in diesem Ordner; Relief-, Höhen-, Prüfer- und
Gate-Dateien bleiben unverändert. Alle Artefakte gehen nach `/tmp/p10` (nicht `/tmp/w3/bundle_r.js`,
nicht `/tmp/gate_loch.json`).

## Befehle (im Ordner `relief3d`)

```sh
# alles in einem Lauf (Build, Hash-Vergleich, Lochscan + Positivkontrolle C3, 56 Nahbilder, Übersicht)
sh pruefung/alle_kacheln/alles.sh /tmp/p10b   # P10b: ~10 min (Wände ~4 min)
# Einzelschritte
python3 pruefung/alle_kacheln/baue_alle_kacheln.py --out /tmp/p10          # Paket + HTML (~30 s)
NODE_PATH=/tmp/w3/node_modules REF=index.html NEU=/tmp/p10/alle_kacheln.html \
  OUT=/tmp/p10/hash_vergleich.json node pruefung/alle_kacheln/hash_vergleich.js   # D1/G1/D2 identisch?
KONTROLLE=C3 sh pruefung/alle_kacheln/lochscan_alle.sh /tmp/p10                # R5_loch 56 Kacheln
NODE_PATH=/tmp/w3/node_modules HTML=/tmp/p10/alle_kacheln.html DIR=/tmp/p10/nahbilder \
  node pruefung/alle_kacheln/nahbild_alle.js                                     # 56 Nahbilder + karte.png
python3 pruefung/alle_kacheln/uebersicht.py /tmp/p10/nahbilder /tmp/p10/nahbilder_uebersicht.png 320 /tmp/p10/lochscan_alle.json
```

`NODE_PATH`/`NODE_DIR` zeigen nur lesend auf vorhandene `node_modules` (three 0.170, esbuild, playwright).
Das esbuild-Bundle landet in einem Temp-Ordner, nicht in `/tmp/w3`.

## Verfahren (wiederverwendet, nicht neu erfunden)

`index.html` wird von `neu/baue_viewer.py` gebaut: `neu/pipeline.py` → `neu.mesh.build_manifest()` erzeugt
aus `relief_daten.json.gz` die Kachelmeshes D1, G1, D2 (`neu.mesh.tile_mesh()`, 0,5-m-Raster, `rs=2`), der
Viewer `neu/viewer.js` baut je Kachel Oberfläche + Seiten + Boden (geschlossener Körper) in Ebene `gelaende`.

- **D1, G1, D2**: `build_manifest()` wird unverändert aufgerufen (Standardvarianten: Gelände 2, Wegende 1,
  Kreuzung 24). Ergebnis ist bytegleich zum Paket in `index.html` (Beleg unten).
- **übrige 53 Kacheln**: dieselbe Funktion `neu.mesh.tile_mesh()` auf dem sichtbaren `GB`-Höhenfeld – das
  Verfahren von D2 (`locked_visible_GB_bytes`). Die 293 `terrain_extensions`-Vertices des Pakets
  (Rampenauslauf außerhalb D1/G1, alle in C1) werden wie in `pruefung/neu_mesh_adapter.py` gesetzt
  (`--ohne-erweiterung` schaltet das ab).
- **Viewer** `viewer_alle.js`: `tileColor`, `foundationGeometry`, `makeMesh` sind unveränderte Kopien aus
  `neu/viewer.js`; Kachelliste kommt aus dem Paket. `window.__test.bereit`, `__szene`, `dump`, `kam`,
  `setView` wie im Original, dazu `focus(kachel, abstand)`. Kachelgrenzen: Spalte 42, Zeile 43 Zellen
  (wie `pruefe_regeln.feld`); die Zellreihen z = 301–303 liegen in keiner Kachel und sind nicht gebaut.
- Query-Parameter: `?tile=C3` (Fokus), `?kacheln=C3,D3` (Teilmenge), `?nosh=1`, `?clay=1`, `?raster=0`.
- Größe: HTML ≈ 12 MB (kleiner als index.html mit 14 MB), alle 56 Kacheln in einer Datei, Ladezeit
  headless ≈ 5 s. Kachelgruppen sind daher nicht nötig, über `?kacheln=` aber möglich (Lochscan mit
  `Q=?kacheln=…` mehrfach laufen lassen und `loch_auswertung.py` mit mehreren Läufen summieren).

## Prüfungen

- `hash_vergleich.js`: lädt `index.html` und das neue HTML in Chromium und vergleicht je Kachel
  SHA-256 der Weltkoordinaten und Indizes von `terrain_surface_*`, `terrain_sides_*`, `terrain_bottom_*`.
- Build prüft zusätzlich: Prototypen = `tile_mesh()` auf ihrem Höhenfeld, Naht aller 97 Nachbarpaare
  (gemeinsame Randvertices gleich hoch).
- `lochscan_alle.sh`: ruft `pruefung/loch_o18g.js` **unverändert** (`HTML=/tmp/p10/alle_kacheln.html
  OUT=/tmp/p10/loch_alle_roh.json RAND=0.6`), `loch_auswertung.py` zählt je Kachel.
  Positivkontrolle `--testloch C3` entfernt ein Dreieck in C3; der Scan muss dort genau 3 offene Kanten finden.
- `nahbild_alle.js`: je Kachel ein PNG schräg von oben (Kamera wie `focus()` in `neu/viewer.js`,
  Abstand × 1,6, 1024 × 768, gelber Kachelrand), plus `karte.png`.

Ergebnisse dieses Stands: `ergebnis/` (Berichte, Übersichtsbild, Kartenbild). Die 56 Einzel-PNGs sind
nicht eingecheckt (56 PNGs, 1024 × 768, zusammen ≈ 44 MB; Kopie unter `/workspace/p10_nahbilder/`) und werden mit obigem Befehl in ~2 min neu erzeugt.


## P10b – Ergänzungen

**Nahbild für eine Stelle** (`nahbild.js`, ein Browserlauf, ~5–12 s je Aufruf):

```sh
export NODE_PATH=/tmp/w3/node_modules
# ganze Kachel, Standardblick (wie focus(): Azimut 35,5°, Neigung 45,5°, Abstand 78,6)
node pruefung/alle_kacheln/nahbild.js --kachel C3 --out /tmp/p10b/c3.png
# Punkt x|z (Rastermeter wie Gate-Trefferlisten), Blick nach Norden, flach, nah
node pruefung/alle_kacheln/nahbild.js --xz 140,35 --abstand 30 --azimut 0 --neigung 30 --out /tmp/p10b/d1_wandfuss.png
# senkrecht von oben, nur Gelände (ohne Overlays), Clay, schneller mit Teilmenge
node pruefung/alle_kacheln/nahbild.js --xz 147,236 --abstand 60 --neigung 90 --ohne wasser,wege,waende --clay --nur-kacheln D6,C6,E6,D5,D7 --out /tmp/p10b/d6_oben.png
# mehrere Stellen in einem Lauf (JSON-Liste mit kachel|x,z, abstand, azimut, neigung, out, titel)
node pruefung/alle_kacheln/nahbild.js --liste /tmp/p10b/stellen.json
```
Azimut = Blickrichtung (0 = Nord/−z, 90 = Ost/+x, 180 = Süd/+z, 270 = West/−x), Neigung = Grad unter der
Horizontalen (90 = senkrecht), Abstand = Kamera–Ziel. Das Ziel liegt auf der Geländehöhe am Punkt.
Im Viewer selbst: `window.__test.blick({kachel:'C3'})` bzw. `blick({x:140, z:35, abstand:30, azimut:0, neigung:30})`.

**Zellreihen z 301–303:** `ny = 303`, Zeilen à 43 Zellen ergeben 7 × 43 = 301. Die Reihen z = 301 und 302 gehören
zur Karte (`SPEC.md`: Raster 336 × 303, letzte Zeile 10 px = 0,4 m hoch; `PRUEFPROTOKOLL.md`: Randzeile 302 übernimmt
Werte der Zeile 301), und `pruefe_regeln.feld()` ordnet sie per `np.clip(z//43, 0, 6)` der Zeile 7 zu. Deshalb
reichen die Kacheln A7–H7 jetzt bis z = 303 (45 statt 43 Zellen, 8 280 statt 7 395 Vertices); `--ohne-randzeilen`
stellt den P10-Stand her. Die letzte Reihe ist im 0,5-m-Höhengitter wie jede andere 1 m breit (so liegt sie in GB vor).

**Wegprofile:** Für die 53 Nicht-Prototyp-Kacheln wird jetzt auch `neu.mesh.terrain_heights()` (gleiche Varianten
wie D1/G1) aufgerufen. Nur D6 ändert sich (490 Vertices, max. 0,75 m, Ebene `rampenkreuzung_gemeinsame_ebene_weicher_rand`);
alle anderen 52 bleiben auf GB (+ C1-Erweiterung). Ränder bleiben durch den 3-m-Kachelrand-Fade auf GB (Naht 0,0 m).
`--ohne-wegprofile` schaltet das ab.

**Wandkörper:** `waende_alle()` führt den Schleifenrumpf von `neu.wand.build_wall_manifest()` mit denselben
privaten Funktionen (`_chunks`, `_network_solid`, `_terrain_heights`) für alle Kacheln aus; D1/G1 werden gegen die
Pipeline-Hashes geprüft. D2 bleibt wie in der Pipeline wandfrei (die unterdrückten 2 Abschnitte zeigt `?d2wand=1`).
Laufzeit ≈ 4 min (`--ohne-alle-waende` = P10-Stand).

**Wege/Wasser:** In `index.html` (Kern-Viewer) gibt es für D1/G1/D2 keine eigenen Wege- oder Wassermeshes – beides
ist dort nur Vertexfarbe (VC) bzw. bei D1/G1 Geländeprofil. Damit Wege und Wasser auf allen Kacheln sichtbar sind,
zeichnet `viewer_alle.js` sie aus `relief_daten.json.gz` nach dem Verfahren des Legacy-Viewers `main.js`:
Wege-Overlay aus `WEGA` (Vertex-Alpha, +0,05 m, Brücken als Boxen) und Wasser aus `WV` im Raster-Wassernetz
(Pfad `?wneu=0`: Spiegelglättung, Randabsenkung, Farben/Alpha/Schaum; ohne den Shader- und Konturflächen-Teil).
Beides liegt in den Ebenen `wege`/`wasser`, nicht `gelaende` – der Lochscan ist davon nicht betroffen.
`?ohne=wasser,wege,waende` blendet sie aus. Zahlen je Kachel: `ergebnis/darstellung.md`.

## Grenzen

- Der Lochscan sieht nur Meshes der Ebene `gelaende`. Jede Kachel ist ein geschlossener Rasterkörper
  (Oberfläche + Seiten + Boden); ein R5-Treffer entsteht nur bei fehlenden/entarteten Dreiecken. Optische
  „Löcher“ (Spalten zwischen Kacheln, Senken, Klippen) erfasst er nicht – dafür Nahtprüfung und Nahbilder.
- Objekte (Bäume, Felsen, Häuser) und die Rampen-Bänder (`rampenwege`) sind nicht dargestellt.
