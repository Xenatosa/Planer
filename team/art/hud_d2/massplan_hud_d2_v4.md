# Massplan Dorf-HUD D2 „Obsidian & Glut“ – v4 (vollständige Einstiegspunkte)

Stand 22.10.2026 · basiert auf v3 · Feedback Fabian: „Mir fehlt noch so viel im HUD, z. B. Inventar, Heldenbeschwörung …“
Kosten 0 $ (Python/PIL, nur D2-Bausteine). HUD v5 und `team/art/_alt/` werden nicht verwendet.

## Dateien
- `massplan_hud_d2_v4.png`: Plan mit Mehr-Menü (offen, rosa). Ressourcen- und Event-Liste stehen nur in der Legende, ihre Maße sind unverändert gegenüber v3.
- `massplan_hud_d2_v4_bloecke.png`: alles zu
- `massplan_hud_d2_v4_bloecke_mehr.png`: Mehr-Menü offen
- `massplan_hud_d2_v4_elemente.json`
- `_src/massplan_hud_d2_v4.py`: Prüfung mit 0 Befunden
- Ressourcen- und Event-Liste offen: siehe `massplan_hud_d2_v3_bloecke_ressourcen.png` und `massplan_hud_d2_v3_bloecke_events.png`. Die Werte sind gleich geblieben.

## 1. Feature-Inventar (nur, was in den Plänen steht)
Abkürzungen:
- **Scaffold** = `D2MenuScaffold.cs` (Branch `ui/menus-d2-geruest`)
- **GDD** = `team/gdd/GDD_v1.6.13.md`

| Feature | Platz im HUD | Quelle |
|---|---|---|
| Dorf, Gebäude, Häuptlingsfeuer | Dock „Dorf“ (Welt) | GDD 2/4, kernvision_fabian.md |
| Bauen | Dock „Bauen“ | GDD 4 (keine Bauzeiten, Nr. 103) |
| Soldaten, Formationen | Dock „Armee“ | GDD 5/6 (units, formations) |
| Heldenliste, Sternaufstieg, Level-Rückholung | Dock „Helden“ | GDD 6/7.5, helden/Helden-System_v1.md, level-rueckholung-v1.md |
| Ausrüstung am Helden | Dock „Helden“ → Held → Ausrüstung | ausruestung/ausruestung_konzept_v1.md, GDD 18 |
| Kampagne Epoche 1 | Dock „Karte“ | GDD 8, kampagne/kampagne_epoche1_v1.md |
| Weltkarte, Schlachtfelder | Dock „Karte“ | gdd/specs/weltkarte_v1.md, schlachtfeld_maps_plan_v1.md |
| **Heldenbeschwörung** (Banner, Ahnenruf-Tickets, Echo-Shop) | **links H1, mit Glut-Ring hervorgehoben** | GDD 7, helden/beschwoerung-pools-v1.md, Scaffold `summon_banner` |
| Fortschrittspass „Häuptlings-Pfad“ | links H2 „Pass“ | kampagne/fortschrittspass_skizze.md |
| Gilde „Stämme“ (Spende, Gilden-Shop, Stammes-Jagd) | links H3 „Gilde“ | GDD 11, Scaffold `guild_tribe` |
| Events (alle laufenden, inkl. Würfel-Event, Weltboss, Turnier, Event-Helden) | links V1 + Event-Liste | GDD 13/22/25/26/28, events/event_katalog.md, Scaffold `events`, `dice_event` |
| Login-Kalender / Gratis (20 Kristalle/Tag) | rechts S1 „Gratis“ | GDD 7.4 |
| Shop / Angebote (Kristalle, Pakete, Event-Pakete) | rechts S2 „Shop“; Plus an der Kristall-Pill | GDD 14/29, finanzen/monetarisierungskonzept-v4.md, Scaffold `gem_shop` |
| Mail / Postfach | rechts S3 „Mail“ | finanzen/codex_paket_event_tokens_b_v1.md |
| **Inventar** (Gegenstände, Gegenstand-Aufwertung, Fragmente) | **rechts S4 „Inventar“** (Reiter im Menü) | ausruestung/item_system_v1.md, Scaffold `inventory_items`, `item_upgrade`, `fragment_inventory` |
| Ressourcen / Lager | Kiste K1 + Liste | gdd/specs/ressourcen_regel_v1.md, F6_sammeln_offline.md |
| Währungen Zeitkristalle, Wissen, Gold | Währungszeile | GDD 3/7.2 |
| Quests: Haupt-, Tages-, Wochenquests | Quest-Leiste unten (Tipp öffnet die Aufgaben mit Reitern) | quests/quest-system-v1.md, GDD 21.1 |
| Chat (nur Gilde, U18 gesperrt) | Chat-Knopf C1 | GDD 11 / K-L3 |
| Profil | Avatar A1 | GDD (Profil/Titel), quest-system-v1.md |
| Forschung | Mehr M1 (zusätzlich über das Gebäude im Dorf) | GDD 21, forschung/forschung_konzept_v1.1.md, Scaffold `research` |
| Arena (ab Epoche 2) | Mehr M2 | GDD 12, Scaffold `arena` |
| Ranglisten | Mehr M3 | GDD 13/22/23 |
| Ahnenprüfung | Mehr M4 | GDD 20, Scaffold `ancestral_trial` |
| Minigames | Mehr M5 | GDD 17, minigame/minigames_spec_law_v1.md, Scaffold `minigames` |
| Erfolge | Mehr M6 | quests/quest-system-v1.md, quests/erfolge.csv |
| Artefakte & Sets | Mehr M7 | GDD 18, Scaffold `artifacts_sets` |
| Allgemeine Aufwertung | Mehr M8 | Scaffold `general_upgrade` |
| Abo „Chronist“ | Mehr M9 (zusätzlich im Shop) | GDD 14 |
| Kosmetik (Rahmen, Skins) | Mehr M10 | ausruestung/cosmetic_products_vorschlag.csv, GDD 14 |
| Einstellungen (inkl. Pflicht-Knopf „Verträge hier kündigen“) | Mehr M11 | GDD 19.x Nr. 5 |
| Hilfe / FAQ / AGB | Mehr M12 | GDD 25.12 |
| Offline-Sammeln | kein Knopf, Popup beim Login | F6_sammeln_offline.md |

**Nicht aufgenommen, weil kein Plan existiert:**
- **Götter:** Laut `finanzen/codex_paket_waehrungen_v1.md` sollen Dokumente „nachgeliefert“ werden. `team/goetter` gibt es nicht.
- **Freunde:** Kein Treffer in den Plänen. Laut GDD gibt es nur Gruppenchat, keine Privatnachrichten.
- **Stammesfehde:** erst „Launch + 1 Saison“.
- **VIP:** nur ein Input-Dokument (`finanzen/vip_input_f5_f6_v1.md`), ohne Entscheidung.
- Die Ordner `team/gilden` und `team/weltkarte` fehlen. Die Inhalte stehen im GDD bzw. in `gdd/specs`.

## 2. Gruppierung (UX-Logik wie bei AFK Arena, Rise of Kingdoms, Whiteout Survival)
- **Dock (5 Tabs, unverändert):** die Kernschleife Dorf, Armee, Bauen, Helden, Karte.
- **Links, „Wachstum/Live“:** Events V1 (316), **Beschwören H1 (488)**, Pass H2 (660), Gilde H3 (832). Alle 120x120, Abstand 172, Hitbox 120x152.
  - Beschwören liegt als stärkster Monetarisierungs- und Motivationspunkt direkt unter Events und bekommt den Glut-Ring. Er sitzt nicht im Dock, weil die Tabs Orte sind und keine Aktion.
- **Rechts, „Konto/täglich“:** Gratis S1 (316), Shop S2 (488), Mail S3 (660), **Inventar S4 (832)**, Mehr S5 (1004). Ebenfalls 120x120, Abstand 172.
- **Mehr-Menü:** Raster aus 4x3 Kacheln à 120 (Hitbox 120x152, Abstand 144/176) im `d2_dropdown_liste`.
  - Position 452/400, Größe 600x592.
  - Anker: rechte Kante = S5, Unterkante 12 px über S5. Dock und Mehr-Knopf bleiben frei.
  - Seltene Systeme liegen hier.
- **Dorfmitte bleibt frei:** x 176–904 und y 330–1380 enthält nur die Kiste und die Overlays.
- **Overlays sind modal:** Es ist immer nur eins offen (Ressourcen, Events oder Mehr). Ein Tipp auf den Scrim schließt es.

## Prüfung
Das Skript prüft Touch ≥ 96, Safe Top 90, Dock und Geste, Hitbox- und sichtbare Überlappung sowie, dass die Overlays über dem Dock bleiben. Ergebnis: 0 Befunde. Overlays gegen Fremdelemente sind gewollt und von der Prüfung ausgenommen.

Gesichtet in Originalgröße und als 200-%-Ausschnitte (Mehr-Raster, linke Spalte, Plan). Alle Kachel-Labels sind ≤ 140 px breit (Assert).

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
| S2 | Seitenknopf Shop / Angebote | 932 | 488 | 120 | 120 | 932,488 120x152 | d2_btn_quadrat_normal |
| S2L | Label Shop | 932 | 612 | 120 | 28 |  | Text Baloo 800 22 |
| S2B | Badge Shop | 1000 | 492 | 48 | 38 |  | d2_badge_zaehler |
| S3 | Seitenknopf Mail | 932 | 660 | 120 | 120 | 932,660 120x152 | d2_btn_quadrat_normal |
| S3L | Label Mail | 932 | 784 | 120 | 28 |  | Text Baloo 800 22 |
| S3B | Badge Mail | 1000 | 664 | 48 | 38 |  | d2_badge_zaehler |
| S4 | Seitenknopf Inventar | 932 | 832 | 120 | 120 | 932,832 120x152 | d2_btn_quadrat_normal |
| S4L | Label Inventar | 932 | 956 | 120 | 28 |  | Text Baloo 800 22 |
| S5 | Seitenknopf Mehr | 932 | 1004 | 120 | 120 | 932,1004 120x152 | d2_btn_quadrat_normal / _gedrueckt (offen) |
| S5L | Label Mehr | 932 | 1128 | 120 | 28 |  | Text Baloo 800 22 |
| H1 | Seitenknopf Beschwören | 28 | 488 | 120 | 120 | 28,488 120x152 | d2_btn_quadrat_normal + Glut-Ring (Akzent) |
| H1L | Label Beschwören | 18 | 612 | 140 | 28 |  | Text Baloo 800 22 |
| H1B | Badge Beschwören | 96 | 492 | 48 | 38 |  | d2_badge_zaehler |
| H2 | Seitenknopf Pass | 28 | 660 | 120 | 120 | 28,660 120x152 | d2_btn_quadrat_normal |
| H2L | Label Pass | 28 | 784 | 120 | 28 |  | Text Baloo 800 22 |
| H2B | Badge Pass | 96 | 664 | 48 | 38 |  | d2_badge_zaehler |
| H3 | Seitenknopf Gilde | 28 | 832 | 120 | 120 | 28,832 120x152 | d2_btn_quadrat_normal |
| H3L | Label Gilde | 28 | 956 | 120 | 28 |  | Text Baloo 800 22 |
| H3B | Badge Gilde | 96 | 836 | 48 | 38 |  | d2_badge_zaehler |
| M0 | Mehr-Menue (offen) | 452 | 400 | 600 | 592 |  | d2_dropdown_liste (9-Slice 72) |
| M1 | Kachel Forschung | 476 | 464 | 120 | 120 | 476,464 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M2 | Kachel Arena | 620 | 464 | 120 | 120 | 620,464 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M3 | Kachel Ranglisten | 764 | 464 | 120 | 120 | 764,464 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M4 | Kachel Ahnenprüfung | 908 | 464 | 120 | 120 | 908,464 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M5 | Kachel Minigames | 476 | 640 | 120 | 120 | 476,640 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M6 | Kachel Erfolge | 620 | 640 | 120 | 120 | 620,640 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M7 | Kachel Artefakte | 764 | 640 | 120 | 120 | 764,640 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M8 | Kachel Aufwertung | 908 | 640 | 120 | 120 | 908,640 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M9 | Kachel Abo | 476 | 816 | 120 | 120 | 476,816 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M10 | Kachel Kosmetik | 620 | 816 | 120 | 120 | 620,816 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M11 | Kachel Einstellungen | 764 | 816 | 120 | 120 | 764,816 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
| M12 | Kachel Hilfe | 908 | 816 | 120 | 120 | 908,816 120x152 | d2_btn_quadrat_normal + Label Baloo 20 |
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

## Icon-Liste (neu in D2, alle 80 außer wo angegeben)
- Bestehend aus v3: d2_ico_res_* (64/72), d2_ico_kiste (72), d2_ico_events, d2_ico_event_* (72), d2_ico_uhr (24), d2_ico_mail, d2_ico_gratis, d2_ico_shop, d2_ico_chat, d2_ico_quest, Dock-Tabs
- Neu links: **d2_ico_beschwoerung**, d2_ico_pass, d2_ico_gilde
- Neu rechts: **d2_ico_inventar**, d2_ico_mehr
- Neu im Mehr-Menü: d2_ico_forschung, d2_ico_arena, d2_ico_rangliste, d2_ico_ahnenpruefung, d2_ico_minigames, d2_ico_erfolge, d2_ico_artefakte, d2_ico_aufwertung, d2_ico_abo, d2_ico_kosmetik, d2_ico_einstellungen, d2_ico_hilfe

## Offene Fragen
1. **Götter:** Gibt es ein System? Ohne Plan gibt es keinen Knopf. Platz wäre links H4 (y 1004) oder eine Kachel im Mehr-Menü.
2. **Freunde:** sind gewollt? Die Pläne sehen bisher nur Gilden-Chat vor.
3. **Pass:** Soll der Knopf erst ab L10 erscheinen? Gilde erst ab Häuptlingsfeuer 6, Arena erst ab Epoche 2? Vorschlag: gesperrte Knöpfe ausblenden statt grau anzeigen.
4. **Forschung:** nur über das Gebäude oder zusätzlich im Mehr-Menü (so geplant)?
5. **Inventar:** Sollen Fragmente ein eigener Reiter im Inventar sein (so geplant) oder ein eigener Einstieg?
6. **Abo:** reicht die Kachel im Mehr-Menü plus Shop, oder braucht es einen eigenen Knopf?
7. Aus v2/v3 noch offen: Gold oder Muscheln, Event-Icon, Sortierung der Event-Liste.
