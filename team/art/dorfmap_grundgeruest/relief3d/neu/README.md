# Gelaendeschicht und gekacheltes Reliefmesh

Ohne `RELIEF_NEU=1` bleiben `gen_relief.py` und `baue_html.py` auf dem
Legacy-Pfad. Mit dem Schalter erzeugt `gen_relief.py` aus `vektor.json`,
`felder.npz` und dem vorhandenen Relief `neu/relief_neu.json.gz`. Der opt-in
Build bindet das Paket in den Three.js-Kernviewer ein und schreibt dieselbe
standalone HTML nach `index.html` und `neu/index.html`.

`neu_mesh_tiles` enthaelt deterministische indizierte Meshes fuer D1, G1 und
D2. D1 und G1 beginnen am sichtbaren Hoehenfeld `GB`: Wege werden an den
Spline mit Laengsprofil und Breite angeglichen, Kreuzungen an eine gemeinsame
Ebene mit Uebergangsrand, Wasser an die vorhandene Wasseroberflaeche und
Bauzonen an ein lokales Hoehenprofil. Wegenden nutzen die in `vektor.json`
abgelegten Auslaeufe. Aenderungen werden an Kachelraendern und im Wandabstand
ausgeblendet. D2 bleibt exakt auf dem sichtbaren `GB`-Quellfeld.

`RELIEF_GELAENDE_VAR=0|1|2` schaltet die drei deterministischen Profilstaerken.
Variante `2` ist Standard: sie veraendert D1/G1-Profilvertices und hatte im
Clay-Vergleich keinen Metrikanstieg gegen Variante `0`. Variante `1` bleibt die
vollstaerkere, getestete Alternative mit sechs Metrikanstiegen. Variante `2`
ist allerdings nur 0,59 mm (D1) bzw. 1,44 mm (G1) stark; die festen
Nahbildkameras zeigen gegen Variante `0` keine geaenderten Pixel. Das Profil
ist im Mesh aktiv, aber dort visuell nicht aufgeloest.
`neu/mesh.py` protokolliert die Delta-Messwerte je Kachel. Zellquellspalten
und das bestehende Relief-Paket werden nicht ueberschrieben.

Die Wandschicht wird aus den Profil-Polylinien in `vektor.json` als separates
Mesh fuer D1 und G1 gebaut; D2 bleibt wandfrei. `WANDVAR=0|1` schaltet die
Breite und Konturvariante. Die Standardvariante wird nach Form-, Bild- und
Clay-Delta-Pruefungen ausgewaehlt. Der Viewer rendert Terrain und Waende als
eigene Three.js-Meshes und weist das LOD1-Dreiecksbudget aus.

Die Tests in `test_neu_kern.py` und `test_wand.py` pruefen deterministische
Mesh-Ausgabe, das D2-Hoehenbyte-Lock, Quellspalten, Wandmeshes und das
Dreiecksbudget. `test_beanstandungen.py` behaelt die festen bestehenden
Schwellen bei; ein Punkt gilt erst als behoben, wenn sein Test gruen wird.
Die Fabianbilder in `referenz_neg/` bleiben unveraenderte Negativreferenzen
und sind keine Geometrieeingabe.
