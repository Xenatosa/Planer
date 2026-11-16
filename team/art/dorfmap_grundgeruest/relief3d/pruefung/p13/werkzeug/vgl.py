import numpy as np, os, json
from PIL import Image, ImageDraw
from zaehl import zaehl
from scipy.ndimage import uniform_filter
sh="B4_Q2,B4_Q3,B4_Q4,C4_U,C4_Q1,B5_U,C5_U,H3_U,H4_U,G3_U,G3_Q2,G4_U,G4_Q2,H2_U,D3_U".split(',')
os.makedirs('vergleich',exist_ok=True); aus={}
for s in sh:
  _,dv=zaehl(f'vorher/{s}.png'); _,dn=zaehl(f'nachher/{s}.png')
  dens=uniform_filter(dv.astype(float),size=(150,200)); y,x=np.unravel_index(dens.argmax(),dens.shape)
  x0=int(min(max(x-100,0),960-200)); y0=int(min(max(y-75,0),680-150)); box=(x0,y0,x0+200,y0+150); aus[s]=box
  V=Image.open(f'vorher/{s}.png').convert('RGB'); N=Image.open(f'nachher/{s}.png').convert('RGB')
  W=Image.new('RGB',(1200+10,450+70),'white'); dr=ImageDraw.Draw(W)
  W.paste(V.crop(box).resize((600,450),Image.NEAREST),(0,30)); W.paste(N.crop(box).resize((600,450),Image.NEAREST),(610,30))
  dr.text((5,8),f'{s} vorher (?silh=0)  Ausschnitt {box} x3, dunkle Pixel im Bild: {int(dv.sum())}',fill='black')
  dr.text((615,8),f'nachher (P13 FrontSide), dunkle Pixel im Bild: {int(dn.sum())}',fill='black')
  W.save(f'vergleich/{s}_x3.png')
  # Markierung nachher (Rest)
  M=N.copy(); a=np.array(M); a[dn]=[255,0,0]; Image.fromarray(a).save(f'vergleich/{s}_nachher_rest_markiert.png')
json.dump(aus,open('ausschnitte.json','w'))
