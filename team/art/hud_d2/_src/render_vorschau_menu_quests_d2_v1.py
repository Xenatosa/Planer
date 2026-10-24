#!/usr/bin/env python3
"""Render D2 quest overview and quest-detail previews at 576x1024."""
from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
HUD = HERE.parent
REPO = HUD.parents[2]
ART_SOURCE = Path("/workspace/handygame-plan/team/art")
ASSETS = REPO / "team/art/ui-kit/menus_v3/_src/inventar_v4_assets"
EXPORT = ART_SOURCE / "ui-kit/menus_v3/vorlage_D2_export"
ICONS = ART_SOURCE / "hud_d2/icons_v1"
FONT_BALOO = ASSETS / "Baloo2-Variable.ttf"
FONT_LILITA = ASSETS / "LilitaOne-Regular.ttf"
HERO_XP = ART_SOURCE / "ui-kit/menus_v3/_assets/ico_heldenxp.png"
OUT_MAIN = HUD / "vorschau_menu_quests_d2_v1.png"
OUT_DETAIL = HUD / "vorschau_menu_quests_d2_v1_detail.png"

W, H = 1080, 1920
OUT_SIZE = (576, 1024)
PANEL = (14, 304, 1052, 1348)
C_TEXT = (243, 231, 207, 255)
C_MUTED = (185, 169, 136, 255)
C_SOFT = (214, 199, 166, 255)
C_GLOW = (255, 138, 42, 255)
C_BRONZE = (201, 138, 74, 235)
C_INK = (11, 9, 8, 255)


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
    stripe = Image.new("RGBA", (1, height))
    pixels = stripe.load()
    for yy in range(height):
        t = yy / max(height - 1, 1)
        pixels[0, yy] = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3)) + (255,)
    layer = stripe.resize((width, height), Image.Resampling.BILINEAR)
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width - 1, height - 1), radius, fill=255)
    layer.putalpha(mask)
    base.alpha_composite(layer, (x, y))
    if outline:
        ImageDraw.Draw(base, "RGBA").rounded_rectangle(
            (x, y, x + width - 1, y + height - 1), radius,
            outline=outline, width=outline_width,
        )


def load_sprite(name: str) -> Image.Image:
    return Image.open(EXPORT / f"{name}.png").convert("RGBA")


def nine_slice(image: Image.Image, size: tuple[int, int], borders: tuple[int, int, int, int]) -> Image.Image:
    left, top, right, bottom = borders
    sw, sh = image.size
    dw, dh = size
    if dw < left + right or dh < top + bottom:
        raise ValueError(f"9-slice target too small: {size}, borders={borders}")
    sx = (0, left, sw - right, sw)
    sy = (0, top, sh - bottom, sh)
    dx = (0, left, dw - right, dw)
    dy = (0, top, dh - bottom, dh)
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    for row in range(3):
        for col in range(3):
            src_box = (sx[col], sy[row], sx[col + 1], sy[row + 1])
            dst_size = (dx[col + 1] - dx[col], dy[row + 1] - dy[row])
            if dst_size[0] <= 0 or dst_size[1] <= 0:
                continue
            piece = image.crop(src_box)
            if piece.size != dst_size:
                piece = piece.resize(dst_size, Image.Resampling.LANCZOS)
            out.alpha_composite(piece, (dx[col], dy[row]))
    return out


def paste_9(base: Image.Image, name: str, box: tuple[int, int, int, int], borders: tuple[int, int, int, int]) -> None:
    x, y, w, h = box
    base.alpha_composite(nine_slice(load_sprite(name), (w, h), borders), (x, y))


def fit_icon(path: Path, size: tuple[int, int]) -> Image.Image:
    icon = Image.open(path).convert("RGBA")
    icon.thumbnail(size, Image.Resampling.LANCZOS)
    output = Image.new("RGBA", size, (0, 0, 0, 0))
    output.alpha_composite(icon, ((size[0] - icon.width) // 2, (size[1] - icon.height) // 2))
    return output


def icon(name: str, size: tuple[int, int]) -> Image.Image:
    return fit_icon(ICONS / f"{name}.png", size)


def add_glow(base: Image.Image, box: tuple[int, int, int, int], color=(255, 106, 24, 180), blur=24) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    x, y, width, height = box
    ImageDraw.Draw(layer, "RGBA").rounded_rectangle(
        (x, y, x + width, y + height), radius=20, fill=color,
    )
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))


def clipped_row_glow(base: Image.Image, row_box: tuple[int, int, int, int], button_box: tuple[int, int, int, int]) -> None:
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    x, y, w, h = button_box
    ImageDraw.Draw(glow, "RGBA").rounded_rectangle(
        (x - 26, y - 14, x + w + 26, y + h + 14), radius=26,
        fill=(255, 100, 23, 150),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(32))
    mask = Image.new("L", base.size, 0)
    rx, ry, rw, rh = row_box
    ImageDraw.Draw(mask).rectangle((rx + 4, ry + 4, rx + rw - 5, ry + rh - 5), fill=255)
    glow.putalpha(Image.eval(glow.getchannel("A"), lambda a: a))
    from PIL import ImageChops
    glow.putalpha(ImageChops.multiply(glow.getchannel("A"), mask))
    base.alpha_composite(glow)


def draw_primary_button(base: Image.Image, box: tuple[int, int, int, int], label: str, size: int) -> None:
    x, y, w, h = box
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x, y + 8, x + w, y + h + 8), 20, fill=(91, 39, 19, 255))
    rounded_gradient(base, box, (255, 192, 106), (216, 78, 14), 18,
                     outline=(255, 218, 164, 230), outline_width=2)
    d = ImageDraw.Draw(base, "RGBA")
    d.line((x + 18, y + 5, x + w - 18, y + 5), fill=(255, 246, 224, 130), width=2)
    d.text((x + w // 2, y + h // 2 - 2), label, font=font(FONT_LILITA, size),
           fill=(255, 248, 232, 255), anchor="mm", stroke_width=1,
           stroke_fill=(79, 31, 13, 160))


def draw_secondary_button(base: Image.Image, box: tuple[int, int, int, int], label: str, size: int) -> None:
    x, y, w, h = box
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x, y + 7, x + w, y + h + 7), 20, fill=(10, 8, 7, 255))
    rounded_gradient(base, box, (61, 43, 31), (24, 17, 13), 18,
                     outline=(168, 129, 82, 190), outline_width=2)
    ImageDraw.Draw(base, "RGBA").text((x + w // 2, y + h // 2 - 1), label,
                                      font=font(FONT_LILITA, size), fill=C_TEXT,
                                      anchor="mm", stroke_width=1,
                                      stroke_fill=(7, 6, 5, 180))


def draw_base() -> Image.Image:
    # Reuse the exact D2 shop chrome treatment: matching top bar, scrim and inactive dock.
    src_dir = str(HERE)
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    import render_vorschau_menu_shop_d2_v1c as shop_chrome
    base = Image.open(shop_chrome.CHROME).convert("RGBA")
    if base.size != (W, H):
        raise SystemExit(f"HUD-Chrome erwartet {W}×{H}, erhalten {base.size}")
    shop_chrome.draw_dock_background(base)
    shop_chrome.add_full_screen_scrim(base)
    shop_chrome.draw_dock_tabs(base)
    return base


def draw_outer_panel(base: Image.Image) -> None:
    px, py, pw, ph = PANEL
    rounded_gradient(base, PANEL, (31, 23, 19), (12, 10, 9), 30,
                     outline=C_BRONZE, outline_width=3)
    ImageDraw.Draw(base, "RGBA").rounded_rectangle(
        (px + 8, py + 8, px + pw - 9, py + ph - 9), 23,
        outline=(239, 186, 124, 58), width=1,
    )


def draw_header_and_tabs(base: Image.Image) -> None:
    px, py, pw, _ = PANEL
    base.alpha_composite(icon("d2_ico_quest", (68, 68)), (px + 24, py + 13))
    d = ImageDraw.Draw(base, "RGBA")
    d.text((px + 104, py + 6), "AUFGABEN", font=font(FONT_LILITA, 54),
           fill=(255, 226, 181, 255), stroke_width=1,
           stroke_fill=(40, 21, 12, 180))
    d.text((px + 108, py + 59), "TÄGLICH · HEUTE",
           font=font(FONT_BALOO, 22, 800), fill=(198, 179, 146, 255))

    close = load_sprite("d2_btn_quadrat_normal").resize((72, 72), Image.Resampling.LANCZOS)
    base.alpha_composite(close, (px + pw - 90, py + 12))
    ImageDraw.Draw(base, "RGBA").text(
        (px + pw - 54, py + 48), "×", font=font(FONT_LILITA, 42),
        fill=(245, 223, 189, 255), anchor="mm",
    )

    labels = ("TUTORIAL", "HAUPT", "NEBEN", "TÄGLICH", "WOCHE", "ERFOLGE", "EVENT")
    active = 3
    x0, y, width, height, gap = px + 26, py + 98, 136, 78, 8
    for i, label in enumerate(labels):
        x = x0 + i * (width + gap)
        sprite = "d2_tab_aktiv" if i == active else "d2_tab_inaktiv"
        paste_9(base, sprite, (x, y, width, height), (8, 8, 8, 12 if i == active else 10))
        d = ImageDraw.Draw(base, "RGBA")
        d.text((x + width // 2, y + height // 2 - 2), label,
               font=font(FONT_LILITA, 22),
               fill=(255, 217, 168, 255) if i == active else (185, 169, 136, 255),
               anchor="mm", stroke_width=1, stroke_fill=(8, 6, 5, 155))
        if i == active:
            base.alpha_composite(icon("d2_ico_badge_punkt", (28, 28)), (x + width - 36, y + 3))


def draw_summary(base: Image.Image) -> None:
    px, py, pw, _ = PANEL
    # This is a factual pool summary from quest-system-v1; no daily chest or activity score is defined.
    rounded_gradient(base, (px + 30, py + 190, 610, 44), (35, 26, 21), (17, 13, 11), 18,
                     outline=(122, 90, 58, 145), outline_width=1)
    ImageDraw.Draw(base, "RGBA").text(
        (px + 48, py + 212), "5 AUS DEM POOL + ANMELDUNG",
        font=font(FONT_BALOO, 20, 800), fill=(214, 199, 166, 255), anchor="lm",
    )
    rounded_gradient(base, (px + pw - 350, py + 190, 320, 44), (78, 39, 20), (29, 17, 12), 18,
                     outline=(201, 138, 74, 165), outline_width=1)
    ImageDraw.Draw(base, "RGBA").text(
        (px + pw - 190, py + 212), "1 ABHOLBEREIT",
        font=font(FONT_LILITA, 21), fill=(255, 217, 168, 255), anchor="mm",
    )


REWARDS = {
    "crystal": ("d2_ico_zeitkristall", "Zeitkristalle"),
    "clock": ("d2_ico_uhr", "Glutuhren"),
    "food": ("d2_ico_nahrung", "Nahrung"),
    "wood": ("d2_ico_holz", "Holz"),
    "xp": (None, "Heldenerfahrung"),
    "shell": ("d2_ico_gold_muschel", "Muscheln"),
}


def draw_reward(base: Image.Image, x: int, y: int, kind: str, amount: str) -> int:
    sprite, label = REWARDS[kind]
    art = fit_icon(HERO_XP, (34, 34)) if sprite is None else icon(sprite, (34, 34))
    base.alpha_composite(art, (x, y))
    d = ImageDraw.Draw(base, "RGBA")
    d.text((x + 39, y + 17), amount, font=font(FONT_LILITA, 21),
           fill=(243, 231, 207, 255), anchor="lm")
    amount_w = d.textbbox((0, 0), amount, font=font(FONT_LILITA, 21))[2]
    label_x = x + 46 + amount_w
    d.text((label_x, y + 17), label, font=font(FONT_BALOO, 20, 800),
           fill=(185, 169, 136, 255), anchor="lm")
    label_w = d.textbbox((0, 0), label, font=font(FONT_BALOO, 20, 800))[2]
    return label_x + label_w - x + 16


QUESTS = [
    {"title": "Willkommen zurück", "desc": "Melde dich heute an.", "progress": (1, 1), "ready": True,
     "rewards": [("crystal", "20"), ("clock", "×2 · 15 Min")]},
    {"title": "Ernte einholen", "desc": "Sammle 3-mal Produktion ein.", "progress": (2, 3), "ready": False,
     "rewards": [("crystal", "8"), ("food", "100")]},
    {"title": "Fleißige Hände", "desc": "Verbessere 3 Gebäude.", "progress": (1, 3), "ready": False,
     "rewards": [("crystal", "8"), ("wood", "100")]},
    {"title": "Kriegerdrill", "desc": "Bilde 10 Einheiten aus.", "progress": (6, 10), "ready": False,
     "rewards": [("crystal", "8"), ("xp", "30")]},
    {"title": "Auf ins Feld", "desc": "Spiele 2 Kampagnenmissionen (Wiederholungen zählen).", "progress": (1, 2), "ready": False,
     "rewards": [("crystal", "8"), ("xp", "40")]},
    {"title": "Volle Bäuche", "desc": "Gib 500 Nahrung aus.", "progress": (320, 500), "ready": False,
     "rewards": [("crystal", "8"), ("shell", "30")]},
]


def draw_bar(base: Image.Image, x: int, y: int, width: int, height: int, progress: float) -> None:
    paste_9(base, "d2_bar_bg", (x, y, width, height), (15, 2, 15, 2))
    if progress > 0:
        fill_w = max(48, round(width * min(1.0, progress)))
        fill_w = min(width, fill_w)
        paste_9(base, "d2_bar_fill_glut", (x, y - 4, fill_w, height + 8), (27, 8, 27, 8))


def draw_quest_row(base: Image.Image, y: int, quest: dict[str, object]) -> None:
    x, width, height = 36, 1008, 156
    row_box = (x, y, width, height)
    ready = bool(quest["ready"])
    paste_9(base, "d2_listenkarte_neutral", row_box, (12, 8, 8, 8))
    if ready:
        # A contained warm edge makes the claimable row read as complete without lighting the whole panel.
        ImageDraw.Draw(base, "RGBA").rectangle(
            (x + 2, y + 2, x + width - 3, y + height - 3),
            outline=(255, 138, 42, 205), width=2,
        )
    quest_icon = "d2_ico_quest_fertig" if ready else "d2_ico_quest"
    base.alpha_composite(icon(quest_icon, (68, 68)), (x + 20, y + 43))

    text_x = x + 106
    d = ImageDraw.Draw(base, "RGBA")
    d.text((text_x, y + 10), str(quest["title"]), font=font(FONT_LILITA, 31),
           fill=(255, 240, 213, 255), stroke_width=1, stroke_fill=(10, 8, 7, 180))
    d.text((text_x, y + 48), str(quest["desc"]), font=font(FONT_BALOO, 21, 700),
           fill=(185, 169, 136, 255))

    current, total = quest["progress"]
    ratio = current / total
    bar_x, bar_y, bar_w, bar_h = text_x, y + 78, 565, 28
    draw_bar(base, bar_x, bar_y, bar_w, bar_h, ratio)
    ImageDraw.Draw(base, "RGBA").text((bar_x + bar_w + 14, bar_y + 13),
                                      f"{current} / {total}", font=font(FONT_LILITA, 21),
                                      fill=(255, 217, 168, 255) if ready else C_SOFT,
                                      anchor="lm")

    rx, ry = text_x, y + 116
    rx += draw_reward(base, rx, ry, quest["rewards"][0][0], quest["rewards"][0][1])
    draw_reward(base, rx + 4, ry, quest["rewards"][1][0], quest["rewards"][1][1])

    btn = (x + width - 204, y + 34, 180, 84)
    if ready:
        clipped_row_glow(base, row_box, btn)
        draw_primary_button(base, btn, "ABHOLEN", 28)
    else:
        draw_secondary_button(base, btn, "LOS", 29)


def draw_main(base: Image.Image) -> None:
    draw_outer_panel(base)
    draw_header_and_tabs(base)
    draw_summary(base)
    list_y = PANEL[1] + 255
    for index, quest in enumerate(QUESTS):
        draw_quest_row(base, list_y + index * 164, quest)
    # Restore a clean, continuous outside frame after card glows and content.
    px, py, pw, ph = PANEL
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((px, py, px + pw - 1, py + ph - 1), 30,
                        outline=(201, 138, 74, 245), width=3)
    d.rounded_rectangle((px + 8, py + 8, px + pw - 9, py + ph - 9), 23,
                        outline=(239, 186, 124, 58), width=1)


def draw_detail(base: Image.Image) -> None:
    draw_outer_panel(base)
    draw_header_and_tabs(base)
    px, py, pw, _ = PANEL

    # Selected quest identity and its exact GDD objective.
    paste_9(base, "d2_panel_frame_muted", (36, py + 202, 1008, 214), (72, 72, 72, 72))
    base.alpha_composite(icon("d2_ico_quest_fertig", (108, 108)), (66, py + 255))
    d = ImageDraw.Draw(base, "RGBA")
    d.text((202, py + 225), "TÄGLICH · ANMELDUNG", font=font(FONT_BALOO, 21, 800),
           fill=(255, 177, 90, 255))
    d.text((202, py + 257), "Willkommen zurück", font=font(FONT_LILITA, 42),
           fill=(255, 240, 213, 255), stroke_width=1, stroke_fill=(10, 8, 7, 180))
    d.text((202, py + 309), "Melde dich heute an.", font=font(FONT_BALOO, 25, 700),
           fill=(214, 199, 166, 255))
    rounded_gradient(base, (202, py + 354, 256, 42), (100, 51, 24), (39, 22, 14), 18,
                     outline=(255, 138, 42, 190), outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.text((330, py + 375), "FERTIG · ABHOLBEREIT", font=font(FONT_LILITA, 19),
           fill=(255, 217, 168, 255), anchor="mm")

    # Full progress block.
    d.text((56, py + 452), "FORTSCHRITT", font=font(FONT_BALOO, 21, 800),
           fill=(185, 169, 136, 255))
    d.text((1024, py + 452), "1 / 1", font=font(FONT_LILITA, 24),
           fill=(255, 217, 168, 255), anchor="ra")
    draw_bar(base, 56, py + 484, 968, 34, 1.0)

    # Reward stack uses the project's real D2 icons; the clock's research-only use is explicit.
    d = ImageDraw.Draw(base, "RGBA")
    d.text((56, py + 554), "BELOHNUNG", font=font(FONT_BALOO, 22, 800),
           fill=(255, 220, 173, 255))
    paste_9(base, "d2_panel_frame", (36, py + 592, 1008, 326), (72, 72, 72, 72))

    reward_rows = [
        ("d2_ico_zeitkristall", "20", "Zeitkristalle", "Verdiente Währung"),
        ("d2_ico_uhr", "2 × 15 Min", "Glutuhren", "Nur für Forschung"),
    ]
    for idx, (ico, amount, title, subtitle) in enumerate(reward_rows):
        yy = py + 608 + idx * 150
        base.alpha_composite(icon(ico, (76, 76)), (66, yy + 15))
        d = ImageDraw.Draw(base, "RGBA")
        d.text((166, yy + 9), title, font=font(FONT_LILITA, 32),
               fill=(255, 240, 213, 255))
        d.text((166, yy + 51), amount, font=font(FONT_LILITA, 26),
               fill=(255, 217, 168, 255))
        d.text((410, yy + 53), subtitle, font=font(FONT_BALOO, 21, 700),
               fill=(185, 169, 136, 255))
        if idx == 0:
            ImageDraw.Draw(base, "RGBA").line((62, yy + 132, 1018, yy + 132),
                                              fill=(122, 90, 58, 150), width=2)

    btn_box = (286, py + 1060, 508, 122)
    add_glow(base, (btn_box[0] - 36, btn_box[1] - 24, btn_box[2] + 72, btn_box[3] + 48),
             color=(255, 104, 22, 104), blur=36)
    draw_primary_button(base, btn_box, "ABHOLEN", 39)

    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((px, py, px + pw - 1, py + 1347), 30,
                        outline=(201, 138, 74, 245), width=3)
    d.rounded_rectangle((px + 8, py + 8, px + pw - 9, py + 1340), 23,
                        outline=(239, 186, 124, 58), width=1)


def save_preview(image: Image.Image, path: Path) -> None:
    final = image.convert("RGB").resize(OUT_SIZE, Image.Resampling.LANCZOS)
    final.save(path, optimize=True)


def render() -> tuple[Path, Path]:
    main = draw_base()
    draw_main(main)
    save_preview(main, OUT_MAIN)

    detail = draw_base()
    draw_detail(detail)
    save_preview(detail, OUT_DETAIL)
    return OUT_MAIN, OUT_DETAIL


if __name__ == "__main__":
    for output in render():
        print(output)
