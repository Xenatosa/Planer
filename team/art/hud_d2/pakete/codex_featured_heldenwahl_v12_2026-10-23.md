# Codex-Paket — Featured-Heldenwahl v12 (23.10.2026)

**Absender:** New Bot · **Fabian:** leere Rate-up-Slots und Picker mit Chance sowie Fragment-Unlock.

## Lieferung

- [Leere Slots](../vorschau_menu_beschwoeren_d2_featured_v12_slots_leer.png) — drei leise Rate-up-Platzhalter.
- [Picker](../vorschau_menu_beschwoeren_d2_featured_v12_picker.png) — Sheet mit Nara, Olm und Kiko.
- [Renderer](../_src/render_vorschau_menu_beschwoeren_featured_v12.py) — Python/Pillow.
- [Interaktive HTML-Vorschau](../../ui-kit/menus_v3/_src/html/v3_2_obsidian_beschwoeren_featured_v12_interaktiv.html) — Slot → Picker → Held auswählen → Slot gefüllt; X und Außentap schließen.

## Chance und Fragmente

- Nara: 50 % des SSR-Pools; bei 2 % SSR-Basisrate ungefähr 1 % pro Ziehung.
- Olm und Kiko zeigen die GDD-Basis-Poolraten für SR (18 %) und R (80 %); das sind keine Einzelheld-Quoten.
- Fragmentstände sind Entwurfsbeispiele: 12/80, 47/80 und 80/80. Bei 80/80 ist „Held freischalten“ markiert.

## Scope

Nur Featured-Auswahl-UI und Vorschau-Dateien; Basis ist v10b, Hintergrund und Chrome bleiben unverändert.
Keine Unity-Änderungen und keine Bildgenerierung; der Renderer komponiert mit Python/Pillow.
