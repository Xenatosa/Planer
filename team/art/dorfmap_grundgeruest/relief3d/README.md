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
