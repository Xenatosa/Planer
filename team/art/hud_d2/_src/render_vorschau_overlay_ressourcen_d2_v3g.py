#!/usr/bin/env python3
"""Render a twelve-tile, no-scroll resource capacity preview in the D2 HUD."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
HUD = HERE.parent
ROOT = HUD.parents[2]
CHROME = HUD / "vorschau_hud_d2_v7_3_lvl12.png"
ASSETS = ROOT / "team/art/ui-kit/menus_v3/_src/inventar_v4_assets"
OUTPUT = HUD / "vorschau_overlay_ressourcen_d2_v3g.png"

W, H = 1080, 1920
FONT_BALOO = ASSETS / "Baloo2-Variable.ttf"
FONT_LILITA = ASSETS / "LilitaOne-Regular.ttf"

C_TEXT = (242, 235, 220, 255)
C_MUTED = (163, 162, 153, 255)
C_GLUT = (255, 146, 49, 255)
C_FOOD = (255, 126, 48, 255)
C_WOOD = (241, 154, 62, 255)
C_STONE = (174, 176, 175, 255)
C_GOLD = (255, 197, 93, 255)
C_KNOWLEDGE = (174, 160, 255, 255)
C_AMBER = (255, 173, 78, 255)
C_METAL = (185, 192, 193, 255)
C_EPOCH = (133, 190, 218, 255)

SLOTS = [
    {"name": "NAHRUNG", "icon": "nahrung.png", "amount": 14900, "capacity": 20000,
     "items": 1, "item_name": "FASS", "yield": 5000, "rate": 960, "accent": C_FOOD},
    {"name": "HOLZ", "icon": "holz.png", "amount": 12480, "capacity": 20000,
     "items": 3, "item_name": "KISTE", "yield": 2500, "rate": 420, "accent": C_WOOD},
    {"name": "STEIN", "icon": "stein.png", "amount": 8215, "capacity": 20000,
     "items": 0, "item_name": "FASS", "yield": 0, "rate": 180, "accent": C_STONE},
    {"name": "MUSCHELN", "icon": "gold.png", "amount": 3270, "capacity": 8000,
     "items": 2, "item_name": "BEUTEL", "yield": 100, "rate": 12,
     "accent": C_GOLD, "tag": "GOLD-SKIN"},
    {"name": "WISSEN", "icon": "wissen.png", "amount": 930, "capacity": 5000,
     "items": 1, "item_name": "FOLIANT", "yield": 250, "rate": 75, "accent": C_KNOWLEDGE},
    {"name": "BERNSTEIN", "icon": "kristall.png", "amount": 1820, "capacity": 5000,
     "items": 2, "item_name": "AMPULLE", "yield": 120, "rate": 35, "accent": C_AMBER},
    {"name": "METALL", "icon": "metal", "amount": 6250, "capacity": 12000,
     "items": 2, "item_name": "BARREN", "yield": 400, "rate": 210, "accent": C_METAL},
    {"name": "EPOCHENMARKEN", "icon": "uhr.png", "amount": 760, "capacity": 3000,
     "items": 1, "item_name": "SIEGEL", "yield": 50, "rate": 24, "accent": C_EPOCH},
    {"name": "RUNEN", "locked": True},
    {"name": "ARTEFAKTE", "locked": True},
    {"name": "RELIQUIEN", "locked": True},
    {"name": "ESSENZ", "locked": True},
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


def chamfer_points(x: int, y: int, width: int, height: int, cut: int):
    return [(x + cut, y), (x + width - cut, y), (x + width, y + cut),
            (x + width, y + height - cut), (x + width - cut, y + height),
            (x + cut, y + height), (x, y + height - cut), (x, y + cut)]


def chamfer_gradient(base: Image.Image, box, top, bottom, cut: int, outline) -> None:
    x, y, width, height = box
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = layer.load()
    for yy in range(height):
        t = yy / max(height - 1, 1)
        color = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        for xx in range(width):
            pixels[xx, yy] = (*color, 255)
    mask = Image.new("L", (width, height), 0)
    pts = [(px - x, py - y) for px, py in chamfer_points(x, y, width, height, cut)]
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    layer.putalpha(mask)
    base.alpha_composite(layer, (x, y))
    ImageDraw.Draw(base, "RGBA").polygon(chamfer_points(x, y, width, height, cut),
                                           outline=outline, width=1)


def draw_plus(d: ImageDraw.ImageDraw, cx: int, cy: int, color,
              arm: int = 10, thickness: int = 4) -> None:
    radius = max(1, thickness // 2)
    d.rounded_rectangle((cx - arm, cy - thickness // 2,
                         cx + arm, cy + thickness // 2), radius, fill=color)
    d.rounded_rectangle((cx - thickness // 2, cy - arm,
                         cx + thickness // 2, cy + arm), radius, fill=color)


def draw_lock(d: ImageDraw.ImageDraw, cx: int, cy: int, color,
              scale: float = 1.0) -> None:
    sw = max(2, round(2 * scale))
    d.arc((cx - 8 * scale, cy - 11 * scale, cx + 8 * scale, cy + 9 * scale),
          180, 360, fill=color, width=sw)
    d.rounded_rectangle((cx - 10 * scale, cy - 1 * scale,
                         cx + 10 * scale, cy + 15 * scale), 3 * scale,
                        fill=(39, 42, 43, 255), outline=color, width=sw)
    d.ellipse((cx - 1 * scale, cy + 4 * scale,
               cx + 1 * scale, cy + 6 * scale), fill=color)
    d.line((cx, cy + 6 * scale, cx, cy + 10 * scale), fill=color, width=sw)


def draw_metal_icon(base: Image.Image, x: int, y: int, size: int) -> None:
    d = ImageDraw.Draw(base, "RGBA")
    w, h = size, size * 0.60
    points = [(x + 2, y + h * 0.36), (x + w * 0.24, y + 2),
              (x + w * 0.80, y + 2), (x + w - 2, y + h * 0.36),
              (x + w * 0.78, y + h), (x + w * 0.22, y + h)]
    d.polygon(points, fill=(116, 128, 132, 255), outline=(210, 216, 213, 230))
    d.line((x + w * 0.18, y + h * 0.40, x + w * 0.82, y + h * 0.40),
           fill=(230, 235, 232, 200), width=1)
    d.line((x + w * 0.22, y + h - 2, x + w * 0.48, y + h * 0.40),
           fill=(72, 82, 86, 210), width=1)


def draw_slot_icon(base: Image.Image, row: dict, x: int, y: int, size: int) -> None:
    if row["icon"] == "metal":
        draw_metal_icon(base, x + 2, y + 9, size - 4)
    else:
        icon = fit_icon(ASSETS / row["icon"], size)
        base.alpha_composite(icon, (x, y))


def draw_cta(base: Image.Image, x: int, y: int, width: int, height: int,
             row: dict, enabled: bool) -> None:
    if enabled:
        glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
        ImageDraw.Draw(glow).polygon(chamfer_points(x - 2, y - 1, width + 4, height + 3, 18),
                                     fill=(255, 121, 32, 75))
        base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(6)))
        top, bottom = (255, 151, 48), (198, 60, 19)
        edge, ink, badge = (255, 190, 111, 190), (255, 246, 229, 255), (124, 45, 17, 255)
    else:
        top, bottom = (97, 96, 89), (48, 51, 51)
        edge, ink, badge = (137, 136, 127, 165), (176, 174, 164, 255), (42, 44, 44, 255)

    d = ImageDraw.Draw(base, "RGBA")
    cut = max(14, height // 5)
    d.polygon(chamfer_points(x, y + 5, width, height, cut),
              fill=(91, 39, 19, 255) if enabled else (30, 32, 32, 255))
    chamfer_gradient(base, (x, y, width, height - 5), top, bottom, cut, edge)
    d = ImageDraw.Draw(base, "RGBA")
    cx, cy = x + 52, y + height // 2 - 2
    hexagon = [(cx - 18, cy - 28), (cx + 18, cy - 28), (cx + 31, cy),
               (cx + 18, cy + 28), (cx - 18, cy + 28), (cx - 31, cy)]
    d.polygon(hexagon, fill=badge, outline=edge)
    draw_plus(d, cx, cy, ink, arm=17, thickness=7)
    d.text((x + 100, cy), "EINSETZEN", font=font(FONT_BALOO, 24),
           fill=ink, anchor="lm")
    d.line((x + width - 30, cy - 12, x + width - 18, cy,
            x + width - 30, cy + 12), fill=ink, width=4)


def draw_active_tile(base: Image.Image, x: int, y: int, width: int, height: int, row: dict) -> None:
    can_use = row["items"] > 0
    accent = row["accent"]
    border = (130, 91, 49, 220) if can_use else (90, 88, 81, 210)
    rounded_gradient(base, (x, y, x + width, y + height), (34, 34, 31), (15, 19, 22), 18,
                     outline=border, outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x + 14, y + 12, x + width - 14, y + 16), 2,
                        fill=accent[:3] + ((205 if can_use else 110),))

    draw_slot_icon(base, row, x + 16, y + 20, 62)
    d = ImageDraw.Draw(base, "RGBA")
    title_x, title_y = x + 88, y + 21
    title_font = font(FONT_BALOO, 24)
    d.text((title_x, title_y), row["name"], font=title_font, fill=C_TEXT,
           stroke_width=1, stroke_fill=(8, 10, 11, 160))
    if row.get("tag"):
        tag_x = title_x
        d.rounded_rectangle((tag_x, y + 54, tag_x + 96, y + 78), 10,
                            fill=(75, 56, 24, 255), outline=(179, 134, 62, 210), width=1)
        d.text((tag_x + 48, y + 56), row["tag"], font=font(FONT_BALOO, 13),
               fill=C_GOLD, anchor="ma")

    stock_line = f"{number(row['amount'])} / {number(row['capacity'])}"
    d.text((x + 16, y + 94), stock_line, font=font(FONT_LILITA, 22),
           fill=(220, 216, 203, 255))
    bar = (x + 16, y + 128, x + width - 16, y + 141)
    d.rounded_rectangle(bar, 6, fill=(9, 13, 15, 255), outline=(76, 76, 70, 180), width=1)
    fill_width = max(2, round((bar[2] - bar[0] - 2) * row["amount"] / row["capacity"]))
    d.rounded_rectangle((bar[0] + 1, bar[1] + 1, bar[0] + fill_width, bar[3] - 1), 5,
                        fill=accent[:3] + (255,))

    d.text((x + 16, y + 157), f"PRODUKTION  +{number(row['rate'])}/h",
           font=font(FONT_BALOO, 17), fill=accent if can_use else (186, 183, 172, 255))
    d.text((x + 16, y + 190), f"×{row['items']} {row['item_name']}  →  +{number(row['yield'])}",
           font=font(FONT_BALOO, 20), fill=C_TEXT if can_use else C_MUTED)

    draw_cta(base, x + 14, y + 226, width - 28, 96, row, can_use)


def draw_locked_tile(base: Image.Image, x: int, y: int, width: int, height: int,
                     row: dict) -> None:
    rounded_gradient(base, (x, y, x + width, y + height), (27, 29, 30), (13, 17, 19), 18,
                     outline=(73, 77, 77, 205), outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x + 14, y + 12, x + width - 14, y + 16), 2,
                        fill=(99, 103, 101, 110))
    d.text((x + 16, y + 22), row["name"], font=font(FONT_BALOO, 23),
           fill=(188, 187, 179, 255))
    d.text((x + 16, y + 104), "Noch nicht freigeschaltet", font=font(FONT_BALOO, 17),
           fill=(147, 148, 142, 255))
    d.rounded_rectangle((x + 16, y + 151, x + width - 16, y + 164), 6,
                        fill=(9, 12, 14, 255), outline=(65, 68, 68, 170), width=1)
    d.text((x + 16, y + 180), "GESPERRT", font=font(FONT_BALOO, 17),
           fill=(124, 128, 126, 255))

    button_x, button_y, button_w, button_h = x + 14, y + 226, width - 28, 96
    d.polygon(chamfer_points(button_x, button_y + 5, button_w, button_h, 19),
              fill=(30, 32, 32, 255))
    chamfer_gradient(base, (button_x, button_y, button_w, button_h - 5),
                     (67, 70, 69), (37, 40, 40), 19, (91, 95, 94, 160))
    d = ImageDraw.Draw(base, "RGBA")
    center_y = button_y + button_h / 2 - 2
    draw_lock(d, button_x + 49, center_y - 1, (156, 158, 153, 220), scale=2.0)
    d.text((button_x + 93, center_y), "GESPERRT",
           font=font(FONT_BALOO, 22), fill=(166, 166, 158, 255), anchor="lm")


def draw_chest_target(base: Image.Image) -> None:
    x, y, size = 252, 200, 88
    left, top, right, bottom = x - 9, y - 9, x + size + 9, y + size + 9
    d = ImageDraw.Draw(base, "RGBA")
    color, length = (255, 151, 48, 245), 19
    for sx, sy, dx, dy in ((left, top, 1, 1), (right, top, -1, 1),
                           (left, bottom, 1, -1), (right, bottom, -1, -1)):
        d.line((sx, sy, sx + dx * length, sy), fill=color, width=3)
        d.line((sx, sy, sx, sy + dy * length), fill=color, width=3)


def draw_panel(base: Image.Image) -> None:
    # Nearly full-width panel extends to 24 px above the bottom of the canvas.
    px, py, pw, ph = 12, 304, 1056, 1592
    rounded_gradient(base, (px, py, px + pw, py + ph), (27, 31, 33), (9, 14, 18), 23,
                     outline=(172, 116, 64, 235), outline_width=2)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((px + 7, py + 7, px + pw - 8, py + ph - 8), 18,
                        outline=(184, 150, 103, 65), width=1)
    d.rounded_rectangle((px + 22, py + 18, px + 29, py + 63), 3, fill=C_GLUT)
    d.text((px + 43, py + 17), "LAGER", font=font(FONT_LILITA, 38), fill=C_TEXT,
           stroke_width=1, stroke_fill=(9, 11, 12, 190))

    margin_x, gap_x = 16, 10
    tile_w = (pw - margin_x * 2 - gap_x * 2) // 3
    tile_x = tuple(px + margin_x + col * (tile_w + gap_x) for col in range(3))
    tile_y0, tile_h, gap_y = py + 80, 340, 12
    for index, row in enumerate(SLOTS):
        col, line = index % 3, index // 3
        x = tile_x[col]
        y = tile_y0 + line * (tile_h + gap_y)
        if row.get("locked"):
            draw_locked_tile(base, x, y, tile_w, tile_h, row)
        else:
            draw_active_tile(base, x, y, tile_w, tile_h, row)

    total = sum(row["rate"] for row in SLOTS if not row.get("locked"))
    fy, fh = py + 1499, 68
    rounded_gradient(base, (px + 20, fy, px + pw - 20, fy + fh),
                     (22, 27, 29), (11, 16, 19), 15,
                     outline=(108, 87, 64, 205), outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((px + 35, fy + 15, px + 40, fy + 53), 3, fill=C_GLUT)
    d.text((px + 57, fy + 18), "GESAMTPRODUKTION /h", font=font(FONT_BALOO, 19),
           fill=(198, 190, 171, 255))
    d.text((px + pw - 36, fy + 7), f"+{number(total)} /h", font=font(FONT_LILITA, 34),
           fill=(255, 218, 166, 255), anchor="ra",
           stroke_width=1, stroke_fill=(19, 15, 12, 190))


def render() -> Path:
    if not CHROME.is_file():
        raise SystemExit(f"HUD-Chrome fehlt: {CHROME}")
    image = Image.open(CHROME).convert("RGBA")
    if image.size != (W, H):
        raise SystemExit(f"Erwartet HUD-Chrome {W}×{H}, erhalten: {image.width}×{image.height}")

    # Dim the complete HUD, including quest area and dock; place the Lager above it.
    draw_chest_target(image)
    scrim = Image.new("RGBA", image.size, (4, 7, 10, 255))
    alpha = Image.new("L", image.size, 0)
    mask = alpha.load()
    start_y, fade_y, end_y = 0, 1300, H
    for y in range(start_y, end_y):
        if y <= fade_y:
            opacity = 168
        else:
            progress = (y - fade_y) / (end_y - fade_y)
            opacity = round(168 + (105 - 168) * progress)
        for x in range(W):
            mask[x, y] = opacity
    scrim.putalpha(alpha)
    image.alpha_composite(scrim)
    draw_panel(image)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(OUTPUT, optimize=True)
    return OUTPUT


if __name__ == "__main__":
    print(render())
