# P3 Texturschicht – Ergebnis (Branch art/dorfmap-p3, Basis 8e374b0), 16.11.2026

## Kurz
- **T1_fleckrand 94 → 0** ohne Ausnahme. Die Flecken (Schnee gegen Gras/Erde) haben jetzt weiche, organische Raender statt Pixeltreppen.
- **T2 (Textur abgeschnitten):** Feinband-Farbe FW.c kommt jetzt aus der fertigen VC. Vorher war sie vor den spaeteren VC-Glaettungen abgegriffen, dadurch waren am Feinbandrand gerade oder treppige Flecken abgeschnitten (C2, H2, H5, H6, E6 u. a.). Die NW-Ecke (A1/A2), ein verschmiertes Rechteck ohne Detail, hat jetzt Textur und einen organischen Rand.
- **QA P4 C3 Hangfuss x≈85:** Die punktierte Linie kam aus dem Bildschirm-Bump (dFdx/dFdy), wo der Hang streifend gesehen wird. Sie ist behoben (main.js, nur Darstellung).
- **T3, T4, T5:** Bildpruefung ohne Texturbefund, Form-Befunde gehen an P1 (siehe AUSNAHMEN_P3.md).
- **Hoehen und Wege unberuehrt.** Die geschuetzten SHA sind bitgleich, in beiden gz sind nur die Schluessel `VC` und `FW.c` anders.
- Andere Familien: keine steigt (alle Zahlen identisch).

## Gate (eigene Lochscan-Datei `/workspace/.p3_tmp/gate_loch_p3.json`, Skript `p3_nahbilder/werkzeug/gate_p3.sh`, Pruefer unveraendert)

| Familie | vorher 8e374b0 | nachher P3 |
|---|---:|---:|
| **pruefe_regeln gesamt** | **570** | **476** (mit `BILD_T2..T5=ok` 472) |
| T1_fleckrand | 94 | **0** |
| T2/T3/T4/T5 bildpruefung_offen | je 1 | je 1 ohne Flag, 0 mit `BILD_T*=ok` (Bildpruefung unten) |
| R1_blind | 24 | 24 |
| R2_getrennt | 15 | 15 |
| R3_laengs_m / R3_quer_pct / R3_woelb_m | 35 / 23 / 22 | 35 / 23 / 22 |
| R5_loch | 17 | 17 |
| R6_wasser_schnee | 4 | 4 |
| G2_spitze_oben / G3_spitze_unten | 3 / 3 | 3 / 3 |
| G2_spitze_oben_fein / G3_spitze_unten_fein | 8 / 2 | 8 / 2 |
| G5_beule_klippe | 68 | 68 |
| G6_facette | 220 | 220 |
| G7_wand_glatte_flaeche | 1 | 1 |
| G8_fluss_nicht_bis_rand | 1 | 1 |
| G7b_wandkontur rauheit / kantenschaerfe / feld | 1 / 1 / 24 | 1 / 1 / 24 |
| **r8_kreuzung** (R8_stufe 9, R8_gitter 10, R8_quer 5, R8a_wegende 24) | **48** | **48** |
| **r9_form** (R8b_delle 25, R9_saegezahn 34, R9w_wellen 275) | **334** | **334** |
| Lochscan offen_innen | 0 | 0 |

Das Gate bleibt ROT wegen der Form-Familien (P1/P2), nicht wegen der Textur. `regeln_letzter_lauf.json` ist der Lauf ohne `BILD_T*`-Flags (476).
Eigene Nachmessung `p3_nahbilder/werkzeug/t1_p3.py`: T1 = 0, dc_max auf bewertetem Land 62,0 (Schwelle 70), 0 Punkte > 70.

## T1 je Kachel (vorher → nachher), Nahbild je Kachel `p3_nahbilder/<Kachel>_drauf_T1.jpg` und `_schraeg_T1.jpg` (vorher | nachher + 300-%-Ausschnitt)
A3 1→0, B3 5→0, B4 3→0, B5 1→0, B6 2→0, C2 2→0, C4 1→0, C5 1→0, C6 3→0, C7 2→0, D2 7→0, D3 3→0, E1 2→0, E2 6→0, E3 3→0, E4 4→0, E6 1→0, F1 2→0, F2 4→0, F4 2→0, F5 9→0, G1 3→0, G2 3→0, G3 4→0, G5 4→0, G6 1→0, H2 4→0, H3 1→0, H4 1→0, H5 4→0, H6 5→0 (zusammen 94 → 0).
Uebersicht: `p3_nahbilder/uebersicht_T1_1.jpg` … `_4.jpg` (alle 31 Kacheln, drauf und schraeg, vorher | nachher).

## Bildpruefung T2–T5 (alle 56 Kacheln, Feldkamera Textur | Clay, Kameras in `werkzeug/kameras_p3.py`)
| Pruefung | Ergebnis | Nahbilder |
|---|---|---|
| T2 Textur abgeschnitten | **bestanden.** Abgeschnittene Flecken am Feinbandrand (C2, E6, H2, H5, H6) sind weg, die NW-Ecke A1/A2 hat Textur. Uebrig ist nur eine Formkante am Plateaurand A1/A2, auch im Clay → P1 | `ecke_drauf_T2.jpg`, `ecke_schraeg_T2.jpg`, `C2_schraeg_T1.jpg`, `H5_drauf_T1.jpg`, `E6_drauf_T1.jpg` |
| T3 Streifen/Ringe | **bestanden (Textur).** Kein Streifen und kein Ring in der Textur. D1-Clay: schwacher Ring und Nahtlinie im Neu-Netz (Form, kaum sichtbar) → P1 | `bildpruefung/T3_kern_D1_D2_vorher_nachher_clay.jpg`, `bildpruefung/T3_kern_G1_vorher_nachher_clay.jpg`, `bildpruefung/T3_D1_wegende_textur_clay.jpg` |
| T4 graue Flussstreifen | **bestanden.** 9 Flusskameras A3…H7 ohne graue Streifen. Weisse Linien im Wasser (C7/E7/G7) gab es schon vorher, sie gehoeren zum Wassernetz und zur Uferform | `bildpruefung/T4_fluss_vorher_nachher_clay.jpg` |
| T5 Textur vs Clay | **bestanden.** Textur folgt der Form, kein Texturmuster ohne Form. Formbefunde (C4-Treppen, B1/C1-Rampen, E1/F1-Wasserfallzaehne, C2-Hausplaetze) → P1 | `bildpruefung/feld_textur_clay_1.jpg` … `_7.jpg` |

## QA P4 Zusatz: punktierte Texturlinie C3 Hangfuss (x≈85, z 105–112)
- Ursache, mit Ausschluss-Renders belegt: Es liegt nicht an Vertexfarbe, Tint/Schnee (FW.t/FW.s), Normalen, Schatten, Linienobjekten oder Wandtextur. Mit `?nobump=1` verschwindet die Linie. Der Detail-Bump in `main.js` rechnet mit dFdx/dFdy. Wo eine Hangrippe fast streifend gesehen wird, geht det→0 und dFdx(hb) wird sehr gross. Dann kippt die Normale, und es entstehen dunkle Punktreihen.
- Fix (`main.js`, nur Shader): Der Bump wird ausgeblendet, wenn die Bildschirm-Facette streifend gesehen wird (`gz=|dot(normalize(cross(dpx,dpy)),normalize(vViewPosition))|`, `grd*=smoothstep(.08,.3,gz)`). Mit `?bumpkante=alt` gibt es den alten Stand zum Vergleich. Zusaetzlich rendert das Feinband-Material nur noch die Vorderseite (`side:FrontSide, shadowSide:DoubleSide`). Das Feinband ist ein reines Hoehenfeld (alle Dreiecke nach oben gewickelt, Schuerze aus).
- Nahbild (Spielkamera nah 35°, 15 m, wie `qa_p4/bilder_8e374b0/G6_C3_3_nah.jpg`): `p3_nahbilder/qa_p4_C3_hangfuss.jpg` (vorher | nachher, 300 % Textur und Clay). Clay-Nachweis: `p3_nahbilder/qa_p4_C3_clay_rueckseiten.jpg`. Im Clay bleiben die Linien, weil `?clay=1` beidseitig rendert. Nur mit Vorderseiten verschwinden sie, also gibt es dort keine Formkante.
- Wirkung sonst: Die mittlere Bildabweichung aller T1-, Feld- und Flussbilder vor und nach der Shader-Aenderung liegt bei hoechstens 0,16 Graustufen. Es aendern sich nur streifend gesehene Stellen.
- Hinweis: Das eingecheckte `index.html` (Relief-Neu, nur D1/G1/D2) enthaelt diesen Bump-Code nicht (aelteres Bundle). Dort wurde nur die Datennutzlast getauscht. Wirksam ist der Fix im Vollkarten-Viewer (`baue_html.py`-Legacy-Pfad und `qa_p4/baue_vollansicht.py`) und bei jedem neuen Bundle-Bau aus `main.js`.

## Was geaendert wurde (nur Farbe/Darstellung)
- `gen_textur.py`: neuer Modus `python3 gen_textur.py vc`. Das alte Verhalten bleibt Standard (`textur_t42u()`). Ablauf von `vc_lauf()`:
  1. `vc_ecke_nw_p3`: NW-Ecke, Rand mit Rauschen verzogen, Detail aus 35,5 m Abstand uebernommen.
  2. `vc_fleckrand_p3`: iterative Land-Glaettung nur dort, wo dc > 62 im T1-Bereich, mit weichem Gewicht, bis nichts mehr uebrig ist.
  3. `FW.c` = bilineare fertige VC am Feinpunkt.
  Geschrieben werden `relief_daten.json.gz` und `neu/relief_neu.json.gz`, dabei nur `VC` und `FW.c`. Der Modus ist idempotent: Ein zweiter Lauf meldet „unveraendert“.
- `relief_daten.json.gz`, `neu/relief_neu.json.gz`: nur `VC`, `FW.c` anders (`werkzeug/schluessel_p3.py`), `neu_mesh_tiles` gleich.
- `index.html` = `neu/index.html`: nur die Nutzlast (NEU_GZ) getauscht, Bundle-Bytes unveraendert.
- `main.js`: Bump-Ausblendung an streifenden Facetten, Feinband FrontSide (QA P4).
- `pruefung/regeln_letzter_lauf.json`: vom Gate neu geschrieben.
- Neu: `pruefung/p3_nahbilder/` (Nahbilder, Blaetter, `werkzeug/`), `pruefung/AUSNAHMEN_P3.md`, dieser Bericht.

## SHA-Nachweis (sha256sum, vorher 8e374b0 = nachher)
```
neu/zellen_relief.csv       99d30e55310453725aa1c9613900b5203f430f75f19745244fe3ebd650fc93fa
neu/vektor.json             aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e
neu/felder.json             e4e2ec8f5f4b7b7bb825f8fdda6c0400b5525e9c8c31153f7d9b10d4185e3435
D2-Hoehe (GB, Kachel D2)    749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6
GB    ce965aa718f08f2b790e28285bce4b578f9a6a727a46d9b9758a04aeee684855
G     ce481e30160cbfe6c8425ba7eba2a625a9ffa4ac1b26db87d4647dff43d39e5d
WV    532f2579edcc8d092c44a793263380820eb50265e0c6ccdd4c7f1d3a40d31477
WEGA  2f65ecaf06d2318e69105f8715a87d49358a68411f6244ef63fedce4c39fde06
FW.h  de29b16793fb5dd99e1591e122666ec01fe473b2c9a5dd6b154e3c0f544d8d4d
FW.vid 2dcc01294221be77549eeb9beac9930bfdd28c1a4e8891c2c9bbcfdaee17b0d0
FW.band bc856985772a872631015e3c0dc46b362beb0b78452f640bd20dc8ee2f1ac2c0
FW.t  1a5464782ded887d9cb7b5a5b9b85b58b12242b1d6763747255adb1b18673cd2
FW.s  5ff3dcbda3d5a032916f507163578f444140f0e3530ea2705da7d9acc23c3fb9
wege  c885bbfb8ab5e8c10e32ccd2ef69113ddfbaee08864a433a81e83e4fa43214ee
rampenwege 7e868f9ab32c7328529d888ca2a7e9a3d075dee04e355a32c3e2a1c288f19780
bruecken 3f5d0da6bbab8cbfe417caea7f6dd42f09c7e2fdb1613c390a9f381157815c2e
haeuser a765321360ecfdf6dec655aabf0dd081fe9f890c25ecfdde8a5ea3b074448e9e
```
Pruefskript: `p3_nahbilder/werkzeug/sha_p3.py` (Ausgabe vorher und nachher zeilengleich). `git diff 8e374b0` auf die drei neu/-Dateien ist leer.

## Offene Punkte
- **Bindung an das Neu-Netz:** `neu_mesh_tiles.source_relief_sha256` zeigt auf die alte `relief_daten`-SHA (5e8fdb51…). Die Neu-Pipeline (p3d17) wurde bewusst nicht neu gebaut, weil sich Hoehen nicht aendern duerfen. Wer sie neu baut, muss diese Pruefung beachten.
- **Nach jedem Relief-Neubau durch L1/L2:** `python3 gen_textur.py vc` und danach `python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py` laufen lassen (idempotent), sonst kommen T1 und die Feinbandkanten zurueck.
- `/tmp/w3` (gemeinsame Node-Werkzeuge fuer `export_gate.sh` und den L1-Lauf) ist beim Box-Neustart gegen 07:45 MEZ verschwunden. P3 laeuft deshalb mit eigenem `/workspace/.p3_node`.
- Die Form-Befunde aus AUSNAHMEN_P3.md gehen an P1.

## Wiederholen
```
git checkout 8e374b0 -- relief_daten.json.gz neu/relief_neu.json.gz
python3 gen_textur.py vc && python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py
sh pruefung/p3_nahbilder/werkzeug/gate_p3.sh
python3 pruefung/p3_nahbilder/werkzeug/sha_p3.py; python3 pruefung/p3_nahbilder/werkzeug/schluessel_p3.py
```
