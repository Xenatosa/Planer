#!/usr/bin/env python3
"""Build the v15 summon reveal preview and its static PNG keyframes."""
from __future__ import annotations

import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
HUD = HERE.parent
V3 = HUD.parent / "ui-kit" / "menus_v3"
ASSETS = V3 / "_assets"
HTML_DIR = V3 / "_src" / "html"
OUT = HUD
W, H = 1080, 1920


def uri(path: Path) -> str:
    return path.resolve().as_uri()


def img(path: Path, cls: str = "", alt: str = "") -> str:
    return f'<img class="{cls}" src="{uri(path)}" alt="{alt}">'


def page() -> str:
    font_dir = Path("/workspace/handygame-plan/team/art/ui/fonts")
    portraits = ASSETS / "portraits_circle"
    icons = HUD / "icons_v1"
    featured_bg = ASSETS / "bg_menu_beschwoeren_featured_comic_v2.png"
    standard_bg = ASSETS / "bg_menu_beschwoeren_std_comic_v2.png"
    hero = lambda key: uri(portraits / f"{key.lower()}_circle.png")
    dock = [("dorf", "Dorf"), ("helden", "Helden"), ("karte", "Karte"),
            ("armee", "Armee"), ("gilde", "Gilde"), ("inventar", "Inventar")]

    dock_html = "".join(
        f'<div class="dock-item {"active" if key == "dorf" else ""}">'
        f'{img(icons / f"d2_ico_dock_{key}{"" if key == "dorf" else "_inaktiv"}.png", "dock-icon", label)}'
        f'<span>{label}</span>{"<i></i>" if key == "dorf" else ""}</div>'
        for key, label in dock
    )

    return f'''<!doctype html>
<html lang="de" data-mode="featured" data-pull="10x">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=1080,initial-scale=1">
<title>Beschwören · Reveal v15</title>
<style>
@font-face{{font-family:Lilita;src:url("{uri(font_dir / 'LilitaOne-Regular.ttf')}")}}
@font-face{{font-family:Baloo;src:url("{uri(font_dir / 'Baloo2-Variable.ttf')}");font-weight:400 800}}
@font-face{{font-family:Outfit;src:url("{uri(ASSETS / 'fonts' / 'QGYvz_MVcBeNP4NJtEtq.woff2')}")}}
*{{box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;margin:0;overflow:hidden}}
body{{position:relative;background:#100d0c;color:#f6ebd8;font-family:Baloo,system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
button{{font:inherit;color:inherit}}
.scene{{position:absolute;inset:0;background:center/cover no-repeat url("{uri(featured_bg)}");transition:background-image .2s ease}}
html[data-mode="standard"] .scene{{background-image:url("{uri(standard_bg)}")}}
.scene::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,7,8,.72) 0%,rgba(8,7,8,.2) 26%,rgba(8,7,8,.28) 57%,rgba(8,7,8,.68) 84%,#0b0909 100%);pointer-events:none}}
.ember-wash{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 55%,rgba(255,132,34,.16),transparent 42%),radial-gradient(ellipse at 50% 74%,rgba(255,117,29,.18),transparent 27%);pointer-events:none}}
.topbar{{position:absolute;z-index:10;left:40px;top:18px;width:1000px;height:96px;padding:8px 12px;display:grid;grid-template-columns:280px 80px 280px 280px;gap:8px;align-items:center;background:linear-gradient(180deg,rgba(10,9,9,.94),rgba(15,11,10,.9));border:1px solid rgba(199,150,90,.4);border-radius:34px;box-shadow:0 14px 28px rgba(0,0,0,.36),inset 0 1px 0 rgba(255,225,180,.12)}}
.resource{{height:74px;border-radius:38px;display:flex;align-items:center;gap:10px;padding:5px 18px;background:linear-gradient(180deg,rgba(41,32,27,.96),rgba(20,16,14,.98));border:2px solid #705b43;box-shadow:inset 0 0 0 3px rgba(0,0,0,.36),inset 0 1px 0 rgba(255,231,190,.19)}}
.resource img{{width:55px;height:55px;object-fit:contain;filter:drop-shadow(0 3px 5px rgba(0,0,0,.5))}}
.resource b{{font:40px/1 Lilita;color:#fff1d5;text-shadow:0 3px 0 rgba(0,0,0,.5)}}
.plus{{width:72px;height:72px;border-radius:50%;display:grid;place-items:center;color:#ffd175;font:48px/1 Lilita;background:linear-gradient(#30241c,#17110d);border:2px solid #806747;box-shadow:0 4px 12px #0008,inset 0 1px 0 #fff3}}
.back{{position:absolute;z-index:10;left:28px;top:144px;width:112px;height:112px;border-radius:28px;border:2px solid #876a4c;background:linear-gradient(145deg,#33251d,#171210);box-shadow:inset 0 1px 0 #fff2,0 8px 18px #0008;color:#f3dfbd;font:64px/1 Lilita;cursor:pointer}}
.title{{position:absolute;z-index:10;left:180px;top:138px;width:720px;height:88px;text-align:center;font:64px/88px Lilita;letter-spacing:1px;color:#ffe2b1;text-shadow:0 4px 0 #26140c,0 0 24px rgba(255,143,54,.52)}}
.mode-rail{{position:absolute;z-index:10;left:200px;top:236px;width:680px;height:84px;display:grid;grid-template-columns:1fr 1fr;padding:8px;gap:8px;border:2px solid rgba(191,126,62,.86);border-radius:34px;background:linear-gradient(180deg,rgba(28,22,19,.98),rgba(13,11,10,.98));box-shadow:0 8px 24px #0007,inset 0 1px 0 #fff2}}
.mode-tab{{border:1px solid rgba(177,137,95,.55);border-radius:26px;background:rgba(9,8,8,.72);color:#d8c9b4;font:30px/1 Lilita;cursor:pointer;transition:.18s ease}}
.mode-tab.active{{color:#301708;background:linear-gradient(180deg,#ffc571,#f28a30 58%,#c95116);border:2px solid #ffe0aa;box-shadow:inset 0 2px 0 #fff7,0 0 22px rgba(244,134,42,.4)}}
.ratebar{{position:absolute;z-index:9;left:48px;top:342px;width:984px;height:94px;display:flex;align-items:center;justify-content:space-between;padding:10px 20px 10px 28px;border:1.5px solid rgba(187,126,63,.76);border-radius:24px;background:linear-gradient(100deg,rgba(25,18,15,.94),rgba(40,25,16,.91) 50%,rgba(19,14,12,.92));box-shadow:0 9px 18px #0005,inset 0 1px 0 #fff2}}
.rate-title{{font:26px/1.15 Lilita;color:#f4d3a2;letter-spacing:.3px}}
.rate-slots{{display:flex;gap:12px;align-items:center}}
.slot{{width:70px;text-align:center;color:#cfad7d;opacity:.78}}
.slot .plusmark{{display:grid;place-items:center;width:44px;height:44px;margin:0 auto 2px;border:1px dashed rgba(241,184,103,.76);border-radius:50%;font:29px/1 Lilita;color:#ffcf87}}
.slot small{{font:13px/1 Lilita;letter-spacing:.2px}}
html[data-mode="standard"] .ratebar{{display:none}}
.cards{{position:absolute;z-index:5;left:0;right:0;top:472px;display:grid;grid-template-columns:repeat(5,184px);grid-template-rows:252px 252px;column-gap:18px;row-gap:24px;justify-content:center;align-content:center;perspective:1600px}}
.card{{position:relative;width:184px;height:252px;padding:0;border:0;background:transparent;border-radius:24px;cursor:pointer;touch-action:manipulation;perspective:1200px;filter:drop-shadow(0 14px 12px rgba(0,0,0,.55));transition:filter .18s ease,transform .18s ease}}
.card.type-large{{width:340px;height:490px}}
.card:hover{{filter:drop-shadow(0 16px 18px rgba(255,147,51,.3))}}
.card:focus-visible{{outline:4px solid #ffe3a8;outline-offset:6px}}
.card-inner{{position:absolute;inset:0;border-radius:24px;transform-style:preserve-3d;transition:transform .68s cubic-bezier(.18,.78,.18,1)}}
.card.is-open .card-inner{{transform:rotateY(180deg)}}
.face{{position:absolute;inset:0;overflow:hidden;border-radius:24px;backface-visibility:hidden;-webkit-backface-visibility:hidden}}
.backface{{border:2px solid #e1a45e;background:linear-gradient(135deg,#533018 0%,#171211 19%,#171211 70%,#733c1c 100%);box-shadow:inset 0 0 0 4px rgba(0,0,0,.72),inset 0 0 0 6px rgba(232,176,99,.44),inset 0 2px 0 rgba(255,255,255,.46),0 0 0 1px #120d0a}}
.backface::before{{content:"";position:absolute;inset:13px;border-radius:15px;border:1px solid rgba(246,194,124,.55);background:radial-gradient(circle at 50% 47%,rgba(255,133,43,.42),transparent 34%),linear-gradient(140deg,rgba(255,226,169,.09),transparent 30%,rgba(255,151,54,.07));box-shadow:inset 0 0 22px #0009}}
.backface::after{{content:"";position:absolute;left:50%;top:50%;width:88px;height:88px;transform:translate(-50%,-50%) rotate(45deg);border:2px solid #efbd78;border-radius:22px;box-shadow:0 0 20px rgba(255,158,70,.4),inset 0 0 12px rgba(255,174,84,.22);background:linear-gradient(135deg,rgba(255,190,110,.18),rgba(24,16,13,.2) 48%,rgba(255,134,43,.24))}}
.sigil{{position:absolute;z-index:2;left:50%;top:50%;width:51px;height:51px;transform:translate(-50%,-50%);border:1px solid #ffe0a3;border-radius:50%;display:grid;place-items:center;color:#ffe1a8;font:31px/1 Lilita;text-shadow:0 0 14px #ff9b3d;box-shadow:0 0 20px rgba(255,160,60,.45)}}
.back-word{{position:absolute;z-index:2;left:0;right:0;bottom:28px;text-align:center;color:#e3b981;font:12px/1 Lilita;letter-spacing:2px;text-shadow:0 2px 4px #000}}
.frontface{{transform:rotateY(180deg);border:2px solid var(--rarity);padding:13px 12px 12px;background:linear-gradient(146deg,rgba(80,51,31,.98),rgba(20,16,15,.99) 34%,rgba(27,18,14,.99) 76%,rgba(87,45,20,.98));box-shadow:inset 0 0 0 4px rgba(0,0,0,.62),inset 0 0 0 6px color-mix(in srgb,var(--rarity) 52%,transparent),inset 0 1px 0 rgba(255,255,255,.5),0 0 18px color-mix(in srgb,var(--rarity) 34%,transparent)}}
.frontface::before{{content:"";position:absolute;inset:9px;border:1px solid color-mix(in srgb,var(--rarity) 60%,transparent);border-radius:15px;pointer-events:none}}
.frontface::after{{content:"";position:absolute;top:-20px;right:20px;width:32px;height:160px;transform:rotate(-34deg);background:linear-gradient(90deg,transparent,rgba(255,255,255,.12),transparent);pointer-events:none}}
.card-content{{position:relative;z-index:1;width:100%;height:100%;display:flex;flex-direction:column;align-items:center}}
.kind{{min-height:18px;color:var(--rarity);font:12px/1.1 Lilita;letter-spacing:.7px;text-align:center;text-shadow:0 2px 4px #000}}
.portrait-ring{{width:86px;height:86px;margin:7px auto 5px;padding:4px;border-radius:50%;background:linear-gradient(140deg,#fff0be,var(--rarity) 42%,#57321f 75%,#ffd996);box-shadow:0 0 0 2px rgba(0,0,0,.8),0 0 18px color-mix(in srgb,var(--rarity) 58%,transparent),inset 0 1px 2px #fff9}}
.portrait-ring img{{width:100%;height:100%;border-radius:50%;object-fit:cover;border:2px solid rgba(20,14,12,.92)}}
.hero-name{{margin-top:1px;color:#fff0d0;font:23px/1.08 Lilita;text-shadow:0 2px 0 #25130a,0 0 10px color-mix(in srgb,var(--rarity) 36%,transparent)}}
.rarity-pill{{margin-top:8px;min-width:74px;padding:4px 11px;border-radius:14px;border:1px solid color-mix(in srgb,var(--rarity) 72%,transparent);background:linear-gradient(180deg,color-mix(in srgb,var(--rarity) 26%,#201612),rgba(10,9,9,.92));text-align:center;color:var(--rarity);font:13px/1 Lilita;letter-spacing:.7px;box-shadow:0 3px 8px #0007}}
.fragment .kind{{margin-bottom:0}}
.fragment .portrait-ring{{width:68px;height:68px;margin:5px auto 2px}}
.quantity{{margin-top:0;color:#fff4d8;font:34px/.98 Lilita;letter-spacing:.2px;text-shadow:0 3px 0 #411d0a,0 0 16px color-mix(in srgb,var(--rarity) 62%,transparent)}}
.fragment .counter{{margin-top:3px;min-width:82px;padding:2px 8px;border-radius:11px;border:1px solid rgba(249,208,150,.5);background:rgba(9,8,8,.78);color:#ffdda5;font:14px/1.05 Lilita;letter-spacing:.2px;text-align:center}}
.progress-mini{{width:90px;height:4px;margin-top:4px;border-radius:4px;background:#241a14;overflow:hidden}}
.progress-mini i{{display:block;height:100%;width:var(--progress);background:linear-gradient(90deg,#e86a21,#ffd17e);box-shadow:0 0 8px #ff9a3d}}
.type-large .frontface{{padding:21px 18px 18px}}
.type-large .card-content{{justify-content:center}}
.type-large .kind{{font-size:16px}}
.type-large .portrait-ring{{width:148px;height:148px;margin:12px auto 10px;padding:6px}}
.type-large .hero-name{{font-size:37px}}
.type-large .rarity-pill{{margin-top:14px;min-width:112px;font-size:19px;padding:7px 14px}}
.type-large.fragment .portrait-ring{{width:122px;height:122px;margin:10px auto 7px}}
.type-large .quantity{{font-size:56px;margin-top:3px}}
.type-large.fragment .counter{{font-size:21px;padding:5px 13px;margin-top:8px}}
.type-large .progress-mini{{width:148px;height:7px;margin-top:7px}}
.label-chip{{position:absolute;z-index:9;left:310px;top:1034px;width:460px;height:55px;display:flex;align-items:center;justify-content:center;border:1px solid rgba(227,171,103,.77);border-radius:28px;background:linear-gradient(180deg,rgba(35,23,16,.95),rgba(17,12,10,.97));color:#ffe1b1;font:23px/1 Lilita;letter-spacing:.5px;box-shadow:0 5px 13px #0007,inset 0 1px 0 #fff2;text-shadow:0 2px 0 #1c0e07}}
.all-open{{position:absolute;z-index:10;left:320px;top:1104px;width:440px;height:70px;border:1px solid #ffdb9f;border-radius:24px;background:linear-gradient(180deg,#8d582c,#583218 53%,#372014);box-shadow:inset 0 2px 0 #fff5,0 5px 0 #1c110b,0 0 24px rgba(255,157,63,.22);color:#fff1d7;font:27px/1 Lilita;cursor:pointer}}
.all-open:active{{transform:translateY(2px)}}
.all-open:focus-visible,.purchase:focus-visible,.mode-tab:focus-visible{{outline:4px solid #ffe8bd;outline-offset:4px}}
.pity{{position:absolute;z-index:8;left:90px;top:1200px;width:900px;height:66px;display:flex;align-items:center;gap:18px;padding:0 22px;border:1px solid rgba(209,148,82,.7);border-radius:34px;background:rgba(18,13,11,.92);box-shadow:0 6px 15px #0007}}
.pity .caption{{width:200px;color:#efcf9e;font:18px/1 Lilita;letter-spacing:.4px;white-space:nowrap}}
.pity-bar{{height:15px;flex:1;overflow:hidden;border-radius:10px;border:1px solid #876647;background:#090808}}
.pity-bar i{{display:block;width:41.25%;height:100%;background:linear-gradient(90deg,#da5b1c,#ffbe69);box-shadow:0 0 12px #ff983d}}
.pity b{{color:#ffe4bd;font:23px/1 Lilita;white-space:nowrap}}
.purchase-row{{position:absolute;z-index:8;left:38px;top:1310px;width:1004px;height:142px;display:grid;grid-template-columns:1fr 1fr;gap:28px}}
.purchase{{height:132px;border:2px solid #ffe0ae;border-radius:26px;background:linear-gradient(180deg,#ffbf69 0%,#f57b24 56%,#c64d13 100%);box-shadow:inset 0 4px 0 rgba(255,255,255,.46),inset 0 -7px 0 rgba(80,32,10,.3),0 6px 0 #4a260f,0 0 24px rgba(255,126,39,.36);color:#fff8e9;text-shadow:0 3px 0 #6d300f;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px}}
.purchase .main{{display:flex;align-items:center;gap:10px;font:32px/1 Lilita}}
.purchase .main img{{width:37px;height:37px;object-fit:contain;filter:drop-shadow(0 2px 3px #55230d)}}
.purchase small{{font:17px/1 Baloo;color:#fff2de;text-shadow:0 2px 0 #60260e}}
.infochip{{position:absolute;z-index:8;left:320px;top:1480px;width:440px;height:68px;display:flex;align-items:center;justify-content:center;gap:12px;border:1px solid rgba(183,126,70,.75);border-radius:36px;background:rgba(17,12,10,.93);color:#ead5b4;font:22px/1 Lilita;box-shadow:0 6px 15px #0007}}
.infochip img{{width:38px;height:38px;object-fit:contain}}
.dock{{position:absolute;z-index:12;left:0;right:0;top:1680px;height:240px;border-top:1px solid rgba(236,211,174,.28);background:linear-gradient(180deg,rgba(16,13,12,.9),rgba(8,8,9,.99));display:grid;grid-template-columns:repeat(6,1fr);padding-top:0;box-shadow:0 -12px 34px rgba(0,0,0,.36)}}
.dock-item{{position:relative;display:flex;flex-direction:column;align-items:center;padding-top:27px;color:#b8aa94;font:28px/1 Lilita;text-shadow:0 2px 0 #000}}
.dock-item .dock-icon{{width:91px;height:82px;object-fit:contain;filter:drop-shadow(0 5px 7px rgba(0,0,0,.5));opacity:.82}}
.dock-item.active{{height:205px;margin-top:-25px;padding-top:20px;border:2px solid #d8782d;border-radius:30px;background:linear-gradient(180deg,rgba(174,91,34,.74),rgba(63,35,22,.82));color:#fff0d4;box-shadow:inset 0 1px 0 #ffdc9b66,0 0 20px rgba(230,119,43,.25)}}
.dock-item.active .dock-icon{{width:111px;height:96px;opacity:1}}
.dock-item i{{position:absolute;bottom:20px;width:58px;height:7px;border-radius:5px;background:#ff9c4b}}
.count-toast{{position:absolute;right:28px;top:442px;z-index:10;display:none;padding:6px 12px;border:1px solid #dbab70;border-radius:16px;background:rgba(17,11,9,.92);color:#ffe3b7;font:15px/1 Lilita}}
html[data-mode="standard"] .count-toast{{top:442px}}
@media (prefers-reduced-motion:reduce){{.card-inner,.mode-tab{{transition:none}}}}
</style>
</head>
<body>
<div class="scene"></div><div class="ember-wash"></div>
<div class="topbar">
  <div class="resource">{img(HUD / 'icons_v1' / 'd2_ico_zeitkristall.png', '', 'Zeitkristalle')}<b>250</b></div>
  <div class="plus">+</div>
  <div class="resource">{img(HUD / 'icons_v1' / 'd2_ico_wissen.png', '', 'Wissen')}<b>1,2M</b></div>
  <div class="resource">{img(HUD / 'icons_v1' / 'd2_ico_gold_muschel.png', '', 'Gold')}<b>12,4K</b></div>
</div>
<button class="back" aria-label="Zurück">‹</button>
<div class="title">BESCHWÖREN</div>
<div class="mode-rail" role="tablist" aria-label="Beschwörungsart">
  <button class="mode-tab" data-mode-button="standard" role="tab" aria-selected="false">Standard</button>
  <button class="mode-tab active" data-mode-button="featured" role="tab" aria-selected="true">Featured</button>
</div>
<div class="ratebar" aria-label="Rate-up-Auswahl">
  <div class="rate-title">RATE-UP WÄHLEN · 14 Tage</div>
  <div class="rate-slots">
    <div class="slot"><span class="plusmark">+</span><small>SLOT 1</small></div>
    <div class="slot"><span class="plusmark">+</span><small>SLOT 2</small></div>
    <div class="slot"><span class="plusmark">+</span><small>SLOT 3</small></div>
  </div>
</div>
<div class="cards" id="cards" aria-label="Beschwörungskarten"></div>
<div class="label-chip" id="label-chip">10× · 10 KARTEN</div>
<button class="all-open" id="all-open" type="button">Alle aufdecken</button>
<div class="pity"><span class="caption">SSR-GARANTIE</span><div class="pity-bar"><i></i></div><b>33 / 80</b></div>
<div class="purchase-row">
  <button class="purchase" data-pull-button="1x"><span class="main">{img(HUD / 'icons_v1' / 'd2_ico_zeitkristall.png', '', '')}1× BESCHWÖREN</span><small>150 · EINE KARTE</small></button>
  <button class="purchase" data-pull-button="10x"><span class="main">{img(HUD / 'icons_v1' / 'd2_ico_zeitkristall.png', '', '')}10× BESCHWÖREN</span><small>1.350 · ZEHN KARTEN</small></button>
</div>
<div class="infochip">{img(ASSETS / 'ico_heldenxp.png', '', '')}<span>Wahrscheinlichkeiten &amp; Garantie</span></div>
<div class="dock">{dock_html}<div style="position:absolute;left:390px;bottom:11px;width:300px;height:10px;border-radius:5px;background:rgba(255,255,255,.92)"></div></div>
<div class="count-toast" id="count-toast"></div>
<script>
const HERO = {{
  NARA: {{name:'NARA', rarity:'SSR', color:'#ffc164', image:'{hero('nara')}'}},
  OLM: {{name:'OLM', rarity:'SR', color:'#c6a4ff', image:'{hero('olm')}'}},
  KIKO: {{name:'KIKO', rarity:'R', color:'#77c9f1', image:'{hero('kiko')}'}},
  RUKA: {{name:'RUKA', rarity:'SSR', color:'#ffc164', image:'{hero('ruka')}'}},
}};
const FEATURED_TEN = [
  {{kind:'hero', hero:'NARA'}},
  {{kind:'fragment', hero:'OLM', amount:5, progress:'12 / 80', fill:'15%'}},
  {{kind:'hero', hero:'KIKO'}},
  {{kind:'fragment', hero:'NARA', amount:3, progress:'29 / 80', fill:'36%'}},
  {{kind:'hero', hero:'OLM'}},
  {{kind:'fragment', hero:'KIKO', amount:8, progress:'44 / 80', fill:'55%'}},
  {{kind:'fragment', hero:'RUKA', amount:3, progress:'29 / 80', fill:'36%'}},
  {{kind:'hero', hero:'RUKA'}},
  {{kind:'fragment', hero:'OLM', amount:2, progress:'46 / 80', fill:'58%'}},
  {{kind:'fragment', hero:'KIKO', amount:5, progress:'49 / 80', fill:'61%'}},
];
const PULLS = {{
  featured: {{
    '1x': [{{kind:'hero',hero:'NARA'}}],
    '10x': FEATURED_TEN,
  }},
  standard: {{
    '1x': [{{kind:'fragment',hero:'KIKO',amount:5,progress:'12 / 80',fill:'15%'}}],
    '10x': [
      {{kind:'fragment',hero:'KIKO',amount:5,progress:'12 / 80',fill:'15%'}},
      {{kind:'hero',hero:'OLM'}},
      {{kind:'fragment',hero:'OLM',amount:3,progress:'15 / 80',fill:'19%'}},
      {{kind:'hero',hero:'KIKO'}},
      {{kind:'fragment',hero:'NARA',amount:2,progress:'31 / 80',fill:'39%'}},
      {{kind:'fragment',hero:'KIKO',amount:4,progress:'16 / 80',fill:'20%'}},
      {{kind:'hero',hero:'RUKA'}},
      {{kind:'fragment',hero:'OLM',amount:2,progress:'17 / 80',fill:'21%'}},
      {{kind:'hero',hero:'NARA'}},
      {{kind:'fragment',hero:'KIKO',amount:3,progress:'19 / 80',fill:'24%'}},
    ]
  }}
}};
const cardsNode = document.getElementById('cards');
const labelNode = document.getElementById('label-chip');
const toastNode = document.getElementById('count-toast');
let mode = 'featured', pull = '10x';

function cardMarkup(item, index, large=false) {{
  const h = HERO[item.hero], type = item.kind === 'fragment' ? 'fragment' : 'hero';
  const rarity = h.color;
  const back = `<span class="face backface"><span class="sigil">✦</span><span class="back-word">D2 · BESCHWÖRUNG</span></span>`;
  let front;
  if (type === 'fragment') {{
    front = `<span class="face frontface"><span class="card-content fragment">
      <span class="kind">${{h.name}} · FRAGMENT</span>
      <span class="portrait-ring"><img src="${{h.image}}" alt="${{h.name}}"></span>
      <span class="quantity">×${{item.amount}}</span>
      <span class="counter">${{item.progress}}</span>
      <span class="progress-mini" style="--progress:${{item.fill}}"><i></i></span>
    </span></span>`;
  }} else {{
    front = `<span class="face frontface"><span class="card-content">
      <span class="kind">HELD</span>
      <span class="portrait-ring"><img src="${{h.image}}" alt="${{h.name}}"></span>
      <span class="hero-name">${{h.name}}</span>
      <span class="rarity-pill">${{h.rarity}}</span>
    </span></span>`;
  }}
  const revealLabel = type === 'fragment' ? `${{h.name}}-Fragmente ×${{item.amount}}, Stand ${{item.progress}}` : `${{h.name}}, Seltenheit ${{h.rarity}}`;
  return `<button class="card ${{large ? 'type-large' : ''}} ${{type}}" data-index="${{index}}" style="--rarity:${{rarity}}" type="button" aria-label="Karte ${{index+1}}: ${{revealLabel}} aufdecken" aria-pressed="false">
    <span class="card-inner">${{back}}${{front}}</span></button>`;
}}

function drawCards(openAll=false) {{
  const data = PULLS[mode][pull];
  cardsNode.classList.toggle('single', data.length === 1);
  cardsNode.style.gridTemplateColumns = data.length === 1 ? '340px' : 'repeat(5,184px)';
  cardsNode.style.gridTemplateRows = data.length === 1 ? '490px' : '252px 252px';
  cardsNode.innerHTML = data.map((item,index)=>cardMarkup(item,index,data.length===1)).join('');
  cardsNode.querySelectorAll('.card').forEach((card,index)=>{{
    if(openAll){{card.classList.add('is-open');card.setAttribute('aria-pressed','true')}}
    card.addEventListener('click',()=>{{
      const now = card.classList.toggle('is-open'); card.setAttribute('aria-pressed',String(now)); updateCount();
    }});
  }});
  labelNode.textContent = data.length === 1 ? '1× · 1 KARTE' : '10× · 10 KARTEN';
  updateCount();
}}
function updateCount() {{
  const total = cardsNode.querySelectorAll('.card').length;
  const shown = cardsNode.querySelectorAll('.card.is-open').length;
  toastNode.textContent = `${{shown}} / ${{total}} AUFGEDECKT`;
  toastNode.style.display = total > 1 ? 'block' : 'none';
}}
function setMode(next) {{
  mode = next; document.documentElement.dataset.mode = mode;
  document.querySelectorAll('[data-mode-button]').forEach(button=>{{
    const active = button.dataset.modeButton === mode;
    button.classList.toggle('active',active); button.setAttribute('aria-selected',String(active));
  }});
  drawCards(false);
}}
function setPull(next) {{ pull = next; document.documentElement.dataset.pull = pull; drawCards(false); }}
document.querySelectorAll('[data-mode-button]').forEach(button=>button.addEventListener('click',()=>setMode(button.dataset.modeButton)));
document.querySelectorAll('[data-pull-button]').forEach(button=>button.addEventListener('click',()=>setPull(button.dataset.pullButton)));
document.getElementById('all-open').addEventListener('click',()=>{{
  cardsNode.querySelectorAll('.card').forEach(card=>{{card.classList.add('is-open');card.setAttribute('aria-pressed','true')}}); updateCount();
}});
const key = location.hash.replace('#','').split('-');
if(['featured','standard'].includes(key[0])) mode=key[0];
if(['1x','10x'].includes(key[1])) pull=key[1];
document.documentElement.dataset.mode=mode; document.documentElement.dataset.pull=pull;
document.querySelectorAll('[data-mode-button]').forEach(button=>{{const active=button.dataset.modeButton===mode;button.classList.toggle('active',active);button.setAttribute('aria-selected',String(active))}});
drawCards(key[2] === 'open');
</script>
</body></html>'''


def render(html_path: Path, output: Path, fragment: str) -> None:
    url = html_path.resolve().as_uri() + f"#{fragment}"
    subprocess.run([
        "google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
        "--hide-scrollbars", "--force-device-scale-factor=1",
        f"--window-size={W},{H}", "--virtual-time-budget=2500",
        "--allow-file-access-from-files", f"--screenshot={output}", url,
    ], check=True, capture_output=True, timeout=120)


def main() -> None:
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    html_path = HTML_DIR / "v3_2_obsidian_beschwoeren_featured_v15_interaktiv.html"
    html_path.write_text(page(), encoding="utf-8")
    frames = [
        ("featured", "1x", "closed"), ("featured", "1x", "open"),
        ("featured", "10x", "closed"), ("featured", "10x", "open"),
        ("standard", "1x", "closed"), ("standard", "1x", "open"),
    ]
    for mode, pull, state in frames:
        filename = f"vorschau_menu_beschwoeren_d2_{mode}_v15_{pull}_{state}.png"
        render(html_path, OUT / filename, f"{mode}-{pull}-{state}")
        mirror = V3 / f"v3_2_obsidian_beschwoeren_{mode}_v15_{pull}_{state}.png"
        mirror.write_bytes((OUT / filename).read_bytes())
    mirror_html = V3 / "_src" / "html" / "v3_2_obsidian_beschwoeren_featured_v15_interaktiv.html"
    mirror_html.write_bytes(html_path.read_bytes())
    print("Rendered 6 v15 PNG keyframes (1080×1920) and one interactive HTML page.")


if __name__ == "__main__":
    main()
