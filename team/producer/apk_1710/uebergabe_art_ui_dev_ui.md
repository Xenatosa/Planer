> ⛔ HUD v5.7 ist gestrichen (Fabian 22.10.2026), gültig ist D2 Obsidian & Glut + Dock A braun. Gesamtes HUD v5 (inkl. Icons `hud_c_ico_*`, `HudV5NumberFormat`) ist gestrichen; Dorf-HUD und Icons werden neu in D2 erstellt. Vorlage: `team/art/GUELTIG.md`.

Ergebnis: team/producer/apk_1710/uebergabe_art_ui_dev_ui.md (HUD v5.7 final für PR #96)
Kosten: 1 Gen ca. 0,064 $ (Lieferung 7.5); AD-Fixes und Events-Icon nur Skript, 0 $
Kritiker: geprueft ja (Auflagen 1–3 erledigt)
Geprüft von: geprüft Art Director (17.10.), Epochen Kritiker
Offene Fragen: keine
Nächster Empfänger: Dev UI (PR #96, Branch ui/hud-v5)
Regel: Keine Bestätigungs-/Danke-Nachrichten, keine reinen Status-Nachrichten.

# Übergabe Art UI → Dev UI: HUD v5.7 final (17.10.2026)
Quelle lokal: `team/art/ui-kit/hud/v5/export/`. Zielpfade wie bisher in PR #96. Abgleich per Git-Blob-SHA gegen PR #96 (Stand heute, nur lesend). Insgesamt 9 Dateien nachreichen: 5 Updates + 4 neue. Volle Asset-Liste: `team/producer/apk_1710/art_ui_assets.md`.

## 1. Veraltet in PR #96 – Update auf v5.7 (5)
| Datei | Quelle (team/…) | Ziel im PR | Was ist neu |
|---|---|---|---|
| HANDOFF_DEV_UI.md | art/ui-kit/hud/v5/export/HANDOFF_DEV_UI.md | Assets/Art/UI/HUD/v5/HANDOFF_DEV_UI.md | Abschnitte v5.7 FINAL + Auflagen (Dock 96/60/144, Plus-Bindung, Event-Platzhalter) |
| hud_layout.csv | art/ui-kit/hud/v5/export/hud_layout.csv | Assets/_Project/Resources/HUD/v5/hud_layout.csv | Dock-Positionen und -Größen neu, `hud_dock_pass` raus, Plus-Bindung, Event-Platzhalter, neue cfg-Zeilen |
| hud_c_ico_gold.png | art/ui-kit/hud/v5/export/hud_c_ico_gold.png | Assets/Art/UI/HUD/v5/hud_c_ico_gold.png | neuere Fassung (Fallback-ID; Skin über Iconset → gold_eiszeit) |
| hud_c_ico_wissen.png | art/ui-kit/hud/v5/export/hud_c_ico_wissen.png | Assets/Art/UI/HUD/v5/hud_c_ico_wissen.png | neuere Fassung |
| hud_c_ico_events.png | art/ui-kit/hud/v5/export/hud_c_ico_events.png | Assets/Art/UI/HUD/v5/hud_c_ico_events.png | 9. Datei: Federn grau-braun statt bunt (Skript `tools/ui_art_fx_naturfedern.py`), gleiche Größe 247×256 |

## 2. Neu in v5.7 – nachreichen (4, alle einbauen)
| Datei | Quelle (team/…) | Ziel im PR | Größe px | Inhalt |
|---|---|---|---|---|
| hud_c_ico_login_kalender.png | art/ui-kit/hud/v5/export/hud_c_ico_login_kalender.png | Assets/Art/UI/HUD/v5/hud_c_ico_login_kalender.png | 256×256 | Login-Kalender (Kerbholz), Gen, abgenommen AD |
| hud_c_ico_gratis.png | art/ui-kit/hud/v5/export/hud_c_ico_gratis.png | Assets/Art/UI/HUD/v5/hud_c_ico_gratis.png | 256×256 | Gratis (Vorratstopf ohne Ähren), Gen + Skript-Fix, abgenommen AD |
| hud_c_evt_platzhalter.png | art/ui-kit/hud/v5/export/hud_c_evt_platzhalter.png | Assets/Art/UI/HUD/v5/hud_c_evt_platzhalter.png | 645×460 | neutraler Event-Platzhalter (Trommel, Federn grau-braun), abgenommen AD |
| hud_c_dot_soft.png | art/ui-kit/hud/v5/export/hud_c_dot_soft.png | Assets/Art/UI/HUD/v5/hud_c_dot_soft.png | 18×18 | dezenter Punkt (gold, 18 px) für Shop und Gratis |

Nicht einbauen (liegen lokal nur als Referenz): `hud_c_ico_login_kalender_alt.png`, `hud_c_ico_gratis_alt.png`, `hud_c_ico_armee_nieten.png`.
Optional (Doku/Vorschau): `team/art/ui-kit/hud/v5/ICONSET_EPOCHEN.md` (wird in hud_layout.csv referenziert) und `team/art/ui-kit/previews/contact_hud_f5_v5.png`. Die Vorschau ersetzt `Assets/Art/UI/HUD/v5/hud_v5_7_compose_preview.png`.

## 3. Config- und Unlock-Änderungen (game_config.csv, Kurzform)
- `dock.order`: `events;shop;pass;mehr` → **`events;login;gratis;shop;mehr`**
- `unlock.hud_dock_pass` **streichen**. `unlock.hud_dock_shop` = `{type: level, value: 6}` bleibt (Vorschlag) und bündelt Shop, Pässe/VIP und Angebote. Default gesperrt, U18 immer aus.
- `unlock.hud_dock_login` und `unlock.hud_dock_gratis`: kein Key = sichtbar (ab Start).
- Plus an Kristallen (`hud.currency_1.shop`): nur sichtbar, wenn `unlock.hud_dock_shop` erfüllt ist UND NICHT `player.u18`. `HudUnlockRules.IsCurrencyShopButtonVisible` im PR macht das schon so. Die Pille bleibt gleich breit.
- `events.featured`: `mammutjagd` → **`platzhalter`** (Sprite `hud_c_evt_platzhalter`). Echte Events tauschen per `hud_c_evt_<event_id>`.
- Neue Keys: `hud.login_popups = 0` (keine Pop-ups beim Login), `hud.countdown.blink = false` (U18: keine Angebots-Countdowns), `offers.banner_max = 1`, `badges.soft.<id>` (dezenter Punkt, max. 1 je Icon, kein Rot, keine Zahl).
- Dock-Layout: Platte 96×96, Icon 60 px (Mehr 50), Label 24 px, Trefferfläche 144×144 (= 48 dp), Abstand 144. Anker oben rechts x 20, y 212/356/500/644/788. Gesperrte Einträge fallen weg, die übrigen rücken nach oben.

## 4. hud_dock_pass / hud_c_ico_pass entfernen
- `Assets/Art/UI/HUD/v5/hud_c_ico_pass.png` aus PR #96 nehmen. Der Pass liegt jetzt als Reiter im Shop, im HUD gibt es kein eigenes Pass-Icon.
- Zeile `hud_dock_pass` ist in der neuen `hud_layout.csv` schon raus. `dock.order` ohne `pass` (siehe 3).
- `HudUnlockRules.cs`: `hud_dock_pass`/`hud_pass` in `IsOffer` (Z. 52/54) und den Alias `unlock.hud_pass` (Z. 62) streichen oder als toten Fallback stehen lassen. Pässe/VIP folgen nur noch `unlock.hud_dock_shop`.
- `ui_strings.csv`: `hud.v5.dock.pass` und `hud.v5.message.pass` streichen. **Neu:** `hud.v5.dock.login,Login,Login` und `hud.v5.dock.gratis,Gratis,Free` (fehlen im PR).
- `_alt`-Dateien im PR ebenfalls nicht einbauen: `hud_c_ico_armee_alt`, `hud_c_ico_bauen_alt`, `hud_c_ico_gold_muenze_alt`, `hud_c_ico_wissen_alt`.
- `hud_c_evt_mammutjagd.png` kann als Event-Illu für ein späteres Mammut-Event bleiben, ist aber nicht mehr Default.
