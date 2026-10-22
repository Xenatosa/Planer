# Massplan Dorf-HUD D2 – v6.3 (Plus an Zeitkristalle angedockt)

Stand: 22.10.2026, basiert auf v6.2.
Feedback von Fabian: „Das Plus von Zeitkristalle kann mehr nach links anheften.“
Alles andere ist unverändert.

## Änderung (Währungszeile, y 98, Höhe 80)
| Element | v6.2 x | v6.3 x | Hitbox |
|---|---|---|---|
| R1 Pill Zeitkristalle | 172 (bis 420) | 172 (bis 420) | 172–380 (208×96) |
| R2 Plus | 432 | **380** (bis 460) | 380–476 (96×96) |
| R3 Pill Wissen | 532 | **480** | 480–728 |
| R4 Pill Gold | 800 | **748** (bis 996) | 748–996 |

Begründung:
- **Plus angedockt:** Der Plus-Kreis sitzt halb auf dem rechten Pill-Ende (40 px Überlappung). Das ist das Muster von AFK Arena und Whiteout: Plus und Zahl wirken als eine Einheit, ohne Lücke dazwischen.
- **Kein Konflikt mit der Zahl:** Die Zahl „1.250“ endet bei ca. x 356, also vor dem Plus.
- **Hitboxen ohne Überlappung:** Die Pill-Hitbox endet bei 380, dort übernimmt das Plus. Zwischen Plus-Hitbox (476) und Wissen liegen 4 px.
- **Gleichmäßige Zeile:** Der sichtbare Abstand Plus→Wissen und Wissen→Gold beträgt je 20 px. Rechts sind danach bis 1052 noch 56 px frei.
- **Prüfung angepasst:** Die bewusste Sicht-Überlappung R1/R2 ist in der automatischen Prüfung als Ausnahme eingetragen.

## Prüfung
- Die automatische Prüfung meldet 0 Befunde.
- Gesichtet in Originalgröße und als 200-%-Ausschnitt der Währungszeile.

## Werte (px, 1080×1920)
| ID | Element | x | y | w | h | Hitbox | Sprite/Text |
|---|---|---|---|---|---|---|---|
| A1 | Avatar (Portraet) | 28 | 98 | 128 | 128 | 28,90 128x144 | d2_panel_frame (9-Slice) |
| A2 | Level-Badge | 92 | 182 | 60 | 40 |  | d2_badge_stufe |
| R1 | Pill Zeitkristalle | 172 | 98 | 248 | 80 | 172,90 208x96 | d2_pill_ressource |
| R2 | Plus Zeitkristalle -> Shop | 380 | 98 | 80 | 80 | 380,90 96x96 | d2_btn_plus_pill + d2_ico_plus |
| R3 | Pill Wissen | 480 | 98 | 248 | 80 | 480,90 248x96 | d2_pill_ressource |
| R4 | Pill Gold (Muscheln) | 748 | 98 | 248 | 80 | 748,90 248x96 | d2_pill_ressource |
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
| S1 | Seitenknopf Beschwören | 932 | 420 | 120 | 120 | 932,420 120x152 | d2_btn_quadrat_normal + Glut-Ring |
| S1L | Label Beschwören | 922 | 544 | 140 | 28 |  | Text Baloo 800 22 |
| S1B | Badge Beschwören | 1000 | 424 | 48 | 38 |  | d2_badge_zaehler |
| S2 | Seitenknopf Angebote | 932 | 592 | 120 | 120 | 932,592 120x152 | d2_btn_quadrat_normal |
| S2L | Label Angebote | 932 | 716 | 120 | 28 |  | Text Baloo 800 22 |
| S2B | Badge Angebote | 1000 | 596 | 48 | 38 |  | d2_badge_zaehler |
| S3 | Seitenknopf Pass | 932 | 764 | 120 | 120 | 932,764 120x152 | d2_btn_quadrat_normal |
| S3L | Label Pass | 932 | 888 | 120 | 28 |  | Text Baloo 800 22 |
| S3B | Badge Pass | 1000 | 768 | 48 | 38 |  | d2_badge_zaehler |
| H1 | Seitenknopf Wettkampf | 28 | 488 | 120 | 120 | 28,488 120x152 | d2_btn_quadrat_normal |
| H1L | Label Wettkampf | 28 | 612 | 120 | 28 |  | Text Baloo 800 22 |
| H1B | Badge Wettkampf | 96 | 492 | 48 | 38 |  | d2_badge_zaehler |
| B1 | Seitenknopf Bauen | 932 | 1552 | 120 | 120 |  | d2_btn_quadrat_normal |
| B1B | Badge Bauen | 1000 | 1556 | 48 | 38 |  | d2_badge_zaehler |
| N1 | Mini-Knopf Mail | 848 | 196 | 96 | 96 |  | d2_btn_quadrat_normal (96) |
| N2 | Mini-Knopf Mehr | 956 | 196 | 96 | 96 |  | d2_btn_quadrat_normal (96) / _gedrueckt (offen) |
| N1B | Badge Mail | 900 | 200 | 40 | 34 |  | d2_badge_zaehler |
| M0 | Mehr-Menue (offen) | 452 | 304 | 600 | 416 |  | d2_dropdown_liste (9-Slice 72) |
| M1 | Kachel Forschung | 476 | 368 | 120 | 120 | 476,368 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M2 | Kachel Minigames | 620 | 368 | 120 | 120 | 620,368 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M3 | Kachel Erfolge | 764 | 368 | 120 | 120 | 764,368 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M4 | Kachel Artefakte | 908 | 368 | 120 | 120 | 908,368 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M5 | Kachel Aufwertung | 476 | 544 | 120 | 120 | 476,544 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M6 | Kachel Kosmetik | 620 | 544 | 120 | 120 | 620,544 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M7 | Kachel Einstellungen | 764 | 544 | 120 | 120 | 764,544 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M8 | Kachel Hilfe | 908 | 544 | 120 | 120 | 908,544 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
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
| T1 | Tab Dorf | 0 | 1708 | 180 | 164 |  |  |
| T1P | Aktive Platte Dorf | 10 | 1682 | 160 | 196 |  | d2_dock_platte_aktiv |
| T1I | Icon Dorf (aktiv) | 30 | 1686 | 120 | 112 |  | Icon neu D2 |
| T1T | Label Dorf (aktiv) | 10 | 1812 | 160 | 44 |  | Lilita 34 #FFF3D6 |
| T1S | Indikator | 60 | 1860 | 60 | 8 |  | d2_dock_indikator |
| T2 | Tab Helden | 180 | 1708 | 180 | 164 |  |  |
| T2I | Icon Helden | 222 | 1722 | 96 | 88 |  | Icon neu D2 |
| T2T | Label Helden | 190 | 1814 | 160 | 38 |  | Lilita 30 #BFAE8E |
| T3 | Tab Karte | 360 | 1708 | 180 | 164 |  |  |
| T3I | Icon Karte | 402 | 1722 | 96 | 88 |  | Icon neu D2 |
| T3T | Label Karte | 370 | 1814 | 160 | 38 |  | Lilita 30 #BFAE8E |
| T4 | Tab Armee | 540 | 1708 | 180 | 164 |  |  |
| T4I | Icon Armee | 582 | 1722 | 96 | 88 |  | Icon neu D2 |
| T4T | Label Armee | 550 | 1814 | 160 | 38 |  | Lilita 30 #BFAE8E |
| T5 | Tab Gilde | 720 | 1708 | 180 | 164 |  |  |
| T5I | Icon Gilde | 762 | 1722 | 96 | 88 |  | Icon neu D2 |
| T5T | Label Gilde | 730 | 1814 | 160 | 38 |  | Lilita 30 #BFAE8E |
| T6 | Tab Inventar | 900 | 1708 | 180 | 164 |  |  |
| T6I | Icon Inventar | 942 | 1722 | 96 | 88 |  | Icon neu D2 |
| T6T | Label Inventar | 910 | 1814 | 160 | 38 |  | Lilita 30 #BFAE8E |
| T2B | Badge Helden | 302 | 1716 | 48 | 38 |  | d2_badge_zaehler |
| T5B | Badge Gilde | 842 | 1716 | 48 | 38 |  | d2_badge_zaehler |
| G1 | Gestenleiste (System) | 390 | 1896 | 300 | 10 |  | System |
