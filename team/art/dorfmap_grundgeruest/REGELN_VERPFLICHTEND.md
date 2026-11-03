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
