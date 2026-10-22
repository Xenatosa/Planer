# Massplan Dorf-HUD D2 „Obsidian & Glut“ – v2

Stand 22.10.2026 · basiert auf v1 (`39d5148`) · Feedback Fabian: Top-Leiste nur 3 Währungen, übrige Ressourcen in einer Liste hinter dem Knopf „Ressourcen“.
Kosten 0 $ (Python/PIL, nur D2-Bausteine aus `manifest_9slice.json`). HUD v5 und `team/art/_alt/` werden nicht verwendet.

## Dateien
- `massplan_hud_d2_v2.png`: Massplan 2200x1920 (Canvas plus Legende)
- `massplan_hud_d2_v2_bloecke.png`: D2-Blöcke, Liste zu
- `massplan_hud_d2_v2_bloecke_liste.png`: D2-Blöcke, Liste offen (mit Scrim)
- `massplan_hud_d2_v2_elemente.json`: alle Werte
- `_src/massplan_hud_d2_v2.py`: Generator mit Selbstprüfung (Ergebnis: 0 Befunde)

## Änderungen gegenüber v1
1. **Währungszeile** (eine Zeile neben dem Avatar, y 98, h 80, Hitbox y 90–186):
   - Zeitkristalle 172/98 248x80
   - Plus → Shop 432/98 80x80, Hitbox 422,90 100x96
   - Wissen 532/98 248x80
   - Gold (Muscheln) 800/98 248x80, endet bei 1048 (Rand 32)
   - Abstand zwischen den Pills 20 px. Die Zahl (Lilita 40) beginnt bei x+84 und hat 152 px Platz für maximal 6 Zeichen, z. B. „45.600“.
2. **Holz, Stein und Nahrung** sind aus der Top-Leiste entfernt.
3. **Knopf „Ressourcen“** sitzt direkt unter der Währungszeile, linksbündig mit der ersten Pill:
   - Position 172/194, Größe 300x120 (Knopfhöhe 120). Sprite `d2_btn_sekundaer_normal`, im offenen Zustand `d2_btn_filter_aktiv`.
   - Inhalt: Icon 64 bei x+16, Text Baloo 800 28 ab x+92 (Textbreite 148, endet bei x+241), Chevron 28 bei x+256 (zeigt nach unten, wenn zu, nach oben, wenn offen).
4. **Event-Banner V1** rückt von y 316 auf **y 340**, weil der Knopf bis y 314 reicht. Die Seitenleiste bleibt unverändert.
5. **Ressourcen-Liste (offen)**, Sprite `d2_dropdown_liste`:
   - Position 172/326, Größe 600x448, also bis y 774. Damit bleiben über 900 px Abstand zum Dock (Freiraum-Linie 1676).
   - Kopf „LAGER“ (Baloo 22, text.muted)
   - 3 Zeilen à 120 px, jeweils über die ganze Breite antippbar (576x120):
     - Icon 72
     - Name Baloo 800 28
     - Lagerbalken 240x22 (`d2_bar_bg` + `d2_bar_fill_glut`)
     - Menge Lilita 36, rechtsbündig
     - „/ Lager“ Baloo 22 #A89674; wenn das Lager voll ist, „voll“ in state.missing #FF6A5A
   - Zwischen den Zeilen steht `d2_dropdown_trenner`.
   - Ein Scrim (Alpha 110) liegt nur über der Welt, das Dock bleibt frei. Ein Tipp auf den Scrim oder auf den Knopf schließt die Liste.
   - Die Liste überdeckt das Event-Banner absichtlich, weil sie modal ist. Die Prüfung nimmt dieses Paar aus.
6. **Beschriftungen im Plan:** Die Tags Q1 und L0 stehen jetzt unten rechts in ihrer Box (vorher berührte Q1 den Tag Q2). V1 steht unten links, die Zeilen L1–L3 ebenfalls unten links.

## Selbstprüfung
Das Skript prüft automatisch:
- Touch ≥ 96
- Safe Top 90
- Dock und Gestenzone 48
- Überlappung von Hitboxen
- Überlappung sichtbarer Boxen
- Liste oberhalb des Dock

Ergebnis: **0 Befunde**.

Zusätzlich habe ich die PNGs in Originalgröße und als 200-%-Ausschnitte angesehen (Top-Leiste, Liste, Quest/Dock).

## Werte (alle px, Canvas 1080x1920)
| ID | Element | x | y | w | h | Hitbox | Sprite/Text |
|---|---|---|---|---|---|---|---|
| A1 | Avatar (Portraet) | 28 | 98 | 128 | 128 | 28,90 128x144 | d2_panel_frame (9-Slice) |
| A2 | Level-Badge | 92 | 182 | 60 | 40 |  | d2_badge_stufe |
| R1 | Pill Zeitkristalle | 172 | 98 | 248 | 80 | 172,90 248x96 | d2_pill_ressource |
| R2 | Plus Zeitkristalle -> Shop | 432 | 98 | 80 | 80 | 422,90 100x96 | d2_btn_plus_pill + d2_ico_plus |
| R3 | Pill Wissen | 532 | 98 | 248 | 80 | 532,90 248x96 | d2_pill_ressource |
| R4 | Pill Gold (Muscheln) | 800 | 98 | 248 | 80 | 800,90 248x96 | d2_pill_ressource |
| RB | Knopf Ressourcen | 172 | 194 | 300 | 120 |  | d2_btn_sekundaer_normal / _filter_aktiv (offen) |
| RBI | Icon Ressourcen | 188 | 222 | 64 | 64 |  | Icon neu D2 |
| RBC | Chevron auf/zu | 428 | 240 | 28 | 28 |  | Icon neu D2 |
| L0 | Ressourcen-Liste (offen) | 172 | 326 | 600 | 448 |  | d2_dropdown_liste (9-Slice 72) |
| L0H | Kopf 'LAGER' | 196 | 350 | 552 | 32 |  | Text Baloo 700 22, Sperrung 3 |
| L1 | Zeile Holz | 184 | 390 | 576 | 120 |  | Zeile (ganze Zeile antippbar) |
| L1I | Icon Holz | 196 | 414 | 72 | 72 |  | Icon neu D2 |
| L1N | Name Holz | 284 | 408 | 240 | 40 |  | Text Baloo 800 28 |
| L1B | Lagerbalken Holz | 284 | 464 | 240 | 22 |  | d2_bar_bg + d2_bar_fill_glut |
| L1W | Menge Holz | 540 | 404 | 196 | 48 |  | Text Lilita 36 rechtsb. |
| L1C | Lager Holz | 540 | 456 | 196 | 34 |  | Text Baloo 700 22 rechtsb. |
| L2 | Zeile Stein | 184 | 510 | 576 | 120 |  | Zeile (ganze Zeile antippbar) |
| L2I | Icon Stein | 196 | 534 | 72 | 72 |  | Icon neu D2 |
| L2N | Name Stein | 284 | 528 | 240 | 40 |  | Text Baloo 800 28 |
| L2B | Lagerbalken Stein | 284 | 584 | 240 | 22 |  | d2_bar_bg + d2_bar_fill_glut |
| L2W | Menge Stein | 540 | 524 | 196 | 48 |  | Text Lilita 36 rechtsb. |
| L2C | Lager Stein | 540 | 576 | 196 | 34 |  | Text Baloo 700 22 rechtsb. |
| L3 | Zeile Nahrung | 184 | 630 | 576 | 120 |  | Zeile (ganze Zeile antippbar) |
| L3I | Icon Nahrung | 196 | 654 | 72 | 72 |  | Icon neu D2 |
| L3N | Name Nahrung | 284 | 648 | 240 | 40 |  | Text Baloo 800 28 |
| L3B | Lagerbalken Nahrung | 284 | 704 | 240 | 22 |  | d2_bar_bg + d2_bar_fill_glut |
| L3W | Menge Nahrung | 540 | 644 | 196 | 48 |  | Text Lilita 36 rechtsb. |
| L3C | Lager Nahrung | 540 | 696 | 196 | 34 |  | Text Baloo 700 22 rechtsb. |
| S1 | Seitenknopf Events | 932 | 316 | 120 | 120 | 932,316 120x152 | d2_btn_quadrat_normal |
| S1L | Label Events | 932 | 440 | 120 | 28 |  | Text Baloo 800 22 |
| S1B | Badge Events | 1000 | 320 | 48 | 38 |  | d2_badge_zaehler |
| S2 | Seitenknopf Gratis / Login | 932 | 488 | 120 | 120 | 932,488 120x152 | d2_btn_quadrat_normal |
| S2L | Label Gratis | 932 | 612 | 120 | 28 |  | Text Baloo 800 22 |
| S2B | Badge Gratis | 1000 | 492 | 48 | 38 |  | d2_badge_zaehler |
| S3 | Seitenknopf Shop | 932 | 660 | 120 | 120 | 932,660 120x152 | d2_btn_quadrat_normal |
| S3L | Label Shop | 932 | 784 | 120 | 28 |  | Text Baloo 800 22 |
| S4 | Seitenknopf Mail / Mehr | 932 | 832 | 120 | 120 | 932,832 120x152 | d2_btn_quadrat_normal |
| S4L | Label Mail | 932 | 956 | 120 | 28 |  | Text Baloo 800 22 |
| S4B | Badge Mail | 1000 | 836 | 48 | 38 |  | d2_badge_zaehler |
| V1 | Event-Platzhalter (Banner) | 28 | 340 | 312 | 168 |  | d2_panel_frame_glut |
| C1 | Chat-Knopf | 28 | 1396 | 120 | 120 |  | d2_btn_quadrat_normal |
| C2 | Badge Chat (ungelesen) | 96 | 1400 | 48 | 38 |  | d2_badge_zaehler |
| Q1 | Quest-Leiste | 28 | 1536 | 720 | 124 |  | d2_panel_frame (9-Slice) |
| Q2 | Quest-Icon | 42 | 1550 | 96 | 96 |  | Icon neu D2 |
| Q3 | Quest-Text | 152 | 1552 | 452 | 40 |  | Text Lilita 30 |
| Q4 | Quest-Fortschritt | 152 | 1608 | 452 | 22 |  | d2_bar_bg + d2_bar_fill_glut |
| Q5 | Quest-Zaehler 3/5 | 616 | 1596 | 116 | 44 |  | Text Lilita 32 |
| D0 | Dock-Hintergrund | 0 | 1708 | 1080 | 212 |  | d2_dock_bg (9-Slice 4/8/4/8) |
| T1 | Tab Dorf | 0 | 1708 | 216 | 164 |  |  |
| T1P | Aktive Platte Dorf | 12 | 1682 | 192 | 196 |  | d2_dock_platte_aktiv |
| T1I | Icon Dorf (aktiv) | 38 | 1686 | 140 | 124 |  | Icon neu D2 |
| T1T | Label Dorf (aktiv) | 12 | 1812 | 192 | 44 |  | Lilita 36 #FFF3D6 |
| T1S | Indikator | 78 | 1860 | 60 | 8 |  | d2_dock_indikator |
| T2 | Tab Armee | 216 | 1708 | 216 | 164 |  |  |
| T2I | Icon Armee | 276 | 1722 | 96 | 88 |  | Icon neu D2 |
| T2T | Label Armee | 228 | 1814 | 192 | 38 |  | Lilita 30 #BFAE8E |
| T3 | Tab Bauen | 432 | 1708 | 216 | 164 |  |  |
| T3I | Icon Bauen | 492 | 1722 | 96 | 88 |  | Icon neu D2 |
| T3T | Label Bauen | 444 | 1814 | 192 | 38 |  | Lilita 30 #BFAE8E |
| T4 | Tab Helden | 648 | 1708 | 216 | 164 |  |  |
| T4I | Icon Helden | 708 | 1722 | 96 | 88 |  | Icon neu D2 |
| T4T | Label Helden | 660 | 1814 | 192 | 38 |  | Lilita 30 #BFAE8E |
| T5 | Tab Karte | 864 | 1708 | 216 | 164 |  |  |
| T5I | Icon Karte | 924 | 1722 | 96 | 88 |  | Icon neu D2 |
| T5T | Label Karte | 876 | 1814 | 192 | 38 |  | Lilita 30 #BFAE8E |
| T4B | Badge Helden | 804 | 1716 | 48 | 38 |  | d2_badge_zaehler |
| G1 | Gestenleiste (System) | 390 | 1896 | 300 | 10 |  | System |

## Icon-Liste (alle neu in D2 zu zeichnen)
| Icon | Größe | Verwendung |
|---|---|---|
| d2_ico_res_zeitkristall | 64 | Pill R1 |
| d2_ico_res_wissen | 64 | Pill R3 |
| d2_ico_res_muscheln | 64 | Pill R4 (Gold) |
| d2_ico_plus | 48 | vorhanden (R2) |
| d2_ico_ressourcen_liste | 64 | Knopf RB (Sack/Kiste) |
| d2_ico_chevron | 28 | RB, eine Datei, für „offen“ um 180° gedreht |
| d2_ico_res_holz | 72 | Liste L1 |
| d2_ico_res_stein | 72 | Liste L2 |
| d2_ico_res_nahrung | 72 | Liste L3 |
| d2_ico_event, d2_ico_gratis, d2_ico_shop, d2_ico_mehr | 96 | Seitenleiste (wie v1) |
| d2_ico_chat, d2_ico_quest | 96 | Chat, Quest (wie v1) |
| d2_ico_tab_dorf/armee/bauen/helden/karte | 140 / 96 | Dock (wie v1) |

## Offene Fragen
1. Welche Ressourcen kommen in die Liste? Bisher sind es Holz, Stein und Nahrung (game_config: res_wood, res_stone, res_food). Kommen später weitere dazu (z. B. Eisen)? Pro Zeile wächst die Liste um 120 px; bis etwa 7 Zeilen bleibt sie über dem Quest-Balken.
2. Soll die Lagergrenze angezeigt werden (Balken plus „/ 20.000“)? Und soll „voll“ rot erscheinen?
3. Zahlenformat: Ab welchem Wert wird gekürzt (z. B. 125.4k)? Die Pills fassen 6 Zeichen.
4. Benennung: Heißt es im UI „Gold“ oder „Muscheln“? Davon hängen Icon und Tooltip ab.
5. Soll ein Tipp auf eine Listenzeile zum Gebäude bzw. zur Info springen, oder ist die Zeile nur Anzeige?
