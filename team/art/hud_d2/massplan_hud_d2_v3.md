# Massplan Dorf-HUD D2 „Obsidian & Glut“ – v3

Stand 22.10.2026 · basiert auf v2 · Feedback Fabian: einklappbare Event-Leiste links, eigener Mail-Knopf, Ressourcen-Knopf nur als Kisten-Icon.
Kosten 0 $ (Python/PIL, nur D2-Bausteine). HUD v5 und `team/art/_alt/` werden nicht verwendet.

## Dateien
- `massplan_hud_d2_v3.png`: Massplan mit Legende. Beide Listen sind nur als Rahmen und Zeilen eingezeichnet; im Spiel ist nie mehr als eine offen.
- `massplan_hud_d2_v3_bloecke.png`: alles zu
- `massplan_hud_d2_v3_bloecke_ressourcen.png`: Ressourcen-Liste offen
- `massplan_hud_d2_v3_bloecke_events.png`: Event-Liste offen
- `massplan_hud_d2_v3_elemente.json`
- `_src/massplan_hud_d2_v3.py`: Selbstprüfung mit 0 Befunden

## Änderungen gegenüber v2
1. **Ressourcen-Knopf K1:** Das ist jetzt nur ein Icon-Knopf `d2_btn_quadrat_normal` (offen: `_gedrueckt`).
   - Position 172/196, Größe 104x104, Icon `d2_ico_kiste` 72 mit 16 px Innenabstand. Kein Text, kein Pfeil.
   - Er sitzt direkt unter der Zeitkristall-Pill, linksbündig mit ihr, mit 10 px Abstand zur Hitbox der Pill.
   - Die Liste L0 hängt weiterhin daran: 12 px darunter, gleiche linke Kante, also 172/312, Größe 600x448 (bis y 760).
2. **Event-Leiste links:** Sie ersetzt das Banner V1.
   - **Eingeklappt:** Knopf V1 bei 28/316, Größe 120x120, Label „Events“, Hitbox 120x152. Das Badge V1B zeigt die Anzahl laufender Events (im Beispiel 5).
   - **Ausgeklappt:** Die Liste W0 (`d2_dropdown_liste`) klappt direkt unter dem Knopf auf, mit gleicher linker Kante: 28/480, Größe 440x572, bis y 1052.
   - Einträge à 108 hoch, jeweils über die ganze Breite antippbar (416x108) und öffnen das Event-Fenster. Inhalt: Icon 72, Name Baloo 800 28 (max. 14 Zeichen), Restzeit Lilita 28 mit Uhr-Glyphe.
   - Unter 1 h erscheint die Restzeit in Glut-Orange, sonst in text.counter.
   - Ab 6 Einträgen scrollt die Liste. Höchstens bis y 1380, also über dem Chat.
3. **Seitenspalte rechts:** Events ist dort weg (jetzt links). Neu sind 4 Knöpfe à 120, im Abstand von 172:
   - Gratis/Login, y 316 (Badge)
   - Shop, y 488
   - **Mail**, y 660 (eigener Knopf, Badge mit ungelesenen Mails)
   - Mehr, y 832 (Badge)
4. **Unverändert:** Währungszeile, Chat, Quest und Dock bleiben wie in v2.
5. **Legende:** Die doppelte Spaltenüberschrift „Hitbox / Sprite“ ist entfernt.

## Prüfung
Das Skript prüft:
- Touch ≥ 96
- Safe Top 90
- Dock und Gestenzone
- Hitbox-Überlappung
- sichtbare Überlappung
- Listen oberhalb des Dock

Ergebnis: 0 Befunde. Die Listen sind Overlays und überlappen Fremdelemente gewollt; diese Paare nimmt die Prüfung aus.

Die PNGs habe ich in Originalgröße und als 200-%-Ausschnitte angesehen.

## Werte (px, 1080x1920)
| ID | Element | x | y | w | h | Hitbox | Sprite/Text |
|---|---|---|---|---|---|---|---|
| A1 | Avatar (Portraet) | 28 | 98 | 128 | 128 | 28,90 128x144 | d2_panel_frame (9-Slice) |
| A2 | Level-Badge | 92 | 182 | 60 | 40 |  | d2_badge_stufe |
| R1 | Pill Zeitkristalle | 172 | 98 | 248 | 80 | 172,90 248x96 | d2_pill_ressource |
| R2 | Plus Zeitkristalle -> Shop | 432 | 98 | 80 | 80 | 422,90 100x96 | d2_btn_plus_pill + d2_ico_plus |
| R3 | Pill Wissen | 532 | 98 | 248 | 80 | 532,90 248x96 | d2_pill_ressource |
| R4 | Pill Gold (Muscheln) | 800 | 98 | 248 | 80 | 800,90 248x96 | d2_pill_ressource |
| K1 | Knopf Ressourcen (Kiste) | 172 | 196 | 104 | 104 |  | d2_btn_quadrat_normal / _gedrueckt (offen) |
| L0 | Ressourcen-Liste (offen) | 172 | 312 | 600 | 448 |  | d2_dropdown_liste (9-Slice 72) |
| L0H | Kopf 'LAGER' | 196 | 336 | 552 | 32 |  | Text Baloo 700 22, Sperrung 3 |
| L1 | Zeile Holz | 184 | 376 | 576 | 120 |  | Zeile (ganze Zeile antippbar) |
| L1I | Icon Holz | 196 | 400 | 72 | 72 |  | Icon neu D2 |
| L1N | Name Holz | 284 | 394 | 240 | 40 |  | Text Baloo 800 28 |
| L1B | Lagerbalken Holz | 284 | 450 | 240 | 22 |  | d2_bar_bg + d2_bar_fill_glut |
| L1W | Menge Holz | 540 | 390 | 196 | 48 |  | Text Lilita 36 rechtsb. |
| L1C | Lager Holz | 540 | 442 | 196 | 34 |  | Text Baloo 700 22 rechtsb. |
| L2 | Zeile Stein | 184 | 496 | 576 | 120 |  | Zeile (ganze Zeile antippbar) |
| L2I | Icon Stein | 196 | 520 | 72 | 72 |  | Icon neu D2 |
| L2N | Name Stein | 284 | 514 | 240 | 40 |  | Text Baloo 800 28 |
| L2B | Lagerbalken Stein | 284 | 570 | 240 | 22 |  | d2_bar_bg + d2_bar_fill_glut |
| L2W | Menge Stein | 540 | 510 | 196 | 48 |  | Text Lilita 36 rechtsb. |
| L2C | Lager Stein | 540 | 562 | 196 | 34 |  | Text Baloo 700 22 rechtsb. |
| L3 | Zeile Nahrung | 184 | 616 | 576 | 120 |  | Zeile (ganze Zeile antippbar) |
| L3I | Icon Nahrung | 196 | 640 | 72 | 72 |  | Icon neu D2 |
| L3N | Name Nahrung | 284 | 634 | 240 | 40 |  | Text Baloo 800 28 |
| L3B | Lagerbalken Nahrung | 284 | 690 | 240 | 22 |  | d2_bar_bg + d2_bar_fill_glut |
| L3W | Menge Nahrung | 540 | 630 | 196 | 48 |  | Text Lilita 36 rechtsb. |
| L3C | Lager Nahrung | 540 | 682 | 196 | 34 |  | Text Baloo 700 22 rechtsb. |
| S1 | Seitenknopf Gratis / Login | 932 | 316 | 120 | 120 | 932,316 120x152 | d2_btn_quadrat_normal |
| S1L | Label Gratis | 932 | 440 | 120 | 28 |  | Text Baloo 800 22 |
| S1B | Badge Gratis | 1000 | 320 | 48 | 38 |  | d2_badge_zaehler |
| S2 | Seitenknopf Shop | 932 | 488 | 120 | 120 | 932,488 120x152 | d2_btn_quadrat_normal |
| S2L | Label Shop | 932 | 612 | 120 | 28 |  | Text Baloo 800 22 |
| S3 | Seitenknopf Mail | 932 | 660 | 120 | 120 | 932,660 120x152 | d2_btn_quadrat_normal |
| S3L | Label Mail | 932 | 784 | 120 | 28 |  | Text Baloo 800 22 |
| S3B | Badge Mail | 1000 | 664 | 48 | 38 |  | d2_badge_zaehler |
| S4 | Seitenknopf Mehr | 932 | 832 | 120 | 120 | 932,832 120x152 | d2_btn_quadrat_normal |
| S4L | Label Mehr | 932 | 956 | 120 | 28 |  | Text Baloo 800 22 |
| S4B | Badge Mehr | 1000 | 836 | 48 | 38 |  | d2_badge_zaehler |
| V1 | Event-Knopf (eingeklappt) | 28 | 316 | 120 | 120 | 28,316 120x152 | d2_btn_quadrat_normal / _gedrueckt (offen) |
| V1L | Label Events | 28 | 440 | 120 | 28 |  | Text Baloo 800 22 |
| V1B | Badge Anzahl Events | 96 | 320 | 48 | 38 |  | d2_badge_zaehler |
| W0 | Event-Liste (ausgeklappt) | 28 | 480 | 440 | 572 |  | d2_dropdown_liste (9-Slice 72) |
| W1 | Eintrag Erntefest | 40 | 496 | 416 | 108 |  | Zeile (antippbar -> Event-Fenster) |
| W1I | Icon Erntefest | 52 | 514 | 72 | 72 |  | Icon neu D2 |
| W1N | Name Erntefest | 140 | 510 | 300 | 40 |  | Text Baloo 800 28 |
| W1T | Restzeit Erntefest | 140 | 554 | 300 | 36 |  | Text Lilita 28 + Uhr-Icon 24 |
| W2 | Eintrag Turnier | 40 | 604 | 416 | 108 |  | Zeile (antippbar -> Event-Fenster) |
| W2I | Icon Turnier | 52 | 622 | 72 | 72 |  | Icon neu D2 |
| W2N | Name Turnier | 140 | 618 | 300 | 40 |  | Text Baloo 800 28 |
| W2T | Restzeit Turnier | 140 | 662 | 300 | 36 |  | Text Lilita 28 + Uhr-Icon 24 |
| W3 | Eintrag Haendler | 40 | 712 | 416 | 108 |  | Zeile (antippbar -> Event-Fenster) |
| W3I | Icon Haendler | 52 | 730 | 72 | 72 |  | Icon neu D2 |
| W3N | Name Haendler | 140 | 726 | 300 | 40 |  | Text Baloo 800 28 |
| W3T | Restzeit Haendler | 140 | 770 | 300 | 36 |  | Text Lilita 28 + Uhr-Icon 24 |
| W4 | Eintrag Bauwoche | 40 | 820 | 416 | 108 |  | Zeile (antippbar -> Event-Fenster) |
| W4I | Icon Bauwoche | 52 | 838 | 72 | 72 |  | Icon neu D2 |
| W4N | Name Bauwoche | 140 | 834 | 300 | 40 |  | Text Baloo 800 28 |
| W4T | Restzeit Bauwoche | 140 | 878 | 300 | 36 |  | Text Lilita 28 + Uhr-Icon 24 |
| W5 | Eintrag Gilden-Jagd | 40 | 928 | 416 | 108 |  | Zeile (antippbar -> Event-Fenster) |
| W5I | Icon Gilden-Jagd | 52 | 946 | 72 | 72 |  | Icon neu D2 |
| W5N | Name Gilden-Jagd | 140 | 942 | 300 | 40 |  | Text Baloo 800 28 |
| W5T | Restzeit Gilden-Jagd | 140 | 986 | 300 | 36 |  | Text Lilita 28 + Uhr-Icon 24 |
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

## Icon-Liste (neu in D2)
| Icon | Größe | Verwendung |
|---|---|---|
| d2_ico_res_zeitkristall / _wissen / _muscheln | 64 | Währungs-Pills |
| d2_ico_kiste | 72 | Ressourcen-Knopf K1 (ersetzt `d2_ico_ressourcen_liste` und `d2_ico_chevron`) |
| d2_ico_res_holz / _stein / _nahrung | 72 | Ressourcen-Liste |
| d2_ico_events | 80 | Event-Knopf V1 (alternativ das Icon des Top-Events) |
| d2_ico_event_erntefest / _turnier / _haendler / _bauwoche / _gildenjagd | 72 | Event-Einträge (Beispiele; ein Icon pro Event-Typ) |
| d2_ico_uhr | 24 | Restzeit |
| d2_ico_mail | 80 | Seitenknopf Mail |
| d2_ico_gratis, d2_ico_shop, d2_ico_mehr | 80 | Seitenspalte |
| d2_ico_chat, d2_ico_quest, Dock-Tabs | wie v2 | |

## Offene Fragen
1. Event-Knopf: festes Events-Icon oder das Icon des Events, das am frühesten endet?
2. Welche Event-Typen gibt es konkret? Davon hängen Namen (max. 14 Zeichen) und Icons ab.
3. Reihenfolge der Event-Einträge: nach Restzeit oder nach Priorität?
4. Soll der Kisten-Knopf ein Badge bekommen, z. B. „!“, wenn ein Lager voll ist?
5. Bleibt der Mail-Badge eine Zahl, oder reicht ein Punkt?
6. Aus v2 noch offen: Gold oder Muscheln, Zahlenformat k/M, weitere Ressourcen in der Liste.
