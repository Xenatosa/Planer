
## Runde O6 (Stand 01.11.2026, 21:10)
- G1 Wasserrand fluss_7/fluss_9: V3 Konturwasser (Marching Triangles, 0,25 m, gegen gezeichneten Boden) gebaut, Zaehne bleiben sichtbar (o6c/fluss_7_c.png). Nur noch mit ?wneu=1. Nach 2 Versuchen (clip, Kontur) offen; Verdacht: Stufen stammen aus 1-m-Buckets von __hSurf oder aus der Bodenfarbe selbst.
- G2 Rampen: Unterteilung 0,4 m, kein Rand-Fade an Gabeln, Kehren breiter, hellere Farbe. rampe_13: weisser Riss weg, kleiner dunkler Schlitz bleibt. rampe_4: Band bleibt gerade und dunkel (teilweise besser).
- G3 wand_0_24: Sand-Unterdrueckung auf Steilflaechen getestet, Bild unveraendert. Die hellen Keile unten rechts sind sehr wahrscheinlich Baumstaemme vor der Kamera, kein Bodenfehler. Aenderung zurueckgenommen.
- G4 fluss_3: ?vc=1 behebt Saegezahn am Schneerand nicht, bleibt opt-in. Offen.
- G5: Ladezeit headless 4,1 s, keine Fehler. HTML: /workspace/dorfmap_3d_runde_O6.html.

## Runde O7 H1/H2 (01.11.2026)
- H1 bestaetigt: Spiegel (WR) nur auf nassen Zellen definiert; Konturnetz (wneu) lief zudem nur ueber Zellen mit nassem Nachbarn -> Kante = Zellmaske. Debugbild pruefung/o7/o7_dbg_fluss7.png (links alt, rechts ausgedehnt; blau Tiefe>0, rot Boden ueber Spiegel, gelb |d|<2 cm).
- H2 gebaut (Spiegel 4 m ausserhalb glatt fortgesetzt, Relaxation, Kontur gegen gezeichneten Boden, Alpha 0-20 cm, ?wneu=1). Die Nulllinie bleibt aber gestuft: der GEZEICHNETE Boden springt an der Maskengrenze um ca. 0,6-0,8 m (letzte nasse Zelle meist exakt 0,40 m tief, 0,5 m daneben bereits -0,2..-0,4). Das Flussbett ist zellweise eingeschnitten, die Ufer sind senkrechte Stufen.
- H3 (max. 10 cm Glaettung) reicht dafuer nicht. Abbruch hier, Entscheidung noetig.
