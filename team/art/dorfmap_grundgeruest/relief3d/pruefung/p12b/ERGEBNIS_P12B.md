# P12b-v3 – Wasserrand im 56-Kachel-Viewer weich statt geklemmt

Branch `devui/dorfmap-p12b-v4`, Basis `art/dorfmap-fertig` @ `9742a92` (#28 gemergt); Cherry-Pick von `c53ea45` (v3) ohne Konflikte.
Code aus dem alten Branch `devui/dorfmap-p12b` (61ce08a) übernommen, nur `pruefung/alle_kacheln/viewer_alle.js`.

Kosten: 0 € zusätzlich, Codex: nein (Dev UI selbst), Laufzeit: bau_endstand 389 s / Arbeitszeit ca. 30 min

## Ursache
`viewer_alle.js` baute das Wassernetz aus der Maske WV so: Wasservertices auf WD (O5 senkt flaches Wasser < 0,12 m unter den
Boden), trockene Randvertices auf `min(mittl. WR, GL+0,02)` mit Alpha 0,14, Farbe/Alpha nach ungeglätteter Wassertiefe
(springt an der Maskengrenze, Bett 0,6 m unter Spiegel). Die sichtbare Wasserkante lag damit fest auf dem 0,5-m-Maskenraster → Treppen.

## Umsetzung (`?wrand=0` = alter Zustand)
- Wasservertices auf dem geglätteten Spiegel WR (ohne O5-Absenkung); Maske, Spiegel, Schaum unverändert.
- Ring 1 (trocken, neben Wasser): Spiegel flach fortgesetzt. Boden höher → Gelände schneidet den Spiegel entlang der interpolierten
  Höhenlinie; Boden bis 0,3 m tiefer → Tiefenblende (Alpha × 0,6); tiefer (Klippe/Fall) → wie Ring 2.
- Ring 2 (Außenrand): unter dem Boden (GL − 0,05), Alpha 0.
- Tiefe für Farbe/Alpha 2× 3×3 (4/2/1) weichgezeichnet → Übergang über 1–2 Zellen.
- Kein Wasser entfernt, Flusslauf unverändert (WV/WR nicht verändert, alle Maskenvertices bleiben im Netz):
  alt 31 Meshes / 56110 Dreiecke / 31350 Vertices; neu 32 / 66780 / 36786, davon 31323 mit Alpha > 0,01 (`wasser_mesh_zaehlung.json`). Konsolenfehler 0.

## index.html / Gate-Mesh
Das Klemmen steht auch im Legacy-Pfad von `main.js` (Raster-Wasser), der in index.html hinter dem `RELIEF_NEU_VIEWER`-Return liegt
und nicht erreicht wird; `neu/viewer.js` zeichnet kein Wasser. index.html, neu/index.html und das Bundle bleiben unverändert.

## Nachweise
- Gate (ohne NODE_PATH) je Regel und Trefferliste identisch zu 9742a92: 372 / 31 / 325 / W1 0 / W1-56 0, Lochscan 0.
- D2 bitgleich: index.html unverändert (ebeb46a1/6835acf2/b33d5a64); 56-Kachel-Viewer: Gelände D1/G1/D2 (Positionen, Indizes,
  Farben) identisch zu index.html (`hash_vergleich_D1G1D2.json`, alle_identisch true).
- bau_endstand.sh: ENDBAU BITGLEICH, 25/25 aus leerem Ordner, 389 s auf 9742a92 (Soll-sha256 unverändert gegenüber 9742a92, `sha256_bau_p12b.txt`).

## Nahbilder `/workspace/p12b_nahbilder/` (Farbe, nosh=1; vorher = `?wrand=0` = Stand d301315, nachher, ohne Wasser)
- E2-Westufer: Rastertreppe am Wasserrand → weiche, fast gerade Kante.
- E3-Bach: Blocktreppen am Ostufer weg. Rest am Westufer: dünne dunkle Zickzacklinie, auch **ohne Wasser** sichtbar → steckt in der
  Geländefarbe (VC), Art-Befund. Schmaler Abschnitt z≈100 etwas blasser, bleibt durchgehend sichtbar.
- H7-Bucht: Rasterkanten an Bucht und Inseln weg, Ufer rund, Inseln bleiben.
- G7: Ostteil des Nordufers und Südufer deutlich glatter. **Rest:** am Nordufer westlich x≈265 bleibt eine weichere, aber noch
  erkennbare Treppe. Das Gelände selbst ist dort glatt (Bild ohne Wasser); die Treppe ist der Rand der Wassermaske, über den der
  Spiegel nicht hinausreicht. Versuche (Klippenschwelle aufgehoben; Alpha über weichgezeichnete Bedeckung) änderten links kaum etwas
  bzw. ließen den E3-Bach verblassen und wurden verworfen. Sauber lösbar nur mit einer Wassermaske, die dem Ufer folgt (Art/Daten).
