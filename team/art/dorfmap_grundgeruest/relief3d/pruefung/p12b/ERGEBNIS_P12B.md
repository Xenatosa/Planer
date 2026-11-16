# P12b – Wasserrand im 56-Kachel-Viewer weich statt geklemmt

Branch `devui/dorfmap-p12b`, Basis P12 (`devui/dorfmap-p12`, PR #24) → P11b-v2 (PR #23) → `d5b17e2` (art/dorfmap-fertig).
- **Abhängigkeit:** nach #23 und #24 mergen.
- L3c (#22, noch offen) ist nicht enthalten. Die Änderung betrifft nur den Renderer und gilt für jeden Datenstand.

## Ursache (Befund Art L3c / #22)
`viewer_alle.js` hat das Wassernetz aus WV bisher so gebaut:
- Wasservertices liegen auf WD. Darin steckt die O5-Absenkung: Wasser, das flacher als 0,12 m ist, wird unter den Boden gelegt.
- Trockene Randvertices liegen auf `min(mittl. WR, GL+0,02)`, mit Alpha 0,14.
- Farbe und Alpha richten sich nach der Wassertiefe je Vertex. An der Maskengrenze springt diese Tiefe, weil das Bett 0,6 m unter dem Spiegel liegt.

Dadurch saß die sichtbare Wasserkante fest auf den Vertices der 0,5er Maske, und es entstanden Treppen (E2-West, E3, H7-Bucht und Ufer allgemein). Ohne Wasser ist das Gelände dort glatt (`/workspace/p12b_nahbilder/ohne_wasser/`).

## Umsetzung (`pruefung/alle_kacheln/viewer_alle.js`, Schalter `?wrand=0` = alter Zustand)
- **Wasservertices** liegen auf dem geglätteten Spiegel WR, die O5-Absenkung entfällt. Maske, Spiegel und Schaum sind unverändert.
- **Ring 1** (trocken, neben Wasser): Der Spiegel wird flach fortgesetzt (Mittel der WR-Nachbarn).
  - Liegt der Boden höher, schneidet das Gelände den Spiegel entlang der interpolierten Höhenlinie statt entlang des Rasters.
  - Liegt der Boden bis 0,3 m tiefer, gibt es eine Tiefenblende (Alpha × 0,6).
  - Liegt er tiefer (Klippe oder Fall), wird Ring 1 wie der Außenrand behandelt.
- **Ring 2** (Außenrand des Netzes): unter dem Boden (GL − 0,05), Alpha 0.
- **Tiefenblende:** Die Wassertiefe je Vertex wird zweimal mit 3×3 (Gewichte 4/2/1) weichgezeichnet und nur für Farbe und Alpha genutzt. Der Übergang reicht damit über 1–2 Zellen statt über eine Rasterkante.
- **Kein Wasser entfernt:** Alle Maskenvertices bleiben im Netz.
  - Netz alt: 31 Kacheln mit Wasser, 56062 Dreiecke, 31338 Vertices.
  - Netz neu: 32 Kacheln (Ring 1 reicht in eine Nachbarkachel), 66772 Dreiecke, 36786 Vertices, davon 31286 sichtbar (Alpha > 0,01).
  - Der Flusslauf ist unverändert (WV und WR werden nicht verändert). Belege: `wasser_mesh_zaehlung.json`.

## Gate-Mesh / index.html
Das Klemmen steht auch in `main.js` (Zeilen 240/241, Legacy-Raster-Wasser). Dieser Pfad ist in index.html nicht erreichbar: Er liegt hinter `if(window.RELIEF_NEU_VIEWER){… renderNeuCore …; return;}` (Zeile 19). `neu/viewer.js` (Gate-Mesh-Viewer) zeichnet kein Wasser.
- Deshalb ist **index.html unverändert**. Bundle-sha256 = `21f9a79951bd4a6e8a2ba8ca73a5f6e17518933115b10c67302c00a574f6dab1` (Stand P12, `pruefung/p12/bundle_sha.py`).
- `bau_endstand.sh` liefert danach alle 20 Ausgaben bitgleich (Lauf siehe unten).

## Nachweise
- **Gate je Regel und Trefferliste** identisch: 374 / 33 / 325 / W1 0 / W1-56 0.
- **D2 bitgleich:**
  - Geometrie: index.html ist unverändert (ebeb46a1/6835acf2/b33d5a64).
  - 56-Kachel-Viewer: der Hash-Vergleich meldet D1/G1/D2-Gelände und Wände identisch zu index.html (`hash_vergleich_D1G1D2.json`).
  - Geändert ist nur das Wassernetz (Geometrie und Vertexfarben/Alpha) im 56-Kachel-Viewer. Am Gelände-Material und an den Shadern ändert sich nichts.
- **Nahbilder** liegen in `/workspace/p12b_nahbilder/` (Farbe, nosh=1; vorher = `?wrand=0`). Sammelblätter in `vergleich/`, Listen in `nahbild_liste*.json`.
  - **E2-Westufer:** Die harte Rastertreppe am Ostrand des Wassers ist zu einer weichen, fast geraden Kante geworden (Ausschnitt `E2_ausschnitt_vorher_nachher_ohneWasser.png`). Der helle Film am Westrand ist weg.
  - **E3-Bach:** Die Blocktreppen am Ostufer sind weg, der Rand ist weich.
    - Rest: Am Westufer bleibt eine dünne dunkle Zickzacklinie. Sie ist auch **ohne Wasser** sichtbar, steckt also in der Gelände-Farbe (VC), nicht im Renderer → Art.
    - Der schmale Abschnitt bei z ≈ 100 ist durch die Tiefenblende etwas blasser, aber durchgehend sichtbar.
  - **H7-Bucht Südost:** Die Rasterkanten der Bucht und der Inseln sind weg, die Ufer sind rund. Die Inseln bleiben.
  - **Übersicht E7–H7 und G7:** Die Ufer sind glatter; Schaumlinien, Inseln und Wasserfälle sind unverändert. Schwebende Wasserflächen sind nicht zu sehen.
- `bau_endstand.sh` auf diesem Stand: ENDBAU BITGLEICH, 20/20, 280 s (`sha256_bau_p12b.txt`).
