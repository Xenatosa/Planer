# Kurzbericht · Inventar komplett neu v4

**Branch:** `art/hud-d2-inventar-komplett-neu-v4` · **Basis:** `origin/main`

## Was neu

- Neues HTML und neuer Chrome-Renderer, unabhängig vom v3c-Aufbau: fünf Icon-Tabs, Such- und Sortierleiste, visuelles Dreispaltenraster mit Seltenheitsrahmen und großem Detailsheet.
- 42 Mock-Gegenstände in den fünf deutschen Kategorien. Ressourcenkarten, Ausrüstung, Fragmente und Verbrauchsgüter zeigen unterschiedliche Mengen, Fortschritte und Aktionen.
- Top-Pills zeigen Kristall, Wissen und Gold-Muschel. Im Dock ist Inventar aktiv.
- Drei PNG-Keyframes: Alle mit ausgewähltem Knochenhelm, Ausrüstung und offenes Detailsheet. Maße jeweils **1080 × 1920 px**.
- Das HTML bündelt seine benötigten D2-Sprites, Ausrüstungsbilder und Schriften unter `_src/inventar_v4_assets/`; keine externen Laufzeitquellen.

## Prüfung

- Chrome-Renderer für alle drei Keyframes ausgeführt; Maße geprüft.
- Browser-Klickprobe: Tab Ausrüstung zeigt 8 Einträge; Antippen des Speers öffnet das Sheet mit **ANLEGEN**; Fragmente zeigen 6 Einträge und Fortschritt; Verbrauch zeigt 16 Einträge und **VERWENDEN**; Suche nach „Glutuhr“ ergibt einen Treffer; Sortierung wechselt.
- Scrim mindestens 65 %, Vignette aktiv. Randmittelwert über je 20 Außenpixel, y100–1663: Inventar **15,4**, Beschwören v16 **18,4**, Differenz **3,0**.
- Sichttexte deutsch, ohne Spiegelung. `git diff --check` sauber.

## Kosten

- Bildgenerierung: **0 $**. Vorhandene D2-Sprites, Equip-Icons und Schriften verwendet.

**DONE · 2026-10-23 20:42:24 CEST Europe/Berlin**
