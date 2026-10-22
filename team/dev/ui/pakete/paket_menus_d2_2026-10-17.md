> ⛔ HUD v5.7 ist gestrichen (Fabian 22.10.2026), gültig ist D2 Obsidian & Glut + Dock A braun. Gesamtes HUD v5 (inkl. Icons `hud_c_ico_*`, `HudV5NumberFormat`) ist gestrichen; Dorf-HUD und Icons werden neu in D2 erstellt. Vorlage: `team/art/GUELTIG.md`.

# Codex-Paket: Menüs auf Vorlage D2 „Obsidian & Glut“ umstellen (17.10.2026)

Freigabe: AD, Kritiker, Codex r4, Fabians Korrektur eingearbeitet. Repo Xenatosa/epodarien, nur Konto Xenatosa.
Branch: `ui/menus-d2` von main. Ergebnis als PR, nicht selbst mergen. android.yml tabu. Nur Assets/_Project/Scripts/UI/, Art-Import und Config/ui_strings anfassen.

## Quellen (alle unter team/art/ui-kit/menus_v3/)
- vorlage_D2.md: Spec mit Raster, Farben, Typo, Komponenten samt Zuständen, 9-Slice-Regel und Box-Regel. Diese Spec ist verbindlich.
- vorlage_D2_layout_helden.csv: Layout Helden-Detail (Layout D4 im Stil D2).
- vorlage_D2_export/: 69 PNG plus manifest_9slice.json. Die Slice-Ränder kommen aus dem Manifest.
- config/menus_v3_mock_strings.json, Bereich ui_d2: die Texte, nach ui_strings übernehmen (DE, EN als Platzhalter).
- Referenzbilder: v3_2_obsidian_helden_detail_v2.png, v3_2_obsidian_bauen.png, v3_2_obsidian_armee.png.

## Reihenfolge (je ein Commit)
1. **D2-Grundlage:** `MenuThemeD2` (Farben und Typo aus Config bzw. ScriptableObject), D2-Komponenten in UiFactory: Panel/Box, Button primär/sekundär/ghost, Tab, Slot, Liste/Karte, Filterchip und die D2-Top-Leiste für Menüs. Alle Zustände laut Spec (normal, gedrückt, gesperrt, aktiv, leer).
2. **Helden-Detail** nach vorlage_D2_layout_helden.csv: große, frei stehende Figur, Tabs, Ausrüstungsslots. Die Slots kommen aus der Config, 10 Slots, die Liste liefert gear_slots.csv von Game Design. Nicht hart verdrahten; leere Slots im Leer-Zustand zeigen.
3. **Bauen** (BuildDialogLayout) auf D2 umstellen. Die F6-Logik (Kosten-Umbruch, Text „bis Stufe 6“) bleibt.
4. **Armee** auf D2 umstellen.
Die alten violett/creme Stile werden für diese drei Bildschirme komplett ersetzt, aber nicht gelöscht, solange andere Bildschirme sie noch nutzen.

## Feste Regeln
- ~~Die Dorf-Top-Leiste (HUD v5.7 / F6) bleibt unverändert.~~ GESTRICHEN (Fabian 22.10.2026): Die Dorf-Top-Leiste wird neu in D2 erstellt (Top-Leiste, Quest-Leiste, Dock A braun mit Glut-Orange-Platte).
- Inhalte liegen immer in ihrer Box, mindestens 12 px Innenabstand (Config `ui_d2.box_padding_min`).
- Touch-Ziele mindestens 120 px.
- Kein Text im Bild, alle Texte über ui_strings und TMP.
- Keine weißen Platzhalter und keine Kürzel/Schlüssel im UI. Fehlende Sprites werden ausgeblendet, mit einer Warnung pro ID.
- Alle Maße, Farben und die Slot-Anzahl stehen per Config. Shop-Badges an Pass und Limits sind verboten, für U18 gelten die Regeln aus #142 und Job 32.

## Abstimmung mit Ausrüstung v1.7.3
team/dev/pakete/2026-10-17_codex_ausruestung_v173.md (Dev Gameplay) baut Filter, Sortierung, Vergleichspfeile und das Inventar. Dieses Paket liefert die D2-Komponenten und die Hülle des Helden-Details mit den Slots. Das Ausrüstungs-Paket nutzt diese Komponenten und baut keine eigenen D2-Stile. Laufen beide parallel, fasst nur dieses Paket die Datei für das Helden-Detail-Layout an. Die Ausrüstung hängt sich über eine Schnittstelle ein (z. B. `IHeroGearPanel` bzw. `HeroDetailLayout.GearSlotsRoot`).

## Abnahme
- EditMode: 9-Slice-Ränder kommen aus manifest_9slice.json. Alle Buttons und Tabs der drei Bildschirme sind mindestens 120 px groß. Kein Kindelement liegt außerhalb seiner Box (Innenabstand ≥ 12). Das Helden-Detail baut so viele Slots, wie die Config vorgibt.
- PlayMode: Helden-Detail, Bauen und Armee öffnen und schließen ohne Fehler. Die Dorf-Top-Leiste ist unverändert, per Screenshot-Vergleich oder RectTransform-Test.
- CI grün, kein Test gelöscht.
- Modern-Gate: je Bildschirm ein Screenshot (1080×1920) neben dem Referenzbild in den PR. Vor dem APK-Merge gehen die Screenshots an den AD und danach an den Kritiker.
