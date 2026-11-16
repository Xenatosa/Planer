import sys,os,json
from PIL import Image,ImageDraw
pts=json.load(open(sys.argv[1] if len(sys.argv)>1 else '/tmp/p4b/punkte.json'));os.makedirs('/tmp/p4b/paar',exist_ok=True)
for q in pts:
    a=Image.open(f'detail/farbe/{q["n"]}.png').convert('RGB');b=Image.open(f'detail/clay/{q["n"]}.png').convert('RGB')
    w=480;h=int(a.height*w/a.width);a=a.resize((w,h));b=b.resize((w,h))
    c=Image.new('RGB',(2*w,h+22),'white');c.paste(a,(0,22));c.paste(b,(w,22));d=ImageDraw.Draw(c)
    d.text((4,5),f'{q["n"]}  x={q["x"]} z={q["z"]}  d={q.get("d",15)} m, el={q.get("el",35)} Grad, az={q.get("az",0)} | links Farbe, rechts Ton (clay)  dc8c174',fill=(150,0,0))
    for o in (0,w):
        cx,cy=o+w//2,22+h//2;d.line((cx-10,cy,cx-4,cy),fill='red');d.line((cx+4,cy,cx+10,cy),fill='red');d.line((cx,cy-10,cx,cy-4),fill='red');d.line((cx,cy+4,cx,cy+10),fill='red')
    c.save(f'paar/{q["n"]}.jpg',quality=80)
