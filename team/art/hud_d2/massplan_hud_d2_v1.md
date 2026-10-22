# Maßplan Dorf-HUD D2 „Obsidian & Glut“ v1

**Stand:** 22.10.2026 · Grundlage: Entscheidung Fabian 22.10.2026 (HUD v5/v5.7 gestrichen, Dorf-HUD neu in D2). Vorlage: `team/art/ui-kit/menus_v3/vorlage_D2.md`, Bausteine `vorlage_D2_export/` (+ `manifest_9slice.json`), Dock A in D2-Tönung (warmes Dunkelbraun, Platte Glut-Orange, kein Blau, keine Gold-Kerbe).
**Abnahme:** offen (Art Director + Kritiker, Modern-Gate).

Dateien:
- `massplan_hud_d2_v1.png` – Maßplan 1080×1920 (Raster 10/40, Safe Areas, alle Boxen mit ID, Hitboxen gestrichelt) + Legende mit Wertetabelle und D2-Farbfeldern (Gesamtbild 2200×1920).
- `massplan_hud_d2_v1_bloecke.png` – echte `d2_*`-Sprites an diesen Positionen (9-Slice laut Manifest), über abgedunkeltem `e1_village_bg_stilA_v2` (Farbe 60 %, Helligkeit 55 %). Leere Icons = neutraler Platzhalter „Icon neu D2“.
- `massplan_hud_d2_v1_elemente.json` – Maschinenlesbare Werte (Quelle dieser Tabelle).
- `_src/massplan_hud_d2_v1.py` – erzeugt alles (nur PIL, 0 $, keine KI-Bilder). Enthält eine Prüfung (Touch ≥ 96, Safe Area, Überlappung der Hitboxen und sichtbaren Boxen): **0 Befunde**.

Nicht verwendet: alles aus `team/art/_alt/` (HUD v5/v5.7, `hud_c_ico_*`, Stil-C-Holzbalken, `HudV5NumberFormat`).

## Rahmen
| Wert | px | Begründung |
|---|---|---|
| Canvas | 1080×1920 | Referenz-Canvas D2, Scale With Screen Size, Match 0,5 |
| Safe-Top (Notch) | 0–90 | Top-Anker zählen ab y 90 |
| Gestenzone | 1872–1920 (48) | keine Hitbox reicht hinein; Dock-Grund füllt sie (`dock.bottom` #080604), Gestenleiste 300×10 bei 390/1896 |
| Außenrand | 28 links/rechts | D2-Raster (nutzbar 1024) |
| Touch-Minimum | 96 (Fabian); Ziel D2 120 | Alle Knöpfe 120 sichtbar; Pills 80 sichtbar mit 96 Hitbox; Quest-Icon 96 (≥ 70) |
| Freiraum über Dock | Quest-Leiste endet 1660, Platte beginnt 1682 | D2: nichts unter 1676 außer Dock |

## Elemente (alle px, Ursprung oben links)
| ID | Element | x | y | w | h | Hitbox (wenn ≠ sichtbar) | Sprite / Text | Hinweis |
|---|---|---|---|---|---|---|---|---|
| A1 | Avatar (Portraet) | 28 | 98 | 128 | 128 | 28,90 128×144 | d2_panel_frame (9-Slice) | Portraet 104 innen (12 px), antippbar -> Profil |
| A2 | Level-Badge | 92 | 182 | 60 | 40 | – | d2_badge_stufe | innen rechts unten 4/4, Lilita 26 |
| R1 | Pill Holz | 172 | 98 | 280 | 80 | 172,90 280×96 | d2_pill_ressource | Icon 64 bei x+8/y+8, Zahl Lilita 40 ab x+84 |
| R2 | Pill Stein | 472 | 98 | 280 | 80 | 472,90 280×96 | d2_pill_ressource | Icon 64 bei x+8/y+8, Zahl Lilita 40 ab x+84 |
| R3 | Pill Nahrung | 772 | 98 | 280 | 80 | 772,90 280×96 | d2_pill_ressource | Icon 64 bei x+8/y+8, Zahl Lilita 40 ab x+84 |
| R4 | Pill Gold | 172 | 194 | 280 | 80 | 172,186 280×96 | d2_pill_ressource |  |
| R5 | Pill Kristalle | 472 | 194 | 280 | 80 | 472,186 280×96 | d2_pill_ressource |  |
| R6 | Plus Kristalle -> Shop | 764 | 194 | 80 | 80 | 754,186 120×96 | d2_btn_plus_pill + d2_ico_plus | sichtbar 80 (= Pill-Hoehe), Hitbox 120x96 (beginnt 2 px hinter Kristall-Pill) |
| S1 | Seitenknopf Events | 932 | 316 | 120 | 120 | 932,316 120×152 | d2_btn_quadrat_normal | Icon 80 bei x+20/y+20; Hitbox inkl. Label 120x152 |
| S1L | Label Events | 932 | 440 | 120 | 28 | – | Text Baloo 800 22 | Text #EADFC6, Kontur 3 px #000 |
| S1B | Badge Events | 1000 | 320 | 48 | 38 | – | d2_badge_zaehler | innen rechts oben 4/4 |
| S2 | Seitenknopf Gratis / Login | 932 | 488 | 120 | 120 | 932,488 120×152 | d2_btn_quadrat_normal | Icon 80 bei x+20/y+20; Hitbox inkl. Label 120x152 |
| S2L | Label Gratis | 932 | 612 | 120 | 28 | – | Text Baloo 800 22 | Text #EADFC6, Kontur 3 px #000 |
| S2B | Badge Gratis | 1000 | 492 | 48 | 38 | – | d2_badge_zaehler | innen rechts oben 4/4 |
| S3 | Seitenknopf Shop | 932 | 660 | 120 | 120 | 932,660 120×152 | d2_btn_quadrat_normal | Icon 80 bei x+20/y+20; Hitbox inkl. Label 120x152 |
| S3L | Label Shop | 932 | 784 | 120 | 28 | – | Text Baloo 800 22 | Text #EADFC6, Kontur 3 px #000 |
| S4 | Seitenknopf Mail / Mehr | 932 | 832 | 120 | 120 | 932,832 120×152 | d2_btn_quadrat_normal | Icon 80 bei x+20/y+20; Hitbox inkl. Label 120x152 |
| S4L | Label Mail | 932 | 956 | 120 | 28 | – | Text Baloo 800 22 | Text #EADFC6, Kontur 3 px #000 |
| S4B | Badge Mail | 1000 | 836 | 48 | 38 | – | d2_badge_zaehler | innen rechts oben 4/4 |
| V1 | Event-Platzhalter (Banner) | 28 | 316 | 312 | 168 | – | d2_panel_frame_glut | Icon 96 bei x+16/y+16, 'EVENT' + Countdown Lilita 30 rechts |
| C1 | Chat-Knopf | 28 | 1396 | 120 | 120 | – | d2_btn_quadrat_normal | Icon 80 innen |
| C2 | Badge Chat (ungelesen) | 96 | 1400 | 48 | 38 | – | d2_badge_zaehler |  |
| Q1 | Quest-Leiste | 28 | 1536 | 720 | 124 | – | d2_panel_frame (9-Slice) | ganze Leiste antippbar; Ende 1660 (16 px vor Platten-Oberkante 1682) |
| Q2 | Quest-Icon | 42 | 1550 | 96 | 96 | – | Icon neu D2 | >= 70 gefordert, 96 gewaehlt |
| Q3 | Quest-Text | 152 | 1552 | 452 | 40 | – | Text Lilita 30 | 1 Zeile, Ellipse '...' |
| Q4 | Quest-Fortschritt | 152 | 1608 | 452 | 22 | – | d2_bar_bg + d2_bar_fill_glut |  |
| Q5 | Quest-Zaehler 3/5 | 616 | 1596 | 116 | 44 | – | Text Lilita 32 | rechtsbuendig |
| D0 | Dock-Hintergrund | 0 | 1708 | 1080 | 212 | – | d2_dock_bg (9-Slice 4/8/4/8) | bottom-anchored, deckt Gestenzone mit |
| T1 | Tab Dorf | 0 | 1708 | 216 | 164 | – |  | Hitbox 216x164 (bis Gestenzone) |
| T1P | Aktive Platte Dorf | 12 | 1682 | 192 | 196 | – | d2_dock_platte_aktiv | Overlay, ragt 26 hoch |
| T1I | Icon Dorf (aktiv) | 38 | 1686 | 140 | 124 | – | Icon neu D2 |  |
| T1T | Label Dorf (aktiv) | 12 | 1812 | 192 | 44 | – | Lilita 36 #FFF3D6 |  |
| T1S | Indikator | 78 | 1860 | 60 | 8 | – | d2_dock_indikator |  |
| T2 | Tab Armee | 216 | 1708 | 216 | 164 | – |  | Hitbox 216x164 (bis Gestenzone) |
| T2I | Icon Armee | 276 | 1722 | 96 | 88 | – | Icon neu D2 |  |
| T2T | Label Armee | 228 | 1814 | 192 | 38 | – | Lilita 30 #BFAE8E |  |
| T3 | Tab Bauen | 432 | 1708 | 216 | 164 | – |  | Hitbox 216x164 (bis Gestenzone) |
| T3I | Icon Bauen | 492 | 1722 | 96 | 88 | – | Icon neu D2 |  |
| T3T | Label Bauen | 444 | 1814 | 192 | 38 | – | Lilita 30 #BFAE8E |  |
| T4 | Tab Helden | 648 | 1708 | 216 | 164 | – |  | Hitbox 216x164 (bis Gestenzone) |
| T4I | Icon Helden | 708 | 1722 | 96 | 88 | – | Icon neu D2 |  |
| T4T | Label Helden | 660 | 1814 | 192 | 38 | – | Lilita 30 #BFAE8E |  |
| T5 | Tab Karte | 864 | 1708 | 216 | 164 | – |  | Hitbox 216x164 (bis Gestenzone) |
| T5I | Icon Karte | 924 | 1722 | 96 | 88 | – | Icon neu D2 |  |
| T5T | Label Karte | 876 | 1814 | 192 | 38 | – | Lilita 30 #BFAE8E |  |
| T4B | Badge Helden | 804 | 1716 | 48 | 38 | – | d2_badge_zaehler | innen im Tab |
| G1 | Gestenleiste (System) | 390 | 1896 | 300 | 10 | – | System | nicht antippbar |

## Begründung (kurz)
- **Top-Leiste zweizeilig (90–282):** 5 Pills à 280 + Plus passen nicht neben den Avatar in eine Zeile (Pillbreite D2 = 280, Zahl Lilita 40 ab x+84). Zeile 1 Produktions-Rohstoffe Holz/Stein/Nahrung (172/472/772, Abstand 20, rechts bündig auf 1052), Zeile 2 Währungen Gold/Kristalle + Plus. Zeilenabstand 16 → Pill-Hitboxen 280×96 stoßen ohne Überlappung aneinander.
- **Plus nur an Kristallen** (D2-Regel): sichtbar 80×80, Hitbox 120×96 (x 754–874), keine Überlappung mit der Kristall-Pill (endet 752).
- **Avatar 128×128** (≥ 96) mit Level-Badge innen rechts unten (4/4, `d2_badge_stufe`), Hitbox 128×144 bis zur Zeilenmitte.
- **Seitenleiste rechts** x 932–1052, Raster 172 ab y 316: Knopf 120×120 (`d2_btn_quadrat_normal`), Label Baloo 800 22 darunter (28 hoch), Hitbox inkl. Label 120×152, 20 px Luft dazwischen. Zähler-Badges innen rechts oben 4/4 (Regel B).
- **Event-Platzhalter** links oben 28/316 312×168 (`d2_panel_frame_glut`), damit die Dorfmitte (x 352–920, y 296–1380) frei bleibt.
- **Chat** links 28/1396 120×120 mit Badge, **Quest-Leiste** 28/1536 720×124 links über dem Dock (wie Dock A), Icon 96, Text Lilita 30, Balken 452×22, Zähler „3/5“. Endet 1660 (16 px vor der aktiven Platte).
- **Dock** exakt nach D2/Dock A: 1080×212 ab y 1708, 5 Tabs à 216 (Dorf, Armee, Bauen, Helden, Karte); Hitbox je 216×164 (bis 1872, also vor der Gestenzone). Aktiv „Dorf“: Platte 192×196 bei 12/1682 (ragt 26), Icon 140×124, Label Lilita 36 #FFF3D6, Indikator 60×8 bei 78/1860. Inaktiv: Icon 96×88 bei x+60/1722, Label Lilita 30 #BFAE8E bei 1814. Badge Helden 48×38 innen.

## Farben
Alle aus `vorlage_D2.md` Abschnitt 3 inkl. Dock-Tönung D2 (im Maßplan als Farbfelder): bg.base #120E0C, panel #2C201A→#120D0B, line.bronze #C98A4A, line.bronze.light #C9A96E, line.muted #8A7656, line.dark #7A664E, text.counter #A89674, glut #FF8A2A, glut.deep #E0601A, glut.light #FFB15A, glut.text #FFD9A8, glut.plus #FFD27A, text.main #F3E7CF, text.muted #B9A988, text.bone #EADFC6, ink #0B0908, ink.brown #2A1206, accent.moon #3FE0D0, state.plus #9BE37A, state.missing #FF6A5A, dock.bottom #080604, Dock-Label #BFAE8E / #FFF3D6, aktive Platte rgb(255,150,60).

## Neue D2-Icons (zu erstellen)
| Icon (Vorschlag Dateiname) | Größe Export | Einsatz |
|---|---|---|
| `d2_ico_res_holz` | 128 (Einsatz 64) | Pill Holz |
| `d2_ico_res_stein` | 128 (64) | Pill Stein |
| `d2_ico_res_nahrung` | 128 (64) | Pill Nahrung |
| `d2_ico_res_gold` | 128 (64) | Pill Gold |
| `d2_ico_res_kristall` | 128 (64) | Pill Kristalle |
| `d2_ico_side_events` | 160 (80) | Seitenknopf Events |
| `d2_ico_side_gratis` | 160 (80) | Gratis / Login-Belohnung |
| `d2_ico_side_shop` | 160 (80) | Shop |
| `d2_ico_side_mehr` | 160 (80) | Mail / Mehr |
| `d2_ico_chat` | 160 (80) | Chat |
| `d2_ico_quest` | 192 (96) | Quest-Leiste |
| `d2_ico_event_platzhalter` | 192 (96) | Event-Banner (generisch) |
| `d2_ico_dock_dorf` / `_armee` / `_bauen` / `_helden` / `_karte` | 280×248 (aktiv 140×124, inaktiv 96×88) | Dock |
| `d2_portrait_rahmen` (optional) | 128 | runde Porträtmaske im Avatar |
Vorhanden und genutzt: `d2_ico_plus` (Kristall-Plus), alle Rahmen-/Pill-/Badge-/Dock-Sprites.

## Offene Fragen
1. **Zahlenformat** neu (HudV5NumberFormat gestrichen): Vorschlag Tausenderpunkt bis 99.999, danach „123,4K“ / „1,2 Mio“? Bei 5+ Ziffern bleibt die 280er Pill knapp (Platz ab x+84: 184 px ≈ 6 Zeichen Lilita 40).
2. **Zwei Zeilen Top-Leiste OK?** Alternative: Holz/Stein/Nahrung als schmale Pills 200 (Icon 64 + 4–5 Ziffern) in einer Zeile + Gold/Kristalle – dann aber nur 5 Ziffern.
3. **Seitenknöpfe:** Labels unter dem Knopf (außerhalb der Box) oder ohne Label? Mail und Mehr getrennt oder zusammen (hier zusammen „Mehr“ mit Mail-Badge)?
4. **Touch 96 vs. D2 120:** Pill-Hitbox nur 96 hoch (zwei Zeilen); alle Knöpfe 120. Reicht 96 für die Pills?
5. **Event-Platzhalter:** links oben (hier) oder unter der Seitenleiste rechts? Mehrere Events gleichzeitig (Stapel/Karussell)?
6. **Chat-Badge vs. Notification-Badge:** eigener Benachrichtigungs-Knopf oder nur Badges an Mail/Events?
7. Dorf-Top-Leiste galt laut vorlage_D2.md als „Paket F6, unverändert“ – durch Entscheidung 22.10. überholt; Zeile in vorlage_D2.md bei Gelegenheit nachziehen.
