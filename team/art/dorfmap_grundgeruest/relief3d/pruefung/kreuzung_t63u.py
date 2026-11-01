# t63u Runde K [S]: Kreuzungen Wasser x Wege (Zellen), Rampen/Serpentinen, Haeuser (Grundriss), Bauplaetze/Plaetze (Overlay) - nur fuer neues Wasser und gesamt
import json,gzip,base64,sys,csv,numpy as np
def lade(p):
    D=json.load(gzip.open(p));return D,np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(607,673)>-900
Dj,Wj=lade(sys.argv[1]);Dk,Wk=lade(sys.argv[2]);NEU=Wk&~Wj
def zaehl(D,M):
    inn=lambda x,z:(lambda i,j:0<=j<607 and 0<=i<673 and M[j,i])(int(round(x*2)),int(round(z*2)))
    wz=sum(1 for c in D['wege'] if any(M[min(606,2*c[1]+a),min(672,2*c[0]+b)] for a in (0,1,2) for b in (0,1,2)))
    rp=sum(1 for r in D['rampenwege'] for x,z in r if inn(x,z))
    hs=0
    for h in D['haeuser']:
        x0,x1,z0,z1=h['x']-h['b']/2,h['x']+h['b']/2,h['z']-h['t']/2,h['z']+h['t']/2
        if M[max(0,int(z0*2)):int(z1*2)+1,max(0,int(x0*2)):int(x1*2)+1].any():hs+=1
    O=list(csv.DictReader(open('../raster_c20_z25_overlay_plaetze_wege.csv')))
    ov=lambda k:sum(1 for r in O if r[k] not in('','0') and M[2*int(r['cy'])+1,2*int(r['cx'])+1])
    return {'wegzellen':wz,'rampen_serpentinen_punkte':rp,'haeuser_grundriss_achsparallel':hs,'overlay_bauplatz':ov('bauplatz'),'overlay_platz':ov('platz'),'overlay_weg':ov('weg_id'),'overlay_bruecke':ov('bruecke'),'overlay_furt':ov('furt')}
R={'neues_wasser_vertices':int(NEU.sum()),'kreuzung_neues_wasser':zaehl(Dk,NEU),'wasser_gesamt_runde_J':zaehl(Dj,Wj),'wasser_gesamt_runde_K':zaehl(Dk,Wk),
   'hinweis':'Overlay (c20) deckt nur x>=141 ab; der Westarm liegt bei x<100 -> dort keine Overlay-Wege/Bauplaetze. Wegzellen = relief_daten wege (Zellraster), Haus-Grundriss ohne Drehung (grob, eher zu viel).'}
json.dump(R,open(sys.argv[3],'w'),indent=1);print(json.dumps(R))
