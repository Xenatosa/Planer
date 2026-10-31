# t63u: im_wasser = Wasserspiegel (3x3-Ecken) ueber Objektfuss, gleiche Regel wie Raycast-Auswertung
# t62u: Baeume/Felsen/Findlinge/Steine/Geroell gegen das ANGEZEIGTE Gelaende (GB) pruefen [S]
import json,gzip,base64,sys,numpy as np,scipy.ndimage as nd
D=json.load(gzip.open(sys.argv[1] if len(sys.argv)>1 else 'relief_daten.json.gz'));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
f=lambda k:np.frombuffer(base64.b64decode(D[k]),np.float32).reshape(GY,GX).astype(float)
import os;G=f(os.environ.get('FELD') or (D.get('GB') and 'GB' or 'G'));WV=f('WV');gy,gx=np.gradient(G,1/RS);SL=np.degrees(np.arctan(np.hypot(gx,gy)))
W=WV>-900;GMX=nd.maximum_filter(G,3);GMN=nd.minimum_filter(G,3);Wn=nd.binary_dilation(W,iterations=1)
WM3=nd.maximum_filter(WV,3)
def at(A,x,z,o=1):return nd.map_coordinates(A,[[z*RS],[x*RS]],order=o,mode='nearest')[0]
R={}
for k,unten in(('baeume',0.3),('felsen',0),('findlinge',0),('steine',0),('geroell',0)):
    L=D.get(k) or [];c=dict(n=len(L),schwebend_gt_0_3m=0,versunken_gt_0_5m=0,steil_gt_45=0,im_wasser=0,max_abw_m=0.0)
    for o in L:
        x,y,z,h=o[0],o[1],o[2],o[3];g=at(G,x,z);hi=at(GMX,x,z,0);lo=at(GMN,x,z,0);yb=y-unten
        d=yb-hi if yb>hi else (yb-lo if yb<lo else 0.0)   # Abweichung zur Gelaendespanne im 1-m-Fenster
        # versunken: Baum >0,5 m, Stein >0,6*h (Steine stecken absichtlich etwas im Boden)
        tol=0.5 if k=='baeume' else max(0.5,0.6*h)
        if d>0.3:c['schwebend_gt_0_3m']+=1
        if d<-tol:c['versunken_gt_0_5m']+=1
        if at(SL,x,z)>45 and k in('baeume',):c['steil_gt_45']+=1
        if at(WM3,x,z,0)>yb:c['im_wasser']+=1
        c['max_abw_m']=max(c['max_abw_m'],round(abs(d),2))
    R[k]=c
print(json.dumps(R))
