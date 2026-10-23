#!/usr/bin/env python3
"""Render v12 Featured hero selection states from the existing v10b screen."""
from __future__ import annotations

import base64
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
V3 = Path("/workspace/handygame-plan/team/art/ui-kit/menus_v3")
FONTS = Path("/workspace/handygame-plan/team/art/ui/fonts")
BASE = ROOT / "vorschau_menu_beschwoeren_d2_featured_v10b_closed.png"
HTML_OUT = V3 / "_src/html/v3_2_obsidian_beschwoeren_featured_v12_interaktiv.html"
OUT_EMPTY = ROOT / "vorschau_menu_beschwoeren_d2_featured_v12_slots_leer.png"
OUT_PICKER = ROOT / "vorschau_menu_beschwoeren_d2_featured_v12_picker.png"
PORTRAIT_DIR = V3 / "_assets/portraits_circle"

W, H = 1080, 1920
INK = (24, 14, 9, 246)
PANEL = (31, 19, 12, 249)
GOLD = (237, 172, 83, 255)
PALE = (255, 231, 190, 255)
MUTED = (204, 174, 133, 255)
RARITY = {
    "NARA": (255, 177, 67, 255),
    "OLM": (81, 176, 255, 255),
    "KIKO": (190, 184, 173, 255),
}
HEROES = (
    {"id": "NARA", "name": "Nara", "rarity": "SSR", "fragments": 12,
     "chance": "50 % vom SSR · ≈ 1 % je Ziehung"},
    {"id": "OLM", "name": "Olm", "rarity": "SR", "fragments": 47,
     "chance": "SR-Pool · 18 % Bannerchance"},
    {"id": "KIKO", "name": "Kiko", "rarity": "R", "fragments": 80,
     "chance": "R-Pool · 80 % Bannerchance"},
)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "LilitaOne-Regular.ttf" if bold else "Baloo2-Variable.ttf"
    result = ImageFont.truetype(str(FONTS / name), size)
    if not bold:
        try:
            result.set_variation_by_axes([800])
        except Exception:
            pass
    return result


def centered(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str,
             fnt: ImageFont.FreeTypeFont, fill, **kwargs) -> None:
    draw.text(xy, text, font=fnt, fill=fill, anchor="mm", **kwargs)


def rounded(draw: ImageDraw.ImageDraw, box, radius: int, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def circle_portrait(hero: str, size: int) -> Image.Image:
    source = Image.open(PORTRAIT_DIR / f"{hero.lower()}_circle.png").convert("RGBA")
    scale = 3
    source = ImageOps.fit(source, (size * scale, size * scale), method=Image.Resampling.LANCZOS)
    mask = Image.new("L", source.size, 0)
    ImageDraw.Draw(mask).ellipse((1, 1, source.width - 2, source.height - 2), fill=255)
    source.putalpha(Image.composite(mask, source.getchannel("A"), mask))
    return source.resize((size, size), Image.Resampling.LANCZOS)


def draw_dashed_slot(draw: ImageDraw.ImageDraw, cx: int, cy: int, label: str):
    radius = 22
    bounds = (cx - radius, cy - radius, cx + radius, cy + radius)
    for start in range(0, 360, 36):
        draw.arc(bounds, start=start + 3, end=start + 25, fill=(229, 174, 99, 245), width=2)
    draw.line((cx - 7, cy, cx + 7, cy), fill=(255, 221, 166, 255), width=3)
    draw.line((cx, cy - 7, cx, cy + 7), fill=(255, 221, 166, 255), width=3)
    centered(draw, (cx, cy + 35), label, font(13, True), (231, 197, 151, 255))


def empty_screen(base: Image.Image) -> Image.Image:
    screen = base.convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    rounded(d, (765, 451, 1045, 559), 23, (18, 11, 8, 255), (150, 94, 49, 190), 2)
    # A quiet prompt above the three tappable empty slots.
    centered(d, (905, 469), "RATE-UP WÄHLEN", font(16, True), (255, 222, 172, 255),
             stroke_width=1, stroke_fill=(45, 24, 11, 255))
    for x, label in zip((813, 905, 997), ("SLOT 1", "SLOT 2", "SLOT 3")):
        draw_dashed_slot(d, x, 510, label)
    screen.alpha_composite(layer)
    return screen


def add_shadow(layer: Image.Image, box, radius=34, blur=18):
    shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(box, radius=radius, fill=(0, 0, 0, 190))
    layer.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(blur)))


def draw_fragment_bar(d: ImageDraw.ImageDraw, box, current: int, color):
    x1, y1, x2, y2 = box
    rounded(d, box, (y2 - y1) // 2, (10, 7, 5, 255), (118, 79, 43, 255), 1)
    inner = (x1 + 2, y1 + 2, x1 + 2 + int((x2 - x1 - 4) * current / 80), y2 - 2)
    if current:
        rounded(d, inner, max(1, (y2 - y1 - 4) // 2), color)


def draw_hero_row(layer: Image.Image, hero: dict, y: int):
    d = ImageDraw.Draw(layer, "RGBA")
    x1, x2, h = 82, 998, 170
    rarity = RARITY[hero["id"]]
    bg = (37, 23, 14, 250)
    edge = (128, 84, 43, 230)
    rounded(d, (x1, y, x2, y + h), 24, bg, edge, 2)
    d.line((x1 + 22, y + 2, x2 - 22, y + 2), fill=(255, 216, 153, 55), width=2)

    # D2 rarity ring and portrait.
    cx, cy, portrait_size = 158, y + 83, 104
    d.ellipse((cx - 57, cy - 57, cx + 57, cy + 57), fill=(16, 11, 8, 255), outline=rarity, width=4)
    portrait = circle_portrait(hero["id"], portrait_size)
    layer.alpha_composite(portrait, (cx - portrait_size // 2, cy - portrait_size // 2))
    rounded(d, (cx - 25, y + 139, cx + 25, y + 163), 10,
            (rarity[0], rarity[1], rarity[2], 255), (25, 15, 8, 255), 2)
    centered(d, (cx, y + 151), hero["rarity"], font(16, True), (28, 17, 10, 255))

    d.text((246, y + 18), hero["name"], font=font(31, True), fill=PALE,
           stroke_width=1, stroke_fill=(51, 25, 10, 255))
    badge_box = (378, y + 22, 448, y + 55)
    rounded(d, badge_box, 13, (rarity[0], rarity[1], rarity[2], 232), (28, 17, 10, 255), 2)
    centered(d, (413, y + 39), hero["rarity"], font(17, True), (27, 17, 10, 255))
    d.text((246, y + 60), hero["chance"], font=font(20), fill=(255, 218, 161, 255),
           stroke_width=1, stroke_fill=(28, 16, 9, 220))
    d.text((246, y + 101), "FRAGMENTE", font=font(16, True), fill=(206, 178, 141, 255))
    d.text((383, y + 97), f'{hero["fragments"]} / 80', font=font(21, True), fill=PALE)
    draw_fragment_bar(d, (246, y + 135, 746, y + 150), hero["fragments"], rarity)

    if hero["fragments"] >= 80:
        # It is a design hint only; interaction in the HTML uses it as a slot choice.
        rounded(d, (780, y + 56, 974, y + 115), 17,
                (255, 166, 54, 255), (255, 220, 148, 255), 2)
        centered(d, (877, y + 75), "HELD", font(17, True), (43, 23, 10, 255))
        centered(d, (877, y + 96), "FREISCHALTEN", font(16, True), (43, 23, 10, 255))
        centered(d, (877, y + 136), "80 / 80 BEREIT", font(15, True), (255, 211, 132, 255))
    else:
        rounded(d, (805, y + 61, 958, y + 111), 18,
                (50, 32, 19, 255), (185, 128, 64, 245), 2)
        centered(d, (881, y + 86), "WÄHLEN", font(20, True), (255, 227, 188, 255))


def picker_screen(empty: Image.Image) -> Image.Image:
    dimmed = Image.blend(empty.convert("RGB"), Image.new("RGB", (W, H), (0, 0, 0)), 0.57)
    screen = dimmed.convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    panel = (54, 518, 1026, 1328)
    add_shadow(layer, panel)
    d = ImageDraw.Draw(layer, "RGBA")
    rounded(d, panel, 36, (30, 19, 13, 252), (200, 136, 68, 255), 3)
    rounded(d, (61, 525, 1019, 1321), 30, (25, 16, 11, 246), (255, 220, 165, 62), 1)

    centered(d, (540, 564), "HELD FÜR RATE-UP WÄHLEN", font(36, True), PALE,
             stroke_width=2, stroke_fill=(61, 29, 11, 255))
    centered(d, (540, 610), "Raten laut GDD · SR/R zeigen Basis-Poolraten", font(19), MUTED)
    d.line((91, 642, 989, 642), fill=(181, 119, 58, 190), width=2)
    d.ellipse((938, 540, 1001, 603), fill=(22, 14, 10, 255), outline=(199, 139, 72, 255), width=2)
    centered(d, (970, 571), "×", font(38, True), PALE)

    for hero, y in zip(HEROES, (660, 844, 1028)):
        draw_hero_row(layer, hero, y)

    rounded(d, (242, 1220, 838, 1281), 22, (49, 32, 19, 255), (169, 113, 56, 255), 2)
    centered(d, (540, 1250), "HELD ANTIPPEN · SLOT 1 FÜLLEN", font(22, True),
             (243, 213, 171, 255))
    centered(d, (540, 1301), "80 Fragmente = Held freischalten", font(18, True),
             (255, 199, 114, 255))
    screen.alpha_composite(layer)
    return screen


def data_uri(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def make_html(empty_path: Path) -> str:
    portraits = {h["id"]: data_uri(PORTRAIT_DIR / f'{h["id"].lower()}_circle.png') for h in HEROES}
    screen_src = os.path.relpath(empty_path, HTML_OUT.parent).replace(os.sep, "/")
    hero_json = "[" + ",".join(
        "{" + ",".join((
            f'"id":"{h["id"]}"', f'"name":"{h["name"]}"',
            f'"rarity":"{h["rarity"]}"', f'"fragments":{h["fragments"]}',
            f'"chance":"{h["chance"]}"', f'"portrait":"{portraits[h["id"]]}"',
        )) + "}"
        for h in HEROES
    ) + "]"
    return f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>Featured Heldenwahl v12 · Interaktiv</title>
<style>
@font-face{{font-family:Lilita;src:url(file:///workspace/handygame-plan/team/art/ui/fonts/LilitaOne-Regular.ttf)}}
@font-face{{font-family:Baloo;src:url(file:///workspace/handygame-plan/team/art/ui/fonts/Baloo2-Variable.ttf);font-weight:400 800}}
*{{box-sizing:border-box}}html,body{{margin:0;width:100%;height:100%;overflow:hidden;background:#080605;color:#f6e5c9;font-family:Baloo,sans-serif}}
#frame{{position:absolute;width:1080px;height:1920px;transform-origin:top left;overflow:hidden}}
#screen{{position:absolute;inset:0;width:1080px;height:1920px}}
.slot{{position:absolute;top:470px;width:82px;height:80px;z-index:3;border:0;background:transparent;border-radius:50%;cursor:pointer}}
.slot:nth-of-type(1){{left:772px}}.slot:nth-of-type(2){{left:864px}}.slot:nth-of-type(3){{left:956px}}
.slot.filled{{top:468px;border-radius:50%;background:#21150d;border:3px solid var(--rarity);box-shadow:0 0 12px var(--rarity)}}
.slot img{{width:60px;height:60px;border-radius:50%;object-fit:cover;margin:4px auto 0}}
.slot .tag{{position:absolute;bottom:-5px;left:50%;transform:translateX(-50%);background:var(--rarity);color:#21150d;border:1px solid #251407;border-radius:8px;padding:0 5px;font:14px Lilita}}
.scrim{{position:absolute;inset:0;background:rgba(0,0,0,.57);z-index:10;display:none}}
.scrim.open{{display:block}}
.sheet{{position:absolute;left:54px;top:518px;width:972px;height:810px;border-radius:36px;border:3px solid #c88842;background:linear-gradient(180deg,#20140d,#190f0a 70%,#21150d);box-shadow:0 16px 35px #000c,inset 0 0 0 5px rgba(255,220,165,.06);padding:24px 27px;}}
.title{{position:absolute;left:150px;top:22px;width:672px;text-align:center;font:36px Lilita;color:#ffe7be;text-shadow:0 2px 0 #3d1c09}}
.subtitle{{position:absolute;top:69px;left:60px;width:852px;text-align:center;color:#c9ae85;font-size:19px}}
.close{{position:absolute;right:21px;top:18px;width:62px;height:62px;border:2px solid #c78b48;border-radius:50%;background:#160e09;color:#ffebcb;font:38px Lilita;cursor:pointer}}
.rows{{position:absolute;left:27px;right:27px;top:142px;display:flex;flex-direction:column;gap:14px}}
.hero{{position:relative;height:170px;width:916px;border:2px solid #80542b;border-radius:24px;background:linear-gradient(115deg,#2b1b11,#21150d);cursor:pointer;color:inherit;text-align:left;padding:0;display:block;touch-action:manipulation}}
.hero.selected{{border-color:#ffcf7a;box-shadow:0 0 0 3px #4b2b11,0 0 20px #ffb54c88,inset 0 0 18px #ffcb731e}}
.portrait{{position:absolute;left:19px;top:25px;width:114px;height:114px;border:4px solid var(--rarity);border-radius:50%;background:#100b08}}
.portrait img{{width:100%;height:100%;border-radius:50%;object-fit:cover}}
.rarity-under{{position:absolute;left:47px;top:130px;padding:1px 10px;border:2px solid #1a1009;border-radius:10px;background:var(--rarity);color:#21150d;font:16px Lilita}}
.name{{position:absolute;left:164px;top:14px;font:31px Lilita;color:#ffe7be;text-shadow:0 1px 0 #381907}}
.rarity-chip{{position:absolute;left:296px;top:21px;padding:2px 12px;border-radius:13px;background:var(--rarity);color:#21150d;font:17px Lilita}}
.chance{{position:absolute;left:164px;top:57px;color:#ffdaa1;font-size:20px}}
.frag-label{{position:absolute;left:164px;top:100px;color:#ceb28d;font:16px Lilita;letter-spacing:.5px}}
.frag-count{{position:absolute;left:301px;top:96px;color:#ffe7be;font:21px Lilita}}
.bar{{position:absolute;left:164px;top:135px;width:500px;height:15px;border:1px solid #76502d;border-radius:9px;background:#0a0705;overflow:hidden}}
.bar i{{display:block;height:100%;border-radius:9px;background:var(--rarity);box-shadow:0 0 8px var(--rarity)}}
.action{{position:absolute;right:17px;top:59px;width:174px;height:51px;border:2px solid #b98143;border-radius:17px;background:#322013;color:#ffe3bc;font:20px Lilita;text-align:center;display:flex;align-items:center;justify-content:center}}
.hero.ready .action{{height:61px;top:53px;background:linear-gradient(#ffd070,#f79b31);border-color:#ffe5a5;color:#321a08;font-size:17px;line-height:1.05}}
.ready-label{{position:absolute;right:17px;top:119px;width:174px;text-align:center;color:#ffd384;font:15px Lilita}}
.footer{{position:absolute;left:188px;top:701px;width:596px;height:61px;border:2px solid #a97138;border-radius:22px;background:#312013;color:#f3d5ab;font:22px Lilita;cursor:pointer}}
.footer:disabled{{opacity:.8;cursor:default}}
.unlock-note{{position:absolute;left:0;right:0;bottom:13px;text-align:center;color:#ffc772;font:18px Lilita}}
.hero:focus-visible,.close:focus-visible,.footer:focus-visible,.slot:focus-visible{{outline:4px solid #fff0c7;outline-offset:3px}}
</style></head><body><main id="frame">
<img id="screen" src="{screen_src}" alt="Featured Beschwören, Rate-up-Slots leer">
<button class="slot" data-slot="0" aria-label="Leeren Rate-up-Slot 1 öffnen"></button><button class="slot" data-slot="1" aria-label="Leeren Rate-up-Slot 2 öffnen"></button><button class="slot" data-slot="2" aria-label="Leeren Rate-up-Slot 3 öffnen"></button>
<div class="scrim" id="scrim"><section class="sheet" role="dialog" aria-modal="true" aria-label="Featured-Helden wählen">
<div class="title" id="sheet-title">HELD FÜR RATE-UP WÄHLEN</div><div class="subtitle">Raten laut GDD · SR/R zeigen Basis-Poolraten</div>
<button class="close" id="close" aria-label="Picker schließen">×</button><div class="rows" id="rows"></div>
<button class="footer" id="choose" disabled>HELD ANTIPPEN · SLOT FÜLLEN</button><div class="unlock-note">80 Fragmente = Held freischalten</div>
</section></div></main>
<script>
(() => {{
 const frame=document.getElementById('frame'), scrim=document.getElementById('scrim'), rows=document.getElementById('rows');
 const heroes={hero_json}; const colors={{NARA:'#ffb143',OLM:'#51b0ff',KIKO:'#beb8ad'}};
 let activeSlot=0, selected=null; const slots=[null,null,null];
 function fit(){{const s=Math.min(innerWidth/1080,innerHeight/1920);frame.style.transform=`scale(${{s}})`;frame.style.left=`${{(innerWidth-1080*s)/2}}px`;frame.style.top=`${{(innerHeight-1920*s)/2}}px`;}}
 addEventListener('resize',fit);fit();
 function makeRows(){{rows.replaceChildren();heroes.forEach(h=>{{
   const b=document.createElement('button');b.type='button';b.className='hero';if(h.fragments>=80)b.classList.add('ready');
   b.style.setProperty('--rarity',colors[h.id]);b.dataset.id=h.id;
   const p=document.createElement('span');p.className='portrait';const img=document.createElement('img');img.src=h.portrait;img.alt='';p.append(img);
   const badge=document.createElement('span');badge.className='rarity-under';badge.textContent=h.rarity;
   const name=document.createElement('span');name.className='name';name.textContent=h.name;
   const chip=document.createElement('span');chip.className='rarity-chip';chip.textContent=h.rarity;
   const chance=document.createElement('span');chance.className='chance';chance.textContent=h.chance;
   const fl=document.createElement('span');fl.className='frag-label';fl.textContent='FRAGMENTE';
   const fc=document.createElement('span');fc.className='frag-count';fc.textContent=`${{h.fragments}} / 80`;
   const bar=document.createElement('span');bar.className='bar';const fill=document.createElement('i');fill.style.width=`${{h.fragments/80*100}}%`;bar.append(fill);
   const action=document.createElement('span');action.className='action';action.textContent=h.fragments>=80?'HELD FREISCHALTEN':'WÄHLEN';
   b.append(p,badge,name,chip,chance,fl,fc,bar,action);
   if(h.fragments>=80){{const ready=document.createElement('span');ready.className='ready-label';ready.textContent='80 / 80 BEREIT';b.append(ready)}}
   b.addEventListener('click',()=>selectHero(h.id));rows.append(b);
 }});}}
 function renderSlots(){{document.querySelectorAll('.slot').forEach((el,i)=>{{const h=slots[i];el.replaceChildren();el.classList.toggle('filled',!!h);if(h){{
   el.style.setProperty('--rarity',colors[h.id]);const img=document.createElement('img');img.src=h.portrait;img.alt=h.name;const tag=document.createElement('span');tag.className='tag';tag.textContent=h.rarity;el.append(img,tag);el.setAttribute('aria-label',`Slot ${{i+1}}: ${{h.name}} ändern`);
  }}else{{el.removeAttribute('style');el.setAttribute('aria-label',`Leeren Rate-up-Slot ${{i+1}} öffnen`)}}}});}}
 function openPicker(index){{activeSlot=index;selected=slots[index]?.id||null;document.getElementById('sheet-title').textContent=`HELD FÜR SLOT ${{index+1}} WÄHLEN`;scrim.classList.add('open');makeRows();updateSelection();}}
 function selectHero(id){{selected=id;updateSelection();}}
 function updateSelection(){{document.querySelectorAll('.hero').forEach(el=>el.classList.toggle('selected',el.dataset.id===selected));const c=document.getElementById('choose');c.disabled=!selected;c.textContent=selected?`${{selected}} IN SLOT ${{activeSlot+1}} ÜBERNEHMEN`:'HELD ANTIPPEN · SLOT FÜLLEN';}}
 document.querySelectorAll('.slot').forEach(el=>el.addEventListener('click',()=>openPicker(Number(el.dataset.slot))));
 document.getElementById('close').addEventListener('click',()=>scrim.classList.remove('open'));
 scrim.addEventListener('click',e=>{{if(e.target===scrim)scrim.classList.remove('open')}});
 document.getElementById('choose').addEventListener('click',()=>{{if(!selected)return;slots[activeSlot]=heroes.find(h=>h.id===selected);renderSlots();scrim.classList.remove('open')}});
 renderSlots();
}})();
</script></body></html>'''


def main():
    if not BASE.exists():
        raise FileNotFoundError(BASE)
    base = Image.open(BASE).convert("RGBA")
    if base.size != (W, H):
        raise ValueError(f"Expected {(W, H)} base image, got {base.size}")
    empty = empty_screen(base)
    empty.convert("RGB").save(OUT_EMPTY, "PNG", optimize=True)
    picker_screen(empty).convert("RGB").save(OUT_PICKER, "PNG", optimize=True)
    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_text(make_html(OUT_EMPTY), encoding="utf-8")
    print(f"wrote {OUT_EMPTY} ({empty.size})")
    print(f"wrote {OUT_PICKER} ({W}, {H})")
    print(f"wrote {HTML_OUT}")


if __name__ == "__main__":
    main()
