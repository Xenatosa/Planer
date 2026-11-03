# Runde O – Status (t67u)

> **Pflicht:** Regeln in `team/art/dorfmap_grundgeruest/REGELN_VERPFLICHTEND.md` (R1–R8, G1–G11, T1–T6). **Neu R8 Wegkreuzungen und Gabelungen** (Abschnitt "R8 Wegkreuzungen und Gabelungen", Beleg D1/G1 t120u). Vor jedem Export/ZIP `sh pruefung/export_gate.sh` (pruefe_regeln.py) – bei Treffern kein Export.

Basis 364ede6 (Runde N inkl. Nachher-Nahbilder gesichert).
Fabians Befunde: 1 Flussende Westrand, 2 Baeume auf Abstieg, 3/4 Nadelspitzen, 5 Trichter in Wand.
- [ ] A Fehlerzaehler pruefung/fehlerzaehler_t67u.py
- [ ] B Generator-Fixes
- [ ] C Sichtraster >=120 Nahbilder
- [ ] D Doku
- [x] O1 Flussende West: Ursache = Rundenpruefung M zaehlte je Strang nur EIN Randende; Westarm (Strang 12) endete bei x=2,5 z=245. Fix runde_o_t67u.rand_oeffnen: 39 Rasterzeilen bis x=0 offen, Spiegel faellt 0,03 m/Ecke. [F] 73 Randzellen x0-4 z240-278 nur Anzeige-Spalten (boden/wasser_anzeige). t42u summe 0 [S]
- [x] O2 Wege frei: 1,5 m + 0,5*h (Krone) bzw. 0,5*Groesse neben Wegzellen, Rampenachsen, Bruecken, Bauplaetzen, Plaetzen, Hoefen. Entfernt: Baeume 121, Felsen 2, Findlinge 2, Steine 127, Geroell 137 [S]. Baeume 1590->1468.
- [x] A Fehlerzaehler pruefung/fehlerzaehler_t67u.py; vorher (3f3210d): Spitzen 425, Nadeln>1,5m 56, Senken>0,8m 93, >2m 25 (max 6,04 m), enge Grate 818, Stufe Bandrand 2886, Objekte auf Wegen 389, Flussend-Kandidaten 4 [S]
- [x] O3 Entspitzen+Senken fuellen (runde_o_t67u.entspitzen): Spitzen 15, Nadeln 4, Senken>0,8m 1, >2m 0 (max 1,21) [S]. Zellen-CSV/glb unveraendert. Raycast-Hoehen muessen neu.

## O4 Objekthoehen
Raycast-Treffer (2985) in strahl_hoehe_t65u.json uebernommen, neu gebaut. objekte_voll: schwebend/versunken/im Wasser 0/0/0 fuer alle 5 Arten [S].

## O5 Bandrand-Stufen
Sichtbar in Clay (krater_1/2: rechteckige Kanten). Ursache: Feinband-Rand bis 5,5 m ueber/unter Grobnetz. Fix bandrand_weich (2 m Ueberblendung auf exakte Grobform). Stufen 2886 -> 0, Spitzen 15 -> 17, Nadeln 4 -> 8 (max 2,2 m bei 326|32), Senken >2 m 0, Spalt 0, t42u 0 [S]. Raycast noch neu noetig. b4-Ort gefunden: x~102 z~114 (Kegelfeld, b4h0b_vor).

## O6 Grate + Objekte
Grat-Stauchung gegen 5-m-Median (max 2,26 m Abtrag). b4-Kegelfeld (x~102 z~114) im Nachher-Bild weg, Grate im Hintergrund noch leicht zackig [S, angesehen]. Zaehler: Spitzen 16, Nadeln 8, enge Grate 775, Stufen 0. Raycast nach Uebernahme 0/0/0 [S].

## O7 Grate rund + Grobnetz-Nadeln
Laplace-Rundung konvexer Kanten: enge Grate 775 -> 272, Spitzen 16 -> 13 [S]. Grobnetz-Einzelspitzen ausserhalb Band gestaucht (22 Punkte, max 1,4 m) -> [F] 9 Zellen Anzeige-Spalten in zellen_relief.csv geaendert, t42u summe 0, Spalt 0 [S]. Nadeln >1,5 m: 8 (alle am Bandrand/Grobnetz neben Wasser/Band). Raycast nach Uebernahme 0/0/0 [S].

## O7 Sichtprüfung (Fabian-Kameras) [S]
- b34_spitze1–3_o7: Hänge rund, keine Stacheln/Kegel mehr sichtbar. b34_spitze4: Kamera steckt im Baum (Kamera unbrauchbar, kein Geländefehler).
- b5_senke_o7: Trichter weg, Mulde rund. b1_fluss_o7: Wasser läuft bis zum Kartenrand. fe0_o7: Fluss endet im See.
- Sicht-Raster 121+121 läuft neu nach test/t67u/sicht_o7 (alte Bilder in test/t67u/sicht bleiben).

## O8 (Stapel 1) [S]
- Defekte aus Sicht O7: wand_144_0_clay (Blick auf 167|19) und wand_264_0_clay (278|22): scharfe Nadeln am Wandfuss = Feinband-Nadeln 1 m innerhalb Bandrand (Zähler: 8 Stück, alle genau 4 Punkte vom Bandrand). krater_0–3_clay: rechteckige Schattierungsnähte.
- Fix: nadel_kappen (nur Nadelumgebung r=0,75 m, Übergang zum Bandrand weich, Rand selbst unverändert) -> Nadeln >1,5 m 8 -> 3, Spitzen 13 -> 9. Keine weitere Flächenglättung (Felskonturen bleiben).
- Fix: Normalen-Glättung in main.js ohne harte Schwelle bei ny=0,75 (weicher Übergang 0,65–0,85) gegen Nähte. Sichtprüfung folgt nach Neu-Render.
- Spalt 0, t42u 0, Raycast 0/0/0. bergauf entlang Pfad: 6 Ecken bei x 2,5–5 / z 253,5: der in O geöffnete Westarm fällt 3 cm/Ecke zum Westrand; der Prüfer kennt nur einen Auslass (Ost) und läuft den Arm rückwärts. Wasser fließt dort real zum Rand [A]. Schon in O7 so (nicht neu).

## O8 Stapel 2 [S]
- Rampen/Abstiege (Bild 2, Steuerhinweis): alte Rampen = 1,6 m breites Band, Höhe aus Grobnetz an nur 2 Randpunkten +0,10 m -> über Feinrelief schwebend oder eingesunken, harte Kanten, linealgerade (rampe_0–3_o8 alt, wand_96_24_tex, b34_spitze2_o7).
- Fix main.js: Höhe per Strahl auf sichtbare Oberfläche (Grob+Feinnetz), 5 Querpunkte (+2/+6/+7 cm), Ränder blenden auf 0 aus, leicht geschwungen (±0,45 m), Farbe linear (vorher zu hell). Nahbilder test/t67u/o8/rampe_*_nah_o8c/o8d.
- grob_entspitzen auch am Wasser (Boden >= Wasser+0,3 m): 20 Punkte, max 2,66 m. Rest: 13 Grobpunkte > 1,5 m an Feinband-Ecken (z. B. 158|18 6,1 m, 131|160 7,2 m) -- dort teilt das Grobnetz Ecken mit dem Feinband, Absenken würde einen Spalt reißen. Offen [S].
- Krater-Clay-Nähte: Test ?nosn=1 sieht gleich aus -> Ursache NICHT Normalen-Glättung. Offen.
- Wandbänder auf "zu glatt" geprüft (wand_*_tex O7): Felsflächen mit Kontur und Textur, keine weitere Flächenglättung gemacht.

## O8 Stapel 3 (Ränder/Flussenden/Rampen)
- Ränder nord 177/217, ost 80/195/265: Wasser läuft in Kerbe bis Rand [S]. west_276: eckiger Wasserblock mit harter Kante [S] offen. ost_283, fe1 (Baum), fe2 (Hausdach) verdeckt -> nicht beurteilbar.
- fe3 Wasser am Rand, fe4 Teich [S].
- b4h5b: dünne Nahtlinie in Felswand (Feinband-Rand) [S] offen.
- Rampen o8d (rampe_1/2_nah): dunkler, folgt Gelände, geschwungen, kein Lineal-Streifen mehr [S]. rampe_5/12_nah und 6–13 nicht angesehen.

## O9 Schritt 1 (Flussenden, Ränder, Prüfer)
- West 276: Zeilen-Lineal-Ufer -> Ufer um geöffnete Arme weich (Gauss 2 Zellen), Wasser folgt Ufer (kerbe()). Bild o9/rand_west_276__o9b, west_276_oben__o9b, rand_west_247__o9b, fe3__o9b: weiche Kerbe bis Rand, kein Block [S]. Erster Versuch (U-Profil je Spalte, o9a) gab Glaskasten-Grube -> verworfen.
- Neue Kameras ohne Baum/Dach: fe1_neu, fe2_neu, ost_283_neu (o9a) und fe0–4_oben (o9c). fe1_neu: flache Wasserfläche, frei sichtbar. fe2_neu: Rinne neben Haus, sichtbar. ost_283_neu: trotz neuer Kamera wieder Baum davor -> nicht beurteilbar (offen).
- 5 blinde Enden einzeln (Wasserhöhen-Auszug):
  - 223,5|219,5: Skelett-Ende an Stufe, Nachbarecke 2 cm tiefer -> fließt weiter, kein Ende.
  - 216|244: flache Fläche -17,25, hängt flach an -17,26/-17,30 -> Teil des Unterlauf-Sees.
  - 13,5|253: flacher Seitenzipfel -17,93, flach verbunden (979 Ecken) bis Ostrand x 336 -> Bucht, kein Ende.
  - 1,5|276: liegt am Westrand (1,5 m), Prüfer-Toleranz war 1 m -> Artefakt.
  - 321|276: Streifen -18,17 hängt am Ostausgang -18,20 -> Ausgang selbst.
  - Prüfer korrigiert: Ende blind nur ohne anstiegsfreien Wasserweg zum Rand. Jetzt 0 blinde Enden [S].
- Längsprofil-Prüfer: alle Randausgänge (auch West) als Auslass, Quelle nur aus randentwässernden Ecken. bergauf_pfad 6 -> 0 [S]. 3970 Ecken = Endsee-Becken x151–210/z42–194 (bis 2,73 m unter Überlauf) [A], getrennt als endsee_ecken gezählt.

## O9 Schritt 2 (Teilstand, Spitzen)
- grob_spitzen_alle (runde_o_t67u.py) auf G vor Feinband-Bau + in G_ANZ mitgeführt: 31 Spitzen/208 Punkte gestaucht, max 5,82 m. Spalt 0, t42u 0 [R].
- Fehlerzähler [R]: spitzen 11 (vorher 9 – neue lokale Maxima im Feinband), nadeln 3, senken>0,8 m 3 (max 1,7), enge Grate 249 (vorher 272).
- Angesehen [S] (o9d/e/f/g, clay): 158|18 + 161|22 deutlich besser (158|18 eine Facettenkante bleibt); 321|205 + 268|25 kleine Kegel/Facetten OFFEN.
  Nadel 314|36 = Felsgrat, natürlich. Nadel 93|100 = kleine Dreifachzacke auf Felskuppe, OFFEN. Nadel 67|42 Kamera unbrauchbar.
  Senke 110|113 = Mulde auf Felskuppe, wirkt natürlich. Senke 210|37 Kamera steckt in Fels, OFFEN.
- Enge Grate: noch keine Stichprobe. OFFEN.

## O9 Schritt 2b (Kegel/Zacken)
- Ursache 321|205 + 268|25: Kegel breiter als 5er-Median, direkt am Feinband-Rand (Bandnachbar, deshalb von grob_entspitzen ausgelassen). Fix: kegel_breit (9er-Median) auf G VOR dem Feinband-Bau, nur wo nicht Band-Inneres -> Fein folgt, kein Spalt. 5 Kegel/58 Punkte, max 2,78 m [R].
- 93|100 Dreifachzacke: Feinnetz-Rest (FH), Fix zacken_fein (2 Durchgaenge, Rand-Rampe 5 Zellen, nur absenken): 13 Zacken/344 Punkte [R].
- Bilder o9h/o9i [S]: 321|205 Kegel weg (flache Dreiecks-Schattierung bleibt -> Schritt 3 Normalen), 93|100 glatt, 158|18/161|22 ok. 268|25: flache Wandplatten am Kliffrand sichtbar -> Schritt 3 (Waende).
- Messung [R]: Spalt 0, t42u 0, spitzen 7, nadeln 0, senken>0,8 5 (max 1,7), grate 259, stufe_bandrand 0, blinde Enden 0.
- Kameras 67|42/210|37 von oben: nur dunkle Wand, keine Auffaelligkeit [S]; Ost 283 Texturbild steht in Baeumen/Haus -> neue Kamera von aussen folgt.

## O9 Schritt 3 (Naehte Clay)
- Ursache Kraterrand-Naehte: Normalen-Sprung an der Feinband-Grenze. Grob- und Feinnetz rechnen Normalen getrennt (je nur aus eigenen Dreiecken) -> gleiche Position, andere Schattierung -> gerade/polygonale Linien entlang der Bandgrenze. Keine Vertexduplikat-/Material-Naht (Positionen identisch, Spalt 0).
- Fix main.js: Randnormalen beider Netze = Gradient des Grobnetzes (gN9), im Feinband 0,75 m weich eingeblendet. Rein Schattierung, Positionen unveraendert.
- Bilder o9k (vorher) / o9l (nachher) [S]: krater_1 gerade Kanten weg, krater_2 Polygon-Umriss weg, krater_0/3 sauber; 268|25 flache Wandplatten weg (gleiche Ursache); wand_0_24 Zacken am Wandfuss weg.
- b4h5b: alte Kamera steckt im Fels; neue b4h5b_o/_o2 (o9m) zeigen keine Nahtlinie [S].
- Versuch Schuerzen-Normalen kopieren (o9m) gab feine dunkle Linien -> verworfen.
- Ost 283: neue Kamera ost_283_aussen (o9mtex, von ausserhalb des Kartenrands): Wasser laeuft weich in Rinne bis Rand, kein Baum vor Linse [S].

## O9 Schritt 4 – Rampen (erledigt)
- 28 Nahkameras (cams_o9r) gerendert, rampe_12 rendert fehlerfrei -> alter Ausfall nicht reproduzierbar [S].
- Nachgemessen [R]: Rampenband ueberbrueckte Feinrelief (1 m Abtastung), schweben max 1.42 m (rampe_9), Rampen 2/7/9/12/13 betroffen.
- Fix main.js: Rampenlinie 3x verdichtet -> schweben max 0.50 m, Stellen >0.15 m: 85 -> 41 (Rest: Querrichtung an Felskanten) [R]. Neu gerendert o9t, angesehen [S]: liegt auf, Gabel rampe_13 geschlossen.
## O9 Schritt 2 Rest – Senken/Grate angesehen (o9s, Ton) [S]
- 5 Senken: natuerliche Mulden/Tuempel, kein Fix.
- 12 Grate: meist echte Felsgrate. Offen: spitzer Zahn 105|47 und 225|228, Rautenmuster 54|162.
- zellen_relief.csv geklaert: Nebenprodukt (nur boden_anzeige_m, 63 Zellen), checkout, ABWEICHUNGEN, t42u 0
- O9 Reste: Einzelzahn-Klemme Grobnetz (gen_relief nach grob_entspitzen): 1 Zahn (105|47) [R]. 225|228 = Felskante an Wand (-10,9 m), 0,9 m, natuerlich -> belassen. 54|162 Rautenmuster = Dreiecksschattierung eines 0,6-m-Buckels im Grobnetz lod2, kosmetisch, belassen. Spalt viewer 0 [R]
- Untracked Bilder: o8/o9/sicht_o7 committet (Beleg), o9z per test/t67u/.gitignore
- O9 S5 laeuft: Vollrender o9z (Kette /workspace/t65/kette_o9y.sh, Log r_o9y_kette.log), Defektliste /workspace/t65/defekte_o9z.md; Textur-Boegen 0-17 angesehen (75/121)
- O9 S5 Fixes Stapel 1 (main.js): Rampenrand an Kanten geklemmt+ausgeblendet (>0,5 m quer), Rampenenden ueber 2 m weich ausgeblendet -> wand_312_168 "Brett" weich [S o9v].
- wand_48_120 "helles Rechteck" = Hauswand im Anschnitt, kein Gelaendefehler [S].
- wand_0_24 Zahnreihe: 2 Shader-Versuche (Flaechennormale, Feinschnee) ohne Wirkung [S o9w/o9u] -> zurueckgenommen; offen, Ton-Bild abwarten.
- S5: Textur-Boegen 0-27 alle angesehen [S]. Clay-Gegenprobe wand_0_24/fluss_7/fluss_9: Geometrie glatt, Zaehne/Treppen nur Farbe/Wasserrand (offen, kosmetisch). Clay-Kette laeuft (8/121).
- S5 (13:15): .gitignore in test/t67u korrigiert (Muster o9z/ relativ). Clay alle 30 Boegen verkleinert (6 je Bild) gesichtet [S], Einzelsicht folgt. Rampen 2/13 mit aktuellem index.html neu (o9r2) angesehen [S].
- S5 Clay: alle 34 Clay-Boegen (121+15 Bilder) einzeln in voller Groesse angesehen [S]. Keine Loecher/Risse/Schweber. Rest: Haarlinien-Schatten, Waschbrett an Steilhaengen (offen). Liste: /workspace/t65/defekte_o9z.md
- S5 Kosmetik (2a/2b), nur Shader/Farbe, keine Geometrie [A]:
  - Schnee-/Felsgrenze: Rauschen (nzS) + breitere smoothstep auf st, sn und vFS. wand_0_24 neu (o9n, o9n2) angesehen [S]: obere Schneekante jetzt weich statt Zaehne; Zacken unten rechts schwaecher, aber noch sichtbar (offen, vermutlich Schattierung schmaler Dreiecke).
  - Wasserrand: weiche Maske (gewichtete 5x5-Unschaerfe der Wasserzellen, Alpha per smoothstep im Fragment-Shader). fluss_7/fluss_9 neu angesehen [S]: kaum sichtbarer Unterschied. Die Treppen am linken Ufer von fluss_9 und die Saegezaehne an fluss_7 sitzen in der Ufer-Schattierung des Gelaendes, nicht in der Wasserkante -> mit Farbe allein NICHT behoben (offen, braeuchte Ufer-Geometrie-Glaettung).
- Aufgabe 3: rampe_2/rampe_13 mit aktuellem HTML neu (o9n) angesehen [S]: rampe_2 liegt am Hang auf, laeuft steil; rampe_13 Gabel = Kehre, liegt auf, nicht lineal-gerade. Kein Schweben gesehen.
- S6 Endmessung nach 3bc9d35 [S]: Spalt (Viewer) 0,0; t42u Summe 0; Fehlerzaehler spitzen 7, nadeln_1_5m 0, senken_0_8m 5, senken_2m 0, senke_max 1,7, enge_grate 259, stufe_bandrand 0, objekte_auf_wegen alle 0, wasser_ohne_randweg 5485, flussenden_blind 0; Budget 1 055 021 Dreiecke. Raycast: NICHT gemessen (2 Laeufe, Timeout 300 s beim Laden). Label "Runde O" steht schon. HTML kopiert nach /workspace/dorfmap_3d_runde_O.html.

### O9 Nachlauf (01.11., ab e3e67ad)
- N1 Raycast laeuft wieder [S]: test_strahl_t62u.js hat jetzt W/H/TO aus der Umgebung und loggt Seitenfehler. Mit W=1024 H=640 NOUI=1 war die Seite nach 158 s bereit (vorher 1280x800, 2x Timeout 300 s). Keine Seitenfehler, kein paralleles Chromium, Speicher 7 GB frei, Platte 17 GB frei. Ursache vermutlich die groessere Software-Render-Flaeche [A].
- N1 Ergebnis [S]: Raycast ist NICHT 0/0/0. baeume 17 schwebend / 129 versunken, felsen 1/3, findlinge 2/0, steine 10/0, geroell 54/96 (>0,15 m), im Wasser 0. Ursache: Objekthoehen kommen aus dem Raycast-Cache pruefung/strahl_hoehe_t65u.json (Runde M); das O9-Gelaende ist seitdem geaendert. Der letzte "Raycast 0" galt also nicht mehr. Fix folgt (Cache neu aus Raycast, neu bauen, nachmessen).
- N2 wasser_ohne_randweg 5485 aufgeschluesselt [S] (pruefung/wasser_ohne_randweg_aufschluesselung_o9.py), 15 stehende Gewaesser:
  - Endsee x151-211/z42-195: 3969 (gewollte Senke).
  - Tuempel West x11-33/z39-57 eben -9,45: 932 (seit Runde M gewollt eben), dazu 2 kleine Becken daneben 89 + 47.
  - 8 Eisflaechen Nord-Plateau (z 4-14, Spiegel ~13,6, WASSER_FARBE): 395, alle dicht.
  - 2 Pfuetzen Sued (z 208-212, senke_becken=1): 31 + 21, dicht.
  - 1 einzelner Wasserpunkt x4,5/z273: echter Rest -> wird entfernt.
  - Ueberlauf-Test (Bodennachbar tiefer als Spiegel -5 cm): nur Tuempel West, 5 Punkte, max 14 cm.
  - Fazit: Der Zaehler zaehlt jedes stehende Gewaesser. Ausser dem Einzelpunkt (und 5 Randpunkten am Tuempel) kein Flussfehler.

### N3 Ufer + Raycast (O9 Nachlauf)
- gen_relief.py: ufer_weich (Ufer-Hoehen bis 2 m vom Wasser, max 0,54 m, Mittel 0,08 m [S]), Einzelsenken-Hebung (4 Ecken [S]), vc_ufer_weich (Uferfarbe bis 3 m vom Wasser weichgezeichnet, 13,2 % der Ecken [S]).
- Ursache der Ufer-Treppen: die Uferfarbe folgte dem 1-m-Zellraster [A, Bildvergleich fluss_9_u gegen fluss_9_v]. Rechtes Ufer fluss_9: dunkle Streifen weg (angesehen). Linkes Ufer: Saegezaehne an der Wasserkante bleiben sichtbar (angesehen, NICHT behoben; Wasserkanten-Mesh, offen).
- Raycast-Cache strahl_hoehe_t65u.json aus neuem Lauf aufgefrischt; Raycast danach 0/0/0 in allen 5 Arten [S].
- wasser_ohne_randweg 5484 [S]: 14 stehende Gewaesser, alle gewollt (siehe N2).

## Runde O3 (Stand 01.11.)
- Schnee-Kaestchen: Ursache NICHT Eckfarben (VC weich, hf-Mittel 1,41) [S], sondern Detail-Bump dFdx/dFdy + 1,7-m-Kachel [A, per ?nobump=1 bestaetigt]. Fix: Kachel 5,1 m, Bump auf flachen Flaechen 0,22 statt 0,6. Angesehen an 6 Kameras (fluss_7/9, gipfel_3, krater_1, rampe_4, rand_2): Kaestchen weg.
- Saegezaehne Ufer fluss_9/fluss_7: NICHT behoben. Feinband-Glaettung wirkungslos (Ufer liegt im Grobnetz) [S]; Spiegel-Glaettung verkleinert Zaehne, erzeugt aber Bergauf-Fluss (31) bzw. ist zu invasiv -> verworfen. Alpha-Rand (Tiefe) ohne sichtbare Wirkung.
- fluss_7 heller Keil / Treppenschatten und wand_0_24 Sandstreifen: nicht behoben, nicht neu untersucht.
- Endmessung: Spalt 0, t42u 0, Raycast 0/0/0 alle Typen, Budget 1 047 817 Dreiecke; Fehlerzaehler: spitzen 7, senken_0_8m 5, enge_grate 259, wasser_ohne_randweg 5484, sonst 0.

## Runde O4 Schritt A (fluss_7, Ebenen-Schalter, Bilder /workspace/t65/o4a)
- base, noramp, noov, nobump, nosh: Platten + Zahnreihen unveraendert sichtbar (angesehen).
- nowa (Wasser aus): Platten, mittlere Zahnreihe, Treppenschatten, Zickzackband WEG, Boden glatt (angesehen) -> Ursache = Wassernetz [S].
- clay: kein Wasser, Boden-Form hat nur leichte Kerben oben (angesehen).
- Zusatz [S]: Renderer mit H=640 laeuft im Handy-LOD (1-m-Boden), Wasser im 0,5-m-Raster. WV wird in gen auf mind. G+0,05 gesetzt -> duenner Wasserfilm in Zellform ueber Schnee.

## Runde O4 Schritt B Versuch 1 (Bilder /workspace/t65/o4m, angesehen)
- Wasser-Alpha erst ab 7 cm Tiefe (statt -3 cm): fluss_7 NICHT besser (Platten/Zaehne bleiben, Sand liegt frei mit blauen Kanten), fluss_9 Treppen links unveraendert. Zurueckgenommen.
- Schluss [A]: Die Kanten kommen nicht vom Alpha-Schwellwert, sondern von der Wassernetz-Geometrie (Vertex-Hoehen/Dreiecke im 0,5-m-Raster ueber 1-m-Boden). Naechster Weg: Tiefenmaske je Pixel im Shader (Bodenhoehe als Textur) - noch nicht gebaut.

## Runde O4 F1/F2 (Stand nach diesem Commit)
- F1: Schalter ?lod=0 erzwingt Desktop-Netz. Headless-Lauf (W=1024 H=640, Wartezeit 600 s) laedt NICHT fertig (Timeout, kein Bild /workspace/t65/o4n). Desktop-LOD daher NICHT geprueft [S].
- F2: Tiefenmaske je Pixel im Wasser-Shader (Bodenhoehe GL als Float-Textur, bilinear per texelFetch, alpha*=smoothstep(0,0.35,Tiefe+Noise)), Eckhoehen unveraendert. Bilder /workspace/t65/o4o fluss_7_o, fluss_9_o angesehen: Zaehne, Platten und Treppen links bei fluss_9 praktisch UNVERAENDERT -> wirkt nicht.
- Vermutung [A]: der sichtbare Boden ist das Feinnetz fwMesh (eigene Hoehen fh), nicht G/GL; die Maske misst gegen die falsche Bodenhoehe. Naechster Versuch: Bodentextur aus fwMesh-Hoehen bauen.

## Runde O5 Schritt 1: weiche Wasserkante aus Szenentiefe (Schalter ?softwater=0 aus)
- Tiefenpass: Szene ohne Wassernetz mit colorWrite=false in WebGLRenderTarget+DepthTexture (Handy/lod=1: halbe Aufloesung). Wasser-Shader: Bodenpunkt entlang Sehstrahl, senkrechte Tiefe, alpha=smoothstep(0,0.30,Tiefe), Uferaufhellung nahe 0.
- Kosten [A]: ein zusaetzlicher Geometrie-Durchlauf (Dreiecke pro Bild etwa x2 im Vertex-Teil, Fragment billig). Budget-Skript nicht gelaufen.
- Bilder /workspace/t65/o5b fluss_7_b, fluss_9_b (Handy-LOD, 640 px) angesehen: Zaehne, Platten, Treppen UNVERAENDERT -> wirkt nicht.
- Offen [A]: nicht geprueft, ob der Shader-Zweig ueberhaupt greift (kein Debug-Bild). Moeglich auch: die Zaehne sind nicht die Alpha-Kante, sondern andere Teile der Ebene 'wasser' (z. B. ALT-Wassergruppe Zeile 89 oder Uferschaum-Vertexfarbe). Naechster billiger Test: Debug-Farbe Tiefe=rot.
- softwater=0 vs Standard und lod=1 vs Standard nicht gerendert (keine Wirkung, Zeit gespart).

## Runde O5 Diagnose D1/D2
- D1 [S]: Ebene 'wasser' hat nur 2 Gruppen: ALT-Wasser (main.js ~Z.93, nur im Modus 'alt' sichtbar, hier unsichtbar) und das NEU-Wassernetz wmesh (~Z.201). Kein eigener Uferschaum/Eis/Flussband-Mesh (Schaum = Vertexfarbe in wmesh). Neuer Schalter ?hide=winnen,wrand teilt wmesh: winnen = Zellen mit 4 nassen Ecken, wrand = Randzellen.
- D2 [S] Bilder /workspace/t65/o5c_wrand/fluss_7_wrand.png und o5c_winnen/fluss_7_winnen.png angesehen:
  - hide=wrand: Zaehne, Platten, Mittelstreifen bleiben (nur Randsaum fehlt, dafuer kleine Stufen links).
  - hide=winnen: Zaehne, blaue Platten, Mittelstreifen WEG; Boden glatt, nur kleine Randsaum-Kerben links unten.
  -> Ursache = INNERE Wasserzellen von wmesh, nicht der Rand.
- Vermutung D3 [A]: innere Zellen mit Spiegel nur knapp ueber Boden (gen setzt WV>=G+0,05) und Spiegelstufen zwischen See/Fluss (WR-Klemme WV-0,25..+0,1 erhaelt die Stufen). Shader-Masken (880fa1d, a265266) aenderten nichts -> ungeprueft, ob der Patch greift.
- D4 teilweise: Szenentiefen-Pass jetzt standardmaessig AUS (?softwater=1 an), kein Zusatzpass mehr. Pixel-Tiefenmaske aus 880fa1d noch drin (billig, aber ohne Wirkung).

## Runde O5 D3 Test 1 (Bild /workspace/t65/o5d/fluss_7_d.png angesehen)
- Nur Darstellung: Spiegelglaettung 16 statt 8 Durchgaenge, Klemme WV-0,6..+0,3 statt -0,25..+0,1.
- Ergebnis: blaue Platten/Mittelstreifen deutlich weicher (Kanten verschwimmen), Zahnreihen oben und mitte-links UNVERAENDERT. Nicht sauber.
- Risiko [A]: Darstellungs-Spiegel kann lokal bis 0,3 m ueber/0,6 m unter Datenwert liegen; Bergauf-Pruefung des Darstellungsspiegels nicht gemacht (Daten unveraendert, Laengsprofil unberuehrt).

## Runde O5 E1 Versuch 1 (Bilder /workspace/t65/o5e fluss_7_e, fluss_9_e angesehen)
- Darstellung: nasse Ecken mit Tiefe <0,12 m weich (smoothstep, 2x Gauss) bis Boden-0,15 m abgesenkt.
- fluss_7: Platten fast weg, Zahnreihen oben und Mitte-links bleiben. fluss_9: Treppen links/rechts bleiben. Nicht sauber.
- Spiegel-Bergauf-Zahl (/workspace/t65/spiegel_bergauf_o5.py, Nachbarpaare deren Darstellungs-Gefaelle dem Daten-Gefaelle widerspricht, >1 cm): WR 428 Paare (max 0,09 m); WD sichtbarer Teil (ueber Boden) 859 Paare (max 0,10 m). Kein Paar >0,10 m im sichtbaren Wasser [S].

## Runde O5 E1 Versuch 2 (Bilder /workspace/t65/o5f fluss_7_f, fluss_9_f angesehen)
- Handy-LOD: Wasserhoehen der ungeraden Ecken wie Boden aus geraden Ecken interpoliert (gleiche 1-m-Ebenen).
- Ergebnis: praktisch gleich wie Versuch 1. Zaehne fluss_7 oben/Mitte-links und Treppen fluss_9 bleiben. NICHT SAUBER nach zwei Versuchen -> laut Auftrag dokumentiert, weiter mit E2/E3.
- V2 nur noch mit ?wlod=1 aktiv (ohne Wirkung).

## Runde O5 E2
- Tiefenmaske/Hoehentextur aus 880fa1d entfernt, alte Alpha-Maske (vWM) wieder aktiv. softwater-Pass standardmaessig aus (?softwater=1). E1 V1 (Absenken flacher Ecken) bleibt, weil Platten sichtbar weicher.

## Runde O5 E3 (Endmessung trotz nicht sauberer Ufer)
- Bilder /workspace/t65/o5g wand_0_24_g, rampe_4_g, rampe_13_g, fluss_3_g angesehen; Befunde in ABWEICHUNGEN.md.
- [S] Spalt 0, t42u Summe 0, bergauf_pfad_summe 0, Raycast (W=1024 H=640 NOUI=1, bereit nach 332 s): alle Klassen 0 schwebend/0 versunken/0 im Wasser, Handy-Budget 1 047 817 Dreiecke.

## O6 G1 – Wassernetz geometrisch an Tiefe=0 clippen
- Umgesetzt [A]: Marching-Triangles je Wasserdreieck, Schnittpunkte exakt auf Boden (Höhe = Spiegel − Tiefe, linear auf Kante). Schalter `?clip=1` (Standard aus).
- Gesehen [S]: o6a/fluss_7_a.png, o6a/fluss_9_a.png. Zähne am linken Ufer fluss_7 und Stufen fluss_9 **bleiben**. Zusätzlich harte hellblaue Platten (fluss_7 rechts unten) – schlechter als O5.
- Folgerung [A]: Die Zähne sitzen nicht in der Wasser-Schnittlinie; vermutlich Boden/Schnee-Grenze im Grobnetz (gleiches Muster wie G4). Deshalb Clip nur als Schalter, Standard unverändert O5.

## O5b Ladehänger (Brave/IE „Lade Welt …“)
- Ursache: seit e30690b (O8b) Rampenhöhen per Raycaster gegen das komplette Bodennetz (Millionen Dreiecke, ohne Beschleunigung), seit O9 S4 3x dichter. Blockiert den Hauptthread minutenlang (headless: >5 min statt 4 s). Kein JS-Fehler, kein fehlender Download.
- Fix: gleiche Höhe (höchster Treffer von oben) über Raster-Buckets (2 m), Ladezeit headless 4,3 s. Abweichung Rampe zu Strahl-Boden 0,00 m (Messung chk.js).
- Robust: Ladestufen im Ladebildschirm, Fehler/unhandled rejections sichtbar, Hinweis nach 60 s, WebGL-/DecompressionStream-Prüfung, Tiefentextur nur mit ?softwater=1.

## O7 I1–I5 (01.11.)
- I1/I2 erledigt (ee77b88). I3: t42u 0, bergauf 0, Spalt wie Basis, Raycast 1 Baum/7 Steine schwebend, 0 im Wasser, 1,137 M, 8,2 s. Nicht gemessen: Fehlerzaehler (braucht FW_NPZ), Rampen/Bruecken am Wasser einzeln.
- I4 angesehen: 29 Fluss-/Randkameras (Textur), 37 von 40 Stichproben-Kameras nur Textur (Render-Lauf brach ab, Clay fehlt). Endsee/Tuempel West keine eigene Kamera.
- Mangelliste: fluss_7 Achsen-Stufen im Wasser; fluss_4 dunkle eckige Wasserflaeche; rand_ost_80 duenne dunkle Linie am Hang; rand_ost_265 punktierte Linie im Hang; wand_264_24 Saegezahn-Kante; wand_288_144 Keile; nicht beurteilbar (Kamera in Baeumen): fluss_8, rand_8, rand_9, rand_ost_283.

## O8 J1 (01.11.)
- Spalt 0,28 m (6 Kanten, 108|46, LS1) war KEINE Regression durch ufer_profil: gleich bei 5c1c575 und e3e67ad nachgeneriert [S]. Fruehere "Spalt 0" bezogen sich offenbar auf LS2 bzw. aeltere Daten [A].
- Ursache: G_ANZ wird nach dem Feinband-Export (FW) noch geaendert (u. a. Einzelzahn 105|47) -> Feinband-Randpunkt 108,5|46 6,32 m vs Grobnetz 5,73 m.
- Fix: gen_relief.py `_bandnaht_j1` setzt Feinband-Randpunkte auf das Grobnetz (17 839 Randpunkte, 3 geaendert, max 0,59 m). Aus mit NAHT_ALT=1.
- Objekthoehen neu per Raycast aufgenommen (2 867), neu generiert: schwebend 0/0/0/0/0 (vorher 1 Baum 320,4|278,0 + 7 Steine) [S].
- Spalt LS1 0, LS2 0; t42u 0; bergauf_pfad 0.

## O8 J2 (01.11.)
- gen_relief.py `bett_glatt` (aus mit BETT_ALT=1): Bett-Tiefe im Wasser = Gauss 2,5 m ueber nasse Ecken, min 5 cm, Ufer-smoothstep bleibt, Aenderung max 0,5 m. 20 471 Ecken, max +0,46/-0,45 m. Nasse Ecken mit Tiefe <0 bzw. <5 cm: vorher 0, nachher 0 (die "negativen Tiefen" aus O7 waren Viewer-Werte __hSurf vs WE, nicht Daten) [S].
- WV unveraendert; Spalt 0/0, t42u 0, bergauf_pfad 0.
- fluss_7 vorher/nachher (pruefung/o8/f7_vn.png): praktisch gleich, Stufen bleiben. Clay (f7_cl.png) zeigt: die Stufen sind der Umriss der nassen Zellen (Treppen-Kontur der Wassermaske), nicht das Bett [S]. Mit Zellwerten unveraendert nicht weiter loesbar ohne Wasser-/Ufer-Darstellung ueber die Zellmaske hinaus. 2. Versuch -> dokumentiert, weiter.

## O8 J3 (Defektliste, Kameras)
- fluss_4: dunkle eckige Flaeche nach J2 weicher; Rest = Tiefenfarbe des Wassers, keine Geometriekante (clay glatt). OK.
- rand_ost_80 / rand_ost_265 / wand_264_24: duenne gepunktete Linien sichtbar, auch im Clay. Hoehen dort stetig (Bandrand ~x 326, Spalt 0). Versuch 1: Schuerzen-Normalen vom Quellvertex -> keine Aenderung. Versuch 2: Schuerze 0,08 statt 0,35 m -> keine Aenderung. Beide zurueckgenommen. OFFEN, Ursache unbekannt.
- wand_264_24 Saegezahn: nicht mehr deutlich sichtbar. wand_288_144: Keile am Wandfuss weiterhin sichtbar (clay). OFFEN, nicht angefasst (keine Versuche mehr im Budget).
- Kameras fluss_8/rand_8/rand_9/rand_ost_283 versetzt (_neu): nicht mehr im Baum. rand_8_neu/rand_9_neu zeigen im Clay den Kartenrand/Aussenflaeche.
- Neu: tuempel_west (gut), see_senke (Blick durch Daecher verdeckt, Kamera ungeschickt), see_mitte (Kratersee gut, im Clay feine Zackenlinien am unteren Bildrand).
Bilder: pruefung/o8/o8j3_s*.png, o8j3c.png

## O8 J4
- 40 Stichproben im Clay gerendert (pruefung/o8/o8s_0..2.png). Gelaende meist glatt. Auffaellig: wand_48_168 feine waagrechte Rillen (Terrassenstreifen), Haarlinien wie J3 bei wand_264_24. Keine Loecher, keine Zacken-Ausreisser.
- Fehlerzaehler (FW_NPZ): pruefung/fehler_o8.json – spitzen 7, nadeln 0, senken_0_8m 5, senken_2m 0, enge_grate 259, stufe_bandrand 0, Objekte auf Wegen 0, flussenden_blind 0.
- Rampen am Wasser (90 Punkte): dy -0,02 m, liegen auf. Bruecken (20 Zellen): Deck 0,31-0,51 m ueber Boden (Soll +0,3), keine ueber nassen Vertices.
- Raycast nach J2 erneut: schwebend 0/0/0/0/0.

## O8 J5 Endmessung
Spalt LS1/LS2 0/0; t42u summe 0; Laengsprofil bergauf_pfad 0, Stufen >1 m ausserhalb Schlucht 0; Raycast schwebend 0; index.html 15,5 MB, relief_daten 8,0 MB. Ladezeit nicht neu gemessen.

# Runde O9
## K0 Ladezeit
/workspace/dorfmap_3d_runde_O8.html, headless Chromium (SwiftShader), 1280x800, bis __test.bereit: 7,71 / 8,28 / 7,95 s, Median 7,95 s (< 10 s). Skript: test_ladezeit.js

## K1 Wasserkontur glätten
- gen_relief.py: `kontur_glatt` (Gauss SIG 4 auf Nassmaske, nur ruhiges Wasser 9x9-Spiegelspanne <0,1 m, Entfernungen die Gewässer teilen werden zurückgenommen). Gilt für alle Flüsse. Zellwerte unverändert, nur Anzeige-Spalten. Abschaltbar mit KONTUR_ALT=1.
- Ergebnis: +77 / −243 Ecken, kein Gewässer geteilt, Randabfluss erhalten (Randecken 95→93), Spalt 0, t42u 0, Stufen >1 m ausserhalb Schlucht 0, bergauf_pfad 1 (vorher 0, eine Ecke >2 cm, dokumentiert).
- Ehrlich: Sichtbarer Effekt in fluss_7/3/9/4 minimal (t65/k1_vn3.png). Die Treppe bei fluss_7 kommt vor allem vom zellbasierten Sand-/Uferband der Textur (gen_textur), nicht von der Wassermaske. Breitere Glättung (ohne Ruhig-Filter) erzeugte bergauf_pfad 14–18 → verworfen. Nach 2 Ansätzen dokumentiert, offen: Texturband an geglättete Kontur binden.

## K1b Uferfarbe an Kontur, Aufwärtspunkt, Wasserkörper
- Uferband (dunkler Saum, Kies, Flussgrund) aus geglättetem Ecken-Nassfeld (Gauss 0,6 m der finalen Wasserkontur) statt Zellmaske (`ufer_farbe`, abschaltbar UFERFARBE_ALT=1).
- Aufwärtspunkt geklärt: Stück 2, Nordrand (Ecke 25/429, +3,5 cm). Ursache: K1 nahm die Rinnen-Ecken der 13,40-m-Auslassspalte weg, der Pfad lief dann über 13,44. Fix: Ecken tiefer als ein nasser Nachbar (>2 cm) werden nicht weggenommen → bergauf_pfad 0.
- 18→19 geklärt: kein Tümpel, eine einzelne zugefügte Ecke (Zelle ~x325,y272) ohne Altwasser-Anschluss. Fix: solche Einzelstücke verworfen → 18→18.
- Neu: zu 76 / weg 229, Randecken 95→93, Spalt 0, t42u 0, Stufen >1 m ausserhalb Schlucht 0, bergauf_pfad 0. zellen_relief.csv nur Anzeigespalten geändert.
- Angesehen (t65/k1b_vn.png, k1b/tuempel_west_n.png): Uferfarbe minimal weicher. Die eckige Kante bei fluss_7 bleibt: Clay zeigt, dass sie Geometrie ist (Bett-/Uferterrassen aus ufer_profil, zellgebunden), nicht Farbe. Nicht behoben (2 Ansätze verbraucht). Wasser auf Land: im Textur-Render nicht gesehen; Tümpel West zeigt vorne eine leicht pixelige Wasserkante (0,5-m-Ecken-Alpha).

## K2 Ostrand-Haarlinien (rand_ost_80, rand_ost_265, wand_264_24) – NICHT behoben
- Neu: Diagnose `?dbgmat=farbe|nrm|wire` (rot Grobnetz, grün Feinband, blau Overlay), dazu ?hide=wrand,winnen, ?noov=1, ?nowa=1, ?lod=0 angesehen (t65/k2, k2d, k2_sheet.png).
- Befund: Linien sind dunkle, gepunktete Pixelreihen (Rasterfunken), sowohl genau auf der Grenze Feinband/Grobnetz als auch im Innern des Feinbands entlang von Rücken. Auch mit Normalen-Material und bei lod 0/1 und 2 sichtbar, nicht mit Overlay/Wasser/Schatten des Feinbands verbunden; im einfarbigen Doppelseiten-Material nicht sichtbar. Ohne Schürze werden die Grenzlinien schwächer, die Innenlinien bleiben.
- Versuche (alle ohne sichtbare Wirkung, zurückgenommen): (1) Schürzen-Ecken erben Normale der Oberkante, (2) waagrechter Kragen 0,3 m unter das Grobnetz, (3) 1-m-Rissfüller unter Feinband (stach durch, schwarz). Nach 3 Versuchen dokumentiert. Vermutung: T-Stöße/Faltdreiecke im Feinband selbst; nächster Schritt wäre eine Kantenzählung je Feinband-Dreieck (offene Kanten innen, Rückseiten-Dreiecke).

## O9 K3 (Keile/Rillen/Endsee-Rand)
- wand_288_144: Feinhoehen geprueft. Keine 1-Ecken-Kerbe; die "Keile" sind eine echte ~1 m breite Rinne plus scharfe Schattenkante am Feinbandrand (Band endet bei x~301 auf 12,0 m). Neu `keile_fein` (1-Ecken-breite Kerben/Grate >0,6 m auf 40 %): 111 Ecken kartenweit, an wand_288_144 keine Aenderung, Render vorher/nachher gleich. NICHT behoben.
- wand_48_168 Rillen: in Clay feine waagrechte Streifen, wahrscheinlich Felsschicht-Terrassen (gewollt, `_lk`). Nicht veraendert, NICHT behoben (2 Versuche-Regel: 1 Versuch, dann nach Abwaegung belassen).
- Endsee-Rand: angesehen (Clay+Textur), natuerlich, nur kleine Kerben, kein Geometriefehler -> unveraendert.
## O9 K4 Durchgang
- Kamera see_senke neu: [22,6,104] -> [34.4,-8.8,116.5] (vorher hinter Dach), pruefung/o8/cams_o8_j3.json.
- Fehlerzaehler pruefung/fehler_o9.json: spitzen 6 (O8: 7), nadeln 0, senken>0,8m 4 (5), >2m 0, enge_grate 259, stufe_bandrand 0, Objekte auf Wegen 0, flussenden_blind 0.
- t42u summe 0; Spalt 0,0 m; bergauf_pfad 0 (bergauf_summe 3922); Raycast schwebend 0/0/0/0/0 (Punktliste neu, alte hatte 574 statt 567 Steine); Budget summe 1,138 M (gerendert lod1 1,376 M); Ladezeit median 8,2 s (8,8/7,8/8,2).
- Export /workspace/dorfmap_3d_runde_O9.html.
- Offen: K2 Haarlinien Ostrand, fluss_7 Eckigkeit (Ufer-Terrassen), wand_288_144 Schattenkeil, wand_48_168 Rillen.

## O10 L1 Dreiecksbudget
- Gemessen per WebGL-Hook (test_gl_l1.js, lod=1, 390x844, Ansicht schraeg), 1 Frame: vorher Bildpass 1.375.862 Dreiecke. Ursache des Unterschieds zu 1,138 M: Wasser (222.218) und 2 kleine Meshes (16.392 Wege-Wasser/Overlay) sind transparent+DoubleSide -> three.js zeichnet sie zweimal (Rueckseite, dann Vorderseite). Baeume/Steine/Schuerzen/Overlay sind NICHT die Ursache.
- Fix: forceSinglePass:true an den 3 transparenten DoubleSide-Materialien. Nachher Bildpass 1.137.252 (< 1,3 M). Wasser-Render vorher/nachher (endsee_rand, fluss_7) optisch gleich.
- Ehrlich dazu: der Wassertiefen-Pass (Rendertarget, halbe Aufloesung) zeichnet zusaetzlich 792.424 Dreiecke je Frame; die GPU verarbeitet also ~1,93 M Dreiecke/Frame. renderer.info zeigt nur den letzten Pass (Bild). Schatten: kein Einfluss (Zahl mit nosh=1 gleich).

## O10 L2 Haarlinien Ostrand
- Kantenzaehlung (test_kanten_l2.js, je Gelaende-Mesh, Positionen auf 1 mm verschweisst): Feinband 181.332 Dreiecke, 0 doppelte, 0 entartete, 0 Rueckseiten (n.y<0), 9 Kanten mit >2 Nutzern, 8.932 offene Kanten (Bandrand/Schuerze), 2.144 Faltkanten (Nachbarnormalen dot<-0,2). Davon 1.747 Schuerze/Flaeche (gewollt senkrecht) und 397 echte Faltdreiecke (Messergrate 1 Ecke breit).
- Fix 1 gen_relief `messergrate_fein` (1-Ecken-Grate/-Kerben >0,3 m, auch diagonal, halbe Hoehe zum Nachbarmittel, 6.277 Ecken): echte Falten 397 -> 158, an rand_ost_80 3 -> 0. Haarlinien danach noch sichtbar -> nicht die Hauptursache.
- Ursache: Tiefen-Konkurrenz an der Naht Feinband/Grobnetz (Feinband-Rand und Schuerze liegen fast tiefengleich auf dem Grobnetz, einzelne Pixel der dunklen Schuerze/Kante gewinnen). Gegenprobe: polygonOffset -1/-2 (Feinband nach vorn) -> Linien deutlich STAERKER.
- Fix 2 main.js: matF.polygonOffset +1/+2 (Feinband minimal nach hinten): Linien an rand_ost_80, rand_ost_265, wand_264_24 im Textur-Render weg (/workspace/t65/l2q.png). Gegenkontrolle fluss_4, wand_288_144, wand_48_168 ohne neue Fehler (/workspace/t65/l2c.png).

## O10 L3 fluss_7 Eckigkeit
- ufer_profil: Abstaende si/so jetzt aus geglaettetem signiertem Distanzfeld (Versuch 1 Gauss 1,5 Ecken, Versuch 2 Gauss 4 Ecken = 2 m; Stand: 4). bett_ecken 8.595 -> 13.252, land_ecken 2.643 -> 3.005. bergauf_pfad 0, bergauf_summe 3922 unveraendert.
- Render fluss_7 Clay+Textur vorher/nachher (/workspace/t65/l3s.png, l3t.png): KEIN sichtbarer Unterschied. Die eckige Form liegt also nicht im Uferprofil (fluss_7 ist nicht im Feinband). Wahrscheinlich Bettform aus G/Anzeige-Netz bzw. Wasserkoerper-Rand selbst. Nach 2 Versuchen: NICHT behoben, dokumentiert.

## O10 Aufraeumen (02.11.)
Uncommittet vorgefunden: L4-Versuch halbfertig (gen_relief.py breite=16, Daten aus breite=8-Testlauf). Komplett zurueckgenommen.

## O10 L3b fluss_7 Eckigkeit – NICHT behoben (2 Versuche)
Eingrenzung (Bilder /workspace/t65/l3b, l3c.png, l3e.png): Clay mit/ohne Wasser rund; Textur ohne Wasser (?nowa=1) rund; ?hide=winnen,wrand unveraendert eckig -> Ursache ist das Wassermesh (wmesh). Wireframe (?wwire=1, neu) zeigt eckige Wasserflaeche.
Versuch 1/2: fortgesetzten Spiegel ausserhalb 1 m bzw. 0,5 m mit 0,25 bzw. 1,0 m/m absenken -> optisch unveraendert (nur Rauschen). Reichweitengrenze ist es also nicht. Zurueckgenommen.
Vermutung (ungeprueft): Wasserfarbe/Alpha kippt ueber nur 0..0,375 m Tiefe (col(): e=1-min(1,t*4)); kleine Zellstufen im Grobnetz-Bett, im Clay unsichtbar, werden so als eckige Farbkante sichtbar. Naechster Schritt: Farbrampe ueber Tiefe breiter bzw. Tiefe vor der Farbe glaetten.

## O10 L4 wand_288_144 Feinbandrand – NICHT behoben (2 Versuche)
bandrand_weich breite 16: Kerbe weg, Schattenkante weicher, aber Raycast 81 schwebende Objekte (19 Baeume, 61 Geroell). breite 12: 27 schwebend. Basis breite 8: 1. Beides verworfen (Objekte werden offenbar vor dem Bandrand-Ausgleich platziert).

## O10 L5 Durchgang (Stand dieses Commits)
t42u 0 | Spalt 0,0 m | bergauf_pfad 0 (summe 3922) | Raycast 1 Baum (325.8/280.8, 0,32 m), sonst 0 | Fehlerzaehler: spitzen 4, nadeln 0, senken>0,8 m 3, >2 m 0, enge_grate 249, stufe_bandrand 20, Objekte auf Wegen 0 | Budget lod1 Bildpass 1,133 M (+ Tiefenpass FBO 0,793 M), test_budget 1,134 M | Ladezeit Median 7,96 s.
Hinweis: stufe_bandrand 20 und 1 schwebender Baum waren in O9 0/0 – kommt aus L2/L3 (messergrate/Uferprofil), nicht untersucht.

## O11 M2 Determinismus
Ursache: relief_daten.json.gz trug den gzip-Zeitstempel (Inhalt war bei jedem Lauf gleich, zcat-md5 identisch). Fix mtime=0. Zwei Laeufe: alle Daten-/pruefung-JSON identisch, index.html identisch. Alle Zufallsquellen sind geseedet.

## O11 M1 Regressionen
Bisect (Worktrees, gleicher Ablauf): 543a49e/6dbe706 stufe_bandrand 0, Raycast 0; 1ee1d59 (L2 messergrate_fein) stufe_bandrand 20; e6e4cd7 (L3 Uferprofil) zusaetzlich 1 Baum schwebend.
Fix: messergrate_fein laesst 2 Ecken am Bandrand aus (6175 statt 6277 Ecken). Baum: Objekthoehen kommen aus dem Raycast-Cache pruefung/strahl_hoehe_t65u.json, der nach Gelaendeaenderungen veraltet. Neues Werkzeug pruefung/strahl_cache_auffrischen.py (Ablauf: gen, html, Raycast, auffrischen, gen, html, Raycast).
Ergebnis: stufe_bandrand 0, Raycast 0/0/0/0/0, Spalt 0, t42u 0, bergauf_pfad 0. 3. Lauf identisch (Fixpunkt).

## O11 M3 Wasserfarbe (nur Farbe/Alpha, Geometrie/Raycast unveraendert)
Bilder /workspace/t65/m3 (vt/vc vorher, nt Versuch 1, n2/n2c Versuch 2), Uebersicht /workspace/t65/m3b.png.
Versuch 1: Rampe smoothstep 0..1,2 m + Farbtiefe geglaettet + Rand-Alpha 0..0,35 m -> Ecken weicher, aber alle Gewaesser grau/blass (Endsee, fluss_3). Verworfen.
Versuch 2 (behalten): Farbtiefe geglaettet (Mittel aus +-0,75/1,5 m), Rampe (1-u)^2 ueber 0..0,75 m, Rand-Alpha smoothstep 0..0,35 m. Farbe nahe vorher, etwas matter. fluss_7: Ecken weicher, als hellere Kante aber noch sichtbar -> TEILWEISE. Clay an allen 6 Stellen pixelgleich. ?wfarbe=alt zeigt vorher.

## O11 M4 – bandrand_weich breite 12 + Objekte aus aufgefrischtem Cache
- breite 12 (env BANDRAND_B, Default 12), Kette gen→html→Raycast→Cache auffrischen (281 Bäume, 6 Felsen, 16 Findlinge, 5 Steine, 493 Geröll neu)→gen→Raycast.
- Vor Auffrischen: 11 Bäume/1 Fels/1 Findling/13 Geröll schwebend; danach Raycast 0.
- stufe_bandrand 0, Spalt 0, t42u summe 0, bergauf_pfad 0, Determinismus 2× gleicher Hash.
- Fehlerzähler: spitzen 4, senken>0.8 m 1, enge_grate 256 (vorher 249).
- wand_288_144: Wandfuß leicht weicher, Wand bleibt steil – Verbesserung gering.

## O11 M5 – Durchgang (Stand b4d884f, Daten unverändert seit M4-Lauf)
- t42u summe 0, Spalt 0.0, bergauf_pfad 0, Raycast 0 schwebend, stufe_bandrand 0, Determinismus ok (Werte aus M4-Kette auf identischem Build).
- Fehlerzähler: spitzen 4, senken>0.8 m 1, enge_grate 256.
- Budget lod1: Bildpass 1.134 M (<1.3 M), FBO 0.793 M. Ladezeit Median 8.92 s (8.92/9.28/8.89).
- 25 Kameras × Clay+Textur = 50 Bilder (/workspace/t65/m5), alle angesehen (als Kontaktbögen 2 Bilder/Zeile).
  Ostrand/Wände (8): rand_ost_80, rand_ost_265, wand_264_24, wand_288_144, wand_288_72, wand_312_168, wand_312_216, aus_ost_aussen – keine Löcher/Schweber; wand_288_144 Wandfuß weiterhin steil; aus_ost_aussen zeigt Schichten-Schürze (gewollt).
  Wasser: fluss_3/9/4 ok; fluss_7 hellere eckige Uferkante noch sichtbar; Endsee ok; Tümpel West helle Flecken auf Wasser (Spiegelung/Schneeflächen?) – offen.
  Sonst ok: gipfel_0, klippe_a, rampe_3, rand_2, waldrand_a, see_fluss_naht, fluss_8_neu.
  Kamera-Probleme (keine Geländefehler): aus_ost_oben, baum_80_175, platz_Q1 Kamera steckt im Baum; krater_rand Kamera in/unter Gelände (Bild leer).
- Export /workspace/dorfmap_3d_runde_O11.html (=index.html, 15.5 MB), headless geladen bis bereit (Ladezeittest).

## O12 N1 – Tümpel West helle Flecken
- Ursache NICHT M3: Flecken schon im Vorher-Bild (m3/tuempel_west_vt.png, ?wfarbe=alt-Stand) und auch mit ?nowa=1 (ohne Wasser, n1d/tuempel_west_nowa.png) identisch da.
- Es sind sonnenbeschienene Stellen des Gelände-/Schneebodens in der Lücke des Klippen-Schattens; die blockigen Ränder kommen von der Schattenkarten-Auflösung. Das Wasser ist dort flach und fast durchsichtig.
- Versuch 1: Alpha-Boden aus geglätteter Tiefe (≥0,35 m), keine sichtbare Änderung → zurückgenommen. Kein Code geändert.
- Offen: höhere Schattenkarten-Auflösung oder Wasser-Mindestdeckung bei flachem Wasser; beides ist ein größerer Eingriff mit Risiko für fluss_3/4/9 → nicht gemacht.

## O12 N2 – Kameras repariert (pruefung/nah_kameras_t65u.json), Bilder /workspace/t65/n2, alle einzeln in voller Größe angesehen
- aus_ost_oben → [318,12,268]: Osthang mit Wald und Haus, frei; Clay: Hang/Grat ok.
- baum_80_175 → [68,26,187]: Baumgruppe und Häuser von oben, frei; Clay: Hügel ok, feine Linien-Artefakte (bekannt).
- platz_Q1 → [26,4,292]: frei. Die Platzfläche ist eine untexturierte graue Platte (Platzhalter, Befund). Clay: glatt.
- krater_rand: erst [253,24,65], dann noch im Starthaus (16×16 m) → [253,40,50]: Dorf von oben, frei; Clay ok.
- rampe_4: In der Textur läuft ein unscharfes Weg-Band quer durchs Bild nahe der Kamera, im Clay nicht zu sehen → Weg-Overlay über der Kante, offen (nicht untersucht).
- rampe_13: Weg endet abrupt an der Kante, mit dunklem Rechteck am Ende → offen.
- Angesehen: 14 Bilder (6 Kameras × 2, plus krater_rand 2× nachgerendert).

## O12 N3 – fluss_7 helle eckige Kante (2 Versuche, beide zurückgenommen)
- Ohne Wasser (?nowa=1, n3/fluss_7_nowa.png) gibt es keine Ecke → die Kante kommt vom Wassermesh-Rand.
- Versuch 1: Shader-Alpha aus Szenentiefe weicher (0,30→0,75 m). Keine Wirkung, denn der Szenentiefen-Pfad ist aus (__swU.on=0, headless geprüft); es greift die Vertex-Alpha.
- Versuch 2: Vertex-Rand-Alpha über 0..0,75 m statt 0..0,35 m. fluss_7-Ecke etwas weicher, aber noch sichtbar; fluss_3 klar schlechter (flaches Wasser wird durchsichtig/bräunlich) → zurückgenommen.
- Offen: echte Abhilfe wären geglättete Randvertices bzw. ein feinerer Wasserrand (Mesh-Arbeit) oder der Szenentiefen-Pfad an; beides nicht klein.
- Angesehen voll: fluss_7 a/b/nowa, fluss_3/9/4, Endsee, Tümpel West (b).

## O12 N3b – fluss_7 Wasserrand geglättet (3 Versuche, alle zurückgenommen)
- V1 (af1f86e, Revert db051ac): Kontur und Rand-Alpha aus geglättetem Nassfeld (gewichtetes 3×3 im 0,5-m-Abstand, höchstens 15 cm über Rohtiefe). Das Mesh nutzt bereits Marching Triangles auf 0,25-m-Subzellen. fluss_7 und fluss_3 sehen fast gleich aus wie vorher → keine Wirkung.
- V2 (Radius 1,5 m, +30 cm): fluss_7-Ecke bleibt; rechts erscheinen braune Flecken/Löcher im Wasser → schlechter, verworfen.
- Diagnose ?wwire=1 (n3b/fluss_7_wire.png): Das Wassermesh deckt die ganze eckige Zone ab. Die helle Ecke ist **nicht** der Mesh-Rand, sondern liegt mitten im Wasser (gerade Kante bei ca. Bild-y 330, flache, durchsichtige Zone). Damit war die Annahme „Randvertices glätten“ falsch.
- V3: Rand-Alpha aus geglätteter Tiefe dc über 0..0,4 m → Bild unverändert, zurückgenommen.
- Ladezeit lag in allen Versuchen bei 7,5–7,9 s. main.js entspricht wieder b3eedd0.
- Offen / Vermutung [nicht geprüft]: Die Ecke stammt aus der Wasserhöhe WE (grobe Zellen, bilinear) bzw. einer Schatten-/Licht-Kante auf der Wasserfläche, nicht aus Kontur oder Alpha. Nächster sinnvoller Test: ?wfarbe=alt und Schatten aus nur auf dem Wasser.
- Angesehen voll: fluss_7 v1/v2/v3/wire, m5 fluss_7, n3 nowa, fluss_3 v1 + m5 fluss_3 = 8.

## O12 N4 – wand_288_144 Wandfuß: nur dokumentiert
- Stand unverändert seit O10 L4/O11: echte, ca. 1 m breite Rinne plus scharfe Schattenkante am Feinbandrand (das Band endet bei x≈301 auf 12,0 m). Wandfuß leicht weicher als in O9, die Wand bleibt steil. Kein Eingriff in O12.

## O12 N5 – Durchgang auf 2214266 (main.js = b3eedd0)
- spitzen 4, senken>0,8 m 1, enge_grate 256, stufe_bandrand 0; det-Hashes gleich; Raycast 0; Spalt 0,0; t42u 0; bergauf_pfad 0 (bergauf_summe 3922).
- Budget lod1: Bildpass 1,134 M, FBO-Pass 0,793 M. Ladezeit 7,88 / 7,53 / 7,62 s, Median 7,62 s.
- Export neu: /workspace/dorfmap_3d_runde_O12.html (04:38).
- O12 insgesamt einzeln in voller Größe angesehen: ca. 40 Bilder.
- Offen: fluss_7 Ecke (Ursache nicht Wasserrand, s. N3b), wand_288_144, Tümpel-West-Schattenlücken, rampe_4/13 (Wege-Bot).

## O13 P1 – Hypothese „Schatten auf der Wasserfläche“ (Bilder /workspace/t65/p1)
- fluss_7: Mit ?nosh=1 (alle Schatten aus) und mit „Wasser empfängt keine Schatten“ ist die helle eckige Kante unverändert da → **widerlegt**. Die Ursache ist kein Schatten (und laut N3b auch nicht der Mesh-Rand).
- Tümpel West: Mit ?nosh=1 sind die hellen Flecken weg; mit „Wasser ohne Schatten“ sind sie noch da → sie sind besonnter **Boden unter dem Wasser** in Lücken des Felsschattens (wie in N1), nicht Schatten auf dem Wasser.
- V1: normalBias 0,12→0,03 → Flecken unverändert, und das Wasser wird insgesamt dunkler. Zurückgenommen.
- V2: shadow.radius 1,6→4 → die Kanten der Flecken nur minimal weicher, Flecken und Treppenrand bleiben. Zurückgenommen.
- V3 nicht gemacht: Die Lücken sehen nach einem echten Schattenloch aus (vermutlich Werfer-Geometrie mit treppigem Umriss). Das lässt sich nicht mit Bias/Weichheit lösen. Nächster Schritt wäre: herausfinden, welches Mesh dort den Schatten wirft (Ebenen einzeln castShadow aus) [nicht geprüft].
- Nicht gelöst → kein Export O13. main.js = 0b843be.
- Angesehen voll: fluss_7 nosh/wnosh, tuempel_west nosh/wnosh/v1/v2 = 6.

## O14 (Stand 434686b + Doku)
- Q1 Naht: T-Stöße Feinband/Grobnetz (LS1 8826, LS2 4413) zugenäht (817e8f6); Spaltmessung 0 bei beiden LOD; Schürze standardmäßig aus (?schuerze=1 = alt). Kanten Feinnetz: Falten 1856→137, mehr2 9→0.
- Q1-Verifikation ohne Schürze: 9 Außen-/Randkameras (Nord 100/250, Süd 80/200, West 60/220, Ost 130, Ecken NW/SO) + aus_ost_aussen, Clay, o12 vs O14 LOD2 und O14 LOD0: Ränder/Wände identisch, kein Spalt sichtbar.
- Q2: keine Datenänderung nötig. „Schlitz“ x148–157,z25–32 ist der Einschnitt der rampe_12 selbst und liegt ganz unter dem Rampenband (BANDZ=1), wird nicht gerendert. Spitze (158,18): 13,5 m nur im Roh-G, Anzeige-GB=7,99 bereits glatt. CSV unverändert.
- Durchgang: det gleich, Raycast 0, Spalt 0,0, t42u 0, bergauf_pfad 0 (bergauf_summe 3922), stufe_bandrand 0, Budget lod1 1,127 M (fbo 786k), Ladezeit Median 7,3 s (Export 09:07: 8,5 s).
- Bilder: Haarlinien-Stellen vorher/nachher (t65/o14, Textur+Clay) und 10 Stichproben + Randansichten (t65/o14v). Haarlinien an Kreuzung rampe_2/12, Mittelgebirge, rand_ost_80/265 weg.
- Offen: feine dunkle Linien an Silhouetten-/Gratkanten (z. B. wand_288_72, wand_312_168) sowohl in O12 als auch O14 → nicht vom Band, Ursache ungeklärt. Schwacher Restpunkt-Strich auf dem Grat in r_kreuz (nrm) ungeklärt. Schluchtkante aus Fabians Screenshot = Kreuzung rampe_2/12.
- Export /workspace/dorfmap_3d_runde_O14.html, Banner „Ansicht: NEU (Relief t67u, Runde O14)“.

## O15 (Fabian t76u/t77u)
- Weg zerfranst (Zelle 153|26, Kreuzung rampe_2/12): Ursache Viewer – Rampen-Overlay mit Randalpha 0 (Schleier statt Kante), Loecher wo Hang >0,8 m quer (Alpha 0), bei Handy-LOD Grobnetz-Buckel ueber dem Band; Wege-Maske WEGA mit weichem Alpha aus Zellmaske (viele schwache Werte -> Wolken/Flecken).
  Fix (main.js, kartenweit alle Rampen + WEGA): Rampe QO ±1,08/0,88, Randalpha 0,3 statt 0, Loch-Schwelle 1,4 m; Handy-LOD: Band ueber Querbuckeln (max ±0,3 m) +QH*1,3. WEGA: Alpha-Schwelle smoothstep(0,22..0,52)*0,88, Hoehe +0,16 (Handy) / +0,05. Keine Zellwerte, keine Daten geaendert (det gleich).
  Vorher/nachher /workspace/t65/o15 (b1_oben_*_t / *_t2) und Ausschnitte zk2_neu.png, zh_vn.png: Kreuzung jetzt durchgehend mit klaren Raendern; Handy noch etwas weich.
- Schraege 133|173: ist der Ruecken, der rampe_9 traegt (Rampe (130,161)->(140,198), Zelle 133|173 liegt 0,4 m neben der Rampenmitte, Hoehe 11 -> ~7 m, Osten Abfall auf ~0-5 m). Entfernen = Rampe weg -> NICHT gemacht, Rueckfrage an Fabian.
- Durchgang: det gleich, Spalt 0, t42u 0, bergauf_pfad 0, Budget 1,127 M, Ladezeit 7,5 s. Raycast: 1 Baum (97.75,99.75) 0,36 m – auch mit O14-HTML reproduzierbar, also nicht durch O15 entstanden; offen.
- Kritischer Blick: 16 Handy-Kameras (13 Rampen + 3 WEGA) vorher/nachher /workspace/t65/o15k, nur als verkleinerte Raster angesehen + r3 voll; WEGA-Kameras schlecht gewaehlt (Haeuser/leer).
- Export /workspace/dorfmap_3d_runde_O15.html, Banner "Runde O15".

## Runde O16 (F t77u: rampe_9 + Ruecken 133|173 entfernen)
- Umsetzung nur Anzeige (runde_o16.py, spaet in gen_relief.py): G_ANZ/VC harmonisch gefuellt (Laplace) im Bereich um rampe_9 + Kasten x125,5–139,5 z153,5–195, weicher Uebergang 3 m; Feinband-Ecken dort auf Grobform; rampenwege[9] entfernt -> 13 Rampen. G, RAMPPROF, Zufallsfolgen unberuehrt.
- CSV gegen O15 (fddcdfd): nur Spalte boden_anzeige_m, 806 Zeilen. begehbar/bebaubar/untergrund/hindernis usw.: 0 Aenderungen. t42u 0.
- R1 Erreichbarkeit (CSV begehbar_3d, 4er-Nachbarn, |dh|<=0,6 und <=1,0 gleich): rampe_9 ist nicht der einzige Weg; Hauptkomponente 22669 -> 22595 Zellen ohne Rampenkorridor (151 Zellen). Ohne Rampe zusaetzlich 7 Flankenzellen abgeschnitten: (131,173-174) 7,3-7,5 m, (136,177) 5,9 m, (137-138,179-181) 4,7-5,3 m – liegen alle auf der abgetragenen Flanke; Kraterrand (132,162) bleibt erreichbar, keine Terrasse abgeschnitten. Achtung: CSV markiert den Korridor weiter als begehbar (Zellwerte bewusst nicht geaendert), Gelaende dort ist jetzt ein weicher Hang.
- Objekte: 17 Baeume/4 Felsen/1 Findling/1 Stein/140 Geroell auf Feinband abgesenkt (nur absenken), 41 Geroell der Rueckenflanke entfernt; Baum (97.75,99.75) behoben. Raycast: 0 schwebend.
- Durchgang: det gleich, Spalt 0, t42u 0, bergauf_pfad 0, stufe_bandrand 0, Objekte auf Wegen 0, lod1 Bild 1,125 M, Ladezeit Median 7,6 s.
- Fehlerzaehler misst jetzt den Endstand des Feinbands (vorher Zwischenstand vor Nachlauf): spitzen 5, senken_0_8m 19, enge_grate 258. Senken alle ausserhalb des Bereichs (FW ausserhalb identisch zu O15) -> Messaenderung, nicht neu. Im Bereich: 1 Spitze am Westrand (124,75|155,5), Grate am westlichen Kraterrand x~124 (vorhanden).
- Bilder /workspace/t65/o16: Stelle b2_schraeg/b2_oben vorher/nachher, Textur+Clay, Desktop 1400 + Handy lod=2 (16) + 5 Umgebung u1-u5 (Textur Desktop) = 21 Bilder, alle einzeln in voller Groesse angesehen. Nicht angesehen: Umgebung in Clay/Handy. Erster Stand hatte gerade Naht an der Kastenkante (Clay) -> O16b weicher Rand, neu gerendert.
- Rest-Befund: oestlich bleibt die vorhandene Rinne als laengliche Kante sichtbar; westlicher Fels hat eine steilere Ostflanke.
- Rampen-IDs: rampe_10..13 heissen jetzt rampe_9..12 (sicht_kameras zaehlt durch). Aeltere Eintraege oben nutzen die alten IDs.
- Export /workspace/dorfmap_3d_runde_O16.html, Banner "Runde O16".

## Runde O17 (02.11.) – Steinband zusammenhaengend, Blender-Paket
- Befund Zelle 8885 (cx149 cy26, SENKE/WAND_FUSS) auf Handy lod=2 mit Wege-Overlay aus: Das graue „Steinweg“-Band ist der Wandfuss-/Schutthang (30–45°). Die Geometrie ist glatt (Clay-Bild). In VC und FW-Farben gibt es kein Band. Mit dem Debug-Schalter st=0 (?sbdbg=1) verschwindet das Grau. Ursache: Das Fels- und Schneegewicht wurde pro Pixel aus der Normale des fein verrauschten Feinbands berechnet, dazu kamen Rauschen nzS (±0,15) und vFS-Schneeflecken. Die Hangneigung liegt genau im Uebergangsbereich, daher die Fetzen.
- Fix nur im Shader (Grobnetz und Feinband): Der VCT-Alphakanal traegt die geglaettete Neigung (zentrale Differenzen aus GB, 2× Box-Filter r=3, also ca. 1,5 m). Wo die geglaettete Neigung < 1,3–1,9 ist (Wandfuss/Schutt, kS bis 0,8), kommen Fels und Schnee aus dieser glatten Neigung. vFS-Flecken werden dort gedaempft. Echte Waende bleiben unveraendert. Vergleich mit ?steinband=alt (= O16). Keine Daten, Zellen oder Netze geaendert.
- Versuche: V1 (nur weniger Rauschen) ohne sichtbare Wirkung. V2/V3 (nur Grobnetz) mit kaum Wirkung und eckiger Grob/Fein-Kante, verworfen. V4 (beide Materialien) ist die aktuelle Fassung.
- Stellen (Handy 540x960, lod=2, Wege aus, alt|neu in /workspace/t65/o17/paar_*.png, alle einzeln angesehen): Hauptstelle a/b, s0 95/200, s3 307/223, s4 293/166, s5 171/239, s7 256/226 und s8 82/46 sind deutlich zusammenhaengender. s2 210/39 (harte waagrechte Kante oben) und s6 284/28 (Treppenkante unten links) sehen gleich aus, beide Kanten gab es schon vorher. s1 293/88 ist von Baeumen verdeckt, s9 162/186 ist Seeufer ohne Steinband, beide nicht aussagekraeftig. Nicht angesehen: Clay-Bilder v4 und b_vor_c.
- Durchgang: relief_daten/CSV/z25.glb md5 nach gen_relief-Neulauf gleich (det). t42u 0. Spalt 0,0. bergauf_pfad 0 (Summe 3922). stufe_bandrand 0 (spitzen 5, senken 19, grate 258, wie O16). Raycast: 0 schwebend, versunken Baum 1, Geroell 8, Stein im Wasser 1. Die Werte sind bytegleich mit dem O16-HTML (gleicher md5 der Auswertung), also nicht neu; der Cache wurde nicht aufgefrischt, weil die Geometrie unveraendert ist. Budget lod1 1,125 M. Ladezeit Median 11,15 s, das ist **ueber 10 s**. Allerdings lag die Box-Last bei 20, und O16 mass im selben Lauf 10,87 s. Der Unterschied liegt im Rauschen. Bei normaler Last bitte nachmessen.
- __test.dump() (nur lesend) fuer den Blender-Export. Neue Skripte pruefung/blender_dump_o17.js, blender_paket_o17.py, blender_test_render.py, README_Blender_O17.md.
- Export /workspace/dorfmap_3d_runde_O17.html (Banner "Runde O17"). Blender-Paket /workspace/dorfmap_blender_O17/.

## t82u – Feld-3D-HTMLs je Rasterfeld
- 56 Dateien dorfmap_3d_feld_A1…H7.html, Skripte relief3d/feld/ (README dort). Daten Commit 7a138db, Relief/gen_relief.py/relief_daten unverändert.
- Geometrie-Identität (Mesh-Dump gekürzt vs. ungekürzt, nur Ausschnitt): D1 29/29 gleich; A1, H7 nur Abweichung in zwei Wege-Meshes, die im Ausschnitt 0 Vertices haben (nicht gezeichnet). Vorherige Kürzung von WV hatte H7-Wasser verändert → WV/WEGA jetzt ungekürzt.
- Vergleichsbilder Feld vs. Hauptviewer (gleiche Kamera) D1, A1, H7 einzeln angesehen: im Feld deckungsgleich.

## Runde O18 (02.11.) – Wandfuss-Zacken, Fluesse, Wasser ohne Fluss
- runde_o18.py: wasser_raus, gelaende (Gipfel runden), feinband, fluss_tiefer (Bruecken weich), grob_wand_glatt, entstacheln.
- Messung Zacken (pruefung/o18/zacken_t83u.py) vor/nach: fein unten 1424->101, oben 272->60; grob sichtbar unten 312->65, oben 145->28. Grob-Steilquads >6: 190->117.
- Regression: t42u 0, Spalt 0 (4 Raender), bergauf_pfad 0, stufe_bandrand 0 (direkt), Raycast nach Cache 0 schwebend / max 1,1 m Findling, Budget lod1 1,13 M, Ladezeit 11,1 s (Median, gemessen waehrend 2 Render-Jobs liefen, daher nicht sauber).
- Export /workspace/dorfmap_3d_runde_O18.html; Felder /workspace/dorfmap_felder_3d (56 + reihe_1..7.zip).
- Offen: Feinband bis zum Wandfuss erweitern; Gelaende-Rundung ohne Band; Textur-Uebergaenge (Shadermasken A1/A2/B2/E1); G1-Block; Steinpfad D1/F1 (UEBERGABE.md); Kegel am Nordrand C2; F6-Restzacken.

## O18c – Abschluss (Commit-Basis 24c67ab)
- Neu: Shader-Masken weich (?maske=alt = O17), Grau-Angleich jetzt Grob+Fein (keine senkrechte Farbkante am Bandrand); gipfel_rund (grob, max 2 m) + fein_gipfel (max 1,5 m).
- Regression: t42u 0; Spalt 0 (alle Raender); bergauf_gt_2cm 0 (Wasser-Stufen >30 cm: 1304, max 2,72 m, Kaskaden); stufe_bandrand 0 (bandrand_t83u; fehlerzaehler_t67u meldet 1086, misst FW-Dump vor Naht – nicht vergleichbar); Raycast nach Cache: 0 schwebend, 0 ohne Treffer, Geroell 7 versunken (max 0,81 m); Budget lod1 1.135.009 Dreiecke; Ladezeit Median 7,49 s (10,6/7,49/7,40, keine Jobs parallel).
- Zacken >0,25 m vor->nach: fein unten 1424->76, oben 272->50; grob unten 312->30, oben 145->17. Grob-Steilquads >6: 190->0, >3: 702->65. Tabelle 56 Felder: pruefung/o18/felder_56_messung.md.
- Bilder (pruefung/o18/bilder/o18c_nach_clay, o18c_nach_tex, je 22): angesehen Ton A1_wand A2_nah B1_wand B2_nah C1_wand C2_nah D1_wand E1_wand F1_schraeg G1_wand G1_schraeg H1_wand; Textur A1_wand A2_nah B2_nah C2_nah D1_wand E1_wand F1_wand G1_schraeg. Nicht angesehen: restliche 10 Ton- und 14 Texturbilder; Vorher-Textur nur A1/B1/C1; die 12 Zusatzstellen nicht gerendert (Job abgebrochen).
- Offen: C2-Kegel Zahnkante am Grat (vermutlich Wand-Mesh, nicht Gelaende); G1-Gipfel noch spitz-pyramidal; B2 gerader Knick im Hang; E1-Nordrand: trockene Rinne bis Kartenrand (171–182|0, bis -9,6 m) – bestand schon vor O18; A1 braune Flaeche mit harter Kante am Kartenrand; H2 Kartenrandpunkt.
- F1-Steinpfad: overlayseitig (rampenwege[1] endet blind 2 Zellen vor Nordwand 227|36), siehe UEBERGABE.md.
- Exporte: /workspace/dorfmap_3d_runde_O18.html, /workspace/dorfmap_felder_3d/ (56 HTML + reihe_1..7.zip, Banner Commit 24c67ab).

## O18d – sichtbare Fehler (Daten-Commit dd8e113)
- Neu (runde_o18.py, nur Anzeige-Gelaende/Wasser): C2-Kegel ins Feinband (Zahnkante weg), gipfel_rund/fein_gipfel mit weichem Auslauf, Feinband bis an konvexe Kanten, farbe_weich (A1), haus_sockel (Gelaende am Haus y+0,40 -> grauer Sockelstreifen weg), ufer_weich + ufer_boeschung (max 0,9 m/m, max 1,5 m Abtrag; B2-Knick), fein_entzacken (H2-Randspalte 1,61 m weg), fluss_einschnitt (Wasser -0,2 m, Bettmulde bis 0,7 m), 23 versunkene/nasse Objekte entfernt (pruefung/o18/versunken_weg.json).
- Regression: t42u 0; Spalt 0; bergauf_gt_2cm 0 (Stufen >30 cm 1304, unveraendert); stufe_bandrand_gt0,3 9 (max 0,41 m; fehlerzaehler 4012, FW-Dump vor Naht); Raycast 0 schwebend/versunken/nass (Baeume, Felsen, Findlinge); Budget lod1 1.202.239 (<1,3 M); deterministisch (md5 gleich). Ladezeit nicht neu gemessen.
- Zacken vorher(O18c)->O18d: fein unten 76->222, oben 50->126; grob unten 30->154, oben 17->304. Von den Top-40 liegen 27/17/39/40 im Wasser/Uferrand (Bettmulde), 13 fein-oben an Hausplateaus. Spitzen (s1>0,25|s3>1,5) 261->153 (P1a)->227 (Haus-/Uferkanten).
- Noch sichtbar: Hausplateaus in Ton-Ansicht kastenfoermig; B2-Ufer am Haus steil/felsfarben; Zacken-Zuwachs an Ufern; A1 brauner Streifen weich aber rechteckig; G1 noch leicht spitz.
- Exporte: /workspace/dorfmap_3d_runde_O18.html (= index.html dd8e113), /workspace/dorfmap_felder_3d/ 56 HTML + reihe_1..7.zip (Banner dd8e113).

## O18e (Haus-Sockel neu, Zacken)
- haus_sockel ersetzt: keine Plateaus/Kaesten mehr. Nur heben wo Gelaende < Hausbasis-0,05 m; Smoothstep-Auslauf 6 m, Steigung <= 0,35 m/m; Hebung blendet 2-3,5 m vor Wasser auf 0 aus (kein Heben in Wasser/Bachbett, keine neue Ufer-Boeschung). Max. Hebung 3,11 m.
- ufer_boeschung s 0,9->0,6 (31 Grad, unter Fels-Schwelle des Shaders).
- Zacken (zacken_t83u): fein unten 52 / oben 12, grob unten 5 / oben 0 (O18d: 222/126, 154/304). Neu: grob_entzacken (Laplace-Mittel, Median gab Schachbrett), fein_entzacken thr 0,22; Bachbett mit wassermaskiertem Gauss geglaettet.
- Regression: t42u 0; lod1 Budget 1,188 M Dreiecke; Raycast nach Cache-Auffrischung: Baeume 2 versunken / 3 im Wasser (von 1438), sonst 0 schwebend.
- Nicht gemacht: Ufer-Fallback "nur Sockelrandzone des Hauses heben" braucht Hausgeometrie-Aenderung (nicht erlaubt, nur Anzeige-Terrain). Treppenmuster am Feinbandrand (X_H2, X_E1) aus O18d nicht behoben.
- Exporte: /workspace/dorfmap_3d_runde_O18.html, 56 Feld-HTML + reihe_1..7.zip (je 8, zipfile), Banner 397bdde.

### O18e Bildpruefung Teil 1 (Export 397bdde, Renders /tmp/o18/G)
- Ton schraeg angesehen: B2, A1, C2, G1, E1, F1, D1, H1, A2, B1, C1. Textur schraeg: A1, D1, E1, H1 (B2/C2/A2 Textur-Render lief noch).
- Kein Kastenplateau, keine Dreiecks-Spitzen in den Boden, kein Fels-Sockel an Haeusern gesehen.
- Rest: B2/C2 weiche Huegel mit facettierten Flaechen um Haeuser (Sockel-Hebung bis 3,1 m wirkt als Beule); Perlen-/Treppenlinien an Klippenoberkanten (E1, F1, G1, H1, D1); leichte Streifen (Moire) an Haengen D1/C1; A1 Textur harte Braun/Schnee-Kante oben links.
- Bach-Kameras Y_* zu nah/flach, nicht aussagekraeftig.
- Noch keine Verbesserungsschleife durchgefuehrt.

## O18f (letzte Schleife, Daten-Commit 5ab2c63)
- Sockel-Hebung gedeckelt 1,2 m, Auslauf 8 m (gen: max 1,2). Neu kante_bilateral (Feinband, Punkte mit 3x3-Spanne >1 m, bilateral sr 0,3 m, 2 It.) vor fein_entzacken. farbe_weich A1: Box 30x60, sigma 9.
- Regression: t42u 0; Zacken fein 60/9, grob 5/0; lod1 1,187 M; Raycast: Baeume 2 versunken/3 im Wasser (1439), sonst 0, Cache unveraendert.
- Export /workspace/dorfmap_3d_runde_O18.html, 56 Feld-HTML + reihe_1..7.zip (je 8), Banner 5ab2c63.
- Bilder /tmp/o18/H (Ton 11 schraeg + 3 nah; Textur A1,B1,C1,D1). Pixel-Diff zu O18e klein (mittl. <0,2/255): Wirkung kaum sichtbar.
- Rest (nur dokumentiert, kein Umbau mehr): B2/C2 weiche Kuppen um Haeuser mit Knicklinien dazwischen (C2_nah); Perlenlinien an Klippenoberkanten E1/F1/G1/H1/D1 bleiben -> Ursache vermutlich nicht Hoehe (Bilateral wirkte nicht), eher Wand-/Band-Naht-Geometrie; Moire D1/C1 Ursache nicht geprueft; A1 Braun-Schnee-Uebergang weicher, Braunflaeche bleibt.

## O18g (Durchsicht-Schlitze H1/G1, Magenta-Marker)
- Ursache: `_bandnaht_j1` lief vor den O18d-f-Nachschritten (Ufer, Sockel, Entzacken, Flusseinschnitt, kante_bilateral) -> Fein-/Grobnaht (T-Stoesse am Bandrand) wieder offen. Fix: Naht am Ende von gen erneut exakt (1180 Punkte angepasst).
- pruefung/loch_o18g.js (offene Innenkanten, 2-cm-verschweisst): index.html 1500 -> 0; alle 56 Felder: 0 innen (Rest = Feldschnittkanten/Sockel-Unterkante).
- Magenta-Klickmarker nur noch mit ?dbg=1; Kamera nicht mehr unter Gelaende/von unten.
- Regression: t42u 0, Zacken fein 45/16 grob 5/0, Budget lod1 1,187 M.

## O18h – Wegbereich zurückgesetzt (598c197, 6e515db)
- Weg ±3 m (+2 m Auslauf, ≥2 m zum Wasser) auf Stand vor O18 zurück, danach fein_entzacken; Raycast-Cache aufgefrischt (6e515db).
- t42u 0 (CSV: nur boden_anzeige_m, 687 Werte); stufe_bandrand 0; Spalt 0/4 Ränder; bergauf 0 (max 0,011 m); lod1 1 186 669 Dreiecke; Lochscan index 0, 56 Felder 0 echte Innenlöcher (nur Schnittkante/Sockel).
- Zähne fein 28/17, grob 5/0.
- Offen: Raycast 2 Bäume versunken + 3 im Wasser, 3 Steine im Wasser, 8 Geröll versunken (vorher 0).
- Ansicht G1-Weg O17 vs. jetzt (w1): Weg-Band wieder durchgehend, aber Terrassenkante weich, Felswand gerundet, heller Wulst an der Unterkante – O17-Optik NICHT erreicht.
- H1/A1/C2 Ton+Textur angesehen: keine Durchsichten; Hänge weich/verwaschen, Textur in A1 streifig.
- Export O18, 56 Felder, reihe_1..7.zip, O18_felder_1/2.zip mit Banner 6e515db neu gebaut.

## Status O18i (Stand d78e8ed)
- Wandkontur: gipfel_rund (Wand Ø 0,93 m) und fein_gipfel (Ø 0,56 m) wirken jetzt nur außerhalb der Wand. Die Kontur ist klarer als in O18h, aber noch weicher als in O17 (f65298b w1).
- Raycast: 0 schwebend, 0 versunken, 0 im Wasser. 19 Objekte wurden über versunken_weg.json entfernt.
- Lippe unter dem G1-Weg (_weg_wulst): die Geometrie sinkt nur leicht (8,08 → 7,77). Das helle Band ist weiter sichtbar. Nicht gelöst, 3 Versuche aufgebraucht.
- Regression: t42u 0 | Spalt 0 an allen 4 Rändern | bergauf 0 (max 0,011 m) | stufe_bandrand 0 | lod1 1.177.224 Dreiecke | Lochscan: Index 0, 56 Felder 0 echte Innenlöcher | Zacken: fein 31/24, grob 7/0 | pruefung/o18/regression_o18i.json
- Gesichtet: B1, D1, G1, E1, F1 in Ton und Textur, keine Durchsicht. Die Wände in E1/F1 sind steil, oben aber weich gerundet.
- Ladezeit: 9,33 / 9,38 / 9,11 s, Median 9,33 s (< 10 s)
- Export: dorfmap_3d_runde_O18.html, 56 Felder, reihe_1..7.zip, O18_felder_1/2.zip

## Status O18j (Stand c4bbd9b)
- Wandrauheit (Mittel |h − Gauss 1 m| auf 46.846 Wandzellen): grob O17 0,589 | O18i 0,449 | O18j 0,463. Fein (gleiche vid): O17 0,496 | O18j 0,485.
- Verursacher an der Wand: grob_entzacken (0,17 + 0,05 m), grob_wand_glatt (0,016 m), entstacheln (0,013 m).
  - grob_wand_glatt und entstacheln wirken jetzt nur außerhalb der Wand.
  - grob_entzacken macht an der Wand nur noch 3 statt 8 Durchgänge. Ganz ohne grob_entzacken an der Wand stiegen die Grobzacken von 7 auf 48.
- Kein Schritt „Wandband aus O17 übernehmen“: fein fehlen nur 2 %. Grob würden die Zacken wieder steigen.
- G1-Streifen: die Ursache ist Geometrie. Unter der Wegkante lag eine flache Stufe, und der Shader legt Schnee nach der Normalen (|N.y|) darauf; in der Ton-Ansicht ist die Fläche genauso hell.
  - Die Stufe ist jetzt auf die Linie Wegkante → Gelände in 4 m abgesenkt, nur in Feld G1. Kartenweit stiegen die Feinzacken auf 42–49.
- Regression: pruefung/o18/regression_o18j.json
  - t42u 0, Spalt 0, bergauf 0 (max 0,011 m), stufe_bandrand 0, lod1 1.179.170 Dreiecke
  - Lochscan: Index 0, 56 Felder 0 echte Innenlöcher
  - Zacken: fein 30/30 (O18i 31/24), grob 9/0 (O18i 7/0)
  - Raycast: 0 (1 Geröll entfernt)
  - Ladezeit: Median 9,19 s
- Angesehen (Vollbild): w1 O17/jetzt, G1 Ton + Textur, E1, F1, D1, C1, H1. Keine Durchsicht.
  - Die Simse ist weg, darunter ist der Hang aber weiter hell verschneit.
  - Die Wände sind steil, oben aber weiter gerundet und nicht so kantig wie in O17.

## t127u Ehrlicher Ausgangswert (Gate kartenweit, keine Ausnahmen mehr)
- pruefe_regeln.py: 596 Treffer, Ausnahmen 0. `_ausnahme` ist abgeschaltet, auch fuer die Kreuzungen 2x11, 3x5 und die Kehre 12.
- r8_kreuzung.py: 48 (R8_stufe 9, R8_gitter 10, R8_quer 5, R8a_wegende 24 von 24). Quer an reinen Wegenden wird jetzt senkrecht zur Wegrichtung gemessen.
- r9_form.py (neu): 334 (R8b_delle 25, R9_saegezahn 34 Felder, R9w_wellen 275).
- **Summe 978.** D2 hat 0 Treffer in R8/R9 (Regressionsbasis). G1: R8a 1, Delle 1, Saegezahn 1, Wellen 6. D1: R8 5, R8a 3, Delle 2, Saegezahn 1, Wellen 23.
- export_gate.sh ruft alle drei Pruefer auf und meldet ROT, wenn einer Treffer hat.
