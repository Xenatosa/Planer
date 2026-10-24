#!/usr/bin/env python3
"""Render the D2 quests overview and detail at 576x1024."""
from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
HUD = HERE.parent
REPO = HUD.parents[2]
ART_CANDIDATES = (REPO / "team/art", Path("/workspace/handygame-plan/team/art"))


def asset_path(relative: str) -> Path:
    for root in ART_CANDIDATES:
        path = root / relative
        if path.exists():
            return path
    raise FileNotFoundError(f"D2 art asset not found: {relative}")


ASSETS = REPO / "team/art/ui-kit/menus_v3/_src/inventar_v4_assets"
EXPORT = asset_path("ui-kit/menus_v3/vorlage_D2_export")
ICONS = asset_path("hud_d2/icons_v1")
REVEAL = asset_path("ui-kit/menus_v3/_assets/reveal_v16")
FONT_BALOO = ASSETS / "Baloo2-Variable.ttf"
FONT_LILITA = ASSETS / "LilitaOne-Regular.ttf"
HERO_XP = asset_path("ui-kit/menus_v3/_assets/ico_heldenxp.png")

OUT_MAIN = HUD / "vorschau_menu_quests_d2_v2.png"
OUT_DETAIL = HUD / "vorschau_menu_quests_d2_v2_detail.png"

W, H = 1080, 1920
OUT_SIZE = (576, 1024)
PANEL = (14, 304, 1052, 1372)
DETAIL_PANEL = (14, 304, 1052, 1280)

C_TEXT = (243, 231, 207, 255)
C_MUTED = (185, 169, 136, 255)
C_SOFT = (214, 199, 166, 255)
C_GLUT = (255, 138, 42, 255)
C_GLOW = (255, 138, 42, 255)
C_BRONZE = (201, 138, 74, 245)
C_INK = (11, 9, 8, 255)
C_GOLD = (255, 217, 168, 255)


def font(path: Path, size: int, weight: int = 800) -> ImageFont.FreeTypeFont:
    result = ImageFont.truetype(str(path), size)
    if path == FONT_BALOO:
        try:
            result.set_variation_by_axes([weight])
        except (AttributeError, OSError):
            pass
    return result


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


def paste_9(base: Image.Image, name: str, box: tuple[int, int, int, int],
            borders: tuple[int, int, int, int]) -> None:
    x, y, w, h = box
    base.alpha_composite(nine_slice(load_sprite(name), (w, h), borders), (x, y))


def fit_icon(path: Path, size: tuple[int, int]) -> Image.Image:
    icon = Image.open(path).convert("RGBA")
    icon.thumbnail(size, Image.Resampling.LANCZOS)
    output = Image.new("RGBA", size, (0, 0, 0, 0))
    output.alpha_composite(icon, ((size[0] - icon.width) // 2, (size[1] - icon.height) // 2))
    return output


def icon(name: str, size: tuple[int, int]) -> Image.Image:
    path = next((root / "hud_d2/icons_v1" / f"{name}.png"
                 for root in ART_CANDIDATES
                 if (root / "hud_d2/icons_v1" / f"{name}.png").exists()), None)
    if path is None:
        path = next((root / "ui-kit/menus_v3/vorlage_D2_export" / f"{name}.png"
                     for root in ART_CANDIDATES
                     if (root / "ui-kit/menus_v3/vorlage_D2_export" / f"{name}.png").exists()), None)
    if path is None:
        path = next((root / "ui-kit/menus_v3/_assets/reveal_v16" / f"{name}.png"
                     for root in ART_CANDIDATES
                     if (root / "ui-kit/menus_v3/_assets/reveal_v16" / f"{name}.png").exists()), None)
    if path is None:
        raise FileNotFoundError(f"Quest icon not found: {name}")
    return fit_icon(path, size)


def draw_gradient(base: Image.Image, box: tuple[int, int, int, int],
                  top: tuple[int, int, int], bottom: tuple[int, int, int],
                  radius: int, outline: tuple[int, int, int, int] | None = None,
                  outline_width: int = 1) -> None:
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


def add_clipped_glow(base: Image.Image, box: tuple[int, int, int, int],
                     color: tuple[int, int, int, int], blur: int,
                     clip_box: tuple[int, int, int, int]) -> None:
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow, "RGBA").rounded_rectangle(
        (box[0], box[1], box[0] + box[2], box[1] + box[3]),
        radius=28, fill=color,
    )
    glow = glow.filter(ImageFilter.GaussianBlur(blur))
    mask = Image.new("L", base.size, 0)
    x, y, w, h = clip_box
    ImageDraw.Draw(mask).rounded_rectangle((x + 5, y + 5, x + w - 6, y + h - 6),
                                           radius=14, fill=255)
    glow.putalpha(ImageChops.multiply(glow.getchannel("A"), mask))
    base.alpha_composite(glow)


def texture_card(base: Image.Image, box: tuple[int, int, int, int],
                 ready: bool = False, muted: bool = False) -> None:
    x, y, w, h = box
    add_clipped_glow(base, (x + 70, y + 18, w - 140, h - 30),
                     (255, 105, 22, 140 if ready else 36), 24, box)
    paste_9(base, "d2_listenkarte_neutral", box, (12, 8, 8, 8))
    # A very fine ember grain gives the dark panel some material depth.
    grain = Image.new("RGBA", (w - 12, h - 12), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grain, "RGBA")
    for yy in range(7, h - 18, 14):
        for xx in range((yy * 37) % 31 + 9, w - 18, 47):
            gd.point((xx, yy), fill=(255, 214, 164, 9 if not muted else 5))
    mask = Image.new("L", grain.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, grain.width - 1, grain.height - 1),
                                           radius=14, fill=255)
    grain.putalpha(ImageChops.multiply(grain.getchannel("A"), mask))
    base.alpha_composite(grain, (x + 6, y + 6))
    if ready:
        d = ImageDraw.Draw(base, "RGBA")
        d.rounded_rectangle((x + 2, y + 2, x + w - 3, y + h - 3), 14,
                            outline=(255, 155, 66, 230), width=3)
        d.line((x + 20, y + 4, x + w - 20, y + 4), fill=(255, 226, 180, 140), width=2)
    if muted:
        veil = Image.new("RGBA", (w - 12, h - 12), (8, 8, 7, 128))
        m = Image.new("L", veil.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, veil.width - 1, veil.height - 1),
                                            radius=14, fill=140)
        veil.putalpha(m)
        base.alpha_composite(veil, (x + 6, y + 6))


def draw_primary_button(base: Image.Image, box: tuple[int, int, int, int], label: str,
                        face_size: int) -> None:
    x, y, w, h = box
    add_clipped_glow(base, (x - 12, y + 1, w + 24, h + 15), (255, 102, 22, 115), 20,
                     (x - 4, y - 3, w + 8, h + 8))
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x, y + 8, x + w, y + h + 8), 18, fill=(73, 31, 14, 255))
    draw_gradient(base, box, (255, 192, 106), (216, 78, 14), 17,
                  outline=(255, 226, 177, 245), outline_width=2)
    d = ImageDraw.Draw(base, "RGBA")
    d.line((x + 18, y + 5, x + w - 18, y + 5), fill=(255, 246, 224, 160), width=2)
    d.text((x + w // 2, y + h // 2 - 2), label, font=font(FONT_LILITA, face_size),
           fill=(255, 248, 232, 255), anchor="mm", stroke_width=1,
           stroke_fill=(79, 31, 13, 170))


def draw_secondary_button(base: Image.Image, box: tuple[int, int, int, int], label: str) -> None:
    x, y, w, h = box
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x, y + 6, x + w, y + h + 6), 16, fill=(8, 7, 6, 255))
    draw_gradient(base, box, (64, 47, 34), (23, 17, 13), 15,
                  outline=(153, 114, 74, 190), outline_width=2)
    ImageDraw.Draw(base, "RGBA").text((x + w // 2, y + h // 2 - 1), label,
                                      font=font(FONT_LILITA, 25), fill=C_TEXT,
                                      anchor="mm", stroke_width=1,
                                      stroke_fill=(7, 6, 5, 180))


def draw_base() -> Image.Image:
    # Shop v1c owns the approved D2 top bar and dock treatment.
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import render_vorschau_menu_shop_d2_v1c as shop_chrome

    base = Image.open(shop_chrome.CHROME).convert("RGBA")
    if base.size != (W, H):
        raise SystemExit(f"HUD-Chrome expected {W}×{H}, received {base.size}")
    shop_chrome.draw_dock_background(base)
    shop_chrome.add_full_screen_scrim(base)
    shop_chrome.draw_dock_tabs(base)
    return base


def draw_outer_panel(base: Image.Image, panel: tuple[int, int, int, int]) -> None:
    x, y, w, h = panel
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow, "RGBA").rounded_rectangle((x, y + 12, x + w, y + h + 12),
                                                       30, fill=(0, 0, 0, 210))
    base.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(22)))
    add_clipped_glow(base, (x + 28, y + 10, w - 56, 160), (255, 110, 32, 70), 34, panel)
    paste_9(base, "d2_panel_frame", panel, (72, 72, 72, 72))
    draw_gradient(base, (x + 10, y + 10, w - 20, h - 20), (35, 25, 20), (12, 10, 9),
                  26, outline=(255, 226, 181, 60), outline_width=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x + 2, y + 2, x + w - 3, y + h - 3), 28,
                        outline=C_BRONZE, width=3)
    d.rounded_rectangle((x + 10, y + 10, x + w - 11, y + h - 11), 23,
                        outline=(239, 186, 124, 70), width=1)
    # Fine engraved corner lines remain fully inside the frame.
    for sx in (x + 20, x + w - 20):
        sign = 1 if sx == x + 20 else -1
        d.line((sx, y + 46, sx + sign * 26, y + 46), fill=(255, 185, 112, 100), width=2)
        d.line((sx, y + 46, sx, y + 68), fill=(255, 185, 112, 70), width=2)


def draw_header(base: Image.Image, detail: bool = False) -> None:
    px, py, pw, _ = DETAIL_PANEL if detail else PANEL
    back_box = (px + 24, py + 12, 78, 78)
    draw_gradient(base, back_box, (65, 47, 34), (24, 17, 13), 20,
                  outline=(202, 150, 93, 205), outline_width=2)
    base.alpha_composite(icon("d2_ico_zurueck", (42, 42)), (back_box[0] + 18, back_box[1] + 18))

    d = ImageDraw.Draw(base, "RGBA")
    title = "TAGESAUFGABE" if detail else "AUFGABEN"
    title_size = 57 if not detail else 52
    d.text((px + 126, py + 6), title, font=font(FONT_LILITA, title_size),
           fill=(255, 231, 193, 255), stroke_width=1, stroke_fill=(40, 21, 12, 190))
    subtitle = "TÄGLICH · ERNTE" if detail else "TÄGLICH · 5 AUS DEM POOL + ANMELDUNG"
    d.text((px + 130, py + 57), subtitle, font=font(FONT_BALOO, 21, 800), fill=C_MUTED)

    # A contained quest seal balances the title and reinforces the active feature.
    seal_x, seal_y = px + pw - 106, py + 14
    draw_gradient(base, (seal_x, seal_y, 72, 72), (80, 45, 24), (22, 15, 11), 21,
                  outline=(221, 157, 86, 165), outline_width=2)
    base.alpha_composite(icon("d2_ico_quest_fertig" if detail else "d2_ico_quest", (48, 48)),
                         (seal_x + 12, seal_y + 12))


TABS = [
    ("TUTORIAL", "d2_ico_quest_fertig"),
    ("HAUPT", "d2_ico_quest"),
    ("NEBEN", "d2_ico_quest"),
    ("TÄGLICH", "d2_ico_gratis_login"),
    ("WOCHE", "d2_ico_kiste"),
    ("ERFOLGE", "d2_ico_erfolge"),
    ("EVENT", "d2_ico_events"),
]


def draw_tabs(base: Image.Image, active: int = 3, y: int = 404) -> None:
    x0, width, height, gap = 40, 136, 86, 8
    for index, (label, icon_name) in enumerate(TABS):
        x = x0 + index * (width + gap)
        sprite = "d2_tab_aktiv" if index == active else "d2_tab_inaktiv"
        paste_9(base, sprite, (x, y, width, height), (8, 8, 8, 12 if index == active else 10))
        if index == active:
            add_clipped_glow(base, (x + 12, y + height - 21, width - 24, 16),
                             (255, 115, 35, 130), 8, (x, y, width, height))
            ImageDraw.Draw(base, "RGBA").line((x + 14, y + height - 5,
                                                 x + width - 14, y + height - 5),
                                                fill=(255, 138, 42, 235), width=4)
        ico = icon(icon_name, (32, 32))
        if index != active:
            ico = ImageEnhance.Brightness(ico).enhance(0.72)
        base.alpha_composite(ico, (x + (width - 32) // 2, y + 10))
        d = ImageDraw.Draw(base, "RGBA")
        d.text((x + width // 2, y + 52), label, font=font(FONT_LILITA, 18),
               fill=(255, 223, 177, 255) if index == active else (179, 163, 132, 255),
               anchor="mm", stroke_width=1, stroke_fill=(8, 6, 5, 165))
        if index == active:
            base.alpha_composite(icon("d2_ico_badge_punkt", (23, 23)), (x + width - 31, y + 4))


def draw_reward_preview(base: Image.Image) -> None:
    x, y, w, h = 36, 504, 1008, 170
    add_clipped_glow(base, (x + 100, y + 8, w - 200, h - 12), (255, 105, 24, 95), 28,
                     (x, y, w, h))
    paste_9(base, "d2_panel_frame_glut", (x, y, w, h), (72, 72, 72, 72))
    draw_gradient(base, (x + 9, y + 9, w - 18, h - 18), (59, 35, 23), (22, 14, 11),
                  21, outline=(255, 214, 160, 90), outline_width=1)
    # Crystal stage has its own inner bezel and light edge.
    draw_gradient(base, (x + 19, y + 18, 132, 134), (103, 57, 28), (25, 16, 12),
                  19, outline=(241, 175, 103, 205), outline_width=2)
    add_clipped_glow(base, (x + 45, y + 39, 81, 81), (255, 110, 35, 90), 22,
                     (x + 20, y + 18, 130, 134))
    base.alpha_composite(icon("d2_ico_zeitkristall", (100, 100)), (x + 35, y + 34))

    d = ImageDraw.Draw(base, "RGBA")
    d.text((x + 174, y + 27), "TAGESPRÄMIE", font=font(FONT_BALOO, 22, 800),
           fill=(255, 178, 94, 255), stroke_width=1, stroke_fill=(30, 14, 8, 140))
    d.text((x + 170, y + 56), "20 LOGIN + 5 × 8 AUS QUESTS",
           font=font(FONT_LILITA, 29), fill=(255, 241, 215, 255),
           stroke_width=1, stroke_fill=(15, 9, 7, 170))
    d.line((x + 174, y + 103, x + 697, y + 103), fill=(215, 157, 96, 100), width=2)
    d.text((x + 174, y + 117), "Reset täglich um 04:00", font=font(FONT_BALOO, 20, 700),
           fill=(193, 176, 145, 255))

    # A compact total seal makes the complete GDD reward visible at a glance.
    seal = (x + w - 224, y + 19, 202, 132)
    draw_gradient(base, seal, (78, 43, 25), (22, 15, 12), 24,
                  outline=(255, 177, 93, 210), outline_width=2)
    base.alpha_composite(icon("d2_ico_zeitkristall", (48, 48)), (seal[0] + 14, seal[1] + 38))
    d = ImageDraw.Draw(base, "RGBA")
    d.text((seal[0] + 72, seal[1] + 39), "60", font=font(FONT_LILITA, 48),
           fill=(255, 217, 168, 255), anchor="lm", stroke_width=1, stroke_fill=(39, 19, 9, 180))
    d.text((seal[0] + 77, seal[1] + 91), "ZEITKRISTALLE", font=font(FONT_BALOO, 16, 800),
           fill=(224, 199, 163, 255), anchor="lm")
    # Engraved corner strokes stay inside the card's inset.
    d.line((x + 160, y + 16, x + 182, y + 16), fill=(255, 215, 162, 80), width=2)
    d.line((x + 160, y + 16, x + 160, y + 34), fill=(255, 215, 162, 60), width=2)


REWARD_INFO = {
    "crystal": ("d2_ico_zeitkristall", "ZEITKRISTALLE"),
    "clock": ("d2_ico_uhr", "GLUTUHREN"),
    "food": ("d2_ico_nahrung", "NAHRUNG"),
    "wood": ("d2_ico_holz", "HOLZ"),
    "xp": (None, "HELDEN-EP"),
    "shell": ("d2_ico_gold_muschel", "MUSCHELN"),
}


QUESTS = [
    {"title": "Ernte einholen", "desc": "Sammle 3-mal Produktion ein.",
     "type": "ERNTE", "icon": "d2_ico_nahrung", "progress": (3, 3), "ready": True,
     "rewards": [("crystal", "8"), ("food", "100")]},
    {"title": "Fleißige Hände", "desc": "Verbessere 3 Gebäude.",
     "type": "BAUEN", "icon": "d2_ico_bauen", "progress": (1, 3), "ready": False,
     "rewards": [("crystal", "8"), ("wood", "100")]},
    {"title": "Kriegerdrill", "desc": "Bilde 10 Einheiten aus.",
     "type": "ARMEE", "icon": "d2_ico_dock_armee", "progress": (6, 10), "ready": False,
     "rewards": [("crystal", "8"), ("xp", "30")]},
    {"title": "Auf ins Feld", "desc": "Spiele 2 Kampagnenmissionen (Wiederholungen zählen).",
     "type": "KAMPAGNE", "icon": "d2_ico_dock_karte", "progress": (1, 2), "ready": False,
     "rewards": [("crystal", "8"), ("xp", "40")]},
    {"title": "Volle Bäuche", "desc": "Gib 500 Nahrung aus.",
     "type": "MUSCHELN", "icon": "d2_ico_gold_muschel", "progress": (320, 500), "ready": False,
     "rewards": [("crystal", "8"), ("shell", "30")]},
    {"title": "Willkommen zurück", "desc": "Melde dich heute an.",
     "type": "ANMELDUNG", "icon": "d2_ico_gratis_login", "progress": (1, 1),
     "claimed": True, "rewards": [("crystal", "20")]},
]


def draw_progress(base: Image.Image, x: int, y: int, width: int, height: int,
                  current: int, total: int, muted: bool = False) -> None:
    paste_9(base, "d2_bar_bg", (x, y, width, height), (15, 2, 15, 2))
    if current > 0:
        fill_width = max(32, round(width * min(1, current / max(total, 1))))
        paste_9(base, "d2_bar_fill_glut", (x + 1, y - 3, min(width - 2, fill_width), height + 6),
                (27, 8, 27, 8))
    if muted:
        ImageDraw.Draw(base, "RGBA").rounded_rectangle(
            (x + 1, y, x + width - 2, y + height - 1), 8, fill=(14, 13, 11, 120))


def draw_reward_chip(base: Image.Image, x: int, y: int, width: int,
                     kind: str, amount: str, muted: bool = False) -> None:
    paste_9(base, "d2_chip", (x, y, width, 38), (33, 4, 33, 4))
    sprite, label = REWARD_INFO[kind]
    art = fit_icon(HERO_XP, (28, 28)) if sprite is None else icon(sprite, (28, 28))
    if muted:
        art = ImageEnhance.Brightness(art).enhance(0.4)
    base.alpha_composite(art, (x + 8, y + 5))
    d = ImageDraw.Draw(base, "RGBA")
    ink = (164, 153, 129, 255) if muted else (238, 222, 188, 255)
    label_text = f"{amount} {label}"
    face = font(FONT_LILITA, 18)
    while d.textbbox((0, 0), label_text, font=face)[2] > width - 47 and face.size > 15:
        face = font(FONT_LILITA, face.size - 1)
    d.text((x + 43, y + 19), label_text, font=face, fill=ink, anchor="lm",
           stroke_width=1 if not muted else 0, stroke_fill=(8, 6, 5, 135))


def draw_icon_frame(base: Image.Image, x: int, y: int, icon_name: str,
                    category: str, muted: bool = False, large: bool = False) -> None:
    width, height = (178, 244) if large else (108, 126)
    draw_gradient(base, (x, y, width, height), (74, 47, 29), (20, 15, 12), 17,
                  outline=(191, 139, 83, 205) if not muted else (104, 94, 77, 160), outline_width=2)
    d = ImageDraw.Draw(base, "RGBA")
    d.line((x + 12, y + 3, x + width - 12, y + 3),
           fill=(255, 218, 160, 120) if not muted else (175, 164, 140, 70), width=2)
    if large:
        icon_size = 126
        art_y = y + 32
        cat_y = y + 178
        category_size = 22
    else:
        icon_size = 72
        art_y = y + 12
        cat_y = y + 96
        category_size = 15
    art = icon(icon_name, (icon_size, icon_size))
    if muted:
        art = ImageEnhance.Brightness(art).enhance(0.42)
    base.alpha_composite(art, (x + (width - icon_size) // 2, art_y))
    d.text((x + width // 2, cat_y), category, font=font(FONT_BALOO, category_size, 800),
           fill=(255, 191, 116, 255) if not muted else (157, 148, 128, 255),
           anchor="mm", stroke_width=1, stroke_fill=(9, 7, 6, 175))


def draw_quest_row(base: Image.Image, y: int, quest: dict[str, object], selected: bool = False) -> None:
    x, width, height = 36, 1008, 154
    ready = bool(quest.get("ready", False))
    claimed = bool(quest.get("claimed", False))
    box = (x, y, width, height)
    texture_card(base, box, ready=ready, muted=claimed)
    draw_icon_frame(base, x + 14, y + 14, str(quest["icon"]), str(quest["type"]), muted=claimed)

    text_x = x + 140
    title_fill = (255, 242, 217, 255) if not claimed else (169, 159, 138, 255)
    body_fill = C_MUTED if not claimed else (139, 133, 118, 255)
    d = ImageDraw.Draw(base, "RGBA")
    d.text((text_x, y + 7), str(quest["title"]), font=font(FONT_LILITA, 29),
           fill=title_fill, stroke_width=1, stroke_fill=(9, 7, 6, 170))
    d.text((text_x, y + 40), str(quest["desc"]), font=font(FONT_BALOO, 19, 700), fill=body_fill)

    current, total = quest["progress"]
    bar_x, bar_y, bar_w, bar_h = text_x, y + 70, 540, 22
    draw_progress(base, bar_x, bar_y, bar_w, bar_h, current, total, muted=claimed)
    d = ImageDraw.Draw(base, "RGBA")
    counter_fill = (255, 218, 170, 255) if ready and not claimed else body_fill
    d.text((bar_x + bar_w + 11, bar_y + 11), f"{current} / {total}",
           font=font(FONT_LILITA, 20), fill=counter_fill, anchor="lm")

    rewards = quest["rewards"]
    draw_reward_chip(base, text_x, y + 105, 242, rewards[0][0], rewards[0][1], muted=claimed)
    if len(rewards) > 1:
        draw_reward_chip(base, text_x + 252, y + 105, 208, rewards[1][0], rewards[1][1], muted=claimed)

    if ready:
        draw_primary_button(base, (x + width - 194, y + 48, 170, 60), "ABHOLEN", 23)
    elif claimed:
        # Claimed rows are always sorted last and end with the game's real completed-quest seal.
        draw_gradient(base, (x + width - 83, y + 39, 62, 62), (73, 51, 31), (19, 15, 11),
                      20, outline=(147, 125, 89, 150), outline_width=2)
        base.alpha_composite(icon("d2_ico_quest_fertig", (42, 42)),
                             (x + width - 73, y + 49))
    else:
        draw_secondary_button(base, (x + width - 178, y + 48, 154, 60), "LOS")


def draw_main(base: Image.Image) -> None:
    draw_outer_panel(base, PANEL)
    draw_header(base)
    draw_tabs(base, active=3, y=404)
    draw_reward_preview(base)
    list_y = 686
    # Claimable first, in-progress tasks next, already claimed login last.
    for index, quest in enumerate(QUESTS):
        draw_quest_row(base, list_y + index * 162, quest)
    x, y, w, h = PANEL
    d = ImageDraw.Draw(base, "RGBA")
    d.rounded_rectangle((x + 2, y + 2, x + w - 3, y + h - 3), 28,
                        outline=C_BRONZE, width=3)
    d.rounded_rectangle((x + 10, y + 10, x + w - 11, y + h - 11), 23,
                        outline=(239, 186, 124, 70), width=1)


def draw_reward_tile(base: Image.Image, box: tuple[int, int, int, int],
                     kind: str, amount: str, item_name: str) -> None:
    x, y, w, h = box
    add_clipped_glow(base, (x + 45, y + 18, w - 90, h - 35), (255, 111, 28, 44), 24, box)
    paste_9(base, "d2_panel_frame_muted", box, (72, 72, 72, 72))
    draw_gradient(base, (x + 9, y + 9, w - 18, h - 18), (42, 31, 24), (17, 13, 11),
                  19, outline=(233, 179, 119, 100), outline_width=1)
    # Small corner diamonds and separator give each reward a collectible presentation.
    d = ImageDraw.Draw(base, "RGBA")
    d.polygon(((x + 16, y + 16), (x + 24, y + 24), (x + 16, y + 32), (x + 8, y + 24)),
              fill=(255, 198, 126, 190))
    d.polygon(((x + w - 16, y + 16), (x + w - 8, y + 24),
               (x + w - 16, y + 32), (x + w - 24, y + 24)), fill=(255, 198, 126, 190))
    d.line((x + 20, y + 59, x + 20, y + h - 30), fill=(194, 137, 82, 120), width=2)
    d.line((x + 20, y + h - 30, x + w - 20, y + h - 30), fill=(194, 137, 82, 100), width=2)
    sprite, _ = REWARD_INFO[kind]
    art = fit_icon(HERO_XP, (100, 100)) if sprite is None else icon(sprite, (100, 100))
    base.alpha_composite(art, (x + 36, y + 84))
    d = ImageDraw.Draw(base, "RGBA")
    d.text((x + 154, y + 63), item_name, font=font(FONT_BALOO, 22, 800),
           fill=(255, 195, 124, 255))
    d.text((x + 151, y + 102), amount, font=font(FONT_LILITA, 54),
           fill=(255, 241, 215, 255), stroke_width=1, stroke_fill=(10, 7, 5, 180))
    d.line((x + 152, y + 168, x + w - 34, y + 168), fill=(182, 132, 82, 110), width=1)
    d.text((x + 152, y + 187), "QUEST-LOHN", font=font(FONT_BALOO, 18, 800),
           fill=(179, 162, 134, 255))


def draw_detail(base: Image.Image) -> None:
    draw_outer_panel(base, DETAIL_PANEL)
    draw_header(base, detail=True)
    draw_tabs(base, active=3, y=404)

    # Large quest identity card with a real harvest icon, full goal and glowing completion state.
    x, y, w, h = 36, 504, 1008, 318
    texture_card(base, (x, y, w, h), ready=True)
    draw_icon_frame(base, x + 20, y + 24, "d2_ico_nahrung", "ERNTE", large=True)
    text_x = x + 228
    d = ImageDraw.Draw(base, "RGBA")
    d.text((text_x, y + 26), "TÄGLICH · ERNTE", font=font(FONT_BALOO, 22, 800),
           fill=(255, 179, 97, 255))
    d.text((text_x - 2, y + 59), "Ernte einholen", font=font(FONT_LILITA, 43),
           fill=(255, 242, 217, 255), stroke_width=1, stroke_fill=(9, 7, 6, 170))
    d.text((text_x, y + 113), "Sammle 3-mal Produktion ein.", font=font(FONT_BALOO, 25, 700),
           fill=(214, 199, 166, 255))
    # Status is close to the quest title and never crosses the card's right edge.
    draw_gradient(base, (text_x, y + 157, 248, 42), (99, 49, 22), (37, 21, 13),
                  18, outline=(255, 138, 42, 205), outline_width=1)
    ImageDraw.Draw(base, "RGBA").text((text_x + 124, y + 178), "FERTIG · ABHOLBEREIT",
                                       font=font(FONT_LILITA, 18), fill=C_GOLD, anchor="mm")
    d = ImageDraw.Draw(base, "RGBA")
    d.text((text_x, y + 214), "FORTSCHRITT", font=font(FONT_BALOO, 18, 800), fill=C_MUTED)
    d.text((x + w - 30, y + 214), "3 / 3", font=font(FONT_LILITA, 22),
           fill=C_GOLD, anchor="ra")
    draw_progress(base, text_x, y + 244, w - 272, 25, 3, 3)

    d = ImageDraw.Draw(base, "RGBA")
    d.text((42, 850), "BELOHNUNGEN", font=font(FONT_BALOO, 23, 800),
           fill=(255, 221, 176, 255))
    d.line((226, 865, 1038, 865), fill=(190, 136, 83, 115), width=2)

    # The pair of framed rewards is deliberately a single row, with a generous claim area below.
    reward_frame = (36, 884, 1008, 548)
    paste_9(base, "d2_panel_frame", reward_frame, (72, 72, 72, 72))
    draw_gradient(base, (45, 893, 990, 530), (34, 25, 20), (15, 12, 10),
                  24, outline=(235, 184, 127, 70), outline_width=1)
    draw_reward_tile(base, (56, 910, 468, 278), "crystal", "8", "ZEITKRISTALLE")
    draw_reward_tile(base, (536, 910, 488, 278), "food", "100", "NAHRUNG")

    draw_primary_button(base, (346, 1210, 388, 102), "ABHOLEN", 34)
    d = ImageDraw.Draw(base, "RGBA")
    d.line((74, 1340, 1006, 1340), fill=(151, 108, 67, 115), width=2)
    base.alpha_composite(icon("d2_ico_uhr", (34, 34)), (82, 1361))
    d.text((128, 1377), "Bleibt bis zum Tagesreset um 04:00 abholbar.",
           font=font(FONT_BALOO, 20, 700), fill=(186, 170, 140, 255), anchor="lm")

    px, py, pw, ph = DETAIL_PANEL
    d.rounded_rectangle((px + 2, py + 2, px + pw - 3, py + ph - 3), 28,
                        outline=C_BRONZE, width=3)
    d.rounded_rectangle((px + 10, py + 10, px + pw - 11, py + ph - 11), 23,
                        outline=(239, 186, 124, 70), width=1)
    # Hide the underlying village quest strip while keeping the shop's dock untouched.
    under_y = py + ph + 1
    under_h = max(1, 1668 - under_y)
    draw_gradient(base, (0, under_y, W, under_h), (16, 12, 10), (9, 7, 6), 0)
    ImageDraw.Draw(base, "RGBA").line((0, under_y, W, under_y),
                                      fill=(255, 255, 255, 26), width=2)


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
