#!/usr/bin/env python3
"""Render a new resource-control dashboard inside the D2 village HUD."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
HUD = HERE.parent
ROOT = HUD.parents[2]
CHROME = HUD / "vorschau_hud_d2_v7_3_lvl12.png"
ASSETS = ROOT / "team/art/ui-kit/menus_v3/_src/inventar_v4_assets"
OUTPUT = HUD / "vorschau_overlay_ressourcen_d2_v3.png"

W, H = 1080, 1920
FONT_BALOO = ASSETS / "Baloo2-Variable.ttf"
FONT_LILITA = ASSETS / "LilitaOne-Regular.ttf"

C_TEXT = (243, 235, 216, 255)
C_MUTED = (171, 166, 151, 255)
C_GLUT = (255, 143, 48, 255)
C_WOOD = (255, 166, 67, 255)
C_STONE = (177, 177, 171, 255)
C_FOOD = (255, 126, 48, 255)

ROWS = [
    {"name": "HOLZ", "icon": "holz.png", "amount": 12480, "capacity": 20000,
     "items": 3, "item_name": "KISTE", "yield": 2500, "rate": 420,
     "series": [0.20, 0.33, 0.28, 0.49, 0.44, 0.61, 0.74], "accent": C_WOOD, "enabled": True},
    {"name": "STEIN", "icon": "stein.png", "amount": 8215, "capacity": 20000,
     "items": 0, "item_name": "FASS", "yield": 0, "rate": 180,
     "series": [0.18, 0.24, 0.20, 0.31, 0.29, 0.39, 0.46], "accent": C_STONE, "enabled": False},
    {"name": "NAHRUNG", "icon": "nahrung.png", "amount": 14900, "capacity": 20000,
     "items": 1, "item_name": "FASS", "yield": 5000, "rate": 960,
     "series": [0.24, 0.30, 0.42, 0.39, 0.57, 0.70, 0.84], "accent": C_FOOD, "enabled": True},
]


def font(path: Path, size: int, weight: int = 800) -> ImageFont.FreeTypeFont:
    result = ImageFont.truetype(str(path), size)
    if path == FONT_BALOO:
        try:
            result.set_variation_by_axes([weight])
        except (AttributeError, OSError):
            pass
    return result


def number(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def fit_icon(path: Path, size: int) -> Image.Image:
    icon = Image.open(path).convert("RGBA")
    icon.thumbnail((size, size), Image.Resampling.LANCZOS)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.alpha_composite(icon, ((size - icon.width) // 2, (size - icon.height) // 2))
    return out


def rounded_gradient(base: Image.Image, box, top, bottom, radius: int,
                     outline=None, outline_width: int = 1) -> None:
    x0, y0, x1, y1 = box
    width, height = x1 - x0, y1 - y0
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = layer.load()
    for yy in range(height):
        t = yy / max(height - 1, 1)
        color = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        for xx in range(width):
            pixels[xx, yy] = (*color, 255)
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width - 1, height - 1), radius, fill=255)
    layer.putalpha(mask)
    base.alpha_composite(layer, (x0, y0))
    if outline:
        ImageDraw.Draw(base, "RGBA").rounded_rectangle(
            (x0, y0, x1 - 1, y1 - 1), radius, outline=outline, width=outline_width
        )


def cut_points(x: int, y: int, width: int, height: int, cut: int):
    return [(x + cut, y), (x + width - cut, y), (x + width, y + height // 2),
            (x + width - cut, y + height), (x + cut, y + height),
            (x, y + height - cut), (x, y + cut)]


def cut_gradient(base: Image.Image, box, top, bottom, cut: int, outline) -> None:
    x, y, width, height = box
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = layer.load()
    for yy in range(height):
        t = yy / max(height - 1, 1)
        color = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        for xx in range(width):
            pixels[xx, yy] = (*color, 255)
    mask = Image.new("L", (width, height), 0)
    local = [(px - x, py - y) for px, py in cut_points(x, y, width, height, cut)]
    ImageDraw.Draw(mask).polygon(local, fill=255)
    layer.putalpha(mask)
    base.alpha_composite(layer, (x, y))
    ImageDraw.Draw(base, "RGBA").polygon(cut_points(x, y, width, height, cut), outline=outline, width=1)


def draw_meter(base: Image.Image, x: int, y: int, size: int, fraction: float, label: str,
               accent) -> None:
    d = ImageDraw.Draw(base, "RGBA")
    box = (x + 4, y + 4, x + size - 4, y + size - 4)
    d.ellipse(box, fill=(11, 14, 16, 255), outline=(75, 75, 70, 255), width=4)
    d.arc(box, start=-90, end=-90 + round(360 * fraction), fill=accent, width=4)
    d.text((x + size / 2, y + size / 2), label, font=font(FONT_LILITA, 14),
           fill=C_TEXT if fraction > 0.25 else C_MUTED, anchor="mm")


def draw_sparkline(base: Image.Image, box, series, color) -> None:
    x, y, width, height = box
    pad = 4
    low, high = min(series), max(series)
    span = max(high - low, 0.01)
    points = [(x + pad + i * (width - 2 * pad) / (len(series) - 1),
               y + height - pad - (value - low) / span * (height - 2 * pad))
              for i, value in enumerate(series)]
    d = ImageDraw.Draw(base, "RGBA")
    d.line(points, fill=color, width=2, joint="curve")
    px, py = points[-1]
    d.ellipse((px - 3, py - 3, px + 3, py + 3), fill=color)


def draw_action(base: Image.Image, x: int, y: int, width: int, height: int, row) -> None:
    enabled = row["enabled"]
    if enabled:
        glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
        ImageDraw.Draw(glow).polygon(cut_points(x - 2, y - 1, width + 4, height + 4, 15),
                                     fill=(255, 127, 37, 90))
        base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(9)))
        top, bottom = (255, 151, 48), (204, 66, 19)
        edge, badge, ink = (255, 190, 105, 225), (125, 48, 20, 255), (255, 247, 228, 255)
        shadow = (100, 39, 17, 255)
    else:
        top, bottom = (105, 101, 92), (53, 54, 52)
        edge, badge, ink = (150, 145, 133, 180), (43, 43, 41, 255), (181, 177, 167, 255)
        shadow = (34, 34, 32, 255)

    d = ImageDraw.Draw(base, "RGBA")
    d.polygon(cut_points(x, y + 4, width, height, 15), fill=shadow)
    cut_gradient(base, (x, y, width, height - 4), top, bottom, 15, edge)
    d = ImageDraw.Draw(base, "RGBA")
    # Compact hex sigil carries the plus; the wide clipped CTA avoids the old round-button look.
    hx, hy = x + 14, y + 24
    hexagon = [(hx + 12, hy), (hx + 36, hy), (hx + 48, hy + 24),
               (hx + 36, hy + 48), (hx + 12, hy + 48), (hx, hy + 24)]
    d.polygon(hexagon, fill=badge, outline=edge)
    cx, cy = hx + 24, hy + 24
    d.rounded_rectangle((cx - 12, cy - 2, cx + 12, cy + 2), 2, fill=ink)
    d.rounded_rectangle((cx - 2, cy - 12, cx + 2, cy + 12), 2, fill=ink)
    d.text((x + 75, y + 17), "EINSETZEN", font=font(FONT_BALOO, 14),
           fill=ink, stroke_width=1, stroke_fill=(21, 15, 12, 90))
    d.text((x + 75, y + 39), f"+{number(row['yield'])}", font=font(FONT_LILITA, 25),
           fill=ink, stroke_width=1, stroke_fill=(21, 15, 12, 90))


def draw_resource_tile(base: Image.Image, x: int, y: int, width: int, height: int, row) -> None:
    enabled = row["enabled"]
    accent = row["accent"]
    frame = (141, 92, 46, 220) if enabled else (90, 88, 81, 220)
    rounded_gradient(base, (x, y, x + width, y + height), (35, 33, 29), (15, 19, 22), 20,
                     outline=frame, outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x + 12, y + 12, x + width - 12, y + 15), 1,
                        fill=accent[:3] + ((210 if enabled else 110),))

    icon = fit_icon(ASSETS / row["icon"], 56)
    base.alpha_composite(icon, (x + 14, y + 20))
    d.text((x + 78, y + 27), row["name"], font=font(FONT_BALOO, 21),
           fill=C_TEXT if enabled else (204, 201, 193, 255),
           stroke_width=1, stroke_fill=(7, 9, 10, 190))
    pct = row["amount"] / row["capacity"]
    draw_meter(base, x + width - 72, y + 17, 58, pct, f"{int(pct * 100 + 0.5)}%", accent)

    d = ImageDraw.Draw(base, "RGBA")
    d.text((x + 16, y + 86), number(row["amount"]), font=font(FONT_LILITA, 31),
           fill=C_TEXT, stroke_width=1, stroke_fill=(7, 9, 10, 190))
    d.text((x + 18, y + 122), f"VON {number(row['capacity'])}",
           font=font(FONT_BALOO, 14), fill=C_MUTED)

    prod_box = (x + 13, y + 159, x + width - 13, y + 239)
    rounded_gradient(base, prod_box, (20, 23, 24), (11, 15, 17), 12,
                     outline=(67, 69, 66, 190), outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.text((x + 25, y + 168), "PRODUKTION /h", font=font(FONT_BALOO, 13), fill=C_MUTED)
    d.text((x + 25, y + 189), f"+{number(row['rate'])}/h", font=font(FONT_LILITA, 22),
           fill=accent if enabled else (205, 203, 194, 255))
    draw_sparkline(base, (x + 146, y + 178, 104, 48), row["series"], accent)

    # Pack count sits in a separate inventory chip, away from the per-hour meter.
    chip = (x + 14, y + 250, x + width - 14, y + 286)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle(chip, 10, fill=(12, 15, 17, 245),
                        outline=(76, 75, 69, 200), width=1)
    d.rounded_rectangle((x + 25, y + 260, x + 42, y + 277), 3,
                        fill=(94, 65, 39, 255) if enabled else (72, 70, 65, 255),
                        outline=(171, 132, 81, 170) if enabled else (126, 122, 112, 150), width=1)
    d.line((x + 33, y + 260, x + 33, y + 277), fill=(195, 158, 104, 155), width=1)
    d.text((x + 52, y + 255), f"×{row['items']}  ·  {row['item_name']}",
           font=font(FONT_BALOO, 17), fill=C_TEXT if enabled else C_MUTED)

    draw_action(base, x + 14, y + 294, width - 28, 96, row)


def draw_production_footer(base: Image.Image, x: int, y: int, width: int, height: int) -> None:
    rounded_gradient(base, (x, y, x + width, y + height), (23, 28, 30), (12, 17, 20), 18,
                     outline=(100, 84, 64, 210), outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.text((x + 22, y + 13), "LIVE-PRODUKTION /h", font=font(FONT_BALOO, 16),
           fill=(194, 187, 169, 255))
    d.text((x + width - 22, y + 4), "+1.560 /h", font=font(FONT_LILITA, 34),
           fill=(255, 218, 166, 255), anchor="ra",
           stroke_width=1, stroke_fill=(24, 17, 12, 190))
    d.line((x + 21, y + 56, x + width - 21, y + 56), fill=(118, 90, 59, 205), width=1)

    rates = [("HOLZ", "+420/h", C_WOOD), ("STEIN", "+180/h", C_STONE),
             ("NAHRUNG", "+960/h", C_FOOD)]
    gap, cell_w = 10, (width - 44 - 2 * 10) // 3
    for index, (name, rate, color) in enumerate(rates):
        cx = x + 16 + index * (cell_w + gap)
        d.rounded_rectangle((cx, y + 71, cx + cell_w, y + 137), 11,
                            fill=(13, 18, 20, 255), outline=(67, 72, 70, 190), width=1)
        d.rounded_rectangle((cx + 12, y + 83, cx + 16, y + 124), 2, fill=color)
        d.text((cx + 27, y + 80), name, font=font(FONT_BALOO, 13), fill=C_MUTED)
        d.text((cx + 27, y + 100), rate, font=font(FONT_LILITA, 21), fill=C_TEXT)


def draw_chest_target(base: Image.Image) -> None:
    # Angular corner marks pick out the HUD chest without drawing a second control.
    x, y, size = 252, 200, 88
    left, top, right, bottom = x - 9, y - 9, x + size + 9, y + size + 9
    d = ImageDraw.Draw(base, "RGBA")
    color = (255, 151, 48, 245)
    length = 19
    for sx, sy, dx, dy in ((left, top, 1, 1), (right, top, -1, 1),
                           (left, bottom, 1, -1), (right, bottom, -1, -1)):
        d.line((sx, sy, sx + dx * length, sy), fill=color, width=3)
        d.line((sx, sy, sx, sy + dy * length), fill=color, width=3)
    d.ellipse((x + size // 2 - 2, y - 12, x + size // 2 + 2, y - 8), fill=(255, 190, 103, 255))


def draw_panel(base: Image.Image) -> None:
    px, py, pw, ph = 150, 304, 900, 690
    rounded_gradient(base, (px, py, px + pw, py + ph), (28, 32, 34), (9, 14, 18), 25,
                     outline=(174, 118, 65, 235), outline_width=2)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((px + 7, py + 7, px + pw - 8, py + ph - 8), 19,
                        outline=(183, 150, 104, 75), width=1)

    # Header is a compact dashboard masthead, not a warehouse/list title row.
    d.rounded_rectangle((px + 23, py + 22, px + 28, py + 61), 2, fill=C_GLUT)
    d.text((px + 40, py + 14), "LAGER", font=font(FONT_LILITA, 34), fill=C_TEXT,
           stroke_width=1, stroke_fill=(10, 12, 12, 210))
    d.text((px + 42, py + 51), "DORFRESERVEN  ·  AUSLASTUNG & EINSATZ",
           font=font(FONT_BALOO, 13), fill=C_MUTED)
    tag = (px + pw - 224, py + 24, px + pw - 22, py + 58)
    d.rounded_rectangle(tag, 16, fill=(12, 17, 19, 255), outline=(77, 87, 83, 210), width=1)
    d.ellipse((tag[0] + 11, tag[1] + 12, tag[0] + 20, tag[1] + 21), fill=C_GLUT)
    d.text((tag[0] + 29, tag[1] + 8), "DORFDEPOT · LIVE", font=font(FONT_BALOO, 13),
           fill=(215, 205, 182, 255))

    tile_y, tile_w, tile_h, gap = py + 86, 276, 400, 16
    tile_x = px + 20
    for index, row in enumerate(ROWS):
        draw_resource_tile(base, tile_x + index * (tile_w + gap), tile_y, tile_w, tile_h, row)

    draw_production_footer(base, px + 20, py + 508, pw - 40, 160)


def render() -> Path:
    if not CHROME.is_file():
        raise SystemExit(f"HUD-Chrome fehlt: {CHROME}")
    image = Image.open(CHROME).convert("RGBA")
    if image.size != (W, H):
        raise SystemExit(f"Erwartet HUD-Chrome {W}×{H}, erhalten: {image.width}×{image.height}")

    # Keep HUD top and bottom untouched; strongly darken only the village field behind text.
    scrim = Image.new("RGBA", image.size, (0, 0, 0, 0))
    ImageDraw.Draw(scrim).rectangle((150, 292, W - 1, 1707), fill=(3, 7, 10, 174))
    image.alpha_composite(scrim)
    draw_chest_target(image)
    draw_panel(image)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(OUTPUT, optimize=True)
    return OUTPUT


if __name__ == "__main__":
    print(render())
