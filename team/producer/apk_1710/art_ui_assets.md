> ⛔ HUD v5.7 ist gestrichen (Fabian 22.10.2026), gültig ist D2 Obsidian & Glut + Dock A braun. Gesamtes HUD v5 (inkl. Icons `hud_c_ico_*`, `HudV5NumberFormat`) ist gestrichen; Dorf-HUD und Icons werden neu in D2 erstellt. Vorlage: `team/art/GUELTIG.md`.

Ergebnis: team/producer/apk_1710/art_ui_assets.md (v5.7 final mit Auflagen)
Kosten: Lieferung 7.5 1 Gen ca. 0,064 $; AD-Fixes 7.6 und Events-Icon nur Skript, 0 $. Liste per Skript `team/art/tools/apk1710_inventory.py`, GitHub-Connector nur lesend
Kritiker: geprueft ja, Auflagen 1–3 erledigt
Geprüft von: Epochen Kritiker (Auflagen 1–3) und geprüft Art Director (17.10., inkl. Fix Ähren und Federn)
Offene Fragen: In PR #96 nachzureichen: 9 Dateien (4 neu; Update auf v5.7: hud_layout.csv, HANDOFF_DEV_UI.md, hud_c_ico_gold, hud_c_ico_wissen, hud_c_ico_events), siehe uebergabe_art_ui_dev_ui.md. Lieferung 1–3 (17 Dateien) mit in APK als Stil-alt, Redo F7+
Nächster Empfänger: Dev UI (PR #96, Branch ui/hud-v5)
Regel: Keine Bestätigungs-/Danke-Nachrichten, keine reinen Status-Nachrichten.

# Art UI-Assets für die Test-APK 17.10.2026 (Stand v5.7 final, AD-abgenommen 17.10.)
Abgleich mit github.com/Xenatosa/epodarien: Branch `main` (rekursiver Baum) und PR #96 „feat(ui): HUD v5.7 + Lilita One (Style C)“ (offen, Branch `ui/hud-v5`). Vergleich über Dateiname und Git-Blob-SHA. Größen mit Pillow gemessen. 9-Slice für HUD als L/T/R/B, für Lieferung 1–7 als L,R,T,B (wie in `lieferung-ui-art.md`).

**Statistik (87 Assets):** im Repo (main) 16 · in PR #96 50 · fehlt im Repo 21.
**Nicht einbauen:** alle `_alt`, `_nieten`, `_muenze_alt` sowie `hud_c_ico_pass` (der Pass liegt jetzt im Shop) und `ui_btn_fab_build`.
**Update auf v5.7:** Die Datei liegt in PR #96, lokal gibt es aber eine neuere Fassung unter dem genannten Pfad. Die muss in den PR.
**Lieferung 1–3, fehlt im Repo:** Die Dateien wurden auf Halos geprüft (hell und dunkel): keine Halos. Sie sind kein Stil C, sondern im älteren Stil von Lieferung 1, und werden nur in Screens außerhalb des HUD genutzt. Darum mit in APK, markiert als **Stil-alt, Redo F7+**. Kein Asset ohne Datei, also kein prozeduraler Fallback nötig.
Die HUD-v5-Sprites liegen in PR #96 unter `Assets/Art/UI/HUD/v5/`, Lieferung 1–7 auf main unter `Assets/_Project/Art/UI/…`, die Docs auf main unter `docs/team/art/…`.

## A HUD v5 (Sprites/Daten)
| ID | Pfad (team/…) | Status | 9-Slice | Größe px | Repo |
|---|---|---|---|---|---|
| HANDOFF_DEV_UI | art/ui-kit/hud/v5/export/HANDOFF_DEV_UI.md | final | n/a | – | im Repo (main, ABWEICHEND) + in PR #96 (VERALTET) → **Update auf v5.7**: art/ui-kit/hud/v5/export/HANDOFF_DEV_UI.md |
| hud_c_avatar_ring | art/ui-kit/hud/v5/export/hud_c_avatar_ring.png | final | – | 185×181 | in PR #96 |
| hud_c_badge_dot | art/ui-kit/hud/v5/export/hud_c_badge_dot.png | final | – | 42×50 | in PR #96 |
| hud_c_badge_level | art/ui-kit/hud/v5/export/hud_c_badge_level.png | final | – | 68×76 | in PR #96 |
| hud_c_bar_fill | art/ui-kit/hud/v5/export/hud_c_bar_fill.png | final | 6/0/6/0 | 56×12 | in PR #96 |
| hud_c_bar_track | art/ui-kit/hud/v5/export/hud_c_bar_track.png | final | 8/6/8/6 | 61×17 | in PR #96 |
| hud_c_btn_close | art/ui-kit/hud/v5/export/hud_c_btn_close.png | final | – | 68×76 | in PR #96 |
| hud_c_btn_plus | art/ui-kit/hud/v5/export/hud_c_btn_plus.png | final | – | 52×54 | in PR #96 |
| hud_c_dot_soft | art/ui-kit/hud/v5/export/hud_c_dot_soft.png | final | – | 18×18 | fehlt → neu in v5.7, in PR #96 nachreichen: art/ui-kit/hud/v5/export/hud_c_dot_soft.png |
| hud_c_evt_mammutjagd | art/ui-kit/hud/v5/export/hud_c_evt_mammutjagd.png | final | – | 640×458 | in PR #96 |
| hud_c_evt_platzhalter | art/ui-kit/hud/v5/export/hud_c_evt_platzhalter.png | final · **abgenommen AD** (17.10.; neutraler Platzhalter, Federn grau-braun; tauschbar über hud_c_evt_<event_id>) | – | 645×460 | fehlt → neu in v5.7, in PR #96 nachreichen: art/ui-kit/hud/v5/export/hud_c_evt_platzhalter.png |
| hud_c_frame_panel | art/ui-kit/hud/v5/export/hud_c_frame_panel.png | final | 65/65/65/65 | 150×150 | in PR #96 |
| hud_c_frame_pill | art/ui-kit/hud/v5/export/hud_c_frame_pill.png | final | 190/170/190/170 | 400×360 | in PR #96 |
| hud_c_frame_pill_slim | art/ui-kit/hud/v5/export/hud_c_frame_pill_slim.png | final | 85/75/85/75 | 190×170 | in PR #96 |
| hud_c_frame_sheet | art/ui-kit/hud/v5/export/hud_c_frame_sheet.png | final | 65/65/65/65 | 150×150 | in PR #96 |
| hud_c_frame_tile | art/ui-kit/hud/v5/export/hud_c_frame_tile.png | final | 100/100/100/100 | 220×220 | in PR #96 |
| hud_c_sheet_handle | art/ui-kit/hud/v5/export/hud_c_sheet_handle.png | final | – | 481×170 | in PR #96 |
| hud_c_tab_active | art/ui-kit/hud/v5/export/hud_c_tab_active.png | final | – | 244×250 | in PR #96 |
| hud_c_tab_normal | art/ui-kit/hud/v5/export/hud_c_tab_normal.png | final | – | 233×229 | in PR #96 |
| hud_layout | art/ui-kit/hud/v5/export/hud_layout.csv | final | n/a | – | im Repo (main, ABWEICHEND) + in PR #96 (VERALTET) → **Update auf v5.7**: art/ui-kit/hud/v5/export/hud_layout.csv |

## B Icons Set eiszeit (24)
| ID | Pfad (team/…) | Status | 9-Slice | Größe px | Repo |
|---|---|---|---|---|---|
| hud_c_ico_kristall | art/ui-kit/hud/v5/export/hud_c_ico_kristall.png | final | – | 204×256 | in PR #96 |
| hud_c_ico_gold | art/ui-kit/hud/v5/export/hud_c_ico_gold.png | final als Fallback-ID; Skin über Iconset → gold_eiszeit | – | 250×256 | in PR #96 (VERALTET) → **Update auf v5.7**: art/ui-kit/hud/v5/export/hud_c_ico_gold.png |
| hud_c_ico_wissen | art/ui-kit/hud/v5/export/hud_c_ico_wissen.png | final | – | 232×256 | in PR #96 (VERALTET) → **Update auf v5.7**: art/ui-kit/hud/v5/export/hud_c_ico_wissen.png |
| hud_c_ico_slot3 | art/ui-kit/hud/v5/export/hud_c_ico_slot3.png | final (nur Editor-Platzhalter, nicht im Spiel) | – | 250×256 | in PR #96 |
| hud_c_ico_events | art/ui-kit/hud/v5/export/hud_c_ico_events.png | final (17.10.: Federn grau-braun, Skript-Fix nach AD-Regel) | – | 247×256 | in PR #96 (VERALTET) → **Update auf v5.7**: art/ui-kit/hud/v5/export/hud_c_ico_events.png |
| hud_c_ico_shop | art/ui-kit/hud/v5/export/hud_c_ico_shop.png | final | – | 256×255 | in PR #96 |
| hud_c_ico_pass | art/ui-kit/hud/v5/export/hud_c_ico_pass.png | ersetzt (Pass liegt im Shop; im HUD ungenutzt, nicht einbauen) | – | 240×256 | in PR #96 |
| hud_c_ico_mehr | art/ui-kit/hud/v5/export/hud_c_ico_mehr.png | final | – | 256×77 | in PR #96 |
| hud_c_ico_ressourcen | art/ui-kit/hud/v5/export/hud_c_ico_ressourcen.png | final | – | 241×256 | in PR #96 |
| hud_c_ico_dorf | art/ui-kit/hud/v5/export/hud_c_ico_dorf.png | final | – | 240×256 | in PR #96 |
| hud_c_ico_armee | art/ui-kit/hud/v5/export/hud_c_ico_armee.png | final | – | 249×256 | in PR #96 |
| hud_c_ico_bauen | art/ui-kit/hud/v5/export/hud_c_ico_bauen.png | final | – | 256×255 | in PR #96 |
| hud_c_ico_helden | art/ui-kit/hud/v5/export/hud_c_ico_helden.png | final | – | 256×250 | in PR #96 |
| hud_c_ico_karte | art/ui-kit/hud/v5/export/hud_c_ico_karte.png | final | – | 256×201 | in PR #96 |
| hud_c_ico_holz | art/ui-kit/hud/v5/export/hud_c_ico_holz.png | final | – | 256×224 | in PR #96 |
| hud_c_ico_stein | art/ui-kit/hud/v5/export/hud_c_ico_stein.png | final | – | 256×216 | in PR #96 |
| hud_c_ico_nahrung | art/ui-kit/hud/v5/export/hud_c_ico_nahrung.png | final | – | 250×256 | in PR #96 |
| hud_c_ico_einwohner | art/ui-kit/hud/v5/export/hud_c_ico_einwohner.png | final | – | 234×256 | in PR #96 |
| hud_c_ico_felle | art/ui-kit/hud/v5/export/hud_c_ico_felle.png | final | – | 256×237 | in PR #96 |
| hud_c_ico_fackel | art/ui-kit/hud/v5/export/hud_c_ico_fackel.png | final | – | 232×256 | in PR #96 |
| hud_c_ico_vorrat | art/ui-kit/hud/v5/export/hud_c_ico_vorrat.png | final (Basis für hud_c_ico_gratis) | – | 256×255 | in PR #96 |
| hud_c_ico_quest | art/ui-kit/hud/v5/export/hud_c_ico_quest.png | final | – | 206×256 | in PR #96 |
| hud_c_ico_forschung | art/ui-kit/hud/v5/export/hud_c_ico_forschung.png | final | – | 218×256 | in PR #96 |
| hud_c_ico_einstellungen | art/ui-kit/hud/v5/export/hud_c_ico_einstellungen.png | final | – | 245×256 | in PR #96 |

## B Gold-Skins
| ID | Pfad (team/…) | Status | 9-Slice | Größe px | Repo |
|---|---|---|---|---|---|
| hud_c_ico_gold_eiszeit | art/ui-kit/hud/v5/export/hud_c_ico_gold_eiszeit.png | final | – | 256×216 | in PR #96 |
| hud_c_ico_gold_e2 | art/ui-kit/hud/v5/export/hud_c_ico_gold_e2.png | final | – | 256×231 | in PR #96 |

## B Icons v5.7 final (Gen e0_ui_hud_v5_7_login_gratis)
| ID | Pfad (team/…) | Status | 9-Slice | Größe px | Repo |
|---|---|---|---|---|---|
| hud_c_ico_login_kalender | art/ui-kit/hud/v5/export/hud_c_ico_login_kalender.png | final · **abgenommen AD** (17.10.) | – | 256×256 | fehlt → neu in v5.7, in PR #96 nachreichen: art/ui-kit/hud/v5/export/hud_c_ico_login_kalender.png |
| hud_c_ico_gratis | art/ui-kit/hud/v5/export/hud_c_ico_gratis.png | final · **abgenommen AD** (17.10.) | – | 256×256 | fehlt → neu in v5.7, in PR #96 nachreichen: art/ui-kit/hud/v5/export/hud_c_ico_gratis.png |

## B Icons alt
| ID | Pfad (team/…) | Status | 9-Slice | Größe px | Repo |
|---|---|---|---|---|---|
| hud_c_ico_armee_alt | art/ui-kit/hud/v5/export/hud_c_ico_armee_alt.png | alt – NICHT EINBAUEN | – | 256×254 | in PR #96 |
| hud_c_ico_armee_nieten | art/ui-kit/hud/v5/export/hud_c_ico_armee_nieten.png | alt – NICHT EINBAUEN | – | 249×256 | fehlt |
| hud_c_ico_bauen_alt | art/ui-kit/hud/v5/export/hud_c_ico_bauen_alt.png | alt – NICHT EINBAUEN | – | 235×256 | in PR #96 |
| hud_c_ico_gold_muenze_alt | art/ui-kit/hud/v5/export/hud_c_ico_gold_muenze_alt.png | alt – NICHT EINBAUEN | – | 250×256 | in PR #96 |
| hud_c_ico_wissen_alt | art/ui-kit/hud/v5/export/hud_c_ico_wissen_alt.png | alt – NICHT EINBAUEN | – | 250×256 | in PR #96 |
| hud_c_ico_login_kalender_alt | art/ui-kit/hud/v5/export/hud_c_ico_login_kalender_alt.png | alt – NICHT EINBAUEN | – | 188×256 | fehlt |
| hud_c_ico_gratis_alt | art/ui-kit/hud/v5/export/hud_c_ico_gratis_alt.png | alt – NICHT EINBAUEN | – | 237×256 | fehlt |

## C Rahmen/Panels/Buttons L1–7 (L,R,T,B)
| ID | Pfad (team/…) | Status | 9-Slice | Größe px | Repo |
|---|---|---|---|---|---|
| ui_quest_banner | art/ui-kit/quest/ui_quest_banner.png | final | 40,40,40,40 | 192×110 | im Repo (main) |
| ui_quest_banner_done | art/ui-kit/quest/ui_quest_banner_done.png | final | 40,40,40,40 | 192×110 | im Repo (main) |
| ui_progressbar_bg | art/ui-kit/quest/ui_progressbar_bg.png | final · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | 12,12,12,12 | 64×24 | fehlt |
| ui_progressbar_fill | art/ui-kit/quest/ui_progressbar_fill.png | final · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | 12,12,12,12 | 64×24 | fehlt |
| ui_siedlerfeuer_pill | art/ui-kit/quest/ui_siedlerfeuer_pill.png | final · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | 40,40,38,38 | 192×80 | fehlt |
| ui_tag_siedlerfeuer_x4 | art/ui-kit/quest/ui_tag_siedlerfeuer_x4.png | final · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | 24,24,22,22 | 96×48 | fehlt |
| ui_unitcard_header | art/ui-kit/army/ui_unitcard_header.png | final · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | 32,32,32,16 | 128×72 | fehlt |
| ui_summon_banner_frame | art/ui-kit/summon/ui_summon_banner_frame.png | final · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | 48,48,48,48, | 256×192 | fehlt |
| ui_btn_rates_info | art/ui-kit/summon/ui_btn_rates_info.png | final · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | – | 128×128 | fehlt |
| ui_badge_free | art/ui-kit/summon/ui_badge_free.png | final · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | 32,32,30,30 | 200×64 | fehlt |
| ui_pity_fill | art/ui-kit/summon/ui_pity_fill.png | final · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | 12,12,12,12 | 64×24 | fehlt |
| ui_btn_close | art/ui-kit/common/ui_btn_close.png | final (Screens); im HUD: hud_c_btn_close · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | – | 128×128 | fehlt |
| ui_badge | art/ui-kit/common/ui_badge.png | final (Screens); im HUD: hud_c_badge_dot · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | – | 64×64 | fehlt |
| ui_avatar_frame | art/ui-kit/common/ui_avatar_frame.png | ersetzt durch ui_avatar_frame_v002 und HUD: hud_c_avatar_ring | – | 192×192 | im Repo (main) |
| ui_btn_fab_build | art/ui-kit/common/ui_btn_fab_build.png | ersetzt (Bauen = normaler Tab, kein FAB) · nicht in APK | – | 160×160 | fehlt |
| ui_ribbon | art/ui-kit/common/ui_ribbon.png | final | 70,70,0,0 | 320×110 | im Repo (main) |
| ui_ribbon_white | art/ui-kit/common/ui_ribbon_white.png | final · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | 70,70,0,0 | 320×110 | fehlt |
| ui_filter_chip_active | art/ui-kit/common/ui_filter_chip_active.png | final | 34,34,34,34 | 160×72 | im Repo (main) |
| ui_filter_chip | art/ui-kit/common/ui_filter_chip.png | final | 34,34,34,34 | 160×72 | im Repo (main) |
| ui_mission_reinforce_banner | art/ui-kit/mission/ui_mission_reinforce_banner.png | final · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | 44,44,44,44 | 224×128 | fehlt |
| ui_power_fill | art/ui-kit/mission/ui_power_fill.png | final · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | 12,12,12,12 | 64×24 | fehlt |
| ui_power_marker | art/ui-kit/mission/ui_power_marker.png | final · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | – | 24×48 | fehlt |
| ui_tag_winter | art/ui-kit/resbar/ui_tag_winter.png | final · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | 48,24,22,22 | 96×48 | fehlt |
| ui_tag_hunger | art/ui-kit/resbar/ui_tag_hunger.png | final · mit in APK · **Stil-alt, Redo F7+** (Halo-Prüfung 17.10.: keine Halos; kein Stil C, älterer L1-Stil, nur Screens außerhalb des HUD) | 48,24,22,22 | 96×48 | fehlt |
| ui_tag_winter_bg | art/ui-kit/resbar/ui_tag_winter_bg.png | final | 24,24,22,22 | 96×48 | im Repo (main) |
| ui_tag_hunger_bg | art/ui-kit/resbar/ui_tag_hunger_bg.png | final | 24,24,22,22 | 96×48 | im Repo (main) |
| ui_avatar_frame_v002 | art/ui-kit/common/ui_avatar_frame_v002.png | final | – | 192×192 | im Repo (main) |
| ui_btn_fab_build_v002 | art/ui-kit/common/ui_btn_fab_build_v002.png | ersetzt (Bauen = normaler Tab, kein FAB) | – | 160×160 | im Repo (main) |
| ui_panel_light_v002 | art/ui/panels/ui_panel_light_v002.png | final | 56,56,56,56 | 192×192 | im Repo (main) |
| ui_panel_light_rivets_v002 | art/ui/panels/ui_panel_light_rivets_v002.png | final (Variante, nur große Panels) | 56,56,56,56 | 192×192 | im Repo (main) |
| ui_panel_dark_v002 | art/ui/panels/ui_panel_dark_v002.png | final | 56,56,56,56 | 192×192 | im Repo (main) |
| ui_panel_dark_rivets_v002 | art/ui/panels/ui_panel_dark_rivets_v002.png | final (Variante, nur große Panels) | 56,56,56,56 | 192×192 | im Repo (main) |
