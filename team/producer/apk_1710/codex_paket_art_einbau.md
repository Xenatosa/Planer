> ⛔ HUD v5.7 ist gestrichen (Fabian 22.10.2026), gültig ist D2 Obsidian & Glut + Dock A braun. Gesamtes HUD v5 (inkl. Icons `hud_c_ico_*`, `HudV5NumberFormat`) ist gestrichen; Dorf-HUD und Icons werden neu in D2 erstellt. Vorlage: `team/art/GUELTIG.md`.

Ergebnis: team/producer/apk_1710/codex_paket_art_einbau.md (P3 Art-Einbau APK 17.10., VORVERSION 09:00, final 13:15 per eigener Routine)
Kosten: keine bisher (ein Codex-Lauf über New Bot, kein Bild-/Gen-Budget)
Kritiker: n/a (Einbau abgenommener Art, kein neuer Entwurf)
Geprüft von: Epochen Dev UI (Abgleich asset-register.csv, e1_buildings_bp_manifest.json v6, art_umgebung_center.json v2, dev_ui_eingang.md bis 08:54)
Offene Fragen: Lücken siehe Abschnitt 8 (Paket 4 Tauschplatz/Palisade in_review, Dorfboden v2 in_review, Boden-Platzierung, Plattenmaß 252 vs. 256 px)
Nächster Empfänger: New Bot (Codex-Start nach #96 und F6), Kopie Art Director
Regel: Keine Bestätigungs-/Danke-Nachrichten, keine reinen Status-Nachrichten.

# Codex-Paket P3: Art-Einbau für die Test-APK 17.10.
Absender: Epochen Dev UI · Repo Xenatosa/epodarien · Modell Codex GPT-6 Luna, Extra High
Branch: `ui/art-einbau-apk` · ein PR · Merge durch New Bot bei grünen Checks
Reihenfolge: startet erst, wenn #96 (HUD v5.7, inkl. Job 24) und F6 (`ui/bau-panel-fix`) auf main sind (siehe codex_ui_apk.md A/B). Branch von main NACH diesen Merges abzweigen.
Quelle aller Dateien: `/workspace/handygame-plan/team/art/…` (unten als `art/…`). Nur die hier gelisteten Dateien übernehmen. Alles, was nicht `approved`/`final`/`freigegeben` ist, bleibt draußen.

## 0. Nicht in diesem PR
- Die 9 HUD-v5.7-Dateien (hud_layout.csv, HANDOFF_DEV_UI.md, hud_c_ico_gold/wissen/events, hud_c_ico_login_kalender, hud_c_ico_gratis, hud_c_evt_platzhalter, hud_c_dot_soft) laufen über #96/Job 24.
- Verboten: `e1_bld_center_bp*_v003`, `e1_bld_center_bp10_v004`, alle `*_ki_v00x`, alle `bp*_v001` von quarry/storage/hut/woodcutter (ersetzt durch v002), `hero_ruka_splash_bg.png`, `hero_ruka_splash_bg_empty_v002.png`, alles unter `_anime_verworfen/`, `_verworfen/`, `_v001/`, `_v002/`, alle `_alt`-Dateien, `ui_btn_fab_build`, E2-Boden (entfällt heute).
- Kein Rig, keine Splash-Ebenen/Speedlines (kommen in F7).

## 1. Gebäude-Tausch per Override-Tabelle (Pflicht, Vorgabe AD)
### 1.1 Config
- Neue Keys in game_config.csv, in BEIDEN Kopien (`Assets/StreamingAssets/RemoteConfig/` und `Assets/_Project/Data/CSV/`), plus Default in `RemoteConfigValues.cs`:
  `buildings.sprite_override.<building_id>.bp<nn> = <sprite_id>`
  - `<building_id>` exakt wie in buildings.csv (z. B. `bld_center`; Codex prüft die IDs gegen buildings.csv), `<nn>` zweistellig wie im Dateinamen (bp01, bp03, bp04 …). Der Parser akzeptiert beliebige Breakpoint-Nummern (Tauschplatz nutzt 1/3/5).
  - Leerer Wert = kein Override.
### 1.2 Logik (neuer Resolver, z. B. `BuildingSpriteResolver` unter Assets/_Project/Scripts/UI/Village/)
- Eingabe: building_id, Gebäudestufe. Kandidaten = alle bp-Keys dieses Gebäudes mit gesetztem Wert UND auffindbarem Sprite. Gezeigt wird der Kandidat mit der höchsten bp-Nummer ≤ Stufe.
- Kein Kandidat (Key fehlt, Wert leer, Datei fehlt, alle bp > Stufe) → bisheriges prozedurales Sprite (`e1_bld_<id>_std_l<n>_v00x` bzw. aktueller Placeholder). Dabei KEIN `Debug.LogWarning`/`LogError` und kein missing-Sprite: Lookup über eine Try-Variante (`TryGetSprite` o. ä.), die still null liefert.
- Der Resolver wird überall genutzt, wo heute das Gebäude-Sprite gesetzt wird: Dorf (iso), Bau-Panel/BuildingCard-Preview (F6) und BuildingInfoPanel-Portrait. Beim Stufenwechsel neu auflösen.
- Neues Sprite: Pivot 0.5/0 sitzt auf der unteren Footprint-Spitze (Ecke (u0+n, v0+n), siehe handoff-dev.md Kap. 4). Keine Skalierung, kein Offset. Sorting wie bisher (Sorting Group je Gebäude, Custom Axis 0/1/0).
### 1.3 Tabelle (Stand 09:00)
| building_id | Footprint | bp01 | bp04 | bp07 | bp10 | Status |
|---|---|---|---|---|---|---|
| bld_center | 4×4 | e1_bld_center_bp01_v005 | e1_bld_center_bp04_v005 | e1_bld_center_bp07_v005 | e1_bld_center_bp10_v005 | final (AD 17.10., Pivot-Fix), 1304×1538 RGBA, Plattenspitze x 652 |
| bld_quarry | 3×3 | e1_bld_quarry_bp01_v002 | …bp04_v002 | …bp07_v002 | …bp10_v002 | approved (AD 17.10.), 1040×1063 |
| bld_storage | 3×3 | e1_bld_storage_bp01_v002 | …bp04_v002 | …bp07_v002 | …bp10_v002 | approved, 1024×935 |
| bld_hut | 2×2 | e1_bld_hut_bp01_v002 | …bp04_v002 | …bp07_v002 | …bp10_v002 | approved, 696×574 |
| bld_woodcutter | 2×2 | e1_bld_woodcutter_bp01_v002 | …bp04_v002 | …bp07_v002 | …bp10_v002 | approved, 672×947 |
| bld_gatherer | 2×2 | e1_bld_gatherer_bp01_v001 | …bp04_v001 | …bp07_v001 | …bp10_v001 | approved, 568×455 |
| bld_barracks | 3×3 | e1_bld_barracks_bp01_v001 | …bp04_v001 | …bp07_v001 | **kein Key anlegen** | approved, 1008×723; ab Stufe 10 bleibt bp07 (AD bestätigt) |
| bld_shell_beach | 2×2 | e1_bld_shell_beach_bp01_v001 | …bp04_v001 | …bp07_v001 | …bp10_v001 | approved, 712×521 |
| bld_hunter | 2×2 | e1_bld_hunter_bp01_v001 | …bp04_v001 | …bp07_v001 | …bp10_v001 | approved, 608×417 |
| bld_shaman_hut | 3×3 | e1_bld_shaman_hut_bp01_v001 | …bp04_v001 | …bp07_v001 | …bp10_v001 | approved, 1096×993 |
| bld_trader | 3×3 | (leer) bp01 | (leer) bp03 | (leer) bp05 | – | LÜCKE: e1_bld_trader_bp{01,03,05}_v001 in_review (Paket 4) |
| bld_palisade (gerades Stück) | 1×1 | (leer) | (leer) | (leer) | (leer) | LÜCKE: e1_bld_palisade_bp{01,04,07,10}_v001 in_review (Paket 4) |
| bld_palisade_{corner,end,tee,cross,gate} | 1×1 | (leer) | (leer) | (leer) | (leer) | keine Assets, Zeilen nur reserviert; Autotile bleibt prozedural |
- „…bpNN_vK“ = gleicher Präfix wie in der Zeile, z. B. `e1_bld_quarry_bp04_v002`.
- Werden trader/palisade bis 13:00 abgenommen, trägt die finale Version (13:15) die Werte nach; dann nur Config + Dateien ergänzen, keine Code-Änderung.
- Quelle: `art/ui/buildings/<sprite_id>.png`, Pivots/Footprints verbindlich aus `art/ui/buildings/e1_buildings_bp_manifest.json` (v6) bzw. `team/producer/apk_1710/art_umgebung_center.json`.

## 2. Import-Vorgaben (für alle Welt-Sprites)
- Texture Type Sprite (2D and UI), Single, PPU 256, Mesh Type Full Rect, keine Mips, Wrap Clamp, Filter Bilinear, Max Size 2048, Format ASTC 6x6 (Android-Override), sRGB an, Alpha is Transparency an (bei RGBA).
- Pivot Custom: Gebäude (0.5, 0); Chibis (0.5, 0.0859) laut `art/ui/heroes/battle/pivots.json`, Schatten gleicher Pivot; Porträts und Splash (0.5, 0.5).
- Atlanten im bestehenden Ordner `ArtPipeline/UISpriteAtlases` (genauen Pfad im Repo suchen), Sprite Atlas v2, Allow Rotation AUS, Tight Packing aus, Padding 4, Max 2048², Include in Build an:
  - `atlas_bld_e1_<building_id>` je Gebäude (Zentrum ergibt mehrere Seiten, das ist ok).
  - `atlas_hero_<hero_id>` je Held: battle + battle_shadow + portrait + portrait_alpha. Passt es nicht auf eine Seite, sind 2 Seiten erlaubt, nie > 2048².
  - `atlas_village_bg_e1` für die Boden-Chunks (eigener Atlas, 1 Chunk je Seite).
  - Ruka-Splash: KEIN Atlas, Einzeltextur (1024×1536, Max Size 2048, ASTC 6x6).
- UI-Sprites (Abschnitt 6) bleiben bei den UI-Regeln aus handoff-dev.md: PPU 100, 9-Slice-Border laut Tabelle, ASTC 6x6, in die bestehenden UI-Atlanten.

## 3. Zielordner im Repo
Bevorzugt die bestehende Konvention von SpriteCatalog/SpriteKeys übernehmen (Codex prüft zuerst, wie Sprites heute per ID geladen werden). Wenn per Resources geladen wird:
| Art | Quelle (art/…) | Ziel |
|---|---|---|
| Gebäude-Breakpoints | ui/buildings/e1_bld_<id>_bp<nn>_v<k>.png | Assets/_Project/Resources/Art/Buildings/E1/ (Dateiname = sprite_id) |
| Chibis + Schatten | ui/heroes/battle/hero_<id>_battle{,_shadow}.png, pivots.json | Assets/_Project/Resources/Art/Heroes/Battle/ (pivots.json nur als Doku nach docs/team/art/) |
| Porträts | ui/heroes/hero_<id>_portrait{,_alpha}.png | Assets/_Project/Resources/Art/Heroes/Portraits/ |
| Ruka-Splash | ui/heroes/hero_ruka_splash.png | Assets/_Project/Resources/Art/Heroes/Splash/ |
| Dorfboden-Chunks | ui/village/e1_village_bg_stilA_v2_chunk_r{0-2}_c{0-2}.png + _chunks.json | Assets/_Project/Resources/Art/Village/E1/ |
| UI Stil-alt (17) | ui-kit/<ordner>/<datei>.png | Assets/_Project/Art/UI/<ordner>/ (wie Lieferung 1–7 auf main) |
Placeholder unter `Assets/_Project/Art/Buildings/E1/bld_*.png` NICHT löschen (sind Fallback).

## 4. Helden (Stil A, 2D-Comic, alle vom AD abgenommen)
IDs: ruka, terwish, bako, gorm, mira, tala, olm, kiko, nara.
| Asset | Dateien | Zuordnung | Fallback |
|---|---|---|---|
| Porträt | hero_<id>_portrait.png (256² RGB), hero_<id>_portrait_alpha.png (256² RGBA) | SpriteKeys `hero_<id>_portrait` / `hero_<id>_portrait_alpha` → Heldenliste, Aufstellungs-Vorschau (Block-Karten), General-Button (runde Maske nutzt _alpha) | bisheriges Default-/Placeholder-Porträt, still (keine Warnung) |
| Chibi | hero_<id>_battle.png + _battle_shadow.png (1024² RGBA) | SpriteKeys `hero_<id>_battle` / `hero_<id>_battle_shadow` in der Battle-View (#105); Schatten als Kind-Renderer, gleicher Pivot, SortingOrder Figur −1 | bisheriges Kampf-Sprite |
| Ruka-Splash | hero_ruka_splash.png (1024×1536, vollflächig) | RukaSplashLayout zeigt EIN Bild. bg-Ebene deaktivieren bzw. Referenz entfernen, ohne Missing-Warnung. hero_ruka_splash_bg darf nicht mehr im Build referenziert sein. | – (Datei vorhanden) |
Register: die neuen `_typA`-Zeilen sind `freigegeben`; ältere Zeilen `hero_*_battle` mit `in_review` sind durch die AD-Abnahme 08:26 überholt (gleiche Dateinamen).

## 5. Dorfboden (Hintergrund)
- Neuer Key `village.background_sprite` (beide game_config-Kopien + RemoteConfigValues). Wert heute: `e1_village_bg_stilA_v2` (approved AD 17.10.). Leer → alter Boden, still.
- Umsetzung: 3×3 Chunks à 1365² (RGB, ohne Alpha) laut `e1_village_bg_stilA_v2_chunks.json` (Ursprung oben links, r=Zeile, c=Spalte) als Hintergrund-Layer HINTER dem Iso-Gitter, eigene Sorting Layer unter den Tiles, PPU 256, Pivot (0, 1). Zentriert auf den Dorfmittelpunkt (Zentrum-Footprint), Tiles bleiben darüber sichtbar.
- Kein Austausch der Iso-Tiles, keine Gebäude-Entfernung. Volle Integration bleibt F7.
- Wird v2 bis 13:00 abgenommen, setzt die finale Version den Wert auf `e1_village_bg_stilA_v2` (gleiches Raster).

## 6. UI Stil-alt (17 Dateien, außerhalb HUD, „Redo F7+“)
Quelle `art/ui-kit/…`, 9-Slice L,R,T,B:
quest/ui_progressbar_bg (12,12,12,12), quest/ui_progressbar_fill (12,12,12,12), quest/ui_siedlerfeuer_pill (40,40,38,38), quest/ui_tag_siedlerfeuer_x4 (24,24,22,22), army/ui_unitcard_header (32,32,32,16), summon/ui_summon_banner_frame (48,48,48,48), summon/ui_btn_rates_info (–), summon/ui_badge_free (32,32,30,30), summon/ui_pity_fill (12,12,12,12), common/ui_btn_close (–), common/ui_badge (–), common/ui_ribbon_white (70,70,0,0), mission/ui_mission_reinforce_banner (44,44,44,44), mission/ui_power_fill (12,12,12,12), mission/ui_power_marker (–), resbar/ui_tag_winter (48,24,22,22), resbar/ui_tag_hunger (48,24,22,22).
Nur dort verdrahten, wo der Screen heute schon einen Platzhalter mit gleicher ID nutzt. Im HUD gelten die hud_c_-Varianten.

## 7. Abnahme
1. EditMode-Test `BuildingSpriteResolverTests`:
   - Key gesetzt + Datei vorhanden → neues Sprite (Name = sprite_id).
   - Breakpoint-Auswahl bld_center: Stufe 1 → bp01, Stufe 5 → bp04, Stufe 10 → bp10.
   - bld_barracks Stufe 10 → bp07 (kein bp10-Key).
   - Key leer → prozedurales Sprite; Key gesetzt, Datei fehlt → prozedurales Sprite; jeweils `LogAssert.NoUnexpectedReceived()`.
2. EditMode: `village.background_sprite` leer → alter Boden, keine Logs.
3. Keine missing-/Warn-Logs im Test-Build (Dorf, Bau-Panel, Heldenliste, Aufstellung, Ruka-Splash einmal durchklicken, Logcat prüfen).
4. CI grün (EditMode, PlayMode, Gitleaks), kein Test gelöscht oder übersprungen, android.yml unverändert.
5. Emulator-Screenshots 1080×1920 in den PR: Dorf (Zentrum + mindestens 3 neue Gebäude sichtbar, Boden), Bau-Panel, Heldenliste, Aufstellung (combat_v2_enabled an, falls Abschnitt E aus codex_ui_apk.md gemergt ist; sonst vermerken).
6. Kein Atlas > 2048², kein Sprite rotiert, Padding 4.

## 8. Lücken (Stand 09:00)
- bld_trader bp01/03/05 und bld_palisade bp01/04/07/10: Dateien da, aber in_review (Paket 4). Zeilen leer bis Abnahme; sonst prozedural.
- Palisaden-Autotile-Teile (corner/end/tee/cross/gate): keine Stil-A-Assets, bleiben prozedural.
- Dorfboden: v1 approved und eingeplant, v2 in_review. Art hat keine Vorgabe zu Platzierung/Skalierung des Bodens zum Iso-Gitter (Mittelpunkt, Maßstab, Verhältnis zu `village.tile_spacing` +15 % aus F6). Vorschlag Dev UI: zentriert auf das Zentrum, PPU 256, keine Skalierung.
- Plattenmaß laut Manifest 252 px je Tile, Iso-Gitter 256 px je Tile (PPU 256): Gebäudeplatten sind ca. 1,6 % kleiner als der Footprint. Vorschlag: so lassen, keine Skalierung.
- Iso-Tiles, Deko und E2 bleiben prozedural/interim (kein Stil A vorhanden).
- Splash anderer Helden: keine (nicht nötig für die APK).

## Nachtrag 09:01 (Dev UI)
- Für den Dorfboden gilt v2 (e1_village_bg_stilA_v2.png plus 9 Chunks laut e1_village_bg_stilA_v2_chunks.json); die Retusche hat der AD beauftragt.
- Werkplatz und Höhlenwohnung bekommen per Config-Offset `village.plot_offset.<bld_id> = du;dv` etwa 1 Kachel nach rechts, damit sie nicht in den Wald ragen. Die Standorte berechnet IsoMap.Layout; das Offset kommt dort hinzu, Default 0;0. Kontrollbild: review/e1_village_bg_stilA_v2_slots.png.
- HUD-Icons und Avatar regeln Job 24/25 auf ui/hud-v5-7-nachtrag. In diesem Paket nichts am HUD ändern.

## FREIGABE 09:30 (Dev UI): Alle Art-Lieferungen für P3 sind vom AD abgenommen
Verbindliche Quelle für Pfade, Pivots und Sonderregeln ist team/producer/apk_1710/dev_ui_eingang.md (alle Einträge ab 08:18). Bei Widerspruch gilt der neuere Eintrag. Kurz zusammengefasst:
- Zentrum v005, Gebäude-Pakete 1–4 (11 Gebäude) per Override-Tabelle. Palisade mit Achse a/b (_mirror), bp10_v002. barracks hat keinen bp10-Eintrag.
- Boden e1_village_bg_stilA_v2 plus 3×3 Chunks, zentriert auf dem Zentrum, PPU 256, ohne Skalierung. village.plot_offset für Werkplatz und Höhlenwohnung +1 Kachel nach rechts.
- Tiles nur aus env_e1_stilA_manifest.json v2 (NICHT aus dem Basis-Manifest), Fallback env_e1_manifest.json.
- Deko aus deco_e1_stilA_manifest.json v2. Pivot liegt auf der Kachelmitte ohne den alten +64-px-Versatz, die Schatten-Pivots kommen aus dem Manifest.
- Helden: 9 Chibis plus Schatten, 9 Porträts (RGB/alpha), Ruka-Splash v002 als ein einziges Bild. Die alten bg-Dateien nicht verwenden.
- Art UI: die 17 Übergangsdateien laut art_ui_assets.md (außerhalb des HUD). Das HUD selbst läuft über #127.
