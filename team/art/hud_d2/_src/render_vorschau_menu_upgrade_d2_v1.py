#!/usr/bin/env python3
"""Render the available and blocked D2 building-upgrade previews."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
HUD = HERE.parent
HTML = HERE / "menu_upgrade_d2_v1.html"
ROOT = HUD.parents[2]
OUT = HUD
W, H = 1080, 1920

SCREENS = {
    "ready": "vorschau_menu_upgrade_d2_v1.png",
    "locked": "vorschau_menu_upgrade_d2_v1_gesperrt.png",
}


def main() -> None:
    chrome = shutil.which("google-chrome") or shutil.which("google-chrome-stable") or shutil.which("chromium")
    if not chrome:
        raise SystemExit("Chrome/Chromium wurde nicht gefunden.")
    assets = ROOT / "team/art/ui-kit/menus_v3/_src/inventar_v4_assets"
    required = [
        HTML,
        HUD / "vorschau_hud_d2_v7_3_lvl12.png",
        ROOT / "team/art/gebaeude_neu_b/e1_bld_woodcutter_bp04.png",
        *(assets / name for name in (
            "Baloo2-Variable.ttf", "LilitaOne-Regular.ttf", "holz.png",
            "stein.png", "nahrung.png", "gold.png",
        )),
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
            "--force-device-scale-factor=1",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=1200",
            f"--window-size={W},{H}",
            "--allow-file-access-from-files",
            f"--screenshot={output}",
            url,
        ]
        subprocess.run(command, check=True, timeout=45, stdout=subprocess.DEVNULL,
                       stderr=subprocess.PIPE, text=True)
        with Image.open(output) as image:
            if image.size != (W, H):
                raise SystemExit(f"{filename}: erwartet {W}×{H}, erhalten {image.width}×{image.height}")
        print(f"{output.relative_to(ROOT)} · {W}×{H}")


if __name__ == "__main__":
    main()
