# Screens gegen Prototyp-Scope (M1–M3) geschärft

Von: Juno (UI) · 23.10.2026 · Auftrag Chef (Paket Systeme & Grundlagen)
Quellen: `GDD_v1.6.13.md` (epodarien/docs/finanzen/basis_gdd), Meilensteine Teil B, `GUELTIG.md` (Planer, Stand 22.10.), PR #152 (14 D2-Menügerüste).

## Die 14 D2-Gerüste (PR #152) im Scope-Urteil

| Menü (Gerüst in PR #152) | Prototyp-Grundlage? | Meilenstein | Begründung |
|---|---|---|---|
| Forschung | **JA** | M1–M3 | Kap. 21 wirkt direkt auf Kernloop (Produktion +12 %, Lager, Winter, Kampfbonus); CSVs liegen im Spiel-Repo; die Sim rechnet Forschung in den Tag-8-Aufstieg ein. |
| Inventar | **JA** | M1–M3 | Items existieren (Glutuhr-Familie, Kisten, Trophäen-Rest); Quests und Kampagne geben Items; Verfalls-Hinweis (Uhr-Chip) ist Dev-Pflicht. |
| Beschwörung / Banner | **JA** | M3 | Im Prototyp-Scope (ohne Echtgeld, nur verdiente Kristalle); Chancen-Pity-Regeln gelten, aber kein IAP. |
| Fragment-Inventar | **JA** | M3 | Hängt an Beschwörung/Helden (Olmm-Fragmente L10, Wahl-Fragmente sind M4+, UI kann beides zeigen). |
| Allgemeines Aufwerten (general_upgrade) | **FRAGE** | L12-Feature | Gouverneure schalten erst auf Kampagnen-L12 frei (Kampagne v1.4, Features-Spalte). Für die Grundlage unnötig, aber schadet nicht. Abstimmung mit Kai, was die Seite wirklich zeigt. |
| Gegenstände-Upgrade / Schmiede | TEILWEISE | M3.5 | Direkt hinter dem Prototyp; Schmiede ist Tab am Kriegerlager. Gerüst reicht für jetzt. |
| Artefakte & Sets | TEILWEISE | M3.5 | Gleiches Bild wie Schmiede (Kap. 18). |
| Gilden / Stämme | NEIN | M4 | Kap. 11, Freischaltung Häuptlingsfeuer 6. |
| Arena | NEIN | M5 | Kap. 12, mit Epoche 2. |
| Events + Würfel-Event | NEIN | M6 | Kap. 13, Events/Ranglisten. |
| Minispiele | NEIN | später | Burgensturm-Spec existiert, aber nicht im Prototyp-Scope (GDD Kap. 1). |
| Ahnenprüfung | NEIN | M5/M6 | Normierter Kampf im Stammeswettstreit (Kap. 20/24); braucht Dev-Spezifikation. |
| Edelstein-Shop | NEIN | M7 | Echtgeld = Soft Launch; im Prototyp nur verdiente Kristalle, U18-Regeln (U18: Angebote aus) sind im Code schon berücksichtigt. |

**Konsequenz für die Unity-Integration:** Die vier Prototyp-Gerüste (Forschung, Inventar, Beschwörung, Fragmente) bekommen nach Fabians Freigabe der Fenster-Inhalte zuerst Inhalt. Die übrigen zehn bleiben leere Gerüste hinter dem Router (kein Dock-Knopf nötig, bis das Milestone-Fenster kommt).

## Fehlende Screens, die NICHT in PR #152 sind

| Screen | Prototyp? | Stand |
|---|---|---|
| Angebote / Pass | NEIN (M7) | Shop-Dock und Pass sind per Default gesperrt (Unlock-Regeln), U18 immer aus. Kein Handlungsbedarf für den Prototyp. |
| Events-Detail | NEIN (M6) | Event-Kachel + Dock-Einstieg routen bereits auf das Events-Gerüst (PR #152). Detail-Inhalt später. |
| Einstellungen | **JA** | Fehlt komplett, auch als Gerüst. Grundlage (Sound, Sprache, U18-, Account-Handling für den Test-APK-Lauf). → kleines eigenes Gerüst nach PR #152, gleiche Bauart. |
| Karte (Dorf-/Weltkarte-Freigabe) | **JA** | Karten-Konzept E1 ist verbindlich (`karten_konzept/`), Massplan v3.7 noch nicht freigegeben. UI-Seite wartet auf Freigabe. |

## Blocker, die ich beim Prüfen gefunden habe

1. **Fabians lokaler Planer-Branch `art/hud-d2-reveal-karten-3d-v13` ist nicht gepusht.** Die freigegebenen Fenster-Mocks (Gilde Innen v4b, Außen v8; Referenzen Inventar v2 / Armee v1b) und die D2-Mock-PNGs (`v3_2_obsidian_*.png`, `vorlage_D2_export/`, Dock A) fehlen im Planer-main — nur `vorlage_D2.md` und die Masspläne sind da. Ohne die Mocks kann ich die freigegebenen Fenster nicht Unity-reif bauen. Bitte pushen oder mich freigeben, den Branch zu holen.
2. **`GUELTIG.md` listet das D2-Dorf-HUD (Massplan v6.3) nicht als verbindliche Fassung.** Der Massplan v6.3 (Plus an Zeitkristalle angedockt, 0 Befunde) sollte als gültige Zeile eingetragen werden, sonst baut jemand nach altem Stand.
3. **PR #152 CI:** Compile-Fehler (maxTextureSize, fehlendes Using) sind von mir gefixt; 22 EditMode-Tests laufen noch, Fix läuft.
