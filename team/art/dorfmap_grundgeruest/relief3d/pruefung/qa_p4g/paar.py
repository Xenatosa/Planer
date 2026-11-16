"""Farbe|Clay nebeneinander. Aufruf: WURZEL=/tmp/p4c STAND=8cd6d37 python3 paar.py punkte.json
liest WURZEL/detail/{farbe,clay}/<n>.png, schreibt WURZEL/paar/<n>.jpg"""
import sys,os,json
from PIL import Image,ImageDraw
W=os.environ.get('WURZEL','/tmp/p4c');ST=os.environ.get('STAND','8cd6d37')
pts=json.load(open(sys.argv[1]));os.makedirs(f'{W}/paar',exist_ok=True)
for q in pts:
    a=Image.open(f'{W}/detail/farbe/{q["n"]}.png').convert('RGB');b=Image.open(f'{W}/detail/clay/{q["n"]}.png').convert('RGB')
    w=480;h=int(a.height*w/a.width);a=a.resize((w,h));b=b.resize((w,h))
    c=Image.new('RGB',(2*w,h+22),'white');c.paste(a,(0,22));c.paste(b,(w,22));d=ImageDraw.Draw(c)
    d.text((4,5),f'{q["n"]}  x={q["x"]} z={q["z"]}  d={q.get("d",15)} m, el={q.get("el",35)} Grad, az={q.get("az",0)} | links Farbe, rechts Ton (clay)  {ST}',fill=(150,0,0))
    for o in (0,w):
        cx,cy=o+w//2,22+h//2;d.line((cx-10,cy,cx-4,cy),fill='red');d.line((cx+4,cy,cx+10,cy),fill='red');d.line((cx,cy-10,cx,cy-4),fill='red');d.line((cx,cy+4,cx,cy+10),fill='red')
    c.save(f'{W}/paar/{q["n"]}.jpg',quality=80)
