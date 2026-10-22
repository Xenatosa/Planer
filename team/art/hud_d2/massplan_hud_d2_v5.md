# Massplan Dorf-HUD D2 „Obsidian & Glut“ – v5 (nach Spielerlogik sortiert)

Stand 22.10.2026, basiert auf v4.

Feedback von Fabian: Inventar und Gilde werden oft genutzt und gehören ins Dock (dann 6 Tabs). Pass und Beschwörung sollen nicht links stehen. Links nur Events, Ranglisten und Ähnliches.

Hinweis zum Namen: Das ist der **D2-Maßplan v5**. Er ist nicht das verworfene alte „HUD v5/v5.7“.

Kosten 0 $ (Python/PIL), nur D2-Bausteine.

## Dateien
- `massplan_hud_d2_v5.png`: Plan, Mehr-Menü offen in Rosa
- `massplan_hud_d2_v5_bloecke.png`: alles zu
- `massplan_hud_d2_v5_bloecke_mehr.png`: Mehr-Menü offen
- `massplan_hud_d2_v5_elemente.json`
- `_src/massplan_hud_d2_v5.py`: Prüfung meldet 0 Befunde
- Ressourcen- und Event-Liste sind unverändert, die Bilder dazu liegen in v3.

## Grundregel (wie AFK Arena, Whiteout Survival, Rise of Kingdoms)
- **Dock = Orte und Kernschleife**, die mehrmals pro Sitzung geöffnet werden.
- **Links = Wettbewerb und Zeitlimit**, also alles, was man „nicht verpassen“ will. Hier steht keine Monetarisierung.
- **Rechts = Belohnungen und Monetarisierung.** Das deckt sich mit dem rechten Daumen und dem Blick, der rechts oben auf Angebote fällt.
- **Mehr = seltene Systeme.** Es ist ein Raster aus 3×3 Kacheln.
- Die Dorfmitte (x 176–904, y 330–1380) bleibt frei.

## Platzierung mit Begründung
| Element | Platz | Begründung |
|---|---|---|
| Dorf | Dock 1 (aktiv) | Startbildschirm; wie die Heimat-Tabs bei AFK Arena und Whiteout links außen |
| Helden | Dock 2 | Wird am häufigsten genutzt (Level, Sterne, Ausrüstung); kernvision: Helden gibt es nur im Menü |
| Inventar | Dock 3 | Fabian: wird oft genutzt; Gegenstände, Fragmente und Aufwertung täglich; Taschen-Tab wie bei Whiteout und RoK |
| Karte | Dock 4 | Kampagne und Weltkarte sind der Fortschrittsmotor; Mitte rechts ist gut mit dem Daumen erreichbar |
| Gilde | Dock 5 | Fabian: wird oft genutzt; tägliche Spende und Stammes-Jagd; Allianz-Tab wie bei Whiteout und RoK |
| Armee | Dock 6 | Soldaten und Formationen werden mehrmals täglich angepasst. Seltener als Helden, aber eigener Ort, bleibt deshalb im Dock. Formationen sind zusätzlich vor jedem Kampf erreichbar |
| **Bauen** | **nicht im Dock**: Knopf rechts unten B1 (932/1396) + Tipp auf Bauplatz oder Gebäude | Bauen passiert im Dorf selbst. Ohne Bauzeiten (GDD Nr. 103) baut man in Schüben, also wie der Hammer bei RoK. Der Knopf spiegelt Chat C1. Ein Badge zeigt baubare Gebäude |
| Events (Liste) | links V1 | Zeitlich begrenzt, Kern der linken Spalte |
| Ranglisten | links H1 | Wettbewerb; bei AFK Arena und RoK auf der Seite oder im Event-Kontext |
| Arena | links H2 (ab Epoche 2) | PvP und tägliche Versuche; Badge zeigt freie Kämpfe |
| Ahnenprüfung („Prüfung“) | links H3 | Wiederkehrender Wettbewerbs-/Herausforderungs-Modus wie der King's Tower bei AFK; Turnier und Weltboss bleiben in der Event-Liste |
| **Beschwören** | **rechts S1 mit Glut-Ring** | Stärkster Motivations- und Umsatzpunkt; oben rechts ist die prominenteste Seitenposition |
| Pass „Häuptlings-Pfad“ | rechts S2 | Monetarisierung mit Fortschritt; Badge zeigt abholbare Stufen |
| Shop | rechts S3 (+ Plus an der Kristall-Pill) | Monetarisierung |
| Gratis / Login | rechts S4 | Tägliche Belohnung; die Nähe zum Shop ist bewusst gewählt |
| Mail | rechts S5 | Belohnungen und Kompensationen kommen per Post |
| Mehr | rechts S6 | Letzter Knopf der rechten Spalte; das Menü klappt nach oben auf (Anker: rechte Kante gleich S6, 12 px Abstand) |
| Chat | links unten C1 | Unverändert (Gilden-Chat, für Spieler unter 18 aus) |
| Quests | Quest-Leiste | Unverändert; Reiter für Tages- und Wochenquests sowie Erfolge |
| Profil | Avatar | Unverändert |
| Ressourcen | Kiste K1 | Unverändert |
| Forschung, Minigames, Erfolge, Artefakte & Sets, Aufwertung, Abo, Kosmetik, Einstellungen (mit „Verträge kündigen“), Hilfe | Mehr M1–M9 | Selten oder über einen anderen Weg erreichbar. Forschung liegt auch am Gebäude, Erfolge auch in den Quests, das Abo auch im Shop |

Aus dem Mehr-Menü entfernt: Arena, Ranglisten und Ahnenprüfung (jetzt links).

## Dock-Maße (6 Tabs)
- **Breite und Hitbox:** 1080 / 6 = 180 pro Tab. Die Hitbox ist 180×164.
- **Aktive Platte:** 160×196, Position x+10, ragt 26 px hoch. Sie ist proportional zur alten Platte (v4: 192 auf 216).
- **Icon aktiv:** 120×112.
- **Icon inaktiv:** 96×88 bei x+42.
- **Labels:** 160 breit. Die Schrift ist aktiv Lilita 34 (vorher 36) und inaktiv 30. Ein Assert stellt sicher, dass jedes Label höchstens 148 px breit ist; „Inventar“ passt.
- **Abstände:** Zwischen den Icons bleiben 84 px Luft. In der 200-%-Ansicht wirkt das Dock nicht gedrängt.

## Prüfung
- Das Skript prüft Touch ≥ 96, Safe Top 90, Dock und Geste sowie Überlappungen. Ergebnis: 0 Befunde.
- Die Bilder wurden in Originalgröße und als 200-%-Ausschnitte angesehen (Dock links und rechts, Mehr-Menü, Plan).
- Die rechte Spalte endet mit der Mehr-Hitbox bei 1328. Danach folgt Bauen ab 1396 und endet bei 1548, also über der Dock-Platte (1682).

## Werte (px, 1080×1920)
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
| S1 | Seitenknopf Beschwören | 932 | 316 | 120 | 120 | 932,316 120x152 | d2_btn_quadrat_normal + Glut-Ring |
| S1L | Label Beschwören | 922 | 440 | 140 | 28 |  | Text Baloo 800 22 |
| S1B | Badge Beschwören | 1000 | 320 | 48 | 38 |  | d2_badge_zaehler |
| S2 | Seitenknopf Pass | 932 | 488 | 120 | 120 | 932,488 120x152 | d2_btn_quadrat_normal |
| S2L | Label Pass | 932 | 612 | 120 | 28 |  | Text Baloo 800 22 |
| S2B | Badge Pass | 1000 | 492 | 48 | 38 |  | d2_badge_zaehler |
| S3 | Seitenknopf Shop | 932 | 660 | 120 | 120 | 932,660 120x152 | d2_btn_quadrat_normal |
| S3L | Label Shop | 932 | 784 | 120 | 28 |  | Text Baloo 800 22 |
| S4 | Seitenknopf Gratis | 932 | 832 | 120 | 120 | 932,832 120x152 | d2_btn_quadrat_normal |
| S4L | Label Gratis | 932 | 956 | 120 | 28 |  | Text Baloo 800 22 |
| S4B | Badge Gratis | 1000 | 836 | 48 | 38 |  | d2_badge_zaehler |
| S5 | Seitenknopf Mail | 932 | 1004 | 120 | 120 | 932,1004 120x152 | d2_btn_quadrat_normal |
| S5L | Label Mail | 932 | 1128 | 120 | 28 |  | Text Baloo 800 22 |
| S5B | Badge Mail | 1000 | 1008 | 48 | 38 |  | d2_badge_zaehler |
| S6 | Seitenknopf Mehr | 932 | 1176 | 120 | 120 | 932,1176 120x152 | d2_btn_quadrat_normal / _gedrueckt (offen) |
| S6L | Label Mehr | 932 | 1300 | 120 | 28 |  | Text Baloo 800 22 |
| H1 | Seitenknopf Ranglisten | 28 | 488 | 120 | 120 | 28,488 120x152 | d2_btn_quadrat_normal |
| H1L | Label Ranglisten | 18 | 612 | 140 | 28 |  | Text Baloo 800 22 |
| H2 | Seitenknopf Arena | 28 | 660 | 120 | 120 | 28,660 120x152 | d2_btn_quadrat_normal |
| H2L | Label Arena | 28 | 784 | 120 | 28 |  | Text Baloo 800 22 |
| H2B | Badge Arena | 96 | 664 | 48 | 38 |  | d2_badge_zaehler |
| H3 | Seitenknopf Prüfung | 28 | 832 | 120 | 120 | 28,832 120x152 | d2_btn_quadrat_normal |
| H3L | Label Prüfung | 28 | 956 | 120 | 28 |  | Text Baloo 800 22 |
| B1 | Seitenknopf Bauen | 932 | 1396 | 120 | 120 | 932,1396 120x152 | d2_btn_quadrat_normal |
| B1L | Label Bauen | 932 | 1520 | 120 | 28 |  | Text Baloo 800 22 |
| B1B | Badge Bauen | 1000 | 1400 | 48 | 38 |  | d2_badge_zaehler |
| M0 | Mehr-Menue (offen) | 596 | 572 | 456 | 592 |  | d2_dropdown_liste (9-Slice 72) |
| M1 | Kachel Forschung | 620 | 636 | 120 | 120 | 620,636 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M2 | Kachel Minigames | 764 | 636 | 120 | 120 | 764,636 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M3 | Kachel Erfolge | 908 | 636 | 120 | 120 | 908,636 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M4 | Kachel Artefakte | 620 | 812 | 120 | 120 | 620,812 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M5 | Kachel Aufwertung | 764 | 812 | 120 | 120 | 764,812 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M6 | Kachel Abo | 908 | 812 | 120 | 120 | 908,812 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M7 | Kachel Kosmetik | 620 | 988 | 120 | 120 | 620,988 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M8 | Kachel Einstellungen | 764 | 988 | 120 | 120 | 764,988 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M9 | Kachel Hilfe | 908 | 988 | 120 | 120 | 908,988 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
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
| T3 | Tab Inventar | 360 | 1708 | 180 | 164 |  |  |
| T3I | Icon Inventar | 402 | 1722 | 96 | 88 |  | Icon neu D2 |
| T3T | Label Inventar | 370 | 1814 | 160 | 38 |  | Lilita 30 #BFAE8E |
| T4 | Tab Karte | 540 | 1708 | 180 | 164 |  |  |
| T4I | Icon Karte | 582 | 1722 | 96 | 88 |  | Icon neu D2 |
| T4T | Label Karte | 550 | 1814 | 160 | 38 |  | Lilita 30 #BFAE8E |
| T5 | Tab Gilde | 720 | 1708 | 180 | 164 |  |  |
| T5I | Icon Gilde | 762 | 1722 | 96 | 88 |  | Icon neu D2 |
| T5T | Label Gilde | 730 | 1814 | 160 | 38 |  | Lilita 30 #BFAE8E |
| T6 | Tab Armee | 900 | 1708 | 180 | 164 |  |  |
| T6I | Icon Armee | 942 | 1722 | 96 | 88 |  | Icon neu D2 |
| T6T | Label Armee | 910 | 1814 | 160 | 38 |  | Lilita 30 #BFAE8E |
| T2B | Badge Helden | 302 | 1716 | 48 | 38 |  | d2_badge_zaehler |
| T5B | Badge Gilde | 842 | 1716 | 48 | 38 |  | d2_badge_zaehler |
| G1 | Gestenleiste (System) | 390 | 1896 | 300 | 10 |  | System |

## Icon-Liste (neu in D2, 80 px wenn nicht anders angegeben)
- **Dock:** d2_ico_tab_dorf, d2_ico_tab_helden, d2_ico_tab_inventar, d2_ico_tab_karte, d2_ico_tab_gilde, d2_ico_tab_armee (96, aktiv 120)
- **Links:** d2_ico_events, d2_ico_rangliste, d2_ico_arena, d2_ico_ahnenpruefung
- **Rechts:** d2_ico_beschwoerung, d2_ico_pass, d2_ico_shop, d2_ico_gratis, d2_ico_mail, d2_ico_mehr, d2_ico_bauen (Hammer)
- **Mehr:** d2_ico_forschung, d2_ico_minigames, d2_ico_erfolge, d2_ico_artefakte, d2_ico_aufwertung, d2_ico_abo, d2_ico_kosmetik, d2_ico_einstellungen, d2_ico_hilfe
- **Aus v3 unverändert:** d2_ico_kiste, d2_ico_res_*, d2_ico_event_*, d2_ico_chat, d2_ico_quest, d2_ico_uhr

## Offene Fragen
1. **Armee oder Bauen im Dock?** Gewählt ist Armee, Bauen bekommt einen eigenen Knopf. Falls Bauen der Hauptloop ist, kann man die beiden tauschen. Dann bräuchte Armee den Zugang über die Kampfvorbereitung.
2. **Reihenfolge im Dock:** Dorf, Helden, Inventar, Karte, Gilde, Armee. Soll Karte stattdessen in die Mitte (Position 3 oder 4)?
3. **Beschriftung der Ahnenprüfung:** „Prüfung“ passt in 120 px, „Ahnenprüfung“ nicht. Ist das in Ordnung?
4. **Gesperrte Systeme ausblenden?** Das betrifft Arena (ab Epoche 2), Gilde (ab Häuptlingsfeuer 6) und Pass (ab L10). Bei 6 Tabs würde ein gesperrter Gilde-Tab Lücken erzeugen. Vorschlag: den Tab grau zeigen, mit Schloss und dem Text „ab Feuer 6“.
5. **Linke Spalte erweitern?** Turnier und Weltboss sind in der Event-Liste. Sollen sie eigene Knöpfe links bekommen? Platz wäre bei y 1004 und 1176.
6. Weiter offen: Götter, Freunde, VIP. Außerdem aus v2/v3: Gold oder Muscheln.
