#!/usr/bin/env python3
"""Rendere das BAU-MENÜ D2 v1d als Übersicht, Scroll- und Detailansicht."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
HUD = HERE.parent
HTML = HERE / "menu_bau_d2_v1d.html"
OUT = HUD
W, H = 1080, 1920

SCREENS = {
    "liste": "vorschau_menu_bau_d2_v1d.png",
    "scroll": "vorschau_menu_bau_d2_v1d_scroll.png",
    "detail": "vorschau_menu_bau_d2_v1d_detail.png",
}


def main() -> None:
    chrome = shutil.which("google-chrome") or shutil.which("google-chrome-stable") or shutil.which("chromium")
    if not chrome:
        raise SystemExit("Chrome/Chromium wurde nicht gefunden.")
    if not HTML.is_file():
        raise SystemExit(f"HTML fehlt: {HTML}")
    buildings = HUD.parent / "gebaeude_neu_b"
    required = [
        buildings / name for name in (
            "e1_bld_woodcutter_bp01.png", "e1_bld_storage_bp01.png",
            "e1_bld_hut_bp01.png", "e1_bld_shell_beach_bp01.png",
            "e1_bld_hunter_bp01.png", "e1_bld_quarry_bp01.png",
            "e1_bld_trader_bp01.png", "e1_bld_center_bp01.png",
            "e1_bld_gatherer_bp01.png", "e1_bld_woodcutter_bp04.png",
        )
    ] + [
        HUD / "vorschau_hud_d2_v7_3_lvl12.png",
        HUD.parent / "ui-kit/menus_v3/_src/inventar_v4_assets/holz.png",
        HUD.parent / "ui-kit/menus_v3/_src/inventar_v4_assets/stein.png",
        HUD.parent / "ui-kit/menus_v3/_src/inventar_v4_assets/nahrung.png",
        HUD.parent / "ui-kit/menus_v3/_src/inventar_v4_assets/gold.png",
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
