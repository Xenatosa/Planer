#!/usr/bin/env python3
"""Render the D2 chat, player options, and report sheet at 576x1024."""
from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
SRC = HERE / "_src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
import render_vorschau_menu_quests_d2_v2 as d2  # noqa: E402


OUT_MAIN = HERE / "vorschau_menu_chat_d2_v1d.png"
OUT_OPTIONS = HERE / "vorschau_menu_chat_d2_v1d_optionen.png"
OUT_REPORT = HERE / "vorschau_menu_chat_d2_v1d_melden.png"
OUT_BLOCK = HERE / "vorschau_menu_chat_d2_v1d_blockieren.png"
OUT_SIZE = (576, 1024)
PANEL = (14, 304, 1052, 1372)
HERO_DIR = HERE.parent / "heroes"

C_TEXT = (243, 231, 207, 255)
C_SOFT = (214, 199, 166, 255)
C_MUTED = (185, 169, 136, 255)
C_GOLD = (255, 217, 168, 255)
C_ORANGE = (255, 138, 42, 255)
C_RED = (238, 75, 57, 255)
C_LINE = (188, 137, 86, 105)


def font(path: Path, size: int, weight: int = 800) -> ImageFont.FreeTypeFont:
    return d2.font(path, size, weight)


def draw_text(base: Image.Image, xy: tuple[int, int], value: str, size: int,
              color=C_TEXT, *, lilita: bool = False, anchor: str | None = None,
              stroke: bool = False) -> None:
    ImageDraw.Draw(base, "RGBA").text(
        xy, value, font=font(d2.FONT_LILITA if lilita else d2.FONT_BALOO, size),
        fill=color, anchor=anchor,
        stroke_width=1 if stroke else 0,
        stroke_fill=(19, 10, 7, 185) if stroke else None,
    )


def fit_text(base: Image.Image, xy: tuple[int, int], value: str, width: int,
             size: int, color=C_TEXT, *, lilita: bool = False,
             minimum: int = 16, anchor: str | None = None,
             stroke: bool = False) -> None:
    path = d2.FONT_LILITA if lilita else d2.FONT_BALOO
    face = font(path, size)
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    while probe.textbbox((0, 0), value, font=face)[2] > width and face.size > minimum:
        face = font(path, face.size - 1)
    ImageDraw.Draw(base, "RGBA").text(
        xy, value, font=face, fill=color, anchor=anchor,
        stroke_width=1 if stroke else 0,
        stroke_fill=(19, 10, 7, 185) if stroke else None,
    )


def fitted_font(value: str, width: int, size: int, *, lilita: bool = False,
                minimum: int = 16) -> ImageFont.FreeTypeFont:
    path = d2.FONT_LILITA if lilita else d2.FONT_BALOO
    face = font(path, size)
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    while probe.textbbox((0, 0), value, font=face)[2] > width and face.size > minimum:
        face = font(path, face.size - 1)
    return face


def bubble_line_layout(lines: tuple[str, ...], width: int, size: int,
                       *, padding: int = 24, line_gap: int = 34
                       ) -> tuple[list[ImageFont.FreeTypeFont], list[int], int]:
    """Measure a text block with fixed line spacing and vertical padding."""
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    faces = [fitted_font(line, width, size) for line in lines]
    boxes = [probe.textbbox((0, 0), line, font=face, anchor="lm")
             for line, face in zip(lines, faces)]
    offsets = [box[1] + index * line_gap for index, box in enumerate(boxes)]
    top_offset = min(offsets)
    centers = [padding - top_offset + index * line_gap
               for index in range(len(lines))]
    content_bottom = max(center + box[3]
                         for center, box in zip(centers, boxes))
    return faces, centers, content_bottom


def draw_header(base: Image.Image) -> None:
    x, y, w, _ = PANEL
    back = (x + 24, y + 12, 78, 78)
    d2.draw_gradient(base, back, (65, 47, 34), (24, 17, 13), 20,
                     outline=(202, 150, 93, 205), outline_width=2)
    base.alpha_composite(d2.icon("d2_ico_zurueck", (42, 42)),
                         (back[0] + 18, back[1] + 18))
    fit_text(base, (x + 126, y + 5), "CHAT", w - 275, 56,
             (255, 231, 193, 255), lilita=True, minimum=38, stroke=True)
    fit_text(base, (x + 130, y + 61), "GEMEINSAM IN EPODARIEN", w - 300, 22,
             C_MUTED, minimum=17)

    # Translation is a compact header icon like the back control, with an orange
    # active state and a small status ember instead of a separate text switch.
    control = (x + w - 24 - 78, y + 12, 78, 78)
    d2.draw_gradient(base, control, (86, 50, 28), (29, 19, 14), 20,
                     outline=(247, 158, 83, 220), outline_width=2)
    draw = ImageDraw.Draw(base, "RGBA")
    gx, gy = control[0] + 39, control[1] + 39
    orange = (255, 153, 67, 255)
    draw.ellipse((gx - 20, gy - 20, gx + 20, gy + 20),
                 outline=orange, width=3)
    draw.arc((gx - 10, gy - 20, gx + 10, gy + 20), 75, 285,
             fill=orange, width=2)
    draw.arc((gx - 10, gy - 20, gx + 10, gy + 20), 255, 105,
             fill=orange, width=2)
    draw.arc((gx - 19, gy - 10, gx + 19, gy + 10), 0, 180,
             fill=orange, width=2)
    draw.arc((gx - 19, gy - 10, gx + 19, gy + 10), 180, 360,
             fill=orange, width=2)
    draw.line((gx - 18, gy, gx + 18, gy), fill=orange, width=2)
    draw.ellipse((gx + 11, gy + 11, gx + 21, gy + 21),
                 fill=orange, outline=(37, 23, 16, 255), width=2)


def draw_outer_panel(base: Image.Image) -> None:
    d2.draw_outer_panel(base, PANEL)
    draw_header(base)


def draw_tabs(base: Image.Image) -> None:
    tabs = (("WELT", 0), ("GILDE", 2), ("PRIVAT", 1), ("SYSTEM", 3))
    x0, y, width, height, gap = 42, 412, 240, 82, 10
    for index, (label, unread) in enumerate(tabs):
        x = x0 + index * (width + gap)
        active = index == 0
        sprite = "d2_tab_aktiv" if active else "d2_tab_inaktiv"
        d2.paste_9(base, sprite, (x, y, width, height),
                   (8, 8, 8, 12 if active else 10))
        if active:
            d2.add_clipped_glow(base, (x + 14, y + height - 20, width - 28, 15),
                                (255, 115, 35, 115), 8, (x, y, width, height))
            ImageDraw.Draw(base, "RGBA").line((x + 17, y + height - 5,
                                                 x + width - 17, y + height - 5),
                                                fill=(255, 138, 42, 230), width=4)
        center_x = x + width // 2 - (17 if unread else 0)
        draw_text(base, (center_x, y + height // 2), label, 25,
                  C_GOLD if active else C_SOFT, lilita=True, anchor="mm")
        if unread:
            badge = (x + width - 39, y + 11, 31, 31)
            d2.draw_gradient(base, badge, (255, 154, 65), (190, 61, 27), 16,
                             outline=(255, 221, 171, 220), outline_width=2)
            draw_text(base, (badge[0] + 15, badge[1] + 15), str(unread), 18,
                      (255, 245, 224, 255), lilita=True, anchor="mm")


def draw_avatar(base: Image.Image, box: tuple[int, int, int, int],
                hero: str = "ruka") -> None:
    """Place an in-repo hero portrait inside a clipped bronze bezel."""
    x, y, size, _ = box
    inset = 5
    inner_size = size - inset * 2
    portrait_path = HERO_DIR / f"hero_{hero}_portrait_alpha.png"
    with Image.open(portrait_path) as source:
        portrait = source.convert("RGBA")
    # Cover-crop to a square before resizing, then mask every pixel to the bezel.
    sw, sh = portrait.size
    crop_size = min(sw, sh)
    left, top = (sw - crop_size) // 2, (sh - crop_size) // 2
    portrait = portrait.crop((left, top, left + crop_size, top + crop_size))
    portrait = portrait.resize((inner_size, inner_size), Image.Resampling.LANCZOS)
    underlay = Image.new("RGBA", portrait.size, (35, 22, 15, 255))
    underlay.alpha_composite(portrait)
    mask = Image.new("L", portrait.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, inner_size - 1, inner_size - 1),
                                            12, fill=255)
    underlay.putalpha(mask)
    base.alpha_composite(underlay, (x + inset, y + inset))
    ImageDraw.Draw(base, "RGBA").rounded_rectangle(
        (x, y, x + size - 1, y + size - 1), 17,
        outline=(239, 175, 103, 235), width=3,
    )


def draw_guild_tag(base: Image.Image, x: int, y: int, label: str,
                   width: int) -> None:
    d2.draw_gradient(base, (x, y, width, 34), (76, 52, 33), (30, 21, 15), 12,
                     outline=(176, 127, 77, 130), outline_width=1)
    fit_text(base, (x + width // 2, y + 17), label, width - 14, 18,
             (239, 203, 154, 255), lilita=True, minimum=14, anchor="mm")


def draw_system_message(base: Image.Image, y: int) -> None:
    draw = ImageDraw.Draw(base, "RGBA")
    draw.line((115, y + 34, 330, y + 34), fill=(172, 125, 80, 72), width=1)
    draw.line((750, y + 34, 965, y + 34), fill=(172, 125, 80, 72), width=1)
    draw_text(base, (540, y + 7), "SYSTEM · 09:41", 18,
              C_MUTED, lilita=True, anchor="mm")
    fit_text(base, (540, y + 44), "Das Erntefest beginnt. Viel Freude beim Sammeln!",
             610, 24, (207, 190, 158, 255), minimum=19, anchor="mm")


def draw_incoming(base: Image.Image, y: int, name: str, guild: str,
                  time: str, lines: tuple[str, ...], avatar: str = "ruka",
                  *, translated_from: str | None = None,
                  translate_button: bool = False) -> int:
    draw_avatar(base, (56, y + 48, 92, 92), avatar)
    draw_text(base, (165, y + 7), name, 25, C_TEXT, lilita=True)
    name_width = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox(
        (0, 0), name, font=font(d2.FONT_LILITA, 25))[2]
    tag_x = 165 + name_width + 12
    tag_width = 190 if guild == "[MORGENROT]" else 194
    draw_guild_tag(base, tag_x, y + 4, guild, tag_width)
    draw_text(base, (1016, y + 19), time, 19, C_MUTED, anchor="rm")
    bubble_x, bubble_y, bubble_width = 164, y + 48, 860
    text_width = bubble_width - 44
    text_size = 27 if len(lines) == 1 else 26
    faces, centers, content_bottom = bubble_line_layout(
        lines, text_width, text_size)
    addition_top = content_bottom + 12
    addition_face = None
    addition_center = None
    if translated_from:
        label = "Übersetzt · Original anzeigen"
        addition_face = fitted_font(label, bubble_width - 46, 19, minimum=16)
        addition_bbox = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox(
            (0, 0), label, font=addition_face, anchor="lm")
        addition_center = addition_top - addition_bbox[1]
        content_bottom = addition_center + addition_bbox[3]
    elif translate_button:
        content_bottom = addition_top + 34
    bubble_height = content_bottom + 24
    bubble = (bubble_x, bubble_y, bubble_width, bubble_height)
    d2.draw_gradient(base, bubble, (57, 40, 29), (24, 18, 14), 20,
                     outline=(168, 121, 76, 115), outline_width=2)
    draw = ImageDraw.Draw(base, "RGBA")
    for line, face, center in zip(lines, faces, centers):
        draw.text((bubble[0] + 23, bubble[1] + center), line, font=face,
                  fill=C_TEXT, anchor="lm")
    if translated_from:
        draw.text((bubble[0] + 23, bubble[1] + addition_center), label,
                  font=addition_face, fill=(211, 188, 153, 255), anchor="lm")
    elif translate_button:
        button = (bubble[0] + 22, bubble[1] + addition_top, 158, 34)
        d2.draw_gradient(base, button, (81, 54, 33), (35, 24, 17), 11,
                         outline=(192, 142, 87, 170), outline_width=1)
        draw_text(base, (button[0] + button[2] // 2, button[1] + button[3] // 2),
                  "ÜBERSETZEN", 17, (242, 208, 165, 255), lilita=True, anchor="mm")
    return 48 + max(bubble_height, 92)


def draw_outgoing(base: Image.Image, y: int, time: str,
                  lines: tuple[str, ...]) -> int:
    draw_text(base, (966, y + 18), time, 18, C_MUTED, anchor="rm")
    draw_text(base, (1018, y + 18), "DU", 22, C_GOLD, lilita=True, anchor="rm")
    bubble_x, bubble_y, bubble_width = 322, y + 39, 702
    faces, centers, content_bottom = bubble_line_layout(
        lines, bubble_width - 42, 27)
    bubble_height = content_bottom + 24
    bubble = (bubble_x, bubble_y, bubble_width, bubble_height)
    d2.draw_gradient(base, bubble, (95, 54, 29), (39, 24, 17), 20,
                     outline=(220, 142, 76, 150), outline_width=2)
    draw = ImageDraw.Draw(base, "RGBA")
    for line, face, center in zip(lines, faces, centers):
        draw.text((bubble[0] + 22, bubble[1] + center), line, font=face,
                  fill=(255, 231, 203, 255), anchor="lm")
    return 39 + bubble_height


def draw_emote(base: Image.Image, cx: int, cy: int) -> None:
    draw = ImageDraw.Draw(base, "RGBA")
    draw.ellipse((cx - 15, cy - 15, cx + 15, cy + 15),
                 outline=(255, 218, 170, 255), width=3)
    draw.ellipse((cx - 7, cy - 6, cx - 4, cy - 3), fill=(255, 218, 170, 255))
    draw.ellipse((cx + 4, cy - 6, cx + 7, cy - 3), fill=(255, 218, 170, 255))
    draw.arc((cx - 8, cy - 1, cx + 8, cy + 9), 5, 175,
             fill=(255, 218, 170, 255), width=2)


def draw_input(base: Image.Image) -> None:
    draw_text(base, (52, 1452), "NACHRICHT", 19, C_MUTED, lilita=True)
    box = (42, 1477, 996, 94)
    d2.draw_gradient(base, box, (44, 32, 24), (17, 14, 12), 20,
                     outline=(183, 130, 78, 175), outline_width=2)
    emote = (58, 1492, 64, 64)
    d2.draw_gradient(base, emote, (81, 52, 31), (32, 21, 16), 17,
                     outline=(212, 154, 98, 165), outline_width=2)
    draw_emote(base, emote[0] + emote[2] // 2, emote[1] + emote[3] // 2)
    # The empty field is intentional: no sample or placeholder copy is displayed.
    draw = ImageDraw.Draw(base, "RGBA")
    draw.line((148, 1496, 148, 1552), fill=(181, 132, 83, 96), width=2)
    send = (862, 1490, 160, 68)
    d2.draw_gradient(base, send, (154, 78, 34), (69, 36, 22), 17,
                     outline=(255, 175, 95, 210), outline_width=2)
    draw_text(base, (send[0] + send[2] // 2, send[1] + send[3] // 2),
              "SENDEN", 23, C_TEXT, lilita=True, anchor="mm")


def draw_chat() -> Image.Image:
    base = d2.draw_base()
    draw_conversation(base)
    return base.resize(OUT_SIZE, Image.Resampling.LANCZOS)


def draw_action_icon(base: Image.Image, kind: str, x: int, cy: int,
                     color=(241, 199, 147, 255)) -> None:
    draw = ImageDraw.Draw(base, "RGBA")
    if kind == "profile":
        draw.ellipse((x + 12, cy - 16, x + 34, cy + 6),
                     outline=color, width=3)
        draw.arc((x + 6, cy - 1, x + 40, cy + 26), 195, 345,
                 fill=color, width=3)
    elif kind == "write":
        draw.rounded_rectangle((x + 5, cy - 18, x + 41, cy + 12), 8,
                               outline=color, width=3)
        draw.polygon(((x + 12, cy + 10), (x + 9, cy + 21),
                      (x + 23, cy + 11)), fill=color)
    elif kind == "mute":
        draw.arc((x + 9, cy - 17, x + 37, cy + 16), 180, 360,
                 fill=color, width=3)
        draw.line((x + 9, cy, x + 9, cy + 12), fill=color, width=3)
        draw.line((x + 37, cy, x + 37, cy + 12), fill=color, width=3)
        draw.line((x + 16, cy + 4, x + 30, cy + 4), fill=color, width=3)
        draw.line((x + 10, cy - 16, x + 37, cy + 18), fill=color, width=3)
    elif kind == "report":
        draw.line((x + 11, cy - 20, x + 11, cy + 20), fill=color, width=3)
        draw.polygon(((x + 13, cy - 18), (x + 38, cy - 11),
                      (x + 14, cy - 2)), outline=color, fill=(82, 47, 26, 255))
    elif kind == "translate":
        draw.rounded_rectangle((x + 5, cy - 18, x + 42, cy + 18), 7,
                               outline=color, width=2)
        draw.text((x + 11, cy - 15), "A", font=font(d2.FONT_LILITA, 19), fill=color)
        draw.line((x + 27, cy - 6, x + 36, cy - 6), fill=color, width=2)
        draw.line((x + 27, cy, x + 36, cy), fill=color, width=2)
        draw.line((x + 27, cy + 6, x + 36, cy + 6), fill=color, width=2)
    elif kind == "block":
        points = ((x + 24, cy - 21), (x + 40, cy - 13),
                  (x + 37, cy + 9), (x + 24, cy + 20),
                  (x + 11, cy + 9), (x + 8, cy - 13))
        draw.polygon(points, outline=color, fill=(83, 27, 22, 255))
        draw.line((x + 16, cy, x + 32, cy), fill=color, width=3)


def draw_action_row(base: Image.Image, y: int, label: str, kind: str,
                    *, report: bool = False, danger: bool = False,
                    arrow: bool = False) -> None:
    box = (58, y, 964, 66)
    if danger:
        top, bottom = (105, 41, 31), (47, 20, 17)
        outline = (235, 88, 66, 220)
    elif report:
        top, bottom = (78, 48, 28), (29, 20, 15)
        outline = (224, 149, 85, 185)
    else:
        top, bottom = (51, 38, 29), (20, 15, 12)
        outline = (160, 119, 80, 135)
    d2.draw_gradient(base, box, top, bottom, 15, outline=outline, outline_width=2)
    icon_color = ((255, 196, 180, 255) if danger else
                  (255, 186, 119, 255) if report else (237, 195, 143, 255))
    draw_action_icon(base, kind, box[0] + 15, y + box[3] // 2, icon_color)
    label_color = ((255, 207, 195, 255) if danger else
                   (255, 216, 173, 255) if report else C_TEXT)
    fit_text(base, (box[0] + 77, y + 33), label, box[2] - 150, 25,
             label_color, lilita=True, minimum=18, anchor="lm")
    if arrow:
        draw = ImageDraw.Draw(base, "RGBA")
        cx = box[0] + box[2] - 24
        draw.line((cx - 5, y + 25, cx + 2, y + 33), fill=icon_color, width=3)
        draw.line((cx + 2, y + 33, cx - 5, y + 41), fill=icon_color, width=3)


def draw_reason(base: Image.Image, y: int, label: str, *, selected: bool = False) -> None:
    box = (72, y, 936, 46)
    d2.draw_gradient(base, box, (39, 30, 23), (20, 16, 13), 13,
                     outline=(178, 133, 85, 155), outline_width=1)
    fit_text(base, (box[0] + 20, y + 23), label, 820, 22,
             C_SOFT, minimum=18, anchor="lm")
    draw = ImageDraw.Draw(base, "RGBA")
    cx, cy = box[0] + box[2] - 27, y + box[3] // 2
    draw.ellipse((cx - 12, cy - 12, cx + 12, cy + 12),
                 outline=(231, 179, 111, 230), width=2)
    if selected:
        draw.ellipse((cx - 6, cy - 6, cx + 6, cy + 6),
                     fill=(255, 153, 67, 255))


def draw_sheet_frame(base: Image.Image, x: int, y: int, w: int, h: int) -> ImageDraw.ImageDraw:
    scrim = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(scrim, "RGBA").rounded_rectangle((24, 402, 1056, 1660), 26,
                                                     fill=(7, 6, 6, 188))
    base.alpha_composite(scrim)
    d2.add_clipped_glow(base, (x + 60, y + 2, w - 120, 180),
                        (255, 112, 34, 67), 25, (x, y, w, h))
    d2.paste_9(base, "d2_panel_frame_glut", (x, y, w, h), (72, 72, 72, 72))
    d2.draw_gradient(base, (x + 9, y + 9, w - 18, h - 18),
                     (43, 29, 22), (13, 11, 10), 23,
                     outline=(255, 222, 177, 74), outline_width=1)
    draw = ImageDraw.Draw(base, "RGBA")
    draw.rounded_rectangle((x + 2, y + 2, x + w - 3, y + h - 3), 25,
                           outline=(216, 148, 88, 230), width=3)
    d2.draw_gradient(base, (492, y + 17, 96, 8), (177, 133, 91),
                     (107, 76, 52), 4)
    return draw


def draw_sheet_title(base: Image.Image, draw: ImageDraw.ImageDraw, y: int, title: str) -> None:
    draw_text(base, (62, y + 44), title, 31, (255, 222, 180, 255), lilita=True)
    d2.draw_gradient(base, (976, y + 25, 46, 46), (67, 45, 31), (26, 18, 14), 16,
                     outline=(182, 131, 83, 175), outline_width=1)
    draw.line((990, y + 39, 1008, y + 57), fill=C_SOFT, width=3)
    draw.line((1008, y + 39, 990, y + 57), fill=C_SOFT, width=3)


def draw_profile_card(base: Image.Image, y: int) -> None:
    profile = (58, y, 964, 112)
    d2.draw_gradient(base, profile, (59, 39, 27), (24, 17, 13), 17,
                     outline=(193, 135, 79, 150), outline_width=2)
    draw_avatar(base, (74, y + 10, 92, 92), "ruka")
    draw_text(base, (190, y + 20), "Rabenfeder", 29, C_TEXT, lilita=True)
    draw_guild_tag(base, 366, y + 16, "[MORGENROT]", 194)
    draw_text(base, (190, y + 64), "GILDENMITGLIED · WELTCHAT", 20,
              C_MUTED, lilita=True)


def draw_options_sheet(base: Image.Image) -> None:
    x, y, w, h = 36, 520, 1008, 820
    draw = draw_sheet_frame(base, x, y, w, h)
    draw_sheet_title(base, draw, y, "SPIELEROPTIONEN")
    draw_profile_card(base, y + 96)
    start = y + 226
    draw_action_row(base, start, "PROFIL ANSEHEN", "profile")
    draw_action_row(base, start + 74, "PRIVAT SCHREIBEN", "write")
    draw_action_row(base, start + 148, "ÜBERSETZEN · AUTO FÜR DIESEN SPIELER", "translate")
    draw_action_row(base, start + 222, "STUMMSCHALTEN", "mute")
    draw_action_row(base, start + 296, "MELDEN", "report", report=True, arrow=True)
    draw_action_row(base, start + 370, "BLOCKIEREN", "block", danger=True)


def draw_report_sheet(base: Image.Image) -> None:
    x, y, w, h = 36, 410, 1008, 1050
    draw = draw_sheet_frame(base, x, y, w, h)
    draw_sheet_title(base, draw, y, "Nachricht melden")

    quote = (58, y + 82, 964, 126)
    d2.draw_gradient(base, quote, (59, 39, 27), (24, 17, 13), 17,
                     outline=(193, 135, 79, 150), outline_width=2)
    draw_text(base, (quote[0] + 22, quote[1] + 22), "Gemeldete Nachricht", 20,
              C_MUTED, lilita=True)
    draw_text(base, (quote[0] + 22, quote[1] + 57), "Farnläufer · Weltchat · 09:45",
              20, C_GOLD, lilita=True)
    fit_text(base, (quote[0] + 22, quote[1] + 99),
             "„Le sentier du nord est prêt !“", quote[2] - 44, 23,
             C_TEXT, minimum=19, anchor="lm")

    fit_text(base, (64, y + 230), "Warum möchtest du diese Nachricht melden?", 920, 22,
             (255, 200, 141, 255), lilita=True, minimum=19)
    reasons = (
        "Spam/Werbung",
        "Belästigung/Beleidigung",
        "Hassrede/Diskriminierung",
        "Drohung/Gewalt",
        "Betrug/Kontakt außerhalb des Spiels",
        "Gefahr für Kinder",
        "Möglicherweise rechtswidriger Inhalt",
    )
    for index, reason in enumerate(reasons):
        draw_reason(base, y + 264 + index * 50, reason, selected=index == 0)

    draw_text(base, (64, y + 626), "Erläuterung · optional", 20,
              (255, 200, 141, 255), lilita=True)
    explanation = (72, y + 650, 936, 78)
    d2.draw_gradient(base, explanation, (29, 23, 19), (18, 15, 13), 13,
                     outline=(166, 124, 82, 155), outline_width=2)
    fit_text(base, (explanation[0] + 16, explanation[1] + 27),
             "Warum ist der Inhalt aus deiner Sicht rechtswidrig? (max. 500 Zeichen)",
             explanation[2] - 32, 20, C_MUTED, minimum=17, anchor="lm")

    check = (76, y + 746, 28, 28)
    d2.draw_gradient(base, check, (41, 31, 24), (18, 15, 13), 7,
                     outline=(193, 147, 95, 210), outline_width=2)
    confirmation = (
        "Ich bestätige nach bestem Wissen und in gutem Glauben, dass meine Angaben",
        "richtig und vollständig sind.",
    )
    draw = ImageDraw.Draw(base, "RGBA")
    for index, line in enumerate(confirmation):
        fit_text(base, (116, y + 752 + index * 25), line, 850, 19,
                 C_SOFT, minimum=17, anchor="lm")

    submit = (58, y + 805, 964, 60)
    d2.draw_gradient(base, submit, (168, 87, 37), (87, 41, 23), 17,
                     outline=(255, 178, 104, 220), outline_width=2)
    draw_text(base, (540, submit[1] + submit[3] // 2), "Meldung senden",
              24, C_TEXT, lilita=True, anchor="mm")

    note_lines = (
        "Übermittelt werden deine Spieler-ID, die gemeldete Nachricht mit Zeitpunkt und",
        "die Spieler-ID der gemeldeten Person. Die gemeldete Person erfährt nicht, wer",
        "gemeldet hat. Unsere Moderation prüft die Meldung. Das Ergebnis bekommst du",
        "in deinem Postfach im Spiel. ",
    )
    note_face = font(d2.FONT_BALOO, 17)
    for index, line in enumerate(note_lines):
        draw.text((64, y + 884 + index * 24), line, font=note_face,
                  fill=C_MUTED, anchor="lm")
    link_x = 64 + draw.textlength(note_lines[-1], font=note_face)
    link_text = "Datenschutz"
    draw.text((link_x, y + 884 + 3 * 24), link_text, font=note_face,
              fill=(255, 174, 100, 255), anchor="lm")
    link_width = draw.textlength(link_text, font=note_face)
    draw.line((link_x, y + 884 + 3 * 24 + 9, link_x + link_width,
               y + 884 + 3 * 24 + 9), fill=(255, 174, 100, 255), width=1)


def draw_block_confirm(base: Image.Image) -> None:
    x, y, w, h = 36, 620, 1008, 650
    draw_sheet_frame(base, x, y, w, h)
    draw_text(base, (62, y + 54), "Rabenfeder blockieren?", 31,
              (255, 222, 180, 255), lilita=True)
    body = (
        "Du siehst keine Nachrichten mehr von Rabenfeder, und",
        "Rabenfeder kann dich nicht einladen oder als Freund",
        "hinzufügen. Rabenfeder wird nicht benachrichtigt.",
        "Aufheben kannst du das unter Einstellungen > Blockiert.",
    )
    for index, line in enumerate(body):
        fit_text(base, (64, y + 125 + index * 36), line, 900, 24,
                 C_SOFT, minimum=20, anchor="lm")

    buttons = (
        ("Blockieren", "danger"),
        ("Blockieren und melden", "report"),
        ("Abbrechen", "neutral"),
    )
    for index, (label, style) in enumerate(buttons):
        by = y + 300 + index * 94
        button = (58, by, 964, 72)
        if style == "danger":
            d2.draw_gradient(base, button, (151, 48, 37), (65, 22, 18), 18,
                             outline=(255, 104, 82, 230), outline_width=2)
            color = (255, 220, 210, 255)
        elif style == "report":
            d2.draw_gradient(base, button, (105, 54, 30), (42, 24, 17), 18,
                             outline=(238, 138, 76, 215), outline_width=2)
            color = (255, 218, 181, 255)
        else:
            d2.draw_gradient(base, button, (53, 40, 30), (21, 16, 13), 18,
                             outline=(167, 126, 84, 165), outline_width=2)
            color = C_SOFT
        fit_text(base, (button[0] + button[2] // 2, by + 36), label,
                 button[2] - 44, 25, color, lilita=True, minimum=20, anchor="mm")


def draw_conversation(base: Image.Image) -> None:
    draw_outer_panel(base)
    draw_tabs(base)
    gap = 24
    y = 509
    draw_system_message(base, y)
    y += 56 + gap
    y += draw_incoming(base, y, "Rabenfeder", "[MORGENROT]", "09:42",
                       ("Der Erntepfad ist frei – ich habe die Karren",
                        "schon bereitgestellt."), "ruka") + gap
    y += draw_incoming(base, y, "Moorlicht", "[GLUTFUNKEN]", "09:43",
                       ("Der Bachweg ist frei. Die Körbe stehen bereit.",), "nara",
                       translated_from="Englisch") + gap
    y += draw_incoming(base, y, "Farnläufer", "[GLUTFUNKEN]", "09:45",
                       ("Le sentier du nord est prêt !",), "tala",
                       translate_button=True) + gap
    y += draw_outgoing(base, y, "09:46",
                       ("Danke! Ich bringe die Körbe gleich zur Mühle.",)) + gap
    draw_incoming(base, y, "Kieselpfad", "[MORGENROT]", "09:47",
                  ("Am Nordpfad ist noch Platz für Helfer.",), "kiko")
    draw_input(base)

def draw_options() -> Image.Image:
    base = d2.draw_base()
    draw_conversation(base)
    draw_options_sheet(base)
    return base.resize(OUT_SIZE, Image.Resampling.LANCZOS)


def draw_report() -> Image.Image:
    base = d2.draw_base()
    draw_conversation(base)
    draw_report_sheet(base)
    return base.resize(OUT_SIZE, Image.Resampling.LANCZOS)


def draw_blockieren() -> Image.Image:
    base = d2.draw_base()
    draw_conversation(base)
    draw_block_confirm(base)
    return base.resize(OUT_SIZE, Image.Resampling.LANCZOS)


def main() -> None:
    draw_chat().save(OUT_MAIN, optimize=True)
    draw_options().save(OUT_OPTIONS, optimize=True)
    draw_report().save(OUT_REPORT, optimize=True)
    draw_blockieren().save(OUT_BLOCK, optimize=True)
    for output in (OUT_MAIN, OUT_OPTIONS, OUT_REPORT, OUT_BLOCK):
        with Image.open(output) as rendered:
            if rendered.size != OUT_SIZE:
                raise SystemExit(f"{output.name}: expected {OUT_SIZE}, got {rendered.size}")
        print(f"Wrote {output} · {OUT_SIZE[0]}×{OUT_SIZE[1]}")


if __name__ == "__main__":
    main()
