# Kurzbericht — Beschwören Reveal v16

**Branch:** `art/hud-d2-reveal-komplett-neu-v16`
**Basis:** `origin/main` (`6a7c852`), frischer Worktree

## Umsetzung

- Featured und Standard als neue Reveal-Fläche aufgebaut: individuelle Basalt/Portal-Karten, neue Aktionstasten, neue 1×/10×-Marker, neue Garantie-Leiste und ein 3–4–3-Fächer für zehn Karten. Gegenüber v15 (zwei Fünferreihen) ist die Anordnung klar anders.
- Ritualhallen-Bühne bleibt; Unschärfe plus dunkler Scrim (mindestens 62 %) und Vignette lassen Karten und Aktionen führen.
- Featured startet mit drei leeren Rate-up-Siegelplätzen und „RATE-UP WÄHLEN · 14 Tage“. Die HTML-Vorschau enthält die Auswahl für diese Plätze.
- Einzelkarten-Flip, „Alle aufdecken“, Standard/Featured und 1×/10× sind interaktiv. Fragment-Reveal zeigt Portrait, große Menge (z. B. `×5`) und Fortschritt (`12 / 80`); Helden zeigen Portrait, Name und Seltenheit.

## Lieferung und Prüfung

- HTML: `team/art/ui-kit/menus_v3/_src/html/v3_2_obsidian_beschwoeren_reveal_v16_interaktiv.html`
- Renderer: `team/art/hud_d2/_src/render_vorschau_menu_beschwoeren_reveal_d2_v16.py`
- Sechs PNG-Keyframes unter `team/art/hud_d2/`, jeweils **1080×1920**: Featured 1×/10× geschlossen/offen sowie Standard 1× geschlossen/offen.
- Browser-Klickprobe bestanden: 1× rendert eine Karte, 10× zehn einzeln tippbare Karten, Einzel-Flip und „Alle aufdecken“ funktionieren; Rate-up-Auswahl funktioniert. Fragmenttext `×5` und `12 / 80` geprüft. `git diff --check` ohne Befund.
- Bildgenerierung: nicht verwendet. Kosten: **0 $**.

**DONE · 2026-10-23 19:56:44 CEST Europe/Berlin**
