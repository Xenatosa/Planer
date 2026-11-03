# PLAN O18 neu (t126u) – nur Analyse, wartet auf Freigabe

Stand: Branch art/dorfmap-grundgeruest, Commit nach 80a0c62. Seit t126u wurde keine Geometrie und keine Pipeline geaendert.
Der Schattenversuch in main.js ist zurueckgesetzt und liegt als Kopie in /workspace/kreuz/main_schatten_versuch.js.

## 1. Fehlerklassen mit gemessener Ursache
| # | Klasse | Ort / Beleg | Gemessene Ursache | Status |
|---|---|---|---|---|
| K1 | Kreuzung abgehackt | D1 rampe_2 x rampe_11 152.3\|28.5, Bild o18_kreuzung/vorher/D1_ton.png | `_weg_eben()` setzt jeden Punkt auf das Laengsprofil der *naechsten* Rampe (kd.query bis 6.1 m). rampe_2 liegt dort bei 5.73 m, rampe_11 bei 4.53-5.43 m, also an der Voronoi-Grenze ein Sprung von 1.0-1.6 m. Gemessen: Stufe 1.39 m je 0.25 m, Gitter 2.18 m, Quer 23 %. Das Gate sah es nicht, weil `_ausnahme` R3-Treffer bis 6 m um rampe_2x11 und 3x5 ausnimmt. | gemessen |
| K2 | weitere Kreuzungen/Kehren | R8-Lauf (r8_kreuzung.py): Summe 41 (Stufe 9, Gitter 10, Quer 22), 31 Knoten. C3 Kehre rampe_12: Stufe 0.95, Quer 141 %. D6 rampe_3x5: 0.46 / 0.34 / 15 % | Gleiche Ursache wie K1 (naechste Rampe springt; bei der Kehre derselbe Weg mit >8 m Laengsabstand) | gemessen |
| K3 | Wegende ohne Auslauf | G1 rampe_1 oben 273.4\|21.2; Wegenden H4/G3 rampe_9, D1 rampe_11, H5, C5, C6 mit Stufe 0.22-0.34 m | Das Band endet am letzten Rampenpunkt. Der Uebergang macht nur das Quer-Fade 4.5-6 m, es gibt keinen Laengs-Auslauf. 24 von 24 Rampenenden sind R1_blind (Kontakt zu Dorfweg <1.5 m: 0) | gemessen, G1 oben nur 0.05 m Stufe: der Absatz ist dort die Bandkante quer, noch zu messen |
| K4 | Delle neben Weg (G1) | G1 unter der Plateaukante (Fabian Bild 1) | **Noch nicht gemessen.** Verdacht: Boeschungs-tanh in `_weg_eben` und `_senke_fuellen` hebt nur Gruben >0.95 m an, flachere Mulden bleiben. Messen: lokales Minimum, Tiefe gegen den Rand, Stufe, die es erzeugt hat (Zwischenstaende speichern) | offen |
| K5 | Saegezahnrand D1 | Bild t123u, saege/D1_schatten_an/aus/neu.png | Zwei Ursachen. (a) Schattenkarte: 4096 Texel ueber 476 m = 0.116 m je Texel, bei Sonne el 22 Grad am Boden 0.31 m, plus PCF-Radius 1.6. Das macht die gezackten, verschmierten Hell/Dunkel-Raender. Mit Schatten aus sind sie weg, mit einem Schattenfrustum, das der Kamera folgt (min ±24 m), werden die Raender scharf (Versuch, zurueckgesetzt). (b) Senkrechte Streifen auf der Wandflaeche unten links bleiben auch ohne Schatten: Geometrie-Facetten im 0.5-m-Grobraster (Wandkante als Treppe) | (a) belegt, (b) Zahl offen |
| K6 | Wellen im Hang unter der Plateaukante G1 (Bild 3) | G1 | offen; Verdacht: Ueberlagerung aus Bandboeschung, `_falten_glatt` (spart Wege +3 m aus) und Rand-Fade | offen |
| K7 | Wandform, Wandkronen | t118u offen | nicht neu gemessen | offen |
| K8 | Facetten G6 | Gate G6 | Normalensprung dn>0.25; `_falten_glatt` spart Wege/Waende aus | Basiswert aus letztem Gate |
| K9 | Rauheit Wand | o18j_wandrau | Grob/Fein gegen O17, laut Log | Basis vorhanden |
| K10 | Rampen-Rillen | sichtbar in D1_ton (Laengsstreifen) | offen; Verdacht: Feinband 0.25 m gegen Grob 0.5 m an den Bandkanten (T-Naht) | offen |
| K11 | Terrassen C2 | Fabian frueher | nicht gemessen | offen |
| K12 | G5, R5, R6 (aus t118u) | Gate | Werte aus dem letzten Gatelauf | offen |

## 2. Messregel und Grenzwert je Klasse
- **R8 Kreuzung:**
  - Stufe ≤0.20 m je Nachbarpunkt (0.25 m) innerhalb 4 m.
  - Gitter-Residuum ≤0.15 m je 1 m (Ebenenfit r 2 m).
  - Quer ≤3 %, Kreuzungsflaeche ≤2 %.
  - Keine Ausnahmen (die `_ausnahme`-Regel fuer Kreuzungen faellt weg).
- **R8a Wegende:**
  - Auslauf ≥4 m.
  - Absatz ≤0.10 m je 0.25 m am Ende und an der Bandkante.
  - Quer am Ende gemessen senkrecht zur Wegrichtung, nicht als Gesamtneigung (sonst zaehlt das Laengsgefaelle mit: 4-7 % Fehltreffer).
- **R8b Delle:** lokales Minimum >0.30 m unter dem Ueberlaufrand, innerhalb 6 m von Weg/Kreuzung, nicht auf Fels/Wand.
- **R9 Saegezahnrand:**
  - Hoehen- bzw. Neigungskante (Wandoberkante/-fuss, Bandkante): Zickzack-Amplitude quer zur Kante >0.15 m bei einer Periode <2 m = Treffer.
  - Messung: Kantenlinie per Gradientenschwelle, Abweichung zur geglaetteten Linie (Gauss 2 m).
  - Zusaetzlich Bildregel: Schatten-Texel am Boden ≤0.05 m in Nahsicht.
- **Wellen (Hang):** Amplitude der Hoehe minus Gauss 3 m >0.10 m bei Wellenlaenge 1-4 m auf Hang 0.15-0.8 = Treffer.
- **G1-G11, T1-T6, R1-R7:** wie bisher. Zusaetzlich: kein Wert darf um mehr als +5 steigen, t42u = 0.

## 3. Loesungsansatz, Reihenfolge, Abhaengigkeiten, Risiko
1. **Gate zuerst:**
   - R8/R8a/R8b/R9 und die Wellenregel in pruefe_regeln.py bzw. export_gate.sh, kartenweit mit Liste je Kachel.
   - `_ausnahme` fuer Kreuzungen entfernen.
   - Neuen Basiswert festhalten.
   - Risiko: keins an der Geometrie, aber die Gate-Summe steigt sichtbar (ehrlicher Ausgangswert).
2. **K5a Schatten:**
   - Frustum folgt der Kamera (min ±24 m, max ±238 m), Sonne relativ zum Ziel.
   - Abhaengigkeit: keine.
   - Risiko: Schattenspringen beim Kamerafahren (deshalb nur bei >5 % Zielverschiebung nachziehen) und die Fernsicht unveraendert.
   - Bildvergleich Nah und Fern.
3. **K1/K2 Kreuzungsflaeche (neue Stufe direkt nach `_weg_eben`, Grob und Fein gleich):**
   - Je Knoten Hc = Mittel der Armprofile.
   - Ebene Scheibe r 2.5 m, ≤2 %.
   - Je Arm das Laengsprofil mit Smoothstep ueber L = max(8 m, |dh|/0.08) auf Hc ziehen.
   - Bandhoehe als gewichtetes Mittel 1/d^4 statt der naechsten Rampe (kein Voronoi-Sprung).
   - Boeschung 0.7 ab 2 m, tanh wie O18p.
   - Risiko:
     - Laengsgefaelle der Arme steigt (D1: rampe_11 muss ~1 m ausgleichen, ueber 8-12 m sind das +8-12 %; R3 laengs pruefen).
     - O18r KREUZ=1 hatte so R3 35→45 und G6 +10.
     - Gegenmittel: L verlaengern, Scheibe kleiner. Hoechstens 3 Varianten.
4. **K3 Wegende-Auslauf:**
   - Je Ende ein Laengsfade ≥4 m (Band → Gelaende, Wand oder Platz).
   - Die Bandkante am Ende mit einem halbrunden Fade statt einem harten Abbruch.
   - Abhaengig von 3 (gleiche Knotenliste).
   - Risiko: R1 (Wegverbindung) und G11 (Objekte auf dem Gelaende), deshalb den Raycast neu laufen lassen.
5. **K4/K6 Delle und Wellen G1:**
   - Erst messen, welche Stufe sie erzeugt (Zwischenstaende speichern).
   - Dann gezielt in dieser Stufe beheben (z. B. Mulden ≥0.3 m neben dem Weg auffuellen, nur anheben).
   - Risiko: R5 und G5.
6. **K5b, K10, K8 Facetten, Rillen, Wandstreifen:**
   - Ursache per Zahl klaeren (Grob/Fein-Naht, Rasterdiagonale).
   - Danach Feinband-Kantenausgleich.
   - Risiko: lod1 <1.3 M Dreiecke, Naht-Gate.
7. **K7, K11, K12** danach, jeweils mit eigener Messung.

## 4. Pruefablauf je Schritt
- Bau: `gen_relief.py`, dann `baue_html.py`.
- Gate: `export_gate.sh` (alle Regeln, keine Ausnahmen).
- Regression:
  - Raycast loch_o18g.js vor G11,
  - t42u = 0,
  - Naht,
  - lod1 <1.3 M,
  - keine Klasse +5.
- Nahbilder:
  - Alle 56 Kacheln A-H x 1-7, je Kachel Ton mit Streiflicht schraeg von oben, lod=0, plus Textur mit Wegen AN.
  - Jedes Bild einzeln im Vollbild ansehen.
  - Je Kachel einen Befundsatz in pruefung/o18/kachelbefund.md.
- Vorher/nachher fuer D1, G1 und 3 weitere Kreuzungen, Ablage in /workspace/o18_kreuzung/.
- Commit und Push je Schritt.
- Geliefert wird erst, wenn alle 56 Kacheln alle Regeln bestehen. Ist etwas nicht loesbar, wird es mit Zahlen gemeldet und nicht mitgeliefert.

## 5. Vorgehen REGELWERK_LANDSCHAFT_VOLLSTAENDIG.md
- **Elemente:** Wand/Klippe, Gebirge, Hang, Plateau, Weg/Rampe, Kreuzung, Wegende, Bach, Ufer, Felsen, Deko, Baeume (Platzhalter-Masse), Gebaeude (Platzhalter-Masse), Uebergaenge.
- **Je Element:**
  - Soll-Form,
  - Masse aus der Dorfkarte [S]/[R],
  - Proportionen,
  - Uebergang zu den Nachbarelementen,
  - Natuerlichkeit (Rauheit, Kantenradius),
  - Messregel mit Zahl und Grenzwert,
  - Pruefskript.
- Nur Form, Geometrie und Masse, keine Textur.
- Fehlende Messwerte werden erst gemessen: Ist-Verteilung je Element aus relief_daten, die Soll-Werte aus der Dorfkarte.
- Danach Abschnitte je Kachel A1-H7, die angeben, welche Elemente es dort gibt und welche Sollwerte gelten.
- Verlinkt aus REGELN_VERPFLICHTEND.md.
- Wird erst nach dem Kreuzungs-/D1-Auftrag geschrieben, wie verlangt.

## 6. Pruefung der New-Bot-Hypothesen (t127u, gemessen)
- **H1 "Raster kann Waende nicht":**
  - Teilweise bestaetigt.
  - 19 Wandzonen ≥10 m² (Neigung >1). Mittlere Horizontalbreite 4.5 m (9 Grobzellen), Hoehe 10.9 m, max. Neigung im Median 7.4.
  - Keine Zone ist schmaler als 2 m. Das Raster bildet die Waende also ab, aber mit ~1.2 m Hoehe je 0.5-m-Zelle. Daraus entstehen die Facettenstreifen (K5b).
  - Waende als eigene Meshes wuerden genau das beheben.
- **H2 "Saegezahn und Kreuzung aus Raster-Schwellwert":**
  - Saegezahn: widerlegt fuer den Hauptanteil. Ursache ist die Schattenkarte mit 0.116 m je Texel, bei el 22 Grad 0.31 m am Boden (Beleg saege/*.png).
  - Kreuzung: bestaetigt im Sinn "Umschalten statt Abstandsfeld-Mischung". `_weg_eben` nimmt die naechste Rampe, dadurch entsteht ein Sprung von 1.0-1.6 m.
- **H3 "Weg ohne Randueberblendung eingeschnitten":**
  - Fuer die Wegenden bestaetigt: es gibt keinen Laengsauslauf.
  - Fuer die Delle noch nicht gemessen.
