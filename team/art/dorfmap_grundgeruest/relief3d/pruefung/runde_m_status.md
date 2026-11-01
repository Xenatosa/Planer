# Runde M (t65u) – Zwischenstand
Basis 595215f. Werte [S] = selbst gemessen.

## 1 Zellen (101 808) – pruefung/zellen_voll_t65u.json/.csv
- a: alle 0 ausser a_wandname_ohne_klippe 11 558 = gewollt (wand_name ist Gebietsname, nicht Klippe).
- a_baum_ok_auf_wasser_oder_WAND: 2 102 -> 0 [F] (csv_nachlauf).
- 4 Wasser-Restzellen (148|0, 188|36, 222-223|202) trocken [F].
- b_spiegel_unter_bett 323: CSV-Spalte wasserspiegel ist c20-Altwert; neue Spalte wasserspiegel_anzeige_m stimmt mit Anzeige. Offen/gewollt.
- b_bebaubar_hang_gt_30grad 1 223: offen (Bauzonen-Plan anderer Teams, nur lesen).
- c_hoehenstufe_sonst 439: alles Hänge 25,7–54,9° unter Wandwinkel, gewollt.
- d_vertexfarbe >60: 178 -> 168 (111 Vertices geglättet [F]); Rest = einzelne dunkle Punkte im Schnee/an Klippe, angesehen.
- t42u summe 0, Mesh-Spalt 0 (LS1/LS2).

## 3 Gewässer – pruefung/fluss_ausgang_t65u.json
- Hauptfluss: Quelle 212|194 (-0,31) -> Ostrand 336|281,5 (-18,2), 211 m, lückenlos, bergauf 0 (Pfad).
- Lücke See/Fluss 4,24 m geschlossen (34 Wasser-Vertices) [F]; Stummel 1,5 m (19) [F].
- 4 Spiegel-Mulden bis 1,6 cm an der Quelle angehoben [F].
- See -3,0 m: abflusslose Senke (gewollt), daher Profil bergauf_summe 3969 = nur Seepunkte, bergauf_pfad 0.
- Tümpel West (x11-38, z40-60): 2 m tiefer als Bach 16,8 m östlich, kein Abfluss möglich -> Senke; Spiegel war 0,6 m schief, jetzt eben -9,45 [F].
- 2 Plateaubäche -> Ostrand, 2 Nordtümpel -> Nordrand; übrige Schmelzwasser-Tümpel (z<12) und Pfützen bei z≈210 abflusslos (gewollt, Schneeplateau/Uferpfützen).

## 2 Objekte
Bäume 1873->1547, Felsen 95->92, Findlinge 40->30, Steine 871->809, Geröll 956->731 (abgesenkt/steil/Wasser/Überlappung/Abstand) [F]. Browser-Raycast: offen.

## Offen
Raycast, 20+ Nahbilder, Kachelraster, helles Rechteck Süd, Wandstreifen, 13+13 Ansichten, Doku.

## Stand Ende Runde M
Alles erledigt bis auf: Wald-Vorher/Nachher-Draufsicht nicht gerendert, krater_*-Nahkameras falsch platziert, 3 Waldzellen >50 % Verlust. Raycast 0/0/0, Handy 1 053 275, Spalt 0, bergauf_pfad 0, t42u 0. Q1 Farbe gedämpft. Details ABWEICHUNGEN.md.
