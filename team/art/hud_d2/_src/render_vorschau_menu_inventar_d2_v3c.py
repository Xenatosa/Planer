#!/usr/bin/env python3
"""Vorschau Inventar D2 v3 – D2-Sprites + eigener voller Lagerhallen-Hintergrund.
Kein Mock: Grid + Detail-Sheet + Filter-Tabs. Dock→Inventar aktiv.
Top-Pills: Kristall / Wissen / Gold-Muschel (kein Nahrung als Gold).
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

ROOT = Path("/workspace/handygame-plan/team/art/hud_d2")
ICONS = ROOT / "icons_v1"
EXP = Path("/workspace/handygame-plan/team/art/ui-kit/menus_v3/vorlage_D2_export")
FONTS = Path("/workspace/handygame-plan/team/art/ui/fonts")
EQUIP = Path("/workspace/handygame-plan/team/art/ui-kit/menus_v3/_assets/equip")
ASSETS = Path("/workspace/handygame-plan/team/art/ui-kit/menus_v3/_assets")
OUT = ROOT / "vorschau_menu_inventar_d2_v3c.png"

W, H = 1080, 1920
ACTIVE = 5  # Inventar

def font(name, size):
    p = {"lilita": "LilitaOne-Regular.ttf", "baloo": "Baloo2-Variable.ttf"}[name]
    f = ImageFont.truetype(str(FONTS / p), size)
    if name == "baloo":
        try: f.set_variation_by_axes([800])
        except Exception: pass
    return f

def load(p: Path) -> Image.Image:
    return Image.open(p).convert("RGBA")

def paste(base, spr, xy, size=None):
    if size and spr.size != tuple(size):
        spr = spr.resize(tuple(size), Image.Resampling.LANCZOS)
    base.alpha_composite(spr, dest=(int(xy[0]), int(xy[1])))

def nine_slice(spr, tw, th, border=48):
    sw, sh = spr.size
    b = min(border, sw // 3, sh // 3, tw // 3 if tw >= 12 else 1, th // 3 if th >= 12 else 1)
    b = max(b, 1)
    out = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    for src, dst in [
        ((0, 0, b, b), (0, 0)),
        ((sw - b, 0, sw, b), (tw - b, 0)),
        ((0, sh - b, b, sh), (0, th - b)),
        ((sw - b, sh - b, sw, sh), (tw - b, th - b)),
    ]:
        c = spr.crop(src)
        if c.size != (b, b):
            c = c.resize((b, b), Image.Resampling.LANCZOS)
        out.paste(c, dst)
    top = spr.crop((b, 0, sw - b, b)).resize((max(tw - 2 * b, 1), b), Image.Resampling.LANCZOS)
    bot = spr.crop((b, sh - b, sw - b, sh)).resize((max(tw - 2 * b, 1), b), Image.Resampling.LANCZOS)
    left = spr.crop((0, b, b, sh - b)).resize((b, max(th - 2 * b, 1)), Image.Resampling.LANCZOS)
    right = spr.crop((sw - b, b, sw, sh - b)).resize((b, max(th - 2 * b, 1)), Image.Resampling.LANCZOS)
    out.paste(top, (b, 0)); out.paste(bot, (b, th - b))
    out.paste(left, (0, b)); out.paste(right, (tw - b, b))
    mid = spr.crop((b, b, sw - b, sh - b)).resize((max(tw - 2 * b, 1), max(th - 2 * b, 1)), Image.Resampling.LANCZOS)
    out.paste(mid, (b, b))
    return out

def stretch_h(spr, tw, th):
    sw, sh = spr.size
    b = min(64, sw // 3)
    out = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    left = spr.crop((0, 0, b, sh)).resize((b, th), Image.Resampling.LANCZOS)
    right = spr.crop((sw - b, 0, sw, sh)).resize((b, th), Image.Resampling.LANCZOS)
    mid = spr.crop((b, 0, sw - b, sh)).resize((max(tw - 2 * b, 1), th), Image.Resampling.LANCZOS)
    out.paste(left, (0, 0)); out.paste(mid, (b, 0)); out.paste(right, (tw - b, 0))
    return out

def text_shadow(d, xy, text, fnt, fill, shadow=(0, 0, 0)):
    x, y = xy
    d.text((x, y + 3), text, font=fnt, fill=shadow)
    d.text((x, y), text, font=fnt, fill=fill)

def title_grad(canvas, text, cx, y, fnt):
    d = ImageDraw.Draw(canvas)
    bbox = d.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    x = cx - tw // 2
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.text((x, y), text, font=fnt, fill=(255, 120, 30, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(10))
    canvas.alpha_composite(glow)
    d = ImageDraw.Draw(canvas)
    d.text((x, y + 4), text, font=fnt, fill=(0, 0, 0))
    d.text((x, y), text, font=fnt, fill=(255, 209, 168))

def draw_top(canvas):
    pill_src = load(EXP / "d2_pill_ressource.png")
    plus_src = load(EXP / "d2_btn_plus_pill.png")
    fl = font("lilita", 40)
    d = ImageDraw.Draw(canvas)
    pills = [
        (54, 26, "250", ICONS / "d2_ico_zeitkristall.png"),
        (446, 26, "1,2M", ICONS / "d2_ico_wissen.png"),
        (746, 26, "1.240", ICONS / "d2_ico_gold_muschel.png"),
    ]
    for x, y, val, ico_path in pills:
        canvas.alpha_composite(stretch_h(pill_src, 280, 80), dest=(x, y))
        canvas.alpha_composite(load(ico_path).resize((64, 64), Image.Resampling.LANCZOS), dest=(x + 8, y + 8))
        text_shadow(d, (x + 84, y + 18), val, fl, (243, 231, 207))
    canvas.alpha_composite(plus_src.resize((80, 80), Image.Resampling.LANCZOS), dest=(346, 26))
    fp = font("lilita", 44)
    bbox = d.textbbox((0, 0), "+", font=fp)
    tw = bbox[2] - bbox[0]
    d.text((346 + (80 - tw) // 2, 30), "+", font=fp, fill=(255, 210, 122))

def draw_kopf(canvas):
    btn = load(EXP / "d2_btn_quadrat_normal.png")
    paste(canvas, btn, (16, 136), (144, 144))
    paste(canvas, load(EXP / "d2_ico_zurueck.png"), (40, 160), (96, 96))
    paste(canvas, btn, (920, 138), (144, 144))
    paste(canvas, load(EXP / "d2_ico_schliessen.png"), (944, 162), (96, 96))
    title_grad(canvas, "INVENTAR", W // 2, 148, font("lilita", 72))
    d = ImageDraw.Draw(canvas)
    sub = "42 Items · 12/40 Slots frei"
    fb = font("baloo", 28)
    bbox = d.textbbox((0, 0), sub, font=fb)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) // 2, 228), sub, font=fb, fill=(185, 169, 136))

def draw_tabs(canvas):
    labels = ["Alle", "Ressourcen", "Ausrüstung", "Fragmente"]
    d = ImageDraw.Draw(canvas)
    fl = font("lilita", 32)
    for i, lab in enumerate(labels):
        x = 28 + i * 256
        spr = load(EXP / ("d2_tab_aktiv.png" if i == 0 else "d2_tab_inaktiv.png"))
        paste(canvas, spr, (x, 270), (256, 124))
        bbox = d.textbbox((0, 0), lab, font=fl)
        tw = bbox[2] - bbox[0]
        col = (42, 22, 10) if i == 0 else (225, 211, 185)
        if i == 0:
            d.rounded_rectangle((x + 14, 288, x + 242, 380), radius=24,
                                fill=(204, 88, 25, 255), outline=(255, 190, 105, 255), width=2)
            d.line((x + 38, 291, x + 218, 291), fill=(255, 229, 183, 170), width=2)
        text_shadow(d, (x + (256 - tw) // 2, 308), lab, fl, col)

def draw_filter(canvas):
    d = ImageDraw.Draw(canvas)
    paste(canvas, load(EXP / "d2_btn_sekundaer_normal.png"), (28, 410), (120, 120))
    paste(canvas, load(EXP / "d2_ico_suche.png"), (46, 428), (84, 84))
    paste(canvas, nine_slice(load(EXP / "d2_btn_filter_aktiv.png"), 200, 120, 40), (164, 410))
    paste(canvas, nine_slice(load(EXP / "d2_btn_sekundaer_normal.png"), 200, 120, 40), (380, 410))
    paste(canvas, nine_slice(load(EXP / "d2_btn_sekundaer_normal.png"), 200, 120, 40), (596, 410))
    paste(canvas, nine_slice(load(EXP / "d2_btn_sekundaer_normal.png"), 160, 120, 40), (892, 410))
    paste(canvas, load(EXP / "d2_ico_sortieren.png"), (932, 438), (72, 72))
    fb = font("baloo", 26)
    for x, lab, col in [
        (184, "Stacks", (255, 217, 168)),
        (420, "Gear", (243, 231, 207)),
        (620, "Fragmente", (243, 231, 207)),
    ]:
        d.text((x, 450), lab, font=fb, fill=col)

def draw_grid(canvas):
    slots = [
        ("stack", ICONS / "d2_ico_holz.png", "2,4k", "d2_slot_grob.png"),
        ("stack", ICONS / "d2_ico_stein.png", "1,1k", "d2_slot_grob.png"),
        ("stack", ICONS / "d2_ico_nahrung.png", "8,2k", "d2_slot_grob.png"),
        ("stack", ICONS / "d2_ico_uhr.png", "×3", "d2_slot_grob.png"),
        ("gear", EQUIP / "eq_helm.png", "St.4", "d2_slot_geschliffen.png"),
        ("gear", EQUIP / "eq_waffe.png", "", "d2_slot_meister.png"),
        ("gear", EQUIP / "eq_ruestung.png", "St.2", "d2_slot_geschliffen.png"),
        ("gear", EQUIP / "eq_ring1.png", "", "d2_slot_grob.png"),
        ("frag", None, "96", "d2_slot_artefakt.png"),
        ("frag", None, "12", "d2_slot_artefakt.png"),
        ("stack", ICONS / "d2_ico_wissen.png", "×5", "d2_slot_grob.png"),
        ("stack", ICONS / "d2_ico_kiste.png", "×2", "d2_slot_grob.png"),
        ("empty", None, "", "d2_slot_grob.png"),
        ("empty", None, "", "d2_slot_grob.png"),
        ("empty", None, "", "d2_slot_grob.png"),
        ("empty", None, "", "d2_slot_grob.png"),
    ]
    d = ImageDraw.Draw(canvas)
    fb = font("lilita", 22)
    for i, (kind, ico, badge, slot_name) in enumerate(slots):
        col, row = i % 4, i // 4
        x = 28 + col * 148
        y = 546 + row * 176
        paste(canvas, load(EXP / slot_name), (x, y), (140, 140))
        if kind == "empty":
            d.text((x + 52, y + 48), "+", font=font("lilita", 48), fill=(120, 100, 80, 180))
        elif ico and Path(ico).exists():
            paste(canvas, load(ico), (x + 16, y + 16), (108, 108))
        elif kind == "frag":
            # purple placeholder fragment gem
            gem = Image.new("RGBA", (108, 108), (0, 0, 0, 0))
            gd = ImageDraw.Draw(gem)
            gd.polygon([(54, 8), (100, 54), (54, 100), (8, 54)], fill=(181, 123, 255, 220))
            canvas.alpha_composite(gem, dest=(x + 16, y + 16))
        if badge:
            bb = Image.new("RGBA", (70, 32), (0, 0, 0, 0))
            bd = ImageDraw.Draw(bb)
            bd.rounded_rectangle([0, 0, 69, 31], radius=8, fill=(11, 9, 8, 220))
            canvas.alpha_composite(bb, dest=(x + 64, y + 100))
            text_shadow(d, (x + 70, y + 102), badge, fb, (243, 231, 207))
        if i == 4:  # selected helm
            paste(canvas, load(EXP / "d2_slot_auswahl_ring.png"), (x - 6, y - 6), (152, 152))

def draw_detail(canvas):
    panel = nine_slice(load(EXP / "d2_panel_frame.png"), 412, 704, 48)
    canvas.alpha_composite(panel, dest=(640, 546))
    paste(canvas, load(EXP / "d2_slot_geschliffen.png"), (680, 580), (160, 160))
    if (EQUIP / "eq_helm.png").exists():
        paste(canvas, load(EQUIP / "eq_helm.png"), (696, 596), (128, 128))
    d = ImageDraw.Draw(canvas)
    text_shadow(d, (680, 760), "Knochenhelm", font("lilita", 34), (255, 217, 168))
    chip = stretch_h(load(EXP / "d2_chip_seltenheit_sr.png") if (EXP / "d2_chip_seltenheit_sr.png").exists() else load(EXP / "d2_chip.png"), 200, 44)
    canvas.alpha_composite(chip, dest=(680, 820))
    d.text((700, 828), "Geschliffen", font=font("baloo", 22), fill=(214, 199, 166))
    lines = [
        "Helm aus Mammutknochen.",
        "Schützt vor Frost und",
        "Keulenschlägen. E1-Platzhalter.",
    ]
    y = 880
    for line in lines:
        d.text((680, y), line, font=font("baloo", 24), fill=(243, 231, 207))
        y += 36
    text_shadow(d, (680, 1056), "+42 Leben", font("lilita", 28), (155, 227, 122))
    d.text((680, 1096), "Stufe 4 · Cap Feuer−1", font=font("baloo", 22), fill=(185, 169, 136))
    paste(canvas, nine_slice(load(EXP / "d2_btn_primaer_normal.png"), 332, 120, 48), (680, 1160))
    text_shadow(d, (760, 1194), "ANLEGEN", font("lilita", 36), (255, 255, 255), (106, 34, 8))

def draw_cap(canvas):
    panel = nine_slice(load(EXP / "d2_panel_frame_muted.png"), 1024, 80, 32)
    canvas.alpha_composite(panel, dest=(28, 1270))
    d = ImageDraw.Draw(canvas)
    text_shadow(d, (56, 1290), "Belegt 28/40  ·  Ressourcen-Stacks gebündelt", font("lilita", 28), (255, 217, 168))

def draw_dock(canvas):
    dock_bg = load(EXP / "d2_dock_bg.png")
    if dock_bg.size != (1080, 212):
        dock_bg = dock_bg.resize((1080, 212), Image.Resampling.LANCZOS)
    canvas.alpha_composite(dock_bg, dest=(0, 1708))
    tabs = [
        ("dorf", "Dorf", False),
        ("helden", "Helden", False),
        ("karte", "Karte", False),
        ("armee", "Armee", False),
        ("gilde", "Gilde", False),
        ("inventar", "Inventar", True),
    ]
    platte = load(EXP / "d2_dock_platte_aktiv.png").resize((176, 210), Image.Resampling.LANCZOS)
    fl = font("lilita", 30)
    fl_on = font("lilita", 34)
    d = ImageDraw.Draw(canvas)
    for i, (key, label, on) in enumerate(tabs):
        tx = i * 180
        if on:
            canvas.alpha_composite(platte, dest=(tx + 2, 1678))
            paste(canvas, load(ICONS / f"d2_ico_dock_{key}.png"), (tx + 30, 1686), (120, 112))
            bbox = d.textbbox((0, 0), label, font=fl_on)
            tw = bbox[2] - bbox[0]
            text_shadow(d, (tx + (180 - tw) // 2, 1810), label, fl_on, (255, 243, 214))
            ind = load(EXP / "d2_dock_indikator.png").resize((60, 8), Image.Resampling.LANCZOS)
            canvas.alpha_composite(ind, dest=(tx + 60, 1860))
        else:
            paste(canvas, load(ICONS / f"d2_ico_dock_{key}_inaktiv.png"), (tx + 42, 1722), (96, 88))
            bbox = d.textbbox((0, 0), label, font=fl)
            tw = bbox[2] - bbox[0]
            d.text((tx + (180 - tw) // 2, 1814), label, font=fl, fill=(191, 174, 142))
    d.rounded_rectangle([390, 1896, 690, 1906], radius=5, fill=(255, 255, 255, 220))

def apply_bg_scrim(canvas: Image.Image) -> None:
    """Reveal-v16-ähnlich: BG ≥62 % abdunkeln, Szene tritt zurück."""
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(scrim, "RGBA")
    for y in range(H):
        if y < int(H * 0.38):
            t = y / max(1, int(H * 0.38) - 1)
            a = int(196 + (178 - 196) * t)  # ~.77 → .70
        elif y < int(H * 0.72):
            t = (y - int(H * 0.38)) / max(1, int(H * 0.72) - int(H * 0.38) - 1)
            a = int(178 + (200 - 178) * t)  # .70 → .78
        else:
            t = (y - int(H * 0.72)) / max(1, H - int(H * 0.72) - 1)
            a = int(200 + (242 - 200) * t)  # .78 → .95
        d.line([(0, y), (W, y)], fill=(7, 8, 10, a))
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette, "RGBA")
    cx, cy = W // 2, int(H * 0.48)
    max_r = int((W ** 2 + H ** 2) ** 0.5 * 0.55)
    for r in range(max_r, int(max_r * 0.28), -8):
        edge = 1 - (r / max_r)
        a = int(150 * max(0, edge - 0.35) / 0.65)
        if a <= 0:
            continue
        vd.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(3, 4, 6, a), width=8)
    canvas.alpha_composite(scrim)
    canvas.alpha_composite(vignette)

def main():
    bg = ImageOps.fit(load(ASSETS / "bg_menu_inventar_comic_v1.png"), (W, H), method=Image.Resampling.LANCZOS)
    canvas = bg.convert("RGBA")
    apply_bg_scrim(canvas)
    # A compact header surface carries the title, metadata and tabs; the storage
    # scene remains exposed around its edges and in the lower aisle.
    d = ImageDraw.Draw(canvas, "RGBA")
    d.rounded_rectangle((20, 132, 1060, 400), radius=28,
                        fill=(14, 10, 8, 226), outline=(183, 125, 66, 245), width=3)
    d.line((54, 135, 1026, 135), fill=(255, 222, 175, 92), width=2)
    # Solid backing keeps item labels and counters readable over shelves and crates.
    d.rounded_rectangle((18, 522, 638, 1248), radius=24,
                        fill=(13, 10, 8, 190), outline=(155, 111, 67, 235), width=2)
    d.line((44, 525, 612, 525), fill=(255, 220, 170, 72), width=2)
    draw_top(canvas)
    draw_kopf(canvas)
    draw_tabs(canvas)
    draw_filter(canvas)
    draw_grid(canvas)
    draw_detail(canvas)
    draw_cap(canvas)
    # fade into dock
    fade = Image.new("RGBA", (W, 40), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fade)
    for i in range(40):
        fd.line([(0, i), (W, i)], fill=(11, 9, 8, int(200 * i / 39)))
    canvas.alpha_composite(fade, dest=(0, 1636))
    draw_dock(canvas)
    canvas.convert("RGB").save(OUT, "PNG", optimize=True)
    print("wrote", OUT, OUT.stat().st_size)

if __name__ == "__main__":
    main()
