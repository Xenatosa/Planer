# 3D-Geländemodell Dorfmap c20 (t34u)
- `gen_modell3d.py` erzeugt alles aus `../raster_c20_z25_zellen.csv` und c20 (c20 bleibt unverändert).
- `dorfmap_c20_z25.obj` + `.mtl` + `textur_c20_8px.jpg` (c20 verkleinert auf 8 px/m). Einheit Meter, 1 Zelle = 1 m, y = oben. 150 146 Ecken, 139 745 Vierecke [R].
- Jede Zelle ist ein flaches Quadrat in ihrer Höhe; Höhensprünge sind senkrechte Wände.
- Renders (Punkt-Render mit z-Buffer, Überhöhung ×3 [F]): render_schraeg_suedost, render_von_oben, render_sued, render_nord, render_ost, render_west.

## Höhen – alles Annahmen [A]
- SENKE 0 m (Bezug), PLATEAU_NORD +8,6, GIPFEL +7,7, OSTPLATEAU +6,7, TAL_SUED −7,6, KRATER 0.
- HANG: glatt interpoliert zwischen den Stufen (−7,1 bis +6,2). SIMS: Mittel der Umgebung.
- Wandzellen bekommen die Höhe der nächsten freien Zelle → die Stufe liegt in der Wandmitte [A]. Wandhöhen 8,6 / 7,6 / 6,7 m stammen aus der Schätzung KL_M und Verhältnissen, nicht gemessen.
- Wasser hat keine eigene Tiefe im Modell (Fluss liegt auf Talhöhe).

## Bekannte Mängel (angesehen)
- Wandflächen zeigen senkrechte Streifen (Textur wird nach unten gezogen).
- Nord-Ansicht: unten Streifen-Artefakt und einzelne dünne Spitzen.
- Kein echter Raytracer, keine Prüfung in Blender o. ä.
