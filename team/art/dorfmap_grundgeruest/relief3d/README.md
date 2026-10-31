# relief3d (t41u) – neues 3D-Relief
Öffnen: index.html (t42u: glattes Relief, c20 als Bodentextur, NEU/ALT-Schalter, „Am Nordwand-Fuß“ mit 1,8-m-Figur).
- gen_relief.py → zellen_relief.csv, dorfmap_relief_z25.glb; gen_textur.py → textur_relief_t42u.jpg; pruefung/pruefe_t42u.py → abgleich_t42u.json, relief_daten.json.gz, relief_zaehlung.json
- gen_wandtextur.py → wand_textur.png; baue_html.py → index.html; test_relief.js → test/*.png + test_ergebnis.json
- Plan: NEUAUFBAU_PLAN.md, Zahlen/Annahmen: ABWEICHUNGEN.md. Altstände: ../_alt/


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
