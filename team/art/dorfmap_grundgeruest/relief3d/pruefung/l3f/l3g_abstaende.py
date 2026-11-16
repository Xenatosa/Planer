# L3g Abstands- und Wassernachweis: Basis = relief_daten.json.gz von 8c1fc80 (Stand nach Schritt 14, Pfad unten), nachher = Arbeitsstand.
import sys,json,gzip,base64,hashlib,numpy as np,scipy.ndimage as nd
sys.path.insert(0,'.');import relief_l3 as L3
from matplotlib.path import Path as MP
A=json.load(gzip.open('/tmp/l3f/rd_8c1.gz'));B=json.load(gzip.open('relief_daten.json.gz'))
rs=A['rs'];GY,GX=A['ny']*rs+1,A['nx']*rs+1
g=lambda D,k,t,sh:np.frombuffer(base64.b64decode(D[k]),t).reshape(sh)
GA,GB_=g(A,'GB',np.float32,(GY,GX)),g(B,'GB',np.float32,(GY,GX))
WA,WB=g(A,'WV',np.float32,(GY,GX)),g(B,'WV',np.float32,(GY,GX))
VA,VB=g(A,'VC',np.uint8,(GY,GX,3)),g(B,'VC',np.uint8,(GY,GX,3))
ge=(GA!=GB_)|(WA!=WB)|(VA!=VB).any(-1)
V=json.load(open('neu/vektor.json'));zw=float(V['karte']['zellweite_m'])
def lin(P,step=0.1):
    L=np.r_[0.0,np.cumsum(np.hypot(*np.diff(P,axis=0).T))];t=np.arange(0,L[-1]+1e-9,step);m=np.zeros((GY,GX),bool)
    m[np.clip(np.rint(np.interp(t,L,P[:,1])*rs).astype(int),0,GY-1),np.clip(np.rint(np.interp(t,L,P[:,0])*rs).astype(int),0,GX-1)]=True;return m
weg=np.zeros((GY,GX),bool)
for w in V['wege']:
    P=np.asarray(w['mittellinie_m'],float)/zw
    if len(P)>=2: weg|=nd.distance_transform_edt(~lin(P),sampling=1/rs)<=w['breite_m']/zw/2
zz,xx=np.mgrid[0:GY,0:GX]/rs;pts=np.c_[xx.ravel(),zz.ravel()];kr=np.zeros((GY,GX),bool)
for k in V['kreuzungen']: kr|=MP(np.asarray(k['polygon_m'],float)/zw).contains_points(pts).reshape(GY,GX)
ram=np.zeros((GY,GX),bool)
for p in A.get('rampenwege',[]):
    P=np.asarray(p,float)[:,:2]
    if len(P)>=2: ram|=lin(P)
ram=nd.distance_transform_edt(~ram,sampling=1/rs)<=1.8
wega=g(A,'WEGA',np.uint8,(GY,GX))>0
for x,z in A['wege']: wega[z*rs:z*rs+rs+1,x*rs:x*rs+rs+1]=True
x0,z0,x1,z1=L3.D2_BOX;d2=np.zeros((GY,GX),bool);d2[z0*rs:z1*rs+1,x0*rs:x1*rs+1]=True
mA=WA>-900;mB=WB>-900
out={'geaenderte_vertices':int(ge.sum()),'gb':int((GA!=GB_).sum()),'wv':int((WA!=WB).sum()),'vc':int((VA!=VB).any(-1).sum()),'zellweite_m':zw,'je_flaeche':{}}
for n,M in (('weg_vektor',weg),('kreuzung',kr),('rampenkern',ram),('WEGA_wege_bruecken',wega),('D2',d2)):
    d=nd.distance_transform_edt(~M,sampling=1/rs)[ge]
    out['je_flaeche'][n]={'geaenderte_vertices_darauf':int((ge&M).sum()),'kleinster_abstand_zellen':round(float(d.min()),2),'kleinster_abstand_m':round(float(d.min())*zw,2)}
out['wasser']={'gb_unter_wasser_geaendert':int(((GA!=GB_)&mA).sum()),'maske_gleich':bool((mA==mB).all()),'wv_gleich':bool((WA==WB).all()),
 'komponenten':[int(nd.label(mA,np.ones((3,3)))[1]),int(nd.label(mB,np.ones((3,3)))[1])],
 'fill_holes_gleich':bool((nd.binary_fill_holes(mA)==nd.binary_fill_holes(mB)).all()),
 'bett_ueber_spiegel_vorher_nachher':[int((GA[mA]>=WA[mA]).sum()),int((GB_[mB]>=WB[mB]).sum())]}
sh=lambda a:hashlib.sha256(a.tobytes()).hexdigest()
out['D2_gb_sha256']=[sh(GA[d2.nonzero()]),sh(GB_[d2.nonzero()])]
out['D2_slice_sha']=[sh(np.ascontiguousarray(GA[z0*rs:z1*rs+1,x0*rs:x1*rs+1])),sh(np.ascontiguousarray(GB_[z0*rs:z1*rs+1,x0*rs:x1*rs+1]))]
zs,xs=np.nonzero(ge);out['box_geaendert_zellen']=[float(xs.min()/rs),float(zs.min()/rs),float(xs.max()/rs),float(zs.max()/rs)]
for n,(x,z) in (('sperr_D1_mulde_159_22.9',(159,22.9)),):
    out[n+'_abstand_zellen']=round(float(np.hypot(xs/rs-x,zs/rs-z).min()),1)
ws=[w for w in V['wege'] if w.get('id')=='rampe_2']
print(json.dumps(out,indent=1))
fd=nd.binary_fill_holes(mB)^nd.binary_fill_holes(mA);zz,xx=np.nonzero(fd)
neu=mB&~mA;zn,xn=np.nonzero(neu)
lab,n=nd.label(neu,np.ones((3,3)))
gr=[]
for k in range(1,n+1):
    a,b=np.nonzero(lab==k);gr.append([round(b.mean()/rs,1),round(a.mean()/rs,1),int(len(a))])
print(json.dumps({'fill_holes_diff_vertices':int(fd.sum()),'fill_holes_diff_box':[float(xx.min()/rs),float(zz.min()/rs),float(xx.max()/rs),float(zz.max()/rs)] if fd.any() else None,
 'neues_wasser_gruppen_x_z_n':gr,'wasser_entfernt':int((mA&~mB).sum()),
 'wv_alt_wasser_geaendert':int(((WA!=WB)&mA).sum()),'wv_alt_wasser_geaendert_box':[float(np.nonzero((WA!=WB)&mA)[1].min()/rs),float(np.nonzero((WA!=WB)&mA)[0].min()/rs)] if ((WA!=WB)&mA).any() else None}))
