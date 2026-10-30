# t34u: Vorher-Bild = t33u-Ebenenbild, alle in t34u geaenderten Zellen rot umrandet + nummeriert
import numpy as np,cv2,sys
from PIL import Image,ImageDraw,ImageFont
a=np.load(sys.argv[1]);b=np.load(sys.argv[2]);S=4
im=Image.open('_alt/pruefung/t33u_ebenen_vollstaendig.png').convert('RGB');d=ImageDraw.Draw(im)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
ch=(a!=b).astype(np.uint8)
cs,_=cv2.findContours(cv2.resize(ch,(336*S,303*S),interpolation=cv2.INTER_NEAREST),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
for c in cs: d.line([tuple(p[0]) for p in c]+[tuple(c[0][0])],fill=(255,0,0),width=3)
L=[('F1',15,4),('F2',30,150),('F3',30,268),('F4',318,282),('F5',125,40),('F6',96,110),('F7',300,120),('F8',178,226),('F9',100,205),('F10',128,150)]
for t,x,y in L:
    d.rectangle((x*S-4,y*S-4,x*S+50,y*S+24),fill='white',outline='red',width=2);d.text((x*S,y*S-3),t,fill='red',font=f)
d.rectangle((0,303*S,1344,303*S+60),fill='white')
d.text((10,303*S+10),f'VORHER t33u: rot umrandet = {int(ch.sum())} Zellen mit falscher ebene (F1–F10, siehe t34u_fehlerliste.csv)',fill='red',font=f)
im.save('pruefung/t34u_vorher_fehler.png')
