#!/usr/bin/env python3
"""Full-screen Mail D2 v6 previews (BG scrim wie Reveal) over a dedicated scriptorium scene."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

ROOT = Path("/workspace/handygame-plan/team/art/hud_d2")
ICONS = ROOT / "icons_v1"
EXP = Path("/workspace/handygame-plan/team/art/ui-kit/menus_v3/vorlage_D2_export")
ASSETS = Path("/workspace/handygame-plan/team/art/ui-kit/menus_v3/_assets")
FONTS = Path("/workspace/handygame-plan/team/art/ui/fonts")
BG = ASSETS / "bg_menu_mail_comic_v1.png"
W, H = 1080, 1920
DOCK_Y = 1708

C_TEXT = (243, 231, 207)
C_MUTED = (194, 177, 145)
C_GLUT = (255, 138, 42)
C_GLUT_TEXT = (255, 217, 168)
C_GREEN = (155, 227, 122)

OUT = ROOT / "vorschau_overlay_mail_d2_v6.png"
OUT_PLAYER = ROOT / "vorschau_overlay_mail_d2_v6_spieler.png"
OUT_READ = ROOT / "vorschau_overlay_mail_d2_v6_gelesen.png"

SYSTEM_MAILS = [
    {
        "id": "S1", "icon": "d2_ico_gratis_login.png", "title": "Vorräte für die Reise",
        "meta": "SYSTEM  ·  HEUTE 09:12", "body": "Ein Gruß aus der Gildenhalle. Diese Vorräte helfen dir auf der nächsten Etappe.",
        "unread": True,
        "rewards": [("d2_ico_holz.png", "Holz", "250", "wood"), ("d2_ico_zeitkristall.png", "Kristall", "20", "crystal")],
    },
    {
        "id": "S2", "icon": "d2_ico_bauen.png", "title": "Wachwechsel am Osttor",
        "meta": "SYSTEM  ·  HEUTE 07:45", "body": "Die Grenzwacht hat ihren Dienst aufgenommen. Der Weg ist wieder frei.",
        "unread": False, "rewards": [],
    },
    {
        "id": "S3", "icon": "d2_ico_arena.png", "title": "Arena-Saison beendet",
        "meta": "SYSTEM  ·  GESTERN 19:20", "body": "Platz 42 erreicht. Deine Saisonübersicht wartet in der Arena.",
        "unread": False, "rewards": [],
    },
]

PLAYER_MAILS = [
    {
        "id": "P1", "icon": "d2_ico_chat.png", "title": "Danke für deinen Einsatz!",
        "meta": "MIRA  ·  VOR 12 MIN.",
        "body": "Wir haben die letzte Expedition geschafft. Danke, dass dein Trupp uns den Rücken freigehalten hat. Morgen brechen wir wieder auf.",
        "unread": True, "rewards": [],
    },
    {
        "id": "P2", "icon": "d2_ico_dock_gilde.png", "title": "Eine neue Route im Archiv",
        "meta": "KIAN  ·  GESTERN 18:36",
        "body": "Die Karte im Stammesarchiv deutet auf einen neuen Weg durch die Berge. Hast du heute Zeit, sie dir anzusehen?",
        "unread": False, "rewards": [],
    },
]


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    fname = {"lilita": "LilitaOne-Regular.ttf", "baloo": "Baloo2-Variable.ttf"}[name]
    f = ImageFont.truetype(str(FONTS / fname), size)
    if name == "baloo":
        try:
            f.set_variation_by_axes([800])
        except Exception:
            pass
    return f


def load(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def paste(canvas: Image.Image, image: Image.Image, xy: tuple[int, int], size=None) -> None:
    if size and image.size != tuple(size):
        image = image.resize(tuple(size), Image.Resampling.LANCZOS)
    canvas.alpha_composite(image.convert("RGBA"), dest=(int(xy[0]), int(xy[1])))


def apply_bg_scrim(canvas: Image.Image) -> None:
    """Reveal-v16-ähnlich: BG ≥62 % abdunkeln, Szene tritt zurück."""
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(scrim, "RGBA")
    for y in range(H):
        if y < int(H * 0.38):
            t = y / max(1, int(H * 0.38) - 1)
            a = int(178 + (158 - 178) * t)
        elif y < int(H * 0.72):
            t = (y - int(H * 0.38)) / max(1, int(H * 0.72) - int(H * 0.38) - 1)
            a = int(158 + (184 - 158) * t)
        else:
            t = (y - int(H * 0.72)) / max(1, H - int(H * 0.72) - 1)
            a = int(184 + (230 - 184) * t)
        d.line([(0, y), (W, y)], fill=(7, 8, 10, a))
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette, "RGBA")
    cx, cy = W // 2, int(H * 0.48)
    max_r = int((W ** 2 + H ** 2) ** 0.5 * 0.55)
    for r in range(max_r, int(max_r * 0.28), -8):
        edge = 1 - (r / max_r)
        a = int(118 * max(0, edge - 0.35) / 0.65)
        if a <= 0:
            continue
        vd.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(3, 4, 6, a), width=8)
    canvas.alpha_composite(scrim)
    canvas.alpha_composite(vignette)


def nine_slice(src: Image.Image, tw: int, th: int, border: int = 40) -> Image.Image:
    sw, sh = src.size
    b = min(border, sw // 3, sh // 3, tw // 3 if tw >= 12 else 1, th // 3 if th >= 12 else 1)
    b = max(b, 1)
    out = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    for src_box, dest in [
        ((0, 0, b, b), (0, 0)), ((sw - b, 0, sw, b), (tw - b, 0)),
        ((0, sh - b, b, sh), (0, th - b)), ((sw - b, sh - b, sw, sh), (tw - b, th - b)),
    ]:
        corner = src.crop(src_box)
        if corner.size != (b, b):
            corner = corner.resize((b, b), Image.Resampling.LANCZOS)
        out.paste(corner, dest)
    for src_box, dest, size in [
        ((b, 0, sw - b, b), (b, 0), (tw - 2 * b, b)),
        ((b, sh - b, sw - b, sh), (b, th - b), (tw - 2 * b, b)),
        ((0, b, b, sh - b), (0, b), (b, th - 2 * b)),
        ((sw - b, b, sw, sh - b), (tw - b, b), (b, th - 2 * b)),
        ((b, b, sw - b, sh - b), (b, b), (tw - 2 * b, th - 2 * b)),
    ]:
        out.paste(src.crop(src_box).resize(size, Image.Resampling.LANCZOS), dest)
    return out


def text_shadow(d: ImageDraw.ImageDraw, xy, value: str, fnt, fill, anchor=None):
    x, y = xy
    d.text((x + 2, y + 3), value, font=fnt, fill=(0, 0, 0, 220), anchor=anchor)
    d.text((x, y), value, font=fnt, fill=fill, anchor=anchor)


def center_text(d: ImageDraw.ImageDraw, box, value: str, fnt, fill, shadow=True):
    x, y, w, h = box
    b = d.textbbox((0, 0), value, font=fnt)
    tx = x + (w - (b[2] - b[0])) / 2 - b[0]
    ty = y + (h - (b[3] - b[1])) / 2 - b[1] - 2
    if shadow:
        text_shadow(d, (tx, ty), value, fnt, fill)
    else:
        d.text((tx, ty), value, font=fnt, fill=fill)


def wrap_text(d: ImageDraw.ImageDraw, value: str, fnt, max_width: int) -> list[str]:
    words, lines, line = value.split(), [], ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if line and d.textlength(candidate, font=fnt) > max_width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def draw_background() -> Image.Image:
    bg = ImageOps.fit(load(BG), (W, H), method=Image.Resampling.LANCZOS, centering=(0.5, 0.52))
    # Keep the writing room visible while giving the cards and controls clear separation.
    apply_bg_scrim(bg)
    return bg


def draw_top(canvas: Image.Image):
    d = ImageDraw.Draw(canvas, "RGBA")
    d.rectangle((0, 0, W, 120), fill=(12, 9, 8, 238))
    d.line((24, 118, 1056, 118), fill=(201, 138, 74, 210), width=2)
    pill = load(EXP / "d2_pill_ressource.png")
    for x, value, icon in [
        (54, "250", "d2_ico_zeitkristall.png"),
        (446, "1,2M", "d2_ico_wissen.png"),
        (746, "1.240", "d2_ico_gold_muschel.png"),
    ]:
        paste(canvas, nine_slice(pill, 280, 80, 42), (x, 24))
        paste(canvas, load(ICONS / icon), (x + 10, 32), (64, 64))
        text_shadow(d, (x + 82, 37), value, font("lilita", 39), C_TEXT)
    paste(canvas, load(EXP / "d2_btn_plus_pill.png"), (346, 24), (80, 80))
    center_text(d, (346, 24, 80, 80), "+", font("lilita", 42), (255, 210, 122))


def draw_dock(canvas: Image.Image):
    d = ImageDraw.Draw(canvas, "RGBA")
    fade = Image.new("RGBA", (W, 40), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fade)
    for yy in range(40):
        fd.line((0, yy, W, yy), fill=(10, 8, 7, round(245 * yy / 39)))
    paste(canvas, fade, (0, DOCK_Y - 40))
    paste(canvas, load(EXP / "d2_dock_bg.png"), (0, DOCK_Y))
    d.line((0, DOCK_Y, W, DOCK_Y), fill=(138, 118, 86, 180), width=2)
    tabs = [("dorf", "Dorf"), ("helden", "Helden"), ("karte", "Karte"), ("armee", "Armee"), ("gilde", "Gilde"), ("inventar", "Inventar")]
    active = load(EXP / "d2_dock_platte_aktiv.png").resize((176, 210), Image.Resampling.LANCZOS)
    label_normal, label_active = font("lilita", 30), font("lilita", 34)
    for i, (key, label) in enumerate(tabs):
        x = i * 180
        if key == "dorf":
            paste(canvas, active, (x + 2, 1678))
            paste(canvas, load(ICONS / f"d2_ico_dock_{key}.png"), (x + 30, 1686), (120, 112))
            center_text(d, (x, 1808, 180, 54), label, label_active, (255, 243, 214))
            paste(canvas, load(EXP / "d2_dock_indikator.png"), (x + 60, 1860), (60, 8))
        else:
            paste(canvas, load(ICONS / f"d2_ico_dock_{key}_inaktiv.png"), (x + 42, 1722), (96, 88))
            center_text(d, (x, 1808, 180, 54), label, label_normal, (191, 174, 142))
    d.rounded_rectangle((390, 1896, 690, 1906), radius=5, fill=(255, 255, 255, 225))


def draw_header(canvas: Image.Image):
    d = ImageDraw.Draw(canvas, "RGBA")
    d.rounded_rectangle((218, 128, 862, 252), radius=28,
                        fill=(14, 10, 8, 210), outline=(166, 116, 65, 225), width=2)
    d.line((254, 131, 826, 131), fill=(255, 222, 175, 72), width=2)
    button = load(EXP / "d2_btn_quadrat_normal.png")
    paste(canvas, nine_slice(button, 112, 112, 30), (20, 132))
    paste(canvas, load(EXP / "d2_ico_zurueck.png"), (44, 156), (64, 64))
    paste(canvas, nine_slice(button, 112, 112, 30), (948, 132))
    paste(canvas, load(EXP / "d2_ico_schliessen.png"), (972, 156), (64, 64))
    text_shadow(d, (540, 137), "POSTFACH", font("lilita", 58), (255, 209, 168), anchor="mt")
    center_text(d, (220, 198, 640, 35), "NACHRICHTEN", font("baloo", 22), C_MUTED, shadow=False)


def draw_tab(canvas: Image.Image, x: int, label: str, icon: str, count: int, active: bool):
    y, w, h = 280, 500, 112
    d = ImageDraw.Draw(canvas, "RGBA")
    kind = "system" if label.lower() == "system" else "player"
    if kind == "system":
        edge = (246, 145, 55, 255) if active else (174, 123, 77, 240)
        fill = (69, 36, 17, 250) if active else (23, 16, 12, 242)
        accent = (255, 147, 56, 255)
    else:
        edge = (91, 214, 221, 255) if active else (62, 144, 155, 235)
        fill = (17, 58, 66, 250) if active else (13, 29, 34, 244)
        accent = (103, 228, 233, 255)
    d.rounded_rectangle((x, y + 4, x + w, y + h + 4), radius=26,
                        fill=(0, 0, 0, 104))
    d.rounded_rectangle((x, y, x + w - 1, y + h - 1), radius=26,
                        fill=fill, outline=edge, width=3 if active else 2)
    d.line((x + 28, y + 4, x + w - 28, y + 4), fill=tuple(accent[:3]) + (132,), width=2)
    if kind == "system":
        # System uses the official ember palette and a sealed-scroll medallion.
        d.ellipse((x + 21, y + 18, x + 96, y + 93), fill=(38, 22, 14, 255), outline=edge, width=3)
        d.ellipse((x + 28, y + 25, x + 89, y + 86), outline=(255, 214, 153, 120), width=1)
        paste(canvas, load(ICONS / icon), (x + 32, y + 27), (52, 52))
        d.polygon([(x + 77, y + 72), (x + 89, y + 86), (x + 74, y + 82)], fill=(224, 106, 38, 255))
    else:
        # Player mail is presented as a chat tab, with a cyan speech-bubble badge and tail.
        d.rounded_rectangle((x + 21, y + 18, x + 96, y + 88), radius=23,
                            fill=(12, 42, 48, 255), outline=edge, width=3)
        d.polygon([(x + 72, y + 80), (x + 91, y + 94), (x + 89, y + 72)], fill=(12, 42, 48, 255))
        paste(canvas, load(ICONS / icon), (x + 28, y + 24), (62, 62))
    d.text((x + 118, y + 28), label.upper(), font=font("lilita", 35),
           fill=C_GLUT_TEXT if kind == "system" and active else accent if kind == "player" and active else C_TEXT)
    if active:
        d.rounded_rectangle((x + 118, y + 78, x + 320, y + 84), radius=3, fill=accent)
    bx, by = x + w - 82, y + 30
    badge = (219, 99, 38, 255) if kind == "system" else (27, 125, 137, 255)
    d.ellipse((bx, by, bx + 52, by + 52), fill=badge if count else (48, 43, 37, 255),
              outline=edge if count else (136, 131, 118, 210), width=2)
    center_text(d, (bx, by, 52, 52), str(count), font("lilita", 28), C_TEXT)
    if active and kind == "system":
        d.rounded_rectangle((x + 28, y + h - 9, x + w - 28, y + h - 3), radius=3, fill=(255, 138, 42, 255))
    elif active:
        d.rounded_rectangle((x + 28, y + h - 9, x + w - 28, y + h - 3), radius=3, fill=(83, 220, 226, 255))


def draw_action_button(canvas: Image.Image, x: int, label: str, icon: str, mode: str):
    y, w, h = 406, 500, 104
    if mode == "primary":
        src, color = load(EXP / "d2_btn_primaer_normal.png"), (255, 244, 222)
    elif mode == "disabled":
        src, color = load(EXP / "d2_btn_sekundaer_gesperrt.png"), (157, 146, 128)
    else:
        src, color = load(EXP / "d2_btn_sekundaer_normal.png"), C_TEXT
    paste(canvas, nine_slice(src, w, h, 42), (x, y))
    if mode == "disabled":
        veil = Image.new("RGBA", (w - 8, h - 8), (15, 13, 12, 80))
        mask = Image.new("L", veil.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, veil.width - 1, veil.height - 1), radius=18, fill=255)
        veil.putalpha(ImageChops.multiply(veil.getchannel("A"), mask))
        paste(canvas, veil, (x + 4, y + 4))
    icon_path = EXP / icon
    if not icon_path.exists():
        icon_path = ICONS / icon
    paste(canvas, load(icon_path), (x + 24, y + 22), (60, 60))
    center_text(ImageDraw.Draw(canvas, "RGBA"), (x + 88, y + 5, w - 104, h - 10), label.upper(), font("lilita", 29), color)


def draw_hint(canvas: Image.Image, done: bool):
    d = ImageDraw.Draw(canvas, "RGBA")
    if done:
        fill, edge, color = (20, 39, 23, 228), (105, 173, 87, 185), C_GREEN
        label = "Beide Tabs gelesen · Belohnungen angenommen · Löschen ist freigeschaltet."
    else:
        fill, edge, color = (30, 20, 15, 235), (143, 103, 65, 185), (232, 205, 168)
        label = "Alles gelesen wirkt auf den aktiven Tab · System-Belohnungen werden dabei angenommen."
    d.rounded_rectangle((30, 524, 1050, 568), radius=18, fill=fill, outline=edge, width=2)
    center_text(d, (42, 524, 996, 44), label, font("baloo", 20), color, shadow=False)


def draw_icon_medallion(canvas: Image.Image, x: int, y: int, size: int, icon: str, unread: bool):
    d = ImageDraw.Draw(canvas, "RGBA")
    edge = (255, 151, 63, 255) if unread else (176, 137, 92, 230)
    d.ellipse((x, y, x + size - 1, y + size - 1), fill=(17, 12, 10, 244), outline=edge, width=4)
    d.ellipse((x + 8, y + 8, x + size - 9, y + size - 9), outline=(255, 224, 177, 88), width=2)
    paste(canvas, load(ICONS / icon), (x + 17, y + 17), (size - 34, size - 34))


def draw_reward_chip(canvas: Image.Image, x: int, y: int, w: int, icon: str, label: str, amount: str, kind: str, claimed: bool):
    fills = {
        "wood": (224, 170, 105, 255),
        "crystal": (171, 222, 247, 255),
        "fragment": (218, 190, 250, 255),
    }
    strokes = {"wood": (255, 221, 164, 255), "crystal": (218, 244, 255, 255), "fragment": (244, 226, 255, 255)}
    text_colors = {"wood": (48, 27, 12, 255), "crystal": (13, 37, 52, 255), "fragment": (39, 20, 57, 255)}
    d = ImageDraw.Draw(canvas, "RGBA")
    d.rounded_rectangle((x, y, x + w, y + 58), radius=20, fill=fills[kind], outline=strokes[kind], width=2)
    paste(canvas, load(ICONS / icon), (x + 8, y + 8), (42, 42))
    d.text((x + 58, y + 15), f"{label}  ×{amount}", font=font("lilita", 21), fill=text_colors[kind])
    if claimed:
        cx = x + w - 23
        d.ellipse((cx - 10, y + 9, cx + 10, y + 29), fill=(42, 99, 45, 255), outline=C_GREEN + (255,), width=2)
        d.line((cx - 5, y + 19, cx - 1, y + 23, cx + 6, y + 14), fill=(231, 255, 218, 255), width=3)


def draw_reward_state(canvas: Image.Image, x: int, y: int, claimed: bool):
    d = ImageDraw.Draw(canvas, "RGBA")
    label = "✓  ANGENOMMEN" if claimed else "BELOHNUNG OFFEN"
    fill = (26, 53, 31, 248) if claimed else (100, 48, 19, 245)
    stroke = (111, 190, 91, 255) if claimed else (239, 133, 50, 255)
    color = C_GREEN if claimed else C_GLUT_TEXT
    d.rounded_rectangle((x, y, x + 214, y + 48), radius=24, fill=fill, outline=stroke, width=2)
    center_text(d, (x + 4, y, 206, 48), label, font("lilita", 18), color)


def draw_card(canvas: Image.Image, box, mail: dict, *, done: bool, roomy: bool = False):
    x, y, w, h = box
    unread = bool(mail["unread"] and not done)
    claimed = bool(done and mail["rewards"])
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer, "RGBA")
    top = (62, 43, 28, 232) if unread else (43, 32, 23, 230)
    bottom = (15, 11, 9, 238)
    for yy in range(h):
        t = yy / max(h - 1, 1)
        col = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3)) + (round(top[3] * (1 - t) + bottom[3] * t),)
        ld.line((0, yy, w, yy), fill=col)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=30, fill=255)
    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), mask))
    paste(canvas, layer, (x, y))
    d = ImageDraw.Draw(canvas, "RGBA")
    d.rounded_rectangle((x, y, x + w - 1, y + h - 1), radius=30,
                        outline=(230, 157, 78, 230) if unread else (150, 112, 72, 195), width=2)
    d.line((x + 36, y + 3, x + w - 36, y + 3), fill=(255, 225, 178, 92), width=2)
    if unread:
        d.rounded_rectangle((x + 6, y + 24, x + 13, y + h - 24), radius=3, fill=(255, 138, 42, 250))

    icon_size = 136 if roomy else 126
    icon_x = x + 28
    icon_y = y + (h - icon_size) // 2
    draw_icon_medallion(canvas, icon_x, icon_y, icon_size, mail["icon"], unread)

    text_x = x + 192
    title_y = y + (34 if roomy else 25)
    title_size = 40 if roomy else 37
    text_shadow(d, (text_x, title_y), mail["title"], font("lilita", title_size), C_TEXT)
    d.text((text_x, title_y + 54), mail["meta"], font=font("baloo", 25 if roomy else 23),
           fill=C_GLUT_TEXT if unread else C_MUTED)
    status = "UNGLESEN" if unread else "GELESEN"
    status_w = 154
    sx, sy = x + w - status_w - 24, title_y + 2
    d.rounded_rectangle((sx, sy, sx + status_w, sy + 42), radius=21,
                        fill=(128, 56, 19, 244) if unread else (26, 42, 27, 240),
                        outline=(255, 166, 80, 255) if unread else (102, 152, 91, 220), width=2)
    center_text(d, (sx, sy, status_w, 42), status, font("lilita", 18), C_GLUT_TEXT if unread else C_GREEN)

    body_font = font("baloo", 28 if roomy else 26)
    body_y = title_y + 101
    max_lines = 3 if roomy else 2
    lines = wrap_text(d, mail["body"], body_font, w - 240)[:max_lines]
    for i, line in enumerate(lines):
        d.text((text_x, body_y + i * 35), line, font=body_font, fill=C_TEXT)

    if mail["rewards"]:
        chip_y = y + h - 76
        chip_x = text_x
        for icon, label, amount, kind in mail["rewards"]:
            chip_w = 218 if label == "Kristall" else 194
            draw_reward_chip(canvas, chip_x, chip_y, chip_w, icon, label, amount, kind, claimed)
            chip_x += chip_w + 14
        draw_reward_state(canvas, x + w - 242, chip_y + 5, claimed)
    elif roomy:
        d.line((text_x, y + h - 74, x + w - 32, y + h - 74), fill=(255, 219, 173, 52), width=1)
        d.text((text_x, y + h - 60), "PERSÖNLICHE NACHRICHT", font=font("lilita", 18), fill=(210, 179, 137))


def draw_player_bubble(canvas: Image.Image, box, mail: dict, *, done: bool, tail_right: bool):
    """Cool-toned chat bubble used only for personal player messages."""
    x, y, w, h = box
    unread = bool(mail["unread"] and not done)
    edge = (92, 219, 228, 255) if unread else (75, 149, 159, 225)
    top = (27, 69, 76, 246) if unread else (24, 48, 53, 242)
    bottom = (10, 23, 27, 248)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer, "RGBA")
    for yy in range(h):
        t = yy / max(h - 1, 1)
        col = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3)) + (round(top[3] * (1 - t) + bottom[3] * t),)
        ld.line((0, yy, w, yy), fill=col)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=42, fill=255)
    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), mask))
    paste(canvas, layer, (x, y))
    d = ImageDraw.Draw(canvas, "RGBA")
    d.rounded_rectangle((x, y, x + w - 1, y + h - 1), radius=42, outline=edge, width=3 if unread else 2)
    # Message-tail silhouette differentiates the player list from official letter cards.
    if tail_right:
        d.polygon([(x + w - 110, y + h - 4), (x + w - 60, y + h + 28), (x + w - 78, y + h - 4)], fill=bottom, outline=edge)
        tail_x = x + w - 82
    else:
        d.polygon([(x + 108, y + h - 4), (x + 60, y + h + 28), (x + 82, y + h - 4)], fill=bottom, outline=edge)
        tail_x = x + 80
    d.line((x + 38, y + 3, x + w - 38, y + 3), fill=(151, 241, 244, 100), width=2)
    d.rounded_rectangle((x + 10, y + 28, x + 16, y + h - 36), radius=3,
                        fill=(97, 224, 229, 255) if unread else (75, 149, 159, 210))

    icon_size = 118
    ax, ay = x + 34, y + 42
    d.ellipse((ax, ay, ax + icon_size, ay + icon_size), fill=(9, 28, 32, 255), outline=edge, width=4)
    d.ellipse((ax + 8, ay + 8, ax + icon_size - 8, ay + icon_size - 8), outline=(180, 248, 248, 100), width=2)
    paste(canvas, load(ICONS / mail["icon"]), (ax + 17, ay + 17), (icon_size - 34, icon_size - 34))

    text_x = x + 184
    title_y = y + 32
    text_shadow(d, (text_x, title_y), mail["title"], font("lilita", 38), C_TEXT)
    meta_color = (131, 233, 236, 255) if unread else (143, 189, 190, 255)
    d.text((text_x, title_y + 55), mail["meta"], font=font("baloo", 24), fill=meta_color)
    status = "UNGLESEN" if unread else "GELESEN"
    sx, sy = x + w - 180, title_y + 2
    d.rounded_rectangle((sx, sy, sx + 150, sy + 40), radius=20,
                        fill=(14, 66, 70, 245) if unread else (24, 43, 42, 240), outline=edge, width=2)
    center_text(d, (sx, sy, 150, 40), status, font("lilita", 17), meta_color)
    body_font = font("baloo", 28)
    body_y = title_y + 104
    for i, line in enumerate(wrap_text(d, mail["body"], body_font, w - 250)[:4]):
        d.text((text_x, body_y + i * 37), line, font=body_font, fill=C_TEXT)
    d.line((text_x, y + h - 74, x + w - 36, y + h - 74), fill=(135, 221, 226, 68), width=1)
    d.text((text_x, y + h - 59), "PERSÖNLICHER CHAT", font=font("lilita", 18), fill=(147, 208, 210, 255))


def unread_count(mails: list[dict], done: bool) -> int:
    return 0 if done else sum(bool(m["unread"]) for m in mails)


def draw_message_content(canvas: Image.Image, tab: str, done: bool):
    sys_count, player_count = unread_count(SYSTEM_MAILS, done), unread_count(PLAYER_MAILS, done)
    d = ImageDraw.Draw(canvas, "RGBA")
    d.rounded_rectangle((22, 268, 1058, 578), radius=28,
                        fill=(13, 9, 8, 184), outline=(164, 112, 63, 225), width=2)
    d.line((54, 271, 1026, 271), fill=(255, 221, 174, 68), width=2)
    draw_tab(canvas, 28, "System", "d2_ico_mail.png", sys_count, tab == "system")
    draw_tab(canvas, 552, "Spieler", "d2_ico_chat.png", player_count, tab == "player")

    current = SYSTEM_MAILS if tab == "system" else PLAYER_MAILS
    current_unread = unread_count(current, done)
    open_rewards = any(bool(m["rewards"]) for m in SYSTEM_MAILS) and not done
    deletion_enabled = sys_count == 0 and player_count == 0 and not open_rewards
    draw_action_button(canvas, 28, "Alles gelesen", "d2_ico_quest_fertig.png", "primary" if current_unread else "disabled")
    draw_action_button(canvas, 552, "Löschen", "d2_ico_schliessen.png", "secondary" if deletion_enabled else "disabled")
    draw_hint(canvas, done)

    if tab == "system":
        boxes = [(28, 594 + i * 344, 1024, 328) for i in range(3)]
        for box, mail in zip(boxes, SYSTEM_MAILS):
            draw_card(canvas, box, mail, done=done)
    else:
        boxes = [(72, 624, 936, 452), (72, 1120, 936, 452)]
        for i, (box, mail) in enumerate(zip(boxes, PLAYER_MAILS)):
            draw_player_bubble(canvas, box, mail, done=done, tail_right=bool(i % 2))


def render(state: str, out: Path):
    canvas = draw_background()
    draw_top(canvas)
    draw_header(canvas)
    if state == "spieler":
        draw_message_content(canvas, "player", done=False)
    elif state == "gelesen":
        draw_message_content(canvas, "system", done=True)
    else:
        draw_message_content(canvas, "system", done=False)
    draw_dock(canvas)
    canvas.convert("RGB").save(out, "PNG", optimize=True)
    print(f"wrote {out} {canvas.size} ({out.stat().st_size} bytes)")


def main():
    render("system", OUT)
    render("spieler", OUT_PLAYER)
    render("gelesen", OUT_READ)


if __name__ == "__main__":
    main()
