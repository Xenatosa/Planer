# NEUAUFBAU_PLAN – echtes 3D-Relief (t41u)

c20 bleibt unverändert. Es dient nur als Vorbild für Lage, Verhältnisse und Stimmung.

## Messung (Maßstab)
- Wandhöhe = Breite des gemalten Wandbands / 25 px pro m [R]. Messwerte: `pruefung/klippen_messung_t40u.csv`.
  - Nord: 14 m (vorher 8,6 m)
  - Südgrat: 16 m (vorher 7,6 m)
  - Krater: 11 m (vorher 7,7 m)
  - Ostgrat: 12 m (vorher 6,7 m)
- Perspektivfaktor k:
  - Der sichtbare Fels in der Nordwand ist etwa 230 px hoch [S], das Band etwa 350 px [S]. Daraus folgt k ≈ 1,5 gegenüber der alten 8,6-m-Annahme [R].
  - Der See ist 38 × 35 Zellen groß, also fast rund [S]. Der Boden ist darum fast in Draufsicht gemalt. Deshalb sind die Wände in c20 eher verkürzt als zu hoch dargestellt.
  - Spanne: 9 m (k = 1) bis 22 m (Blickwinkel 67°) [R]. Gewählt ist das Band, das in der Mitte dieser Spanne liegt [A].
- Rampen-Abflachung im alten Modell: Die Höhe war über das ganze Band von 7–14 m verteilt, die Wand also nur etwa 50° steil statt 90° [R].

## Schritte
1. `gen_relief.py`:
   - Eigene Höhe je Zelle (Ebene → Höhe).
   - Die Wandband-Zellen gehören zur oberen Ebene. Die Wand steht senkrecht am Wandfuß [F].
   - Hänge werden skaliert.
   - Flussbett ist 1,5 m tief, der See 3 m [A].
   - Ausgabe: OBJ + GLB, Sidecar `zellen_relief.csv` (alle Felder + skin_slot neu abgeleitet), Viewer-Daten.
2. Mesh:
   - Flache Zellflächen mit geglätteten Ecken (nur Nachbarn, die weniger als 2,5 m Unterschied haben).
   - Senkrechte Flächen an jeder Kante mit mehr als 2,5 m Sprung. Sie bekommen eine eigene Wandtextur `wand_textur.png`.
   - Sockel bis −30 m.
3. Objekte:
   - Bäume, Felsen, Findlinge und Häuser stehen auf dem neuen Relief. Ihre Größen bleiben wie in t39u.
   - Overlay (Wege, Brücken, Deko) bleibt eine eigene Ebene.
4. Viewer `relief3d/index.html`:
   - Umschalter alt/neu (alte Daten aus `_alt/welt3d_t39u`).
   - Freie Kamera.
   - Bodenblick mit 1,8-m-Figur am Fuß der Nordwand.
5. Headless-Test, vorher/nachher-Bilder aus gleichen Kameras, alle Bilder selbst ansehen.
6. `modell3d/` (t36u + welt3d t39u) per git mv nach `_alt/`. INDEX aktualisieren. Push.

## Was fehlt / offen
- Überhänge: nicht gebaut. Die Wände sind senkrecht, die Schneekante wird nur über die Textur angedeutet.
- Krater-Innenhöhe (+1 m) und Gipfel (14 m) sind [A].
- Die Wandlinie folgt dem Zellraster. Dadurch hat sie 1-m-Treppen im Grundriss.
- Fabian muss entscheiden [F]:
  - ob die gewählten Wandhöhen passen,
  - ob die Wand am Fuß stehen soll (Plateau reicht bis zum Bandende) oder in der Bandmitte.
