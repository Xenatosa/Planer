#!/usr/bin/env python3
"""Render D2 summon reveal v13 with perspective, bevelled physical cards."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
V3 = Path("/workspace/handygame-plan/team/art/ui-kit/menus_v3")
HTML_DIR = V3 / "_src/html"
RAW = V3 / "_html_render"
OUT = ROOT
OVERLAY_DIR = HERE / "reveal_assets"
CARD_DIR = OVERLAY_DIR / "cards_v13"
sys.path.insert(0, str(HERE))

import render_vorschau_menu_beschwoeren_reveal_d2_v11 as v11  # noqa: E402
from render_vorschau_menu_beschwoeren_reveal_d2_v10 import (  # noqa: E402
    W,
    H,
    card_back,
    card_face,
    draw_sigil,
    font,
    masked_portrait,
    paste_rotated,
)
from common import render  # noqa: E402
from menu_d2_chrome import apply_chrome  # noqa: E402

BG_CARDS = v11.BG_CARDS
FACE_HEROES = v11.FACE_HEROES


def card_sprite(flat: Image.Image, depth: int = 12) -> Image.Image:
    """Project a card onto a foreshortened face and add a lit, raised card edge."""
    flat = flat.convert("RGBA")
    width, height = flat.size
    margin = 22
    out_w, out_h = width + depth + margin * 2, height + depth + margin * 2

    # The lower edge is closer to the viewer: a narrower top and shortened back edge.
    tl = (margin + round(depth * 0.30), margin + 9)
    tr = (margin + width - round(depth * 0.72), margin + 3)
    br = (margin + width, margin + height - round(depth * 1.10))
    bl = (margin + 1, margin + height - round(depth * 0.74))
    dx, dy = round(depth * 0.62), depth
    tr_back, br_back, bl_back = (tr[0] + dx, tr[1] + dy), (br[0] + dx, br[1] + dy), (bl[0] + dx, bl[1] + dy)

    obj = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(obj, "RGBA")
    # The right and lower bevels catch warm light; the underside stays deep and heavy.
    d.polygon((tr, br, br_back, tr_back), fill=(48, 22, 11, 255), outline=(191, 104, 38, 255))
    d.line((tr, br), fill=(255, 188, 87, 230), width=max(2, depth // 5))
    d.polygon((bl, br, br_back, bl_back), fill=(117, 51, 18, 255), outline=(222, 122, 43, 255))
    d.line((bl, br), fill=(255, 205, 111, 245), width=max(2, depth // 4))
    d.line((bl_back, br_back), fill=(67, 28, 12, 255), width=max(2, depth // 4))
    d.polygon((tl, tr, br, bl), fill=(37, 19, 12, 255), outline=(255, 194, 91, 255))

    # Pillow's perspective transform maps each destination pixel back to the flat art.
    src = ((0, 0), (width - 1, 0), (width - 1, height - 1), (0, height - 1))
    dst = (tl, tr, br, bl)
    equations, values = [], []
    for (sx, sy), (tx, ty) in zip(src, dst):
        equations.append([tx, ty, 1, 0, 0, 0, -sx * tx, -sx * ty])
        values.append(sx)
        equations.append([0, 0, 0, tx, ty, 1, -sy * tx, -sy * ty])
        values.append(sy)
    coeffs = np.linalg.solve(np.asarray(equations, dtype=float), np.asarray(values, dtype=float))
    face = flat.transform(
        (out_w, out_h), Image.Transform.PERSPECTIVE,
        tuple(float(value) for value in coeffs), Image.Resampling.BICUBIC,
    )
    obj.alpha_composite(face)

    # Narrow specular streaks and a clean upper rim sell the glossy comic varnish.
    shine = Image.new("RGBA", obj.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shine, "RGBA")
    sd.line((tl, tr), fill=(255, 241, 194, 235), width=max(2, depth // 4))
    sd.line((tl, bl), fill=(255, 201, 116, 180), width=max(1, depth // 6))
    sd.polygon((
        (margin + width * .63, margin + 15),
        (margin + width * .71, margin + 11),
        (margin + width * .91, margin + height * .34),
        (margin + width * .84, margin + height * .36),
    ), fill=(255, 246, 222, 48))
    shine.putalpha(ImageChops.multiply(shine.getchannel("A"), face.getchannel("A")))
    obj.alpha_composite(shine.filter(ImageFilter.GaussianBlur(1.2)))

    # Give the whole slab a soft cast shadow that remains visible when rotated in HTML.
    shadow_alpha = obj.getchannel("A").filter(ImageFilter.GaussianBlur(9)).point(lambda p: round(p * .72))
    shadow = Image.new("RGBA", obj.size, (4, 2, 1, 0))
    shadow.putalpha(shadow_alpha)
    shadow = ImageChops.offset(shadow, 1, 8)
    final = Image.new("RGBA", obj.size, (0, 0, 0, 0))
    final.alpha_composite(shadow)
    final.alpha_composite(obj)
    return final


def small_card_face(hero: str, size: tuple[int, int], generic: bool = False) -> Image.Image:
    """Keep all 10x reveal labels comfortably inside the shorter card face."""
    scale = 3
    width, height = size[0] * scale, size[1] * scale
    card = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(card, "RGBA")
    d.rounded_rectangle((12, 15, width-12, height-12), radius=26*scale,
                        fill=(26, 18, 14, 255), outline=(133, 68, 25, 255), width=7*scale)
    for y in range(27, height-27):
        t = (y - 27) / max(1, height - 54)
        d.line((27, y, width-27, y),
               fill=(round(68+35*t), round(31+13*t), round(15+4*t), 255))
    d.rounded_rectangle((30, 30, width-30, height-30), radius=21*scale,
                        outline=(255, 199, 100, 255), width=3*scale)
    d.rounded_rectangle((44, 44, width-44, height-44), radius=16*scale,
                        outline=(255, 228, 173, 130), width=2*scale)
    d.polygon(((width//2, 47*scale), (width//2+10*scale, 58*scale),
               (width//2, 69*scale), (width//2-10*scale, 58*scale)),
              fill=(255, 216, 126, 255))
    if generic:
        draw_sigil(d, width//2, 120*scale, 0.9*scale, (255, 192, 89, 255))
        label, sub = "ECHO", "RITUALKARTE"
    else:
        portrait_size = 86*scale
        portrait = masked_portrait(hero, portrait_size)
        px, py = (width-portrait_size)//2, 45*scale
        card.alpha_composite(portrait, (px, py))
        d.ellipse((px-4*scale, py-4*scale, px+portrait_size+4*scale, py+portrait_size+4*scale),
                  outline=(255, 207, 105, 255), width=3*scale)
        label, sub = hero, "HELDENFRAGMENT"
    label_font = font(25*scale, True)
    bounds = d.textbbox((0, 0), label, font=label_font)
    d.text(((width-(bounds[2]-bounds[0]))/2, 169*scale), label, font=label_font,
           fill=(255, 236, 197, 255), stroke_width=2*scale, stroke_fill=(48, 19, 8, 255))
    sub_font = font(11*scale)
    sub_bounds = d.textbbox((0, 0), sub, font=sub_font)
    d.text(((width-(sub_bounds[2]-sub_bounds[0]))/2, 204*scale), sub, font=sub_font,
           fill=(255, 196, 109, 255))
    return card.resize(size, Image.Resampling.LANCZOS)


def save_card_assets() -> dict[str, dict[str, Path]]:
    CARD_DIR.mkdir(parents=True, exist_ok=True)
    assets: dict[str, dict[str, Path]] = {}
    for size_key, size, depth in (("large", (286, 420), 16), ("small", (172, 254), 11)):
        back_path = CARD_DIR / f"v13_card_back_{size_key}.png"
        card_sprite(card_back(size, gleam=True), depth).save(back_path, "PNG", optimize=True)
        assets[size_key] = {"back": back_path}
        for hero in FACE_HEROES:
            flat = (small_card_face(hero if hero != "GENERIC" else "NARA", size, generic=hero == "GENERIC")
                    if size_key == "small" else
                    card_face(hero if hero != "GENERIC" else "NARA", size, generic=hero == "GENERIC"))
            face_path = CARD_DIR / f"v13_card_face_{hero.lower()}_{size_key}.png"
            card_sprite(flat, depth).save(face_path, "PNG", optimize=True)
            assets[size_key][hero] = face_path
    return assets


def draw_portal_shadow(layer: Image.Image, center: tuple[int, int], width: int, height: int):
    shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(shadow, "RGBA")
    cx, cy = center
    d.ellipse((cx - width // 2, cy - height // 2, cx + width // 2, cy + height // 2),
             fill=(9, 4, 2, 142))
    layer.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(max(7, height // 3))))


def draw_empty_rateup(canvas: Image.Image):
    """Match the v12 no-selection state while leaving the v11 reveal layout intact."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    d.rounded_rectangle((48, 378, 1032, 448), radius=20,
                        fill=(28, 17, 11, 255), outline=(186, 124, 58, 230), width=2)
    d.text((540, 413), "RATE-UP WÄHLEN  ·  14 Tage", font=font(28, True), anchor="mm",
           fill=(255, 222, 172, 255), stroke_width=1, stroke_fill=(45, 24, 11, 255))
    d.rounded_rectangle((765, 451, 1045, 559), radius=23,
                        fill=(18, 11, 8, 255), outline=(150, 94, 49, 190), width=2)
    d.text((905, 469), "RATE-UP WÄHLEN", font=font(16, True), anchor="mm",
           fill=(255, 222, 172, 255), stroke_width=1, stroke_fill=(45, 24, 11, 255))
    for x, label in zip((813, 905, 997), ("SLOT 1", "SLOT 2", "SLOT 3")):
        radius = 22
        for start in range(0, 360, 36):
            d.arc((x-radius, 510-radius, x+radius, 510+radius), start + 3, start + 25,
                  fill=(229, 174, 99, 245), width=2)
        d.line((x - 7, 510, x + 7, 510), fill=(255, 221, 166, 255), width=3)
        d.line((x, 503, x, 517), fill=(255, 221, 166, 255), width=3)
        d.text((x, 545), label, font=font(13, True), anchor="mm", fill=(231, 197, 151, 255))
    canvas.alpha_composite(layer)


def draw_frame(canvas: Image.Image, pull: str, state: str, featured: bool):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    v11.draw_orbit(layer, state)
    items = []
    if pull == "1x":
        size = (286, 420) if featured else (300, 440)
        depth = 16 if featured else 17
        hero = "NARA" if featured else "GENERIC"
        art = card_back(size, gleam=(state == "open")) if state == "closed" else card_face(
            hero if hero != "GENERIC" else "NARA", size, generic=hero == "GENERIC"
        )
        items.append((540, 816, -4 if featured else 3, art, depth))
        badge = "1× · EINE KARTE"
    elif pull == "10x":
        size = (172, 254)
        centers = [(150 + i * 130, 828 - 38 * (3 - abs(i - 3))) for i in range(7)]
        angles = (-17, -12, -6, 0, 6, 12, 17)
        for i, ((cx, cy), angle) in enumerate(zip(centers, angles)):
            hero = BG_CARDS[i]
            art = (card_back(size, gleam=(i % 2 == 0)) if state == "closed" else
                   small_card_face(hero if hero != "GENERIC" else "NARA", size, generic=hero == "GENERIC"))
            items.append((cx, cy, angle, art, 11))
        badge = "10× · 7 KARTEN IN DER VORSCHAU"
    else:
        raise ValueError(f"Unknown pull size: {pull}")

    # Contact shadows sit on the portal plane, beneath each card slab.
    for cx, cy, _angle, art, _depth in items:
        draw_portal_shadow(layer, (cx + 6, cy + int(art.height * .37)), int(art.width * .88), 30 if pull == "10x" else 42)
    for cx, cy, angle, art, depth in items:
        paste_rotated(layer, card_sprite(art, depth), (cx, cy), angle)
    v11.draw_badge(layer, badge)
    canvas.alpha_composite(layer)


def empty_rateup_markup() -> str:
    heroes = (
        ("NARA", "Nara", "SSR", "nara"),
        ("OLM", "Olm", "SR", "olm"),
        ("KIKO", "Kiko", "R", "kiko"),
    )
    choice_buttons = "".join(
        f'<button class="hero-choice" type="button" data-id="{key}">'
        f'<img src="file://{V3 / "_assets/portraits_circle" / f"{asset}_circle.png"}" alt="">'
        f'<span>{name}</span><small>{rarity}</small></button>'
        for key, name, rarity, asset in heroes
    )
    slots = "".join(f'<button class="rateup-slot" type="button" data-slot="{i}" aria-label="Rate-up-Slot {i+1} wählen">'
                    f'<span class="slot-plus">+</span><small>SLOT {i+1}</small></button>' for i in range(3))
    return f'''
<div class="rateup-empty">RATE-UP WÄHLEN · 14 Tage</div>
<div class="rateup-slots"><div class="slots-title">RATE-UP WÄHLEN</div>{slots}</div>
<div class="hero-picker" id="hero-picker" aria-hidden="true">
  <div class="picker-sheet" role="dialog" aria-modal="true" aria-label="Held für Rate-up wählen">
    <button class="picker-close" type="button" aria-label="Schließen">×</button>
    <h2>HELD FÜR RATE-UP WÄHLEN</h2>
    <p>Held für Slot <span id="slot-number">1</span> auswählen</p>
    <div class="hero-choices">{choice_buttons}</div>
  </div>
</div>'''


def v13_css() -> str:
    return '''
.av,.selection-tray,.stage .rateup{display:none!important}
.rateup-empty{position:absolute;left:48px;top:378px;width:984px;height:70px;z-index:10;
  display:flex;align-items:center;justify-content:center;border:2px solid #ba7c3a;border-radius:20px;
  background:#1c110b;color:#ffdeac;font:800 28px/1 Baloo,sans-serif;text-shadow:0 1px 0 #2d180b}
.rateup-slots{position:absolute;left:765px;top:451px;width:280px;height:108px;z-index:10;border:2px solid #965e31;
  border-radius:23px;background:#120b08;color:#ffdeac;text-align:center}
.slots-title{height:31px;padding-top:5px;font:800 16px/1 Baloo,sans-serif}
.rateup-slot{position:absolute;top:35px;width:58px;height:66px;border:0;background:transparent;color:#e5c395;cursor:pointer}
.rateup-slot:nth-of-type(1){left:18px}.rateup-slot:nth-of-type(2){left:110px}.rateup-slot:nth-of-type(3){left:202px}
.rateup-slot .slot-plus{display:flex;width:44px;height:44px;margin:0 auto 1px;align-items:center;justify-content:center;
  border:2px dashed #e5ae63;border-radius:50%;font:26px/1 Baloo,sans-serif;color:#ffdda6}
.rateup-slot small{font:800 12px/1 Baloo,sans-serif}
.rateup-slot img{display:block;width:44px;height:44px;margin:0 auto 1px;border:2px solid var(--rarity,#e5ae63);border-radius:50%;object-fit:cover}
.rateup-slot .slot-rarity{position:absolute;left:50%;top:33px;transform:translateX(-50%);padding:0 4px;border-radius:7px;
  background:var(--rarity,#e5ae63);color:#21130a;font:11px/15px Lilita,sans-serif}
.hero-picker{display:none;position:absolute;inset:0;z-index:30;background:rgba(0,0,0,.68);align-items:center;justify-content:center}
.hero-picker.open{display:flex}
.picker-sheet{position:relative;width:972px;height:810px;border:3px solid #c88842;border-radius:36px;background:linear-gradient(#20140d,#190f0a 70%,#21150d);
  box-shadow:0 16px 35px #000c,inset 0 0 0 5px rgba(255,220,165,.06);padding:48px;color:#ffe7be;text-align:center}
.picker-sheet h2{font:36px Lilita,sans-serif;text-shadow:0 2px 0 #3d1c09}
.picker-sheet p{margin-top:12px;color:#c9ae85;font:20px Baloo,sans-serif}
.hero-choices{display:flex;justify-content:center;gap:24px;margin-top:130px}
.hero-choice{width:230px;height:270px;border:2px solid #80542b;border-radius:24px;background:linear-gradient(115deg,#2b1b11,#21150d);color:#ffe7be;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;font:28px Lilita,sans-serif;cursor:pointer}
.hero-choice img{width:126px;height:126px;border:4px solid #c88842;border-radius:50%;object-fit:cover}
.hero-choice small{padding:2px 10px;border-radius:10px;background:#f4b552;color:#21130a;font:17px Lilita,sans-serif}
.picker-close{position:absolute;right:22px;top:18px;width:62px;height:62px;border:2px solid #c78b48;border-radius:50%;background:#160e09;color:#ffebcb;font:38px Lilita,sans-serif;cursor:pointer}
.reveal-card{filter:drop-shadow(0 12px 11px rgba(0,0,0,.64));}
.reveal-card-inner{transform-style:preserve-3d;transition:transform .62s cubic-bezier(.2,.72,.22,1)}
.reveal-card.is-open .reveal-card-inner{transform:perspective(1000px) rotateY(180deg)}
.reveal-face{width:100%;height:100%;object-fit:fill;backface-visibility:hidden;-webkit-backface-visibility:hidden}
.rateup-slot:focus-visible,.hero-choice:focus-visible,.picker-close:focus-visible{outline:4px solid #fff0c7;outline-offset:4px}
'''


def base_html(featured: bool = True) -> str:
    html = v11.base_html(featured)
    html = re.sub(
        r'<span class="sep">·</span>\s*<span class="hero-name"[^>]*>NARA</span>\s*<span class="sep">·</span>',
        '<span class="sep">·</span><span class="hero-name">WÄHLEN</span><span class="sep">·</span>',
        html,
    )
    html = html.replace("</style>", v13_css() + "\n</style>", 1)
    if featured:
        html = html.replace('<div class="infochip">', empty_rateup_markup() + '\n<div class="infochip">', 1)
    return html


def card_markup(assets: dict[str, dict[str, Path]], pull: str) -> str:
    if pull == "1x":
        layout = [(540, 816, -4, "large", "NARA")]
    else:
        layout = [(150 + i * 130, 828 - 38 * (3 - abs(i - 3)), -17 + 5.67 * i,
                   "small", BG_CARDS[i]) for i in range(7)]
    nodes = []
    for index, (x, y, angle, size_key, hero) in enumerate(layout):
        width, height = Image.open(assets[size_key]["back"]).size
        face = assets[size_key].get(hero, assets[size_key]["NARA"])
        z = 20 + index if pull == "10x" else 30
        if pull == "10x" and index == 3:
            z = 30
        nodes.append(
            f'<button class="reveal-card" type="button" aria-label="Karte {index + 1} aufdecken" '
            f'data-card="{index}" style="left:{x}px;top:{y}px;width:{width}px;height:{height}px;'
            f'transform:translate(-50%,-50%) perspective(1000px) rotateX(5deg) rotate({angle}deg);z-index:{z}">'
            f'<span class="reveal-card-inner"><img class="reveal-face back" src="{assets[size_key]["back"].as_uri()}" alt="Verdeckte Karte">'
            f'<img class="reveal-face front" src="{face.as_uri()}" alt="Aufgedeckte Karte"></span></button>'
        )
    return '<div class="reveal-cards" id="reveal-cards">' + "\n".join(nodes) + "</div>"


def interactive_html(assets: dict[str, dict[str, Path]]) -> str:
    html = base_html(True)
    html = html.replace('<div class="reveal-label" id="reveal-label">1× · EINE KARTE</div>',
                        '<div class="reveal-label" id="reveal-label">10× · 7 KARTEN IN DER VORSCHAU</div>')
    html = html.replace('<div class="infochip">', card_markup(assets, "10x") + '\n<div class="infochip">', 1)
    sizes = {key: Image.open(value["back"]).size for key, value in assets.items()}
    asset_json = json.dumps({key: {name: path.as_uri() for name, path in value.items()}
                             for key, value in assets.items()})
    size_json = json.dumps(sizes)
    script = f'''<script>
(() => {{
  const stage=document.getElementById('reveal-cards'), label=document.getElementById('reveal-label');
  const revealAll=document.getElementById('reveal-all'), picker=document.getElementById('hero-picker');
  const assets={asset_json}, sizes={size_json};
  const cards=['NARA','OLM','KIKO','RUKA','GENERIC','OLM','KIKO'];
  const layouts={{'1x':[{{x:540,y:816,angle:-4,size:'large',hero:'NARA'}}],
    '10x':[0,1,2,3,4,5,6].map(i=>({{x:150+i*130,y:828-38*(3-Math.abs(i-3)),angle:-17+5.67*i,size:'small',hero:cards[i]}}))}};
  function setMode(mode){{
    stage.replaceChildren(); layouts[mode].forEach((item,i)=>{{
      const b=document.createElement('button'); b.type='button'; b.className='reveal-card';
      b.setAttribute('aria-label',`Karte ${{i+1}} aufdecken`);
      Object.assign(b.style,{{left:`${{item.x}}px`,top:`${{item.y}}px`,width:`${{sizes[item.size][0]}}px`,height:`${{sizes[item.size][1]}}px`,
        transform:`translate(-50%,-50%) perspective(1000px) rotateX(5deg) rotate(${{item.angle}}deg)`,zIndex:String(mode==='1x'?30:(i===3?30:20+i))}});
      const inner=document.createElement('span');inner.className='reveal-card-inner';
      const back=document.createElement('img');back.className='reveal-face back';back.alt='Verdeckte Karte';back.src=assets[item.size].back;
      const front=document.createElement('img');front.className='reveal-face front';front.alt='Aufgedeckte Karte';front.src=assets[item.size][item.hero]||assets[item.size].NARA;
      inner.append(back,front);b.append(inner);
      b.addEventListener('click',()=>{{b.classList.toggle('is-open');b.setAttribute('aria-label',b.classList.contains('is-open')?`Karte ${{i+1}} wieder verdecken`:`Karte ${{i+1}} aufdecken`)}});
      stage.append(b);
    }});
    label.textContent=mode==='1x'?'1× · EINE KARTE':'10× · 7 KARTEN IN DER VORSCHAU';
  }}
  revealAll.addEventListener('click',()=>stage.querySelectorAll('.reveal-card').forEach(c=>c.classList.add('is-open')));
  document.querySelectorAll('.btn').forEach((b,i)=>{{const mode=i===0?'1x':'10x';b.tabIndex=0;b.setAttribute('role','button');
    b.addEventListener('click',()=>setMode(mode));b.addEventListener('keydown',e=>{{if(e.key==='Enter'||e.key===' '){{e.preventDefault();setMode(mode)}}}})}});
  const slotValues=[null,null,null], slotEls=[...document.querySelectorAll('.rateup-slot')];let activeSlot=0;
  function renderSlots(){{slotEls.forEach((el,i)=>{{el.replaceChildren();const hero=slotValues[i];
    if(hero){{el.style.setProperty('--rarity',hero.color);const img=document.createElement('img');img.src=hero.img;img.alt='';
      const tag=document.createElement('span');tag.className='slot-rarity';tag.textContent=hero.rarity;el.append(img,tag)}}
    else{{el.style.removeProperty('--rarity');const plus=document.createElement('span');plus.className='slot-plus';plus.textContent='+';el.append(plus)}}
    const caption=document.createElement('small');caption.textContent=`SLOT ${{i+1}}`;el.append(caption);
  }})}}
  slotEls.forEach((el,i)=>el.addEventListener('click',()=>{{activeSlot=i;document.getElementById('slot-number').textContent=String(i+1);picker.classList.add('open');picker.setAttribute('aria-hidden','false')}}));
  document.querySelectorAll('.hero-choice').forEach(el=>el.addEventListener('click',()=>{{
    const data={{NARA:{{name:'Nara',rarity:'SSR',color:'#ffb143',img:'file:///workspace/handygame-plan/team/art/ui-kit/menus_v3/_assets/portraits_circle/nara_circle.png'}},
      OLM:{{name:'Olm',rarity:'SR',color:'#51b0ff',img:'file:///workspace/handygame-plan/team/art/ui-kit/menus_v3/_assets/portraits_circle/olm_circle.png'}},
      KIKO:{{name:'Kiko',rarity:'R',color:'#beb8ad',img:'file:///workspace/handygame-plan/team/art/ui-kit/menus_v3/_assets/portraits_circle/kiko_circle.png'}}}};
    slotValues[activeSlot]=data[el.dataset.id];renderSlots();picker.classList.remove('open');picker.setAttribute('aria-hidden','true');
  }}));
  document.querySelector('.picker-close').addEventListener('click',()=>{{picker.classList.remove('open');picker.setAttribute('aria-hidden','true')}});
  picker.addEventListener('click',e=>{{if(e.target===picker){{picker.classList.remove('open');picker.setAttribute('aria-hidden','true')}}}});
  addEventListener('keydown',e=>{{if(e.key==='Escape'){{picker.classList.remove('open');picker.setAttribute('aria-hidden','true')}}}});
  renderSlots();setMode('10x');
}})();
</script>'''
    html = html.replace("</body>", script + "\n</body>")
    return "\n".join(line.rstrip() for line in html.splitlines()) + "\n"


def render_keyframe(html: str, pull: str, state: str, featured: bool):
    page = "featured" if featured else "standard"
    raw = RAW / f"beschwoeren_{page}_v13_{pull}_{state}_raw.png"
    raw.parent.mkdir(parents=True, exist_ok=True)
    render(html, raw)
    composed = Image.open(raw).convert("RGBA")
    draw_frame(composed, pull, state, featured)
    if featured:
        draw_empty_rateup(composed)
    composed.save(raw, "PNG", optimize=True)
    output = OUT / f"vorschau_menu_beschwoeren_d2_{page}_v13_{pull}_{state}.png"
    apply_chrome(raw, output, "dorf")
    print(f"wrote {output} ({Image.open(output).size})")


def main():
    assets = save_card_assets()
    featured = base_html(True)
    for pull in ("1x", "10x"):
        for state in ("closed", "open"):
            render_keyframe(featured, pull, state, True)
    standard = base_html(False)
    for state in ("closed", "open"):
        render_keyframe(standard, "1x", state, False)

    interactive = HTML_DIR / "v3_2_obsidian_beschwoeren_featured_v13_interaktiv.html"
    interactive.write_text(interactive_html(assets), encoding="utf-8")
    print(f"wrote {interactive}")

    for page, pulls in (("featured", ("1x", "10x")), ("standard", ("1x",))):
        for pull in pulls:
            for state in ("closed", "open"):
                source = OUT / f"vorschau_menu_beschwoeren_d2_{page}_v13_{pull}_{state}.png"
                mirror = V3 / f"v3_2_obsidian_beschwoeren_{page}_v13_{pull}_{state}.png"
                Image.open(source).save(mirror, "PNG", optimize=True)


if __name__ == "__main__":
    main()
