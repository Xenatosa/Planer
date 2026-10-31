# Relief t41u – Messungen, Annahmen, Abweichungen

## Messungen [S]/[R]
- Wandhöhe = Bandbreite px / 25 [R]: Nord 14 m, Suedgrat 16 m, Krater 11 m, Ostgrat 12 m (vorher 8,6/7,6/7,7/6,7 m).
- Sichtbarer Fels Nordwand ca. 230 px [S], Band 350 px → Perspektivfaktor k ≈ 1,5 [R].
- See 38×35 Zellen → Boden fast von oben gezeichnet; Spanne 9 m (k=1) bis 22 m (67°) [R]. Gewählt: Mitte [A].
- Details: pruefung/klippen_messung_t40u.csv.

## Annahmen [A]
- HANG/SIMS skaliert: positiv ×1,7, negativ ×16/7,6.
- Kraterboden 1 m, Gipfel 14 m, Flussbett 1,5 m, See 3 m tief, Wasserspiegel Boden −0,3 m.
- Sprung > 2,5 m = Felswand, kleiner = Böschung. Sockel bis −30 m.
- Suedgrat + unbenannte Bänder: Höhe per Nachbar-Propagation (Median Suedgrat 14,1 statt gemessen 16).

## Abweichungen von c20 [F]
- Wand steht am Bandfuß; Bandzellen gehören zur oberen Ebene (18752 Zellen umgedeutet).
- Krater-Außenhang senkrecht.
- Zellraster sichtbar: 1-m-Treppen im Grundriss, Wasser als flache Stufen, keine Überhänge.
- E40: 112 Stellen außerhalb der Senke (alter Hinweis, nicht korrigiert).

## t42u – Glättung + c20-Textur
- Höhenfeld G auf 0,5-m-Gitter (673×607 Punkte) [R]: Hänge Gauß σ 1,5 m [A]; an Sprüngen > 2,5 m steile Wand per Smoothstep, Kontur mit Rauschen ±~0,4 m [A].
- Dreieck steiler 55° = Wand (Wandtextur 4×8 m, Box-Projektion), sonst Boden mit c20-Draufsicht [A].
- Bodentextur textur_relief_t42u.jpg: c20 (8 px/Zelle), gemaltes Wandband + Schatten (20524 Zellen) mit Farbe der eigenen Ebene aufgefüllt (unscharf) [A]. c20 unverändert.
- Wandhöhe im Modell (max−min G im 5×5-Fenster an steilen Zellen, Median) [R]: Nord 15,45, Suedgrat 15,0, Krater 11,2, Ostgrat 12,0 m. Nord inkl. Hang am Fuß; Suedgrat 1 m unter Messung 16 (Bandhöhe per Nachbar-Ausbreitung).
- Zellen: hoehe_m = Mittel 3×3 G-Punkte, ecke_* = G, klippe WAND/WAND_OBEN/WAND_FUSS, skin_slot wand_fels bei WAND. Abgleich pruefung/abgleich_t42u.json: 0 Abweichungen.
- OBJ entfällt (nur GLB); alter Stand: ../_alt/relief3d_t41u/.

## t43u
- Suedgrat [R]: Talboden TAL_SUED/untere Bandzellen bis 15 Zellen vom Band um bis zu 16,8 m unter Oberkante abgesenkt, Median klippe_hoehe 16,04 m. 11150 Zellen (Reihen 218–276) mit neuen Hoehenwerten, sonst unveraendert. pruefe_t42u: 0 Abweichungen.
- Bodenfarbe: Material-Gewichte (untergrund, Nass am Wasser, Geroell am Wandfuss) je Vertex, c20 nur 12 % Toenung [A]. Fels per Neigung (smoothstep 0,42–0,74 cos) triplanar [A].
- Bekannte Maengel: Waende wirken noch wie gestempelt (Textur gleichmaessig), Schneeboden flach/eintoenig, Wege-Overlay sehr blass, Haeuser/Baeume sind Platzhalter, Kamera "Am Nordwand-Fuss" hat einen Felsen direkt vor der Linse.


## t44u (Schoenheitsrunden 1-8)
- Zellen/Hoehen unveraendert: pruefe_t42u summe 0 nach jeder Runde [R]. Gelaende-Mesh ohne Gebaeude/Plaetze/Wege; Wege = eigenes Overlay-Mesh, Haeuser = eigene Ebene "gebaeude" [R].
- Wandhoehen-Median neu gemessen (max-min G im 5x5-Fenster an steilen Zellen) [R]: Nord 15,45 / Suedgrat 16,04 / Krater 11,20 / Ostgrat 11,99 m. Soll 14/16/11/12 [R]; Nord +1,45 m, weil das Messfenster den Hang am Fuss mitnimmt (seit t42u bekannt).
- Baeume 1470 seit t43u (dbc41ea) in allen Commits; die Zahl 1482 stammte aus einem nicht eingecheckten Zwischenlauf in t44u Runde 1, nicht aus einem Commit [R].
- Haeuser: Masse, Dachneigung (0,40-0,68 x Breite), Wandhoehe (0,52-0,66 x h), Anbau (45 %), Holzstapel (55 %), Laeden (70 %), beleuchtete Fenster (55 %), Rauch (60 % der Kamine), Wind nach Osten [A].
- Felsen-Groesse auf 2,6 begrenzt und 22 % eingesenkt (keine schwebenden/dunklen Unterseiten) [A].
- Kamera "Am Nordwand-Fuss" sucht automatisch einen Punkt mit freier Sicht 14-34 m vor der Wand [A].
- Sockel-Boden -34 m statt -30 m (tiefste Stelle -29,9 m flimmerte durch) [R].
- Leistung [S]: Desktop 1280x800 1,97 Mio Dreiecke / 19 Draws (Haeuser 80 234); Handy 390x844 ?lod=1 1,36 Mio / 20 Draws.
- Bekannte Restmaengel: Wand-Oberkante treppig (0,5-m-Raster), Wandtextur aus der Naehe netzartig, Haeuser von nahem noch kantig, keine Zaeune, Schnee-Schatten unscharf.

## t44u Runden 9-10
- Zellen/Hoehen unveraendert, pruefe_t42u summe 0 [R]. Glaettung der Abbruchkante und Verrundung der Randkerbe nur im Anzeigenetz (x/z bzw. Absenkung am Kartenrand <=5 m), nicht in G/Zellwerten [A].
- Wandhoehe Messmethode [R]: Soll 14/16/11/12 m = Hoehensprung der Wand selbst. Wandfuss-Zelle Nord (253,29): Sprung zur Nachbarzelle exakt 14,0 m [R]. Der Median 15,45 m (max-min G im 5x5-Zellfenster) nimmt den Hang am Fuss/Kopf mit und ist darum ein Obermass; ein 3x3-Fenster auf Zellmitteln (klippe_hoehe_median_3x3_je_wand) liefert Nord 13,5 / Suedgrat 11,36 / Krater 10,21 / Ostgrat 9,87 m und unterschaetzt durch die Mittelung. Massgeblich ist der Zellsprung; beide Mediane nur Kontrolle [A].
- Zaeune [R]: 1480 Segmente geprueft, 1101 gebaut; Regel [A]: Abstand 1,8 m ums Haus, Tuerseite offen, kein Segment auf Wegzelle, nicht naeher als 0,9 m an anderem Haus/Platz, Hoehenunterschied <0,5 m, Abweichung zu Hausboden <1,2 m.
- Schatten [A]: bias -0,0003, normalBias 0,12, radius 1,6, Frustum +-238 m.
- Sockelseiten/Unterseite: Gesteinsschichten per Shader (Dicke 3,1 m und 0,8 m, gewellt) [A].
- Final (Runde 11) [S]: Desktop 1280x800 2,08 Mio Dreiecke / 20 Draws (Haeuser 163 696); Handy 390x844 ?lod=1 1,47 Mio / 21 Draws (vorher e6111b1: 1,36 Mio / 20) -> +8 %, +1 Draw (Zaun-Mesh).
- Wandhoehen [R]: Zellsprung Nord 14,0 m; Median 5x5 Nord 15,45 / Suedgrat 16,04 / Krater 11,20 / Ostgrat 11,99 m (unveraendert, Messmethode s.o.).
- Restmaengel final: Kerbe am Flussaustritt hinten noch V-foermig gerade geschnitten; Wandoberkante aus der Naehe noch leicht gezackt; Dachschnee flaechig hellgrau ohne Struktur; Schnee-Schatten weiterhin weich; Hauswaende glatt (keine Putztextur).

## t47u/t48u Runde 1 (31.10.2026)
- Fluss: 4 Lücken aus c20 geschlossen (x213 y9–18, x219 y229–238, x74 y263–265, x323–327 y268); Hauptfluss jetzt 1 Zusammenhang (6005 Zellen) [S]. wasser_eis/fluss_id/untergrund konsistent (0 Abweichungen) [S]. 7-m-Stufe bei x220 y227 zu Stromschnellen verteilt, größter Spiegelsprung jetzt 1,8 m/Zelle [S].
- Felsform: mehrskaliges Rauschen (Rippen/Runsen), Simse, Schuttfuß [A]. Wirkung im Bild noch gering.
- Krater: Flanken geböscht [A]; noch kein Zugang, noch zu gleichmäßig.
- Offen: Rampen/Serpentinen, 0,25-m-Gitter/Detailnormalen, Felsblöcke statt Wandflächen, fleckiger Schnee mit Gras (Maßstab: referenz/fabian_beispiel_t48u.jpg).

## t48u Runde 3/4 (eb3c248)
- Neu: Ufersteine, Baumgruppen an Klippenkanten, Trockengras-Büschel (instanziert), Kraterkrone nur fleckig Fels, Schaum an Wasserstufen, ferne Berge heller/dunstiger.
- [S] pruefe_t42u summe 0. [S] Desktop 2.474.980 Dreiecke / 26 Draws. Handy nicht neu gemessen.
- Offen/ehrlich: Felsblöcke wirken noch kastig (Quader, zu einheitlich), Bäume im Schatten fast schwarz, Rampen kaum sichtbar, Kraterring noch ohne klare Rippen/Scharten, kein GLB-Export, keine Detail-Normalmap. opensimplex per pip blockiert (PEP 668) → eigenes numpy-fBm; Blender nicht verfügbar.

## t48u Abschluss (R5-R8 + Endpruefung)
- [S] pruefe_t42u summe 0. Wandhoehen-Feld 14/16/11/12 m; Fenster-Median (pruefe_final_t48u.py) Nord 14.0, Suedgrat 16.8, Krater 14.0 (Fenster-Methode ueberhoeht), Ost 12.0.
- [S] Wasser alle IDs 8er-Nachbarschaft: Hauptstueck 6005 Zellen zusammenhaengend; 28 kleine Reststuecke (groesstes 383). Einzelne fluss_id sind zerstueckelt (BACH_SUED 58 Teile), haengen aber ueber andere IDs zusammen.
- [S] Headless: alle 11 Kameras gerendert, fehler [] (Teil 3 geloggt; Teile 1+2 schrieben alle Bilder, hingen danach beim Beenden -> abgebrochen, kein Log).
- [S] Desktop 3 563 681 Dreiecke / 31 Draws; Handy ?lod=1 390x844 1 860 203 / 32 Draws; GLB ?glb=1 laedt (2 Meshes, 2.3 s).
- Abweichung zum Beispielbild: weiterhin stilisiert/low-poly (kantige Felsen, einfache Baeume), kein Foto-Realismus; Fernberge wirken wie gezackte Papierkulisse.

## t53u Gelaendeform
- R6 [S]: Handy ?lod=1 (390x844) 1 163 663 Dreiecke gerendert (vorher 1 871 723), 32 Draws. Felsen Ikosaeder Detail 1, Fichten 6 statt 9 Zweige, 1/3 Geroell. Messung `test_budget.js`.
- R5: Fernberge Hoehenfeld-Ring R 120-2600 m, 4 Oktaven gerundet, grauer Fels; blauer Ring war die Luecke zwischen Kartenrand und Ring-Innenkante (R0 420) -> geschlossen. Ring wird ausgeblendet, wenn Kamera unter -30 m (Ansicht unten).
- Offen: R1 Klippen-Silhouetten/Ueberhaenge, R2 Kraterring-Zugaenge, R3 Serpentinen als Terrain-Rampen, R4 Flussbett/Ufer. Nicht bearbeitet.

## Runde J (t62u) – Wasserlauf
- [A] J1: Der Wasserlauf ist neu gelegt, als Kaskaden im Talboden (fluss_t62u.fluss_kaskade). Wasser am Hang und am Wandfuss des Klippenbandes VB wurde Land. Ein Verbindungskanal (Dijkstra, Bett 0,35 m) hält den Fluss durchgehend. Tiefster Schnitt 1,26 m (Runde I: 8,9 m).
- [A] J2: Zwei kleine Hangwasser-Stücke (21 und 32 Ecken) sind weggefallen.
- [A] J3: Objekte, die im Wasser standen, wurden verschoben oder entfernt: Bäume 28/2, Felsen 2/0, Steine 649/101, Geröll 9/0. In relief_zaehlung.json stehen dadurch bewusst neue Zahlen: baeume 1969→1967, steine 1133→1032. Zellwerte, CSV und grobe glb sind byte-gleich.
- [A] J4: Kein Weg-Overlay wurde verschoben. VB ist das Klippenband und kein Weg.
- [S] J5: Der Fluss kreuzt weiter zwei Wasserscheiden (Strang 13, wie schon in Runde I). Gemessen mit Becken als Senken gibt es 0 Bergauf-Stellen. 22 Becken haben keinen Randabfluss (Endseen). Es gibt Stufen bis 3,54 m (Wasserfälle).
- [S] J6 Raycast (Viewer-Oberfläche): 0 Objekte schweben (>0,3 m). Versunken (>0,5 m): 2 Bäume und 1 Geröll, maximal 0,57 m. Im Wasser stehen 2 Bäume (5–20 cm tief, offen), 144 Steine und 3 Geröll (Bett-/Uferkiesel, ≤0,3 m überflutet).
- [A] J7: Mit 7b19ec9 sind versehentlich zwei __pycache__-.pyc-Dateien eingecheckt. Sie sind harmlos und nicht gelöscht (Regel: nichts löschen).
## Runde K (t63u) – Westarm um die Hügel
- [F] K0: Fabian hat entschieden (t62u): Der Fluss soll im Tal um die Hügel herum fließen. Basis ist 18f24ac. Der alte Stand liegt in git, gelöscht wurde nichts.
- [S] K1: Strang 13 (Westarm, etwa (72,46)→(264,260)) läuft neu durch das westliche Tal (fluss_k.py). Talweg 253 Zellen, Flusslänge 286 m, tiefster Schnitt 1,47 m. 1273 alte Wasserzellen wurden Land (SCHNEE 1223, WALD 50), 1416 Zellen wurden neu Wasser, 47 blieben Wasser. Insgesamt haben sich 7390 Zellen geändert, davon 4701 nur in der Höhe (+5,21/−2,73 m). Bbox x 0–85, y 36–267. Außerhalb des Westbereichs sind es 102 Zellen, alle an der Mündung (y≈262–267). Liste: pruefung/zellen_aenderung_t63u.csv.
- [S] K2: Der Wasserspiegel fällt jetzt überall monoton (spiegel_monoton). Bergauf-Stellen: 0 (Runde J 16044). Stufen über 1 m gibt es nur in der Schlucht-Rinne über die Südgrat-Wand (x 210–220, z 220–227): 18 Stück, maximal 3,31 m. Außerhalb davon ist die größte Stufe 0,77 m. Für die Rinne wurde der Spiegel um bis zu 6,15 m abgesenkt, und zwar nur dort.
- [S] K3: Kreuzungen mit dem neuen Wasser: Wege 0, Rampen 0, Häuser 0, Overlay-Plätze/Wege/Brücken/Furten 0. Darum sind keine Marker nötig (pruefung/kreuzung_t63u.json). Hausflächen, die Wasser berühren: 1 (Runde J 9). Das ist N44 Hütte am bestehenden Endsee (Stück 11).
- [S] K4: Objekte. Bäume an Hängen über 45° wurden entfernt: 30. Bäume am Wasserrand: 10, im Wasser: 1. Steine im Wasser: 100. Bäume gesamt 1967→1873. Raycast (pruefung/strahl_t63u.json): Bäume schwebend 0, versunken 0, im Wasser 0. Steine schwebend >0,3 m: 6 (max 0,43 m, offen). Geröll versunken >0,5 m: 3 (max 0,79 m).
- [S] K5: Mesh-Lücke 0 (LS1/LS2). t42u-Abgleich summe=0 (neu gebaselined). Handy ?lod=1: 1 089 795 Dreiecke (<1,3 M).
- [A] K6: Die Startpunkte der Erosion sind eingefroren (erosion_start_t63u.npy). Ohne das hätte sich die ganze Karte um etwa 0,1 m verschoben.
- [S] K7: Ehrlich offen: Der Südfluss ist auf etwa 360 m eine flache Strecke auf −18 m und wirkt wie stehendes Wasser.
