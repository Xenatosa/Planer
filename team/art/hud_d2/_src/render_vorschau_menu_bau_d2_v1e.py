#!/usr/bin/env python3
"""Render the v1e single-column build list and its scrolled military view."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
HUD = HERE.parent
HTML = HERE / "menu_bau_d2_v1e.html"
BUILDINGS = HUD.parent / "gebaeude_neu_b"
OUT = HUD
W, H = 1080, 1920

SCREENS = {
    "liste": ("vorschau_menu_bau_d2_v1e.png", "screen=list"),
    "military_scroll": ("vorschau_menu_bau_d2_v1e_scroll.png", "screen=military_scroll"),
}

ART = (
    "barracks", "center", "gatherer", "hunter", "hut", "palisade",
    "quarry", "shaman_hut", "shell_beach", "storage", "trader", "woodcutter",
)


def main() -> None:
    chrome = shutil.which("google-chrome") or shutil.which("google-chrome-stable") or shutil.which("chromium")
    if not chrome:
        raise SystemExit("Chrome/Chromium wurde nicht gefunden.")
    required = [HTML, HUD / "vorschau_hud_d2_v7_3_lvl12.png"]
    required.extend(BUILDINGS / f"e1_bld_{name}_bp01.png" for name in ART)
    required.extend(
        HUD.parent / "ui-kit/menus_v3/_src/inventar_v4_assets" / name
        for name in ("Baloo2-Variable.ttf", "LilitaOne-Regular.ttf", "holz.png", "stein.png", "nahrung.png", "gold.png")
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Benötigte Assets fehlen:\n" + "\n".join(missing))

    OUT.mkdir(parents=True, exist_ok=True)
    for _, (filename, query) in SCREENS.items():
        output = OUT / filename
        url = f"{HTML.resolve().as_uri()}?{query}"
        command = [
            chrome,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--force-device-scale-factor=1",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=1200",
            f"--window-size={W},{H}",
            "--allow-file-access-from-files",
            f"--screenshot={output}",
            url,
        ]
        subprocess.run(command, check=True, timeout=45, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        with Image.open(output) as image:
            if image.size != (W, H):
                raise SystemExit(f"{filename}: erwartet {W}×{H}, erhalten {image.width}×{image.height}")
        print(f"{output.relative_to(HUD.parent.parent)} · {W}×{H}")


if __name__ == "__main__":
    main()
