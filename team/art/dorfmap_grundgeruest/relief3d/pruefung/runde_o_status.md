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
