#!/usr/bin/env python3
"""Rendere den Bau-Shop D2 v2 und den Platzierungsmodus als Handy-Keyframes."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
HUD = HERE.parent
HTML = HERE / "menu_bau_d2_v2.html"
W, H = 1080, 1920
SCREENS = {
    "shop": "vorschau_menu_bau_d2_v2.png",
    "place": "vorschau_menu_bau_d2_v2_platzieren.png",
}


def main() -> None:
    chrome = (shutil.which("google-chrome") or shutil.which("google-chrome-stable")
              or shutil.which("chromium") or shutil.which("chromium-browser"))
    if not chrome:
        raise SystemExit("Chrome/Chromium wurde nicht gefunden.")
    if not HTML.is_file():
        raise SystemExit(f"HTML fehlt: {HTML}")

    buildings = HUD.parent / "gebaeude_neu_b"
    building_names = (
        "e1_bld_woodcutter_bp01.png", "e1_bld_center_bp01.png",
        "e1_bld_shell_beach_bp01.png", "e1_bld_hut_bp01.png",
        "e1_bld_storage_bp01.png", "e1_bld_quarry_bp01.png",
        "e1_bld_hunter_bp01.png", "e1_bld_trader_bp01.png",
        "e1_bld_gatherer_bp01.png", "e1_bld_woodcutter_bp04.png",
        "e1_bld_center_bp04.png", "e1_bld_shell_beach_bp04.png",
        "e1_bld_hut_bp04.png", "e1_bld_storage_bp04.png",
        "e1_bld_quarry_bp04.png", "e1_bld_hunter_bp04.png",
        "e1_bld_gatherer_bp04.png", "e1_bld_barracks_bp01.png",
        "e1_bld_barracks_bp04.png", "e1_bld_palisade_bp01.png",
        "e1_bld_palisade_bp04.png", "e1_bld_shaman_hut_bp01.png",
        "e1_bld_shaman_hut_bp04.png",
    )
    resource_dir = HUD.parent / "ui-kit/menus_v3/_src/inventar_v4_assets"
    required = [buildings / name for name in building_names]
    required += [
        HUD / "vorschau_hud_d2_v7_3_lvl12.png",
        *(resource_dir / name for name in (
            "holz.png", "stein.png", "nahrung.png", "gold.png",
            "LilitaOne-Regular.ttf", "Baloo2-Variable.ttf",
        )),
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Benötigte freigegebene Assets fehlen:\n" + "\n".join(missing))

    for screen, filename in SCREENS.items():
        output = HUD / filename
        url = f"{HTML.resolve().as_uri()}?screen={screen}"
        command = [
            chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
            "--disable-dev-shm-usage", "--hide-scrollbars",
            "--force-device-scale-factor=1", "--run-all-compositor-stages-before-draw",
            "--allow-file-access-from-files",
            f"--window-size={W},{H}", f"--screenshot={output}", url,
        ]
        result = subprocess.run(command, check=True, timeout=45, stdout=subprocess.DEVNULL,
                                stderr=subprocess.PIPE, text=True)
        with Image.open(output) as image:
            if image.size != (W, H):
                raise SystemExit(f"{filename}: erwartet {W}×{H}, erhalten {image.width}×{image.height}")
        if "canvas" in result.stderr.lower() and "taint" in result.stderr.lower():
            raise SystemExit("Browser blockierte das Normalisieren der freigegebenen Gebäudeabbildungen.")
        print(f"{output.relative_to(HUD.parent.parent)} · {W}×{H}")


if __name__ == "__main__":
    main()
