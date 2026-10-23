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
OUTPUT = HUD / "vorschau_overlay_ressourcen_d2_v3d.png"

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


def draw_plus(d: ImageDraw.ImageDraw, cx: int, cy: int, color) -> None:
    d.rounded_rectangle((cx - 10, cy - 2, cx + 10, cy + 2), 2, fill=color)
    d.rounded_rectangle((cx - 2, cy - 10, cx + 2, cy + 10), 2, fill=color)


def draw_lock(d: ImageDraw.ImageDraw, cx: int, cy: int, color) -> None:
    d.arc((cx - 8, cy - 11, cx + 8, cy + 9), 180, 360, fill=color, width=2)
    d.rounded_rectangle((cx - 10, cy - 1, cx + 10, cy + 15), 3,
                        fill=(39, 42, 43, 255), outline=color, width=1)
    d.ellipse((cx - 1, cy + 4, cx + 1, cy + 6), fill=color)
    d.line((cx, cy + 6, cx, cy + 10), fill=color, width=1)


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
        ImageDraw.Draw(glow).polygon(chamfer_points(x - 2, y - 1, width + 4, height + 3, 10),
                                     fill=(255, 121, 32, 75))
        base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(6)))
        top, bottom = (255, 151, 48), (198, 60, 19)
        edge, ink, badge = (255, 190, 111, 190), (255, 246, 229, 255), (124, 45, 17, 255)
    else:
        top, bottom = (97, 96, 89), (48, 51, 51)
        edge, ink, badge = (137, 136, 127, 165), (176, 174, 164, 255), (42, 44, 44, 255)

    d = ImageDraw.Draw(base, "RGBA")
    d.polygon(chamfer_points(x, y + 3, width, height, 10),
              fill=(91, 39, 19, 255) if enabled else (30, 32, 32, 255))
    chamfer_gradient(base, (x, y, width, height - 3), top, bottom, 10, edge)
    d = ImageDraw.Draw(base, "RGBA")
    hx, hy = x + 8, y + 10
    hexagon = [(hx + 9, hy), (hx + 22, hy), (hx + 31, hy + 12),
               (hx + 22, hy + 24), (hx + 9, hy + 24), (hx, hy + 12)]
    d.polygon(hexagon, fill=badge, outline=edge)
    draw_plus(d, hx + 15, hy + 12, ink)
    d.text((x + 50, y + height / 2 - 1), "EINSETZEN", font=font(FONT_BALOO, 14),
           fill=ink, anchor="lm")
    d.line((x + width - 20, y + 19, x + width - 13, y + height / 2,
            x + width - 20, y + height - 20), fill=ink, width=2)


def draw_active_tile(base: Image.Image, x: int, y: int, width: int, height: int, row: dict) -> None:
    can_use = row["items"] > 0
    accent = row["accent"]
    border = (130, 91, 49, 220) if can_use else (90, 88, 81, 210)
    rounded_gradient(base, (x, y, x + width, y + height), (34, 34, 31), (15, 19, 22), 14,
                     outline=border, outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x + 10, y + 9, x + width - 10, y + 12), 1,
                        fill=accent[:3] + ((205 if can_use else 110),))

    draw_slot_icon(base, row, x + 11, y + 15, 37)
    d = ImageDraw.Draw(base, "RGBA")
    title_x, title_y = x + 54, y + 10
    title_font = font(FONT_BALOO, 16)
    d.text((title_x, title_y), row["name"], font=title_font, fill=C_TEXT,
           stroke_width=1, stroke_fill=(8, 10, 11, 160))
    if row.get("tag"):
        title_width = d.textbbox((title_x, title_y), row["name"], font=title_font)[2] - title_x
        tag_x = title_x + title_width + 5
        d.rounded_rectangle((tag_x, y + 12, tag_x + 68, y + 29), 7,
                            fill=(75, 56, 24, 255), outline=(179, 134, 62, 210), width=1)
        d.text((tag_x + 34, y + 13), row["tag"], font=font(FONT_BALOO, 9),
               fill=C_GOLD, anchor="ma")

    stock_line = f"{number(row['amount'])} / {number(row['capacity'])}"
    d.text((x + 12, y + 42), stock_line, font=font(FONT_LILITA, 14),
           fill=(220, 216, 203, 255))
    bar = (x + 12, y + 63, x + width - 12, y + 70)
    d.rounded_rectangle(bar, 4, fill=(9, 13, 15, 255), outline=(76, 76, 70, 180), width=1)
    fill_width = max(2, round((bar[2] - bar[0] - 2) * row["amount"] / row["capacity"]))
    d.rounded_rectangle((bar[0] + 1, bar[1] + 1, bar[0] + fill_width, bar[3] - 1), 3,
                        fill=accent[:3] + (255,))

    d.text((x + 12, y + 76), f"PRODUKTION  +{number(row['rate'])}/h",
           font=font(FONT_BALOO, 12), fill=accent if can_use else (186, 183, 172, 255))
    d.text((x + 12, y + 96), f"×{row['items']} {row['item_name']}  →  +{number(row['yield'])}",
           font=font(FONT_BALOO, 13), fill=C_TEXT if can_use else C_MUTED)

    draw_cta(base, x + 12, y + 122, width - 24, 54, row, can_use)


def draw_locked_tile(base: Image.Image, x: int, y: int, width: int, height: int,
                     row: dict) -> None:
    rounded_gradient(base, (x, y, x + width, y + height), (27, 29, 30), (13, 17, 19), 14,
                     outline=(73, 77, 77, 205), outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x + 10, y + 9, x + width - 10, y + 12), 1,
                        fill=(99, 103, 101, 110))
    d.text((x + 12, y + 13), row["name"], font=font(FONT_BALOO, 16),
           fill=(188, 187, 179, 255))
    d.text((x + 12, y + 45), "Noch nicht freigeschaltet", font=font(FONT_BALOO, 12),
           fill=(147, 148, 142, 255))
    d.rounded_rectangle((x + 12, y + 66, x + width - 12, y + 73), 3,
                        fill=(9, 12, 14, 255), outline=(65, 68, 68, 170), width=1)
    d.text((x + 12, y + 84), "GESPERRT", font=font(FONT_BALOO, 12),
           fill=(124, 128, 126, 255))

    button_x, button_y, button_w, button_h = x + 12, y + 122, width - 24, 54
    d.polygon(chamfer_points(button_x, button_y + 3, button_w, button_h, 10),
              fill=(30, 32, 32, 255))
    chamfer_gradient(base, (button_x, button_y, button_w, button_h - 3),
                     (67, 70, 69), (37, 40, 40), 10, (91, 95, 94, 160))
    d = ImageDraw.Draw(base, "RGBA")
    draw_lock(d, button_x + 30, button_y + 17, (156, 158, 153, 220))
    d.text((button_x + 54, button_y + button_h / 2 - 1), "GESPERRT",
           font=font(FONT_BALOO, 13), fill=(166, 166, 158, 255), anchor="lm")


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
    # Keep only a narrow safe margin; the warehouse card spans the HUD width.
    px, py, pw, ph = 12, 304, 1056, 960
    rounded_gradient(base, (px, py, px + pw, py + ph), (27, 31, 33), (9, 14, 18), 23,
                     outline=(172, 116, 64, 235), outline_width=2)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((px + 7, py + 7, px + pw - 8, py + ph - 8), 18,
                        outline=(184, 150, 103, 65), width=1)
    d.rounded_rectangle((px + 22, py + 17, px + 27, py + 55), 2, fill=C_GLUT)
    d.text((px + 39, py + 16), "LAGER", font=font(FONT_LILITA, 32), fill=C_TEXT,
           stroke_width=1, stroke_fill=(9, 11, 12, 190))

    margin_x, gap_x = 16, 10
    tile_w = (pw - margin_x * 2 - gap_x * 2) // 3
    tile_x = tuple(px + margin_x + col * (tile_w + gap_x) for col in range(3))
    tile_y0, tile_h, gap_y = py + 78, 188, 10
    for index, row in enumerate(SLOTS):
        col, line = index % 3, index // 3
        x = tile_x[col]
        y = tile_y0 + line * (tile_h + gap_y)
        if row.get("locked"):
            draw_locked_tile(base, x, y, tile_w, tile_h, row)
        else:
            draw_active_tile(base, x, y, tile_w, tile_h, row)

    total = sum(row["rate"] for row in SLOTS if not row.get("locked"))
    fy, fh = py + 884, 62
    rounded_gradient(base, (px + 20, fy, px + pw - 20, fy + fh),
                     (22, 27, 29), (11, 16, 19), 15,
                     outline=(108, 87, 64, 205), outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((px + 35, fy + 15, px + 39, fy + 47), 2, fill=C_GLUT)
    d.text((px + 53, fy + 15), "GESAMTPRODUKTION /h", font=font(FONT_BALOO, 15),
           fill=(198, 190, 171, 255))
    d.text((px + pw - 39, fy + 5), f"+{number(total)} /h", font=font(FONT_LILITA, 28),
           fill=(255, 218, 166, 255), anchor="ra",
           stroke_width=1, stroke_fill=(19, 15, 12, 190))


def render() -> Path:
    if not CHROME.is_file():
        raise SystemExit(f"HUD-Chrome fehlt: {CHROME}")
    image = Image.open(CHROME).convert("RGBA")
    if image.size != (W, H):
        raise SystemExit(f"Erwartet HUD-Chrome {W}×{H}, erhalten: {image.width}×{image.height}")

    # Solid, edge-to-edge Obsidian gray fully hides the village between HUD chrome.
    ImageDraw.Draw(image, "RGBA").rectangle((0, 292, W - 1, 1707),
                                             fill=(43, 47, 50, 255))
    draw_chest_target(image)
    draw_panel(image)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(OUTPUT, optimize=True)
    return OUTPUT


if __name__ == "__main__":
    print(render())
