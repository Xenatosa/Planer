# Materialflaechen relief3d (t53u)
Tabelle: `materialflaechen.csv`. Zellzahlen [R] aus `zellen_relief.csv` (101 808 Zellen, je 1 m²). Kachelgroesse/Aufloesung/UV-Weg sind Vorschlaege [A]. Texturen werden spaeter selbst gemacht; Texturstil ist derzeit nicht Arbeitsthema (t53u).

- skin_slot-Regel (gen_relief.py): steil -> `wand_fels`, sonst `ug_<untergrund>`. Hausteile melden `haus_<typ>` (main.js Klick).
- Gelaende: eine Vertexfarbe aus Splat-Gewichten (gen_relief.py MAT/gew) + triplanar `wand_textur.png` (512 px) und `detail_textur.png` (256 px).
- Objekte (Haeuser, Baeume, Felsen, Zaeune): nur Vertexfarben, keine UVs.
- GLB `dorfmap_relief_z25.glb`: boden hat TEXCOORD_0 (ganze Karte), TEXCOORD_1 gibt es noch nicht [F].
- Schnittstelle Austausch [A]: je skin_slot eine Datei `tex/<slot>_{albedo,normal,rough}.png`, die der Viewer statt der Splatfarbe laedt; die Gewichte als Splatmap (RGBA je 4 Slots) aus gen_relief.py exportieren; Objekte bekommen TEXCOORD_1-Kachel-UV in Weltmetern.
- Kein Fachwerk modelliert [F]. Kies, Nassufer und Weg haben keinen eigenen skin_slot.
