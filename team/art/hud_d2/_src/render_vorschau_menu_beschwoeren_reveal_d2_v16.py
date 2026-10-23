#!/usr/bin/env python3
"""Render the six fixed v16 summon reveal keyframes from the interactive HTML."""
from pathlib import Path
from urllib.parse import urlencode
import subprocess
import tempfile

from PIL import Image

HERE = Path(__file__).resolve().parent
HUD = HERE.parent
HTML = HUD.parent / "ui-kit" / "menus_v3" / "_src" / "html" / "v3_2_obsidian_beschwoeren_reveal_v16_interaktiv.html"
OUT = HUD
WIDTH, HEIGHT = 1080, 1920
STATES = [
    ("featured", "1x", "0", "vorschau_menu_beschwoeren_d2_featured_v16_1x_closed.png"),
    ("featured", "1x", "1", "vorschau_menu_beschwoeren_d2_featured_v16_1x_open.png"),
    ("featured", "10x", "0", "vorschau_menu_beschwoeren_d2_featured_v16_10x_closed.png"),
    ("featured", "10x", "1", "vorschau_menu_beschwoeren_d2_featured_v16_10x_open.png"),
    ("standard", "1x", "0", "vorschau_menu_beschwoeren_d2_standard_v16_1x_closed.png"),
    ("standard", "1x", "1", "vorschau_menu_beschwoeren_d2_standard_v16_1x_open.png"),
]


def render():
    if not HTML.exists():
        raise SystemExit(f"HTML missing: {HTML}")
    for mode, pull, opened, filename in STATES:
        params = urlencode({"mode": mode, "pull": pull, "open": opened})
        uri = f"{HTML.resolve().as_uri()}?{params}"
        output = OUT / filename
        with tempfile.NamedTemporaryFile(suffix=".png", dir=OUT, delete=False) as temp:
            temp_path = Path(temp.name)
        try:
            subprocess.run([
                "google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
                "--hide-scrollbars", "--allow-file-access-from-files",
                "--force-device-scale-factor=1", f"--window-size={WIDTH},{HEIGHT}",
                "--virtual-time-budget=5000", "--run-all-compositor-stages-before-draw",
                f"--screenshot={temp_path}", uri,
            ], check=True, capture_output=True, timeout=90)
            with Image.open(temp_path) as img:
                if img.size != (WIDTH, HEIGHT):
                    raise RuntimeError(f"Unexpected screenshot size {img.size}: {filename}")
                img.convert("RGB").save(output, format="PNG", optimize=True)
            print(f"{output.relative_to(HUD.parent.parent.parent)}  {WIDTH}x{HEIGHT}  {output.stat().st_size:,} bytes")
        finally:
            temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    render()
