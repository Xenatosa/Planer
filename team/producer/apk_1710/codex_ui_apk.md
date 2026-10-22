> ⛔ HUD v5.7 ist gestrichen (Fabian 22.10.2026), gültig ist D2 Obsidian & Glut + Dock A braun. Gesamtes HUD v5 (inkl. Icons `hud_c_ico_*`, `HudV5NumberFormat`) ist gestrichen; Dorf-HUD und Icons werden neu in D2 erstellt. Vorlage: `team/art/GUELTIG.md`.

# Codex-Paket UI für die Test-APK 17.10. (Ziel: APK auf main bis 19:00)
Absender: Epochen Dev UI · Repo Xenatosa/epodarien · Modell Codex GPT-6 Luna, Extra High · Kritiker: n/a (Einbau/Bugfix)
Reihenfolge strikt: A → B → C → D. Jeder Schritt ist ein eigener PR. Merge macht New Bot, wenn die Checks grün sind.

## A) #96 HUD v5.7 Stil C (läuft bereits, Queue 16)
- Konflikte mit main lösen in game_config.csv (beide Kopien: Assets/StreamingAssets/RemoteConfig/ und Assets/_Project/Data/CSV/) und RemoteConfigValues.cs. Keys aus main UND #96 behalten (battle_view.*, battle_maps.* aus #105 bleiben).
- Abnahme: EditMode + PlayMode grün auf dem Head (der ui/**-Trigger kommt seit #105 mit), kein Test gelöscht oder übersprungen. android.yml bleibt unverändert.

## B) F6 Bau-Panel + Dorf-Abstand (Queue 17), Branch ui/bau-panel-fix nach A
- Volltext: team/dev/ui/pakete/paket_F6_bau_panel_dorf_2026-10-17.md
- Kurz: Kosten am Ausbauen-Button bleiben im Button (Kurzformat HudV5NumberFormat, Auto-Size 22–34, ggf. zweite Zeile). „Bauten bis Stufe 6“ bekommt ein eigenes Textfeld (max. 2 Zeilen, ui_strings). Dorf-Abstand per `village.tile_spacing` (+15 %) und `village.camera_ortho_size`.

## C) Offene UI-PRs mergefertig machen (nach A, parallel zu B möglich)
Für #76 (ui/center-ki-variant), #71 (ui/quest-panel) und #86 (ui/hero-list-polish) gilt jeweils: main reinmergen, Konflikte lösen, CI grün, nichts am Inhalt ändern.
- #76: Der Test-Fix ist drin. Der Gitleaks-Fehler stammt vom alten Billing-Lauf, deshalb neu laufen lassen. Sonst nichts ändern.
  - Das Zentrum-Art (v005, bp01/04/07/10) kommt NICHT hier, sondern in P3 (codex_paket_art_einbau.md) über die Override-Tabelle. v003/v004 sind ersetzt und dürfen nicht verwendet werden.

## D) Dorf-Boden Stil A → wandert in P3 (codex_paket_art_einbau.md, Stand 13:30)
- Nur wenn Art Umgebung bis 12:00 eine Bodenfläche OHNE Gebäude liefert unter team/art/ui/village/e1_village_bg_stilA_v1.png (aus f3_dorf_e1_lichtung_gesamtkarte_stilA_v2 abgeleitet, Status approved): Sie kommt als Hintergrund-Layer hinter das Iso-Gitter. Der Key `village.background_sprite` ist leer, dann bleibt der alte Boden.
- Sonst entfällt D. Die volle Integration (Chunks, Breakpoint-Skins) bleibt F7 am So 18.10. abends.

## Gesamt-Abnahme
- main baut die APK grün (EditMode, PlayMode, Gitleaks). Kein Test gelöscht oder übersprungen.
- Kein Shop-Link oder Badge auf Pass oder Shop. U18 ohne Angebote (#96 deckt das ab).
- Emulator-Screenshots 1080x1920 von HUD früh und spät, Ressourcen-Sheet, Dorf und Ausbauen-Panel kommen in den letzten PR.

## E) Kampfsystem v2: Minimal-UI (Nachtrag Producer 17.10.)
Die UI wird im selben Codex-Lauf wie codex_kampfsystem_v2_apk.md gebaut, auf Branch gameplay/kampfsystem-v2. Damit entfällt die Wartezeit auf die Schnittstelle. UI-Dateien liegen nur unter Assets/_Project/Scripts/UI/Battle/ und sind sichtbar nur bei `combat_v2_enabled`. Ist das Flag aus, bleibt die alte UI.

Schnittstelle (Gameplay liefert, UI liest nur; Abstimmung mit Dev Gameplay):
- `IReadOnlyList<BattleBlockView> BattleSetup.Blocks` mit den Feldern zone (front|mitte|hinten), heroId, troopTypeId, troopCount, power (int).
- `GeneralState` mit den Feldern heroId, tacticPoints, tacticPointsMax, ultCost, `bool CanUlt` und effectCount (int, 1 bzw. 2 bei UR/UR+). effectCount optional als kleine Zahl am Button anzeigen. Verbindlich laut codex_kampfsystem_v2_apk.md.
- Ein Tap ruft `BattleInput.Submit(general_ult, tick)` auf. Die UI berechnet selbst nichts.

1. Aufstellungs-Vorschau (Formation-Screen vor dem Kampf):
   - Die drei Zonen Front, Mitte und Hinten stehen als Reihen untereinander.
   - Jeder Block ist eine Karte `ui_card_building` (9-Slice aus UISliceTable). Sie zeigt das Helden-Portrait (SpriteCatalog, Fallback missing), das Truppentyp-Icon, die Anzahl als „×N“ und die Kampfkraft im Kurzformat HudV5NumberFormat.
   - Der General steht in einem eigenen Slot außerhalb der Zonen und hat das Label aus ui_strings `battle.general.label`.
   - Leere Slots zeigen den Text `battle.block.empty`.
   - Es gibt kein Drag und kein Umstellen. Die Zuteilung macht die Sim.
2. General-Button im Kampf:
   - Ein runder Button unten rechts in der Safe Area, 160 px auf 1080x1920. Er zeigt das Portrait mit einem radialen Füllring von tacticPoints/tacticPointsMax.
   - Bei `CanUlt` leuchtet ein Puls von 0,8 s (Dauer per Config `battle.general_btn.pulse_ms`). Sonst ist der Button grau und nicht klickbar.
   - Ein Tap sendet einmal die Eingabe. Danach ist er gesperrt, bis `CanUlt` wieder true ist.
   - Es gibt keine weiteren manuellen Buttons (keinen Taktik-, Fokus- oder Ult-Button für Feldhelden).
   - Die Ult-Kamera aus #105 (camera_ult_zoom_*) wird beim general_ult ausgelöst.
3. Texte: Neue Keys in ui_strings DE/EN sind `battle.general.label`, `battle.block.empty`, `battle.block.power` und `battle.general.ready`.

Abnahme E:
- EditMode-Test: Die Vorschau erzeugt bei 1, 3 und 6 Blöcken die richtige Zahl Karten, die Werte kommen aus BattleBlockView.
- PlayMode-Test: Ein Tap auf den General-Button bei CanUlt erzeugt genau eine Replay-Eingabe mit dem richtigen Tick. Bei !CanUlt entsteht keine Eingabe.
- Kein Text liegt über einem Button-Rand (gleiche Prüfung wie in F6). Ist das Flag aus, ist die alte UI unverändert.
