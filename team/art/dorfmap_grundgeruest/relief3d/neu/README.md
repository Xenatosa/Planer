# Gelaendeschicht und gekacheltes Reliefmesh

Ohne `RELIEF_NEU=1` bleiben `gen_relief.py` und `baue_html.py` auf dem
Legacy-Pfad. Mit dem Schalter erzeugt `gen_relief.py` aus `vektor.json`,
`felder.npz` und dem vorhandenen Relief `neu/relief_neu.json.gz`. Der opt-in
Build bindet das Paket in den Three.js-Kernviewer ein und schreibt dieselbe
standalone HTML nach `index.html` und `neu/index.html`.

`neu_mesh_tiles` enthaelt deterministische indizierte Meshes fuer D1, G1 und
D2. D1 und G1 beginnen am sichtbaren Hoehenfeld `GB`. Strassen bekommen ein
Laengs- und Querprofil; Rampenprofile laufen an den Enden mindestens 4 m weich
aus. Erkannte Rampenkreuzungen erhalten eine gemeinsame ebene Flaeche mit
weichem Rand. Wasser und Bauzonen behalten ihre bisherigen lokalen Profile.
Die Rampenprofile duerfen im Anschlussbereich an die Wandfuesse das bisherige
Wand-Abstandsschutzgewicht ueberstimmen; eine lokale Sperre schuetzt die
Klippenform bei D1 (140,35). Kachelraender bleiben auf der Quelle. D2 bleibt
exakt auf dem sichtbaren `GB`-Quellfeld.

`RELIEF_GELAENDE_VAR=0|1|2` schaltet drei reproduzierbare Varianten. `0` ist
das bytegleiche Kontrollmesh. `1` bearbeitet Rampenprofile entlang ihrer
gesamten Laenge. `2` ist die gezielte Standardvariante: Rampen werden an den
Endbereichen profiliert und die erkannte D1-Kreuzung wird gemeinsam abgeflacht.
Variante `2` reduziert die D1-Kreuzungsstufe im Neu-Mesh von 1,746 m auf
0,087 m. D1/G1 aendern sich messbar (max. |Delta| 3,311 m bzw. 0,243 m); D2
bleibt bytegleich. **Die Clay-Delta-Pruefung gegen Variante 0 meldet weiterhin
positive Bildmetriken; Variante 2 erfuellt den Bild-Delta-Abbruch nicht.**
Details und Grenzen stehen in `pruefung/ERGEBNIS_p3d2.md`.

`pruefung/neu_mesh_adapter.py` adaptiert das `neu_mesh_tiles`-Hoehenfeld in die
historischen Gate-Eingaben `G`, `GB` und die D1/G1-Stuetzstellen von `FW`.
Pruefer und Schwellen bleiben unveraendert; D2 und alle anderen Quellen werden
im Adapter unangetastet gelassen. Beispiel: `python3 pruefung/neu_mesh_adapter.py
--mesh neu/relief_neu.json.gz --out /tmp/neu_mesh_gate.json.gz`.
`neu/mesh.py` protokolliert die Delta-Messwerte je Kachel. Zellquellspalten
und das bestehende Relief-Paket werden nicht ueberschrieben.

Die Wandschicht wird aus den Profil-Polylinien in `vektor.json` als separates
Mesh fuer D1 und G1 gebaut; D2 bleibt wandfrei. `WANDVAR=0|1` schaltet die
Breite und Konturvariante. Die Standardvariante wird nach Form-, Bild- und
Clay-Delta-Pruefungen ausgewaehlt. Der Viewer rendert Terrain und Waende als
eigene Three.js-Meshes und weist das LOD1-Dreiecksbudget aus.

Die Tests in `test_neu_kern.py`, `test_wand.py`, `test_gelaende_mesh.py` und
`test_mesh_gate_adapter.py` pruefen deterministische Mesh-Ausgabe, D2-
Hoehenbytes, Quellspalten, Adapterpfad und Dreiecksbudget. `test_beanstandungen.py`
fuehrt die unveraenderten Gate-Schwellen auf den adaptierten Neu-Mesh-Daten aus.
Die Fabianbilder in `referenz_neg/` bleiben unveraenderte Negativreferenzen
und sind keine Geometrieeingabe.
