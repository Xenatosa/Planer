#!/usr/bin/env python3
"""Render the interactive Mail v7 HTML into review PNGs."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[4]
HTML = ROOT / "team/art/ui-kit/menus_v3/_src/html/v3_2_obsidian_mail_v7_interaktiv.html"
OUT = ROOT / "team/art/hud_d2"
SCREENS = (
    ("system", "vorschau_overlay_mail_d2_v7.png"),
    ("player", "vorschau_overlay_mail_d2_v7_spieler.png"),
    ("read", "vorschau_overlay_mail_d2_v7_gelesen.png"),
    ("detail", "vorschau_overlay_mail_d2_v7_detail.png"),
)


def chrome_binary(explicit: str | None) -> str:
    candidate = explicit or shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not candidate:
        raise SystemExit("Chrome/Chromium nicht gefunden; --chrome <Pfad> angeben.")
    return candidate


def render(chrome: str, output_dir: Path, only_view: str | None = None) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for view, filename in SCREENS:
        if only_view and view != only_view:
            continue
        output = output_dir / filename
        url = HTML.resolve().as_uri() + "?view=" + view
        command = [
            chrome,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--hide-scrollbars",
            "--allow-file-access-from-files",
            "--force-device-scale-factor=1",
            "--window-size=1080,1920",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=3000",
            "--screenshot=" + str(output),
            url,
        ]
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        if result.returncode != 0 or not output.exists():
            raise SystemExit(f"Chrome-Render fehlgeschlagen ({view}):\n{result.stderr[-2500:]}")
        with Image.open(output) as image:
            if image.size != (1080, 1920):
                raise SystemExit(f"Falsche PNG-Größe für {output.name}: {image.size}, erwartet (1080, 1920)")
        print(f"DONE {output} · 1080×1920")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chrome", help="Chrome/Chromium-Binary")
    parser.add_argument("--output-dir", type=Path, default=OUT, help="Zielordner für die PNGs")
    parser.add_argument("--view", choices=[view for view, _ in SCREENS], help="Nur diesen Vorschaustand rendern")
    args = parser.parse_args()
    if not HTML.is_file():
        raise SystemExit(f"HTML nicht gefunden: {HTML}")
    render(chrome_binary(args.chrome), args.output_dir.resolve(), args.view)


if __name__ == "__main__":
    main()
