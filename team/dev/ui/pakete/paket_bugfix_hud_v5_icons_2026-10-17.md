> ⛔ HUD v5.7 ist gestrichen (Fabian 22.10.2026), gültig ist D2 Obsidian & Glut + Dock A braun. Gesamtes HUD v5 (inkl. Icons `hud_c_ico_*`, `HudV5NumberFormat`) ist gestrichen; Dorf-HUD und Icons werden neu in D2 erstellt. Vorlage: `team/art/GUELTIG.md`.

# Codex-Bugfix: HUD-v5-Icons als weiße Kästen, Avatar als Platzhalter (17.10.2026)

Kein Kritiker nötig (Bugfix). Repo Xenatosa/epodarien. Muss in der 19-Uhr-APK behoben sein.
Branch: KEIN eigener Branch. Der Fix kommt als eigener Commit auf `ui/hud-v5-7-nachtrag` (Job 24), damit sich nichts doppelt und die Dock-Icons dort nur einmal angefasst werden. Falls Job 24 schon gemergt ist: `ui/hud-v5-icons-fix` von main.

## Befund
Fabians Test der Zwischen-APK (Run 39010900947, main 9533a67 nach #96), Screenshot /workspace/uploads/fabian_apk_hud_weisse_icons_0855.png:
- Die 5 Dock-Icons unten und die 4 Seitenleisten-Icons rechts sind weiße Kästen.
- Der Avatar oben links zeigt den Platzhalter „AVATAR“.
- Top-Leiste, Ressourcen-Knopf und Gebäude-Panel sind in Ordnung, also werden Frames und Pills geladen.

## Spuren (von Dev UI am Code geprüft, noch nicht bewiesen)
- Die Sprites laufen über `SpriteCatalog` (Resources), den die ArtPipeline beim Build erzeugt (`BuildScript.PrepareForTests`). Gescannt werden `Assets/_Project/Art` und `Assets/Art`, also auch `Assets/Art/UI/HUD/v5/`.
- Die Dock- und Seiten-Icons laufen über die Auflösung in `SpriteCatalog.cs` ~Z. 140–150: erst `hud_c_ico_<name>_<set>`, dann die Eiszeit-Variante, dann die ID ohne Suffix. Prüfen, ob die Namen aus hud_layout.csv bzw. der Config (dock.order, Seitenleiste) zu den echten Dateinamen passen und ob `SpriteKey.CatalogIds` / `RequiredIds()` sie enthält. Dann prüfen, ob der Catalog nur Pflicht-IDs aufnimmt.
- Weißer Kasten heißt sehr wahrscheinlich, dass `Image.sprite == null` ist, das Image aber trotzdem sichtbar bleibt. Zusätzlich die Import-Settings der Icons prüfen (Texture Type Sprite, nicht Default), Atlas-Zuordnung und Meta-Dateien.
- Avatar: `HudV5View` Z. 269–270 liest `player.avatar_hero`. Ist der Wert nicht gesetzt, nimmt es `SpriteKey.Avatar` (`ui_avatar`), und dafür gibt es offenbar kein Sprite. Soll: Porträt des Anführers bzw. von Ruka (`hero_ruka_portrait_alpha`, neu unter team/art/ui/heroes/), Default per Config.

## Fix-Anforderungen
1. Ursache finden und beheben, sodass alle Dock- und Seiten-Icons sowie der Avatar in der APK echte Sprites zeigen. Das gilt auch für die 4 neuen Icons aus Job 24 (login_kalender, gratis, evt_platzhalter, dot_soft).
2. Fehlt ein Sprite trotzdem, darf kein weißer Kasten erscheinen. Dann das Image ausblenden oder ein neutrales Platzhalter-Icon zeigen und einmal pro ID `Debug.LogWarning` ausgeben.
3. Default `player.avatar_hero` in game_config auf den Ruka-Porträtschlüssel (bzw. LeaderId zur Laufzeit), ohne Hardcode im C#.

## Abnahme
- EditMode-Test: Für jede ID aus dock.order, der Seitenleiste und dem Avatar liefert `SpriteCatalog` nach `PrepareForTests` ein Sprite ungleich null.
- Test: Wenn ein Sprite fehlt, wird kein weißes Image gerendert.
- CI-Unity-Tests grün, APK-Build-Screenshot (Dock, Seitenleiste, Avatar) im PR.
- Nicht selbst mergen.
