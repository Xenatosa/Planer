#!/usr/bin/env python3
"""Render the D2 resource bottom sheet on the approved village HUD Chrome."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
HUD = HERE.parent
ROOT = HUD.parents[2]
CHROME = HUD / "vorschau_hud_d2_v7_3_lvl12.png"
ASSETS = ROOT / "team/art/ui-kit/menus_v3/_src/inventar_v4_assets"
OUT = HUD / "vorschau_overlay_ressourcen_d2_v2c.png"

W, H = 1080, 1920
DOCK_Y = 1708
SHEET = (28, DOCK_Y - 20 - 580, 1024, 580)
FONT_BALOO = ASSETS / "Baloo2-Variable.ttf"
FONT_LILITA = ASSETS / "LilitaOne-Regular.ttf"

C_TEXT = (243, 231, 207, 255)
C_MUTED = (185, 169, 136, 255)
C_BRONZE = (201, 138, 74, 255)
C_BRONZE_HI = (230, 180, 110, 255)
C_GLUT = (255, 138, 42, 255)
C_GLUT_TEXT = (255, 217, 168, 255)
C_DISABLED = (133, 125, 112, 255)
C_DISABLED_TEXT = (169, 160, 146, 255)

ROWS = [
    {"name": "Holz", "icon": "holz.png", "amount": 12480, "capacity": 20000,
     "items": 3, "item": "KISTE", "yield": 2500},
    {"name": "Stein", "icon": "stein.png", "amount": 8215, "capacity": 20000,
     "items": 0, "item": "FASS", "yield": 0},
    {"name": "Nahrung", "icon": "nahrung.png", "amount": 14900, "capacity": 20000,
     "items": 1, "item": "FASS", "yield": 5000},
]


def font(name: str, size: int, weight: int = 800) -> ImageFont.FreeTypeFont:
    path = FONT_LILITA if name == "lilita" else FONT_BALOO
    result = ImageFont.truetype(str(path), size)
    if name == "baloo":
        try:
            result.set_variation_by_axes([weight])
        except (AttributeError, OSError):
            pass
    return result


def fmt(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def paste_icon(canvas: Image.Image, path: Path, x: int, y: int, size: int) -> None:
    icon = Image.open(path).convert("RGBA")
    icon.thumbnail((size, size), Image.Resampling.LANCZOS)
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    layer.alpha_composite(icon, ((size - icon.width) // 2, (size - icon.height) // 2))
    canvas.alpha_composite(layer, (x, y))


def rounded_gradient(canvas: Image.Image, box, top, bottom, radius: int, outline=None, width=1) -> None:
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = layer.load()
    for yy in range(h):
        t = yy / max(h - 1, 1)
        color = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        for xx in range(w):
            px[xx, yy] = (*color, 255)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=255)
    layer.putalpha(mask)
    canvas.alpha_composite(layer, (x0, y0))
    if outline:
        ImageDraw.Draw(canvas, "RGBA").rounded_rectangle(
            (x0, y0, x1 - 1, y1 - 1), radius, outline=outline, width=width
        )


def draw_scrim_and_opener(canvas: Image.Image) -> None:
    canvas.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 118)))
    # Kiste on the Chrome top row is the opener for this sheet.
    x, y, size = 252, 200, 88
    ring = Image.new("RGBA", (size + 14, size + 14), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((0, 0, size + 13, size + 13), outline=C_GLUT[:3] + (220,), width=3)
    canvas.alpha_composite(ring, (x - 7, y - 7))


def draw_sheet(canvas: Image.Image) -> None:
    sx, sy, sw, sh = SHEET
    shadow = Image.new("RGBA", (sw + 24, sh + 28), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((8, 10, sw + 15, sh + 18), 28,
                                             fill=(0, 0, 0, 200))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(16)), (sx - 12, sy - 8))
    rounded_gradient(canvas, (sx, sy, sx + sw, sy + sh), (61, 43, 31), (18, 13, 11), 24,
                     outline=C_BRONZE, width=3)
    d = ImageDraw.Draw(canvas, "RGBA")
    d.rounded_rectangle((sx + 5, sy + 5, sx + sw - 6, sy + sh - 6), 19,
                        outline=(255, 220, 160, 90), width=1)
    d.line((sx + 24, sy + 103, sx + sw - 24, sy + 103), fill=(112, 82, 55, 230), width=2)

    d.text((sx + 30, sy + 18), "LAGER", font=font("lilita", 48), fill=C_GLUT_TEXT,
           stroke_width=1, stroke_fill=(40, 20, 8, 255))
    d.text((sx + 34, sy + 72), "MAX. FÜLLSTAND", font=font("baloo", 20), fill=C_MUTED)
    draw_capacity_ring(canvas, sx + sw - 236, sy + 18, 74, 75)
    draw_close(canvas, sx + sw - 120, sy + 16, 96)

    row_y = sy + 120
    for i, row in enumerate(ROWS):
        y = row_y + i * 142
        active = row["items"] > 0
        draw_card(canvas, sx + 16, y, sw - 32, 130, active=False, radius=18)
        draw_icon_medallion(canvas, sx + 30, y + 20, 88, row["icon"],
                            accent=C_GLUT if active else C_DISABLED)

        d = ImageDraw.Draw(canvas, "RGBA")
        d.text((sx + 140, y + 10), row["name"], font=font("lilita", 32), fill=C_TEXT)
        d.text((sx + 140, y + 46), fmt(row["amount"]), font=font("lilita", 30),
               fill=(255, 239, 212, 255))
        d.text((sx + 263, y + 53), f"/ {fmt(row['capacity'])}", font=font("baloo", 21),
               fill=C_MUTED)
        draw_progress(canvas, sx + 140, y + 96, 330, 16,
                      row["amount"] / row["capacity"], color=C_GLUT if active else C_DISABLED)

        stats_color = C_MUTED if active else C_DISABLED_TEXT
        yield_color = C_GLUT_TEXT if active else C_DISABLED_TEXT
        d.text((sx + 492, y + 25), f"×{row['items']} · {row['item']}",
               font=font("baloo", 27), fill=stats_color)
        d.text((sx + 492, y + 61), f"+{fmt(row['yield'])} {row['name'].upper()}",
               font=font("lilita", 25), fill=yield_color,
               stroke_width=1 if active else 0, stroke_fill=(30, 17, 8, 230))

        draw_plus_button(canvas, sx + sw - 132, y + 17, 96, enabled=active)


def draw_card(canvas: Image.Image, x: int, y: int, w: int, h: int, active: bool, radius: int) -> None:
    top = (53, 38, 28) if active else (38, 28, 21)
    rounded_gradient(canvas, (x, y, x + w, y + h), top, (20, 15, 12), radius,
                     outline=(137, 108, 78, 185), width=1)
    ImageDraw.Draw(canvas, "RGBA").line((x + radius, y + 2, x + w - radius, y + 2),
                                        fill=(255, 229, 185, 100), width=1)


def draw_icon_medallion(canvas: Image.Image, x: int, y: int, size: int, icon: str, accent) -> None:
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse((4, 4, size - 5, size - 5), fill=(14, 10, 8, 230), outline=accent[:3] + (210,), width=2)
    d.ellipse((9, 9, size - 10, size - 10), outline=(255, 225, 170, 80), width=1)
    canvas.alpha_composite(layer, (x, y))
    paste_icon(canvas, ASSETS / icon, x + round(size * .135), y + round(size * .135), round(size * .73))


def draw_progress(canvas: Image.Image, x: int, y: int, w: int, h: int, ratio: float, color) -> None:
    d = ImageDraw.Draw(canvas, "RGBA")
    d.rounded_rectangle((x, y, x + w - 1, y + h - 1), radius=h // 2,
                        fill=(10, 8, 7, 255), outline=(111, 86, 62, 220), width=1)
    fill_w = max(5, min(w - 4, int((w - 4) * ratio)))
    d.rounded_rectangle((x + 2, y + 2, x + fill_w, y + h - 3),
                        radius=max(h // 2 - 2, 2), fill=color[:3] + (255,))
    d.line((x + 8, y + 3, x + max(8, fill_w - 4), y + 3),
           fill=(255, 225, 170, 120), width=1)


def draw_capacity_ring(canvas: Image.Image, x: int, y: int, size: int, pct: int) -> None:
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    box = (5, 5, size - 6, size - 6)
    d.ellipse(box, fill=(18, 13, 10, 245), outline=(120, 91, 62, 220), width=6)
    d.arc(box, -90, -90 + round(360 * pct / 100), fill=C_GLUT, width=8)
    d.arc((10, 10, size - 11, size - 11), 190, 300, fill=(255, 221, 156, 90), width=2)
    canvas.alpha_composite(layer, (x, y))
    d = ImageDraw.Draw(canvas)
    text = f"{pct}%"
    f = font("lilita", 24)
    b = d.textbbox((0, 0), text, font=f)
    d.text((x + (size - (b[2] - b[0])) / 2, y + (size - (b[3] - b[1])) / 2 - 3),
           text, font=f, fill=C_GLUT_TEXT, stroke_width=1, stroke_fill=(30, 17, 8))


def draw_close(canvas: Image.Image, x: int, y: int, size: int) -> None:
    rounded_gradient(canvas, (x, y, x + size, y + size), (46, 32, 23), (23, 16, 13), 22,
                     outline=C_BRONZE_HI, width=3)
    d = ImageDraw.Draw(canvas, "RGBA")
    c = C_GLUT_TEXT
    d.line((x + 33, y + 33, x + size - 33, y + size - 33), fill=c, width=7)
    d.line((x + size - 33, y + 33, x + 33, y + size - 33), fill=c, width=7)


def draw_plus_button(canvas: Image.Image, x: int, y: int, size: int, enabled: bool) -> None:
    if enabled:
        glow = Image.new("RGBA", (size + 28, size + 28), (0, 0, 0, 0))
        ImageDraw.Draw(glow).ellipse((4, 4, size + 23, size + 23), fill=(255, 126, 36, 115))
        canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(11)), (x - 14, y - 14))
        top, bottom, outline, plus = (255, 177, 90), (224, 91, 25), (255, 211, 145, 255), C_TEXT
    else:
        top, bottom = (99, 91, 79), (54, 50, 45)
        outline, plus = (138, 128, 113, 200), C_DISABLED_TEXT
    rounded_gradient(canvas, (x, y, x + size, y + size), top, bottom, size // 2,
                     outline=outline, width=2)
    d = ImageDraw.Draw(canvas, "RGBA")
    d.ellipse((x + 7, y + 7, x + size - 8, y + size - 8),
              outline=(255, 220, 160, 150) if enabled else (172, 161, 143, 90), width=1)
    d.text((x + size / 2, y + size / 2 - 3), "+", font=font("lilita", 54), fill=plus,
           anchor="mm", stroke_width=1,
           stroke_fill=(40, 22, 12, 190) if enabled else (31, 29, 26, 210))


def main() -> None:
    if not CHROME.is_file():
        raise SystemExit(f"Chrome-Vorschau fehlt: {CHROME}")
    canvas = Image.open(CHROME).convert("RGBA")
    if canvas.size != (W, H):
        raise SystemExit(f"Erwartet Chrome {W}×{H}, erhalten: {canvas.width}×{canvas.height}")
    draw_scrim_and_opener(canvas)
    draw_sheet(canvas)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUT, optimize=True)
    print(f"{OUT} · {W}×{H}")


if __name__ == "__main__":
    main()
