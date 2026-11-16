# QA P4b: Kompositbild je Kachel aus rendere_kacheln.js-Ausgabe: oben Uebersicht (U), unten 4 Viertel (Q1 NW, Q2 NO, Q3 SW, Q4 SO).
# Aufruf: python3 komposit.py ROHORDNER ZIELORDNER [label]
import sys, os
from PIL import Image, ImageDraw, ImageFont
roh, ziel = sys.argv[1], sys.argv[2]; lab = sys.argv[3] if len(sys.argv) > 3 else ''
os.makedirs(ziel, exist_ok=True)
try: F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
except Exception: F = ImageFont.load_default()
for c in 'ABCDEFGH':
    for r in range(1, 8):
        t = f'{c}{r}'
        if not os.path.exists(f'{roh}/{t}_U.png'): continue
        x0, z0 = 'ABCDEFGH'.index(c) * 42, (r - 1) * 43
        K = Image.new('RGB', (820, 22 + 580 + 2 * 290), 'white'); d = ImageDraw.Draw(K)
        d.text((6, 3), f'{t}  x {x0}–{x0+42}  z {z0}–{z0+43}   U: Übersicht (P10-Kamera, Schatten aus)   {lab}', fill=(140, 0, 0), font=F)
        K.paste(Image.open(f'{roh}/{t}_U.png').convert('RGB').resize((820, 580), Image.LANCZOS), (0, 22))
        Q = [(x0 + 10.5, z0 + 10.75), (x0 + 31.5, z0 + 10.75), (x0 + 10.5, z0 + 32.25), (x0 + 31.5, z0 + 32.25)]
        for i in range(4):
            im = Image.open(f'{roh}/{t}_Q{i+1}.png').convert('RGB').resize((410, 290), Image.LANCZOS)
            dd = ImageDraw.Draw(im); dd.rectangle([0, 0, 250, 20], fill=(255, 255, 255))
            dd.text((4, 2), f'Q{i+1} {["NW","NO","SW","SO"][i]} Mitte {Q[i][0]:.1f}|{Q[i][1]:.1f}', fill=(0, 0, 0), font=F)
            cx, cy = 205, 145
            for sx in (-1, 1):
                for sy in (-1, 1): dd.line([(cx+sx*8, cy+sy*8), (cx+sx*14, cy+sy*8)], fill=(230, 20, 20), width=2); dd.line([(cx+sx*8, cy+sy*8), (cx+sx*8, cy+sy*14)], fill=(230, 20, 20), width=2)
            K.paste(im, ((i % 2) * 410, 22 + 580 + (i // 2) * 290))
        K.save(f'{ziel}/{t}.jpg', quality=70, optimize=True)
print('ok')
