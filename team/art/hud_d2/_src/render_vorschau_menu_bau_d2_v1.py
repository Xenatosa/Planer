#!/usr/bin/env python3
"""Rendere das BAU-MENÜ D2 v1 als Liste und Gebäudedetail."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
HUD = HERE.parent
HTML = HERE / "menu_bau_d2_v1.html"
OUT = HUD
W, H = 1080, 1920

SCREENS = {
    "liste": "vorschau_menu_bau_d2_v1.png",
    "detail": "vorschau_menu_bau_d2_v1_detail.png",
}


def main() -> None:
    chrome = shutil.which("google-chrome") or shutil.which("google-chrome-stable") or shutil.which("chromium")
    if not chrome:
        raise SystemExit("Chrome/Chromium wurde nicht gefunden.")
    if not HTML.is_file():
        raise SystemExit(f"HTML fehlt: {HTML}")
    buildings = HUD.parent / "gebaeude_neu_b"
    required = [
        buildings / "e1_bld_waldhuette_2.png",
        buildings / "e1_bld_steinbruch_1.png",
        buildings / "e1_bld_bauernhof_1.png",
        buildings / "e1_bld_fischerhuette_1.png",
        HUD.parent / "ui-kit/menus_v3/_src/inventar_v4_assets/bg_inventar.jpg",
        HUD.parent / "ui-kit/menus_v3/_src/inventar_v4_assets/dock_bg.png",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Benötigte Assets fehlen:\n" + "\n".join(missing))

    OUT.mkdir(parents=True, exist_ok=True)
    for screen, filename in SCREENS.items():
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
