#!/usr/bin/env python3
"""Render the v2e resources HUD panel with modern plus buttons and production."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
HUD = HERE.parent
ROOT = HUD.parents[2]
ASSETS = ROOT / "team/art/ui-kit/menus_v3/_src/inventar_v4_assets"
CHROME = HUD / "vorschau_hud_d2_v7_3_lvl12.png"
OUTPUT = HUD / "vorschau_overlay_ressourcen_d2_v2f.png"

W, H = 1080, 1920
FONT_BALOO = ASSETS / "Baloo2-Variable.ttf"
FONT_LILITA = ASSETS / "LilitaOne-Regular.ttf"

PALETTE = {
    "text": (243, 231, 207, 255),
    "text_muted": (185, 169, 136, 255),
    "bronze": (201, 138, 74, 255),
    "bronze_dim": (104, 76, 52, 255),
    "glut": (255, 138, 42, 255),
    "glut_light": (255, 177, 90, 255),
    "glut_text": (255, 217, 168, 255),
    "disabled": (128, 122, 113, 255),
    "disabled_text": (166, 158, 146, 255),
}

ROWS = [
    {
        "name": "HOLZ", "icon": "holz.png", "amount": 12480, "capacity": 20000,
        "items": 3, "item_name": "KISTE", "yield": 2500, "enabled": True,
    },
    {
        "name": "STEIN", "icon": "stein.png", "amount": 8215, "capacity": 20000,
        "items": 0, "item_name": "FASS", "yield": 0, "enabled": False,
    },
    {
        "name": "NAHRUNG", "icon": "nahrung.png", "amount": 14900, "capacity": 20000,
        "items": 1, "item_name": "FASS", "yield": 5000, "enabled": True,
    },
]


def font(path: Path, size: int, weight: int = 800) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(path), size)
    if path == FONT_BALOO:
        try:
            f.set_variation_by_axes([weight])
        except (AttributeError, OSError):
            pass
    return f


def money(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def fit_icon(path: Path, size: int) -> Image.Image:
    icon = Image.open(path).convert("RGBA")
    icon.thumbnail((size, size), Image.Resampling.LANCZOS)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.alpha_composite(icon, ((size - icon.width) // 2, (size - icon.height) // 2))
    return out


def draw_round_gradient(
    base: Image.Image,
    box: tuple[int, int, int, int],
    top: tuple[int, int, int],
    bottom: tuple[int, int, int],
    radius: int,
    outline: tuple[int, int, int, int] | None = None,
    outline_width: int = 1,
) -> None:
    x0, y0, x1, y1 = box
    width, height = x1 - x0, y1 - y0
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    px = layer.load()
    for y in range(height):
        t = y / max(1, height - 1)
        color = tuple(round(a + (b - a) * t) for a, b in zip(top, bottom))
        for x in range(width):
            px[x, y] = (*color, 255)
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width - 1, height - 1), radius, fill=255)
    base.paste(layer, (x0, y0), mask)
    if outline:
        ImageDraw.Draw(base, "RGBA").rounded_rectangle(
            (x0, y0, x1 - 1, y1 - 1), radius, outline=outline, width=outline_width
        )


def draw_modern_plus(base: Image.Image, bx: int, by: int, enabled: bool) -> None:
    """Draw a 96×96 D2 soft-square touch target with a clean plus glyph."""
    if enabled:
        glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
        ImageDraw.Draw(glow).rounded_rectangle(
            (bx - 3, by - 3, bx + 99, by + 99), radius=27,
            fill=(255, 119, 32, 68),
        )
        base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(9)))
        top, bottom = (250, 148, 53), (214, 76, 22)
        edge, glyph = (255, 191, 118, 210), (255, 247, 231, 255)
        glyph_shadow = (111, 48, 19, 100)
    else:
        top, bottom = (108, 103, 94), (60, 59, 55)
        edge, glyph = (155, 149, 137, 180), (187, 182, 171, 255)
        glyph_shadow = (34, 34, 32, 90)

    # One clean gradient surface with a small lower lip: modern, clear and tappable.
    d = ImageDraw.Draw(base, "RGBA")
    lip = (126, 48, 18, 255) if enabled else (39, 39, 37, 255)
    d.rounded_rectangle((bx, by + 4, bx + 96, by + 96), radius=23, fill=lip)
    draw_round_gradient(
        base, (bx, by, bx + 96, by + 92), top, bottom, 23,
        outline=edge, outline_width=1,
    )
    d = ImageDraw.Draw(base, "RGBA")
    highlight = (255, 237, 204, 42) if enabled else (239, 235, 222, 28)
    d.line((bx + 25, by + 5, bx + 71, by + 5), fill=highlight, width=1)

    # Vector plus: crisp arms with rounded joins, independent of display fonts.
    cx, cy = bx + 48, by + 45
    d.rounded_rectangle((cx - 15 + 1, cy - 3 + 2, cx + 15 + 1, cy + 3 + 2),
                        radius=3, fill=glyph_shadow)
    d.rounded_rectangle((cx - 3 + 1, cy - 15 + 2, cx + 3 + 1, cy + 15 + 2),
                        radius=3, fill=glyph_shadow)
    d.rounded_rectangle((cx - 15, cy - 3, cx + 15, cy + 3), radius=3, fill=glyph)
    d.rounded_rectangle((cx - 3, cy - 15, cx + 3, cy + 15), radius=3, fill=glyph)


def add_panel(base: Image.Image) -> None:
    x, y, w, h = 172, 304, 600, 506
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((x - 4, y + 8, x + w + 4, y + h + 14), 34, fill=(0, 0, 0, 190))
    base.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(20)))

    draw_round_gradient(base, (x, y, x + w, y + h), (50, 35, 26), (25, 18, 15), 30,
                        outline=(201, 138, 74, 240), outline_width=2)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x + 7, y + 7, x + w - 8, y + h - 8), 25,
                        outline=(112, 82, 55, 190), width=1)
    d.line((x + 28, y + 63, x + w - 28, y + 63), fill=(111, 78, 49, 210), width=2)

    d.text((x + 24, y + 13), "LAGER", font=font(FONT_BALOO, 25), fill=PALETTE["glut_text"],
           stroke_width=2, stroke_fill=(20, 12, 8, 255))
    d.text((x + 24, y + 43), "VORRÄTE UND EINSETZEN", font=font(FONT_BALOO, 15),
           fill=PALETTE["text_muted"])

    # Three 120 px rows keep the original v2 overlay geometry.
    for index, row in enumerate(ROWS):
        row_y = y + 64 + index * 120
        enabled = row["enabled"]
        row_fill = (43, 30, 23, 205) if enabled else (34, 29, 24, 225)
        d.rounded_rectangle((x + 12, row_y + 2, x + w - 12, row_y + 118), 16,
                            fill=row_fill, outline=(92, 67, 46, 190), width=1)
        if index:
            d.line((x + 26, row_y + 2, x + w - 132, row_y + 2), fill=(143, 104, 68, 100), width=1)

        icon = fit_icon(ASSETS / row["icon"], 72)
        base.alpha_composite(icon, (x + 24, row_y + 24))

        primary = PALETTE["text"] if enabled else (190, 181, 165, 255)
        secondary = PALETTE["text_muted"] if enabled else PALETTE["disabled_text"]
        d.text((x + 112, row_y + 13), row["name"], font=font(FONT_BALOO, 25), fill=primary,
               stroke_width=1, stroke_fill=(12, 8, 6, 210))
        current = f"{money(row['amount'])} / {money(row['capacity'])}"
        d.text((x + 112, row_y + 46), current, font=font(FONT_LILITA, 18), fill=secondary)

        # Inventory capacity bar.
        bar = (x + 112, row_y + 82, x + 248, row_y + 94)
        d.rounded_rectangle(bar, 6, fill=(16, 12, 10, 255), outline=(102, 78, 57, 235), width=1)
        fill_width = max(4, round((bar[2] - bar[0] - 2) * row["amount"] / row["capacity"]))
        bar_color = (211, 104, 35, 255) if enabled else (118, 105, 84, 255)
        d.rounded_rectangle((bar[0] + 1, bar[1] + 1, bar[0] + fill_width, bar[3] - 1), 5,
                            fill=bar_color)

        info = PALETTE["text_muted"] if enabled else PALETTE["disabled_text"]
        d.text((x + 264, row_y + 28), f"×{row['items']} · {row['item_name']}",
               font=font(FONT_BALOO, 20), fill=info)
        yield_color = PALETTE["glut_text"] if enabled else PALETTE["disabled_text"]
        d.text((x + 264, row_y + 59), f"+{money(row['yield'])} {row['name']}",
               font=font(FONT_LILITA, 20), fill=yield_color,
               stroke_width=1 if enabled else 0, stroke_fill=(12, 8, 6, 230))

        # 96×96 modern soft-square touch target, disabled with the same shape.
        bx, by = x + 480, row_y + 12
        draw_modern_plus(base, bx, by, enabled)

    # Separate persistent production rates from the one-off crate/barrel yields.
    footer = (x + 16, y + 432, x + w - 16, y + h - 12)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle(footer, 14, fill=(22, 16, 13, 235),
                        outline=(104, 76, 52, 200), width=1)
    d.rounded_rectangle((x + 23, y + 442, x + 27, y + 486), 2,
                        fill=PALETTE["glut"])
    d.text((x + 38, y + 438), "PRODUKTION /h", font=font(FONT_BALOO, 16),
           fill=PALETTE["glut_text"])
    d.text((x + w - 28, y + 436), "GESAMT +1.560 /h",
           font=font(FONT_LILITA, 20), fill=PALETTE["text"], anchor="ra")
    d.text((x + 38, y + 466), "HOLZ +420  ·  STEIN +180  ·  NAHRUNG +960",
           font=font(FONT_LILITA, 17), fill=PALETTE["text_muted"])


def render() -> Path:
    if not CHROME.is_file():
        raise SystemExit(f"HUD-Chrome fehlt: {CHROME}")
    image = Image.open(CHROME).convert("RGBA")
    if image.size != (W, H):
        raise SystemExit(f"Erwartet HUD-Chrome {W}×{H}, erhalten: {image.width}×{image.height}")

    # Dim only the village playfield. Keep the top resources, quick icons,
    # side controls and bottom dock at their original brightness.
    scrim = Image.new("RGBA", image.size, (0, 0, 0, 0))
    ImageDraw.Draw(scrim).rectangle((150, 300, W - 1, 1707), fill=(0, 0, 0, 82))
    image.alpha_composite(scrim)

    # Chest in the top quick-icon row is the source of this open HUD panel.
    chest_x, chest_y, chest_size = 252, 200, 88
    ring = Image.new("RGBA", (chest_size + 14, chest_size + 14), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((0, 0, chest_size + 13, chest_size + 13),
                                 outline=PALETTE["glut"][:3] + (220,), width=3)
    image.alpha_composite(ring, (chest_x - 7, chest_y - 7))

    add_panel(image)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(OUTPUT, optimize=True)
    return OUTPUT


if __name__ == "__main__":
    print(render())
