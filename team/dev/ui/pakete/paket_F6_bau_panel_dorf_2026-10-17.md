> ⛔ HUD v5.7 ist gestrichen (Fabian 22.10.2026), gültig ist D2 Obsidian & Glut + Dock A braun. Gesamtes HUD v5 (inkl. Icons `hud_c_ico_*`, `HudV5NumberFormat`) ist gestrichen; Dorf-HUD und Icons werden neu in D2 erstellt. Vorlage: `team/art/GUELTIG.md`.

# Codex-Paket F6: Bau-Panel-Bugs + Dorf-Abstand (17.10.2026)
Branch: `ui/bau-panel-fix` (von main, NACH Merge von #96). Repo Xenatosa/epodarien. Modell: Codex GPT-6 Luna, Extra High.

## Ziel
Sichtbare Bugs aus Fabians Emulator-Test (main f012309) beheben, die #96 (HUD v5.7) nicht abdeckt.

## Aufgaben
1. Ausbauen-Button: Kosten-Zahlen laufen über den Button hinaus.
   - Kosten-Zeile als HorizontalLayoutGroup mit Icon+Zahl je Ressource, TMP Auto-Size (min 22, max 34), Overflow Ellipsis verboten → stattdessen Kurzformat (HudV5NumberFormat, z. B. „1,2K“).
   - Mehr als 3 Kostenposten: zweite Zeile oder Button-Höhe aus UISliceTable wachsen lassen. Nichts darf über den 9-Slice-Rand.
2. Text „Bauten bis Stufe 6“ überlappt: Hinweistext in eigenes Textfeld mit festem Platz (ContentSizeFitter/LayoutElement), Auto-Size, max. 2 Zeilen, Text aus ui_strings.
3. Dorf mit mehr Abstand: Gebäude-Footprint-Abstand bzw. Isometrie-Gitterabstand per game_config-Key `village.tile_spacing` (Default so, dass sich Gebäude im Emulator 1080x1920 nicht überlappen, Vorschlag +15 %) und `village.camera_ortho_size`. Kein Hardcode.
4. Nichts an HUD-Top-Leiste ändern (kommt aus #96).

## Dateien (vermutlich)
Assets/_Project/Scripts/UI/* (Bau-/Info-Panel), Village-/Dorf-Skripte, game_config.csv (beide Kopien), ui_strings.csv, EditMode-Tests.

## Abnahme
- EditMode-Tests: Kostenzeile mit 1/3/5 Posten und Werten 9, 9999, 1.2M bleibt innerhalb des Button-Rects; Hinweistext überlappt nicht.
- Kein Test gelöscht oder übersprungen. CI grün (EditMode + PlayMode, Gitleaks).
- Screenshot Emulator 1080x1920 vom Dorf + Ausbauen-Panel im PR.
