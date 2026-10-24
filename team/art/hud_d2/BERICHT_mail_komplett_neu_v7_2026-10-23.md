# Bericht · Mail komplett neu v7

**DONE · 2026-10-23 21:33 CEST (Europe/Berlin)**

- Postfach als eigenständigen Vollbild-Aufbau umgesetzt; keine Mail-v3–v6-Oberfläche übernommen.
- Interaktives HTML mit SYSTEM-/SPIELER-Tabs, globalem Alles-gelesen-Ablauf, automatischer Annahme der System-Belohnungen, Einzelannahme und gesperrtem Löschen bis keine ungelesene Post/offene Belohnung verbleibt.
- Renderer und drei 1080 × 1920 PNG-Zustände erstellt.
- Maßplan erstellt; `FENSTER_SCOPE_v1.md` auf Mail v7 als aktuelle Fassung gesetzt und frühere Stände als abgelöst markiert.
- Bestehende Schriftstuben-Grafik und Inventar-Ressourcen/Dock-Bausteine wiederverwendet; keine Bildgenerierung, Kosten 0 $.
- Keine freigegebenen Inventar-v4g-Dateien geändert.

## Prüfung

- PNG-Abmessungen: 1080 × 1920 px je Zustand.
- Interaktionen im HTML: Tabs, ungelesen-Zähler, Belohnung einzeln annehmen, Alles gelesen, Löschen-Gate und Löschen nach Freigabe.
- `git diff --check` sauber.

## Lieferung

- `vorschau_overlay_mail_d2_v7.png`
- `vorschau_overlay_mail_d2_v7_spieler.png`
- `vorschau_overlay_mail_d2_v7_gelesen.png`
- `massplan_overlay_mail_d2_v7.md`
- `v3_2_obsidian_mail_v7_interaktiv.html`
- `render_vorschau_overlay_mail_d2_v7.py`
