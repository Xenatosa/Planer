# t41u: echtes neues 3D-Relief. Quelle Lage: raster_c20_z25_zellen.csv (+ t36u-Sidecar fuer Felder). c20 unveraendert.
# Ausgabe: relief_daten.json.gz (Viewer), zellen_relief.csv (Sidecar), dorfmap_relief_z25.glb/.obj, relief_zaehlung.json
import os
import csv,json,gzip,base64,numpy as np,scipy.ndimage as nd
B='../';NX,NY=336,303;SPRUNG=2.5
R=list(csv.DictReader(open(B+'_alt/modell3d_t36u/zellen_eigenschaften.csv')))
cols=[c for c in R[0].keys() if not c.startswith('modell_')]
A=lambda k:np.array([r[k] for r in R]).reshape(NY,NX)
eb=A('ebene');wn=A('wand_name');ug=A('untergrund').copy();h0=A('hoehe_m').astype(float);wa=A('wasser_eis')=='1';fl=A('fluss_id');ha=A('hindernis_art')
wand=np.isin(ug,['KLIPPE_WAND','KLIPPE_KANTE'])
# --- Hoehen je Ebene (Wandhoehen aus Messung [R], Rest [A])
WANDH={'Nord':14.0,'Suedgrat':16.0,'Krater':11.0,'Ostgrat':12.0}
EBENE_H={'PLATEAU_NORD':14.0,'OSTPLATEAU':12.0,'TAL_SUED':-16.0,'GIPFEL':14.0,'KRATER':1.0}
H=h0.copy()
pos=h0>0;H[pos]=h0[pos]*1.7;neg=h0<0;H[neg]=h0[neg]*16/7.6          # Hang/Sims skaliert [A]
for e,v in EBENE_H.items():H[eb==e]=v
H[(eb=='SENKE')]=h0[eb=='SENKE']
# Wandband -> obere Ebene (Wand steht am Fuss) [F]
for w,v in {'Nord':14.0,'Krater':11.0,'Ostgrat':12.0}.items():H[wand&(wn==w)]=v
# Suedgrat + unbenannt: hoechster Nachbar ausserhalb Band, ausbreiten
rest=wand&~np.isin(wn,['Nord','Krater','Ostgrat']);K=~rest;Hk=np.where(K,H,-1e9)
for _ in range(60):
    d=nd.grey_dilation(Hk,size=3);neu=rest&~K&(d>-1e8);Hk[neu]=d[neu];K|=neu
    if not (rest&~K).any():break
H[rest]=Hk[rest]
sg=wand&(wn=='Suedgrat');topf=nd.maximum_filter(np.where(sg&(H>-15),H,-1e9),size=31);dsg=nd.distance_transform_edt(~sg)
ziel=((eb=='TAL_SUED')&(dsg<=15)|(sg&(H<=-15.9)))&(topf>-1e8)
H[ziel]=np.minimum(H[ziel],-16-0.8*(1-dsg[ziel]/15))   # t46u: Fuss nie unter Talboden -16,8 (vorher Graeben bis -25,8 m wo Gratoberkante tief lag) [A]
# --- t47u: Flusslücken schliessen (c20: Wasser endet an Wandbaendern / 2-9 Zellen Luecken) [A]
def _flussluecken():
    lab,n=nd.label(wa,np.ones((3,3)));big=[i for i in range(1,n+1) if (lab==i).sum()>=30];log=[]
    for k,i in enumerate(big):
        di,ind=nd.distance_transform_edt(lab!=i,return_indices=True)
        for j in big[k+1:]:
            m=lab==j;dmin=di[m].min()
            if dmin<1.5 or dmin>12:continue
            yb,xb=[v[m][np.argmin(di[m])] for v in np.nonzero(np.ones_like(m))] if False else np.argwhere(m)[np.argmin(di[m])]
            ya,xa=ind[0][yb,xb],ind[1][yb,xb];ha_,hb_=H[ya,xa],H[yb,xb];L=int(max(abs(yb-ya),abs(xb-xa)))+1
            for t in np.linspace(0,1,L*2):
                y=int(round(ya+t*(yb-ya)));x=int(round(xa+t*(xb-xa)))
                for dy in (-1,0,1):
                    for dx in (-1,0,1):
                        yy,xx=y+dy,x+dx
                        if 0<=yy<NY and 0<=xx<NX and not wa[yy,xx]:
                            wa[yy,xx]=True;fl[yy,xx]=fl[ya,xa];H[yy,xx]=ha_+t*(hb_-ha_);wand[yy,xx]=False;ug[yy,xx]='WASSER_EIS'
            log.append(((int(xa),int(ya)),(int(xb),int(yb)),round(float(dmin),1),round(float(ha_),1),round(float(hb_),1)))
    return log
FLUSSLUECKEN=_flussluecken();print('flussluecken',FLUSSLUECKEN)
# t47u: Stufen im Wasserspiegel >1 m/Zelle zu Stromschnellen verteilen [A]
for _ in range(3):
    Hw=np.where(wa,H,np.nan);st=np.zeros_like(wa)
    st[1:]|=np.abs(np.diff(Hw,axis=0))>0.9;st[:-1]|=np.abs(np.diff(Hw,axis=0))>0.9;st[:,1:]|=np.abs(np.diff(Hw,axis=1))>0.9;st[:,:-1]|=np.abs(np.diff(Hw,axis=1))>0.9
    zone=nd.binary_dilation(st,iterations=8)&wa
    if not zone.any():break
    sm=nd.gaussian_filter(np.where(wa,H,0),3)/np.maximum(nd.gaussian_filter(wa.astype(float),3),1e-6);H[zone]=sm[zone]
# t53u R2: Kraterring als Bergkranz: Gipfel/Kerben 3-10 Zellen hinter der Kraterkante (Wandsprung selbst bleibt) [A]
_kd_=nd.distance_transform_edt(~(wand&(wn=='Krater')))
_kr=(~wand)&(_kd_>=2)&(_kd_<=11)&(H>=9)&~wa&(eb!='KRATER')
_gn=nd.gaussian_filter(np.random.default_rng(57).standard_normal((NY,NX)),2.2);_gn/=_gn.std();_gr=1-np.abs(np.clip(_gn/1.6,-1,1))
_fall=np.clip((_kd_-2)/2,0,1)*np.clip((11-_kd_)/5,0,1)
H[_kr]+=(3.2*_gr**2-0.6)[_kr]*_fall[_kr]
# t47u/t48u: natuerliche Abstiegsrampen schraeg an den Waenden (Gelaende, nicht Overlay); Zellwerte folgen aus G [A]
RAMPWEGE=[];RAMPPROF=[]
def _rampen():
    Pl0=json.load(open(B+'pruefung/quelle_plaetze_wachstum_ausbau_planm.json'))['E40'];hm=np.zeros((NY,NX),bool)
    for p in Pl0:
        q=np.array([[(x+200)*1.2,(y+40)*1.2] for x,y in p['poly']]);x0,y0=q.min(0);x1,y1=q.max(0);hm[max(0,int(y0)):int(np.ceil(y1)),max(0,int(x0)):int(np.ceil(x1))]=1
    hm=nd.binary_dilation(hm,iterations=3)|nd.binary_dilation(wa,iterations=2)
    Hsm=nd.gaussian_filter(H,4);gy,gx=np.gradient(Hsm);top=wand&(nd.minimum_filter(H,9)<H-6);log=[]
    yy,xx=np.mgrid[0:NY,0:NX]
    for w,anz in (('Nord',3),('Suedgrat',3),('Krater',4),('Ostgrat',2)):
        cand=np.argwhere(top&(wn==w));r=np.random.default_rng(len(w));r.shuffle(cand);gew=[]
        for y,x in cand[:400]:
            if min(np.hypot(x-155,y-12),np.hypot(x-125,y-126))<32:continue   # t53u: dort Serpentine X084/X069
            dn=-np.array([gx[y,x],gy[y,x]]);l=np.hypot(*dn)
            if l<1e-3:continue
            dn/=l
            for sg in (1,-1):
                tg=np.array([-dn[1],dn[0]])*sg;d=dn*0.45+tg*0.89;d/=np.hypot(*d)
                Ht=H[y,x];L=None
                for s_ in range(6,90):
                    X,Y=int(round(x+d[0]*s_)),int(round(y+d[1]*s_))
                    if not(2<=X<NX-2 and 2<=Y<NY-2) or hm[Y,X]:break
                    if s_>8 and Ht-H[Y,X]>=5 and s_*0.30>=Ht-H[Y,X]:L=s_;break        # Rampe (~17 Grad, t53u) trifft Gelaende
                if L and L>=12 and all(np.hypot(x-a,y-b)>25 for a,b,_ ,_ in gew):gew.append((x,y,d,L))
                if len(gew)>=anz:break
            if len(gew)>=anz:break
        for x,y,d,L in gew:
            Ht=H[y,x];He=H[int(round(y+d[1]*L)),int(round(x+d[0]*L))]
            RAMPWEGE.append([[round(float(x+0.5+d[0]*s_),2),round(float(y+0.5+d[1]*s_),2)] for s_ in np.arange(-1,L+1.01,1.0)])   # Overlay-Pfad (getrennt) [A]
            RAMPPROF.append((np.array([[x+0.5+d[0]*s_,y+0.5+d[1]*s_] for s_ in np.linspace(0,L,L*4+1)]),np.linspace(Ht,He,L*4+1)))
            for k in range(L*3+1):
                s_=k/3;cx,cy=x+d[0]*s_,y+d[1]*s_;hp=Ht+(He-Ht)*s_/L
                ys,xs=slice(max(0,int(cy)-5),int(cy)+6),slice(max(0,int(cx)-5),int(cx)+6)
                rr=np.hypot(xx[ys,xs]+0.5-cx,yy[ys,xs]+0.5-cy);sub=H[ys,xs]
                kern=rr<=1.8;sub[kern]=hp;wand[ys,xs][kern]=False
                rand=(rr>1.8)&(rr<5);fill=hp-(rr-1.8)*1.1;sub[rand]=np.where(sub[rand]<fill[rand],fill[rand],sub[rand])
            log.append((w,int(x),int(y),int(L),round(float(Ht),1),round(float(He),1)))
    return log
RAMPEN=_rampen();print('rampen',RAMPEN)
# t53u R3: Serpentinen (Gelaende, <=17 Grad, Spitzkehren) wo der Overlay-Plan Treppe/Abstieg ueber die Wand braucht: X084 (Wand Nord), X069 (Krater) [A]
SERPENTINEN=[]
def _serp(name,A_,B_,n=4,sg=1):
    A_=np.array(A_,float)+0.5;B_=np.array(B_,float)+0.5;Ht=float(H[int(A_[1]),int(A_[0])]);He=float(H[int(B_[1]),int(B_[0])])
    ax=B_-A_;d=np.hypot(*ax);pe=sg*np.array([-ax[1],ax[0]])/d;soll=abs(Ht-He)/np.tan(np.radians(16.5));s_=np.linspace(0,1,1200)
    for W in np.arange(0,14,0.1):
        P=A_[None]+s_[:,None]*ax[None]+pe[None]*(W*(2/np.pi)*np.arcsin(np.sin(np.pi*n*s_)))[:,None]
        L=np.r_[0,np.cumsum(np.hypot(*np.diff(P,axis=0).T))]
        if L[-1]>=soll:break
    hp=Ht+(He-Ht)*L/L[-1];yy,xx=np.mgrid[0:NY,0:NX]
    for (cx,cy),h in zip(P[::3],hp[::3]):
        ys,xs=slice(max(0,int(cy)-5),int(cy)+6),slice(max(0,int(cx)-5),int(cx)+6)
        rr=np.hypot(xx[ys,xs]+0.5-cx,yy[ys,xs]+0.5-cy);sub=H[ys,xs];kern=(rr<=1.8)&~wa[ys,xs];sub[kern]=h;wand[ys,xs][kern]=False
    RAMPPROF.append((P,hp));RAMPWEGE.append([[round(float(a),2),round(float(b),2)] for a,b in P[::20]]+[[round(float(P[-1,0]),2),round(float(P[-1,1]),2)]])
    SERPENTINEN.append((name,round(Ht,1),round(He,1),round(float(L[-1]),1),round(float(np.degrees(np.arctan(abs(Ht-He)/L[-1]))),1),round(float(W),1)))
_serp('X084',(148,2),(156,37),n=3,sg=1);_serp('X069',(127,133),(122,119),n=3)
print('serpentinen',SERPENTINEN)
Hboden=H.copy()
# t53u R4: Flussbett eingeschnitten: Tiefe nach Abstand zum Ufer, Kiesbaenke, Uferboeschung + Sandufer [A]
_dw=nd.distance_transform_edt(wa);_kb=nd.gaussian_filter(np.random.default_rng(54).standard_normal((NY,NX)),2.5);_kb/=_kb.std()
tiefe=np.where(fl=='SEE',3.0,np.clip(0.45+0.6*_dw,0.45,2.4));kies=wa&(fl!='SEE')&(_kb>0.9)&(_dw>=1.5)
tiefe=np.where(kies,np.minimum(tiefe,0.5),tiefe)
Wsp=np.where(wa,Hboden-0.3,np.nan)
_do,_ix=nd.distance_transform_edt(~wa,return_indices=True);_wl=(Hboden-0.3)[_ix[0],_ix[1]]
_hm4=np.zeros((NY,NX),bool)
for p in json.load(open(B+'pruefung/quelle_plaetze_wachstum_ausbau_planm.json'))['E40']:
    q=np.array([[(x+200)*1.2,(y+40)*1.2] for x,y in p['poly']]);x0,y0=q.min(0);x1,y1=q.max(0);_hm4[max(0,int(y0)):int(np.ceil(y1)),max(0,int(x0)):int(np.ceil(x1))]=1
_ub=(~wa)&(_do<=5)&~wand&~nd.binary_dilation(_hm4,iterations=2)&(H>_wl)&(H-_wl<4)
_sand=0.15+np.where(_kb>0,0.12,0.42)*(_do-0.5)                         # flaches Sandufer (~7 Grad) oder Boeschung (~23 Grad)
H[_ub]=np.minimum(H[_ub],(_wl+_sand)[_ub]);Hboden[_ub]=H[_ub]
H[wa]-=tiefe[wa]
# --- t42u: glattes Hoehenfeld G auf 0,5-m-Gitter (keine 1-m-Treppen). Waende = steile, leicht unregelmaessige Flaechen [A]
RS=2;GX,GY=NX*RS+1,NY*RS+1;WANDWINKEL=55.0
Hn=np.kron(H,np.ones((RS,RS)))                                     # Proben in Zellmitte-Unterteilung
J=np.zeros((NY,NX),bool);J[:,1:]|=np.abs(np.diff(H,axis=1))>SPRUNG;J[:,:-1]|=np.abs(np.diff(H,axis=1))>SPRUNG
J[1:,:]|=np.abs(np.diff(H,axis=0))>SPRUNG;J[:-1,:]|=np.abs(np.diff(H,axis=0))>SPRUNG
wz=nd.gaussian_filter(np.kron(nd.binary_dilation(J,iterations=3),np.ones((RS,RS))).astype(float),2)
rs=np.random.default_rng(42);noi=nd.gaussian_filter(rs.standard_normal(Hn.shape),3);noi/=noi.std()
Hs=nd.gaussian_filter(Hn,3)                                        # sigma 1,5 m [A]
lo=nd.minimum_filter(Hn,15);hi=nd.maximum_filter(Hn,15);Rg=hi-lo
# t47u: mehrskalige Felsform – Rippen/Runsen (grob+mittel+fein), Baender/Simse, Schuttfuss [A]
def _fbm(sig,seed):
    r=np.random.default_rng(seed);n=nd.gaussian_filter(r.standard_normal(Hn.shape),sig);return n/n.std()
nf=0.55*_fbm(10,7)+0.30*_fbm(4,8)+0.15*noi
# t53u R1: domain-warped ridged fBm -> Felsrippen/Runsen (verschieben die Wandlinie), variable Steilheit, Simse [A]
_jj0,_ii0=np.mgrid[0:Hn.shape[0],0:Hn.shape[1]].astype(float)
_wy=_jj0+7*_fbm(14,31);_wx=_ii0+7*_fbm(14,32)
_rw=sum(a*(1-np.abs(np.clip(nd.map_coordinates(_fbm(sg,sd),[_wy,_wx],order=1,mode='reflect')/2.2,-1,1))) for a,sg,sd in ((0.55,7,33),(0.30,3.5,34),(0.15,1.8,35)))
RIB=(_rw-_rw.mean())/_rw.std()                                       # >0 Rippe, <0 Runse
u=(Hs-lo)/np.maximum(Rg,1e-6)-0.5+0.10*nf+0.13*RIB
krz=nd.gaussian_filter(np.kron(nd.binary_dilation(wand&(wn=='Krater'),iterations=4),np.ones((RS,RS))).astype(float),4)
steil_k=(1.3+2.4*np.clip(0.5+0.4*_fbm(18,36),0,1))*(1-krz)+1.6*krz                                            # t47u: Kraterrand als geboeschter Wall statt Senkrechtring [A]
t=np.clip(u*steil_k+0.5+0.25*krz*_fbm(6,11),0,1);t=t*t*(3-2*t)
# t48u R5: Kraterring mit radialen Felsrippen + 4 Scharten; uebrige Waende mit Grat-Rauschen (ridged). Ober-/Unterkante fix (sin(pi t)) [A]
_kc=np.argwhere(wand&(wn=='Krater')).mean(0)*RS;_jj,_ii=np.mgrid[0:Hn.shape[0],0:Hn.shape[1]];_ang=np.arctan2(_jj-_kc[0],_ii-_kc[1])
_rib=np.sin(_ang*13+1.6*_fbm(14,21));_rib=np.sign(_rib)*np.abs(_rib)**0.6
_sch=np.clip((np.abs(np.sin(_ang*2+0.7))-0.93)/0.07,0,1)
_rid=1-2*np.abs(np.clip(_fbm(5,22)/2.5,-1,1))
t=np.clip(t+np.sin(np.pi*t)*(krz*(0.20*_rib-0.45*_sch)+(1-krz)*0.10*(_rid-0.5)),0,1)
_ns=4+np.round(2*np.clip(0.5+0.4*_fbm(20,37),0,1));_tq=np.floor(t*_ns)/_ns;_fr=t*_ns-np.floor(t*_ns)
_led=(_fbm(9,38)>0.0)*(1-krz)
t=np.clip(t*(1-0.55*_led)+0.55*_led*(_tq+np.clip((_fr-0.55)/0.45,0,1)/_ns),0,1)   # Simse: flache Absaetze + steile Stufen
band=0.04*np.sin(t*np.pi*5+1.3*_fbm(8,9))*np.sin(np.pi*t)           # Simse/Baender in der Wand
tw=np.clip(u*1.5+0.62,0,1);apron=np.clip(tw,0,0.3)                    # Schuttkegel am Fuss
Gs=lo+Rg*np.clip(0.8*t+band+0.2*apron/0.3,0,1);Gs=np.where(Rg>SPRUNG,Gs,Hs)
Gsamp=Hs*(1-wz)+Gs*wz
vj,vi=np.mgrid[0:GY,0:GX].astype(float)
G=nd.map_coordinates(Gsamp,[vj-0.5,vi-0.5],order=1,mode='nearest').astype(np.float32)
# t50u: thermische Erosion nur im Wandfuss (Schutthalden, Rinnen); Plateaus/Talboden/Wasser fix [A]
_fm=nd.map_coordinates(((t<0.22)&(Rg>SPRUNG)).astype(float),[vj-0.5,vi-0.5],order=1)>0.5
_fm&=~(nd.map_coordinates(nd.binary_dilation(np.kron(wa,np.ones((RS,RS))),iterations=3).astype(float),[vj-0.5,vi-0.5],order=0)>0.5)
TAL=np.tan(np.radians(34))/RS;Ge=G.astype(np.float64)
for _ in range(30):
    for ax,sh in ((0,1),(0,-1),(1,1),(1,-1)):
        Nb=np.roll(Ge,sh,axis=ax);ok=_fm&np.roll(_fm,sh,axis=ax);ex=np.where(ok,np.clip(Ge-Nb-TAL,0,None)*0.2,0)
        Ge-=ex;Ge+=np.roll(ex,-sh,axis=ax)
# t48u R5: hydraulische Erosion (Tropfen-Modell), nur Wandzone ohne Wasser, Abtrag/Ablage je Punkt max 0,8 m [A]
_hm=nd.map_coordinates(((t>0.05)&(t<0.95)&(Rg>SPRUNG)).astype(float),[vj-0.5,vi-0.5],order=1)>0.5
_hm&=~(nd.map_coordinates(nd.binary_dilation(np.kron(wa,np.ones((RS,RS))),iterations=3).astype(float),[vj-0.5,vi-0.5],order=0)>0.5)
_G0=Ge.copy();_hr=np.random.default_rng(77);_st=np.argwhere(_hm);_st=_st[_hr.integers(0,len(_st),min(30000,len(_st)))]
_gy,_gx=np.gradient(Ge)
for _y,_x in _st:
    y,x=float(_y),float(_x);sed=0.0;v=1.0
    for _k in range(24):
        iy,ix=int(y),int(x)
        if not(0<iy<GY-1 and 0<ix<GX-1) or not _hm[iy,ix]:break
        dy,dx=-_gy[iy,ix],-_gx[iy,ix];l=np.hypot(dx,dy)
        if l<1e-4:break
        ny_,nx_=y+dy/l*0.7,x+dx/l*0.7;h0=Ge[iy,ix];h1=Ge[int(ny_),int(nx_)];dh=h0-h1
        cap=max(dh,0.01)*v*0.5
        if sed>cap or dh<0:dep=min(sed,max(-dh,0)) if dh<0 else (sed-cap)*0.3;Ge[iy,ix]+=dep;sed-=dep
        else:er=min((cap-sed)*0.3,dh*0.5);Ge[iy,ix]-=er;sed+=er
        v=np.sqrt(max(v*v+dh*0.5,0.01));y,x=ny_,nx_
Ge=_G0+np.clip(nd.gaussian_filter(Ge-_G0,0.6),-0.8,0.8)
print('hydro_erosion_m',round(float(np.abs(Ge-_G0).max()),2),round(float(np.abs(Ge-_G0)[_hm].mean()),3))
G=Ge.astype(np.float32)
# t53u R2/R3: Rampen + Serpentinen nach Erosion exakt ins Gitter (Kern 1,6 m eben laengs, Rand weich bis 3,6 m) [A]
from scipy.spatial import cKDTree
_PP=np.concatenate([p for p,_ in RAMPPROF]);_HH=np.concatenate([h for _,h in RAMPPROF]);_kd=cKDTree(_PP)
_vx=np.stack([vi.ravel()/RS,vj.ravel()/RS],1);_r,_k=_kd.query(_vx,distance_upper_bound=7.0);_ok=np.isfinite(_r)
_wv=nd.map_coordinates(np.kron(wa,np.ones((RS,RS))).astype(float),[vj-0.5,vi-0.5],order=0,mode='nearest').ravel()>0.5
_ok&=~_wv;_w=np.clip((7.0-_r[_ok])/5.4,0,1);_w=_w*_w*(3-2*_w);_g=G.ravel().astype(float);_g[_ok]=_g[_ok]*(1-_w)+_HH[_k[_ok]]*_w;G=_g.reshape(G.shape).astype(np.float32)
RAMP_STEIL=[]
for p,h in RAMPPROF:
    gp=nd.map_coordinates(G,[p[:,1]*RS,p[:,0]*RS],order=1);L=np.r_[0,np.cumsum(np.hypot(*np.diff(p,axis=0).T))]
    i=np.searchsorted(L,np.arange(0,L[-1],2.0));sl=np.degrees(np.arctan(np.abs(np.diff(gp[i]))/2.0)) if len(i)>1 else [0]
    RAMP_STEIL.append(round(float(np.max(sl)),1))
print('rampen_max_grad_je_2m',RAMP_STEIL)
wm=np.kron(wa,np.ones((RS,RS))).astype(float);Wn=np.kron(np.nan_to_num(Wsp),np.ones((RS,RS)))
lev=nd.gaussian_filter(Wn*wm,2)/np.maximum(nd.gaussian_filter(wm,2),1e-6)
wmask=nd.map_coordinates(nd.gaussian_filter(wm,1),[vj-0.5,vi-0.5],order=1,mode='nearest')>0.5
WV=np.where(wmask,np.maximum(nd.map_coordinates(lev,[vj-0.5,vi-0.5],order=1,mode='nearest'),G+0.05),-999).astype(np.float32)
# Dreiecke je Teilquadrat (a=oben links,b=oben rechts,c=unten links,d=unten rechts): (a,c,d) und (a,d,b) – gleich im Viewer
def tri_steil(G):
    a=G[:-1,:-1];b=G[:-1,1:];c=G[1:,:-1];d=G[1:,1:];s=1/RS
    def ny(dx1,dy1,dz1,dx2,dy2,dz2):
        n=np.stack([dy1*dz2-dz1*dy2,dz1*dx2-dx1*dz2,dx1*dy2-dy1*dx2]);return np.abs(n[1])/np.linalg.norm(n,axis=0)
    z0=np.zeros_like(a)
    n1=ny(z0,c-a,z0+s,z0+s,d-a,z0+s);n2=ny(z0+s,d-a,z0+s,z0+s,b-a,z0)
    return np.degrees(np.arccos(np.clip(n1,0,1))),np.degrees(np.arccos(np.clip(n2,0,1)))
W1,W2=tri_steil(G);Wq=np.maximum(W1,W2)                           # Neigung je Teilquadrat
neig=Wq.reshape(NY,RS,NX,RS).max((1,3))
steil=neig>WANDWINKEL
Hz=sum(G[dy:dy+GY-1:RS,dx:dx+GX-1:RS][:NY,:NX] for dy in range(3) for dx in range(3))/9    # Zellmittel 3x3 Punkte
Gmax=nd.maximum_filter(np.maximum.reduceat(np.maximum.reduceat(G,np.arange(0,GY-1,RS),0),np.arange(0,GX-1,RS),1)[:NY,:NX],5)
Gmin=nd.minimum_filter(np.minimum.reduceat(np.minimum.reduceat(G,np.arange(0,GY-1,RS),0),np.arange(0,GX-1,RS),1)[:NY,:NX],5)
nb=nd.binary_dilation(steil,structure=np.ones((3,3)))&~steil
mid=(Gmax+Gmin)/2
oben=nb&(Hz>=mid);fuss=nb&(Hz<mid)
kh=np.where(steil|nb,Gmax-Gmin,0.0)
C=np.stack([G[0:-1:RS,0:-1:RS][:NY,:NX],G[0:-1:RS,RS::RS][:NY,:NX],G[RS::RS,RS::RS][:NY,:NX],G[RS::RS,0:-1:RS][:NY,:NX]],-1)
# --- neuer Untergrund: Bandzellen sind jetzt Oberflaeche der oberen Ebene [F]
ug2=ug.copy();ug2[wand]='SCHNEE';ug2[wand&(wn=='Krater')&(nd.gaussian_filter(np.random.default_rng(5).standard_normal((NY,NX)),3)>0.25)]='FELS';ug2[ug=='SCHATTEN']='SCHNEE'
ug2[wa]='WASSER_EIS'
b3d_alt=A('begehbar_3d')=='1'
b3d=(neig<=35)&(b3d_alt|wand)&~(wa&(fl=='SEE'))
ebene2=eb.copy();ebene2[wand]=np.where(wn[wand]=='Nord','PLATEAU_NORD',np.where(wn[wand]=='Ostgrat','OSTPLATEAU',np.where(wn[wand]=='Krater','KRATERRAND','SENKE')))
kl=np.where(steil,'WAND',np.where(oben,'WAND_OBEN',np.where(fuss,'WAND_FUSS','')))
neu={'untergrund':ug2,'untergrund_quelle':np.where(ug2!=ug,'relief_t43u',A('untergrund_quelle')),'ebene':ebene2,'klippe':kl,
 'skin_slot':np.where(steil,'wand_fels',np.char.add('ug_',np.char.lower(ug2.astype(str)))),'hoehe_m':np.round(Hz,2),'hoehe_quelle':np.full((NY,NX),'R_relief_t43u'),
 'neigung_grad':np.round(neig,1),'klippe_hoehe_m':np.round(kh,1),'klippe_hoehe_quelle':np.where(kh>0,'R_messung_t40u','') ,
 'wasser_tiefe_m':np.where(wa,np.round(tiefe,2),0).astype(str),'begehbar_3d':b3d.astype(int),'wasser_eis':wa.astype(int).astype(str),'fluss_id':fl}
extra={'boden_hoehe_m':np.round(Hboden,2),'wasserspiegel_m':np.where(wa,np.round(np.nan_to_num(Wsp),2).astype(str),''),
 'ecke_nw_m':np.round(C[...,0],2),'ecke_no_m':np.round(C[...,1],2),'ecke_so_m':np.round(C[...,2],2),'ecke_sw_m':np.round(C[...,3],2),
 'ebene_c20':eb,'untergrund_c20':ug}
outcols=cols+list(extra)
F={c:(neu[c] if c in neu else extra[c] if c in extra else A(c)) for c in outcols}
with open('zellen_relief.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(outcols)
    for y in range(NY):
        for x in range(NX):w.writerow([F[c][y,x] for c in outcols])
# --- Mesh (gleiche Dreiecke + gleiche Wandregel wie Viewer) -> GLB mit "boden" (UV = c20-Draufsicht) und "waende"
import trimesh
V=np.stack([vi.ravel()/RS,G.ravel(),vj.ravel()/RS],1);UV=np.stack([vi.ravel()/RS/NX,1-vj.ravel()/RS/NY],1)
I=(np.arange(GY-1)[:,None]*GX+np.arange(GX-1)[None,:]);a=I;b=I+1;c=I+GX;d=I+GX+1
T1=np.stack([a,c,d],-1);T2=np.stack([a,d,b],-1)
TT=np.concatenate([T1.reshape(-1,3),T2.reshape(-1,3)]);ST=np.concatenate([W1.ravel(),W2.ravel()])>WANDWINKEL
sc=trimesh.Scene()
sc.add_geometry(trimesh.Trimesh(V,TT[~ST][:,::-1],process=False,visual=trimesh.visual.TextureVisuals(uv=UV)),'boden')
sc.add_geometry(trimesh.Trimesh(V,TT[ST][:,::-1],process=False),'waende')
sc.export('dorfmap_relief_z25.glb');TW=TT[ST]
# --- Objekte (Groessen wie t39u, nur auf neues Relief)
hc=lambda x,y:float(nd.map_coordinates(G,[[y*RS],[x*RS]],order=1,mode='nearest')[0])
OV=list(csv.DictReader(open(B+'raster_c20_z25_overlay_plaetze_wege.csv')))
weg=np.zeros((NY,NX),bool);br=np.zeros((NY,NX),bool);deko=np.zeros((NY,NX),bool)
for o in OV:
    x,y=int(o['cx']),int(o['cy']);weg[y,x]|=bool(o['weg_id']);br[y,x]|=o['bruecke']=='1';deko[y,x]|=o['dekoplaetze_netz']=='1'
rng=lambda x,y,s:((x*73856093)^(y*19349663)^(s*83492791))%10007/10007.0
Pl=json.load(open(B+'pruefung/quelle_plaetze_wachstum_ausbau_planm.json'))['E40'];belegt=np.zeros((NY,NX),bool);haeuser=[]
HH={'Hütte':3,'kompakt':4,'schmal':5,'Standard':5,'Doppelhaus':5,'Eckhaus':6,'Turmhaus':9,'FUNKTION':7,'Quartiersplatz':0.15}
for p in Pl:
    q=np.array([[(x+200)*1.2,(y+40)*1.2] for x,y in p['poly']]);x0,y0=q.min(0);x1,y1=q.max(0)
    ix=slice(max(0,int(x0)),min(NX,int(np.ceil(x1))));iy=slice(max(0,int(y0)),min(NY,int(np.ceil(y1))));belegt[iy,ix]=1
    t=p['typ'];k='FUNKTION' if t.startswith('FUNKTION') else t
    gg=G[iy.start*RS:iy.stop*RS+1,ix.start*RS:ix.stop*RS+1];g=float(np.median(gg)) if gg.size else 0
    haeuser.append({'id':p['id'],'typ':t,'x':round((x0+x1)/2,2),'z':round((y0+y1)/2,2),'b':round(x1-x0,2),'t':round(y1-y0,2),'h':HH[k],'y':round(g,2)})
# t43u: Objekte in Gruppen (Dichte aus weichem Rauschen), Groessen-/Drehvarianz, Kraterrand duenner, Geroell am Wandfuss [A]
rs2=np.random.default_rng(43);dich=nd.gaussian_filter(rs2.standard_normal((NY,NX)),4);dich/=dich.std()
baeume=[];felsen=[];steine=[];geroell=[]
for y in range(NY):
    for x in range(NX):
        if belegt[y,x] or weg[y,x] or steil[y,x]:continue
        u=rs2.random(5)
        if ug2[y,x]=='WALD' and u[0]<0.22*np.clip(0.6+0.8*dich[y,x],0,1.6):
            X,Z=min(x+u[1],NX-0.5),min(y+u[2],NY-0.5);baeume.append([round(X,2),round(hc(X,Z),2),round(Z,2),round(5+6*u[3]**1.5,1),round(u[4]*6.28,2),round(rs2.random(),2)])
        if ug2[y,x]=='FELS' and u[0]<(0.05 if wn[y,x]=='Krater' else 0.09)*np.clip(0.5+dich[y,x],0,2):
            s=0.5+1.6*u[3]**2;X,Z=x+u[1],y+u[2];felsen.append([round(X,2),round(hc(X,Z)-0.25*s,2),round(Z,2),round(s,2),round(u[4]*6.28,2)])
        if deko[y,x] and not wa[y,x] and u[0]<0.5:X,Z=x+u[1],y+u[2];steine.append([round(X,2),round(hc(X,Z)-0.1,2),round(Z,2),round(0.3+0.5*u[3],2),round(u[4]*6.28,2)])
        if fuss[y,x] and not wa[y,x] and u[0]<0.18:
            for _ in range(1+int(u[3]*3)):
                v=rs2.random(4);s=0.2+0.6*v[2]**2;X,Z=x+v[0],y+v[1];geroell.append([round(X,2),round(hc(X,Z)-0.2*s,2),round(Z,2),round(s,2),round(v[3]*6.28,2)])
# t48u: Ufersteine, Baumgruppen an Klippenkanten, Trockengras-Bueschel [A]
ufr=nd.binary_dilation(wa,iterations=1)&~wa&~belegt&~steil;kante=nd.binary_dilation(steil,iterations=4)&~nd.binary_dilation(steil,iterations=1)&~belegt&~wa&~weg
hoch=nd.maximum_filter(Hz,7)-Hz<1.0;gras=[];r48=np.random.default_rng(481);grp_=nd.gaussian_filter(r48.standard_normal((NY,NX)),2.5);grp_/=grp_.std()
for y,x in np.argwhere(ufr):
    u=r48.random(4)
    if u[0]<0.45:X,Z=x+u[1],y+u[2];s=0.25+0.7*u[3]**2;steine.append([round(X,2),round(hc(X,Z)-0.15*s,2),round(Z,2),round(s,2),round(u[0]*14,2)])
for y,x in np.argwhere(kante&hoch&(grp_>0.6)):
    u=r48.random(6)
    if u[0]<0.55:X,Z=x+u[1],y+u[2];baeume.append([round(X,2),round(hc(X,Z),2),round(Z,2),round(5+7*u[3]**1.3,1),round(u[4]*6.28,2),round(u[5],2)])
for y,x in np.argwhere((ug2=='SCHNEE')&~belegt&~weg&~steil&~wa):
    u=r48.random(5)
    if u[0]<0.10*np.clip(grp_[y,x]+0.6,0,2):X,Z=x+u[1],y+u[2];gras.append([round(X,2),round(hc(X,Z),2),round(Z,2),round(0.35+0.5*u[3],2),round(u[4]*6.28,2)])
# t48u: Felsbloecke/Felsplatten entlang aller Wandbaender (eigene Meshes, Instancing) [A]
gzy,gzx=np.gradient(Hz);bl_r=np.random.default_rng(48);felsbloecke=[]
for y,x in np.argwhere(steil&~wa):
    u=bl_r.random(7)
    if True:continue   # t54u: keine Blockinstanzen mehr als Wandform (Fels = Feinrelief FW) [A]
    nx_,nz_=-gzx[y,x],-gzy[y,x];l=np.hypot(nx_,nz_)+1e-6;nx_/=l;nz_/=l   # Blick talwaerts
    X,Z=x+0.5+0.6*(u[1]-0.5),y+0.5+0.6*(u[2]-0.5);Y=hc(X,Z)
    gr=0.45 if u[6]<0.3 else (1.0 if u[6]<0.85 else 1.45)   # t48u R5: Groessenmix klein/mittel/gross [A]
    sx=gr*(2.0+3.8*u[3]**1.3);sy=gr*(1.2+3.0*u[4]**1.5);sz=gr*(1.3+1.6*u[5])
    felsbloecke.append([round(X+0.35*nx_,2),round(Y-0.25*sy,2),round(Z+0.35*nz_,2),round(sx,2),round(sy,2),round(sz,2),round(float(np.arctan2(nx_,nz_)),3),round(u[6]-0.5,2)])
# t53u R1: Ueberhaenge = flache Blender-Felsplatten an der Wandkrone, 1-2 m ueber die Kante talwaerts auskragend [A]
UEBERHANG=0;_ohr=np.random.default_rng(531);_kr2=oben&nd.binary_dilation(steil,iterations=1)&~wa&~belegt&~weg&~nd.binary_dilation(wa,iterations=4)
for y,x in np.argwhere(_kr2):
    u=_ohr.random(6)
    if True:continue   # t54u: Ueberhang-Platten entfernt (Blockhaufen-Eindruck)
    nx_,nz_=-gzx[y,x],-gzy[y,x];l=np.hypot(nx_,nz_)+1e-6;nx_/=l;nz_/=l
    X,Z=x+0.5,y+0.5;Y=float(Gmax[y,x]) if False else hc(X,Z);ko=1.0+1.0*u[1]
    sx=3.0+3.5*u[2];sy=0.9+0.9*u[3];sz=2.2+1.8*u[4]
    felsbloecke.append([round(X+ko*nx_,2),round(Y-0.45*sy,2),round(Z+ko*nz_,2),round(sx,2),round(sy,2),round(sz,2),round(float(np.arctan2(nx_,nz_)),3),round(u[5]-0.5,2)]);UEBERHANG+=1
print('ueberhaenge',UEBERHANG)
lab,n=nd.label(ha=='MASKE');findlinge=[]
for i,s in enumerate(nd.find_objects(lab)):
    m=lab[s]==i+1;cy,cx=nd.center_of_mass(m);a=int(m.sum());X,Z=s[1].start+cx+.5,s[0].start+cy+.5
    findlinge.append([round(X,2),round(hc(X,Z),2),round(Z,2),round(.6*np.sqrt(a),2),round(rng(int(X),int(Z),7)*6.28,2)])
bruecken=[[x+.5,round(float(Hboden[y,x])+0.3,2),y+.5] for y,x in zip(*np.nonzero(br))]
wege=[[int(x),int(y)] for y,x in zip(*np.nonzero(weg))]
start=[h for h in haeuser if h['typ']=='FUNKTION:Starthaus'][0]
# Wandfuss Nordwand naechst Start: Zelle mit Nordnachbar >=10 m hoeher
fz=[(abs(x-start['x'])+abs(y-start['z']),x,y) for y in range(1,NY) for x in range(NX) if wn[y-1,x]=='Nord' and H[y-1,x]-H[y,x]>=10 and abs(H[y,x])<1 and not wa[y,x]]
obj=[(o[0],o[2]) for L in (baeume,felsen,findlinge,steine) for o in L]+[(h['x'],h['z']) for h in haeuser]
frei=lambda x,y:not any(abs(ox-x-.5)<2.5 and 0<oz-y<15 for ox,oz in obj) and not wa[y:y+15,max(0,x-1):x+2].any() and np.abs(H[y:y+15,max(0,x-1):x+2]-H[y,x]).max()<2
fz=sorted(fz);_,fx,fy=next(f for f in fz if frei(f[1],f[2]))
spalten={}
for c in outcols:
    u,idx=np.unique(F[c].astype(str).ravel(),return_inverse=True);dt=np.uint8 if len(u)<256 else np.uint16 if len(u)<65536 else np.uint32
    spalten[c]={'w':u.tolist(),'t':dt.__name__,'i':base64.b64encode(idx.astype(dt).tobytes()).decode()}
b64=lambda a:base64.b64encode(np.ascontiguousarray(a,np.float32).tobytes()).decode()
# t43u: Bodenfarbe je Vertex aus Zelleigenschaften (Splat-Gewichte, weich), c20 nur als schwache Toenung (12 %) [A]
from PIL import Image
up=lambda M,s=1.5:nd.map_coordinates(nd.gaussian_filter(np.kron(M.astype(float),np.ones((RS,RS))),s*RS),[vj-0.5,vi-0.5],order=1,mode='nearest')
nz=lambda s,sd:(lambda a:a/a.std())(nd.gaussian_filter(np.random.default_rng(sd).standard_normal((GY,GX)),s))
MAT={'SCHNEE':(0.88,0.91,0.95),'WALD':(0.70,0.74,0.69),'FELS':(0.52,0.49,0.46),'BODEN':(0.47,0.37,0.27),'SAND':(0.78,0.69,0.53),'WASSER_EIS':(0.66,0.76,0.82)}
gew={k:up(ug2==k)*(1+0.35*nz(4,i))**2 for i,k in enumerate(MAT)}
gew['MOOS']=up(ug2=='WALD',3.0)*np.clip(nz(3,31),0,None)*0.8;MAT['MOOS']=(0.36,0.42,0.27)   # Moos/Nadelstreu am Waldrand [A]
gew['ERDE2']=up(np.isin(ug2,['BODEN','FELS']),2.0)*np.clip(nz(2,33)-0.6,0,None)*0.7;MAT['ERDE2']=(0.38,0.30,0.22)
gew['GEROELL']=up(fuss|steil,1.0)*0.9*(1+0.4*nz(2,11)).clip(0);MAT['GEROELL']=(0.55,0.53,0.50)
_gn=0.6*nz(6,51)+0.4*nz(1.5,52);_sl=np.hypot(*np.gradient(G))*RS   # t48u: fleckiger Schnee – Trockengras/Moos schaut durch, mehr an Kuppen/Hangkanten [A]
gew['GRAS']=up(ug2=='SCHNEE')*np.clip(_gn-0.75+0.5*np.clip(_sl-0.3,0,1),0,None)*2.8;MAT['GRAS']=(0.50,0.47,0.31)
gew['MOOS2']=up(ug2=='SCHNEE')*np.clip(nz(2.5,53)-1.3,0,None)*gew['GRAS'].clip(0,1)*3;MAT['MOOS2']=(0.30,0.36,0.24)
gew['NASS']=np.clip(up(wa,1.0)-0.05,0,1)*0.6;MAT['NASS']=(0.40,0.45,0.48)
S=sum(gew.values())+1e-6;col=sum(np.array(MAT[k])[None,None,:]*(gew[k]/S)[...,None] for k in gew)
c20=np.asarray(Image.open('../_alt/modell3d_t36u/textur_c20_8px.jpg').convert('RGB').resize((GX,GY),Image.BILINEAR)).astype(float)/255
c20=np.stack([nd.gaussian_filter(c20[...,c],6) for c in range(3)],-1);ton=c20/np.maximum(c20.mean(-1,keepdims=True),1e-3)
gzv,gxv=np.gradient(G);weh=np.clip(0.5+0.8*nz(10,41)+0.6*np.tanh(gzv*3),0,1);sn=gew['SCHNEE']/S
col=col*(1-sn*0.10*weh)[...,None]+(sn*0.10*weh)[...,None]*np.array([0.70,0.80,0.95])
col=col*(1+0.12*(ton-1))*(1+0.05*nz(1.5,21))[...,None]
VC=(np.clip(col,0,1)*255).astype(np.uint8)
# t48u R5: GLB neu mit Vertexfarben (boden+waende), fuer GLTFLoader-Pfad im Viewer (?glb=1 ueber lokalen Server) [A]
_vc=np.concatenate([VC.reshape(-1,3),np.full((VC.reshape(-1,3).shape[0],1),255,np.uint8)],1)
sc=trimesh.Scene()
sc.add_geometry(trimesh.Trimesh(V,TT[~ST][:,::-1],process=False,vertex_colors=_vc),'boden')
sc.add_geometry(trimesh.Trimesh(V,TT[ST][:,::-1],process=False,vertex_colors=_vc),'waende')
sc.export('dorfmap_relief_z25.glb')
# t54u: Feinrelief der Wandbaender (0,25 m) als zusammenhaengende Felsform; nur Anzeige, Zellwerte bleiben aus G [A]
FS=4;FXn,FYn=NX*FS+1,NY*FS+1
_rkd=cKDTree(np.concatenate([p for p,_ in RAMPPROF]));_cc=np.stack(np.meshgrid(np.arange(NX)+0.5,np.arange(NY)+0.5),-1).reshape(-1,2)
_nahr=(_rkd.query(_cc,distance_upper_bound=4.5)[0]<9).reshape(NY,NX)
BAND=nd.binary_dilation(steil|oben|fuss,iterations=1)&~nd.binary_dilation(wa,iterations=1)&~belegt&~_nahr
BAND=nd.binary_opening(BAND,iterations=1)|(BAND&steil)
_fy,_fx=np.mgrid[0:FYn,0:FXn].astype(float);_gx=_fx/FS*RS;_gy=_fy/FS*RS
_i=np.minimum(_gx.astype(int),GX-2);_j=np.minimum(_gy.astype(int),GY-2);_ax=_gx-_i;_az=_gy-_j
_A=G[_j,_i];_B=G[_j,_i+1];_C=G[_j+1,_i];_D=G[_j+1,_i+1]
FB=np.where(_az>=_ax,_A+_az*(_C-_A)+_ax*(_D-_C),_A+_ax*(_B-_A)+_az*(_D-_B))       # exakt die G-Dreiecke
_qb=np.kron(BAND,np.ones((FS,FS),bool));_qp=np.pad(_qb,1)
_vin=_qp[:-1,:-1]&_qp[:-1,1:]&_qp[1:,:-1]&_qp[1:,1:]                                   # Vertex innen (alle 4 Quads im Band)
_wf=nd.distance_transform_edt(_vin)/10.0;_wf=np.clip(_wf,0,1);_wf=_wf*_wf*(3-2*_wf)
def _ff(sig,seed):
    r=np.random.default_rng(seed);n=nd.gaussian_filter(r.standard_normal((FYn,FXn)).astype(np.float32),sig);return n/n.std()
_wy=_fy+16*_ff(30,61);_wx=_fx+16*_ff(30,62)
_R=sum(a*(1-np.abs(np.clip(nd.map_coordinates(_ff(sg,sd),[_wy,_wx],order=1,mode='reflect')/2.0,-1,1))) for a,sg,sd in ((0.5,18,63),(0.3,8,64),(0.2,3.5,65)))
_R=(_R-_R.min())/(_R.max()-_R.min())
_sgy,_sgx=np.gradient(FB,1/FS);_sl=np.degrees(np.arctan(np.hypot(_sgx,_sgy)));_sf=np.clip((nd.gaussian_filter(_sl,3)-20)/35,0,1)
_ph=(FB+1.8*_ff(40,66)+0.6*_ff(10,67))/2.6;_fr=_ph-np.floor(_ph);_st=np.clip((_fr-0.15)/0.7,0,1)**2   # Schichtung: Baender/Absaetze
FD=_wf*(_sf*(2.4*_R**1.6+0.9*_st+0.25)+(1-_sf)*(0.9*_R**2))
FH=FB+FD
_fe=_vin&(_wf>0)                                                  # thermische Glaettung gegen Zacken (Grenzwinkel 72 Grad)
_tl=np.tan(np.radians(72))/FS
for _ in range(12):
    for ax,sh in ((0,1),(0,-1),(1,1),(1,-1)):
        Nb=np.roll(FH,sh,axis=ax);ex=np.where(_fe&np.roll(_fe,sh,axis=ax),np.clip(FH-Nb-_tl,0,None)*0.25,0);FH-=ex;FH+=np.roll(ex,-sh,axis=ax)
FH=np.maximum(FH,FB);FH=np.where(_vin,FH,FB)
_ap=nd.gaussian_filter(FH,8)-0.15;FH=np.where(_vin,np.maximum(FH,_wf*_ap+(1-_wf)*FH),FB)   # t54u-A: Schuttfuss/Kehlen fuellen -> flachere Fuesse
_fv=np.argwhere(_qb.any() and np.ones(1,bool))  # Platzhalter
_used=np.zeros((FYn,FXn),bool);_used[:-1,:-1]|=_qb;_used[1:,:-1]|=_qb;_used[:-1,1:]|=_qb;_used[1:,1:]|=_qb
_vid=np.flatnonzero(_used.ravel()).astype(np.uint32)
_vcf=np.stack([nd.map_coordinates(VC.reshape(GY,GX,3)[...,c].astype(float),[_gy.ravel()[_vid],_gx.ravel()[_vid]],order=1) for c in range(3)],1)
FW={'fs':FS,'band':base64.b64encode(np.flatnonzero(BAND.ravel()).astype(np.uint32).tobytes()).decode(),'vid':base64.b64encode(_vid.tobytes()).decode(),
    'h':base64.b64encode(FH.ravel()[_vid].astype(np.float32).tobytes()).decode(),'c':base64.b64encode(np.clip(_vcf,0,255).astype(np.uint8).tobytes()).decode()}
_fsl=np.degrees(np.arctan(np.hypot(*np.gradient(FH,1/FS))))
FW_MESS={'band_zellen':int(BAND.sum()),'dreiecke_voll':int(BAND.sum()*FS*FS*2),'neigung_steilband_mittel':round(float(_fsl[_vin&(_sf>0.5)].mean()),1),
 'neigung_p10_p90':[round(float(np.percentile(_fsl[_vin&(_sf>0.5)],q)),1) for q in (10,90)],'versatz_max_m':round(float(FD.max()),2)}
print('feinrelief',FW_MESS)
WEGA=(np.clip(up(weg,0.6)*1.6,0,1)*255).astype(np.uint8)
D={'nx':NX,'ny':NY,'G':b64(G),'VC':base64.b64encode(VC.tobytes()).decode(),'WEGA':base64.b64encode(WEGA.tobytes()).decode(),'geroell':geroell,'felsbloecke':felsbloecke,'gras':gras,'felsmesh':(json.load(open('blender/fels_meshes.json')) if os.path.exists('blender/fels_meshes.json') else []),'rampenwege':RAMPWEGE,'WV':b64(WV),'rs':RS,'wandwinkel':WANDWINKEL,'ug':spalten['untergrund'],'sprung':SPRUNG,'spalten':spalten,'reihenfolge':outcols,
 'haeuser':haeuser,'baeume':baeume,'felsen':felsen,'findlinge':findlinge,'steine':steine,'bruecken':bruecken,'wege':wege,'start':start,
 'wandfuss':{'x':fx+.5,'z':fy+.5,'h':round(float(H[fy-1,fx]-H[fy,fx]),1),'zelle':int(fy*NX+fx)},'wandhoehen':WANDH,'FW':FW}
open('relief_daten.json.gz','wb').write(gzip.compress(json.dumps(D,ensure_ascii=False).encode(),9))
Z={k:len(D[k]) for k in ['haeuser','baeume','felsen','findlinge','steine','bruecken','wege']}
Z.update(wand_dreiecke=int(len(TW)),boden_dreiecke=int((~ST).sum()),zellen_wand_steil=int(steil.sum()),
 zellen_wand_oben=int(oben.sum()),zellen_wand_fuss=int(fuss.sum()),hoehe_min=float(H.min()),hoehe_max=float(H.max()),wandfuss=D['wandfuss'],
 klippe_hoehe_median_3x3_je_wand={w:round(float(np.median((nd.maximum_filter(Hz,3)-nd.minimum_filter(Hz,3))[steil&nd.binary_dilation(wn==w,iterations=3)])),2) for w in WANDH},   # t44u: nur Abbruch, ohne Hang am Fuss
 klippe_hoehe_median_je_wand={w:round(float(np.median(kh[steil&nd.binary_dilation(wn==w,iterations=3)])),2) for w in WANDH},
 bandzellen_umgedeutet=int(wand.sum()),begehbar_3d=int(b3d.sum()))
json.dump(Z,open('relief_zaehlung.json','w'),indent=1,ensure_ascii=False);print(json.dumps(Z,ensure_ascii=False))
