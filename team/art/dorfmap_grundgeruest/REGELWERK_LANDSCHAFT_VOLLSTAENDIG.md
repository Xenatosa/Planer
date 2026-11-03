# Vollständiges Formregelwerk Landschaft

Stand: 03.11.2026 · Datenstand: `art/dorfmap-regelwerk` auf Basis `9d3f8fc` · Koordinaten: x/z in Metern, y/Höhe in Metern

Dieses Regelwerk legt messbare Formen und Maße für alle in den Zellen und Reliefdaten vorkommenden Landschaftselemente fest. Die Kürzel `LF01–LF24` und `TR01–TR06` sind Sollcodes; die Tabelle in Abschnitt 6 nennt pro Kachel genau die dort ermittelten Elemente und ihre Sollcodes.

## 1. Quellen, Herkunft und Verbindlichkeit

- `[S]` bezeichnet einen Wert, der in den gepflegten Quelldokumenten oder Reliefdaten steht beziehungsweise dort direkt gemessen wurde.
- `[R]` bezeichnet einen Wert, der aus Kartenpixeln, Zellrastern oder Reliefkoordinaten berechnet wurde.
- `[A]` bezeichnet einen festgelegten Platzhalter oder eine Annahme, für die keine messbare Maßangabe in der Dorfkarte vorliegt. Der hier genannte Grenzwert ist trotzdem verbindlich.
- Die Kartenquelle setzt 25 px/m und ein nominales Zellmaß von 1 m fest. Das Raster hat 336 × 303 Zellen; die letzte Bildzeile ist 0,4 m hoch. Die Kachelzuordnung lautet `"ABCDEFGH"[x//42] + str(z//43+1)`. Damit sind die Kacheln 42 × 43 nominale Rastermeter groß; H7 enthält den südlichen Kartenrest. `[S/R]`
- Die Reliefdaten liegen auf einem 0,5-m-Gitter (`rs=2`). Die Ist-Messung dieses Dokuments verwendet das sichtbare Höhenfeld `GB`, Wasseroberfläche `WV`, `zellen_relief.csv` und die serialisierten Wege und Objekte aus `relief_daten.json.gz`. Alle Eingaben bleiben unverändert.
- `SPEC.md` führt die Kartenmessungen und Rasterwerte auf. Die ursprüngliche Master-PNG-Datei wird in diesem Worktree nicht mitgeführt. Pixelmaße in diesem Dokument sind deshalb nur dort als `[R]` übernommen, wo `SPEC.md` oder `ABWEICHUNGEN.md` bereits Maßstab und Rechnung dokumentieren. Nicht dokumentierte Bildmaße werden als `[A]` geführt.
- Für Plateauhöhen stehen in `SPEC.md` ältere Werte von +8,6 m (Nord) und +6,7 m (Ost) neben den späteren Wandhöhen-Sollwerten aus `relief3d/ABWEICHUNGEN.md`. Dieses Regelwerk verwendet die später dokumentierten Sollwerte +14 m und +12 m; das gemessene `GB` hat dort Mediane 13,9995 m (9 917 Zellen) und 11,9993 m (4 227 Zellen). Die Versionsdifferenz bleibt als Quellenkonflikt markiert.
- `PLAN_O18_NEU.md` liefert die O18-Grenzwerte für Kreuzung, Wegende, Delle, Sägezahn und Hangwellen. Der Plan kennzeichnet sich als Analyse, die auf Freigabe wartet; die hier genannten Sollwerte sind als messbare Formregeln dokumentiert, nicht als Behauptung, dass die bestehende Geometrie sie erfüllt.
- `relief3d/README.md` und `ABWEICHUNGEN.md` liefern den aktuellen Modellstand, gemessene Wandhöhen und die Platzhalter-Eigenschaft von Bäumen und Häusern. `MATERIALFLAECHEN.md` enthält keine zusätzlichen Formmaße; Material- und Texturvorgaben daraus sind gemäß Auftragsumfang nicht übernommen.
- Die Datei `relief3d/REGELN_VERPFLICHTEND.md` enthält an diesem Stand die Regeln R8a und R8b. Die Prüfskripte enthalten weitere R-, G- und T-Messungen. Dieses Dokument ergänzt die Form-Sollwerte. T1–T6 bleiben außerhalb dieses Formkatalogs, da sie Darstellung/Farbe prüfen.

### Messdefinitionen

- `Neigung` ist `atan(|gradient(GB)|)` in Grad; Höhengradienten nutzen Meterabstände.
- `Rauheit R1` ist `abs(GB − Gauss(GB, σ=1 m))` in Metern.
- `Effektiver Krümmungsradius` ist `1 / max(abs(Hauptkrümmung))`; ausgegeben werden Punkte mit Krümmungsbetrag mindestens 0,02 1/m. Er ist ein aus dem Höhenfeld berechneter Flächenradius, kein Radius eines Steins oder Gebäudes.
- Verteilungen stehen als `P5 / Median / P95`, jeweils in der genannten Einheit. `n` ist die Anzahl der gemessenen Gitter- oder Objektwerte. Die ausführbare, schreibgeschützte Messung ist `relief3d/pruefung/regelwerk_messung.py`.
- Objekt-`size_parameter` und `height_parameter` sind die im JSON gespeicherten Skalare. Sie sind keine vollständigen Mesh-Begrenzungsboxen. Die bestehende Objektprüfung `G11` misst Lagefehler; ein Mesh-Bounding-Box-Gate ist noch nicht vorhanden.

## 2. Kartenmaße und Elementverteilungen (Ist)

Die Werte dieser Tabellen sind das Ist des Reliefstands vor der Dokumentänderung. Die Sollwerte stehen jeweils daneben in Abschnitt 3–5.

| Element | Ist Höhe GB P5/Median/P95 (m) | Ist Neigung P5/Median/P95 (°) | Ist Rauheit R1 P5/Median/P95 (m) | Ist Radius P5/Median/P95 (m) | Messumfang |
|---|---:|---:|---:|---:|---|
| Landschaft, gesamtes trockenes Gelände | −16,0844 / 0 / 13,9997 | 0 / 0,9588 / 52,0383 | 0 / 0,0177 / 1,0673 | 5,2227 / 25,6814 / 45,8831 | 383 237 Gitterpunkte |
| Plateau, 4 m vom Zellenklassenrand | 11,9958 / 13,997 / 14 | 0 / 0,0006 / 6,1502 | 0 / 0,0009 / 0,1689 | 22,8433 / 33,2549 / 47,6936 | 44 386 Punkte; 14 144 Quellzellen |
| Hang, Zellenklasse HANG | −12,9333 / −7,5387 / 6,0991 | 0,439 / 7,6014 / 54,4497 | 0,0005 / 0,0723 / 0,8586 | 7,3536 / 28,1176 / 46,5752 | 78 491 Punkte; 21 086 Quellzellen |
| Gebirge, benannte Wandzonen und Krater/Gipfel/Sims | −14,7275 / 8,7457 / 14 | 0 / 13,9354 / 70,5724 | 0,0004 / 0,1887 / 1,9787 | 4,1238 / 19,1372 / 44,8102 | 80 422 Punkte; 20 099 Quellzellen |
| Klippe/Wand, WAND-Markierung | −11,8196 / 3,8091 / 11,6525 | 7,6646 / 52,0827 / 78,9124 | 0,0313 / 0,8062 / 2,6799 | 3,6556 / 12,7392 / 40,7947 | 29 697 Punkte; 7 435 Quellzellen |
| Wandkrone, WAND_OBEN | −7,7895 / 8,5192 / 12,9975 | 5,1292 / 21,3775 / 53,0791 | 0,0836 / 0,7806 / 2,1553 | 3,6334 / 9,168 / 34,5608 | 9 017 Punkte; 2 255 Quellzellen |
| Wandfuß, WAND_FUSS | −14,9216 / 1,387 / 6,3247 | 1,8686 / 35,8921 / 65,8364 | 0,0786 / 0,714 / 2,1302 | 4,5813 / 11,0627 / 34,2666 | 9 975 Punkte; 2 503 Quellzellen |
| Rampen, 13 Mittellinien | −13,4107 / 3,8277 / 11,4866 | 3,172 / 13,4335 / 18,3439 | 0,0171 / 0,0623 / 0,3198 | 9,0373 / 20,2343 / 41,2651 | 1 567 Punkte bei 0,5 m Abstand |
| Dorfweg, Rasterwegpunkte | −0,0002 / 0 / 0,0335 | 0 / 0 / 2,5173 | 0 / 0 / 0,0734 | 12,6841 / 23,3617 / 38,6904 | 2 839 Punkte/Zellen |
| Wegenden | −15,0282 / 0,5941 / 12,7963 | 0,942 / 2,4838 / 4,0153 | 0,0383 / 0,1022 / 0,4 | 28,5651 / 32,9026 / 37,24 | 26 Rampenenden |
| Bach-/Fluss-Landseite | −17,9211 / −9,045 / 0,5993 | 20,8336 / 43,3145 / 75,5403 | 0,0243 / 0,2003 / 2,7752 | 4,9448 / 18,9834 / 44,9918 | 1 703 Punkte; 2 696 Quellzellen |
| Seeufer-Landseite | −3,7043 / −3,049 / −2,0502 | 30,1451 / 38,0542 / 51,5666 | 0,0059 / 0,064 / 0,2553 | 18,6958 / 39,7777 / 49,5924 | 591 Punkte; 821 Quellzellen |
| Uferband einschließlich Randgitter | −17,9367 / −5,7983 / 11,7099 | 1,8631 / 27,1066 / 50,9634 | 0,0047 / 0,1405 / 0,6025 | 11,5074 / 30,8446 / 47,6723 | 17 732 Punkte; 4 076 Quell-Uferzellen |

Die Höhenwerte für Bach/Fluss und See beschreiben die trockenen, klassifizierten Landpunkte; Wasserpunkte sind separat über Tiefe und Bettneigung erfasst. Der Radius-P95 umfasst nur Punkte mit `|Krümmung| ≥ 0,02 1/m`.

| Element | Ist Wassertiefe P5/Median/P95 (m) | Ist Bettneigung P5/Median/P95 (°) | Ist Bettrauheit P5/Median/P95 (m) | Messumfang |
|---|---:|---:|---:|---:|
| Bach/Fluss | 0,1547 / 0,9064 / 1,5967 | 1,7434 / 19,0824 / 46,2886 | 0,148 / 0,5 / 0,7498 | 9 081 Wasserpunkte |
| See | 0,4701 / 1,332 / 1,35 | 0,0019 / 1,2097 / 43,2013 | 0,0004 / 0,1281 / 0,5883 | 2 693 Wasserpunkte |

| Übergang | Ist Höhenunterschied zwischen benachbarten 1-m-Zellmitten P5/Median/P95 (m) | Umfang |
|---|---:|---:|
| Plateau–Hang | 0,015 / 0,2536 / 0,5561 | 138 Zellpaare |
| Hang–Wand | 0,0781 / 0,9447 / 4,4884 | 3 872 Zellpaare |
| Ufer–Land | 0,0026 / 0,6453 / 1,1177 | 3 356 Zellpaare |
| Kachelnaht, Neigungsänderung über die Naht P5/Median/P95 | 0 / 0,0445 / 13,9902° | 8 960 Gitterproben |

| Objekt | Ist Anzahl | Ist Parameter P5/Median/P95 | Einheit / Bemerkung |
|---|---:|---:|---|
| Bäume | 1 481 | 5,1 / 7,3 / 10,7 | gespeicherter Höhen-/Skalenparameter m |
| Felsen | 96 | 0,51 / 0,94 / 1,865 | gespeicherter Größenparameter m |
| Felsblöcke | 0 | nicht messbar | keine platzierten Instanzen in `felsbloecke`; acht Mesh-Vorlagen sind keine Platzierungen |
| Findlinge | 32 | 0,6 / 1,2 / 3,5655 | gespeicherter Größenparameter m |
| Steine | 669 | 0,25 / 0,43 / 0,84 | gespeicherter Größenparameter m |
| Geröll | 517 | 0,2 / 0,37 / 0,75 | gespeicherter Größenparameter m |
| Deko/Grasbüschel | 3 917 | 0,38 / 0,61 / 0,83 | gespeicherter Größenparameter m |
| Gebäude | 233 | Breite 4,806 / 6 / 11,368; Tiefe 5 / 6 / 11; Höhenparameter 3 / 5 / 9 | m, Maße aus `haeuser` |

## 3. Geländeformen

### LF01 — Landschaft allgemein

- **Soll-Form:** Ein zusammenhängendes Höhenfeld ohne offene Innenlöcher, nicht endliche Höhen oder doppelte Flächen. Die Zell- und Kartenkontur bleibt an den Quellkoordinaten.
- **Masse [S/R]:** 336 × 303 nominale Rastermeter; 0,5-m-Höhengitter; Kacheln nach der Formel in Abschnitt 1.
- **Proportionen:** Höhen und horizontale Abstände stehen im Verhältnis 1:1 in Metern. Vertikale Überhöhung ist 1,0.
- **Übergänge:** Alle Klassengrenzen folgen den sechs Regeln TR01–TR06.
- **Natürlichkeit:** Rauheit R1-P95 ≤ 1,10 m über das Gesamtgelände; effektiver Radius-P5 ≥ 5,0 m. Die engeren Werte der Einzelelemente gelten zusätzlich.
- **MESSREGEL:** G1 offene Innenlöcher = 0; NaN = 0; Karten- und Zellwerte stimmen mit dem Höhenfeld überein, Abweichungen = 0.
- **Ist:** `383 237` Landpunkte; Neigung 0/0,9588/52,0383°, R1 0/0,0177/1,0673 m, Radius 5,2227/25,6814/45,8831 m.
- **Prüfung:** `pruefung/loch_o18g.js`, `pruefung/pruefe_regeln.py` (G1), `pruefung/pruefe_t42u.py`.

### LF02 — Plateau

- **Soll-Form:** Flache, durchgehende Oberseite. Plateau-Messgebiet beginnt 4 m innerhalb der Quellklassengrenze; der Rand selbst gehört zu TR05 oder TR03.
- **Masse [R]:** Plateaustufen-Sollwerte sind +14 m (Nord) und +12 m (Ostplateau) gegenüber dem Bezugsniveau. Die gemessenen `GB`-Mediane sind 13,9995 m (9 917 Zellen) und 11,9993 m (4 227 Zellen). Zusammen tragen 14 144 Quellzellen PLATEAU_NORD oder OSTPLATEAU.
- **Proportionen:** Neigungs-P95 ≤ 8° im inneren Messgebiet. R1-P95 ≤ 0,20 m. Effektiver Radius-P5 ≥ 20 m.
- **Übergänge:** Plateau–Hang erfüllt TR05; Plateau–Wand erfüllt TR03.
- **Natürlichkeit:** Oberflächenwellen mit R1-Amplitude >0,20 m auf mindestens 1 m² sind unzulässig; der Radius-P5 bleibt ≥20 m.
- **MESSREGEL:** P95 Neigung ≤8° und P95 R1 ≤0,20 m innerhalb des 4-m-Saums.
- **Ist:** Neigung 0/0,0006/6,1502°, R1 0/0,0009/0,1689 m, Radius 22,8433/33,2549/47,6936 m; 44 386 Punkte.
- **Prüfung:** Ist-Messung `pruefung/regelwerk_messung.py`; Grenzwert-Gate **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### LF03 — Hang

- **Soll-Form:** Durchgehende Böschung ohne isolierte Pyramiden, Dellen oder einen abrupten Richtungswechsel der Falllinie. Hangflächen sind keine Wandflächen.
- **Masse [R]:** 21 086 HANG-Zellen; Höhenbereich aus dem bestehenden Bezugssystem, Ist-P5 bis P95 −12,9333 bis +6,0991 m.
- **Proportionen:** Hangkörper hat 8,5°–39° Neigung. Übergangskanten werden getrennt nach TR03/TR05 gemessen. R1-P95 ≤0,90 m; Radius-P5 ≥7 m.
- **Übergänge:** Plateauseite nach TR05, Wandseite nach TR03, Wegseite nach TR01.
- **Natürlichkeit:** Reliefabweichung im 0,25–1,5-m-Bandpass ≤0,10 m Amplitude pro zusammenhängender Fläche ab 1 m²; Radius-P5 ≥7 m.
- **MESSREGEL:** Körperbereich P95-Neigung ≤39°; Bandpass-Amplitude >0,10 m löst R9w aus.
- **Ist:** Neigung 0,439/7,6014/54,4497°, R1 0,0005/0,0723/0,8586 m, Radius 7,3536/28,1176/46,5752 m.
- **Prüfung:** `pruefung/r9_form.py` (R9w); Ausreißer `pruefung/pruefe_regeln.py` (G2–G6); enger Hang-P95 **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### LF04 — Gebirge

- **Soll-Form:** Zusammenhängende Rücken und Wandmassive mit eindeutigem Grat, Hang und Fuß. Die vier benannten Höhenzüge behalten ihre Quellkennung.
- **Masse [R]:** Nord 14 m, Südgrat 16 m, Krater 11 m, Ostgrat 12 m Wandhöhe; 20 099 benannte Gebirgszellen.
- **Proportionen:** Vertikale Höhe zu horizontaler Ausdehnung bleibt 14/16/11/12 m zu den im Raster vorhandenen 8–10 m Wandbändern. R1-P95 ≤2,0 m; effektiver Radius-P5 ≥4 m.
- **Übergänge:** Grat über LF06, Wandfuß über LF07; Hang-Wand über TR03.
- **Natürlichkeit:** Mindestens zwei Maßstäbe: R1-Rauheit im 1-m-Maßstab und Krümmung im 1–10-m-Maßstab. R1-P95 ≤2 m.
- **MESSREGEL:** Vier Wandhöhensprünge bleiben innerhalb ±0,5 m der obigen Sollhöhen; jede Abweichung wird nach Wandname ausgewiesen.
- **Ist:** 80 422 Punkte; Neigung 0/13,9354/70,5724°, R1 0,0004/0,1887/1,9787 m, Radius 4,1238/19,1372/44,8102 m.
- **Prüfung:** `pruefung/regelwerk_messung.py`; Zellsprung `pruefung/klippen_messung_t40u.csv`; Grenzwert-Gate **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### LF05 — Klippe/Wand

- **Soll-Form:** Zusammenhängende Felswand zwischen Oberkante und Wandfuß. Die Wandfläche besitzt keine isolierten Spitzen oder Löcher.
- **Masse [R]:** Wandband 8–10 m horizontale Breite; Höhe Nord 14 m, Südgrat 16 m, Krater 11 m, Ostgrat 12 m. 7 435 WAND-Zellen.
- **Proportionen:** Wandneigung 45°–80°; jede Wandhöhe erfüllt LF04. Effektiver Radius-P5 ≥3,5 m; R1-P95 ≤2,7 m.
- **Übergänge:** Oberkante LF06, Fuß LF07; seitlicher Hanganschluss TR03.
- **Natürlichkeit:** R1-P95 ≤2,7 m; effektiver Radius-P5 ≥3,5 m. Ein Sprung in der Wandkontur über 0,15 m auf weniger als 2 m Periode wird als R9-Zacke gezählt.
- **MESSREGEL:** Wandneigungs-P5 ≥45°, Wandneigungs-P95 ≤80°, R1-P95 ≤2,7 m; R9-Sägezahn = 0.
- **Ist:** Neigung 7,6646/52,0827/78,9124°, R1 0,0313/0,8062/2,6799 m, Radius 3,6556/12,7392/40,7947 m.
- **Prüfung:** `pruefung/pruefe_regeln.py` (G2–G7b), `pruefung/r9_form.py` (R9).

### LF06 — Wandkrone

- **Soll-Form:** Durchgehende, abgerundete Kante zwischen Plateau/Grat und Wand; keine Nadelspitze und keine rückspringende Lücke.
- **Masse [R]:** 2 255 WAND_OBEN-Zellen; Kronenradius ≥1,0 m; horizontaler Übergang vom Grat zur Wand 1–4 m.
- **Proportionen:** Kantenradius ≥0,5 m im Mesh; kein Überhang über 1,0 m ohne eigene tragende Geometrie.
- **Übergänge:** Hangseite nach TR05, Wandseite nach LF05.
- **Natürlichkeit:** R1-P95 ≤2,2 m; effektiver Radius-P5 ≥3,5 m.
- **MESSREGEL:** G5-Klippenbeule ≤0,60 m; keine lokale Spitze >0,45 m gegenüber dem 3×3-Nachbarfeld; R9-Zacke = 0.
- **Ist:** Neigung 5,1292/21,3775/53,0791°, R1 0,0836/0,7806/2,1553 m, Radius 3,6334/9,168/34,5608 m.
- **Prüfung:** `pruefung/pruefe_regeln.py` (G2/G5), `pruefung/r9_form.py` (R9).

### LF07 — Wandfuß

- **Soll-Form:** Die Wand endet in einer zusammenhängenden Fußzone ohne frei schwebende Felskante und ohne abflusslose Mulde über 0,30 m.
- **Masse [R]:** 2 503 WAND_FUSS-Zellen; Übergangsbreite 1–5 m; Schutthang liegt vollständig auf Land.
- **Proportionen:** Höhensprung zum angrenzenden Hang entspricht LF04; seitlicher Fußgradient ≤0,70 m/m.
- **Übergänge:** Wand LF05 in Hang LF03; Geröll LF21 darf den Übergang begleiten, aber nicht die Geländeoberfläche ersetzen.
- **Natürlichkeit:** R1-P95 ≤2,2 m; Radius-P5 ≥4,5 m.
- **MESSREGEL:** Auf der Landseite R8b-Dellentiefe ≤0,30 m innerhalb 6 m von Weg/Kreuzung; Übergangshöhenschritt wird zusätzlich mit TR03 gemessen.
- **Ist:** Neigung 1,8686/35,8921/65,8364°, R1 0,0786/0,714/2,1302 m, Radius 4,5813/11,0627/34,2666 m.
- **Prüfung:** `pruefung/r9_form.py` (R8b), `pruefung/pruefe_regeln.py` (G5/G7b), `pruefung/regelwerk_messung.py`.

## 4. Wege und Wasser

### LF08 — Weg/Rampe

- **Soll-Form:** Durchgehendes, betretbares Band entlang der Kartenmittellinie. Das Band liegt auf dem Gelände und führt ohne Absatz in Anschlussflächen.
- **Masse [R]:** Kartenpfad 30 px = 1,2 m breit. Aktueller Overlay-Querschnitt reicht ±0,88 m voll deckend und ±1,08 m mit Randabblendung; Gesamtausdehnung 2,16 m.
- **Proportionen:** Sollbreite 1,2 m; Quergefälle ≤3,5 %; lokale Wölbung und Längsprofilrest ≤0,08 m pro 4-m-Abschnitt; Längsneigung ≤20°.
- **Übergänge:** Geländeauslauf nach LF13; Hangseite nach TR01; Wandkontakt nach TR02. Kreuzungen folgen LF10/LF11.
- **Natürlichkeit:** R1-P95 ≤0,35 m; effektiver Radius-P5 ≥8 m; keine geraden Bandkanten mit Zackenperiode <2 m.
- **MESSREGEL:** R1 Wegmaske ist 8 m breit um Mittellinie; Längs-/Querneigung und Wölbung erfüllen die genannten Grenzwerte; Wegband ist an jedem 0,25-m-Schritt höchstens 0,20 m versetzt.
- **Ist:** 13 Rampen, 1 567 Mittellinienproben; Neigung 3,172/13,4335/18,3439°, R1 0,0171/0,0623/0,3198 m, Radius 9,0373/20,2343/41,2651 m. Der Overlay-Querschnitt ist breiter als das Kartenmaß von 1,2 m.
- **Prüfung:** `pruefung/pruefe_regeln.py` (R1–R7), `pruefung/r8_kreuzung.py` (R8/R8a), `pruefung/r9_form.py` (R8b/R9/R9w).

### LF09 — Dorfweg

- **Soll-Form:** Verbundene Rasterwege in den Dorf- und Platzbereichen. Die Mittellinie bleibt innerhalb der Wegzellen.
- **Masse [R]:** Eine Quellzelle = 1 m; Kartenmaß 1,2 m; 2 839 serialisierte Wegpunkte/Zellen.
- **Proportionen:** Breite 1,0–1,2 m; Neigung ≤8°; Höhenschwankung R1-P95 ≤0,10 m.
- **Übergänge:** Anschluss an Rampe nach LF08; an Platz oder Haus nach LF24; an Hang/Wand nach TR01/TR02.
- **Natürlichkeit:** R1-P95 ≤0,10 m; Radius-P5 ≥12 m.
- **MESSREGEL:** Acht-Nachbar-Verbund hat genau eine Hauptkomponente; abgetrennte Restkomponente = 0; Wegneigung ≤8°.
- **Ist:** 2 839 Zellen; Neigung 0/0/2,5173°, R1 0/0/0,0734 m, Radius 12,6841/23,3617/38,6904 m.
- **Prüfung:** `pruefung/pruefe_regeln.py` (R2/R3), `pruefung/regelwerk_messung.py`; Verbundgrenze wird mit vorhandenem R2-Gate gemessen.

### LF10 — Kreuzung

- **Soll-Form:** Eine gemeinsame, ebene Wegfläche mit mindestens vier getrennten Richtungsarmen. Wegeprofile verschmelzen in einem Kreis mit Radius 2,5 m.
- **Masse [A]:** Messradius 4 m; ebene Kernfläche Radius 2,5 m nach `PLAN_O18_NEU.md`.
- **Proportionen:** Kern-Quergefälle ≤2 %; benachbarte Höhenpunkte im 0,25-m-Gitter ≤0,20 m; 1-m-Gitterresiduum ≤0,15 m.
- **Übergänge:** Jeder Arm schließt tangential an LF08 oder LF09 an; keine Voronoi-Umschaltung zwischen Rampenprofilen.
- **Natürlichkeit:** R1-P95 ≤0,35 m; effektiver Radius-P5 ≥2,5 m.
- **MESSREGEL:** An jedem Knoten: Stufe ≤0,20 m/0,25 m, Gitterresiduum ≤0,15 m/1 m, Kerngefälle ≤2 %.
- **Ist:** 31 Wegknoten im aktuellen R8-Lauf; der Prüfer weist 9 Stufen-, 10 Gitter- und 5 Quergefälle-Treffer aus.
- **Prüfung:** `pruefung/r8_kreuzung.py` prüft Stufe/Gitter/Quergefälle mit 3 % Quergefälle-Grenze. Für die strengere Sollgrenze 2 % ist ein Zusatzgate **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### LF11 — Gabelung

- **Soll-Form:** Eine durchgehende Wegfläche mit exakt drei Armen; die Abzweigung beginnt im gemeinsamen Knoten und lässt keine keilförmige Lücke.
- **Masse [A]:** Kernradius 2,5 m; Ausgleichsebene über 4 m Messradius nach `PLAN_O18_NEU.md`.
- **Proportionen:** Kern-Quergefälle ≤2 %; jeder Arm hat am Übergang mindestens 1,2 m lichte Breite.
- **Übergänge:** Drei Armprofile werden im Kern auf eine gemeinsame Höhe überblendet; Höhenverlauf pro Arm folgt LF08/LF09.
- **Natürlichkeit:** R1-P95 ≤0,35 m; Radius-P5 ≥2,5 m.
- **MESSREGEL:** Grad des Weggraphen = 3; Stufe ≤0,20 m/0,25 m; Gitterresiduum ≤0,15 m/1 m; Quergefälle ≤2 %.
- **Ist:** Die Quellen enthalten keine eigene Gabelungskennung. Der Messlauf markiert jeden Dorfwegpunkt mit 4-Nachbargrad 3 als Gabelungskandidat; die Kachelbelegung bildet genau diesen reproduzierbaren Kandidatendetektor ab. Eine fachliche Klassifikation aus dem Kartenbild ist mangels Master-PNG offen.
- **Prüfung:** `pruefung/r8_kreuzung.py` für Geometrie; branch-getrennte Zählung **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### LF12 — Kehre

- **Soll-Form:** Weicher Richtungswechsel in der Wegmittellinie ohne Knick oder Überdeckung zweier getrennter Bandflächen.
- **Masse [A]:** Innenradius ≥2,0 m; Wendewinkel wird entlang der Mittellinie über 2 m Sehne gemessen.
- **Proportionen:** Quergefälle ≤3,5 %; Bandbreite 1,2 m; innere Bandkante bleibt geschlossen.
- **Übergänge:** Beide Schenkel schließen nach LF08 an; Anschluss an Kreuzung/Gabelung folgt LF10/LF11.
- **Natürlichkeit:** Mittellinienkrümmung ≤0,5 1/m; R1-P95 ≤0,35 m.
- **MESSREGEL:** Radius ≥2 m und keine Stufe >0,20 m pro 0,25 m im 4-m-Umkreis.
- **Ist:** Kehren werden aus ≥90° Richtungsänderung erkannt; die Kreuzungsprüfung weist eine Haarnadelrampe `rampe_12` aus. Eine eigene Radiusverteilung ist nicht in den Quelldaten gespeichert.
- **Prüfung:** `pruefung/r8_kreuzung.py` (Knotenstufe); Radiusgate **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### LF13 — Wegende

- **Soll-Form:** Das Wegband läuft längs in Gelände, Wand, Kreuzung oder Platz aus. Jedes Ende erhält einen 4-m-Auslauf innerhalb der Kartenkontur.
- **Masse [A]:** Auslauf mindestens 4 m; Prüfstreifen ±2,5 m um die verlängerte Mittellinie gemäß `PLAN_O18_NEU.md`.
- **Proportionen:** Höhenänderung ≤0,10 m je 0,25 m; Quergefälle wird quer zur Laufrichtung gemessen.
- **Übergänge:** Anschlussfläche nach LF01/LF05/LF10/LF11; in Wasser kein Ende.
- **Natürlichkeit:** Keine sichtbare Absatzkante; R1-P95 im Endstreifen ≤0,35 m.
- **MESSREGEL:** Mindestens 4 m Auslauf; jede Nachbarstufe ≤0,10 m/0,25 m; kein blindes Ende außerhalb Kartenrand.
- **Ist:** 26 Rampenenden; Neigung 0,942/2,4838/4,0153°, R1 0,0383/0,1022/0,4 m. R8a meldet 24 Treffer.
- **Prüfung:** `pruefung/r8_kreuzung.py` (R8a), `pruefung/pruefe_regeln.py` (R1).

### LF14 — Bach/Fluss

- **Soll-Form:** Zusammenhängendes Bett mit monotoner Fließrichtung, erkennbarem Bett und beidseitigem Ufer. Wasseroberfläche darf keine trockenen Inselzellen einschließen.
- **Masse [R]:** Nordbach-Median 2,0 m; südlicher Kartenfluss 7,4–10 m aus 185–250 px / 25 px/m. Die Schutzmaske misst für den Südfluss nur 2,5 m und widerspricht damit der gezeichneten Kartenbreite. Sollbreite ist 7,4–10 m.
- **Proportionen:** Wassertiefe 0,3–1,6 m; lokale Tiefenstufen ≤0,5 m je 1 m; auf dem Hauptlauf kein Anstieg über 0,02 m stromab.
- **Übergänge:** Uferland nach TR04; Brücken und Wege bleiben frei; Seeanschluss nach LF15.
- **Natürlichkeit:** Bett-R1-P95 ≤0,75 m; Uferneigung ≤35°; Fließbett schneidet höchstens 1,0 m unter den lokalen Landanschluss ein.
- **MESSREGEL:** 8-Nachbar-Wasserkomponenten; Hauptlauf ohne Bergaufpunkt >0,02 m; Tiefe und Breite innerhalb der obigen Grenzen.
- **Ist:** 2 696 Bach-/Flussquellzellen; 9 081 Wasserpunkte; Tiefe 0,1547/0,9064/1,5967 m; Bettneigung 1,7434/19,0824/46,2886°; Bettrauheit 0,148/0,5/0,7498 m.
- **Prüfung:** `pruefung/pruefe_bergauf_t62u.py`, `pruefung/pruefe_ufer_t62u.py`, `pruefung/fluss_profil_t61u.py`; Breitenprofil je Abschnitt **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### LF15 — See

- **Soll-Form:** Geschlossene Wasserschale mit zusammenhängender Fläche und flachem Bett; kein trockener Spalt zum Hauptfluss.
- **Masse [R/A]:** 821 Quellzellen = 821 m² Nennfläche. Wassertiefe 1–3 m als messbarer Platzhalter-Sollbereich.
- **Proportionen:** Bettneigung P95 ≤5° außerhalb des Ufers; Tiefenänderung ≤0,20 m pro 1 m in der Seemitte.
- **Übergänge:** Wasser-Land nach TR04; Anschluss an Bach/Fluss ohne Höhenlücke >0,20 m.
- **Natürlichkeit:** Bett-R1-P95 ≤0,60 m; effektiver Radius-P5 ≥10 m.
- **MESSREGEL:** Eine Wasserkonnektivitätskomponente; Tiefe 1–3 m in der Seemitte; Neigungs-P95 ≤5° im Bett ohne Uferzellen.
- **Ist:** 2 693 Wasserpunkte; Tiefe 0,4701/1,332/1,35 m; Bettneigung 0,0019/1,2097/43,2013°; Bettrauheit 0,0004/0,1281/0,5883 m. P95 schließt Randpunkte ein und ist kein Seemittewert.
- **Prüfung:** `pruefung/pruefe_ufer_t62u.py`; Lage-/Tiefen-Gate **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### LF16 — Ufer

- **Soll-Form:** Durchgehender Geländestreifen vom Bett bis zum angrenzenden Land; keine senkrechten Uferplatten.
- **Masse [S/R]:** Ufermodellierung 2,5 m Übergangsbreite; 4 076 Quell-Uferzellen.
- **Proportionen:** Landseitige Neigung ≤35°; Höhenänderung über den Uferstreifen ≤1,0 m/m.
- **Übergänge:** Wasser nach LF14/LF15; Land nach LF01; Zellgrenze nach TR04.
- **Natürlichkeit:** R1-P95 ≤0,65 m; effektiver Radius-P5 ≥11 m.
- **MESSREGEL:** 2,5-m-Uferprofil; keine Landneigung >35°; Wasser-Land-Schritt-P95 ≤1,2 m pro benachbarter Zelle.
- **Ist:** Neigung 1,8631/27,1066/50,9634°, R1 0,0047/0,1405/0,6025 m, Radius 11,5074/30,8446/47,6723 m; Ufer-Land-Schritt-P95 1,1177 m.
- **Prüfung:** `pruefung/pruefe_ufer_t62u.py`; Übergangsgate **neu nötig:** `pruefung/regelwerk_pruefen.py`.

## 5. Fels, Deko und Baukörper

### LF17 — Felsen

- **Soll-Form:** Unregelmäßige, kompakte Felsform mit mindestens drei sichtbaren Flächenrichtungen; kein Quader und keine perfekte Kugel.
- **Masse [R]:** Kleiner Kartenfels 50 px = 2 m Durchmesser. Das aktuelle Modellmaß bleibt als Instanzparameter separat messbar.
- **Proportionen:** Höhe/Breite 0,5–0,9; Instanzparameter 0,5–2,0 m; Lageabweichung zur Oberfläche ≤0,15 m.
- **Übergänge:** Kontakt zum Boden ohne sichtbare Lücke; auf Wandflächen gilt LF05; im Wasser gilt LF14/LF15.
- **Natürlichkeit:** Mesh-Abweichung vom besten Ellipsoid RMS 8–25 % des Radius; Kantenradius ≥0,05 m.
- **MESSREGEL:** Durchmesser 1,5–2,5 m für kleine Felsen; Lagefehler ≤0,15 m; Höhen-/Breitenverhältnis 0,5–0,9.
- **Ist:** 96 Instanzen; Parameter 0,51/0,94/1,865 m. Vollständige Mesh-Bounding-Box ist aus dem Platzierungsdatensatz nicht ableitbar.
- **Prüfung:** `pruefung/pruefe_regeln.py` (R6/G11), `pruefung/strahl_objekte_t64u.py`; Ellipsoid- und Lagegate mit 0,15 m **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### LF18 — Felsblöcke

- **Soll-Form:** Große kantige Blöcke als getrennte Körper; keine zusammenhängende Ersatzwand und keine frei schwebenden Platten.
- **Masse [R]:** Mittlerer Felsblock 130 px = 5,2 m Durchmesser. Höhe/Breite 0,5–0,9.
- **Proportionen:** Soll-Durchmesser 3,9–6,5 m; Lageabweichung ≤0,15 m; Bodenüberdeckung 10–30 % der Blockhöhe.
- **Übergänge:** Blockfuß liegt auf LF01, LF05 oder LF07; kein Einbau in Wasser oder Wegfläche.
- **Natürlichkeit:** Ellipsoid-RMS 8–25 %; Kantenradius ≥0,05 m.
- **MESSREGEL:** Instanzzahl und Durchmesser werden pro Kachel gezählt; jeder Block erfüllt 3,9–6,5 m und Bodenüberdeckung 10–30 %.
- **Ist:** 0 platzierte Instanzen in `felsbloecke`; P5/Median/P95 nicht definiert.
- **Prüfung:** `pruefung/pruefe_regeln.py` (R6/G11); bei 0 Instanzen keine Formstichprobe. Instanz- und Bounding-Box-Gate **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### LF19 — Findlinge

- **Soll-Form:** Einzelner, großer, asymmetrischer Stein mit breiter Auflagefläche.
- **Masse [R]:** Kartenmaß 210 px = 8,4 m Durchmesser.
- **Proportionen:** Durchmesser 6,3–10,5 m; Höhe/Breite 0,35–0,70; Einsenkung 10–25 % der Höhe.
- **Übergänge:** Bodenkontakt nach LF01; Abstand zu Häusern und Wegen ≥1 m.
- **Natürlichkeit:** Ellipsoid-RMS 8–25 %; Kantenradius ≥0,05 m.
- **MESSREGEL:** Durchmesser, Höhenverhältnis, Einsenkung und Lagefehler ≤0,15 m werden je Instanz geprüft.
- **Ist:** 32 Instanzen; Parameter 0,6/1,2/3,5655 m. Der aktuelle Parameter liegt deutlich unter dem aus der Karte gerechneten Findlingsmaß.
- **Prüfung:** `pruefung/pruefe_regeln.py` (R6/G11), `pruefung/strahl_objekte_t64u.py`; vollständige Größenmessung **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### LF20 — Steine

- **Soll-Form:** Kleine, unregelmäßige Einzelsteine; Kanten sind gebrochen, kein Stein reicht als Wandkörper.
- **Masse [R/A]:** Modellparameter 0,25–0,84 m als Sollbereich, weil die Karte keine eigene Pixelklasse für Einzelsteine trägt.
- **Proportionen:** Höhe/Breite 0,4–0,8; Bodeneinsenkung 10–30 %.
- **Übergänge:** Boden- und Uferkontakt nach LF01/LF16; keine Instanz auf dem Weg.
- **Natürlichkeit:** Ellipsoid-RMS 8–25 %; Kantenradius ≥0,02 m.
- **MESSREGEL:** 100 % der Instanzen innerhalb 0,25–0,84 m; Lagefehler ≤0,15 m; Weg- und Wasserüberschneidung = 0.
- **Ist:** 669 Instanzen; Parameter 0,25/0,43/0,84 m.
- **Prüfung:** `pruefung/pruefe_regeln.py` (R6/G11), `pruefung/strahl_objekte_t64u.py`; Verhältnis-/Überdeckungs-Gate **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### LF21 — Geröll

- **Soll-Form:** Lockere, bodennahe Gruppe aus kleinen kantigen Stücken am Wandfuß und in Runsen.
- **Masse [A/R]:** Einzelparameter 0,20–0,75 m; Abstand zwischen Steinstützpunkten 0,15–1,0 m.
- **Proportionen:** Höhe/Breite 0,35–0,8; keine zusammenhängende Fläche dicker als 0,75 m.
- **Übergänge:** Verteilung auf LF07 oder LF03; endet spätestens 5 m vom Wandfuß; nicht auf Wasser und Weg.
- **Natürlichkeit:** Gruppenabstand P95 ≤1,0 m; Einzelstein-RMS 8–25 %; Kantenradius ≥0,02 m.
- **MESSREGEL:** P5/Median/P95 der Größenparameter bleibt 0,20/0,37/0,75 m als Zielverteilung; jede Instanz liegt innerhalb 5 m einer Wandfußzelle.
- **Ist:** 517 Instanzen; Parameter 0,2/0,37/0,75 m.
- **Prüfung:** `pruefung/pruefe_regeln.py` (R6/G11), `pruefung/strahl_objekte_t64u.py`; Gruppendistanz-Gate **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### LF22 — Deko

- **Soll-Form:** Bodennahes Grasbüschel mit einzelnen Halmen, ohne harte, flächige Platte.
- **Masse [A/R]:** Höhe 0,35–0,85 m; Breite 1,4 × Höhe aus dem bestehenden Instanzmaß.
- **Proportionen:** Höhe/Breite 0,55–0,75; Geländeüberdeckung 0,05–0,20 m.
- **Übergänge:** Auf Schnee- und Landflächen; nicht auf Wasser, Weg, Gebäude oder Wandfläche.
- **Natürlichkeit:** Halmspitzen streuen innerhalb eines Büschels um höchstens 0,20 m; Kantenradius des Büschel-Silhouettenrandes ≥0,02 m.
- **MESSREGEL:** Höhenparameter 0,35–0,85 m; Lagefehler ≤0,15 m; Deko auf unzulässigen Flächen = 0.
- **Ist:** 3 917 Büschel; Parameter 0,38/0,61/0,83 m.
- **Prüfung:** `pruefung/regelwerk_messung.py`; Flächen- und Silhouettengate **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### LF23 — Bäume (Platzhalter-Masse)

- **Soll-Form:** Aufrechter Stamm mit klarer Krone; Fichtenkrone konisch, Kiefernkrone offen. Bäume sind Volumenkörper und keine Kartenebenen.
- **Masse [R/A]:** Zielhöhe 5–12 m; Kronenbreite 0,4–0,8 × Baumhöhe; Stammhöhe 0,08–0,18 × Baumhöhe.
- **Proportionen:** Stamm lotrecht innerhalb 3°; Abstand zwischen Stämmen ≥1 m; Baumneigung folgt dem lokalen Hang nur bis 15°.
- **Übergänge:** Stammfuß liegt auf LF01; keine Platzierung in Wasser, Weg, Gebäude oder Wandneigung >45°.
- **Natürlichkeit:** Fichtenkrone verjüngt sich in jedem oberen Drittel um mindestens 20 %; Kiefernkrone hat mindestens drei getrennte Kronenlagen. Blatt-/Astspitzen haben Radius ≥0,02 m.
- **MESSREGEL:** Baumhöhe 5–12 m; Krone/Höhe 0,4–0,8; Stützfehler ≤0,15 m; Wandkontakt-, Weg- und Wasser-Treffer = 0.
- **Ist:** 1 481 Instanzen; Skalenparameter 5,1/7,3/10,7 m. Der JSON-Skalar ist keine gemessene Baum-Bounding-Box.
- **Prüfung:** `pruefung/pruefe_regeln.py` (G11), `pruefung/strahl_objekte_t64u.py`; Größen-/Neigungsgate **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### LF24 — Gebäude (Platzhalter-Masse)

- **Soll-Form:** Geschlossener Baukörper mit rechteckigem Grundriss, tragenden Wänden, Sockel, Dach und messbarer Firsthöhe.
- **Masse [R/A]:** Fußabdruck aus `haeuser.b/t`: Breite P5/Median/P95 4,806/6/11,368 m; Tiefe 5/6/11 m. Höhenparameter 3/5/9 m nach Gebäudetyp.
- **Proportionen:** Wandhöhe 0,52–0,66 × Typ-Höhe; Dachanstieg 0,40–0,68 × kleinere Grundrissseite; Sockel 0,45–0,75 m.
- **Übergänge:** Sockel steht auf LF01 mit Höhenabweichung ≤0,10 m; kein Überhang über 0,20 m; Hauskante zu Weg mindestens 0,9 m.
- **Natürlichkeit:** Gebäude-Eckradius 0,05–0,15 m; Dachtraufe bleibt ohne Knick; Firstabweichung ≤0,10 m auf 1 m Länge.
- **MESSREGEL:** Fußabdruck weicht höchstens 0,10 m von `b×t` ab; Sockelfehler ≤0,10 m; Dachanstieg und Wandhöhe erfüllen die Typ-Proportionen.
- **Ist:** 233 Gebäude; Breite 4,806/6/11,368 m, Tiefe 5/6/11 m, Höhenparameter 3/5/9 m.
- **Prüfung:** `pruefung/regelwerk_messung.py`; Hausfußabdruck-/Sockelgate **neu nötig:** `pruefung/regelwerk_pruefen.py`.

## 6. Übergangsregeln

### TR01 — Weg–Hang

- **Soll-Form/Masse [A]:** 2-m-Streifen vom 1,2-m-Wegkern in den Hang; keine freistehende Bandkante.
- **Proportionen:** Wegquergefälle ≤3,5 %; Höhenanstieg außerhalb des Kerns ≤0,70 m je Meter.
- **Natürlichkeit:** Keine seitliche Wulst mit R1-Amplitude >0,10 m über 1 m².
- **MESSREGEL:** Querprofil bei ±1,5 m; Quergefälle ≤3,5 % und seitlicher R1-Auftrag ≤0,10 m.
- **Ist:** In H2, G1 und F6 als Weg-Hang-Typ erkannt; globaler Hang-/Weg-P95 ist in LF03/LF08 dokumentiert.
- **Prüfung:** `pruefung/pruefe_regeln.py` (R3); lokaler Übergangsauftrag **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### TR02 — Weg–Wand

- **Soll-Form/Masse [A]:** Wegende erhält einen mindestens 4 m langen Auslauf bis zur Anschlussfläche innerhalb der Kartenkontur.
- **Proportionen:** Abstand zwischen Wegende und Wand ≥4 m; der gesamte Auslauf liegt auf einer geometrisch durchgehenden Fläche nach LF13.
- **Natürlichkeit:** Keine Wandstufe >0,10 m/0,25 m im Weg-Endprofil.
- **MESSREGEL:** Minimalabstand Wand/Ende ≥4 m; der 4-m-Auslauf ist durchgehend; R1_wand = 0 und R8a-Stufe ≤0,10 m.
- **Ist:** Übergangstyp in G1/H1 erkannt; R8a-Ausgang weist 24 Wegenden aus.
- **Prüfung:** `pruefung/pruefe_regeln.py` (R1), `pruefung/r8_kreuzung.py` (R8a).

### TR03 — Hang–Wand

- **Soll-Form/Masse [A]:** Übergang liegt zwischen Hangfuß/-kopf und Wandfläche; Übergangsband 1–5 m.
- **Proportionen:** Wandmassiv folgt LF04; benachbarte Zellmitten haben P95-Höhendifferenz ≤4,5 m.
- **Natürlichkeit:** R1-P95 im Übergang ≤2,2 m; Radius-P5 ≥3,5 m.
- **MESSREGEL:** P95 Zellmitten-Differenz ≤4,5 m; Wandkontur-Sägezahn = 0.
- **Ist:** 3 872 Zellpaare; Höhenschritt 0,0781/0,9447/4,4884 m.
- **Prüfung:** `pruefung/regelwerk_messung.py`, `pruefung/r9_form.py`; Abschnittszuordnung **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### TR04 — Ufer–Land

- **Soll-Form/Masse [S/R]:** 2,5-m-Profil von Wasseroberfläche zum Land; Übergang umfasst Bettkante, Böschung und trockenes Gelände.
- **Proportionen:** Höhendifferenz benachbarter Zellen P95 ≤1,2 m; landseitige Neigung ≤35°.
- **Natürlichkeit:** R1-P95 ≤0,65 m; kein linearer Uferzahn über >0,15 m innerhalb <2 m Periode.
- **MESSREGEL:** Uferbreite ≥2,5 m; Zellschritt-P95 ≤1,2 m; Uferneigung-P95 ≤35°.
- **Ist:** 3 356 Zellpaare; Schritt 0,0026/0,6453/1,1177 m. Das breite Uferband hat Neigung P95 50,9634° und R1-P95 0,6025 m; P95 überschreitet die Neigungsgrenze.
- **Prüfung:** `pruefung/pruefe_ufer_t62u.py`; lokale Breiten-/Neigungsauswertung **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### TR05 — Plateau–Hang

- **Soll-Form/Masse [A]:** Weicher Höhenwechsel über mindestens 4 m von LF02 zu LF03.
- **Proportionen:** P95-Höhenschritt ≤0,60 m je benachbartem 1-m-Zellpaar; kein Vertikalsprung.
- **Natürlichkeit:** Radius-P5 ≥4 m; kein R9w-Hangwellenausschlag >0,10 m auf ≥1 m².
- **MESSREGEL:** Übergangsbreite ≥4 m; Zellschritt-P95 ≤0,60 m; R9w-Treffer im Übergangsband = 0.
- **Ist:** 138 Zellpaare; Schritt 0,015/0,2536/0,5561 m.
- **Prüfung:** `pruefung/regelwerk_messung.py`, `pruefung/r9_form.py` (R9w); Übergangsbreite **neu nötig:** `pruefung/regelwerk_pruefen.py`.

### TR06 — Kachelnaht

- **Soll-Form/Masse [R]:** Nachbarkacheln teilen dieselben Randkoordinaten und Höhenwerte. Interne Nähte liegen bei x = 42·k m und z = 43·k m.
- **Proportionen:** Höhenversatz über die Naht ≤0,02 m; Normalen-/Neigungsänderung-P95 ≤15° über die beidseitigen 0,5-m-Gitterkanten.
- **Natürlichkeit:** R1-Änderung genau an der Naht weicht höchstens 0,10 m vom 1-m-Umfeld ab.
- **MESSREGEL:** Jede Nahtprobe erfüllt Höhenversatz ≤0,02 m; Naht-Neigungsänderung-P95 ≤15°; offene Kanten = 0.
- **Ist:** Globales Höhenfeld teilt Nahtvertices; Neigungsänderung 0/0,0445/13,9902° über 8 960 Proben. Getrennte Export-Meshes sind damit noch nicht geprüft.
- **Prüfung:** `pruefung/pruefe_mesh_t64u.py` für das gemeinsame Mesh; Nahtabgleich getrennter Kachelexporte **neu nötig:** `pruefung/regelwerk_pruefen.py`.

## 7. Kachelmatrix A1–H7

Jeder Code bezeichnet sowohl das vorkommende Element als auch dessen Sollregel aus Abschnitt 3–6. `LF18` (Felsblöcke) kommt im Reliefdatensatz in keiner Kachel vor, weil die Instanzliste leer ist. `Kachelnaht` wird auf allen 56 Kacheln geführt, da jede Kachel an mindestens eine interne Naht grenzt. Die Präsenzliste stammt aus Quellzellklassen, Objektpositionen und Weggeometrie, nicht aus Sichtung eines Renderbilds. Kreuzungen und Kehren sind geometrische Kandidaten aus Liniennähe beziehungsweise einer Richtungsänderung ≥90°; Gabelungen sind 4-Nachbargrad-3-Kandidaten. Diese Kriterien sind im Messskript festgelegt und reproduzierbar, ersetzen aber keine Sichtklassifikation aus der fehlenden Master-PNG.

| Kachel | Elemente und geltende Sollcodes |
|---|---|
| A1 | LF01 · LF02 · LF03 · LF04 · LF05 · LF06 · LF07 · LF14 · LF16 · LF17 · LF20 · LF22 · LF23 · TR03 · TR04 · TR06 |
| B1 | LF01 · LF02 · LF03 · LF04 · LF05 · LF06 · LF07 · LF08 · LF13 · LF17 · LF22 · LF23 · LF24 · TR03 · TR05 · TR06 |
| C1 | LF01 · LF02 · LF03 · LF04 · LF05 · LF06 · LF07 · LF08 · LF16 · LF17 · LF20 · LF22 · LF23 · LF24 · TR03 · TR04 · TR05 · TR06 |
| D1 | LF01 · LF02 · LF04 · LF05 · LF06 · LF07 · LF08 · LF09 · LF10 · LF11 · LF13 · LF16 · LF20 · LF21 · LF22 · LF23 · LF24 · TR04 · TR06 |
| E1 | LF01 · LF02 · LF04 · LF05 · LF06 · LF07 · LF08 · LF09 · LF10 · LF11 · LF13 · LF14 · LF16 · LF19 · LF20 · LF21 · LF22 · LF23 · LF24 · TR04 · TR06 |
| F1 | LF01 · LF02 · LF04 · LF05 · LF06 · LF07 · LF08 · LF09 · LF10 · LF11 · LF13 · LF14 · LF16 · LF19 · LF20 · LF21 · LF22 · LF23 · TR04 · TR06 |
| G1 | LF01 · LF02 · LF04 · LF05 · LF06 · LF07 · LF08 · LF09 · LF10 · LF11 · LF13 · LF14 · LF16 · LF20 · LF21 · LF22 · LF23 · LF24 · TR02 · TR04 · TR06 |
| H1 | LF01 · LF02 · LF04 · LF05 · LF06 · LF07 · LF09 · LF10 · LF11 · LF16 · LF20 · LF21 · LF22 · LF23 · LF24 · TR02 · TR04 · TR06 |
| A2 | LF01 · LF03 · LF04 · LF05 · LF06 · LF07 · LF14 · LF16 · LF17 · LF20 · LF21 · LF22 · LF23 · LF24 · TR03 · TR04 · TR06 |
| B2 | LF01 · LF03 · LF04 · LF05 · LF07 · LF14 · LF16 · LF20 · LF21 · LF22 · LF23 · LF24 · TR03 · TR04 · TR06 |
| C2 | LF01 · LF02 · LF03 · LF04 · LF05 · LF06 · LF07 · LF08 · LF13 · LF17 · LF21 · LF22 · LF23 · LF24 · TR03 · TR05 · TR06 |
| D2 | LF01 · LF09 · LF10 · LF11 · LF17 · LF20 · LF22 · LF24 · TR06 |
| E2 | LF01 · LF09 · LF10 · LF11 · LF14 · LF16 · LF20 · LF22 · LF24 · TR04 · TR06 |
| F2 | LF01 · LF02 · LF04 · LF05 · LF06 · LF07 · LF09 · LF10 · LF11 · LF14 · LF16 · LF20 · LF21 · LF22 · LF24 · TR04 · TR06 |
| G2 | LF01 · LF09 · LF10 · LF11 · LF20 · LF22 · LF24 · TR06 |
| H2 | LF01 · LF02 · LF03 · LF04 · LF05 · LF06 · LF07 · LF09 · LF10 · LF11 · LF16 · LF17 · LF19 · LF20 · LF22 · LF23 · LF24 · TR01 · TR03 · TR04 · TR06 |
| A3 | LF01 · LF03 · LF14 · LF17 · LF20 · LF22 · LF23 · LF24 · TR04 · TR06 |
| B3 | LF01 · LF03 · LF04 · LF05 · LF06 · LF07 · LF14 · LF16 · LF20 · LF21 · LF22 · LF23 · LF24 · TR03 · TR04 · TR06 |
| C3 | LF01 · LF03 · LF04 · LF05 · LF06 · LF07 · LF08 · LF12 · LF13 · LF17 · LF21 · LF22 · LF23 · LF24 · TR03 · TR06 |
| D3 | LF01 · LF04 · LF05 · LF06 · LF07 · LF08 · LF09 · LF10 · LF11 · LF12 · LF17 · LF19 · LF21 · LF22 · LF24 · TR06 |
| E3 | LF01 · LF09 · LF10 · LF11 · LF14 · LF16 · LF20 · LF22 · LF24 · TR04 · TR06 |
| F3 | LF01 · LF09 · LF10 · LF11 · LF20 · LF22 · LF24 · TR06 |
| G3 | LF01 · LF02 · LF03 · LF04 · LF05 · LF06 · LF07 · LF08 · LF09 · LF10 · LF11 · LF13 · LF17 · LF19 · LF20 · LF21 · LF22 · LF23 · LF24 · TR03 · TR05 · TR06 |
| H3 | LF01 · LF02 · LF03 · LF04 · LF05 · LF06 · LF07 · LF17 · LF19 · LF21 · LF22 · LF23 · TR03 · TR05 · TR06 |
| A4 | LF01 · LF03 · LF14 · LF20 · LF22 · LF23 · LF24 · TR04 · TR06 |
| B4 | LF01 · LF03 · LF04 · LF05 · LF06 · LF07 · LF16 · LF21 · LF22 · LF23 · LF24 · TR03 · TR04 · TR06 |
| C4 | LF01 · LF04 · LF05 · LF06 · LF07 · LF08 · LF13 · LF21 · LF22 · LF23 · LF24 · TR06 |
| D4 | LF01 · LF04 · LF05 · LF06 · LF07 · LF08 · LF09 · LF10 · LF11 · LF12 · LF13 · LF15 · LF16 · LF17 · LF20 · LF21 · LF22 · LF23 · LF24 · TR04 · TR06 |
| E4 | LF01 · LF09 · LF10 · LF11 · LF14 · LF15 · LF16 · LF20 · LF22 · LF24 · TR04 · TR06 |
| F4 | LF01 · LF09 · LF10 · LF11 · LF22 · LF24 · TR06 |
| G4 | LF01 · LF02 · LF04 · LF05 · LF06 · LF07 · LF08 · LF09 · LF10 · LF11 · LF17 · LF20 · LF21 · LF22 · LF23 · LF24 · TR06 |
| H4 | LF01 · LF02 · LF04 · LF05 · LF06 · LF07 · LF08 · LF13 · LF17 · LF21 · LF22 · LF23 · TR06 |
| A5 | LF01 · LF03 · LF14 · LF20 · LF22 · LF23 · LF24 · TR04 · TR06 |
| B5 | LF01 · LF03 · LF04 · LF05 · LF06 · LF07 · LF16 · LF21 · LF22 · LF23 · LF24 · TR03 · TR04 · TR06 |
| C5 | LF01 · LF03 · LF04 · LF05 · LF06 · LF07 · LF08 · LF13 · LF17 · LF21 · LF22 · LF23 · LF24 · TR03 · TR06 |
| D5 | LF01 · LF03 · LF04 · LF05 · LF06 · LF07 · LF14 · LF15 · LF16 · LF17 · LF20 · LF21 · LF22 · LF23 · LF24 · TR04 · TR06 |
| E5 | LF01 · LF04 · LF09 · LF10 · LF11 · LF14 · LF15 · LF16 · LF20 · LF22 · LF23 · LF24 · TR04 · TR06 |
| F5 | LF01 · LF09 · LF10 · LF11 · LF14 · LF16 · LF20 · LF22 · LF24 · TR04 · TR06 |
| G5 | LF01 · LF09 · LF10 · LF11 · LF20 · LF22 · LF24 · TR06 |
| H5 | LF01 · LF02 · LF03 · LF04 · LF05 · LF06 · LF07 · LF08 · LF09 · LF10 · LF11 · LF13 · LF16 · LF17 · LF19 · LF20 · LF21 · LF22 · LF23 · LF24 · TR03 · TR04 · TR05 · TR06 |
| A6 | LF01 · LF03 · LF04 · LF14 · LF20 · LF22 · LF23 · LF24 · TR04 · TR06 |
| B6 | LF01 · LF03 · LF04 · LF05 · LF06 · LF07 · LF14 · LF16 · LF17 · LF20 · LF21 · LF22 · LF24 · TR03 · TR04 · TR06 |
| C6 | LF01 · LF03 · LF04 · LF05 · LF06 · LF07 · LF08 · LF13 · LF17 · LF21 · LF22 · LF23 · TR03 · TR06 |
| D6 | LF01 · LF03 · LF04 · LF05 · LF06 · LF07 · LF08 · LF10 · LF13 · LF14 · LF16 · LF20 · LF21 · LF22 · LF23 · LF24 · TR04 · TR06 |
| E6 | LF01 · LF04 · LF05 · LF06 · LF07 · LF08 · LF13 · LF14 · LF16 · LF20 · LF21 · LF22 · LF23 · TR04 · TR06 |
| F6 | LF01 · LF03 · LF04 · LF05 · LF06 · LF07 · LF08 · LF13 · LF14 · LF16 · LF20 · LF21 · LF22 · LF23 · LF24 · TR03 · TR04 · TR06 |
| G6 | LF01 · LF04 · LF05 · LF06 · LF07 · LF08 · LF14 · LF16 · LF20 · LF21 · LF22 · LF23 · TR04 · TR06 |
| H6 | LF01 · LF03 · LF04 · LF05 · LF06 · LF07 · LF08 · LF13 · LF17 · LF21 · LF22 · LF23 · LF24 · TR03 · TR06 |
| A7 | LF01 · LF14 · LF16 · LF17 · LF20 · LF22 · LF23 · LF24 · TR04 · TR06 |
| B7 | LF01 · LF14 · LF16 · LF20 · LF22 · LF23 · LF24 · TR04 · TR06 |
| C7 | LF01 · LF05 · LF08 · LF13 · LF14 · LF16 · LF20 · LF22 · LF23 · LF24 · TR04 · TR06 |
| D7 | LF01 · LF14 · LF16 · LF20 · LF22 · LF23 · LF24 · TR04 · TR06 |
| E7 | LF01 · LF14 · LF16 · LF20 · LF22 · LF23 · LF24 · TR04 · TR06 |
| F7 | LF01 · LF14 · LF16 · LF20 · LF22 · LF23 · LF24 · TR04 · TR06 |
| G7 | LF01 · LF14 · LF16 · LF17 · LF20 · LF22 · LF23 · LF24 · TR04 · TR06 |
| H7 | LF01 · LF03 · LF14 · LF16 · LF17 · LF20 · LF22 · LF23 · LF24 · TR04 · TR06 |

## 8. Offene Punkte und Grenzen

- Die Master-PNG ist nicht im Worktree. Die über `SPEC.md` dokumentierten Pixelmaße sind reproduziert; neue Bildmaße für Wege, Gebäude oder Vegetation lassen sich ohne die PNG nicht direkt nachmessen. Der Konflikt zwischen älteren Plateauwerten in `SPEC.md` und späteren Werten in `ABWEICHUNGEN.md` ist oben ausgewiesen; die Kachelbelegung und Sollhöhen verwenden den späteren Stand.
- Die Südflussbreite aus Schutzmaske (2,5 m) widerspricht der kartengerechneten Breite (7,4–10 m). LF14 setzt 7,4–10 m als Sollbreite und dokumentiert die 2,5-m-Messung als Ist-Abweichung.
- Die aktuellen Findlinge sind nach gespeichertem Maßparameter deutlich kleiner als das aus 210 px gerechnete Kartenmaß. Felsblöcke sind gar nicht platziert. Diese Sollabweichungen bleiben sichtbar und sind nicht durch die Messdokumentation behoben.
- Die 0,15-m-Objektauflage, Kantenradien von Mesh-Objekten, Übergangsbreiten und getrennte Kachel-Mesh-Nähte besitzen noch kein Gate. Die Stellen nennen jeweils das neu nötige Prüfskript.
- Das Dokument ändert keine Geometrie. Die bestehenden R-/G-Treffer sind damit Ausgangsbefund; ihre Einhaltung ist nicht durch das Regelwerk selbst bestätigt.
