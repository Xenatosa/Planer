# Platzhalter-Felswandtextur (prozedural, kachelbar), 1 Kachel = 4 m breit x 8 m hoch [A]
import numpy as np,random
from PIL import Image,ImageDraw,ImageFilter
random.seed(4);W,H=256,512
a=np.random.default_rng(4).normal(0,1,(H//8,W//8));a=np.kron(a,np.ones((8,8)))
im=Image.fromarray(np.clip(128+a*10,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)).convert('RGB')
px=np.array(im).astype(float)/128;base=np.array([120,98,82])
im=Image.fromarray(np.clip(px*base,0,255).astype(np.uint8));d=ImageDraw.Draw(im)
x=0
while x<W:                                  # senkrechte Pfeiler
    w=random.randint(30,60);d.line([(x,0),(x+random.randint(-6,6),H)],fill=(55,42,36),width=3)
    for _ in range(3):
        y=random.randint(0,H);d.line([(x,y),(x+w,y+random.randint(-15,15))],fill=(70,55,46),width=2)
    x+=w
for _ in range(25):
    x,y=random.randint(0,W),random.randint(0,H);d.polygon([(x,y),(x+20,y+8),(x+6,y+30)],fill=(150,128,110))
im.save('wand_textur.png');print(im.size)
