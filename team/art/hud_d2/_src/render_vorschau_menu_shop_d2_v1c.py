#!/usr/bin/env python3
"""Render the D2 shop v1c preview and matching purchase confirmation."""
from __future__ import annotations

from pathlib import Path
import render_vorschau_menu_shop_d2_v1 as purchase_dialog

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
HUD = HERE.parent
ROOT = HUD.parents[2]
ASSETS = ROOT / "team/art/ui-kit/menus_v3/_src/inventar_v4_assets"
REVEAL = ROOT / "team/art/ui-kit/menus_v3/_assets/reveal_v16"
CHROME = HUD / "vorschau_hud_d2_v7_3_lvl12.png"
OUT_MAIN = HUD / "vorschau_menu_shop_d2_v1c.png"
OUT_BUY = HUD / "vorschau_menu_shop_d2_v1c_kauf.png"

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
        "price": "1,99 €",
        "art": "starter",
        "accent": (255, 138, 42, 255),
    },
    {
        "name": "Häuptlingspaket",
        "line1": "750 Zeitkristalle",
        "line2": "+ Profilrahmen · 20 Wahl-Fragmente",
        "price": "4,99 €",
        "art": "starter",
        "accent": (255, 177, 90, 255),
    },
    {
        "name": "Epochen-Fonds",
        "line1": "2.400 Zeitkristalle",
        "line2": "Feuer 4 / 6 / 8 / 10 + Aufstieg",
        "price": "9,99 €",
        "art": "fund",
        "accent": (192, 143, 88, 255),
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
    x, width, height = 36, 1008, 466
    # Full-width highlight with a large, full-height image stage.
    add_glow(base, (x - 12, y + 8, width + 24, height + 14),
             (255, 100, 25, 255), blur=48, opacity=112)
    rounded_gradient(base, (x, y, width, height), (102, 51, 25), (25, 14, 11), 30,
                     outline=(255, 179, 92, 255), outline_width=5)
    rounded_gradient(base, (x + 8, y + 8, width - 16, height - 16),
                     (50, 31, 22), (15, 11, 10), 24,
                     outline=(255, 220, 166, 115), outline_width=2)

    stage_x, stage_y = x + 18, y + 18
    stage_w, stage_h = 418, height - 36
    stage = Image.new("RGBA", (stage_w, stage_h), (0, 0, 0, 0))
    rounded_gradient(stage, (0, 0, stage_w, stage_h), (91, 48, 26), (24, 15, 12), 23,
                     outline=(244, 166, 86, 195), outline_width=2)
    add_glow(stage, (86, 72, 246, 244), (255, 99, 23, 255), blur=56, opacity=160)
    crystal = fit_icon(ASSETS / "kristall.png", (282, 282))
    small_crystal = fit_icon(ASSETS / "kristall.png", (102, 102))
    rotated_crystal = small_crystal.rotate(18, resample=Image.Resampling.BICUBIC, expand=False)
    stage.alpha_composite(crystal, (68, 42))
    stage.alpha_composite(small_crystal, (27, 280))
    stage.alpha_composite(rotated_crystal, (288, 280))
    # Keep all pixels, including glow and the two small crystals, inside the
    # rounded picture window with a visible inner margin.
    mask = Image.new("L", stage.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, stage_w - 1, stage_h - 1), radius=23, fill=255
    )
    stage.putalpha(mask)
    base.alpha_composite(stage, (stage_x, stage_y))
    ImageDraw.Draw(base, "RGBA").rounded_rectangle(
        (stage_x, stage_y, stage_x + stage_w - 1, stage_y + stage_h - 1),
        23, outline=(255, 197, 122, 255), width=2,
    )

    text_x = x + 466
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((text_x, y + 35, text_x + 218, y + 74), 18,
                        fill=(79, 35, 17, 250),
                        outline=(255, 186, 103, 245), width=2)
    d.text((text_x + 109, y + 54), "ZEITKRISTALLE",
           font=font(FONT_BALOO, 21, 800), fill=(255, 228, 186, 255), anchor="mm")
    title = "Beutel Zeitkristalle"
    title_face = font(FONT_LILITA, 54)
    title_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(title_layer).text((text_x, y + 105), title, font=title_face,
                                    fill=(255, 137, 46, 180), stroke_width=2,
                                    stroke_fill=(255, 113, 35, 140))
    title_glow = title_layer.filter(ImageFilter.GaussianBlur(13))
    base.alpha_composite(title_glow)
    d = ImageDraw.Draw(base, "RGBA")
    d.text((text_x, y + 105), title, font=title_face,
           fill=(255, 242, 220, 255), stroke_width=2,
           stroke_fill=(31, 14, 8, 225))
    d.text((text_x + 2, y + 181), "450 Zeitkristalle",
           font=font(FONT_BALOO, 31, 800), fill=(255, 223, 177, 255))
    d.text((text_x + 2, y + 230), "Für Items, Boosts & Event-Teilnahme",
           font=font(FONT_BALOO, 23, 700), fill=(218, 199, 168, 255))
    d.line((text_x + 2, y + 284, x + width - 34, y + 284),
           fill=(255, 173, 88, 110), width=2)
    d.text((text_x + 2, y + 305), "FESTER INHALT",
           font=font(FONT_BALOO, 20, 800), fill=(255, 181, 99, 255))
    draw_price_button(base, (x + width - 268, y + height - 105, 234, 70),
                      "4,99 €", large=True)


def draw_compact_offer(base: Image.Image, layer: Image.Image, y: int,
                       offer: dict[str, object]) -> None:
    """Draw a compact row with its complete artwork inside a rounded frame."""
    x, width, height = 36, 1008, 176
    accent = offer["accent"]
    rounded_gradient(layer, (x, y, width, height), (48, 36, 27), (14, 12, 11), 22,
                     outline=(153, 117, 76, 210), outline_width=2)
    d = ImageDraw.Draw(layer, "RGBA")
    d.rounded_rectangle((x + 8, y + 14, x + 14, y + height - 14), 3,
                        fill=accent)
    art_x, art_y, art_w, art_h = x + 17, y + 15, 146, height - 30
    rounded_gradient(layer, (art_x, art_y, art_w, art_h), (50, 34, 24), (13, 10, 9), 17,
                     outline=(163, 122, 77, 195), outline_width=2)
    art = Image.new("RGBA", (art_w, art_h), (0, 0, 0, 0))
    add_glow(art, (25, 22, 96, 98), accent, 21, 85)
    if offer["art"] == "fund":
        crystal = fit_icon(ASSETS / "kristall.png", (96, 96))
        clock = fit_icon(ASSETS / "uhr.png", (36, 36))
        art.alpha_composite(crystal, (21, 16))
        art.alpha_composite(clock, (91, 93))
    elif offer["name"] == "Siedler-Starthilfe":
        bako = fit_icon(ROOT / "team/art/heroes/hero_bako_portrait_alpha.png", (105, 120))
        chest = fit_icon(ASSETS / "kiste.png", (44, 44))
        crystal = fit_icon(ASSETS / "kristall.png", (34, 34))
        art.alpha_composite(bako, (12, 5))
        art.alpha_composite(chest, (84, 91))
        art.alpha_composite(crystal, (102, 78))
    else:
        chest = fit_icon(ASSETS / "kiste.png", (96, 96))
        crystal = fit_icon(ASSETS / "kristall.png", (39, 39))
        art.alpha_composite(chest, (18, 20))
        art.alpha_composite(crystal, (91, 89))
    art_mask = Image.new("L", art.size, 0)
    ImageDraw.Draw(art_mask).rounded_rectangle(
        (0, 0, art_w - 1, art_h - 1), radius=17, fill=255
    )
    art.putalpha(ImageChops.multiply(art.getchannel("A"), art_mask))
    layer.alpha_composite(art, (art_x, art_y))
    ImageDraw.Draw(layer, "RGBA").rounded_rectangle(
        (art_x, art_y, art_x + art_w - 1, art_y + art_h - 1),
        17, outline=(198, 151, 98, 235), width=2,
    )

    text_x = x + 184
    d = ImageDraw.Draw(layer, "RGBA")
    d.text((text_x, y + 19), str(offer["name"]), font=font(FONT_LILITA, 34),
           fill=(255, 240, 213, 255), stroke_width=1,
           stroke_fill=(10, 8, 7, 180))
    d.text((text_x + 1, y + 68), str(offer["line1"]),
           font=font(FONT_BALOO, 24, 800), fill=(230, 213, 183, 255))
    d.text((text_x + 1, y + 105), str(offer["line2"]),
           font=font(FONT_BALOO, 21, 700), fill=(179, 161, 134, 255))
    draw_price_button(layer, (x + width - 193, y + 57, 166, 58),
                      str(offer["price"]))


def draw_shop_panel_v1c(base: Image.Image) -> None:
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
    d.text((px + 29, py + 674), "WEITERE ANGEBOTE", font=font(FONT_LILITA, 26),
           fill=(255, 220, 173, 255))
    d.line((px + 270, py + 692, px + pw - 32, py + 692),
           fill=(165, 121, 76, 135), width=2)

    # Three compact rows fit above the frame bottom without cropping.
    list_top = py + 716
    list_bottom = py + ph - 15
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    for index, offer in enumerate(LIST_OFFERS):
        draw_compact_offer(base, layer, list_top + index * 188, offer)
    visible = layer.crop((px + 12, list_top, px + pw - 12, list_bottom))
    base.alpha_composite(visible, (px + 12, list_top))

    # Reassert the frame above all cards and glows.
    d.rounded_rectangle((px, py, px + pw - 1, py + ph - 1), 30,
                        outline=(201, 138, 74, 245), width=3)
    d.rounded_rectangle((px + 8, py + 8, px + pw - 9, py + ph - 9), 23,
                        outline=(239, 186, 124, 54), width=1)


def save_preview(base: Image.Image, path: Path) -> None:
    final = base.convert("RGB").resize(OUT_SIZE, Image.Resampling.LANCZOS)
    final.save(path, optimize=True)


def render() -> tuple[Path, Path]:
    image = Image.open(CHROME).convert("RGBA")
    if image.size != (W, H):
        raise SystemExit(f"HUD-Chrome: erwartet {W}×{H}, erhalten {image.width}×{image.height}")

    draw_dock_background(image)
    add_full_screen_scrim(image)
    draw_dock_tabs(image)
    draw_shop_panel_v1c(image)
    save_preview(image, OUT_MAIN)

    purchase = image.copy()
    purchase_dialog.draw_modal_overlay(purchase)
    purchase_dialog.draw_purchase_modal(purchase, price="1,99 €")
    save_preview(purchase, OUT_BUY)
    return OUT_MAIN, OUT_BUY


if __name__ == "__main__":
    for path in render():
        print(path)
