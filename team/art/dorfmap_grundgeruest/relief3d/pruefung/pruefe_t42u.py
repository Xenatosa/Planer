# t42u Abgleich: CSV-Eigenschaften je Zelle gegen Hoehenfeld G (relief_daten.json.gz) und GLB neu ableiten -> 0 Abweichungen erwartet
import csv,json,gzip,base64,numpy as np,trimesh
D=json.load(gzip.open('relief_daten.json.gz'));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
G=np.frombuffer(base64.b64decode(D['G']),np.float32).reshape(GY,GX).astype(float)
R=list(csv.DictReader(open('zellen_relief.csv')));A=lambda k:np.array([r[k] for r in R]).reshape(NY,NX)
a=G[:-1,:-1];b=G[:-1,1:];c=G[1:,:-1];d=G[1:,1:];s=1/RS
def ang(P,Q,S):
    u=Q-P;v=S-P;n=np.cross(u,v);return np.degrees(np.arccos(np.abs(n[...,1])/np.linalg.norm(n,axis=-1)))
X,Z=np.meshgrid(np.arange(GX-1)*s,np.arange(GY-1)*s);P=lambda x,y,h:np.stack([x,h,y],-1)
t1=ang(P(X,Z,a),P(X,Z+s,c),P(X+s,Z+s,d));t2=ang(P(X,Z,a),P(X+s,Z+s,d),P(X+s,Z,b))
steil=(np.maximum(t1,t2).reshape(NY,RS,NX,RS).max((1,3)))>D['wandwinkel']
Hz=sum(G[dy:dy+GY-1:RS,dx:dx+GX-1:RS][:NY,:NX] for dy in range(3) for dx in range(3))/9
kl=A('klippe');ss=A('skin_slot');ug=A('untergrund')
E={}
E['hoehe_m']=int((np.abs(A('hoehe_m').astype(float)-Hz)>0.006).sum())
E['ecke_nw_m']=int((np.abs(A('ecke_nw_m').astype(float)-G[0:-1:RS,0:-1:RS][:NY,:NX])>0.006).sum())
E['ecke_so_m']=int((np.abs(A('ecke_so_m').astype(float)-G[RS::RS,RS::RS])>0.006).sum())
E['klippe_WAND_vs_steil']=int(((kl=='WAND')!=steil).sum())
soll=np.where(steil,'wand_fels',np.char.add('ug_',np.char.lower(ug.astype(str))))
E['skin_slot']=int((ss!=soll).sum())
E['zell_id']=int((A('zell_id').astype(int)!=np.arange(NX*NY).reshape(NY,NX)).sum())
E['begehbar_auf_wand']=int(((A('begehbar_3d')=='1')&steil).sum())
g=trimesh.load('dorfmap_relief_z25.glb');n={nd_:len(g.geometry[g.graph[nd_][1]].faces) for nd_ in g.graph.nodes_geometry}
ges=2*(GX-1)*(GY-1);E['glb_dreiecke_summe']=int(n['boden']+n['waende']-ges)
wm=int((np.concatenate([t1.ravel(),t2.ravel()])>D['wandwinkel']).sum());E['glb_waende_vs_regel']=int(n['waende']-wm)
out={'abweichungen':E,'summe':sum(abs(v) for v in E.values()),'glb':n,'zellen':NX*NY,'steile_zellen':int(steil.sum())}
json.dump(out,open('pruefung/abgleich_t42u.json','w'),indent=1);print(json.dumps(out))
