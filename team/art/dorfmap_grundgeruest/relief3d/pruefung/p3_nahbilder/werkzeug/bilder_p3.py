# Vergleichsbilder: Modus paar (vorher|nachher je Kamera, Vollbild + 300-%-Ausschnitt) und blatt (Uebersicht mehrerer Kacheln)
from PIL import Image,ImageDraw
import sys,os
def paar(va,na,ziel,titel,names):
    for n in names:
        a=Image.open(f'{va}/{n}.png').convert('RGB');b=Image.open(f'{na}/{n}.png').convert('RGB')
        W,H=a.size;cw,ch=260,180;box=(W//2-cw//2,H//2-ch//2,W//2+cw//2,H//2+ch//2)
        ca=a.crop(box).resize((cw*3,ch*3),Image.LANCZOS);cb=b.crop(box).resize((cw*3,ch*3),Image.LANCZOS)
        out=Image.new('RGB',(W*2+10,H+ch*3+40),'white');out.paste(a,(0,30));out.paste(b,(W+10,30));out.paste(ca,(0,H+40));out.paste(cb,(W+10,H+40))
        d=ImageDraw.Draw(out);t=titel.split('|');d.text((5,5),f'{n} {t[0]}',fill='black');d.text((W+15,5),f'{n} {t[1]}',fill='black');d.text((5,H+32),'Ausschnitt 300 % (Rahmen magenta)',fill='black')
        for o in (0,W+10):d.rectangle((o+box[0],30+box[1],o+box[2],30+box[3]),outline=(255,0,255))
        out.save(f'{ziel}/{n}_{t[2] if len(t)>2 else "vgl"}.jpg',quality=86)
def blatt(dirs,labs,ziel,pro=4,W=560,H=392):
    names=sorted([f[:-4] for f in os.listdir(dirs[0]) if f.endswith('.png')],key=lambda n:(n[1:2],n[0]))
    for k in range(0,len(names),pro):
        N=names[k:k+pro];img=Image.new('RGB',(len(dirs)*(W+6),len(N)*(H+6)),'white');d=ImageDraw.Draw(img)
        for r,n in enumerate(N):
            for j,dd in enumerate(dirs):
                p=f'{dd}/{n}.png'
                if os.path.exists(p):img.paste(Image.open(p).convert('RGB').resize((W,H),Image.LANCZOS),(j*(W+6),r*(H+6)))
            d.rectangle((0,r*(H+6),220,r*(H+6)+16),fill='white');d.text((3,r*(H+6)+2),n+': '+' | '.join(labs),fill='red')
        img.save(f'{ziel}_{k//pro+1:02d}.jpg',quality=82)
if __name__=='__main__':
    if sys.argv[1]=='paar':paar(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6:])
    elif sys.argv[1]=='blatt':blatt(sys.argv[2].split(','),sys.argv[3].split(','),sys.argv[4],int(sys.argv[5]) if len(sys.argv)>5 else 4)
def ausschnitte(va,na,kinds,ziel,pro=8,cw=260,ch=180,s=1.5):
    # Uebersicht: je Kachel Bildmitte-Ausschnitt (150 %) vorher|nachher fuer jede Kameraart
    tiles=sorted({f.rsplit('_',1)[0] for f in os.listdir(va)});Wd,Hd=int(cw*s),int(ch*s)
    for k0 in range(0,len(tiles),pro):
        T=tiles[k0:k0+pro];img=Image.new('RGB',(60+len(kinds)*2*(Wd+6),len(T)*(Hd+6)+20),'white');d=ImageDraw.Draw(img);x=60
        for kd in kinds:
            for lab in ('vorher','nachher'):d.text((x+4,4),f'{kd} {lab}',fill='black');x+=Wd+6
        for r,t in enumerate(T):
            y=20+r*(Hd+6);d.text((4,y+Hd//2),t,fill='black');x=60
            for kd in kinds:
                for src in (va,na):
                    p=f'{src}/{t}_{kd}.png'
                    if os.path.exists(p):
                        a=Image.open(p).convert('RGB');w,h=a.size;img.paste(a.crop((w//2-cw//2,h//2-ch//2,w//2+cw//2,h//2+ch//2)).resize((Wd,Hd),Image.LANCZOS),(x,y))
                    x+=Wd+6
        img.save(f'{ziel}_{k0//pro+1}.jpg',quality=85)
if __name__=='__main__' and sys.argv[1]=='ausschnitte':ausschnitte(sys.argv[2],sys.argv[3],sys.argv[4].split(','),sys.argv[5])
