# Massplan Dorf-HUD D2 „Obsidian & Glut“ – v6 (wenige Seitenknöpfe, Hub-Prinzip)

Stand 22.10.2026, aufbauend auf v5.

Feedback von Fabian:
1. Im Dock soll Inventar ganz rechts stehen, Gilde direkt davor.
2. „Zu viele Knöpfe rechts. Orientier dich an AFK Arena oder anderen großen Mobile Games.“

Kosten 0 $ (Python/PIL), nur D2-Bausteine verwendet.

## Dateien
- `massplan_hud_d2_v6.png`: Plan, Mehr-Menü offen in Rosa
- `massplan_hud_d2_v6_bloecke.png`: alle Menüs zu
- `massplan_hud_d2_v6_bloecke_mehr.png`: Mehr-Menü offen
- `massplan_hud_d2_v6_elemente.json`
- `_src/massplan_hud_d2_v6.py`: die Prüfung meldet 0 Befunde

Ressourcen- und Event-Liste sind unverändert, die Bilder dazu liegen bei v3.

## Referenzen (Recherche per Websuche, 22.10.2026)

| Quelle | Was übernommen wurde |
|---|---|
| [ludo.guide: AFK Arena, User Interface](https://www.ludo.guide/guide/afk-arena/understanding-the-user-interface-ui) | Unten eine feste Leiste mit den Kernmenüs (Campaign, Heroes, Bag …). Oben Währungen. **Links Events, Angebote und Tagesaufgaben.** Rechts nur die AFK-Belohnung. Die Mitte bleibt frei. Übernommen: links „Live“, unten die Orte, Inventar („Bag“) im Dock. |
| [afk.guide: Guild](https://afk.guide/guild/), [Fandom: Guild](https://afk-arena.fandom.com/wiki/Guild) | Bei AFK ist die Gilde ein Gebäude in der Stadt (Ranhorn) und kein eigener Knopf. Fabian will sie im Dock; wir übernehmen das Prinzip, **Features zu bündeln, statt sie als einzelne Knöpfe anzubieten**. |
| [Fandom: Heroes](https://afk-arena.fandom.com/wiki/Heroes) | Formationen sind ein Reiter im Helden-Menü. Wir behalten Armee als Dock-Tab, weil Soldaten bei uns ein eigenes System sind. |
| [basicallyaverage: Whiteout Survival](https://basicallyaverage.com/ginas-revenge-whiteout-survival/), [appgamer: WoS Gems](https://www.appgamer.com/white-out-survival/how-to-get-free-gems) | Whiteout bündelt **alle Events hinter einem Knopf** (Klemmbrett mit Kalender). Mail und kleine Belohnungs-Icons liegen oben rechts als Mini-Icons, die Quest-Liste unten links. Übernommen: Mini-Reihe oben rechts (Mail, Mehr), Events als ein aufklappbarer Hub, Quest-Leiste unten links. |
| [TechWiser: Whiteout Survival Icons](https://techwiser.com/whiteout-survival-icons-and-symbols-meaning/) | Einstellungen, Hilfe, Konto, AGB und Support liegen gesammelt **in einem Einstellungs-Hub**. Mail ist ein Umschlag-Icon. Übernommen: Einstellungen und Hilfe stecken im Mehr-Menü. |
| [wostools: Beginner's Guide](https://wostools.net/beginners-guide) | Gebäude werden direkt im Dorf angetippt. Unten liegen Schnellzugriffe auf Heroes, Troops und die World Map. Übernommen: Bauen über einen Tipp aufs Gebäude, dazu ein Hammer als Schnellzugriff. |
| Wiki zu Whiteout Survival, Abschnitt 5.2 (namu.wiki) | Das Angebots-Icon ist dauerhaft da und bündelt Wochen- und Monatskarte, Login-Geschenk und Aufladebonus. Übernommen: **„Angebote“ fasst Shop, Gratis/Login und Abo zusammen.** |
| Rise of Kingdoms, Clash of Clans | Das ist Erfahrungswissen; Screenshots wurden nicht recherchiert. Beide Spiele haben einen Bau- bzw. Shop-Knopf rechts unten am Daumen und wenige Seitenknöpfe. |

## Platzierung und Begründung
| Element | Platz | Begründung |
|---|---|---|
| Dock | Dorf, Helden, Karte, Armee, Gilde, Inventar | Fabian: Inventar ganz rechts, Gilde davor. Dorf ist Heimat (links außen). Helden werden am häufigsten genutzt. Karte (Kampagne und Weltkarte) ist der Fortschritt. Armee gehört neben die Karte, weil man vor dem Kampf die Formation anpasst. |
| Events | links V1, Liste aufklappbar | wie AFK (links) und Whiteout (alle Events hinter einem Knopf) |
| **Wettkampf (Hub)** | links H1 | fasst Arena, Ranglisten und Ahnenprüfung zusammen, damit links nur 2 Knöpfe stehen. Das Badge zählt freie Arena-Kämpfe. |
| **Beschwören** | rechts S1 mit Glut-Ring | der eine prominente Aufruf zur Aktion |
| **Angebote** | rechts S2 | ein Hub mit den Reitern Shop, Gratis/Login und Abo „Chronist“. Dort liegt auch der Knopf „Verträge kündigen“. |
| Pass | rechts S3 | Häuptlings-Pfad; das Badge zeigt abholbare Stufen. Rechts stehen damit nur 3 Knöpfe. |
| Mail | Mini-Reihe oben rechts N1 (96, ohne Label) | wie Whiteout: Umschlag oben rechts, Badge mit der Zahl |
| Mehr | Mini-Reihe oben rechts N2 (96) | Hub für seltene Funktionen. Das Menü klappt nach unten auf, rechte Kante 1052. |
| Bauen | Hammer B1 rechts unten (932/1396) und Tipp auf Gebäude | Daumenzone, wie RoK und CoC. Er spiegelt den Chat. |
| Chat | links unten C1 | unverändert |
| Quests | Quest-Leiste | unverändert, wie bei Whiteout unten links |
| Profil, Ressourcen | Avatar, Kiste | unverändert |
| Mehr-Menü (4×2) | Forschung, Minigames, Erfolge, Artefakte, Aufwertung, Kosmetik, Einstellungen, Hilfe | Das Abo wurde entfernt (jetzt in Angebote), Arena, Ranglisten und Prüfung ebenfalls (jetzt in Wettkampf). |

**Zählung:**
- Seite links: 2 Knöpfe (Events, Wettkampf)
- Seite rechts: 3 Knöpfe (Beschwören, Angebote, Pass)
- Mini-Reihe oben rechts: 2 Icons (Mail, Mehr)
- Ecken unten: 2 Knöpfe (Chat, Bauen)

Zwischen y 660 (Wettkampf links) bzw. 832 (Pass rechts) und y 1396 ist die gesamte Höhe frei.

## Maße
- Mini-Knöpfe: 96×96, Icon 64, Position y 196 (gleiche Höhe wie die Kiste), x 848 und 956. Sie schließen rechts bündig mit der Seitenspalte ab (1052).
- Mehr-Menü: 600×416 bei 452/304.
- Dock: 6 × 180, wie in v5.
- Die Prüfung im Skript (Touch ≥ 96, Safe Top 90, Geste, Überlappung) meldet 0 Befunde.
- Die Bilder wurden in Originalgröße und in 200-%-Ausschnitten angesehen (oben rechts, Dock).

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
| S2 | Seitenknopf Angebote | 932 | 488 | 120 | 120 | 932,488 120x152 | d2_btn_quadrat_normal |
| S2L | Label Angebote | 932 | 612 | 120 | 28 |  | Text Baloo 800 22 |
| S2B | Badge Angebote | 1000 | 492 | 48 | 38 |  | d2_badge_zaehler |
| S3 | Seitenknopf Pass | 932 | 660 | 120 | 120 | 932,660 120x152 | d2_btn_quadrat_normal |
| S3L | Label Pass | 932 | 784 | 120 | 28 |  | Text Baloo 800 22 |
| S3B | Badge Pass | 1000 | 664 | 48 | 38 |  | d2_badge_zaehler |
| H1 | Seitenknopf Wettkampf | 28 | 488 | 120 | 120 | 28,488 120x152 | d2_btn_quadrat_normal |
| H1L | Label Wettkampf | 28 | 612 | 120 | 28 |  | Text Baloo 800 22 |
| H1B | Badge Wettkampf | 96 | 492 | 48 | 38 |  | d2_badge_zaehler |
| B1 | Seitenknopf Bauen | 932 | 1396 | 120 | 120 | 932,1396 120x152 | d2_btn_quadrat_normal |
| B1L | Label Bauen | 932 | 1520 | 120 | 28 |  | Text Baloo 800 22 |
| B1B | Badge Bauen | 1000 | 1400 | 48 | 38 |  | d2_badge_zaehler |
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

## Icons (neu D2)
- Dock: d2_ico_tab_dorf/helden/karte/armee/gilde/inventar
- Links: d2_ico_events, d2_ico_wettkampf (gekreuzte Schwerter)
- Rechts: d2_ico_beschwoerung, d2_ico_angebote, d2_ico_pass, d2_ico_bauen
- Mini-Reihe: d2_ico_mail, d2_ico_mehr (64)
- Mehr-Menü: forschung, minigames, erfolge, artefakte, aufwertung, kosmetik, einstellungen, hilfe

## Offene Fragen
1. Ist es in Ordnung, Gratis/Login in Angebote zu verschieben? Alternativ könnte es in die Event-Liste.
2. Wettkampf als Hub: Soll sich ein eigener Bildschirm mit 3 Kacheln öffnen (Vorschlag) oder ein Dropdown wie bei den Events?
3. Soll der Bau-Hammer bleiben, oder reicht der Tipp aufs Gebäude? Ohne Hammer wären es 3 Seiten- bzw. Eckknöpfe weniger.
4. Soll Einstellungen ein eigenes Mini-Icon bekommen (dritter Platz in der Mini-Reihe bei x 740)?
5. Weiter offen: Götter, Freunde, VIP, Gold oder Muscheln.
