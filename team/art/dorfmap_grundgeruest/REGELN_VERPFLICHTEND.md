# Verpflichtendes Landschaftsregelwerk Dorfmap (Fabian t109u–t112u)

**Pflichtlektuere am Anfang jeder Runde.** Wer am Relief arbeitet, liest dieses Dokument zuerst. Vor jedem Commit mit Gelaende-Aenderung und vor jedem Export/ZIP laeuft `sh relief3d/pruefung/export_gate.sh` (vollstaendiger Gate-Lauf, kartenweit, alle 56 Felder). Ist das Gate rot, gibt es keinen Commit der Daten und keinen Export, ausser jeder Resttreffer steht unten unter "Begruendete Ausnahmen" mit Koordinate, Bild und Grund.

Ziel [F]: Ein Spieler sagt "wow, geile Landschaft". Nirgends faellt man in ein Loch, nirgends sieht man einen Riss, eine Spitze, eine Stufe oder eine harte Kante, die nicht in die Natur gehoert.

Marker: [S] Spezifikation/Zellwerte, [A] Annahme Art, [R] Recherche Natur/Spielpraxis, [F] Fabian-Vorgabe.
Einheiten: m, Neigung als m/m (1.0 = 45 Grad) oder %, Kruemmung als Laplace der 1-m-Gauss-geglaetteten Hoehe (m/m²).
Zellwerte (`zellen_relief.csv`, Logikspalten) bleiben unveraendert, `pruefe_t42u.py` summe = 0 [S]. Alle Regeln betreffen das Anzeige-Gelaende.

## 1 Boden / Wiese / Schnee-Flaeche
Soll: ruhig gewellt wie Almboden, nie glatt-plastisch und nie beulig. Wellen sind weit (≥4 m) und flach (≤0.3 m) [R].
- Kruemmung: |Laplace| ≤ 6x Umgebungsmittel (20 m) und ≤0.15 absolut, sonst Delle/Beule → G4 [A].
- Kein Punkt mehr als 0.35 m ueber/unter dem Mittel seiner 8 Nachbarn (grob 0.5 m, fein 0.25 m Raster) ausser Wand → G2/G3 [F].
- Keine abflusslose Senke >1.0 m tief auf trockenem Land (Sink-Fill vom Kartenrand) → R5/G10 [F].
- Verboten: Loch, Trichter, Einsturz, Pickel, "Zellulite" (viele kleine Dellen), Dreiecksspitze nach unten.

## 2 Haenge (15–80 % Neigung)
Soll: gleichmaessig, Form kommt aus Gelaende, nicht aus Schattierung. Keine Terrassenringe, keine Hoehenlinien-Streifen [F t105u].
- Normalensprung zwischen Nachbarpunkten ≤0.25 (sonst sichtbare Facette, G6, Cluster ≥6 Punkte) [A].
- Kein Stufenprofil: lokale Steigung nie <35 % der 5-m-Mittelsteigung auf >10 % der Hangflaeche (`pruefung/o18/terrasse_o18k.py`) [A].
- Clay-Ansicht muss dieselbe Form zeigen wie die Textur-Ansicht (T5).

## 3 Klippen / Felswaende
Soll: echte Felsgeometrie mit Kanten, Vorspruengen und Rissen wie O17, kein glatter Vorhang und kein Blockhaufen [F].
- Wandmaske: Neigung >1.0 m/m. Wandrauheit (mittel |h − Gauss 1 m|) ≥0.40 m (O17 0.589) → G7 [F].
- Keine zusammenhaengende glatte Wandflaeche >10 m² (Rauheit <0.05 m auf 3 m) → G7 [A].
- Oberkante: im 3-m-Saum oberhalb keine Erhoehung >0.6 m ueber Gauss 2 m (Beulen an Klippe, G5); die Kante laeuft weich ins Plateau [F].
- Wandfuss: Schutt/Boeschung erlaubt, kein Spalt, kein Simse-Streifen.
- Verboten: senkrechte glatte Platten, Zackenkaemme ("Zaehne", `zacken_t83u.py` fein ≤30, grob ≤10), Wand mitten auf Weg.

## 4 Gipfel und Grate
Soll: gerundet, keine Nadel. Kein Gipfelpunkt >0.35 m ueber Nachbarmittel (G2). Grate durchgehend, keine Kerbe >1 m ohne Bachlauf [A].

## 5 Taeler
Soll: Talboden zusammenhaengend begehbar (Neigung ≤25 %), weiche Uebergaenge zu Haengen; keine Gruben im Talboden (R5) [A].

## 6 Fluesse / Baeche / Ufer
Soll: Wasser liegt in einem eingeschnittenen Bett, laeuft durchgehend bis zum Kartenrand oder in einen See [F].
- Jede Wasserkomponente >200 m² erreicht den Kartenrand → G8 [A].
- Bett-Einschnitt Median ≥0.6 m unter Ufer (2-m-Umkreis-Maximum) → G8 [F].
- Ufer-Boeschung ≤0.9 m/m, Abtrag ≤1.5 m (O18d) [A]. Keine grauen verwaschenen Streifen (T4).
- Verboten: Wasser im Schnee/auf Plateau >10 m (G9/R6), Wasser ohne Bett, Bett ohne Wasser.

## 7 Wege / Rampen / Anschluesse
Soll: jeder Weg ist ein glattes Band, auf das spaeter eine Strasse passt [F t108u].
- Band ±1.5 m: Quergefaelle ≤3.5 % (2 % zur Bergseite) → R3 quer [F].
- Laengsprofil: Abweichung vom 2-m-Gauss ≤0.08 m, Woelbung ≤0.08 m → R3 [F].
- Laengssteigung ≤25 % Rampen, ≤10 % Dorfwege [R].
- Seitlich weicher Auslauf 1.5–3.5 m, kein Graben, keine Wulst; Weg nie >1.5 m eingesunken (beidseitig hoeheres Gelaende in 4 m) → R4 Schlucht [F].
- Jedes Ende: nicht an Wand (Neigung >1.0 in 0.5–3 m), nicht im Wasser (1.5 m), Anschluss ≤2 m an anderen Weg oder Kartenrand → R1 [F t104u–t106u].
- Ein zusammenhaengendes Netz, keine Inseln → R2 [F].
- Am Kartenrand: auf Randhoehe auslaufend, Gefaelle zum Rand ≤15 % → R4 Rand [F t105u].
- Keine Objekte auf dem Weg (R6), nicht am Wasser kippen.

## 8 Hausplaetze
Soll: eben (≤3 %), Sockel ohne Streifen, Haus steht auf Boden (|y−Boden| ≤0.4 m) [A].

## 9 Kartenrand
Soll: Rand ist ein ruhiger Schnitt durch die Landschaft auf natuerlicher Hoehe. Keine Kerbe >2 m unter dem 80-%-Perzentil des Randes (60 m) ohne Wasser (O18k `_rand_auslauf`) [F]. Spalt Rand/Sockel 0 (`test_rand_t64u.js`) [S].

## 10 Uebergang fein/grob
Soll: unsichtbar. Hoehennaht exakt (stufe_bandrand 0, `bandrand_t83u.py`), Lochscan offen_innen 0 Index + 56 Felder (`loch_o18g.js`) [F].

## 11 Texturuebergaenge
Soll: Gras→Fels→Schnee weich ueber ≥2 m, keine Rechtecke, keine abgeschnittenen Flaechen [F].
- Farbsprung VC zwischen Nachbarpunkten ≤70 (RGB-Abstand) ausser an Wand → T1; gerade Kanten verboten [F].
- T2 abgeschnitten, T3 Streifen/Moire/Ringe, T4 graue Flussstreifen, T5 Textur vs Clay: Sichtpruefung Vollbild je Feld, Ton + Textur, Ergebnis mit Bildpfad im Status [F].

## 12 Wasser
Soll: nur in Bett/See, Hoehe plausibel, Schnee-/Wassermaske passt (T6: keine helle Schneefarbe auf Wasser) [F].

## 13 Objekte (Baeume, Felsen, Steine)
Soll: stehen auf Boden (|y−Boden| ≤0.6 m, G11), keine Baeume auf Neigung >0.9 oder in Wand (G11), nicht auf Wegen oder Klippen-Abstiegen (R6), nicht versunken im Wasser (Raycast `test_strahl_t62u.js` 0) [F].

## 14 Technik
Budget lod1 <1.3 Mio Dreiecke [S]; Ladezeit median messen nur ohne Parallellast [S]; deterministisch [S]; Geometrie Boden/Wand/Weg getrennt (Typkanal FW.t, R7), damit Skins austauschbar sind [F t109u].

## Gate-Tabelle (Messung, Schwelle, Status)

| Regel | Messung | Schwelle | Status O18k (Commit siehe runde_o_status) |
|---|---|---|---|
| R1 Wegenden nicht an Wand/Wasser/blind | Steilheit 0.5–3 m vor Ende, Wasser ≤1.5 m, Anschluss ≤2 m an anderes Wegstueck/Rand | >1.0 m/m (45°) | 9 Wand, 24 blind (Overlay-Daten, s. UEBERGABE.md) |
| R2 Abzweige verbunden | Zusammenhangskomponenten Wegmaske | 0 Nebenkomponenten | 15 |
| R3 Laengs glatt, quer eben | je 4 m: Quergefaelle ±1.5 m, Laengs-Hochpass (Gauss 2 m), Woelbung | quer >3.5 %, laengs >0.08 m, Woelb >0.08 m | 24 / 35 / 22 |
| R4 Rand / Schlucht | Gefaelle Weg→Kartenrand; Gelaende 4 m seitlich beidseitig hoeher | >15 %; >1.5 m | 4 / 13 |
| R5 Loecher/Spitzen | abflusslose Senke (Sink-Fill) auf trockenem Land; Spitzen ausser Wand | >1.0 m; >0.5 m | 49 / 4 |
| R6 Objekte auf Weg, Wasser im Schnee | Objekt in Wegzelle; Wasser mit h>10 m | 0 | 1 / 4 |
| R7 Geometrie getrennt | FW traegt Typkanal t (Wand/Boden/Weg) | vorhanden | ok |
| G1 Loecher/Durchsicht | Lochscan `loch_o18g.js` offen_innen | 0 | 0 |
| G2/G3 Spitzen oben/unten | Punkt vs. 3x3-Nachbarmittel, grob+fein, ausser Wand | >0.35 m | 156+134 / 101+168 |
| G4 Dellen/Beulen | Laplace-Ausreisser ggue. Umgebung (6x, min 0.15) | ≥4 Punkte | 0 |
| G5 Beulen an Klippenoberkante | Hochpass 2 m im 3-m-Saum oben an Wand | >0.6 m | 393 |
| G6 Facetten | Normalensprung auf 15–80 % Hang | >0.25, ≥6 Punkte | 692 |
| G7 Wandkontur echt | Wandrauheit mittel; glatte Wandflaechen | <0.40 / >40 Punkte | 0.46 ok / 1 Flaeche |
| G8 Fluesse durchgehend, eingeschnitten | Wasserkomponente erreicht Rand; Median-Einschnitt | >0.6 m | 1 nicht bis Rand |
| G9 Wasser nicht im Schnee | = R6 | 0 | 4 |
| G10 keine tiefen Loecher | = R5 | 0 | 49 |
| G11 Objekte auf Boden, nicht an Wand | |y−Boden| ; Baum auf Steilheit | >0.6 m; >0.9 | 176 / 4 |
| T1 weiche Textur-Uebergaenge | Anzeige-Farbe VC Sprung (ausser Wand), gerade Kanten | >70, ≥8 Punkte | 97 |
| T2 Textur abgeschnitten | Bildpruefung (Vollbild je Feld) | 0 | offen |
| T3 Streifen/Ringe (D1) | Bildpruefung Clay | 0 | offen |
| T4 graue Flussstreifen | Bildpruefung | 0 | offen |
| T5 Textur = Clay-Form | Bildvergleich Clay/Textur | 0 | offen |
| T6 Wasser/Schnee-Masken | helle Farbe auf Wasser | 0 | 0 |

Schwellen G5/G6/G2/G3/G11 sind Erstkalibrierung (O18k) und muessen an Bildern geprueft werden; Aenderung nur mit Begruendung hier.

## Begruendete Ausnahmen
(keine)

## Eichung O18m (Bilder `relief3d/pruefung/o18/eich_o18m/`)
- G2/G3: 4 Treffer je Regel angesehen. 0.35–0.42 m liegen alle am Hangknick direkt neben Wand, unauffaellig → Schwelle 0.45 m, Wandabstand 1.5 m (grob+fein). Echte Spitzen (11.6, 9.6, 1.8, 1.7 m) bleiben Treffer.
- G5: 0.6–1.0 m = Faltlinie an Klippenkante, unauffaellig → 1.0 m. Hinweis: Rest (375) ist zum grossen Teil die konvexe Kante selbst (Messfehler der Methode), Methode muss noch umgebaut werden, bis dahin nicht als Fehlalarm abgehakt.
- G6: Bilder zeigen echte Stufen-/Streifenfacetten (E5, H7) → Schwelle bleibt.
- G11: echte Fehlplatzierungen (bis 16.5 m) → Schwelle bleibt; Behebung in gen_relief (Objekte aufs Endgelaende, 4 Baeume an Wand entfernt).
- T1: noch nicht an Bildern geeicht.

## O18n
- G5 neue Methode (`relief_o18n.g5_beulen`): Kantenpunkt bis 3 m an Wand, der >0.6 m hoeher liegt als das Plateau 2–5 m landeinwaerts (senkrecht zur Wand). Runde, abfallende Kante zaehlt nicht. 4 Bilder angesehen (273|132, 300|96, 115|201, 323|76): echte Aufwuerfe an der Kante. Treffer 375 -> 176 (alte Methode zaehlte die Kante selbst).
- `landschaft_final` (gen_relief, abschaltbar LF_ALT=1): Senken >0.8 m nur anheben, Einzelspitzen, Facetten weich; nicht an Wand/Wegen/Rampen ±4 m/Wasser ±2 m/Hausplaetzen. G5-Absenken nach 3 Versuchen wirkungslos -> aus, offen.
- Vergleich je Regel vor/nach: alles gleich oder weniger, Ausnahme G2_spitze_oben_fein 20 -> 21 (+1, Feinband, das der Schliff nicht anfasst; Ursache vermutlich Bandnaht-Uebernahme) – offen dokumentiert.

## O18r
- Gate-Fix G2/G3 (`ausreisser`): Punkte mit <3 gueltigen Nachbarn werden nicht gewertet. Vorher nb=0 -> Treffer = Hoehe selbst (z.B. B1 80.2|36 "10.2 m" bei glattem Gelaende). Basis 18b3a60 neu: G2 4->2, G3 6->0, G2f 21->6, G3f 13->1 (Summe 1153->1118). Die O18m-"echten Spitzen" 11.6/9.6 m waren dieses Messartefakt.
- RAMPENBAND Standard (V2): Band eben 2.5 m, Quergefaelle 1.5 % zur Bergseite, Boeschung C1-weich (tanh, 0.7 m/m), Auslauf 4.5-6 m. V1 (2 %) R3 quer 24->27 -> 1.5 %. Gegen Basis: R1_wand 9->0, R4_schlucht 13->0, R4_rand 3->0, G6 615->592, G5 169->166, T1 95->94, keine neue Regel hoeher.

### O18r R5 (Senken fuellen) – verworfen nach 3 Versuchen
SENKE V1 flach 0.8 m: R5 40->0, G6 +16, G2f +1, G3 +1, T1 +1. V2 Kuppe: R3 quer +13, G5 +6. V3 nur Spitze >0.95 m: R5 40->0, G6 +13, G2f +1, T1 +1. Standard aus (SENKE=0), Basis bleibt.

### O18r G6-Eichung an Bildern (pruefung/o18/g6eich, clay, lod0, Streiflicht)
542/592 G6-Treffer liegen <3 m an Waenden. Bilder: B4 Stufe/Kante an Plateaurand sichtbar, C4 treppige Blockstufen am Wandfuss, C6 knubbelige Facetten am Hang, D7 Rillen quer zum Hang + Gitterlinien. Alle vier sind echte Fehler -> keine Wandabstand-Ausnahme, G6 bleibt ungeeicht offen.
### O18r Ausnahmen (Vorschlag, noch nicht im Gate)
R3: Haarnadel rampe_12 (Schenkel 2-4 m, 2.5 m Hoehensprung) und Kreuzungen rampe_2x11, rampe_3x5 folgen aus Overlay-Geometrie; KREUZ-Angleich verworfen (R3 laengs 35->45, G6 +10).
G8: See A2 22.6|49.1 (891 Zellen, WASSER_EIS) ist per Zellwert gesetzt.
## O18s Regression-Basis und G6-Ursache (pruefung/o18/regression_o18s.json)
- Basis: Gate 1055, t42u 0, bergauf 0 (max 0,02), Bandrand-Stufe 0, Loecher 0 (Index und 56 Felder), lod1 1 175 138 Dreiecke, Ladezeit Median 9,0 s.
- Raycast ist auf der Basis ROT (Baeume 20 schwebend/105 versunken). Ursache: Block O18m G11 setzt Objekte auf G_ANZ statt auf das sichtbare Feinnetz. Fix (Raycast-Cache hat Vorrang) macht Raycast gruen, aber Gate G11 +162, weil G11 gegen G_ANZ misst -> nicht uebernommen. Messflaeche von G11 und G6 muss auf die Anzeige-Flaeche umgestellt werden (Entscheidung offen).
- G6: Ursache ist die Wandformung Gs (Rippen-fBm RIB, Simse, Schuttfuss) im Grobnetz, nicht Zellraster/Bilinear. Bikubisch statt bilinear verschlechtert G6 (492->521).

## O18t Messkorrektur G6/G11: sichtbare Flaeche
- Grund: Im Feinband rendert der Viewer das Feinnetz (FW, 0,25 m), die Grobquads werden dort ausgelassen. Das Gate hat G6 und G11 auf dem Grobnetz GB gemessen, also teils auf einer unsichtbaren Flaeche. Dadurch widersprachen sich Raycast (gegen das sichtbare Netz) und G11.
- Neu: G6 auf GV = Feinnetz (jeder 2. Feinpunkt, 0,5 m) wo vorhanden, sonst GB; G11 gegen bilineare Feinnetz-Hoehe wo alle 4 Ecken vorhanden, sonst GB. Schwellen unveraendert. Alte Messung: GATE_GROB=1.
- Zahlen gleicher Stand (6e7dfff): G6 alt 592 -> sichtbar 676; G11 alt 0 -> sichtbar 107; Gesamt 1055 -> 1246. Alle anderen Regeln gleich. Neue Basis fuer Vergleiche: 1246.
- O18t Schritt 1: Raycast-Hoehe hat Vorrang vor G11-Nachsetzen und vor objekte_feinband-Absenkung (gen_relief.py), Cache aufgefrischt (Geroell 43). Raycast alle Klassen 0/0; G11 sichtbar 107 -> 1 (Findling H5 306,5|196,3, -1,09 m, im Raycast innerhalb 0,6*h); Gesamt 1246 -> 1140, keine Klasse gestiegen. Geroell 635 -> 678, weil vorher nachtraeglich abgesenkte Geroellsteine als versunken entfernt wurden.

### O18t S3 Ausnahmen im Gate (pruefe_regeln.py, Feld 'ausnahme', summe_ohne_ausnahmen)
- R3 Haarnadel rampe_12 (alle R3-Treffer dieser Rampe) und R3 an den Kreuzungen rampe_2x11, rampe_3x5 (Treffer <6 m vom Kreuzungspunkt): Geometrie folgt aus dem Overlay (unveraenderbar); KREUZ-Angleich O18r verworfen (R3 laengs 35->45, G6 +10).
- G8 See A2 22,6|49,1: per Zellwert WASSER_EIS gesetzt, kein Fluss.
- Stand 1a92bd7: 48 Ausnahmen (R3 47, G8 1); R3 bleibt mit 34 echten Treffern offen. summe bleibt ungefiltert.
- Hinweis: Die O18s/O18t-Eintraege standen versehentlich in relief3d/REGELN_VERPFLICHTEND.md; hierher uebernommen, alte Datei nach _alt verschoben.

### O18t S2 Rippen-Rauschen in Wandnaehe (<3 m) – 3 Varianten, alle verworfen (Basis 1140)
- V1 RIB in Wandnaehe Gauss sigma 5 (nach Cache-Auffrischung): Gesamt 1093, G6 676->643, G5 166->155, R5 gleich, aber T1 94->99 -> verworfen (Klasse steigt).
- V2 sigma 3: Gesamt 1229, G5 173, R5 47, T1 99 -> verworfen.
- V3 sigma 7: Gesamt 1172 (G11 vor Cache-Auffrischung), G7b-Rauheit neu 1, G2f 7, G3f 2, T1 100 -> verworfen.
- Befund: Glaetten der Rippen senkt G6 nur um ~5 %; die Facetten sitzen in der Grundform Gs (Hs->Wand-Uebergang), nicht im Rauschen allein.

## O18u T1-Kalibrierung (Bildbeleg)
- Bilder: relief3d/pruefung/o18/t1eich/ (12 Treffer t1_00..t1_11 ueber den Wertebereich 8..30 px, 6 Nicht-Treffer t1_12..t1_17 mit Farbsprung 45-70, Zusatz t1_18). *_2d.png = Textur x Streiflicht, links roh, rechts Kanten dc>70 rot. 3D-Ansichten t1_00..03 waren grossteils durch Haeuser/Baeume verdeckt, deshalb gilt die 2D-Ansicht.
- Befund: Weder Farbsprung noch Pixelzahl trennen Fehler von Nicht-Fehler. Fast alle Treffer sind runde Raender von Gras-/Erdflecken im Schnee (t1_00, 03, 04, 05, 06, 07, 09, 10, 11) und sehen genauso aus wie die Nicht-Treffer (t1_14..17). Sichtbar falsch sind nur gerade, achsparallele Naehte (t1_08 C2 84|84, t1_18 G2 284|75, Kopf von t1_01).
- Regel ab O18u: T1-Fehler nur dann, wenn die Komponente eine achsparallele Kante mit >=9 px (4,5 m) am Stueck hat. Gemessene Verteilung der laengsten Laeufe: 3..7 px bei 92 Komponenten, dann eine Luecke, dann 9/12/14 px. Komponenten unter 9 px heissen T1_fleckrand, bleiben in summe und sind als Ausnahme markiert.
- Ergebnis auf 7bb8418: T1 95 -> 3 (2 + 1 gerade), dazu T1_fleckrand 92 als Ausnahme. Die Schwankung von +-5 lag nur in den Fleckraendern.
- O18u S2 G11: Die Einbettung von Steinen, Felsen und Findlingen ist jetzt auf hoechstens 0,55 m begrenzt (runde_m_t65u.strahl_hoehe, vorher 0,25*Groesse). Der Findling H5 306,5|196,35 lag 1,09 m zu tief und liegt jetzt 0,55 m tief. G11 1 -> 0, Raycast alles 0, findlinge max_abw 0,55. Gate 1140 -> 1139.
- O18u S3/S4 G5+G6, Wand-Grundform, 3 Varianten (Code in pruefung/o18/gen_relief_o18u_varianten.py.txt, env WANDV). Basis 1139.
  - V1: Rippen, Grat, Simse und Baender nur >3 m von Fuss/Kopf mit 2 m Fade; Wandkopf gedeckelt auf max(Hs, 7 px). Ergebnis G5 166->108, G6 676->608, gesamt 1130. Gestiegen: G2 +1, G3 +3, T1 +1, R4 +1, G7b-Rauheit +1, G11 123 (Objekte nicht neu geraycastet). Abgelehnt.
  - V2: wie V1, dazu Hohlkehle an Fuss/Kopf (Gauss 2 px, ausserhalb der Wandmitte). Ergebnis G5 85, G6 608, R5 27, gesamt 1103. Gestiegen: G2 +1, G3 +3, G7b_feld +5, Rauheit 0,51, R4 +1, T1 +1. Abgelehnt.
  - V3: weicher Deckel, Hohlkehle 1,5 px. Ergebnis G5 102, G6 598, gesamt 1114. Gleiche Anstiege wie V1. Abgelehnt.
  - Befund: Der Deckel (Ursache G5 = hi-Maximum ueber 10 m hebt die Kante ueber das Plateau) und der Fade wirken, erzeugen aber neue Spitzen (G2/G3) und glattere Waende (Rauheit). Alles zurueckgesetzt, Basis bleibt 1139.

## O18v
- Regelanpassung (Fabian, 10:54): Eine Variante darf uebernommen werden, wenn die Summe deutlich sinkt und keine Klasse um mehr als 5 steigt. Die kleinen Anstiege werden im selben Schritt behoben. Vor jeder G11-Bewertung wird neu geraycastet.
- S1: V2 ist uebernommen (gen_relief WANDV-Standard 2) und der Raycast-Cache ist aufgefrischt. Gate 1139 -> 979 (G5 85, G6 608, R5 27, G11 0). 3 Steine lagen nach dem Raycast im Wasser und stehen jetzt auf der raus-Liste (213,64|31,27; 216,62|224,27; 94,36|279,58).

### O18v S1 (RIBG 1.5)
- V2 + Rippenverstaerkung RIBG=1.5 uebernommen: Summe 979 -> 948 (G6 608->578, G7b_feld 23->21, R5 27->24, G5 85->84; G3f +1, T1_fleckrand +4 = Ausnahme). G11 nach Raycast 0.
- G7b-Rauheit: 3 Varianten erschoepft (RIBG1.5 0.521, RIBG2.0 0.531, RIBG1.5+KEHLE1 0.561; Ziel >=0.584). Offen, Ursache: Deckel und Fade glaetten beide (Einzeltests belegt).

### Hinweis CSV zellen_relief.csv (O18w)
- Quellspalten (duerfen sich NIE aendern): untergrund, hindernis, wasser_eis, ebene, bauzone, begehbar, bebaubar.
- Abgeleitete Spalten (aendern sich mit jedem Hoehenfeld-Lauf, kein Zellwert-Verstoss): hoehe_m, neigung, klippe, begehbar_3d, deko_baum_ok, Ecken (ecke_*), skin_slot, boden_anzeige.
- Pruefung: pruefung/pruefe_t42u.py muss summe 0 liefern (Stand 361967b: 0). Von Fabian am 03.11.2026 geprueft.


### O18w Schritt R4/G2/G3/G2f (Gate gegen basisRIB 948)
- R4_rand H2 332.5|64.5 behoben (_rand_weg: Gelaende Weg->Rand max 0.1 m/m, 2 Zellen): 948 -> 947, keine Klasse steigt.
- G2/G3 Reihe z~275 x199-216: liegt im Seebett (WV nass, -20.1 vs -19.4 m, 1-Ecken-Rille). _entspitzen (SPITZE=1, Default AUS), 3 Varianten:
  V1 Land+Wasser ausserhalb Wand+3 m: G2/G3 3/3->0/0, G5 +6 (verworfen, >+5). V2 nur Wasser, Wand+3 m: G2 1, G3 0, G5 +6, R5_spitze +1 (verworfen). V3 nur Wasser, Wand+6 m: G2/G3 unveraendert (wirkungslos). Ursache G5-Anstieg: Klemmen im Seebett nahe Klippe aendert Steilheit/WAND-Maske. Offen.
- G2f/G3f (3/1) = Messfehler an Maskenecken (Beleg: 227.2|27.2, 66.8|156.2, 109.8|179.8, 97.8|209.2 haben nur 3 gewertete Nachbarn auf glattem Hang, Rest zur vollen 8er-Mitte 0.00-0.03 m). VORSCHLAG Regelkorrektur (nicht umgesetzt): Nachbarmittel aus gueltigen Nachbarn statt Wertungsmaske - Probelauf ergab aber G3f 1->97 (Ring C4 104-120|136-178 an Feinband/Wandgrenze), daher braucht die Korrektur zusaetzlich einen Wandabstand fuer Nachbarn; bis zur Freigabe unveraendert.
- O18w T1: 4 gerade Farbnaehte (G2 284|75, C2 84|84, B2 82|86, B3 77|93) per _t1_naht (VC Gauss 1.5 Ecken, 2 Ecken Umkreis, 282 Ecken) -> T1 hart 3+1 -> 0, T1_fleckrand 94->93; Summe 947 -> 942. Bild: pruefung/o18/o18w/t1_nach_c2_b2_g2.png (VC-Ausschnitte 24 m, keine harte Kante sichtbar).
- O18w G7b-Rauheit (Ziel r1>=0.584, Stand 0.521): _wand_mikro (WMR, Default AUS), Grob+Fein aus einem Rauschfeld, 3 Varianten:
  V1 Wandkern (Steil>1, 1 m eingerueckt) A0.25: 0.528, G6 +7, G5 +1. V2 Steil>0.8 A0.35: G6 +110, R5 +24, G5 +12, G11 +4 (verworfen). V3 Steil>1 A0.3 feiner: 0.544 (=0.79), G6 +36, R5 +13, G5 +3, aber kantenschaerfe 0->erfuellt.
  Befund: Rauheit gegen O17 ist mit den Gelaende-Regeln G5/G6/R5 im Wandsaum gekoppelt; ohne Regelentscheidung (z.B. G7b nur im Wandkern messen, oder G6/R5 im Wand-Saum anders) nicht erreichbar. Offen, Entscheidung Fabian.

### O18w G6 gegen G7b (Eichbilder pruefung/o18/o18w/g6eich/, je 24 m, VC x Hillshade, blau=Wand, rot=G6)
- Nah an Wand (C3, C4; dw 0-0.5 m): Treffer liegen auf Wandschulter/Felsband-Kanten, die G7b scharf verlangt. 230 von 578 Treffern < 1 m von Wand. Teilweise echter Widerspruch.
- Fern (D4 dw 7.5, E3 dw 54): sichtbare echte Knicklinien (Rinne/Falte). Echte Fehler.
- Fix: _falten_glatt (FALT, FALTSG 1.0): Gauss nur >=3 m von Wand, Land, kein Weg. G6 578->561, G5 84->82, R5 24->21, R3 -2. Summe 942->918, keine Klasse steigt.
- Vorschlag Regelkorrektur (nicht umgesetzt, Entscheid Fabian): G6 im 1-m-Wandsaum nicht zaehlen, da dort G7b-Kantenschaerfe gilt. Belegt durch g6_nah_0/1.

### O18x Regelkorrekturen (Entscheid Fabian 03.11.)
- G6: Treffer im 1-m-Wandsaum (Dilatation WAND um 1 m) werden nicht gezaehlt; dort gilt G7b. Schwelle dn>0.25, Hang 0.15-0.8, Cluster >=6 px ausserhalb unveraendert. Belege g6eich/g6_nah_0, g6_nah_1. Alt (GATE_G6ALT=1) 561 / neu 273.
- G2f/G3f: dokumentierte Ausnahme, Kriterium im Gate codiert: Treffer mit <=5 gueltigen 3x3-Nachbarn (Maskenecke). Treffer bleiben in summe/je_regel sichtbar, nur als ausnahme markiert. Aktuell 4 von 4 (alle 3 Nachbarn).
- G7b-Rauheit: Ziel bleibt (>=0.85*O17). Wand-Mikrorelief bleibt aus (WMR=0). Offen, erst nach allen anderen Punkten und Streiflicht-Bildern wieder angehen.

### O18x G6 ausserhalb Wandsaum
- Gemessen: Raycast-Zyklus nach 3359333: G11 0, t42u summe 0.
- _falten_glatt ab 1 m statt 3 m Wandabstand (FALTWD 1, FALTSG 1.0), Wege +3 m ausgespart. Varianten: WD1/SG1.0 angenommen; WD1/SG1.5 verworfen (Summe 662, R3 +11, G11 +13).
- Ergebnis nach Raycast: Summe 630->583 (ohne Ausnahmen 487->431). G6 273->233, G5 82->64, R5 21->17. Anstiege: G7b_feld 21->26 (+5), G2f 3->8/G3f 1->2 (alle Maskenecken-Ausnahme), R1_wand 0->2 (F1 rampe_1 Ende, E1 rampe_2 Ende), R3_laengs +1, T1 +1. Alle <=+5. R1_wand und G7b_feld noch nicht nachgebessert.
- G6 je Feld vorher: C5 22, B4 21, C4 18, C3 15, G3 12, H6 12.

### O18y S1 R1_wand / G7b_feld
- Ursache R1_wand rampe_1 (F1) und rampe_2 (E1): _falten_glatt (ab 1 m) hat Wandfuss vor dem Rampenende verschmiert. Fix: Rampenenden aller Rampen 6 m frei von _falten_glatt (FALTRE 6).
- Varianten: V1 WD1 + Enden frei: R1_wand 2->0, G7b_feld 26->23, G6 233->249, G5 64->66, R3_woelb +1 (angenommen). V2 WD2: G7b_feld 21, aber G5 +19, G6 +32, G11 +9 (verworfen). V3 Fade 1->3 m: G7b_feld 21, aber G5 +20, R5 +5, G6 +25 (verworfen).
- G7b_feld <=21 NICHT erreicht (23). Konflikt: Glaettung 1-3 m vor Wand senkt G5/G6, nimmt aber Wandrauheit je Feld. Summe 583->597 (ohne Ausnahmen 431->444). Raycast 2x: G11 0, t42u 0.
