# Prototyp fuer den gekachelten Reliefkern

Mit RELIEF_NEU=1 waehlt gen_relief.py den neuen Pythonpfad. Ohne diese
Variable bleibt die bisherige Pipeline Standard. Der Prototyp liest das
exportierte Relief und zellen_relief.csv und schreibt neu/relief_neu.json.gz.
baue_html.py bindet dieses Paket bei demselben Schalter in main.js ein. Der
Viewer zeichnet echte Meshes fuer D2, G1 und D1; die HTML-Datei bleibt offline
nutzbar.

Die Oberflaechenhoehen von D1/G1 stammen aus den unveraenderten Zellhoehen,
gemittelt auf ein 1-m-Vertexraster. D2 nutzt die GB-Vertices des bestehenden
Reliefs unveraendert auf 0,5-m-Raster. G, GB, FW und alle uebrigen Felder
bleiben im Paket bytegleich. D2 hat keine Wandschicht; seine
Oberflaechen-Vertices bleiben bytegleich zum Quellfeld.
Die Wandschicht wird aus `vektor.json`-Polylinien mit oberem/unterem Profil
und Mindestbreite als eigenes geschlossenes Mesh fuer D1 und G1 gebaut.
`WANDVAR=1` ist die Standardvariante (Profil-Mindestbreite), `WANDVAR=0`
schaltet die breitere 2,4-m-Variante.

test_neu_kern.py prueft deterministische Kachelmeshes, Dreiecksbudget,
D2-Vertexbytes, Zellquellspalten und den Paketgenerator. `test_wand.py` prueft
die profilierten D1/G1-Wandmeshes und das leere D2-Wandmesh. Die sieben Tests in
test_beanstandungen.py sind absichtlich rot, solange die jeweiligen
Beanstandungen messbar bestehen. Sie messen feste Grenzwerte am Meshfeld oder
an den kopierten Negativbildern.

Die Fabianbilder in referenz_neg/ sind Kopien und stehen mit Kachel,
Koordinate und Fehlerbeschreibung in referenz_neg/Index.csv. Sie dienen als
Negativreferenzen, nicht als Geometrieeingabe; nur der Schattenbildtest liest
ein Bild aus diesem Ordner.
