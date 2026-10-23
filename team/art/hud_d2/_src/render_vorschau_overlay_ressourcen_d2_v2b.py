#!/usr/bin/env python3
"""Render the D2 resources overlay v2b preview with per-row use buttons."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
HUD = HERE.parent
ROOT = HUD.parents[2]
ASSETS = ROOT / "team/art/ui-kit/menus_v3/_src/inventar_v4_assets"
OUTPUT = HUD / "vorschau_overlay_ressourcen_d2_v2b.png"

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


def add_panel(base: Image.Image) -> None:
    x, y, w, h = 172, 326, 600, 448
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

    d.text((196, 339), "LAGER", font=font(FONT_BALOO, 25), fill=PALETTE["glut_text"],
           stroke_width=2, stroke_fill=(20, 12, 8, 255))
    d.text((196, 369), "VORRÄTE UND EINSETZEN", font=font(FONT_BALOO, 15),
           fill=PALETTE["text_muted"])

    # Three 120 px rows keep the original v2 overlay geometry.
    for index, row in enumerate(ROWS):
        row_y = 390 + index * 120
        enabled = row["enabled"]
        row_fill = (43, 30, 23, 205) if enabled else (34, 29, 24, 225)
        d.rounded_rectangle((184, row_y + 2, 760, row_y + 118), 16,
                            fill=row_fill, outline=(92, 67, 46, 190), width=1)
        if index:
            d.line((198, row_y + 2, 640, row_y + 2), fill=(143, 104, 68, 100), width=1)

        icon = fit_icon(ASSETS / row["icon"], 72)
        base.alpha_composite(icon, (196, row_y + 24))

        primary = PALETTE["text"] if enabled else (190, 181, 165, 255)
        secondary = PALETTE["text_muted"] if enabled else PALETTE["disabled_text"]
        d.text((284, row_y + 13), row["name"], font=font(FONT_BALOO, 25), fill=primary,
               stroke_width=1, stroke_fill=(12, 8, 6, 210))
        current = f"{money(row['amount'])} / {money(row['capacity'])}"
        d.text((284, row_y + 46), current, font=font(FONT_LILITA, 18), fill=secondary)

        # Inventory capacity bar.
        bar = (284, row_y + 82, 420, row_y + 94)
        d.rounded_rectangle(bar, 6, fill=(16, 12, 10, 255), outline=(102, 78, 57, 235), width=1)
        fill_width = max(4, round((bar[2] - bar[0] - 2) * row["amount"] / row["capacity"]))
        bar_color = (211, 104, 35, 255) if enabled else (118, 105, 84, 255)
        d.rounded_rectangle((bar[0] + 1, bar[1] + 1, bar[0] + fill_width, bar[3] - 1), 5,
                            fill=bar_color)

        info = PALETTE["text_muted"] if enabled else PALETTE["disabled_text"]
        d.text((436, row_y + 28), f"×{row['items']} · {row['item_name']}",
               font=font(FONT_BALOO, 20), fill=info)
        yield_color = PALETTE["glut_text"] if enabled else PALETTE["disabled_text"]
        d.text((436, row_y + 59), f"+{money(row['yield'])} {row['name']}",
               font=font(FONT_LILITA, 20), fill=yield_color,
               stroke_width=1 if enabled else 0, stroke_fill=(12, 8, 6, 230))

        # 96×96 touch target: orange and enabled when an item is available.
        bx, by, diameter = 652, row_y + 12, 96
        if enabled:
            glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
            ImageDraw.Draw(glow).ellipse((bx - 6, by - 5, bx + diameter + 6, by + diameter + 7),
                                         fill=(255, 126, 36, 105))
            base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(12)))
            draw_round_gradient(base, (bx, by, bx + diameter, by + diameter),
                                (255, 177, 90), (224, 91, 25), 48,
                                outline=(255, 211, 145, 255), outline_width=2)
            d = ImageDraw.Draw(base, "RGBA")
            d.ellipse((bx + 7, by + 7, bx + diameter - 8, by + diameter - 8),
                      outline=(255, 220, 160, 150), width=1)
            plus_color = (255, 247, 226, 255)
        else:
            draw_round_gradient(base, (bx, by, bx + diameter, by + diameter),
                                (100, 91, 78), (55, 51, 46), 48,
                                outline=(138, 128, 113, 200), outline_width=2)
            d = ImageDraw.Draw(base, "RGBA")
            d.ellipse((bx + 7, by + 7, bx + diameter - 8, by + diameter - 8),
                      outline=(172, 161, 143, 90), width=1)
            plus_color = (180, 172, 158, 255)
        d.text((bx + diameter / 2, by + diameter / 2 - 2), "+",
               font=font(FONT_LILITA, 54), fill=plus_color, anchor="mm",
               stroke_width=1, stroke_fill=(40, 22, 12, 190) if enabled else (31, 29, 26, 210))


def render() -> Path:
    background_path = ASSETS / "bg_inventar.jpg"
    image = Image.open(background_path).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    image = ImageEnhance.Color(image).enhance(0.58)
    image = ImageEnhance.Brightness(image).enhance(0.46)
    image = image.filter(ImageFilter.GaussianBlur(4)).convert("RGBA")
    image.alpha_composite(Image.new("RGBA", (W, H), (9, 7, 6, 112)))

    # Resource button remains visible above the open list, as in the v2 layout.
    draw_round_gradient(image, (172, 194, 472, 314), (55, 40, 29), (28, 20, 16), 20,
                        outline=(151, 100, 54, 245), outline_width=2)
    icon = fit_icon(ASSETS / "kiste.png", 64)
    image.alpha_composite(icon, (188, 222))
    d = ImageDraw.Draw(image, "RGBA")
    d.text((264, 236), "RESSOURCEN", font=font(FONT_BALOO, 27), fill=PALETTE["glut_text"],
           stroke_width=2, stroke_fill=(12, 8, 6, 230))
    d.polygon(((430, 260), (454, 260), (442, 245)), fill=PALETTE["glut_light"])

    add_panel(image)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(OUTPUT, optimize=True)
    return OUTPUT


if __name__ == "__main__":
    print(render())
