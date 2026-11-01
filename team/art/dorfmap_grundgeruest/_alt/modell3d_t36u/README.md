# modell3d – 3D-Modell der Dorfkarte (t36u)

Quelle: Raster `../raster_c20_z25_zellen.csv` (336×303 Zellen) + Bild c20 (unverändert).
Neu bauen: `python3 gen_modell3d.py` → danach `python3 pruef_eigenschaften.py`, `python3 render_modell3d.py`.

## Dateien
| Datei | Inhalt |
|---|---|
| dorfmap_c20_z25.glb | Hauptmodell (glTF 2.0), 11 Meshes nach `untergrund` |
| dorfmap_c20_z25.obj/.mtl | Gleiche Geometrie, OBJ-Gruppen, nur c20-UV (kein Kachel-UV!) |
| textur_c20_8px.jpg | c20 verkleinert, 8 px pro Zelle (Vorschau-Textur) |
| zellen_eigenschaften.csv | Sidecar: zell_id + alle Rasterfelder + modell_hoehe_m, modell_abw_m, modell_gruppe |
| pruefung_mesh.json / pruefung_eigenschaften.json | Automatische Prüfungen |
| r1…r8_*.png | 8 Ansichten (eigener Renderer) |
| r9_skin_test_schnee.png + skin_test_kachel.png | Skin-Beispiel |
| abweichungen_modell_vs_c20.png, ABWEICHUNGEN_C20.md | Wo das Modell von c20 abweicht [F] |

## Einheiten und Achsen [F]
1 Einheit = 1 m = 1 Zelle = 25 px c20. x = cx (Osten), y = oben, z = cy (Süden). Ursprung = Nordwest-Ecke, Höhe 0.

## Daten am Modell
- `zell_id = cy*336 + cx` (Sockel = −1). Jede Fläche gehört zu genau einer Zelle (eigene 4 Ecken).
- Vertex-Attribute je Primitive: POSITION, NORMAL (geglättet), TEXCOORD_0 = c20-UV, TEXCOORD_1 = 0..1 je Zelle (Kachel-UV), `_ZELL_ID` (float).
- glTF `extras`: Feldliste, Name der Sidecar-Datei, Achsen.
- Alle Eigenschaften: per `zell_id` in `zellen_eigenschaften.csv` nachschlagen. Das Raster bleibt die Quelle.

## Skin auflegen
1. Mesh/Material der Gruppe wählen (z. B. `SCHNEE` → Material `Gelaende_SCHNEE`).
2. Basis-Textur durch die Kachel ersetzen und **TEXCOORD_1** benutzen (Unity: zweiter UV-Kanal, im Shader UV1; Wrap = Repeat).
3. Beispiel: `python3 render_modell3d.py SCHNEE skin_test_kachel.png r9_skin_test_schnee.png` → jede Schnee-Zelle zeigt eine Kachel.
Pro Zelle andere Kachel: im Shader per `_ZELL_ID` oder per Sidecar-Feld auswählen (Atlas).

## Geprüft
Mesh: 220 840 Dreiecke, dicht (ohne Wasser) Euler 2, 0 Umklappungen, 0 entartet, 0 Spitzen, steilster freier Hang 54,3°.
Eigenschaften: 0 Abweichungen bei 101 808 Zellen.

## Nicht geprüft
Kein glTF-Validator, kein Test in Unity/Blender. Nur eigener Renderer. OBJ ohne Kachel-UV.
Wand-Rückseiten tragen die Aufsicht-Textur von c20 (sieht von hinten falsch aus, z. B. Gipfel in r2/r7).
