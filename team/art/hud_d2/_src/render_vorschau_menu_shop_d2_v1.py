#!/usr/bin/env python3
"""Render the D2 shop overview and explicit purchase confirmation preview."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont


HERE = Path(__file__).resolve().parent
HUD = HERE.parent
ROOT = HUD.parents[2]
ASSETS = ROOT / "team/art/ui-kit/menus_v3/_src/inventar_v4_assets"
REVEAL = ROOT / "team/art/ui-kit/menus_v3/_assets/reveal_v16"
CHROME = HUD / "vorschau_hud_d2_v7_3_lvl12.png"
OUT_MAIN = HUD / "vorschau_menu_shop_d2_v1.png"
OUT_BUY = HUD / "vorschau_menu_shop_d2_v1_kauf.png"

W, H = 1080, 1920
OUT_SIZE = (576, 1024)
FONT_BALOO = ASSETS / "Baloo2-Variable.ttf"
FONT_LILITA = ASSETS / "LilitaOne-Regular.ttf"

C_TEXT = (247, 234, 210, 255)
C_MUTED = (185, 169, 136, 255)
C_CHIP = (214, 199, 166, 255)
C_EMBER = (255, 138, 42, 255)
C_EMBER_HI = (255, 192, 106, 255)
C_LINE = (122, 102, 78, 255)
C_PANEL = (23, 19, 17, 255)
C_BROWN = (42, 18, 6, 255)


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


def text_width(draw: ImageDraw.ImageDraw, value: str, face: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), value, font=face)
    return box[2] - box[0]


def wrapped_lines(
    draw: ImageDraw.ImageDraw,
    value: str,
    face: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    lines: list[str] = []
    for paragraph in value.split("\n"):
        words = paragraph.split()
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if current and text_width(draw, candidate, face) > max_width:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    value: str,
    xy: tuple[int, int],
    face: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    max_width: int,
    line_gap: int = 7,
) -> int:
    x, y = xy
    lines = wrapped_lines(draw, value, face, max_width)
    line_height = face.size + line_gap
    for line in lines:
        draw.text((x, y), line, font=face, fill=fill)
        y += line_height
    return y


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


def draw_balance_chip(
    base: Image.Image,
    x: int,
    y: int,
    label: str,
    amount: str,
    icon_path: Path,
) -> None:
    rounded_gradient(base, (x, y, 486, 68), (30, 23, 19), (12, 10, 9), 20,
                     outline=(138, 106, 68, 170), outline_width=2)
    icon = fit_icon(icon_path, (44, 44))
    base.alpha_composite(icon, (x + 16, y + 12))
    d = ImageDraw.Draw(base, "RGBA")
    d.text((x + 73, y + 10), label, font=font(FONT_BALOO, 18, 800),
           fill=(185, 169, 136, 255))
    d.text((x + 73, y + 31), amount, font=font(FONT_LILITA, 30),
           fill=(255, 224, 176, 255))


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


OFFERS = [
    {
        "name": "Siedler-Starthilfe",
        "limit": "1× PRO KONTO",
        "line1": "300 Zeitkristalle",
        "line2": "+ Bako-Skin · Ressourcenkiste",
        "price": "1,99 €",
        "art": "starter",
    },
    {
        "name": "Häuptlingspaket",
        "limit": "1× PRO KONTO",
        "line1": "750 Zeitkristalle",
        "line2": "+ Rahmen · 20 Wahl-Fragmente",
        "price": "4,99 €",
        "art": "crystal",
    },
    {
        "name": "Epochen-Fonds",
        "limit": "1× PRO EPOCHE",
        "line1": "2.400 Zeitkristalle",
        "line2": "Feuer 4 / 6 / 8 / 10 + Aufstieg",
        "price": "9,99 €",
        "art": "fund",
    },
]


def draw_offer_card(
    base: Image.Image,
    y: int,
    offer: dict[str, str],
    selected: bool = False,
) -> None:
    x, width, height = 36, 1008, 286
    border = (201, 138, 74, 230) if selected else (137, 108, 77, 180)
    rounded_gradient(base, (x, y, width, height), (48, 37, 29), (16, 13, 12), 24,
                     outline=border, outline_width=2)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x + 13, y + 15, x + width - 13, y + 18), 2,
                        fill=(255, 177, 90, 145 if selected else 75))

    rounded_gradient(base, (x + 16, y + 30, 218, 220), (37, 27, 21), (12, 10, 9), 20,
                     outline=(132, 98, 64, 170), outline_width=2)
    if offer["art"] == "starter":
        chest = fit_icon(ASSETS / "kiste.png", (142, 142))
        crystal = fit_icon(ASSETS / "kristall.png", (54, 54))
        base.alpha_composite(chest, (x + 52, y + 64))
        base.alpha_composite(crystal, (x + 156, y + 144))
    elif offer["art"] == "fund":
        crystal = fit_icon(ASSETS / "kristall.png", (146, 146))
        clock = fit_icon(ASSETS / "uhr.png", (54, 54))
        base.alpha_composite(crystal, (x + 52, y + 63))
        base.alpha_composite(clock, (x + 155, y + 145))
    else:
        crystal = fit_icon(ASSETS / "kristall.png", (150, 150))
        base.alpha_composite(crystal, (x + 50, y + 62))

    text_x = x + 260
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((text_x, y + 20, text_x + 180, y + 51), 14,
                        fill=(19, 14, 11, 220), outline=(147, 112, 72, 155), width=1)
    d.text((text_x + 90, y + 35), offer["limit"], font=font(FONT_BALOO, 17, 800),
           fill=(208, 187, 151, 255), anchor="mm")
    d.text((text_x, y + 66), offer["name"], font=font(FONT_LILITA, 33),
           fill=(255, 240, 213, 255), stroke_width=1,
           stroke_fill=(10, 8, 7, 180))
    d.text((text_x, y + 120), offer["line1"], font=font(FONT_BALOO, 23, 800),
           fill=(221, 207, 178, 255))
    d.text((text_x, y + 154), offer["line2"], font=font(FONT_BALOO, 22, 700),
           fill=(185, 169, 136, 255))
    d.text((text_x, y + 207), "FESTER INHALT", font=font(FONT_BALOO, 17, 800),
           fill=(255, 177, 90, 255), stroke_width=1,
           stroke_fill=(10, 8, 7, 150))

    price_x = x + width - 265
    rounded_gradient(base, (price_x, y + 216, 102, 48), (65, 47, 28), (29, 20, 13), 15,
                     outline=(170, 132, 76, 165), outline_width=1)
    ImageDraw.Draw(base, "RGBA").text(
        (price_x + 51, y + 240), offer["price"], font=font(FONT_LILITA, 25),
        fill=(255, 218, 160, 255), anchor="mm",
    )
    draw_button(base, (x + width - 151, y + 212, 130, 58), "DETAILS",
                font(FONT_LILITA, 21))


def draw_shop_panel(base: Image.Image) -> None:
    px, py, pw, ph = 14, 304, 1052, 1348
    rounded_gradient(base, (px, py, pw, ph), (31, 23, 19), (12, 10, 9), 30,
                     outline=(201, 138, 74, 230), outline_width=3)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((px + 8, py + 8, px + pw - 9, py + ph - 9), 23,
                        outline=(239, 186, 124, 54), width=1)

    icon = fit_icon(ASSETS / "kiste.png", (62, 62))
    base.alpha_composite(icon, (px + 30, py + 14))
    d = ImageDraw.Draw(base, "RGBA")
    d.text((px + 111, py + 10), "SHOP", font=font(FONT_LILITA, 54),
           fill=(255, 226, 181, 255), stroke_width=1,
           stroke_fill=(40, 21, 12, 180))
    d.text((px + 114, py + 63), "Angebote · Zeitkristalle", font=font(FONT_BALOO, 22, 800),
           fill=(198, 179, 146, 255))
    draw_close_button(base, px + pw - 82, py + 17, 62)

    draw_balance_chip(base, px + 26, py + 112, "VERDIENT", "1.250", ASSETS / "kristall.png")
    draw_balance_chip(base, px + 540, py + 112, "GEKAUFT", "0", ASSETS / "kristall.png")
    draw_tabs(base, py + 197, active=0)

    for index, offer in enumerate(OFFERS):
        draw_offer_card(base, py + 287 + index * 302, offer, selected=index == 0)

    d = ImageDraw.Draw(base, "RGBA")
    d.text((W // 2, py + 1211), "Preise in Euro · Inhalt wird vor dem Kauf angezeigt",
           font=font(FONT_BALOO, 19, 700), fill=(152, 134, 108, 255), anchor="mm")


def draw_modal_overlay(base: Image.Image) -> None:
    overlay = Image.new("RGBA", base.size, (5, 5, 7, 120))
    base.alpha_composite(overlay)


def draw_purchase_modal(base: Image.Image) -> None:
    x, y, width, height = 94, 382, 892, 1190
    rounded_gradient(base, (x, y, width, height), (34, 25, 20), (12, 10, 9), 30,
                     outline=(221, 154, 82, 250), outline_width=3)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x + 8, y + 8, x + width - 9, y + height - 9), 23,
                        outline=(255, 220, 167, 54), width=1)

    d.text((W // 2, y + 35), "KAUF BESTÄTIGEN", font=font(FONT_LILITA, 43),
           fill=(255, 226, 181, 255), anchor="mt",
           stroke_width=1, stroke_fill=(40, 21, 12, 180))
    d.text((W // 2, y + 88), "Siedler-Starthilfe · feste Inhalte",
           font=font(FONT_BALOO, 22, 800), fill=(198, 179, 146, 255), anchor="mt")
    draw_close_button(base, x + width - 78, y + 22, 58)

    rounded_gradient(base, (x + 28, y + 143, width - 56, 206),
                     (48, 37, 29), (16, 13, 12), 22,
                     outline=(150, 113, 75, 180), outline_width=2)
    chest = fit_icon(ASSETS / "kiste.png", (132, 132))
    crystal = fit_icon(ASSETS / "kristall.png", (48, 48))
    base.alpha_composite(chest, (x + 47, y + 179))
    base.alpha_composite(crystal, (x + 151, y + 256))
    d = ImageDraw.Draw(base, "RGBA")
    d.text((x + 220, y + 169), "Siedler-Starthilfe", font=font(FONT_LILITA, 34),
           fill=(255, 240, 213, 255))
    d.text((x + 220, y + 224), "300 Zeitkristalle", font=font(FONT_BALOO, 24, 800),
           fill=(221, 207, 178, 255))
    d.text((x + 220, y + 260), "+ Bako-Skin · Ressourcenkiste",
           font=font(FONT_BALOO, 22, 700), fill=(185, 169, 136, 255))
    d.text((x + 220, y + 300), "Einmalig · 1× pro Konto",
           font=font(FONT_BALOO, 19, 800), fill=(255, 177, 90, 255))

    rounded_gradient(base, (x + 28, y + 365, width - 56, 94),
                     (25, 19, 16), (12, 10, 9), 17,
                     outline=(138, 106, 68, 160), outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.text((x + 52, y + 391), "PREIS", font=font(FONT_BALOO, 20, 800),
           fill=(185, 169, 136, 255))
    d.text((x + width - 51, y + 374), "1,99 €", font=font(FONT_LILITA, 46),
           fill=(255, 218, 160, 255), anchor="ra")
    d.text((x + 52, y + 419), "Google Play · Direktkauf",
           font=font(FONT_BALOO, 18, 700), fill=(147, 131, 106, 255))

    rounded_gradient(base, (x + 28, y + 476, width - 56, 292),
                     (23, 19, 17), (15, 12, 11), 18,
                     outline=(117, 91, 64, 165), outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.text((x + 49, y + 493), "KAUFHINWEIS", font=font(FONT_BALOO, 18, 800),
           fill=(255, 177, 90, 255), stroke_width=1,
           stroke_fill=(10, 8, 7, 150))
    legal = (
        "Der gekaufte Inhalt wird direkt nach dem Kauf gutgeschrieben. Verkäufer ist Google "
        "Commerce Limited; du kaufst über Google Play. Mit der sofortigen Gutschrift verlierst "
        "du dein Widerrufsrecht, wenn du dem vorher ausdrücklich zugestimmt und bestätigt hast, "
        "dass du das weißt. Eine Bestätigung erhältst du von Google Play per E-Mail."
    )
    d = ImageDraw.Draw(base, "RGBA")
    draw_wrapped(d, legal, (x + 49, y + 528), font(FONT_BALOO, 22, 600),
                 (205, 194, 172, 255), width - 98, line_gap=5)

    rounded_gradient(base, (x + 28, y + 786, width - 56, 205),
                     (31, 25, 21), (14, 12, 11), 18,
                     outline=(137, 108, 77, 185), outline_width=1)
    # Checked state represents the explicit, user-initiated consent before checkout.
    bx, by = x + 49, y + 813
    rounded_gradient(base, (bx, by, 42, 42), (255, 171, 76), (205, 80, 22), 9,
                     outline=(255, 220, 170, 215), outline_width=2)
    d = ImageDraw.Draw(base, "RGBA")
    d.line((bx + 10, by + 22, bx + 17, by + 29, bx + 32, by + 12),
           fill=(255, 250, 236, 255), width=5, joint="curve")
    consent = (
        "Ich möchte, dass der gekaufte Inhalt sofort bereitgestellt wird, und stimme dem "
        "ausdrücklich zu. Mir ist bekannt, dass ich dadurch mein Widerrufsrecht verliere."
    )
    draw_wrapped(ImageDraw.Draw(base, "RGBA"), consent, (x + 108, y + 807),
                 font(FONT_BALOO, 23, 700), (232, 221, 199, 255),
                 width - 164, line_gap=6)
    d = ImageDraw.Draw(base, "RGBA")
    d.text((x + 108, y + 943), "Zustimmung für diesen Kauf", font=font(FONT_BALOO, 18, 700),
           fill=(147, 131, 106, 255))

    draw_button(base, (x + 28, y + 1023, 530, 78), "ZU GOOGLE PLAY · 1,99 €",
                font(FONT_LILITA, 27))
    rounded_gradient(base, (x + 576, y + 1023, 260, 78),
                     (38, 30, 25), (17, 14, 12), 18,
                     outline=(139, 108, 77, 170), outline_width=2)
    ImageDraw.Draw(base, "RGBA").text(
        (x + 706, y + 1062), "ABBRECHEN", font=font(FONT_LILITA, 21),
        fill=(210, 192, 160, 255), anchor="mm",
    )


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
    draw_shop_panel(image)
    save_preview(image, OUT_MAIN)

    purchase = image.copy()
    draw_modal_overlay(purchase)
    draw_purchase_modal(purchase)
    save_preview(purchase, OUT_BUY)
    return OUT_MAIN, OUT_BUY


if __name__ == "__main__":
    for path in render():
        print(path)
