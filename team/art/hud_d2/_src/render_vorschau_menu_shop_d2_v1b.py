#!/usr/bin/env python3
"""Render the D2 shop v1b preview. The v1 purchase dialog is intentionally untouched."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
HUD = HERE.parent
ROOT = HUD.parents[2]
ASSETS = ROOT / "team/art/ui-kit/menus_v3/_src/inventar_v4_assets"
REVEAL = ROOT / "team/art/ui-kit/menus_v3/_assets/reveal_v16"
CHROME = HUD / "vorschau_hud_d2_v7_3_lvl12.png"
OUT_MAIN = HUD / "vorschau_menu_shop_d2_v1b.png"

W, H = 1080, 1920
OUT_SIZE = (576, 1024)
FONT_BALOO = ASSETS / "Baloo2-Variable.ttf"
FONT_LILITA = ASSETS / "LilitaOne-Regular.ttf"

def font(path: Path, size: int, weight: int = 800) -> ImageFont.FreeTypeFont:
    result = ImageFont.truetype(str(path), size)
    if path == FONT_BALOO:
        try:
            result.set_variation_by_axes([weight])
        except (AttributeError, OSError):
            pass
    return result


def rounded_gradient(
    base: Image.Image,
    box: tuple[int, int, int, int],
    top: tuple[int, int, int],
    bottom: tuple[int, int, int],
    radius: int,
    outline: tuple[int, int, int, int] | None = None,
    outline_width: int = 1,
) -> None:
    x, y, width, height = box
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = layer.load()
    for yy in range(height):
        t = yy / max(height - 1, 1)
        color = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        for xx in range(width):
            pixels[xx, yy] = (*color, 255)
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, width - 1, height - 1), radius, fill=255
    )
    layer.putalpha(mask)
    base.alpha_composite(layer, (x, y))
    if outline:
        ImageDraw.Draw(base, "RGBA").rounded_rectangle(
            (x, y, x + width - 1, y + height - 1), radius,
            outline=outline, width=outline_width,
        )


def fit_icon(path: Path, size: tuple[int, int]) -> Image.Image:
    icon = Image.open(path).convert("RGBA")
    icon.thumbnail(size, Image.Resampling.LANCZOS)
    output = Image.new("RGBA", size, (0, 0, 0, 0))
    output.alpha_composite(
        icon, ((size[0] - icon.width) // 2, (size[1] - icon.height) // 2)
    )
    return output


def draw_button(
    base: Image.Image,
    box: tuple[int, int, int, int],
    label: str,
    face: ImageFont.FreeTypeFont,
    disabled: bool = False,
) -> None:
    x, y, width, height = box
    d = ImageDraw.Draw(base, "RGBA")
    if disabled:
        d.rounded_rectangle((x, y + 7, x + width, y + height + 7), 20,
                            fill=(31, 32, 31, 255))
        rounded_gradient(base, box, (88, 88, 82), (49, 51, 49), 18,
                         outline=(139, 133, 117, 180), outline_width=2)
        ink = (183, 180, 165, 255)
        d = ImageDraw.Draw(base, "RGBA")
    else:
        d.rounded_rectangle((x, y + 8, x + width, y + height + 8), 20,
                            fill=(91, 39, 19, 255))
        rounded_gradient(base, box, (255, 192, 106), (216, 78, 14), 18,
                         outline=(255, 218, 164, 220), outline_width=2)
        ink = (255, 248, 232, 255)
        d = ImageDraw.Draw(base, "RGBA")
        d.line((x + 18, y + 5, x + width - 18, y + 5),
               fill=(255, 246, 224, 125), width=2)
    d.text((x + width // 2, y + height // 2), label, font=face,
           fill=ink, anchor="mm", stroke_width=1,
           stroke_fill=(79, 31, 13, 150) if not disabled else (34, 34, 31, 120))


def draw_dock_background(base: Image.Image) -> None:
    """Replace the village-selected dock background with the inactive D2 dock."""
    dock_y = 1708
    opaque_cover = Image.new("RGBA", (W, H - 1668), (16, 11, 9, 255))
    base.alpha_composite(opaque_cover, (0, 1668))
    dock_bg = Image.open(ASSETS / "dock_bg.png").convert("RGBA")
    if dock_bg.size != (W, 212):
        dock_bg = dock_bg.resize((W, 212), Image.Resampling.LANCZOS)
    base.alpha_composite(dock_bg, (0, dock_y))
    d = ImageDraw.Draw(base, "RGBA")
    d.line((0, dock_y, W, dock_y), fill=(255, 255, 255, 58), width=2)


def draw_dock_tabs(base: Image.Image) -> None:
    """Lay out the six dim inactive icons after the full-screen background scrim."""
    dock_y = 1708
    items = [
        ("Dorf", ASSETS / "dock_dorf_inaktiv.png"),
        ("Helden", REVEAL / "d2_ico_dock_helden_inaktiv.png"),
        ("Karte", REVEAL / "d2_ico_dock_karte_inaktiv.png"),
        ("Armee", REVEAL / "d2_ico_dock_armee_inaktiv.png"),
        ("Gilde", REVEAL / "d2_ico_dock_gilde_inaktiv.png"),
        ("Inventar", REVEAL / "d2_ico_dock_inventar_inaktiv.png"),
    ]
    label_face = font(FONT_LILITA, 30)
    for index, (label, icon_path) in enumerate(items):
        center_x = index * 180 + 90
        icon = fit_icon(icon_path, (96, 88))
        icon = ImageEnhance.Brightness(icon).enhance(0.82)
        base.alpha_composite(icon, (center_x - 48, dock_y + 14))
        d = ImageDraw.Draw(base, "RGBA")
        d.text((center_x, dock_y + 136), label, font=label_face,
               fill=(153, 137, 109, 255), anchor="mt",
               stroke_width=1, stroke_fill=(9, 7, 6, 210))


def add_full_screen_scrim(base: Image.Image) -> None:
    scrim = Image.new("RGBA", base.size, (4, 7, 10, 255))
    alpha = Image.new("L", base.size, 0)
    pixels = alpha.load()
    fade_y = 1300
    for y in range(H):
        if y <= fade_y:
            opacity = 168
        else:
            progress = (y - fade_y) / (H - fade_y)
            opacity = round(168 + (105 - 168) * progress)
        for x in range(W):
            pixels[x, y] = opacity
    scrim.putalpha(alpha)
    base.alpha_composite(scrim)


def draw_close_button(base: Image.Image, x: int, y: int, size: int = 62) -> None:
    rounded_gradient(base, (x, y, size, size), (58, 43, 33), (22, 17, 15), 19,
                     outline=(208, 164, 112, 165), outline_width=2)
    ImageDraw.Draw(base, "RGBA").text(
        (x + size // 2, y + size // 2 - 2), "×", font=font(FONT_LILITA, 38),
        fill=(245, 223, 189, 255), anchor="mm",
    )


def draw_tabs(base: Image.Image, y: int, active: int = 0) -> None:
    labels = ("ANGEBOTE", "ZEITKRISTALLE", "GLUTUHREN", "PÄSSE")
    x0, gap, width, height = 38, 8, 245, 76
    for index, label in enumerate(labels):
        x = x0 + index * (width + gap)
        if index == active:
            rounded_gradient(base, (x, y, width, height), (112, 55, 27), (43, 25, 17), 18,
                             outline=(255, 194, 118, 220), outline_width=2)
            fill = (255, 240, 213, 255)
        else:
            rounded_gradient(base, (x, y, width, height), (33, 26, 22), (14, 12, 11), 18,
                             outline=(207, 163, 110, 115), outline_width=2)
            fill = (211, 195, 167, 255)
        ImageDraw.Draw(base, "RGBA").text(
            (x + width // 2, y + height // 2), label,
            font=font(FONT_LILITA, 23), fill=fill, anchor="mm",
        )


LIST_OFFERS = [
    {
        "name": "Siedler-Starthilfe",
        "line1": "300 Zeitkristalle",
        "line2": "+ Bako-Skin · Ressourcenkiste",
        "price": "0,99 €",
        "art": "starter",
        "accent": (255, 138, 42, 255),
    },
    {
        "name": "Starter-Server",
        "line1": "Einmaliges Starterangebot",
        "line2": "Feste Inhalte · ohne Ablaufzeit",
        "price": "2,99 €",
        "art": "starter",
        "accent": (205, 149, 92, 255),
    },
]


def add_glow(base: Image.Image, box: tuple[int, int, int, int],
             color: tuple[int, int, int, int], blur: int = 24,
             opacity: int = 90) -> None:
    """Add a contained warm product glow without a halo behind character art."""
    x, y, width, height = box
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    glow = ImageDraw.Draw(layer, "RGBA")
    glow.ellipse((x, y, x + width, y + height),
                 fill=(*color[:3], opacity))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(layer)


def draw_price_button(base: Image.Image, box: tuple[int, int, int, int],
                      price: str, large: bool = False) -> None:
    x, y, width, height = box
    draw_button(base, box, price,
                font(FONT_LILITA, 32 if large else 27))


def draw_featured_offer(base: Image.Image, y: int) -> None:
    x, width, height = 36, 1008, 374
    # Deep warm surface with a layered ember frame and clipped inner bevel.
    add_glow(base, (x - 12, y + 8, width + 24, height + 14),
             (255, 113, 38, 255), blur=38, opacity=75)
    rounded_gradient(base, (x, y, width, height), (77, 42, 24), (21, 14, 12), 28,
                     outline=(255, 171, 83, 255), outline_width=4)
    rounded_gradient(base, (x + 8, y + 8, width - 16, height - 16),
                     (48, 31, 23), (15, 12, 11), 23,
                     outline=(255, 220, 166, 92), outline_width=1)

    # Art stage: real crystal asset composed at three scales. The glow stays on
    # the product art and is a shop accent, not a rarity badge or timer.
    stage = (x + 19, y + 20, 338, 334)
    rounded_gradient(base, stage, (72, 43, 28), (23, 15, 12), 22,
                     outline=(207, 138, 74, 180), outline_width=2)
    add_glow(base, (x + 93, y + 79, 205, 192), (255, 117, 32, 255), 35, 70)
    crystal = fit_icon(ASSETS / "kristall.png", (232, 232))
    small_crystal = fit_icon(ASSETS / "kristall.png", (84, 84))
    rotated_crystal = small_crystal.rotate(18, resample=Image.Resampling.BICUBIC, expand=False)
    base.alpha_composite(crystal, (x + 72, y + 42))
    base.alpha_composite(small_crystal, (x + 43, y + 230))
    base.alpha_composite(rotated_crystal, (x + 249, y + 218))
    # Tiny brass flecks add a crafted, gacha-shop finish without text or badges.
    d = ImageDraw.Draw(base, "RGBA")
    for px, py, radius, alpha in ((x + 43, y + 48, 4, 175),
                                  (x + 311, y + 71, 3, 125),
                                  (x + 278, y + 132, 3, 115),
                                  (x + 42, y + 302, 3, 145)):
        d.ellipse((px - radius, py - radius, px + radius, py + radius),
                  fill=(255, 193, 112, alpha))

    text_x = x + 387
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((text_x, y + 24, text_x + 205, y + 58), 16,
                        fill=(73, 34, 18, 245),
                        outline=(255, 181, 94, 230), width=2)
    d.text((text_x + 102, y + 41), "ZEITKRISTALLE",
           font=font(FONT_BALOO, 19, 800), fill=(255, 220, 173, 255), anchor="mm")
    d.text((text_x, y + 75), "Zeitkristall-Paket", font=font(FONT_LILITA, 43),
           fill=(255, 240, 213, 255), stroke_width=1,
           stroke_fill=(10, 8, 7, 190))
    d.text((text_x + 2, y + 133), "450 Zeitkristalle", font=font(FONT_BALOO, 27, 800),
           fill=(255, 221, 177, 255))
    d.text((text_x + 2, y + 178), "Für Items, Boosts & Event-Teilnahme",
           font=font(FONT_BALOO, 22, 700), fill=(212, 194, 166, 255))
    d.text((text_x + 2, y + 226), "FESTER INHALT", font=font(FONT_BALOO, 17, 800),
           fill=(255, 177, 90, 255))
    draw_price_button(base, (x + width - 238, y + 296, 208, 60), "4,99 €", large=True)


def draw_compact_offer(base: Image.Image, layer: Image.Image, y: int,
                       offer: dict[str, object]) -> None:
    """Draw one broad offer row into the scroll layer."""
    x, width, height = 36, 1008, 370
    accent = offer["accent"]
    rounded_gradient(layer, (x, y, width, height), (46, 35, 28), (14, 12, 11), 23,
                     outline=(141, 111, 79, 200), outline_width=2)
    d = ImageDraw.Draw(layer, "RGBA")
    d.rounded_rectangle((x + 10, y + 14, x + 17, y + height - 14), 4,
                        fill=accent)
    art_box = (x + 25, y + 20, 226, height - 40)
    rounded_gradient(layer, art_box, (43, 30, 23), (12, 10, 9), 19,
                     outline=(156, 116, 75, 175), outline_width=2)
    add_glow(layer, (x + 57, y + 55, 152, 145), accent, 28, 48)
    if offer["art"] == "fund":
        crystal = fit_icon(ASSETS / "kristall.png", (158, 158))
        clock = fit_icon(ASSETS / "uhr.png", (62, 62))
        layer.alpha_composite(crystal, (x + 56, y + 94))
        layer.alpha_composite(clock, (x + 171, y + 213))
    elif offer["art"] == "starter":
        if offer["name"] == "Siedler-Starthilfe":
            bako = fit_icon(ROOT / "team/art/heroes/hero_bako_portrait_alpha.png", (210, 210))
            chest = fit_icon(ASSETS / "kiste.png", (74, 74))
            crystal = fit_icon(ASSETS / "kristall.png", (48, 48))
            layer.alpha_composite(bako, (x + 50, y + 82))
            layer.alpha_composite(chest, (x + 170, y + 258))
            layer.alpha_composite(crystal, (x + 188, y + 230))
        else:
            chest = fit_icon(ASSETS / "kiste.png", (166, 166))
            crystal = fit_icon(ASSETS / "kristall.png", (58, 58))
            layer.alpha_composite(chest, (x + 51, y + 104))
            layer.alpha_composite(crystal, (x + 164, y + 218))
    else:
        crystal = fit_icon(ASSETS / "kristall.png", (158, 158))
        layer.alpha_composite(crystal, (x + 56, y + 95))

    text_x = x + 280
    d = ImageDraw.Draw(layer, "RGBA")
    d.text((text_x, y + 53), str(offer["name"]), font=font(FONT_LILITA, 39),
           fill=(255, 240, 213, 255), stroke_width=1,
           stroke_fill=(10, 8, 7, 180))
    d.text((text_x + 1, y + 122), str(offer["line1"]),
           font=font(FONT_BALOO, 27, 800), fill=(230, 213, 183, 255))
    d.text((text_x + 1, y + 172), str(offer["line2"]),
           font=font(FONT_BALOO, 22, 700), fill=(179, 161, 134, 255))
    d.text((text_x + 1, y + 241), "FESTER INHALT", font=font(FONT_BALOO, 17, 800),
           fill=accent)
    draw_price_button(layer, (x + width - 238, y + height - 82, 208, 60),
                      str(offer["price"]))


def draw_shop_panel_v1b(base: Image.Image) -> None:
    px, py, pw, ph = 14, 304, 1052, 1348
    rounded_gradient(base, (px, py, pw, ph), (31, 23, 19), (12, 10, 9), 30,
                     outline=(201, 138, 74, 235), outline_width=3)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((px + 8, py + 8, px + pw - 9, py + ph - 9), 23,
                        outline=(239, 186, 124, 54), width=1)

    icon = fit_icon(ASSETS / "kiste.png", (66, 66))
    base.alpha_composite(icon, (px + 25, py + 13))
    d = ImageDraw.Draw(base, "RGBA")
    d.text((px + 104, py + 6), "SHOP", font=font(FONT_LILITA, 54),
           fill=(255, 226, 181, 255), stroke_width=1,
           stroke_fill=(40, 21, 12, 180))
    d.text((px + 107, py + 59), "Angebote · Zeitkristalle", font=font(FONT_BALOO, 22, 800),
           fill=(198, 179, 146, 255))
    draw_close_button(base, px + pw - 82, py + 15, 62)

    # The confusing earned/purchased split is gone. Tabs remain expandable and
    # retain the original D2 sizing and active ember treatment.
    draw_tabs(base, py + 97, active=0)
    draw_featured_offer(base, py + 190)

    d = ImageDraw.Draw(base, "RGBA")
    d.text((px + 29, py + 579), "WEITERE ANGEBOTE", font=font(FONT_LILITA, 26),
           fill=(255, 220, 173, 255))
    d.line((px + 270, py + 597, px + pw - 32, py + 597),
           fill=(165, 121, 76, 135), width=2)

    # A masked scroll viewport clips the fourth row exactly at the panel bottom.
    list_top = py + 615
    list_bottom = py + ph - 15
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    for index, offer in enumerate(LIST_OFFERS):
        draw_compact_offer(base, layer, list_top + index * 384, offer)
    visible = layer.crop((px + 12, list_top, px + pw - 12, list_bottom))
    base.alpha_composite(visible, (px + 12, list_top))

    # Scroll track and thumb are visible beside the cards.
    d = ImageDraw.Draw(base, "RGBA")
    track_x = px + pw - 15
    d.rounded_rectangle((track_x, list_top + 6, track_x + 5, list_bottom - 6),
                        2, fill=(104, 83, 64, 150))
    d.rounded_rectangle((track_x - 2, list_top + 36, track_x + 7, list_top + 318),
                        5, fill=(255, 174, 88, 230))

    # Reassert the frame over the intentionally clipped last row.
    d.rounded_rectangle((px, py, px + pw - 1, py + ph - 1), 30,
                        outline=(201, 138, 74, 245), width=3)
    d.rounded_rectangle((px + 8, py + 8, px + pw - 9, py + ph - 9), 23,
                        outline=(239, 186, 124, 54), width=1)


def save_preview(base: Image.Image, path: Path) -> None:
    final = base.convert("RGB").resize(OUT_SIZE, Image.Resampling.LANCZOS)
    final.save(path, optimize=True)


def render() -> Path:
    image = Image.open(CHROME).convert("RGBA")
    if image.size != (W, H):
        raise SystemExit(f"HUD-Chrome: erwartet {W}×{H}, erhalten {image.width}×{image.height}")

    draw_dock_background(image)
    add_full_screen_scrim(image)
    draw_dock_tabs(image)
    draw_shop_panel_v1b(image)
    save_preview(image, OUT_MAIN)
    return OUT_MAIN


if __name__ == "__main__":
    print(render())
