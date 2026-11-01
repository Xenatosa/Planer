# Runde O – Status (t67u)
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
