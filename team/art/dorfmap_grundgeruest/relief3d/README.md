# relief3d (t41u) – neues 3D-Relief
Öffnen: index.html (t42u: glattes Relief, c20 als Bodentextur, NEU/ALT-Schalter, „Am Nordwand-Fuß“ mit 1,8-m-Figur).
- gen_relief.py → zellen_relief.csv, dorfmap_relief_z25.glb; gen_textur.py → textur_relief_t42u.jpg; pruefung/pruefe_t42u.py → abgleich_t42u.json, relief_daten.json.gz, relief_zaehlung.json
- gen_wandtextur.py → wand_textur.png; baue_html.py → index.html; test_relief.js → test/*.png + test_ergebnis.json
- Plan: _alt/NEUAUFBAU_PLAN_t41u.md, Zahlen/Annahmen: ABWEICHUNGEN.md. Altstände: ../_alt/


## Stand t44u Runden 9-10
- Glattere Abbruchkanten (nur Netz), Wandtextur mit weniger Fugen, Moos/Grossfarbe, Schindelfelder, Traufbretter, ungleichmaessiger Dachschnee, Zaeune mit Kollisionspruefung, schaerfere Schatten, Sockel mit Gesteinsschichten.
- Vergleich vorher (e6111b1) / nachher final: `test/t44u_r10/vergleich_*.png`.

## Stand t44u
- Oeffnen: `index.html` (Ansichten Reset/Oben/Unten/Am Nordwand-Fuss/Gehen; `?lod=1` fuer Handy).
- Neue Objekte in `objekte_neu.js` (Fichten, Kiefern, Felsen, Haeuser mit Schindeln, Laeden, Fensterlicht, Vordach, Anbau, Holzstapel, Kaminrauch).
- Test: `KURZ=1 MODI=neu NODE_PATH=/tmp/w3/node_modules node test_relief.js` -> Ansichten schraeg, nordwand, krater, suedwand, oben, unten, rand, rueck, dorf, boden_wand, totale_auge.
- Vergleich vorher (t43u) / nachher: `test/t44u/vergleich_*.png`. Zwischenstaende: `_alt/t44u_zwischenstand/`.

## Stand t47u/t48u (Runden 1-6+)
- Bauen: `python3 gen_relief.py && python3 baue_html.py` -> `index.html` (eine Datei, offline per Doppelklick).
- Pruefen: `python3 pruefung/pruefe_t42u.py` (muss `summe 0` geben).
- Rendern aller 11 Kameras (3 parallele Teil-Laeufe, kein Timeout am Ende): `SUF=r7 OUT=/tmp/r7 sh rendere_alle.sh`; eine Ansicht: `NODE_PATH=/tmp/w3/node_modules node test_einzelansicht.js index.html out.png`.
- GLB-Pfad: `python3 -m http.server 8000` in diesem Ordner, dann `http://localhost:8000/index.html?glb=1` -> Gelaende kommt per GLTFLoader aus `dorfmap_relief_z25.glb` (mit Vertexfarben). Ohne Server / ohne `?glb=1` nutzt der Viewer die eingebetteten Daten (Single-File-Fallback).
- Handy-LOD: `?lod=1` oder automatisch auf Handy.
- Felsformen: `blender/fels_meshes.py` (headless Blender 4.2.3 portable aus download.blender.org, `/tmp/blender-4.2.3-linux-x64/blender -b --python blender/fels_meshes.py`) -> `blender/fels_meshes.json`, wird in die Daten eingebettet.
- Hoehenfeld: fBm-Felsform, Kraterrippen/Scharten, thermische Erosion (Wandfuss), hydraulische Tropfen-Erosion (Wandzone, max 0,8 m); Zellwerte unveraendert (Pruefung summe 0).

### Blender-Workflow (t48u)
- Version: Blender 4.2.3 portable (Linux x64, download.blender.org), headless: `/tmp/blender-4.2.3-linux-x64/blender -b --python blender/fels_meshes.py`
- Parameter: 8 Felsen, Ico-Sphere Subdiv 5, Radius 0.6, Zufalls-Skalierung; Displace VORONOI Staerke 0.16 (Scale 0.55-0.85) + CLOUDS 0.10 (Scale 0.25); Decimate 0.08 (~408 Dreiecke/Fels); Achsen y<->z getauscht, Dreiecks-Reihenfolge umgedreht (sonst Innenseite sichtbar).
- Ausgabe `blender/fels_meshes.json` -> `gen_relief.py` bettet ein. Desktop nutzt Blender-Form, Handy (?lod=1) Ikosaeder.
- GLB: `dorfmap_relief_z25.glb` (Boden + Waende mit Vertexfarben), Start: `python3 -m http.server 8000`, dann `http://localhost:8000/index.html?glb=1`. Ohne Server: `index.html` direkt (Einzeldatei).

## t54u – Wände mit Kontur statt Blockhaufen (Stand Runde B, Commit 87e88c8)
- Grobprofil breiter: mittlere Wandneigung 58,7° grob / 58,6° fein [S]. Sprünge Nord 14,09 / Süd 16,15 / Krater 11,09 / Ost 12,0 m [S].
- Feinrelief: Schichtbänder (Absätze ~2,4 m), Rinnen/Rippen, Tropfen-Erosion, Schnee auf Absätzen und in Rinnen, 5 Felstöne (grau/ocker/dunkel/hell) [A].
- Ufer: flaches Wasser am Rand durchsichtig, Kiesbänke und dunkle Uferlinie in den Bodenfarben [A].
- Rampen am Krater: rampennahe Zellen jetzt im Feinband, Relief dort weich auf 0 → kein glatter grauer Streifen mehr [A].
- Blender-Versuch (blender/wandband_t54u.py, Displace + Voxel-Remesh): wirkt knetig/blasig statt geschichtet, 2,3× Dreiecke, Rand passt nicht nahtlos an das Gelände → nicht übernommen. Bilder: test/t54u/blender_vs_feinrelief_B.jpg.
- Runde C (Voronoi-Klüfte, seitlicher Versatz) verworfen: schwarze Löcher/Schatten im Bild (test/t54u/verworfen_rundeC_schwarze_loecher.png), Code liegt nicht im Repo.
- Prüfung: Zellabgleich summe 0, Wasser größte Komponente 4808 Zellen, Handy 1.075.230 Dreiecke [S].

### t54u Runde D
- Ursache der schwarzen Flecken aus Runde C: kein Schatten/Bump-Problem, sondern ein Namenskonflikt (`_gy/_gx` überschrieben) → Vertexfarben außerhalb des Gitters = 0 (schwarz). Behoben.
- Seitlicher Warp der Feinbasis im Wandband (Vorsprünge/Buchten bis ~2,5 m). Ein Warp im Grobgitter wurde verworfen, weil er zellen_relief.csv verändert hätte (Zellwerte bleiben fix).
- Fels grauer (Palette grau/dunkelgrau, Ocker selten, Shader entsättigt), Schnee in Rinnen, Ufer-Schaum reduziert.
- Prüfungen [S]: Zellabgleich 0, Sprünge 14,09/16,15/11,09/12,0 m, Neigung 55,8° fein / 51,6° grob, größte Wasserkomponente 4808, Handy 1.075.230 Dreiecke.
- Bilder: test/t54u/*_rundeD_r66.png, vgl_*_B_D.jpg.

### t54u Runde E (+ t55u Geometrie, t57u Referenzen)
- Wandband im Feinrelief breiter (Dilation 3 statt 1), stärkerer seitlicher Warp (bis ~5 m), Großrippen/-rinnen in Falllinie, Grat-Türme/Felsnasen an der Oberkante, Schutthalden am Fuß – alles als echte Vertex-Höhen (FD/FH), nicht Shading.
- Formbeweis: `?clay=1` = einfarbig grau, ohne Textur/Vertexfarben/Bump, nur Gelände sichtbar. Silhouetten-Ansichten `silh_sued`, `silh_nord`.
- Grenzen: Höhenfeld → keine echten Überhänge möglich. Feine Rillen kommen weiter zusätzlich aus Bump/Textur (Platzhalter).
- Wasserfall-Fuß: Schaum gedeckelt (max 0,3).
- Prüfungen [S]: Zellabgleich 0; zellen_relief.csv, glb, relief_zaehlung.json, abgleich_t42u.json per git diff unverändert; Sprünge 14,09/16,15/11,09/12,0 m; Neigung 57,4° fein / 46,9° grob; Wasser 4808; Handy 1.107.294 Dreiecke.
- Bilder: *_rundeE_r70.png, *_clay*.png, vgl_D_E_teil1/2.jpg, vgl_ton_E_mit_referenz.jpg.

## Runde F (t57u/t58u/t59u)
- Feinband: Pfeiler (Rippe 14 Feinpunkte), Kare unter dem Grat, bis 60 Gipfelpyramiden (jetzt weiche Spitze/weicher Fuß), Schneepolster 0,2–0,3 m als Geometrie auf Absätzen. [A]
- Politur t58u: Feinband-Basis leicht geglättet (Treppen aus Grobgitter weg), Nadelspitzen gegen Umgebung gedämpft, thermischer Grenzwinkel 71°. [A]
- 36 Felsnasen/Überhänge als Zusatz-Mesh `FW.ov/ovi` (11 520 Dreiecke), hinten und oben ins Gelände eingebettet, Clay-Modus grau. Wirken noch eher wie flache Platten. [A]
- t59u Platzierung: Bäume/Felsen/Findlinge/Steine/Geröll/Gras im Feinband auf Feinhöhe gesetzt, aus steilen Stellen und unter Nasen bis 3 m weggerückt. Zählung in `pruefung/platzierung_t59u.json` (z. B. Bäume vorher 245 steil/Nase, 254 versunken, 34 schwebend → nachher 0 steil/Nase). [S]
- Prüfungen: summe 0, Zelldateien byte-gleich, Sprünge 14.09/16.15/11.09/12.0 m, Neigung 58.8° fein / 47.7° grob, Wasser 4808, Handy 1 118 814 Dreiecke. [S]
- Bilder: test/t54u/*_r72.jpg (11 Ansichten), *_r73.jpg (grau), vgl_E_F_mit_referenz.jpg.

## Runde G
- Felsnasen-Meshes abgeschaltet (sahen wie Platten/Ringe aus); Code bleibt, nur mit `OV=1`. Stattdessen Gesimse im Höhenfeld (steile Kante unter der Oberkante, ~0,9 m, per Rauschmaske sparsam). [A]
- Etwas markanter: Pfeiler 1,0→1,3, Kare 2,2→2,8, Nadel-Dämpfung erst ab 0,9 m Überhöhung (statt 0,5). [A]
- Stelle t58u per Bildabgleich gefunden: Ansicht silh_nord (E), Treffer 0,996; Ort ca. x=186, z=37 (Nordwand-Bereich). Vorher/Nachher: test/t54u/spitze_t58u_vorher_nachher.jpg. [S]
- Prüfungen: summe 0, Zelldateien byte-gleich, Sprünge 14.09/16.15/11.09/12.0 m, Neigung 59.9° fein, Wasser 4808, Handy 1 107 294 Dreiecke; Platzierung 0 Bäume steil nachher (pruefung/platzierung_t59u.json). [S]
- Bilder: test/t54u/*_rundeG_g.jpg (11), *_clayG_g.jpg (grau inkl. Nord und Silhouette Nord).

## Runde H (Basis G 5488f57) – schärfer, Felszahn t58u
- Grate geschärft: Unscharf-Maske nur auf Rücken (FH−gauss3, begrenzt 1,2 m, ×0,4), Pfeiler ×1,05 (G: 1,3).
- Felszahn bei x≈186, z≈37: Grat entlang Hangrichtung, lineares Querprofil (klare Kante), Fuß breiter, 4,5 m; von Nadel-Dämpfung ausgenommen.
- Thermik-Grenzwinkel 66° (G: 71°), damit Neigung unter 60 bleibt.
- Werte [S]: Neigung 59,9°, Summe 0, Dateien unverändert, Sprünge 14,09/16,15/11,09/12,0, Fluss 4808, Handy 1.107.294 Dreiecke, Bäume/Felsen auf steil 0.
- Bilder: test/t54u/*_clayH_h.jpg, *_rundeH_h.jpg, vgl_E_G_H_grau_mit_referenz.jpg, spitze_t58u_E_G_H.jpg.

## Runde I (t61u) – Löcher im Boden und Fluss bergauf
- **Löcher [S]:** Die Ursache war die Handy-Stufe (LOD 2). Dort lagen die Kantenmitten des feinen Bands nicht auf den Kanten des groben Gitters. Das ergab 4.282 Risskanten über 1 cm, maximal 0,50 m. Die Lösung ist ein Snap in `main.js`. Prüfung mit `pruefung/pruefe_mesh_t61u.py`, Ergebnis in `pruefung/mesh_t61u.json`: Spalt max 0,0 m bei LS1 und LS2, 0 NaN, 0 nicht-manifold, 0 Wasser unter Gelände. Rein topologisch bleiben offene Innenkanten übrig (T-Stöße): 26.754 bei LS1 und 13.377 bei LS2. Sie haben aber keinen Spalt. Bilder: `test/t61u/vgl_loch_*`, `loch_a_zoom_t61u.jpg`.
- **Fluss [S]:** Vorher stieg das Wasser stromab um bis zu 8,66 m an, bei (46,5|166,5). 1.813 Vertices lagen höher als ihr Vorgänger stromauf. Der Hauptstrang hatte 98 Anstiege, maximal 1,17 m. Jetzt sind es 0 Anstiege über 2 cm. Der Hauptstrang fällt von -5,97 auf -16,42 m (435,8 m lang). `fluss_t61u.py` macht das so: Der Wasserspiegel folgt dem Hauptarm (dem längsten Oberlauf). Danach wird das Bett nur in der Anzeige eingegraben, im neuen Feld `GB` in `relief_daten`. Das Feld `G` bleibt gleich den Zellen. Die Anzeige weicht an 4.900 Vertices ab, das betrifft 1.876 Zellen, bis 8,9 m tief. Zellen, CSV und glb sind unverändert, Summe 0. Neu steiler als 60° in der Anzeige: 930 Vertices, davon 271 an Land (Bettkanten). Profil: `test/t61u/flussprofil_vorher_nachher_t61u.jpg`, Zahlen in `pruefung/flussprofil_t61u.json`.
- **Budget [S]:** Handy 1.047.657 Dreiecke.

## Runde J (t62u)
Der Fluss läuft jetzt als flache Kaskaden im Talboden, nicht mehr am Hang und nicht am Wandfuß. Steile Neupunkte über 60° an Land: 103 (Runde I 271). Tiefster Schnitt 1,26 m (Runde I 8,9 m). Der Fluss ist durchgehend. Mit Becken als Senken gibt es 0 Bergauf-Stellen. Bilder liegen in test/t62u, Prüfungen in pruefung/*_t62u.json. Wege sind unverändert.
## Runde K (t63u)
Der Westarm fließt jetzt im Tal um die Hügel herum (fluss_k.py). Der Wasserspiegel fällt überall, bergauf 0. Stufen über 1 m gibt es nur in der Schlucht-Rinne (max 3,31 m). Neue Kreuzungen mit Wegen oder Häusern: 0. Bilder liegen in test/t63u (draufsicht_vorher_nachher, laengsprofil_k, nah_fluss_k, ansichten_*), Prüfungen in pruefung/*_t63u.json.

## Runde L (t64u)
Randschlitze 0 m (Viewer, LS1/LS2), K9-Fixes (Südfluss-Stummel, Schluchtwasser, Südwand-Streifen gemindert), Flachland-Farben weich, Lochsuche 29 Nahkameras: 0 Löcher. Mesh-Spalt 0, bergauf 0, Handy 1 099 919 Dreiecke, t42u Summe 0. Offen: Ostrand (bewusst, Sockelwellen), Felswand-Streifen, 6 Objekt-Ausreißer bis 0,79 m. Details ABWEICHUNGEN.md, Bilder test/t64u/, Prüfungen pruefung/*_t64u*.json. Lochsuche: `LOCH=1 CAMS="$(cat pruefung/loch_kameras_t64u.json)" node test_loch_t64u.js`.

Runde M (t65u): Raycast aller Objekte 0 schwebend/0 versunken/0 im Wasser [S]; Bäume 1873->1590 [F] (60 Überlappung, 266 Abstand/Doppelte; vorher 55 Baumpaare <0,1 m; 30 an Lücken nachgesetzt); Tümpel West eben -9,45 [F]; See/Fluss-Lücke zu [F]; Q1-Platz Farbe gedämpft; Handy 1 054 929 Dreiecke [S]; Mesh-Spalt 0, bergauf_pfad 0, t42u Summe 0 [S]. Bilder test/t65u/ (13+13 Ansichten, 34 Nahbilder, Kachelraster tex+clay 4x4).

Runde O (t67u): Flüsse zum Rand geöffnet, Nadeln gekappt (8->3 >1,5 m), grobe Spitzen nahe Wasser gesenkt, Rampen liegen jetzt im Gelände (Raycast, weiche Ränder, geschwungen). Spalt 0, t42u 0, Handy 1 055 021 Dreiecke (Endmessung O9, 01.11.); Raycast O9 nicht erneut gemessen (Testseite lud nicht in 300 s), letzter Wert 0. Schneegrenze verrauscht, weiche Wasserrand-Maske (nur Shader). Offen: Uferstufen fluss_7/fluss_9 (Gelaende-Schattierung), Restzacken wand_0_24 unten. Offen: 13 grobe Band-Eckspitzen, Kraterrand-Nähte, west_276 harte Wasserkante. Details ABWEICHUNGEN.md, pruefung/runde_o_status.md, Bilder test/t67u/.

Runde O5 (01.11.): Wasser-Diagnose mit ?hide=winnen,wrand: Uferzaehne/Platten fluss_7 kommen von INNEREN Wasserzellen [S]. Darstellung: flache Ecken (<0,12 m) weich unter den Boden gesenkt -> Platten weicher; Zaehne fluss_7 und Treppen fluss_9 bleiben (2 Versuche, nicht sauber). Szenentiefen-Pass nur mit ?softwater=1 (Standard aus), Tiefenmaske 880fa1d entfernt. Endmessung [S]: Spalt 0, t42u 0, bergauf_pfad 0, Raycast 0/0/0, Handy 1 047 817 Dreiecke. HTML /workspace/dorfmap_3d_runde_O5.html.

Runde O7 (01.11.): Flussbett im Generator weich geformt (`ufer_profil`, smoothstep B=2,5 m, ≤35°), Zellwerte unveraendert, ?wneu Standard. Messung [S]: t42u 0, bergauf_pfad 0, Spalt wie Basis (0,28 m an 6 Kanten bei 108|46, schon vorher), Raycast 1 Baum + 7 Steine schwebend, 0 im Wasser, ~1,137 M Dreiecke, Ladezeit 8,2 s. fluss_7-Stufen bleiben (im Wasser). HTML /workspace/dorfmap_3d_runde_O7.html.

Runde O8: Spalt 0, Raycast schwebend 0, Bett geglaettet; Details pruefung/runde_o_status.md, Bilder pruefung/o8/.
- O9 (K1b-K4): siehe pruefung/runde_o_status.md; Export dorfmap_3d_runde_O9.html; offen: Haarlinien Ostrand, fluss_7 Uferterrassen, Keil wand_288_144, Rillen wand_48_168.
