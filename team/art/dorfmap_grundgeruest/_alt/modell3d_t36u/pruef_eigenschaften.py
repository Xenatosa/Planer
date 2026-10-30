# t36u: prueft GLB + Sidecar gegen das Raster (Quelle). Erwartet 0 Abweichungen.
import csv,numpy as np,pygltflib as G,json
NX,NY=336,303
R={int(r['cy'])*NX+int(r['cx']):r for r in csv.DictReader(open('../raster_c20_z25_zellen.csv'))}
S={int(r['zell_id']):r for r in csv.DictReader(open('zellen_eigenschaften.csv'))}
ab={'sidecar_fehlt':0,'sidecar_feld_abw':0,'glb_zelle_fehlt':0,'glb_zelle_doppelt':0,'glb_gruppe_falsch':0,'glb_ecke_ausserhalb_zelle':0,'uv1_falsch':0}
for k,r in R.items():
    s=S.get(k)
    if s is None: ab['sidecar_fehlt']+=1;continue
    ab['sidecar_feld_abw']+=sum(s[f]!=r[f] for f in r)
gl=G.GLTF2().load_binary('dorfmap_c20_z25.glb');blob=gl.binary_blob()
def lese(i,n):
    a=gl.accessors[i];bv=gl.bufferViews[a.bufferView];dt={5126:np.float32,5125:np.uint32}[a.componentType]
    return np.frombuffer(blob,dt,a.count*n,bv.byteOffset+(a.byteOffset or 0)).reshape(a.count,n)
gesehen={}
for m in gl.meshes:
    p=m.primitives[0];P=lese(p.attributes.POSITION,3);ID=lese(p.attributes._ZELL_ID,1)[:,0].astype(int);U=lese(p.attributes.TEXCOORD_1,2)
    if m.name in('SOCKEL',): continue
    for q in range(0,len(ID),4):
        i=ID[q];cx,cy=i%NX,i//NX
        if m.name!='WASSER_OBERFLAECHE':
            gesehen[i]=gesehen.get(i,0)+1
            if R[i]['untergrund']!=m.name: ab['glb_gruppe_falsch']+=1
        elif R[i]['wasser_eis']!='1': ab['glb_gruppe_falsch']+=1
        if not ((P[q:q+4,0]>=cx-1e-4)&(P[q:q+4,0]<=cx+1+1e-4)&(P[q:q+4,2]>=cy-1e-4)&(P[q:q+4,2]<=cy+1+1e-4)).all() or (ID[q:q+4]!=i).any(): ab['glb_ecke_ausserhalb_zelle']+=1
        if not np.allclose(U[q:q+4],[[0,0],[1,0],[1,1],[0,1]]): ab['uv1_falsch']+=1
ab['glb_zelle_fehlt']=sum(k not in gesehen for k in R);ab['glb_zelle_doppelt']=sum(v>1 for v in gesehen.values())
ab['zellen_raster']=len(R);ab['summe_abweichungen']=sum(v for k,v in ab.items() if k!='zellen_raster')
json.dump(ab,open('pruefung_eigenschaften.json','w'),indent=1);print(ab)
