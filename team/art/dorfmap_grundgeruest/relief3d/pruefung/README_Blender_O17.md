# Dorfmap Epodarien – Stand Runde O17 in Blender öffnen

**Kurz: Ja.** `dorfmap_O17.glb` lässt sich in Blender über *Datei → Importieren → glTF 2.0 (.glb/.gltf)* öffnen.
Getestet am 02.11.2026 mit **Blender 4.2.3 LTS** (headless): 14 Objekte importiert, alle mit Farbattribut `Color`, Testbild `test_render_cycles.png` gerendert.

## Was drin ist
Die Datei kommt direkt aus der Viewer-Szene (`index.html?lod=0`, volle Auflösung) und hat dieselben Dreiecke und Anzeigehöhen wie der Viewer O17.

| Objekt | Inhalt | Dreiecke |
|---|---|---|
| gelaende_grobnetz | Gelände 0,5-m-Netz, Anzeigehöhen (GB), ohne Bandzellen | 674 566 |
| gelaende_feinband_waende | Feinrelief 0,25 m: Felswände, Wandfuß, Schutt | 654 720 |
| gelaende_rand_sockel / gelaende_bodenplatte | Kartenrand und Unterseite | 10 226 |
| wasser | Flüsse und Seen (Wasserspiegel) | 224 637 |
| baeume_1…5 | 1460 Bäume (Stamm, Kronen, Schnee) | 263 384 |
| felsen_1 | Grasbüschel (Viewer-Gruppe „felsen“) | 27 349 |
| felsen_2…4 | Steine und Geröll | 247 500 |

Insgesamt 2,10 Mio. Dreiecke, 63 MB. Die genaue Liste steht in `dorfmap_O17_inhalt.json`.

**Nicht enthalten:** Gebäude, Wege-Overlay, Brücken-Overlay, Spielfigur, Himmel, Fernberge.

## Einheiten und Achsen
- 1 Blender-Einheit = 1 m. Eine Spielzelle ist 1 m × 1 m, die Karte ist 336 m × 303 m.
- glTF nutzt Y als Höhe. Blender wandelt beim Import automatisch auf Z oben um. Dadurch liegt die Karte bei X 0…336 und Y 0…−303, die Höhe reicht von −34 m (Sockel) bis +30,5 m.
- Die Zellkoordinate (cx, cy) entspricht in Blender X = cx + 0,5 und Y = −(cy + 0,5).

## Farben ansehen
Die Datei verwendet keine Texturen. Alle Farben sind Vertexfarben (Attribut `Color`).
- **Schnell:** Viewport-Shading *Solid* wählen, dann im Shading-Menü (Pfeil oben rechts) *Color → Attribute* einstellen.
- **Zum Rendern:** Im Material einen Knoten *Color Attribute* an *Base Color* hängen. `blender_test_render.py` erledigt das automatisch:
  `blender -b -P blender_test_render.py -- dorfmap_O17.glb bild.png CYCLES`

## Unterschiede zum Viewer
- Der Viewer berechnet Fels, Schnee, das neue Steinband (O17), Rauschen und Wasserglanz erst **im Shader**. In der GLB stehen nur die Grundfarben pro Ecke. Deshalb wirkt sie in Blender heller und schneelastiger. Felswände sind nur so grau, wie es ihre Eckfarbe vorgibt.
- Die Wasserfarbe ist ohne Transparenz und ohne Bewegung.
- Die Instanzen (Bäume, Steine) wurden zu normalen Netzen zusammengefügt, also ein Objekt pro Viewer-Variante.
- Die Datei entspricht der Desktop-Stufe lod=0, nicht der Handy-Stufe lod=2.

## Alte Datei `relief3d/dorfmap_relief_z25.glb`
Sie stammt aus `gen_relief.py` und enthält **nur das Zellgrundgerüst**: Höhen G statt der Anzeigehöhen GB, ohne Feinband und Felswände, ohne Wasser, Bäume und Steine. Sie war zum Abgleich der Zellen gedacht (t42u). Sie bleibt unverändert, entspricht aber nicht dem Bild im Viewer.

## Neu erzeugen
```
cd relief3d && python3 baue_html.py
NODE_PATH=/tmp/w3/node_modules OUT=/tmp/o17_dump.json node pruefung/blender_dump_o17.js
python3 pruefung/blender_paket_o17.py /tmp/o17_dump.json /workspace/dorfmap_blender_O17/dorfmap_O17.glb
```
