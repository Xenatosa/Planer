> ⛔ HUD v5.7 ist gestrichen (Fabian 22.10.2026), gültig ist D2 Obsidian & Glut + Dock A braun. Gesamtes HUD v5 (inkl. Icons `hud_c_ico_*`, `HudV5NumberFormat`) ist gestrichen; Dorf-HUD und Icons werden neu in D2 erstellt. Vorlage: `team/art/GUELTIG.md`.

# Lieferung UI-Art – Placeholder v001 (14.10.2026, rev. nach AD-Review)

Pipeline: Pillow/prozedural, Generatoren `../tools/ui_art_lieferung.py`, `ui_art_main.py`, `ui_art_mission.py`. PNG RGBA sRGB, Straight Alpha, Referenz 1080×1920. Keine AD-Dateien überschrieben.

## 9-Slice-Übersicht (alle Panels/Banner/Bars dieser Lieferung)
Mesh Type Full Rect, Image Type Sliced, PPU 100, Pixels Per Unit Multiplier 1. Werte in px der Quelldatei.

| Sprite | Quelle | Einsatzgröße (Beispiel) | Border L,R,T,B | Fill Center |
|---|---|---|---|---|
| ui_quest_banner / _done | 192×110 | 620×110 | 40,40,40,40 | an |
| ui_progressbar_bg / _fill | 64×24 | 380–700×24 (Fill per Breite, min 24) | 12,12,12,12 | an |
| ui_pity_fill | 64×24 | 0–700×28 (min 24) | 12,12,12,12 | an |
| ui_tag_winter_bg / ui_tag_hunger_bg | 96×48 | 180–260×48–56 | 24,24,22,22 | an |
| ui_tag_winter / ui_tag_hunger (mit Icon) | 96×48 | 96–260×48 | 48,24,22,22 | an |
| ui_power_fill | 64×24 | 0–440×24 (min 24) | 12,12,12,12 | an |
| ui_reinforce_speedlines_mask | 640×160 | 980×170 (Simple, gestreckt) | – | – |
| ui_siedlerfeuer_pill | 192×80 | 360×80 | 40,40,38,38 | an |
| ui_badge_free | 200×64 | 200–560×64–80 | 32,32,30,30 | an |
| ui_unitcard_header (weiß, Image.color) | 128×72 | 310–500×72 | 32,32,32,16 | an |
| ui_summon_banner_frame | 256×192 | 1032×560 | 48,48,48,48 | **aus** |
| ui_ribbon / ui_ribbon_white | 320×110 | 560–620×110 (nur horizontal) | 70,70,0,0 | an |
| ui_filter_chip / _active | 160×72 | 160–260×72 | 34,34,34,34 | an |
| ui_mission_reinforce_banner | 224×128 | 980×170 | 44,44,44,44 | an |
| ui_rarity_shine_mask | 256×256 | wie Rarity-Rahmen | 40,40,40,40 | aus |
| ui_panel_light/dark_v002, _rivets_v002 | 192×192 | frei | 56,56,56,56 | an |
| (Referenz AD) ui_panel_light/dark 56 · ui_resbar_chip 30 · ui_tabbar_bg 60 · ui_btn_* 40,40,40,48 · ui_tab_active 56 · ui_card_building 48 · ui_rarity_* 40 | | | | |

Gestreckte Beispiele: `ui-kit/stretch/demo_*.png`, Kontaktbogen `previews/contact_9slice_stretch.png`.

## Lieferung 1 (Quest, Siedlerfeuer, Unit-Header, Resbar, Beschwörung, VFX, fehlende Sprites)

| ID | Pfad | Größe | Image Type | 9-Slice L,R,T,B |
|---|---|---|---|---|
| ui_quest_banner | ui-kit/quest/ui_quest_banner.png | 192×110 | Sliced | 40,40,40,40 |
| ui_quest_banner_done | ui-kit/quest/ui_quest_banner_done.png | 192×110 | Sliced | 40,40,40,40 |
| ui_ico_quest | ui-kit/quest/ui_ico_quest.png | 128×128 | Simple | – |
| ui_ico_chest | ui-kit/quest/ui_ico_chest.png | 128×128 | Simple | – |
| ui_progressbar_bg | ui-kit/quest/ui_progressbar_bg.png | 64×24 | Sliced | 12,12,12,12 |
| ui_progressbar_fill | ui-kit/quest/ui_progressbar_fill.png | 64×24 | Sliced | 12,12,12,12 |
| ui_siedlerfeuer_pill | ui-kit/quest/ui_siedlerfeuer_pill.png | 192×80 | Sliced | 40,40,38,38 |
| ui_ico_siedlerfeuer | ui-kit/quest/ui_ico_siedlerfeuer.png | 128×128 | Simple | – |
| ui_tag_siedlerfeuer_x4 | ui-kit/quest/ui_tag_siedlerfeuer_x4.png | 96×48 | Simple | 24,24,22,22 (optional sliced, Standard: Simple 96×48) |
| ui_unitcard_header | ui-kit/army/ui_unitcard_header.png | 128×72 | Sliced | 32,32,32,16 |
| ui_resbar_gradient | ui-kit/resbar/ui_resbar_gradient.png | 4×256 | Simple | – Simple, 1080×250 (+Safe-Top) gestreckt |
| ui_summon_bg_bleed | ui-kit/summon/ui_summon_bg_bleed.png | 1242×2688 | Simple | –(1242×2688 Safe-Bleed) |
| ui_summon_bg | ui-kit/summon/ui_summon_bg.png | 1080×1920 | Simple | – |
| ui_summon_banner_frame | ui-kit/summon/ui_summon_banner_frame.png | 256×192 | Sliced | 48,48,48,48, Fill Center aus |
| ui_btn_rates_info | ui-kit/summon/ui_btn_rates_info.png | 128×128 | Simple | – |
| ui_stamp_new | ui-kit/summon/ui_stamp_new.png | 200×120 | Simple | – |
| ui_ico_shard | ui-kit/summon/ui_ico_shard.png | 64×64 | Simple | – |
| ui_badge_free | ui-kit/summon/ui_badge_free.png | 200×64 | Sliced | 32,32,30,30 |
| ui_pity_fill | ui-kit/summon/ui_pity_fill.png | 64×24 | Sliced | 12,12,12,12 |
| vfx_summon_pillar_common_sheet | ui-kit/vfx/vfx_summon_pillar_common_sheet.png | 1024×2048 | Simple / Sheet | –(4×4 Frames à 256×512, 16 Fr.) |
| vfx_summon_cardflip_common_sheet | ui-kit/vfx/vfx_summon_cardflip_common_sheet.png | 1024×720 | Simple / Sheet | –(4×2 à 256×360, 8 Fr.) |
| vfx_summon_pillar_rare_sheet | ui-kit/vfx/vfx_summon_pillar_rare_sheet.png | 1024×2048 | Simple / Sheet | –(4×4 Frames à 256×512, 16 Fr.) |
| vfx_summon_cardflip_rare_sheet | ui-kit/vfx/vfx_summon_cardflip_rare_sheet.png | 1024×720 | Simple / Sheet | –(4×2 à 256×360, 8 Fr.) |
| vfx_summon_pillar_epic_sheet | ui-kit/vfx/vfx_summon_pillar_epic_sheet.png | 1024×2048 | Simple / Sheet | –(4×4 Frames à 256×512, 16 Fr.) |
| vfx_summon_cardflip_epic_sheet | ui-kit/vfx/vfx_summon_cardflip_epic_sheet.png | 1024×720 | Simple / Sheet | –(4×2 à 256×360, 8 Fr.) |
| vfx_summon_pillar_legendary_sheet | ui-kit/vfx/vfx_summon_pillar_legendary_sheet.png | 1024×2048 | Simple / Sheet | –(4×4 Frames à 256×512, 16 Fr.) |
| vfx_summon_cardflip_legendary_sheet | ui-kit/vfx/vfx_summon_cardflip_legendary_sheet.png | 1024×720 | Simple / Sheet | –(4×2 à 256×360, 8 Fr.) |
| vfx_summon_legendary_zaaap_sheet | ui-kit/vfx/vfx_summon_legendary_zaaap_sheet.png | 2048×1536 | Simple / Sheet | –(4×3 à 512×512, 12 Fr., additiv über Screen) |
| vfx_rarity_shine_epic_sheet | ui-kit/vfx/vfx_rarity_shine_epic_sheet.png | 1024×768 | Simple / Sheet | –(4×3 à 256×256, 12 Fr. Loop, über ui_rarity_epic) |
| vfx_rarity_shine_legendary_sheet | ui-kit/vfx/vfx_rarity_shine_legendary_sheet.png | 1024×768 | Simple / Sheet | –(4×3 à 256×256, 12 Fr. Loop, über ui_rarity_legendary) |
| ui_rarity_shine_mask | ui-kit/vfx/ui_rarity_shine_mask.png | 256×256 | Sliced | 40,40,40,40 (wie Rarity-Rahmen) |
| vfx_instant_build_sheet | ui-kit/vfx/vfx_instant_build_sheet.png | 1280×512 | Simple / Sheet | –(5×2 à 256×256, 10 Fr.) |
| ui_ico_lock | ui-kit/common/ui_ico_lock.png | 128×128 | Simple | – |
| ui_btn_close | ui-kit/common/ui_btn_close.png | 128×128 | Simple | – |
| ui_ico_plus | ui-kit/common/ui_ico_plus.png | 128×128 | Simple | – |
| ui_ico_menu | ui-kit/common/ui_ico_menu.png | 128×128 | Simple | – |
| ui_badge | ui-kit/common/ui_badge.png | 64×64 | Simple | – |
| ui_avatar_frame | ui-kit/common/ui_avatar_frame.png | 192×192 | Simple | – |
| ui_ico_arrow | ui-kit/common/ui_ico_arrow.png | 128×128 | Simple | – |
| ui_ico_skull | ui-kit/common/ui_ico_skull.png | 128×128 | Simple | – |
| ui_ico_star | ui-kit/common/ui_ico_star.png | 128×128 | Simple | – |
| ui_path_dot | ui-kit/common/ui_path_dot.png | 40×40 | Simple | – |
| ui_btn_fab_build | ui-kit/common/ui_btn_fab_build.png | 160×160 | Simple | – |
| ui_ribbon | ui-kit/common/ui_ribbon.png | 320×110 | Sliced | 70,70,0,0 |
| ui_ribbon_white | ui-kit/common/ui_ribbon_white.png | 320×110 | Sliced | 70,70,0,0 |
| ui_filter_chip_active | ui-kit/common/ui_filter_chip_active.png | 160×72 | Sliced | 34,34,34,34 |
| ui_filter_chip | ui-kit/common/ui_filter_chip.png | 160×72 | Sliced | 34,34,34,34 |
| unit_inf | ui-kit/units/unit_inf.png | 256×256 | Simple | – |
| unit_spear | ui-kit/units/unit_spear.png | 256×256 | Simple | – |
| unit_ranged | ui-kit/units/unit_ranged.png | 256×256 | Simple | – |
| unit_cav | ui-kit/units/unit_cav.png | 256×256 | Simple | – |
| unit_siege | ui-kit/units/unit_siege.png | 256×256 | Simple | – |
| unit_support | ui-kit/units/unit_support.png | 256×256 | Simple | – |
| unit_locked | ui-kit/units/unit_locked.png | 256×256 | Simple | – |
| ui_campaign_node_done | ui-kit/campaign/ui_campaign_node_done.png | 160×160 | Simple | – |
| ui_campaign_node_current | ui-kit/campaign/ui_campaign_node_current.png | 160×160 | Simple | – |
| ui_campaign_node_locked | ui-kit/campaign/ui_campaign_node_locked.png | 160×160 | Simple | – |
| ui_campaign_node_boss | ui-kit/campaign/ui_campaign_node_boss.png | 160×160 | Simple | – |
| mock_quest_siedlerfeuer | ui-kit/quest/mock_quest_siedlerfeuer.png | 1080×1920 | – | – |
| mock_unitcard_header | ui-kit/army/mock_unitcard_header.png | 1080×700 | – | – |
| mock_summon_screen | ui-kit/summon/mock_summon_screen.png | 1080×1920 | – | – |
| mock_summon_tutorial | ui-kit/summon/mock_summon_tutorial.png | 1080×1920 | – | – |
| demo_ui_pity_fill | ui-kit/stretch/demo_ui_pity_fill.png | 740×260 | – | – |
| demo_ui_progressbar_fill | ui-kit/stretch/demo_ui_progressbar_fill.png | 660×252 | – | – |
| demo_ui_quest_banner | ui-kit/stretch/demo_ui_quest_banner.png | 660×190 | – | – |
| demo_ui_siedlerfeuer_pill | ui-kit/stretch/demo_ui_siedlerfeuer_pill.png | 400×160 | – | – |
| demo_ui_summon_banner_frame | ui-kit/stretch/demo_ui_summon_banner_frame.png | 1072×640 | – | – |
| demo_ui_unitcard_header | ui-kit/stretch/demo_ui_unitcard_header.png | 540×274 | – | – |
| demo_ui_mission_reinforce_banner | ui-kit/stretch/demo_ui_mission_reinforce_banner.png | 1020×250 | – | – |
| demo_ui_ribbon | ui-kit/stretch/demo_ui_ribbon.png | 660×190 | – | – |
| demo_ui_badge_free | ui-kit/stretch/demo_ui_badge_free.png | 600×160 | – | – |
| mock_summon_sequence | ui-kit/vfx/mock_summon_sequence.png | 1080×700 | – | – |

Vorschau:
- `ui-kit/previews/contact_quest_siedlerfeuer.png`
- `ui-kit/previews/contact_army_resbar.png`
- `ui-kit/previews/contact_summon.png`
- `ui-kit/previews/contact_9slice_stretch.png`
- `ui-kit/previews/contact_vfx.png`
- `ui-kit/previews/contact_common_missing.png`
- `ui-kit/previews/anim_summon_pillar_legendary.gif`
- `ui-kit/previews/anim_instant_build.gif`
- `ui-kit/previews/anim_rarity_shine_legendary.gif`

## Lieferung 2: Missions-Screen „Armee verstärken“ (`mission/`, rev. 14.10.2026 nach AD-Korrektur)
Dezent (dunkles Panel, Blau-Akzent, kein Rot, kein Gold-Kaufbutton/Preis). Platzhalter `{X}`/`{Y}` setzt Dev. CTA `ui_btn_secondary` „Zur Armee“ (Sprungziele Kriegerlager/Heldenlevel/Formation, keine Shop-Links). Anzeige wenn Kampfkraft < `ui_power_hint_below_pct`.

**Speedlines – Pflichtregeln:**
- **Einmalig beim Einblenden, NICHT loopen.** 5 Frames @12 fps ≈ 0,42 s, danach Image deaktivieren (letzter Frame ist leer/ausgeblendet).
- **Layer-Reihenfolge (unten → oben):** Banner-BG (`ui_mission_reinforce_banner`) → Speedlines (`vfx_reinforce_speedlines_sheet`) → Icon → Titel/Kampfkraft-Text → Balken + Marker → Button „Zur Armee“.
- Sheet ist bereits mit `ui_reinforce_speedlines_mask` ausgespart (Icon-, Text/Balken- und Button-Bereich). Maske zusätzlich als UI-Mask/Shader nutzbar, falls das Layout abweicht; weiß = sichtbar. Frame-Raum 640×160 ≙ Banner 980×170 (gestreckt).
- `ui_reinforce_speedlines_overlay.png` (Standbild) entfällt.

| ID | Pfad | Größe | Image Type | 9-Slice L,R,T,B / Hinweis |
|---|---|---|---|---|
| ui_mission_reinforce_banner | ui-kit/mission/ui_mission_reinforce_banner.png | 224×128 | Sliced | 44,44,44,44 |
| ui_ico_reinforce | ui-kit/mission/ui_ico_reinforce.png | 128×128 | Simple | – |
| ui_power_fill | ui-kit/mission/ui_power_fill.png | 64×24 | Sliced | 12,12,12,12 |
| ui_power_marker | ui-kit/mission/ui_power_marker.png | 24×48 | Simple | – (Pivot unten-mitte, auf Empfehlungswert setzen) |
| ui_reinforce_speedlines_mask | ui-kit/mission/ui_reinforce_speedlines_mask.png | 640×160 | Simple | – (640×160, weiß = sichtbar, schwarz = Text/Button/Icon ausgespart) |
| vfx_reinforce_speedlines_sheet | ui-kit/mission/vfx_reinforce_speedlines_sheet.png | 1280×480 | Simple | – (2×3 Raster, 5 Frames à 640×160, 5 Fr. @12 fps ≈ 0,42 s, EINMALIG, kein Loop; bereits maskiert) |
| mock_mission_reinforce | ui-kit/mission/mock_mission_reinforce.png | 1080×1920 | – | Mockup |
| mock_reinforce_speedline_sequence | ui-kit/mission/mock_reinforce_speedline_sequence.png | 1000×970 | – | Mockup |

Vorschau: `ui-kit/previews/contact_mission_reinforce.png`, `ui-kit/previews/anim_mission_reinforce.gif` (spielt einmal)


## Lieferung 3 (14.10.2026): Status-Tags Winter/Hunger, Tutorial-Banner – Stil „heroisch-verspielt“ (Styleguide v0.2)
Status-Tags: Bauweise wie `ui_tag_siedlerfeuer_x4` (Pill 96×48, Outline 4), ruhige Farben (Winter Eisblau `#BFE6F5→#7FB8D9`, Hunger Sand `#F2DFC0→#D9A066`), **kein Alarmrot**. Text per TMP (Baloo EB 28, Outline 3), z. B. „Winter 3:12“, „Hunger“. Empfehlung: `_bg` (textlos, ohne Icon) sliced + Icon als Child-Image 44 px.
Tutorial-Banner E0-UI-SUM-02: aus `ui/heroes/hero_ruka_splash.png` (Vordergrund, 65 %) + `hero_ruka_splash_bg.png` (gespiegelt, weichgezeichnet, abgedunkelt) komponiert; Quelldateien unverändert. Titel/„GARANTIERT“ per TMP in der linken Titelzone (x 40–520).

| ID | Pfad | Größe | Image Type | 9-Slice L,R,T,B / Hinweis |
|---|---|---|---|---|
| ui_ico_winter | ui-kit/resbar/ui_ico_winter.png | 128×128 | Simple | – |
| ui_ico_hunger | ui-kit/resbar/ui_ico_hunger.png | 128×128 | Simple | – |
| ui_tag_winter | ui-kit/resbar/ui_tag_winter.png | 96×48 | Sliced | 48,24,22,22 (Icon im L-Rand) |
| ui_tag_hunger | ui-kit/resbar/ui_tag_hunger.png | 96×48 | Sliced | 48,24,22,22 (Icon im L-Rand) |
| ui_tag_winter_bg | ui-kit/resbar/ui_tag_winter_bg.png | 96×48 | Sliced | 24,24,22,22 |
| ui_tag_hunger_bg | ui-kit/resbar/ui_tag_hunger_bg.png | 96×48 | Sliced | 24,24,22,22 |
| banner_tutorial | ui-kit/summon/banner_tutorial.png | 1032×560 | Simple | – Simple, 1032×560, im Slot unter ui_summon_banner_frame (Rahmen 48 deckt Ränder ab); Titelzone links x 40–520 |
| mock_summon_tutorial | ui-kit/summon/mock_summon_tutorial.png | 1080×1920 | – | Mockup |
| mock_resbar_status_tags | ui-kit/resbar/mock_resbar_status_tags.png | 1080×560 | – | Mockup |

Vorschau: `ui-kit/previews/contact_lieferung3.png`, Mockups `summon/mock_summon_tutorial.png`, `resbar/mock_resbar_status_tags.png`.
Icons: Bei Doppelungen gelten `ui-kit/common/ui_ico_*` für UI; `ui/glyphs/glyph_*` (AD) nur als TMP-Inline-Sprites.


## v002 nach Leitbild „heroisch-verspielt“ (14.10.2026, AD-freigegeben)
Altversionen bleiben unverändert (v001 = Datei ohne Suffix). AD-Panels nur **daneben** als v002 abgelegt, Originale nicht überschrieben.

| ID | Pfad | Größe | 9-Slice L,R,T,B | Änderung |
|---|---|---|---|---|
| ui_avatar_frame_v002 | ui-kit/common/ui_avatar_frame_v002.png | 192×192 | – | Holz #C98B4B statt Gold, kein Glanzstern (Gold nur SSR) |
| ui_btn_fab_build_v002 | ui-kit/common/ui_btn_fab_build_v002.png | 160×160 | – | Glanzstern entfernt |
| ui_ico_chest_v002 | ui-kit/quest/ui_ico_chest_v002.png | 128×128 | – | Glanzstern entfernt |
| ui_ico_siedlerfeuer_v002 | ui-kit/quest/ui_ico_siedlerfeuer_v002.png | 128×128 | – | Glanzstern entfernt |
| ui_panel_light_v002 | ui/panels/ui_panel_light_v002.png | 192×192 | 56,56,56,56 | ohne Nieten (Standard) |
| ui_panel_light_rivets_v002 | ui/panels/ui_panel_light_rivets_v002.png | 192×192 | 56,56,56,56 | dezente Nieten (klein, Ton-in-Ton, ohne Outline) – nur große Panels ≥ ca. 800 px |
| ui_panel_dark_v002 | ui/panels/ui_panel_dark_v002.png | 192×192 | 56,56,56,56 | ohne Nieten (Standard) |
| ui_panel_dark_rivets_v002 | ui/panels/ui_panel_dark_rivets_v002.png | 192×192 | 56,56,56,56 | dezente Nieten – nur große Panels |

Vorschau alt vs. neu: `ui-kit/previews/contact_v002.png`. Generator `tools/ui_art_v002.py`.

## Hinweise
- Soundwords („ZAAAP!“, „ZACK!“) jetzt in **Bangers** (OFL, `ui/fonts/Bangers-Regular.ttf` + `OFL_Bangers.txt`, Quelle github.com/google/fonts/ofl/bangers).
- Summon-Mockups nach summon_rates.csv/summon_banners.csv: `mock_summon_screen.png` = banner_standard (150/1.350, Legendär 2 % Basis, ~2,74 % effektiv, Soft Pity ab 61, Hard 80, Episch spät. alle 10, 10× mind. Episch); `mock_summon_tutorial.png` = banner_tutorial, „GARANTIERT: RUKA“, 10× gratis, keine Raten/Pity-Anzeige.
- Rarity-Mapping **bestätigt (AD, 14.10.2026):** R = Selten (blau `#3B7DDD`), SR = Episch (lila `#8E44D9`), SSR = Legendär (gold `#E7A923`). Gewöhnlich (grau) nur für Items, nicht im Helden-/Beschwörungs-Pool.
- E0-UI-SUM-02: Platzhalter-Slot 1032×560 bleibt; banner_tutorial (Ruka-Splash) liefert der Art Director.

## Offene Punkte
- Kein Changelog in handoff-dev.md; „fehlend“ aus UI_UMSETZUNGSPLAN.md abgeleitet.
- Nicht geliefert: Kartenhintergrund, Gegner-Portraits, Banner-Artworks, finale Einheiten-Portraits (Emblem-Platzhalter), Noto Sans JP.
- Freigabe Stil/Final-Art durch Fabian/Art Director.

## Lieferung 4 (16.10.2026): F5 HUD-Konzept + F3 Dorf-Screen modern v1 (ENTWURF, vor Umsetzung an Fabian)
| ID | Pfad | Größe | Hinweis |
|---|---|---|---|
| HUD_KONZEPT_F5 | ui-kit/hud/HUD_KONZEPT_F5.md | – | Layout, Varianten A/B, Badges, Config-IDs, F3-Punkte, fehlende Icons |
| mock_hud_f5_A | ui-kit/hud/mock_hud_f5_A.png | 1080×1920 | Empfehlung, Pillow, Platzhalter-Icons |
| mock_hud_f5_B | ui-kit/hud/mock_hud_f5_B.png | 1080×1920 | Alternative |
| mock_dorf_modern_v1_pillow | ui-kit/f3/mock_dorf_modern_v1_pillow.png | 1080×1920 | Pillow-Basis (Variante A + Bottom-Sheet) |
| mock_dorf_modern_v1 | ui-kit/f3/mock_dorf_modern_v1.png | 1080×1920 | Nano Banana 2.1 edit (1 Gen, ≈0,064 $), Prompt-Log `prompt-logs/e0_ui_mock_dorf_modern_v1_20261016-063650.json` |
| mock_dorf_modern_v1_nb_raw | ui-kit/f3/mock_dorf_modern_v1_nb_raw_1536x2752.png | 1536×2752 | Roh-Ausgabe |
Vorschau: `previews/contact_hud_f5.png`, `previews/contact_f3_modern.png`. Generatoren `tools/ui_art_hud_f5.py`, `tools/ui_art_f3.py`.

## Lieferung 5 (16.10.2026): HUD-Icons F5 + F3 v2 Vorarbeit (Pillow, keine Gens)
14 Icons `ui-kit/hud/icons/<id>.png`, je 128×128, Pivot Center, kein 9-Slice: ui_ico_event, ui_ico_shop, ui_ico_pass, ui_ico_vip, ui_ico_mail, ui_ico_guild, ui_ico_daily, ui_ico_modes, ui_ico_more, ui_ico_collapse, ui_ico_settings, ui_ico_arena, ui_ico_worldboss, ui_ico_tower.
`ui-kit/f3/mock_dorf_modern_v2_pillow.png` (1080×1920, Bottom-Sheet H 300), `ui-kit/f3/NOTIZ_v2.md`. Vorschau `previews/contact_hud_icons.png` (inkl. 48 px + Graustufen). Generatoren `tools/ui_art_hud_icons.py`, `tools/ui_art_f3_v2.py`.

## Lieferung 6 (16.10.2026): F5 v3 (ersetzt HUD v1 A/B)
`ui-kit/hud/v3/`: MOODBOARD_F5.md, HUD_KONZEPT_F5_v3.md, mock_hud_f5_v3.png (1080×1920), world_f5_v3b.png (NB, verwendet), world_f5_v3.png (NB, verworfen), icons/ui_glyph_*.png (16 Linien-Glyphen 128 px, weiß, per Tint färben). Referenzen intern `team/art/ref/f5/`. Vorschau `previews/moodboard_f5.png`, `previews/contact_hud_f5_v3.png`. Generator `tools/ui_art_hud_v3.py`. 2 Nano-Banana-Gens (≈0,12 $).


## Lieferung 7 – F5 HUD v5.4 Stil C (freigegeben, 2026-10-16)
- Mockups: `hud/v5/mock_hud_f5_v5_4_C.png`, `hud/v5/mock_hud_f5_v5_4_C_ressourcen.png`. Vorschau: `previews/contact_hud_f5_v5.png`.
- Export: `hud/v5/export/` mit 36 Sprites `hud_c_*`, `hud_layout.csv` und `HANDOFF_DEV_UI.md`.
- IDs: Rahmen `hud_c_frame_{panel,pill,pill_slim,sheet,tile}`, `hud_c_sheet_handle`, `hud_c_tab_{normal,active}`, `hud_c_btn_{plus,close}`, `hud_c_badge_{dot,level}`, `hud_c_avatar_ring`, `hud_c_bar_{track,fill}`, `hud_c_evt_mammutjagd`, Icons `hud_c_ico_{kristall,gold,slot3,ressourcen,events,shop,pass,mehr,dorf,armee,bauen,helden,karte,holz,stein,nahrung,einwohner,vorrat,felle,fackel}`.
- 9-Slice: pill 190/170/190/170, pill_slim 85/75/85/75, panel und sheet 65, tile 100, bar_track 8/6/8/6, bar_fill 6/0/6/0.
- Quellen: 5 Nano-Banana-Gens (`e0_ui_hud_v5_*` im Register), Skripte `tools/ui_art_hud_v5*.py`. Bauen ist ein normaler Tab.


## Lieferung 7.1 – F5 HUD v5.5 (2026-10-16, nur Skript)
- Dritter Top-Slot = Wissen: `hud/v5/export/hud_c_ico_wissen.png` (Skript `tools/ui_art_hud_v5_wissen.py`: Steintafel aus der ico_slot3-Textur, leuchtende Rune, Verlauf, Kontur, Glanz). `hud.currency_3 = wissen`.
- Badges nur am Events-Einstieg und an den Tabs Armee/Helden, kein Badge am Pass (CSV, Handoff, Mock).
- Pillen 262 px, Auto-Size 30–40, Messwerte im Handoff.
- Mockups: `hud/v5/mock_hud_f5_v5_5_C.png`, `hud/v5/mock_hud_f5_v5_5_C_ressourcen.png`. Vorschau: `previews/contact_hud_f5_v5.png`.
- 7.1 Nachtrag: `hud_c_ico_wissen` jetzt per Nano Banana (1 Gen, Skript-Version `hud_c_ico_wissen_alt`). Zahlformat in den Pillen K/M/B (`hud.number_format.pill`/`.tooltip`), Auto-Size min. 28. Iconset-Plan je Epoche: `hud/v5/ICONSET_EPOCHEN.md`, CSV-Spalte `iconset`, Key `epochs[].hud_iconset`.
- 7.1 Nachtrag 2: hud_c_ico_quest, hud_c_ico_forschung, hud_c_ico_einstellungen (1 Gen), Basis-Set eiszeit vollständig.

- Lieferung 7.2 (v5.6, nur Skript, Kosten 0 $): Mockups `hud/v5/mock_hud_f5_v5_6_C_{frueh,spaet,ressourcen}.png`, Vorschau `previews/contact_hud_f5_v5.png` (3 Zustände). Unlock-Schema `unlock.<element_id>` in CSV und Handoff, Shop/Pass auf 64 px zurückgenommen, Beispielwerte statt ###, Gold als Epochen-Skin (Muschel-Gen offen).

- Lieferung 7.3 (v5.7, 1 Gen, ca. 0,07 $): Tooltip-Mock Währungen, Event-Kachel einklappbar (`hud.event_tile.collapsed`), Kerbe und Unterstrich am aktiven Tab. Neue Icons `hud_c_ico_{gold_eiszeit,gold_e2,bauen,armee}` (alte als `_alt`). Mockups `hud/v5/mock_hud_f5_v5_7_C_{frueh,spaet,tooltip,ressourcen}.png`, `hud/v5/tooltips_topbar_v5_7.png`, Vorschau `previews/contact_hud_f5_v5.png`.

- Lieferung 7.4 (17.10., v5.7 final, nur Skript, 0 $): Shop, Pässe/VIP und Angebote als ein Rand-Icon mit dezentem Punkt; Login-Kalender und Gratis gleich groß (Skript-Icons; Gen erledigt in 7.5); keine Login-Pop-ups, keine blinkenden Countdowns, max. 1 Angebots-Banner, U18 ohne Countdown. Mockups `hud/v5/mock_hud_f5_v5_7_C_final_{frueh,spaet,tooltip,ressourcen}.png`, Vorschau `previews/contact_hud_f5_v5.png`.
- Mock-Welt v5.7 final: `ui/village/e1_village_bg_stilA_v1.png` (AD-abgenommen), als 9:16-Ausschnitt. Tausch auf v2 über `HUD_WORLD_FILE=ui/village/e1_village_bg_stilA_v2.png python3 tools/ui_art_hud_v5.py` (Mitte über `HUD_WORLD_CX`/`HUD_WORLD_CY`).

- Lieferung 7.5 (17.10., v5.7 final mit Auflagen, 1 Gen, ca. 0,064 $): Dock mit 96-px-Platten, 60-px-Icons, Label 24 px, Trefferfläche 144×144 (= 48 dp); Login, Gratis und Shop gleich groß. Mock früh mit Spielerlevel 3. Grünes Plus an Kristallen nur bei `unlock.hud_dock_shop` erfüllt und nicht U18. Event-Kachel mit neutralem Platzhalter `export/hud_c_evt_platzhalter.png` (ohne Mammut). Neue Icons `export/hud_c_ico_{login_kalender,gratis}.png` aus Gen `e0_ui_hud_v5_7_login_gratis` (Kerbholz, Vorratstopf; kein Metall, kein Stoff); Skriptfassungen als `_alt`. Mocks `hud/v5/mock_hud_f5_v5_7_C_final_{frueh,spaet,tooltip,ressourcen}.png`, Vorschau `previews/contact_hud_f5_v5.png`.

- Lieferung 7.6 (17.10., AD-Abnahme, nur Skript, 0 $): `hud_c_ico_gratis` ohne Getreideähren (kein Ackerbau in E1; `tools/ui_art_fx_gratis_ohne_aehren.py`), Event-Platzhalter mit grau-braunen Federn (`tools/ui_art_fx_naturfedern.py`). Die alten Fassungen liegen in `hud/v5/backup_v75/`. Login, Gratis und Platzhalter sind abgenommen AD. Lieferung 1–3 (17 Dateien) ist als Stil-alt, Redo F7+ markiert. Übergabe an Dev UI: `team/producer/apk_1710/uebergabe_art_ui_dev_ui.md`.
- Lieferung 7.7 (17.10., nur Skript, 0 $): `hud_c_ico_events` mit grau-braunen Federn (`tools/ui_art_fx_naturfedern.py`), vorher in `hud/v5/backup_v75/hud_c_ico_events_v001_federn.png`. Mocks und Vorschau neu.
