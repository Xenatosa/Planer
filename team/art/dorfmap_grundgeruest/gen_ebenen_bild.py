import csv,numpy as np,collections
from PIL import Image,ImageDraw,ImageFont
R=list(csv.DictReader(open('raster_c20_z25_zellen.csv')))
assert len(R)==336*303
P={'SENKE':(255,200,0),'WEST':(0,170,255),'WAND':(150,75,0),'TAL_SUED':(170,0,255),'PLATEAU_NORD':(255,40,40),'OSTPLATEAU':(0,200,60),'KRATER':(255,120,200)}
names=list(P);lab=np.full((303,336),-1)
for r in R:
    e=r['ebene']; assert e in P,(r['cx'],r['cy'],e); lab[int(r['cy']),int(r['cx'])]=names.index(e)
assert (lab>=0).all()
S=4;A=0.7
m=Image.open('/workspace/handygame-plan/team/art/karten_konzept/dorfkarte_e1_final_neu/master_v18_p7/KANDIDAT_NICHT_FREIGEGEBEN_master_v18_p7_c20.png').convert('RGB').crop((0,0,336*25,303*25)).resize((336*S,303*S),Image.LANCZOS)
g=np.asarray(m.convert('L').convert('RGB')).astype(float)
pal=np.array([P[n] for n in names],float)
col=np.kron(pal[lab],np.ones((S,S,1)))  # wrong shape fix below
col=pal[lab].repeat(S,0).repeat(S,1)
out=np.clip(A*col+(1-A)*g,0,255).round().astype(np.uint8)
# Abgleich: Zellmitte zurueckrechnen
c=out[S//2::S,S//2::S].astype(float); gb=g[S//2::S,S//2::S]
est=(c-(1-A)*gb)/A
d=((est[:,:,None,:]-pal[None,None])**2).sum(-1).argmin(-1)
bad=(d!=lab).sum(); print('abweichend',bad)
# auch alle Pixel je Zelle gleich zugeordnet
full=((( (out.astype(float)-(1-A)*g)/A)[:,:,None,:]-pal[None,None])**2).sum(-1).argmin(-1)
print('pixel abweichend',(full!=lab.repeat(S,0).repeat(S,1)).sum())
cnt=collections.Counter(r['ebene'] for r in R)
W=out.shape[1];leg=Image.new('RGB',(W,330),'white');dr=ImageDraw.Draw(leg)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26)
dr.text((20,10),f'Ebenen z25 – alle {sum(cnt.values())} Zellen (Feld ebene, t33u). Grund: c20 grau',fill='black',font=f)
for i,n in enumerate(names):
    x=20+(i%4)*330;y=70+(i//4)*120
    dr.rectangle((x,y,x+60,y+60),fill=P[n],outline='black',width=2)
    dr.text((x+70,y),n,fill='black',font=f);dr.text((x+70,y+34),f'{cnt[n]} Zellen',fill='black',font=f)
img=Image.new('RGB',(W,out.shape[0]+330));img.paste(Image.fromarray(out),(0,0));img.paste(leg,(0,out.shape[0]))
img.save('pruefung/t33u_ebenen_vollstaendig.png');print(cnt,img.size)
