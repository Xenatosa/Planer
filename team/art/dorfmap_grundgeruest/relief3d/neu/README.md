# Prototyp fuer den gekachelten Reliefkern

Mit RELIEF_NEU=1 waehlt gen_relief.py den neuen Pythonpfad. Ohne diese
Variable bleibt die bisherige Pipeline Standard. Der Prototyp liest das
exportierte Relief und zellen_relief.csv und schreibt neu/relief_neu.json.gz.
baue_html.py bindet dieses Paket bei demselben Schalter ein. Das Paket
enthaelt unter neu_mesh_tiles je ein deterministisches indiziertes Netz fuer
D2, G1 und D1.

Die Hoehen der Netze stammen direkt aus GB, dem Hoehenfeld, das main.js
tatsaechlich darstellt. G, GB, FW und alle uebrigen Felder bleiben im
Paket bytegleich. Dadurch haben die D2-Vertices dieselben Hoehenbytes wie
die Standardanzeige. Die bestehende Three.js-Pipeline zeichnet die neuen
neu_mesh_tiles-Daten noch nicht; ein Rendereradapter und geaenderte
Geometrie fuer D1/G1 bleiben offen.

test_neu_kern.py prueft deterministische Kachelmeshes, Dreiecksbudget,
D2-Vertexbytes, Zellquellspalten und den Paketgenerator. Die sieben Tests in
test_beanstandungen.py sind absichtlich rot, solange die jeweiligen
Beanstandungen messbar bestehen. Sie messen feste Grenzwerte am Meshfeld oder
an den kopierten Negativbildern.

Die Fabianbilder in referenz_neg/ sind Kopien und stehen mit Kachel,
Koordinate und Fehlerbeschreibung in referenz_neg/Index.csv. Sie dienen als
Negativreferenzen, nicht als Geometrieeingabe; nur der Schattenbildtest liest
ein Bild aus diesem Ordner.
