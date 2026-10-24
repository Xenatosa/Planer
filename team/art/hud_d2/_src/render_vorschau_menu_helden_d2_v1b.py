#!/usr/bin/env python3
"""Render the D2 hero roster and v2-aligned hero detail previews at 1080x1920."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
HUD = HERE.parent
ROOT = HUD.parents[2]
HTML = HERE / "menu_helden_d2_v1b.html"
OUT = HUD
W, H = 1080, 1920

SCREENS = {
    "list": "vorschau_menu_helden_d2_v1b.png",
    "detail": "vorschau_menu_helden_d2_v1b_detail.png",
}


def main() -> None:
    chrome = (
        shutil.which("google-chrome")
        or shutil.which("google-chrome-stable")
        or shutil.which("chromium")
    )
    if not chrome:
        raise SystemExit("Chrome/Chromium wurde nicht gefunden.")

    font_dir = ROOT / "team/art/ui-kit/menus_v3/_src/inventar_v4_assets"
    hero_dir = ROOT / "team/art/heroes"
    reveal_assets = ROOT / "team/art/ui-kit/menus_v3/_assets/reveal_v16"
    required = [
        HTML,
        HUD / "vorschau_hud_d2_v7_3_lvl12.png",
        HERE / "assets/bg_dark_hoehle.png",
        *(HERE / "assets" / name for name in ("eq_ring1.png", "eq_ring2.png", "eq_artefakt2.png")),
        font_dir / "Baloo2-Variable.ttf",
        font_dir / "LilitaOne-Regular.ttf",
        *(hero_dir / f"hero_{name}_portrait_alpha.png" for name in (
            "bako", "gorm", "kiko", "mira", "nara", "olm", "ruka", "tala"
        )),
        hero_dir / "hero_ruka_fullbody_alpha_v4.png",
        *(reveal_assets / name for name in (
            "d2_ico_dock_dorf.png", "d2_ico_dock_helden_inaktiv.png",
            "d2_ico_dock_karte_inaktiv.png", "d2_ico_dock_armee_inaktiv.png",
            "d2_ico_dock_gilde_inaktiv.png", "d2_ico_dock_inventar_inaktiv.png",
        )),
        *(font_dir / name for name in (
            "eq_helm.png", "eq_schultern.png", "eq_waffe.png", "eq_ruestung.png",
            "eq_beine.png", "eq_schuhe.png", "eq_ring.png", "eq_artefakt1.png",
        )),
        font_dir / "gold.png",
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
            "--virtual-time-budget=1600",
            f"--window-size={W},{H}",
            "--allow-file-access-from-files",
            f"--screenshot={output}",
            url,
        ]
        subprocess.run(
            command,
            check=True,
            timeout=45,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        with Image.open(output) as image:
            if image.size != (W, H):
                raise SystemExit(
                    f"{filename}: erwartet {W}×{H}, erhalten {image.width}×{image.height}"
                )
            if image.getbbox() is None:
                raise SystemExit(f"{filename}: Bild ist leer.")
        if output.stat().st_size < 100_000:
            raise SystemExit(f"{filename}: Ausgabe unerwartet klein ({output.stat().st_size} Bytes).")
        print(f"{output.relative_to(ROOT)} · {W}×{H} · {output.stat().st_size:,} Bytes")


if __name__ == "__main__":
    main()
