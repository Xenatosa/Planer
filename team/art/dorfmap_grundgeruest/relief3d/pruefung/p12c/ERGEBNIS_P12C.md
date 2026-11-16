# P12c – Wasserrand nach Abstandsfeld zur Uferlinie (56-Kachel-Viewer)

Branch `devui/dorfmap-p12c`, Basis `art/dorfmap-fertig` @ `1778473` (L3e). Geändert: nur `pruefung/alle_kacheln/viewer_alle.js`.

Kosten: 0 € zusätzlich, Codex: nein (Dev UI selbst), Laufzeit: bau_endstand 507 s / Arbeitszeit ca. 45 min

## Befund (Art Umgebung nach L3e)
Alpha, Tiefenblende und Ufertönung im P12b-Wasser hingen an Maskenvertices (Ring 1 Alpha × 0,6, Ring 2 Alpha 0, Tiefe je
Vertex) und wurden linear über die Dreiecke interpoliert. Ergebnis: heller Sägesaum entlang der Ufer, im Zellraster der Maske
(G7-Nord, F7/G7-Süd, E7-Rinne). Zusätzlich: Wassernormalen je Kachel (`computeVertexNormals`) → Helligkeitslinie im Wasser an
der Kachelnaht F7|G7, und die Absenkung von Ring 2/3 unter den Boden kippte die Randnormalen.

## Umsetzung (Standard; `?wfeld=0` = P12b-Verhalten, `?wrand=0` = alter Stand vor P12b)
1. **Uferlinie** = Nulllinie der Wassertiefe DS = Spiegel − Boden (WR in der Maske, WE in Ring 1), je Rasterzelle per Marching
   Squares als Strecken, Kantenpunkte linear interpoliert (zur Laufzeit im Viewer, nicht rastergebunden).
2. **Abstandsfeld** DIST: vorzeichenbehafteter euklidischer Abstand jedes Wasser-/Randvertex zur nächsten Uferstrecke
   (Suche ± 4 Zellen, Kappung 2 m), + auf der Wasserseite. Als Vertexattribut `wdist` ins Wassermesh.
3. **Fragmentshader** (onBeforeCompile am Wassermaterial): Alpha × smoothstep(0; 0,75 m; wdist), Ufertönung
   mix(…, 0,5 × (1 − smoothstep(0; 0,5 m; wdist))). Weil der Abstand nahezu linear ist, folgt die Blende der Uferlinie und nicht
   den Dreiecken (vertexweise smoothstep erzeugte Zähnchen je Zelle – geprüft und verworfen).
4. **Normalen** kartenweit aus dem Spiegel WR/WE (zentrale Differenzen), ohne die Randabsenkung → keine Kachelnaht im Wasser.
5. **Schaum** im Uferstreifen (DIST < 0,5 m) ausgeblendet, ab 1,5 m wie bisher.
Geometrie (Höhen, Dreiecke), Maske WV, Spiegel WR und Flusslauf unverändert, kein Wasser entfernt.

## Messwerte
- Wassernetz: wfeld=0 (P12b) und neu identisch: 32 Meshes / 67086 Dreiecke / 36915 Vertices (wrand=0: 31 / 56480 / 31511).
  Konsolenfehler und -warnungen: keine (`wasser_mesh_zaehlung.json`).
- `?wfeld=0` rendert bytegleich zum Basis-Viewer @ 1778473 (12/12 Nahbilder).
- Gate (ohne NODE_PATH): regeln 368, r8 31, r9 325, W1 0, W1-56 0, Lochscan 0 (G1 ohne Treffer) = Basis (`gate_lauf.json`).
  Hinweis: `pruefung/regeln_letzter_lauf.json` im Repo steht noch auf 372 (alter Lauf vor L3e, G6_facette 217 statt 213); hier
  bewusst nicht nachgezogen (Auftrag: nur viewer_alle.js + p12c).
- D2 (index.html): Positionen ebeb46a1 / 6835acf2 / b33d5a64, Nahtnormalen surface db48c52f – unverändert (`d2_hashes.json`).
  56-Kachel-Hashvergleich D1/G1/D2 identisch zu index.html (`hash_vergleich_D1G1D2.json`).
- index.html, neu/index.html, vektor.json, zellen_relief.csv, felder.json, gen_relief.py unverändert.
- bau_endstand.sh: ENDBAU BITGLEICH – 29/29 Dateien gleich zum Basis-Soll 1778473 (`sha256_bau_p12c.txt`).

## Nahbilder `/workspace/p12c_nahbilder/` (Farbe, nosh=1; vorher = `?wfeld=0`, nachher, ohne Wasser; Blätter in `vergleich/`)
Liste `nahbild_liste.json` (je nah 14–16 m und Distanz 55–60 m).
- **G7-Nord:** nah – Zähnchen/Sägesaum weg, glatte Uferlinie; Distanz – Sägesaum weg, zusätzlich Kachelnaht F7|G7 im Wasser weg.
  Bleibt: feine, glatte hellere Uferlinie (gewollte Ufertönung) und einzelne helle Pünktchen im Wasser westlich (auch vorher).
- **F7/G7-Süd ≈246|279:** nah – Zähnchen weg, Rand weich. Distanz – Saum glatt; **bleiben** 4–5 helle Spitzen im Wasser nahe am
  Ufer (vorher gleich stark). Sie sind auch im reinen Wasserbild als Alpha-Löcher da: Landvertices knapp über dem
  Spiegel im Wasser (Daten, vgl. ERGEBNIS_L3e „Landvertices 0–0,2 m über dem Spiegel“), nicht der Renderer.
- **E7-Rinne x≈218:** nah – Zacken am Rand weg; Distanz – Ufer glatt. Dunkles Band an der Westwand der Rinne bleibt (Gelände).
- **E2-West:** weich wie P12b, Rand gleichmäßiger. **E3:** Bach bleibt durchgehend sichtbar; Zickzack am Westufer bleibt (Geländefarbe,
  Art-Befund aus P12b). **H7:** unverändert gut, Ufer etwas weicher.
