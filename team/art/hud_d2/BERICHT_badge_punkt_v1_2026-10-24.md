# Bericht: HUD D2 Badge-Punkt v1

Stand: 24.10.2026

## Ergebnis

- `icons_v1/d2_ico_badge_punkt.png`: prozeduraler Glutpunkt als transparentes RGBA-Master mit 256 × 256 px. Glutoranger Verlauf, dunkle Kontur und heller Kern bleiben im 24-px-Einsatz klar erkennbar.
- `vorschau_badge_punkt_v1.png`: Helden-, Karten-, Armee- und Inventar-Dock bei 1:1 (96-px-Icon mit 24-px-Badge) sowie dieselben Ausschnitte in 300 %, auf dunklem HUD-Hintergrund `#1A120C`.
- `_src/render_badge_punkt_v1.py`: Pillow-Renderer für Master und Vorschau.

## Erzeugung

```sh
python3 team/art/hud_d2/_src/render_badge_punkt_v1.py
```

Der Renderer sucht die Dock-Master in `icons_v1` und lokalen HUD-D2-Arbeitskopien. Bei abweichendem Ablageort kann der Ordner mit `--source-dir PFAD` angegeben werden. Das Badge selbst wird vollständig mit Pillow gezeichnet; es wird keine Bild-API verwendet.
