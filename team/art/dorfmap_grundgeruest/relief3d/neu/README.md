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

`RELIEF_GELAENDE_VAR=0|1|2` schaltet drei reproduzierbare Grundvarianten. `0` ist
das bytegleiche Kontrollmesh. `1` bearbeitet Rampenprofile entlang ihrer
gesamten Laenge. `2` ist die gezielte Grundvariante; die benoetigten
Endpunkt- und Kreuzungskorrekturen sind davon unabhaengig schaltbar. D1/G1
werden messbar angepasst, D2 bleibt bytegleich. Die Messwerte und Grenzen
dieses Worktrees stehen in `pruefung/ERGEBNIS_p3d4.md`; die vorherige
Ausgangsmessung steht in `pruefung/ERGEBNIS_p3d2.md`.

Die gezielten Aenderungen an den Rampenenden und Kreuzungen haben eigene
Schalter: `RELIEF_WEGEND_VAR=0|1|2` und
`RELIEF_KREUZUNG_VAR=0|1|2|3|4|5|8|9|10|11|12|13|14`. Standard ist Wegende `1` mit lokalem,
mindestens 4 m langem Auslauf an den drei D1/G1-Enden mit R8a-Treffern und
Kreuzung `14` in diesem Worktree. Wegende `1` begrenzt die lokale
Laengsneigung auf 0,10; Wegende `2` bezieht zusaetzlich das bereits messbar
unauffaellige Ende `156.5|37.5` ein. Kreuzung `0` nutzt einen 4-m-Rand,
Kreuzung `1` einen 8-m-Rand und Kreuzung `2` eine radiale 3-m-Schulter ohne
Laengsarme. Die Auswahl `2` haelt den D1-Schnittpunkt bei 0,116 m und den
Endpunkt `156.5|37.5` bei 0,188 m. Kreuzung `3`, `4` und `5` loesen das
gemeinsame Laengsprofil von `rampe_2` und `rampe_11` mit den unveraenderten
R3-Formelwerten. Sie mischen das Profil seitlich und laengsgerichtet in die
p3d6-Flaeche und staffeln die ebene Kernflaeche sowie ihren radialen Auslauf.
Variante `5` bleibt die p3d8-Referenz. Die p3d10-Varianten `8`, `9` und `10`
loesen `rampe_2` und `rampe_11` ueber die gesamte jeweilige Polylinie mit dem
R3-Gaussoperator und einer gemeinsamen Ebene im 2-m-Kreuzungsradius. Der
voll gewichtete Wegstreifen ist 1,81 m breit; danach folgt ein 10-m-Hoehenfade.
Variante `8` laesst den wandseitigen Rampenabschnitt frei, `9` haelt `rampe_11`
ab Station 40 fest, und `10` begrenzt dort die Abweichung zur p3d6-Flaeche auf
0,25 m. Varianten `11` und `12` halten die geloesten Rampenprofile an ihren
gemeinsamen Mesh-Abtastpunkten zusammen und uebertragen sie ohne hartes
Umschalten. `12` ist in p3d11 Standard, weil es die Kreuzungsstufe und die
R3-Treffer gegenueber `10` senkt; die geforderten Grenzwerte der Kreuzungsstufe,
Querwoelbung und Achsabweichung werden damit noch verfehlt. Die p3d12-Varianten
`13` und `14` koppeln ausserdem alle nahen 2D-Profilstationspaare (Grenzgefälle
0,60 beziehungsweise 0,45) und begrenzen die Ebenenneigung im 2,25-m-Kern auf
3 Prozent. Profilbeiträge werden auch zwischen Kehrenästen gewichtet gemischt;
die profilabgeleitete Ebene läuft C1-stetig bis 4 m aus. `13` ist der neue
Vergleichswert, `14` ist der Standard, weil sie die Kreuzungsstufe gegenüber
`13` weiter senkt. Variante `10` und die
p3d8-Referenz `5` bleiben auswaehlbar. G1 behaelt bei diesen Varianten
Kreuzung `2`; D2 bleibt geometrisch bytegleich.
`RELIEF_WANDFUSS_VAR=0|1|2` schaltet die separate Wandfuss-Anbindung.
Standard ist Variante `2`: Sie teilt die Wandkontur an jedem Wechsel zwischen
den gerenderten Terrain-Dreiecken und bettet die Unterkante 0,15 m ein. So liegt
jeder Konturabschnitt auf einer einzelnen Terrain-Dreiecksfläche. Variante `1`
verwendet die bisherige Konturabtastung mit derselben 0,15-m-Einbettung; Variante
`0` behaelt das Quellprofil. Keine dieser Schalter aendert Quellzellen oder D2.

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
