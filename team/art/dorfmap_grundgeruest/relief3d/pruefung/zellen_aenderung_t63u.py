# t63u Runde K [S]: Zell-Aenderungsliste alt (git 18f24ac) -> neu, plus Kreuzungen neues Wasser x Weg/Bauplatz/Platz/Bruecke/Furt/Belegung
import csv,json,sys,subprocess,io,numpy as np
NX,NY=336,303
alt=subprocess.run(['git','show','18f24ac:./zellen_relief.csv'],capture_output=True,text=True).stdout
def L(R):return lambda k:np.array([r[k] for r in R]).reshape(NY,NX)
a=L(list(csv.DictReader(io.StringIO(alt))));n=L(list(csv.DictReader(open('zellen_relief.csv'))))
wa0=a('wasser_eis')=='1';wa1=n('wasser_eis')=='1';h0=a('hoehe_m').astype(float);h1=n('hoehe_m').astype(float)
ov={k:np.zeros((NY,NX),bool) for k in ('weg','bauplatz','platz','bruecke','furt')}
for r in csv.DictReader(open('../raster_c20_z25_overlay_plaetze_wege.csv')):
    x,y=int(r['cx']),int(r['cy'])
    if r['weg_id']:ov['weg'][y,x]=True
    for k in ('bauplatz','platz','bruecke','furt'):
        if r[k] not in('','0'):ov[k][y,x]=True
bel=np.zeros((NY,NX),bool)
for p in json.load(open('../pruefung/quelle_plaetze_wachstum_ausbau_planm.json'))['E40']:
    q=np.array([[(x+200)*1.2,(y+40)*1.2] for x,y in p['poly']]);x0,y0=q.min(0);x1,y1=q.max(0);bel[max(0,int(y0)):int(np.ceil(y1)),max(0,int(x0)):int(np.ceil(x1))]=1
ov['belegt_haus_platz']=bel
fa,fn,ua,un=a('fluss_id'),n('fluss_id'),a('untergrund'),n('untergrund')
ch=(wa0!=wa1)|(np.abs(h1-h0)>0.05);ys,xs=np.nonzero(ch);rows=[]
for y,x in zip(ys,xs):
    art='wasser_zu_land' if wa0[y,x] and not wa1[y,x] else 'land_zu_wasser' if wa1[y,x] and not wa0[y,x] else 'nur_hoehe'
    rows.append([y*NX+x,x,y,art,int(wa0[y,x]),int(wa1[y,x]),fa[y,x],fn[y,x],ua[y,x],un[y,x],h0[y,x],h1[y,x],round(h1[y,x]-h0[y,x],2)])
w=csv.writer(open('pruefung/zellen_aenderung_t63u.csv','w',newline=''));w.writerow('zell_id,cx,cy,art,wasser_alt,wasser_neu,fluss_alt,fluss_neu,untergrund_alt,untergrund_neu,hoehe_alt,hoehe_neu,delta_m'.split(','));w.writerows(rows)
neuW=wa1&~wa0;altW=wa0&~wa1;west=np.zeros((NY,NX),bool);west[:262,:110]=True
S={'geaendert_zellen':int(ch.sum()),'wasser_zu_land':int(altW.sum()),'land_zu_wasser':int(neuW.sum()),'nur_hoehe':int((ch&(wa0==wa1)).sum()),
 'geaendert_ausserhalb_westgebiet_x<110_y<262':int((ch&~west).sum()),'davon_ueber_0_5m':int((ch&~west&(np.abs(h1-h0)>0.5)).sum()),
 'bbox_x':[int(xs.min()),int(xs.max())],'bbox_y':[int(ys.min()),int(ys.max())],'delta_max_hoch_m':float((h1-h0)[ch].max()),'delta_max_tief_m':float((h1-h0)[ch].min()),
 'kreuzung_neues_wasser':{k:int((neuW&v).sum()) for k,v in ov.items()},'kreuzung_wasser_west_gesamt':{k:int((wa1&v&west).sum()) for k,v in ov.items()},
 'alt_zu_land_untergrund':{k:int(v) for k,v in zip(*np.unique(n('untergrund')[altW],return_counts=True))},
 'neu_wasser_fluss_id':{k:int(v) for k,v in zip(*np.unique(n('fluss_id')[neuW],return_counts=True))}}
json.dump(S,open('pruefung/zellen_aenderung_t63u.json','w'),indent=1);print(json.dumps(S))
