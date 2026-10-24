#!/usr/bin/env python3
"""Render eight simultaneous resource slots in the D2 village HUD."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
HUD = HERE.parent
ROOT = HUD.parents[2]
CHROME = HUD / "vorschau_hud_d2_v7_3_lvl12.png"
ASSETS = ROOT / "team/art/ui-kit/menus_v3/_src/inventar_v4_assets"
OUTPUT = HUD / "vorschau_overlay_ressourcen_d2_v3b.png"

W, H = 1080, 1920
FONT_BALOO = ASSETS / "Baloo2-Variable.ttf"
FONT_LILITA = ASSETS / "LilitaOne-Regular.ttf"

C_TEXT = (242, 235, 220, 255)
C_MUTED = (165, 163, 153, 255)
C_GLUT = (255, 146, 49, 255)
C_GOLD = (255, 196, 92, 255)
C_WOOD = (241, 154, 62, 255)
C_STONE = (174, 176, 175, 255)
C_FOOD = (255, 126, 48, 255)
C_KNOWLEDGE = (166, 152, 255, 255)

SLOTS = [
    {"name": "NAHRUNG", "icon": "nahrung.png", "amount": 14900, "capacity": 20000,
     "items": 1, "item_name": "FASS", "yield": 5000, "rate": 960,
     "accent": C_FOOD, "enabled": True},
    {"name": "HOLZ", "icon": "holz.png", "amount": 12480, "capacity": 20000,
     "items": 3, "item_name": "KISTE", "yield": 2500, "rate": 420,
     "accent": C_WOOD, "enabled": True},
    {"name": "STEIN", "icon": "stein.png", "amount": 8215, "capacity": 20000,
     "items": 0, "item_name": "FASS", "yield": 0, "rate": 180,
     "accent": C_STONE, "enabled": True},
    {"name": "MUSCHELN", "icon": "gold.png", "amount": 3270, "capacity": 8000,
     "items": 2, "item_name": "BEUTEL", "yield": 100, "rate": 12,
     "accent": C_GOLD, "enabled": True, "skin": "GOLD-SKIN"},
    {"name": "WISSEN", "icon": "wissen.png", "amount": 930, "capacity": 5000,
     "items": 1, "item_name": "FOLIANT", "yield": 250, "rate": 75,
     "accent": C_KNOWLEDGE, "enabled": True},
    {"name": "BERNSTEIN", "locked": True, "state": "GESPERRT · LEER"},
    {"name": "METALL", "locked": True, "state": "GESPERRT"},
    {"name": "EPOCHE", "locked": True, "state": "GESPERRT"},
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
    d.rounded_rectangle((cx - 13, cy - 3, cx + 13, cy + 3), 3, fill=color)
    d.rounded_rectangle((cx - 3, cy - 13, cx + 3, cy + 13), 3, fill=color)


def draw_lock(d: ImageDraw.ImageDraw, cx: int, cy: int, color) -> None:
    d.arc((cx - 12, cy - 16, cx + 12, cy + 12), 180, 360, fill=color, width=3)
    d.rounded_rectangle((cx - 15, cy - 2, cx + 15, cy + 22), 5,
                        fill=(40, 43, 44, 255), outline=color, width=2)
    d.ellipse((cx - 2, cy + 5, cx + 2, cy + 9), fill=color)
    d.line((cx, cy + 8, cx, cy + 14), fill=color, width=2)


def draw_action(base: Image.Image, x: int, y: int, width: int, height: int,
                row: dict, enabled: bool) -> None:
    if enabled:
        glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
        ImageDraw.Draw(glow).polygon(chamfer_points(x - 2, y - 2, width + 4, height + 4, 15),
                                     fill=(255, 124, 32, 80))
        base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(8)))
        top, bottom = (255, 163, 56), (192, 58, 22)
        edge, ink = (255, 199, 126, 230), (255, 247, 229, 255)
        shadow = (84, 37, 19, 255)
    else:
        top, bottom = (104, 101, 94), (50, 52, 51)
        edge, ink = (150, 145, 134, 190), (182, 178, 168, 255)
        shadow = (32, 33, 32, 255)

    d = ImageDraw.Draw(base, "RGBA")
    d.polygon(chamfer_points(x, y + 4, width, height, 15), fill=shadow)
    chamfer_gradient(base, (x, y, width, height - 4), top, bottom, 15, edge)
    d = ImageDraw.Draw(base, "RGBA")
    d.line((x + 17, y + 5, x + width - 17, y + 5),
           fill=(255, 234, 197, 50) if enabled else (226, 222, 211, 28), width=1)
    draw_plus(d, x + width // 2, y + 38, ink)
    d.text((x + width / 2, y + 70), "EINSETZEN", font=font(FONT_BALOO, 12),
           fill=ink, anchor="mm")
    d.text((x + width / 2, y + 101), f"+{number(row['yield'])}",
           font=font(FONT_LILITA, 20), fill=ink, anchor="mm")


def draw_active_tile(base: Image.Image, x: int, y: int, width: int, height: int, row: dict) -> None:
    button_enabled = row["items"] > 0
    accent = row["accent"]
    border = (132, 91, 48, 220) if button_enabled else (91, 88, 80, 205)
    rounded_gradient(base, (x, y, x + width, y + height), (34, 34, 31), (15, 19, 22), 17,
                     outline=border, outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x + 11, y + 10, x + width - 12, y + 13), 1,
                        fill=accent[:3] + ((205 if button_enabled else 115),))

    icon = fit_icon(ASSETS / row["icon"], 50)
    base.alpha_composite(icon, (x + 14, y + 19))
    d = ImageDraw.Draw(base, "RGBA")
    title_xy = (x + 72, y + 15)
    d.text(title_xy, row["name"], font=font(FONT_BALOO, 20), fill=C_TEXT,
           stroke_width=1, stroke_fill=(9, 11, 12, 170))
    if row.get("skin"):
        title_w = d.textbbox(title_xy, row["name"], font=font(FONT_BALOO, 20))[2] - title_xy[0]
        tag_x = x + 72 + title_w + 7
        d.rounded_rectangle((tag_x, y + 19, tag_x + 73, y + 37), 8,
                            fill=(70, 52, 24, 255), outline=(173, 129, 58, 220), width=1)
        d.text((tag_x + 36, y + 21), row["skin"], font=font(FONT_BALOO, 10),
               fill=C_GOLD, anchor="ma")

    stock = f"{number(row['amount'])} / {number(row['capacity'])}"
    d.text((x + 72, y + 43), stock, font=font(FONT_LILITA, 16), fill=(218, 215, 203, 255))
    bar = (x + 72, y + 68, x + 278, y + 76)
    d.rounded_rectangle(bar, 4, fill=(9, 13, 15, 255), outline=(78, 77, 70, 200), width=1)
    fill_w = max(2, round((bar[2] - bar[0] - 2) * row["amount"] / row["capacity"]))
    d.rounded_rectangle((bar[0] + 1, bar[1] + 1, bar[0] + fill_w, bar[3] - 1), 3,
                        fill=accent[:3] + (255,))

    d.text((x + 15, y + 90), "PRODUKTION", font=font(FONT_BALOO, 11), fill=C_MUTED)
    d.text((x + 15, y + 109), f"+{number(row['rate'])}/h", font=font(FONT_LILITA, 18),
           fill=accent if row["rate"] != 0 else C_MUTED)
    d.line((x + 113, y + 91, x + 113, y + 150), fill=(92, 87, 76, 210), width=1)
    d.text((x + 127, y + 90), "EINSETZ-STACK", font=font(FONT_BALOO, 11), fill=C_MUTED)
    d.text((x + 127, y + 109), f"×{row['items']}  {row['item_name']}",
           font=font(FONT_BALOO, 16), fill=C_TEXT if button_enabled else C_MUTED)

    draw_action(base, x + 293, y + 20, 116, 132, row, button_enabled)


def draw_locked_tile(base: Image.Image, x: int, y: int, width: int, height: int, row: dict) -> None:
    rounded_gradient(base, (x, y, x + width, y + height), (27, 29, 30), (13, 17, 19), 17,
                     outline=(76, 79, 78, 210), outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x + 11, y + 10, x + width - 12, y + 13), 1,
                        fill=(104, 106, 102, 115))
    d.text((x + 17, y + 20), row["name"], font=font(FONT_BALOO, 20),
           fill=(184, 184, 177, 255))
    d.text((x + 18, y + 52), row["state"], font=font(FONT_BALOO, 12),
           fill=(161, 157, 146, 255))
    d.rounded_rectangle((x + 17, y + 81, x + 278, y + 89), 4,
                        fill=(9, 12, 14, 255), outline=(66, 69, 68, 180), width=1)
    d.text((x + 18, y + 103), "SLOT NOCH NICHT AKTIV", font=font(FONT_BALOO, 13),
           fill=(129, 131, 128, 255))

    # A muted chamfered lock plate occupies the same action area as active slots.
    bx, by, bw, bh = x + 293, y + 20, 116, 132
    d.polygon(chamfer_points(bx, by + 4, bw, bh, 15), fill=(26, 28, 29, 255))
    chamfer_gradient(base, (bx, by, bw, bh - 4), (62, 65, 64), (35, 38, 39), 15,
                     (95, 98, 96, 155))
    d = ImageDraw.Draw(base, "RGBA")
    draw_lock(d, bx + bw // 2, by + 51, (160, 161, 154, 225))
    d.text((bx + bw / 2, by + 99), "GESPERRT", font=font(FONT_BALOO, 11),
           fill=(166, 164, 155, 255), anchor="mm")


def draw_chest_target(base: Image.Image) -> None:
    x, y, size = 252, 200, 88
    left, top, right, bottom = x - 9, y - 9, x + size + 9, y + size + 9
    d = ImageDraw.Draw(base, "RGBA")
    color = (255, 151, 48, 245)
    length = 19
    for sx, sy, dx, dy in ((left, top, 1, 1), (right, top, -1, 1),
                           (left, bottom, 1, -1), (right, bottom, -1, -1)):
        d.line((sx, sy, sx + dx * length, sy), fill=color, width=3)
        d.line((sx, sy, sx, sy + dy * length), fill=color, width=3)


def draw_panel(base: Image.Image) -> None:
    px, py, pw, ph = 150, 304, 900, 906
    rounded_gradient(base, (px, py, px + pw, py + ph), (27, 31, 33), (9, 14, 18), 23,
                     outline=(172, 116, 64, 235), outline_width=2)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((px + 7, py + 7, px + pw - 8, py + ph - 8), 18,
                        outline=(184, 150, 103, 65), width=1)
    d.rounded_rectangle((px + 22, py + 18, px + 27, py + 56), 2, fill=C_GLUT)
    d.text((px + 39, py + 10), "LAGER", font=font(FONT_LILITA, 33), fill=C_TEXT,
           stroke_width=1, stroke_fill=(9, 11, 12, 190))
    d.text((px + 41, py + 47), "8 SPEICHERPLÄTZE  ·  DORFRESERVEN",
           font=font(FONT_BALOO, 13), fill=C_MUTED)

    # Four compact rows of two resource slots; every slot is on this single view.
    tile_x = (px + 20, px + 457)
    tile_y0, tile_w, tile_h, gap_y = py + 80, 423, 174, 12
    for index, row in enumerate(SLOTS):
        col, line = index % 2, index // 2
        x, y = tile_x[col], tile_y0 + line * (tile_h + gap_y)
        if row.get("locked"):
            draw_locked_tile(base, x, y, tile_w, tile_h, row)
        else:
            draw_active_tile(base, x, y, tile_w, tile_h, row)

    total = sum(row["rate"] for row in SLOTS if not row.get("locked"))
    fy, fh = py + 820, 62
    rounded_gradient(base, (px + 20, fy, px + pw - 20, fy + fh),
                     (22, 27, 29), (11, 16, 19), 15,
                     outline=(108, 87, 64, 205), outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((px + 35, fy + 15, px + 39, fy + 47), 2, fill=C_GLUT)
    d.text((px + 53, fy + 15), "GESAMTPRODUKTION /h", font=font(FONT_BALOO, 15),
           fill=(198, 190, 171, 255))
    d.text((px + pw - 39, fy + 5), f"+{number(total)} /h", font=font(FONT_LILITA, 29),
           fill=(255, 218, 166, 255), anchor="ra",
           stroke_width=1, stroke_fill=(19, 15, 12, 190))


def render() -> Path:
    if not CHROME.is_file():
        raise SystemExit(f"HUD-Chrome fehlt: {CHROME}")
    image = Image.open(CHROME).convert("RGBA")
    if image.size != (W, H):
        raise SystemExit(f"Erwartet HUD-Chrome {W}×{H}, erhalten: {image.width}×{image.height}")

    # 67% scrim over the playfield only; top HUD and bottom dock stay clear.
    scrim = Image.new("RGBA", image.size, (0, 0, 0, 0))
    ImageDraw.Draw(scrim).rectangle((150, 292, W - 1, 1707), fill=(3, 7, 10, 170))
    image.alpha_composite(scrim)
    draw_chest_target(image)
    draw_panel(image)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(OUTPUT, optimize=True)
    return OUTPUT


if __name__ == "__main__":
    print(render())
