# Gelaendeschicht und gekacheltes Reliefmesh

Ohne `RELIEF_NEU=1` bleiben die bestehenden `gen_relief.py` und `baue_html.py`
der Standard. Mit dem Schalter erzeugt `gen_relief.py` aus `vektor.json`,
`felder.npz` und dem vorhandenen Relief das Paket `neu/relief_neu.json.gz`.
`baue_html.py` schreibt dazu den eigenstaendigen Three.js-Viewer
`neu/index.html`.

`neu_mesh_tiles` enthaelt deterministische indizierte Meshes fuer D1, G1 und
D2. D1 und G1 beginnen am sichtbaren Hoehenfeld `GB`: Wege werden an den
Spline mit Laengsprofil und Breite angeglichen, Kreuzungen an eine gemeinsame
Ebene mit Uebergangsrand, Wasser an die vorhandene Wasseroberflaeche und
Bauzonen an ein lokales Hoehenprofil. Wegenden nutzen die in `vektor.json`
abgelegten vier Meter Auslaeufe. Aenderungen werden an Kachelraendern und im
Wandabstand ausgeblendet. Der ausgewiesene Punkt D1 (140,35) bleibt auf den
Quellbytes.

D2 wird aus `GB` kopiert, ohne Aenderung. Der Viewer prueft beim Laden die
D2-Hoehenbytefolge und verwendet D1/G1/D2-Vertices im vorhandenen
Three.js-Gelaendenetz. Damit wird die Mesh-Geometrie gezeichnet und auch im
LOD-Aufbau verwendet; Zellquellspalten und bestehende Relief-Felder werden
nicht ueberschrieben.

`RELIEF_GELAENDE_VAR=0` ist die Standardvariante und exportiert die
unveraenderten Quellhoehen als Kontrollmesh. `=1` schaltet die volle
Profilstaerke ein; `=2` gewichtet sie mit 0,02. Beide Profilvarianten hatten
kleine positive Clay-Facetten-Deltas in D1/G1 und sind daher nicht die
Standardauswahl. Alle drei Varianten sind deterministisch und ueber die
Umgebungsvariable schaltbar.

`neu/tests/test_neu_kern.py` prueft deterministische Dreiecksnetze,
D2-Vertexbytes, Quellspalten, D1/G1-Profilbildung und den Paketgenerator.
Die Tests unter `test_beanstandungen.py` verwenden weiterhin die festen
Schwellen des bestehenden Regelwerks; ein Mesh-Fix wird dort erst als behoben
gezaehlt, wenn die zugrunde liegende Messung die Grenze erreicht.

Die Fabianbilder in `referenz_neg/` sind unveraenderte Negativreferenzen und
keine Eingabe fuer die Geometrie.
