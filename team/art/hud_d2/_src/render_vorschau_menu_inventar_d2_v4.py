#!/usr/bin/env python3
"""Rendere die drei Inventar-v4c-Keyframes aus dem interaktiven HTML."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
HUD = HERE.parent
V3 = HUD.parent / "ui-kit" / "menus_v3"
HTML = V3 / "_src" / "html" / "v3_2_obsidian_inventar_v4_interaktiv.html"
ASSETS = V3 / "_src" / "inventar_v4_assets"
OUT = HUD
W, H = 1080, 1920

KEYFRAMES = {
    "alle": "vorschau_menu_inventar_d2_v4_alle.png",
    "ausruestung": "vorschau_menu_inventar_d2_v4_ausruestung.png",
    "detail": "vorschau_menu_inventar_d2_v4_detail_sheet.png",
}


def main() -> None:
    chrome = shutil.which("google-chrome") or shutil.which("google-chrome-stable") or shutil.which("chromium")
    if not chrome:
        raise SystemExit("Chrome/Chromium wurde nicht gefunden.")
    if not HTML.is_file():
        raise SystemExit(f"HTML fehlt: {HTML}")
    required = ["bg_inventar.jpg", "LilitaOne-Regular.ttf", "Baloo2-Variable.ttf", "dock_bg.png"]
    missing = [name for name in required if not (ASSETS / name).is_file()]
    if missing:
        raise SystemExit(f"Inventar-v4-Assets fehlen: {', '.join(missing)}")

    OUT.mkdir(parents=True, exist_ok=True)
    for screen, filename in KEYFRAMES.items():
        output = OUT / filename
        url = f"{HTML.resolve().as_uri()}?screen={screen}"
        command = [
            chrome,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            "--run-all-compositor-stages-before-draw",
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
