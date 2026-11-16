# AUSNAHMEN L3d

## G7-Nordufer westlich x≈265 (Stelle G7_nord) – zweimal gescheitert, Stelle aus

- Befund: Der Nordrand des Wassers zwischen x 244–265, z 254–270 folgt dem Raster der Wassermaske (WV>-900).
  Mit dem gemergten weichen Wasserrand (P12b, 2771f70) ist die Treppe zu kleinen Zacken weichgezeichnet (Periode ≈ 0,5 Zellen = 1 Vertex), aber noch erkennbar
  (Nahbilder `l3d_nahbilder/G7_nord_akt_*_vorher.jpg`, `G7_nord_oben_akt_*_vorher.jpg`, Paar `paar_G7_nord_gross.jpg`).
- Versuch 1 (`relief_l3d.py`, Art „wassermaske“, ueber_spiegel_m 0,25): Maske waechst in angrenzendes Land, bis das Gelaende 0,25 m ueber dem Spiegel liegt
  → 29 neue Wasservertices. Treppe im P12b-Viewer und im alten Viewer unveraendert.
- Versuch 2 (ueber_spiegel_m 0,5): 75 neue Wasservertices, Maske 2 Vertices weiter am Ufer → die Zacken wandern nur mit und bleiben sichtbar.
- Ursache: Der sichtbare Rand ist der Maskenrand selbst (Rastervertex an/aus); solange das Gelaende dort nahezu auf Spiegelhoehe liegt, bleibt jede Maskenkante sichtbar. Ohne Viewer-/Prueferaenderung (verboten) nicht weiter loesbar.
- Ergebnis: Stelle in `pruefung/l3d/l3d_stellen.json` mit `"aktiv": false` und beiden Versuchen dokumentiert. WV/Wassermaske bleiben bitgleich zu 2771f70 (Beleg `l3d_abstaende.json`: maske_gleich, wv_gleich, fill_holes_gleich, 9/9 Komponenten).
- Gate: keine Treffer in G7_nord vorher/nachher (G8 1→1, R6 4→4).

## QA P4d S8 G7 ≈255|282 – nicht reproduzierbar
- Daten: im Umkreis 10 m keine eingeschlossene Landinsel und kein Bettvertex ueber dem Spiegel; 255|282 liegt ≈2,1 m ueber dem Spiegel auf dem Suedufer-Hang (Land, kein Fluss).
  Suche ueber den ganzen Fluss Reihe 7 nach Bett ≥ Spiegel−0,1 m im Wasserinneren: nur 331|266,6 (Hangfuss unter Wasser, Wasser dort unsichtbar, nicht Teil des Befunds).
- Nahbild `l3d_nahbilder/S8_G7_255_282_akt_*_vorher/_nachher.jpg`: keine Platte sichtbar. Keine Aenderung, bitte bei QA mit genauerem Punkt nachpruefen.

## Neue Gate-Treffer
Keine. Gate 372 → 369 (nur G6_facette 217 → 214, drei Treffer in E3 weg, kein neuer Treffer; auch nach der P4d-Erweiterung).
