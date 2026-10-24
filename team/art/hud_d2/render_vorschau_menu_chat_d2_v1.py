#!/usr/bin/env python3
"""Render the D2 chat overview and player report sheet at 576x1024."""
from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
SRC = HERE / "_src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
import render_vorschau_menu_quests_d2_v2 as d2  # noqa: E402


OUT_MAIN = HERE / "vorschau_menu_chat_d2_v1.png"
OUT_OPTIONS = HERE / "vorschau_menu_chat_d2_v1_optionen.png"
OUT_SIZE = (576, 1024)
PANEL = (14, 304, 1052, 1372)

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

    seal = (x + w - 106, y + 14, 72, 72)
    d2.draw_gradient(base, seal, (80, 45, 24), (22, 15, 11), 21,
                     outline=(221, 157, 86, 165), outline_width=2)
    draw = ImageDraw.Draw(base, "RGBA")
    bx, by = seal[0] + 16, seal[1] + 17
    draw.rounded_rectangle((bx, by, bx + 40, by + 29), 9,
                           fill=(56, 32, 20, 255),
                           outline=(255, 219, 170, 255), width=3)
    draw.polygon(((bx + 12, by + 25), (bx + 8, by + 37), (bx + 24, by + 27)),
                 fill=(56, 32, 20, 255), outline=(255, 219, 170, 255))
    for dot_x in (bx + 12, bx + 20, bx + 28):
        draw.ellipse((dot_x - 2, by + 12, dot_x + 2, by + 16),
                     fill=(255, 219, 170, 255))


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


def draw_avatar(base: Image.Image, box: tuple[int, int, int, int], variant: int = 0) -> None:
    """Draw a small generic player portrait, clipped inside its bronze bezel."""
    x, y, size, _ = box
    palettes = (
        ((71, 43, 28, 255), (28, 18, 14, 255), (99, 55, 30, 255),
         (211, 151, 100, 255), (240, 190, 134, 255)),
        ((42, 63, 61, 255), (22, 34, 34, 255), (56, 79, 74, 255),
         (186, 149, 113, 255), (205, 182, 146, 255)),
        ((80, 47, 29, 255), (34, 23, 18, 255), (125, 69, 36, 255),
         (190, 125, 82, 255), (229, 170, 117, 255)),
    )
    bg, hair, cloth, skin, accent = palettes[variant % len(palettes)]
    inset = 6
    inner_size = size - inset * 2
    portrait = Image.new("RGBA", (inner_size, inner_size), (0, 0, 0, 0))
    d2.draw_gradient(portrait, (0, 0, inner_size, inner_size), bg[:3],
                     (17, 13, 11), 15)
    draw = ImageDraw.Draw(portrait, "RGBA")
    # Shoulders, neck and a simple hooded head stay within the portrait mask.
    draw.ellipse((5, 53, inner_size - 5, inner_size + 18), fill=cloth)
    draw.rounded_rectangle((inner_size // 2 - 10, 43, inner_size // 2 + 10, 68),
                           7, fill=skin)
    draw.ellipse((18, 9, inner_size - 16, 59), fill=skin,
                 outline=(54, 32, 23, 255), width=2)
    draw.polygon(((13, 35), (10, 16), (25, 5), (inner_size - 13, 8),
                  (inner_size - 8, 33), (inner_size - 21, 24),
                  (inner_size // 2, 19), (26, 28)), fill=hair)
    draw.polygon(((15, 30), (22, 25), (inner_size - 19, 26),
                  (inner_size - 11, 34), (inner_size - 17, 42),
                  (inner_size // 2, 35), (20, 42)), fill=accent)
    eye_y = 40
    draw.line((27, eye_y, 34, eye_y - 1), fill=(47, 29, 22, 255), width=2)
    draw.line((inner_size - 34, eye_y - 1, inner_size - 27, eye_y),
              fill=(47, 29, 22, 255), width=2)
    draw.line((inner_size // 2 - 4, 52, inner_size // 2 + 4, 52),
              fill=(123, 73, 48, 220), width=2)
    mask = Image.new("L", portrait.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, inner_size - 1, inner_size - 1),
                                            13, fill=255)
    portrait.putalpha(mask)
    base.alpha_composite(portrait, (x + inset, y + inset))
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
                  time: str, lines: tuple[str, ...], avatar: int = 0) -> None:
    draw_avatar(base, (56, y + 48, 92, 92), avatar)
    draw_text(base, (165, y + 7), name, 25, C_TEXT, lilita=True)
    name_width = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox(
        (0, 0), name, font=font(d2.FONT_LILITA, 25))[2]
    tag_x = 165 + name_width + 12
    tag_width = 190 if guild == "[MORGENROT]" else 194
    draw_guild_tag(base, tag_x, y + 4, guild, tag_width)
    draw_text(base, (1016, y + 19), time, 19, C_MUTED, anchor="rm")
    bubble = (164, y + 48, 860, 104)
    d2.draw_gradient(base, bubble, (57, 40, 29), (24, 18, 14), 20,
                     outline=(168, 121, 76, 115), outline_width=2)
    if len(lines) == 1:
        fit_text(base, (bubble[0] + 23, bubble[1] + 52), lines[0], bubble[2] - 44,
                 28, C_TEXT, minimum=21, anchor="lm")
    else:
        for index, line in enumerate(lines):
            fit_text(base, (bubble[0] + 23, bubble[1] + 29 + index * 38), line,
                     bubble[2] - 44, 27, C_TEXT, minimum=20, anchor="lm")


def draw_outgoing(base: Image.Image, y: int, time: str,
                  lines: tuple[str, ...]) -> None:
    draw_text(base, (966, y + 18), time, 18, C_MUTED, anchor="rm")
    draw_text(base, (1018, y + 18), "DU", 22, C_GOLD, lilita=True, anchor="rm")
    bubble = (322, y + 39, 702, 88)
    d2.draw_gradient(base, bubble, (95, 54, 29), (39, 24, 17), 20,
                     outline=(220, 142, 76, 150), outline_width=2)
    if len(lines) == 1:
        fit_text(base, (bubble[0] + 22, bubble[1] + 44), lines[0], bubble[2] - 42,
                 27, (255, 231, 203, 255), minimum=20, anchor="lm")
    else:
        for index, line in enumerate(lines):
            fit_text(base, (bubble[0] + 22, bubble[1] + 25 + index * 34), line,
                     bubble[2] - 42, 26, (255, 231, 203, 255), minimum=20, anchor="lm")


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
    draw_outer_panel(base)
    draw_tabs(base)
    draw_system_message(base, 509)
    draw_incoming(base, 586, "Rabenfeder", "[MORGENROT]", "09:42",
                  ("Der Erntepfad ist frei – ich habe die Karren", "schon bereitgestellt."), 0)
    draw_outgoing(base, 744, "09:44",
                  ("Danke! Ich bringe die Körbe gleich zur Mühle.",))
    draw_incoming(base, 880, "Moorlicht", "[GLUTFUNKEN]", "09:45",
                  ("Ich sammle am Bach. Der Weg ist heute besonders ruhig.",), 1)
    draw_incoming(base, 1034, "Rabenfeder", "[MORGENROT]", "09:46",
                  ("Wer mithelfen mag: Ich teile gern die Route.",), 0)
    draw_outgoing(base, 1193, "09:47",
                  ("Bin dabei – ich übernehme den Nordpfad.",))
    draw_input(base)
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
    elif kind == "block":
        points = ((x + 24, cy - 21), (x + 40, cy - 13),
                  (x + 37, cy + 9), (x + 24, cy + 20),
                  (x + 11, cy + 9), (x + 8, cy - 13))
        draw.polygon(points, outline=color, fill=(83, 27, 22, 255))
        draw.line((x + 16, cy, x + 32, cy), fill=color, width=3)


def draw_action_row(base: Image.Image, y: int, label: str, kind: str,
                    *, report: bool = False) -> None:
    box = (58, y, 964, 66)
    top, bottom = ((78, 48, 28), (29, 20, 15)) if report else ((51, 38, 29), (20, 15, 12))
    outline = (224, 149, 85, 185) if report else (160, 119, 80, 135)
    d2.draw_gradient(base, box, top, bottom, 15, outline=outline, outline_width=2)
    icon_color = (255, 186, 119, 255) if report else (237, 195, 143, 255)
    draw_action_icon(base, kind, box[0] + 15, y + box[3] // 2, icon_color)
    draw_text(base, (box[0] + 77, y + 33), label, 25,
              (255, 216, 173, 255) if report else C_TEXT, lilita=True, anchor="lm")
    draw = ImageDraw.Draw(base, "RGBA")
    cx = box[0] + box[2] - 24
    draw.line((cx - 5, y + 25, cx + 2, y + 33), fill=icon_color, width=3)
    draw.line((cx + 2, y + 33, cx - 5, y + 41), fill=icon_color, width=3)


def draw_reason(base: Image.Image, y: int, label: str) -> None:
    box = (72, y, 936, 44)
    d2.draw_gradient(base, box, (39, 30, 23), (20, 16, 13), 13,
                     outline=(154, 115, 75, 105), outline_width=1)
    fit_text(base, (box[0] + 20, y + 22), label, 825, 22,
             C_SOFT, minimum=18, anchor="lm")
    draw = ImageDraw.Draw(base, "RGBA")
    cx, cy = box[0] + box[2] - 27, y + box[3] // 2
    draw.ellipse((cx - 12, cy - 12, cx + 12, cy + 12),
                 outline=(196, 154, 104, 205), width=2)


def draw_red_block(base: Image.Image, y: int) -> None:
    box = (58, y, 964, 72)
    d2.draw_gradient(base, box, (105, 41, 31), (47, 20, 17), 17,
                     outline=(235, 88, 66, 220), outline_width=2)
    draw_action_icon(base, "block", box[0] + 15, y + 36, (255, 196, 180, 255))
    draw_text(base, (box[0] + 77, y + 36), "BLOCKIEREN", 26,
              (255, 207, 195, 255), lilita=True, anchor="lm")
    draw = ImageDraw.Draw(base, "RGBA")
    cx = box[0] + box[2] - 24
    draw.line((cx - 5, y + 28, cx + 2, y + 36), fill=(255, 196, 180, 255), width=3)
    draw.line((cx + 2, y + 36, cx - 5, y + 44), fill=(255, 196, 180, 255), width=3)


def draw_options_sheet(base: Image.Image) -> None:
    # Keep the approved top bar and dock bright; dim only the underlying chat area.
    scrim = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(scrim, "RGBA").rounded_rectangle((24, 402, 1056, 1660), 26,
                                                     fill=(7, 6, 6, 188))
    base.alpha_composite(scrim)

    x, y, w, h = 36, 450, 1008, 1206
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

    draw_text(base, (62, 494), "SPIELEROPTIONEN", 31,
              (255, 222, 180, 255), lilita=True)
    # Close affordance sits within its own bezel.
    d2.draw_gradient(base, (976, 475, 46, 46), (67, 45, 31), (26, 18, 14), 16,
                     outline=(182, 131, 83, 175), outline_width=1)
    draw.line((990, 489, 1008, 507), fill=C_SOFT, width=3)
    draw.line((1008, 489, 990, 507), fill=C_SOFT, width=3)

    profile = (58, 538, 964, 114)
    d2.draw_gradient(base, profile, (59, 39, 27), (24, 17, 13), 17,
                     outline=(193, 135, 79, 150), outline_width=2)
    draw_avatar(base, (74, 549, 92, 92), 0)
    draw_text(base, (190, 558), "Rabenfeder", 29, C_TEXT, lilita=True)
    draw_guild_tag(base, 366, 554, "[MORGENROT]", 194)
    draw_text(base, (190, 601), "GILDENMITGLIED · WELTCHAT", 20,
              C_MUTED, lilita=True)

    draw_action_row(base, 662, "PROFIL ANSEHEN", "profile")
    draw_action_row(base, 730, "PRIVAT SCHREIBEN", "write")
    draw_action_row(base, 798, "STUMMSCHALTEN", "mute")
    draw_action_row(base, 866, "MELDEN", "report", report=True)

    draw_text(base, (62, 950), "MELDEGRUND AUSWÄHLEN", 23,
              (255, 200, 141, 255), lilita=True)
    draw_text(base, (1016, 950), "1 AUSWÄHLEN", 17, C_MUTED,
              lilita=True, anchor="ra")
    fit_text(base, (64, 982),
             "Weltchat · Rabenfeder · 09:46 · „Ich teile gern die Route.“",
             940, 21, C_SOFT, minimum=17)
    draw_reason(base, 1009, "Spam oder unerwünschte Werbung")
    draw_reason(base, 1056, "Belästigung oder Einschüchterung")
    draw_reason(base, 1103, "Hassrede oder Diskriminierung")
    draw_reason(base, 1150, "Möglicherweise rechtswidrige Inhalte")

    draw_text(base, (64, 1210), "ERLÄUTERUNG · ERFORDERLICHE BEGRÜNDUNG", 21,
              (255, 200, 141, 255), lilita=True)
    explanation = (72, 1235, 936, 70)
    d2.draw_gradient(base, explanation, (29, 23, 19), (18, 15, 13), 13,
                     outline=(166, 124, 82, 155), outline_width=2)
    # Keep the explanation field blank; it is a real input surface, not sample copy.
    draw.rounded_rectangle((explanation[0] + 11, explanation[1] + 10,
                            explanation[0] + explanation[2] - 12,
                            explanation[1] + explanation[3] - 11),
                           8, outline=(99, 77, 56, 95), width=1)

    check = (76, 1320, 28, 28)
    d2.draw_gradient(base, check, (41, 31, 24), (18, 15, 13), 7,
                     outline=(193, 147, 95, 210), outline_width=2)
    fit_text(base, (116, 1334),
             "Ich bestätige nach bestem Wissen und in gutem Glauben, dass meine Angaben richtig und vollständig sind.",
             860, 21, C_SOFT, minimum=17, anchor="lm")
    fit_text(base, (64, 1365),
             "Dein Name und deine E-Mail-Adresse werden mitübermittelt.",
             940, 19, C_MUTED, minimum=16)

    submit = (58, 1390, 964, 60)
    d2.draw_gradient(base, submit, (55, 48, 39), (26, 23, 20), 16,
                     outline=(143, 130, 108, 115), outline_width=2)
    draw_text(base, (540, submit[1] + submit[3] // 2), "MELDUNG SENDEN",
              22, (175, 163, 141, 255), lilita=True, anchor="mm")

    draw_red_block(base, 1465)
    fit_text(base, (62, 1557),
             "Blockierte Spieler können dir keine Privatnachrichten mehr senden.",
             940, 21, C_MUTED, minimum=17)
    draw_text(base, (540, 1600), "GRUND, BEGRÜNDUNG UND NACHRICHT GEHEN AN DIE MODERATION",
              17, (159, 143, 119, 255), lilita=True, anchor="mm")


def draw_options() -> Image.Image:
    base = d2.draw_base()
    draw_outer_panel(base)
    draw_tabs(base)
    draw_system_message(base, 509)
    draw_incoming(base, 586, "Rabenfeder", "[MORGENROT]", "09:42",
                  ("Der Erntepfad ist frei – ich habe die Karren", "schon bereitgestellt."), 0)
    draw_outgoing(base, 744, "09:44",
                  ("Danke! Ich bringe die Körbe gleich zur Mühle.",))
    draw_incoming(base, 880, "Moorlicht", "[GLUTFUNKEN]", "09:45",
                  ("Ich sammle am Bach. Der Weg ist heute besonders ruhig.",), 1)
    draw_incoming(base, 1034, "Rabenfeder", "[MORGENROT]", "09:46",
                  ("Wer mithelfen mag: Ich teile gern die Route.",), 0)
    draw_outgoing(base, 1193, "09:47",
                  ("Bin dabei – ich übernehme den Nordpfad.",))
    draw_input(base)
    draw_options_sheet(base)
    return base.resize(OUT_SIZE, Image.Resampling.LANCZOS)


def main() -> None:
    draw_chat().save(OUT_MAIN, optimize=True)
    draw_options().save(OUT_OPTIONS, optimize=True)
    print(f"Wrote {OUT_MAIN}")
    print(f"Wrote {OUT_OPTIONS}")


if __name__ == "__main__":
    main()
