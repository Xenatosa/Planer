# t48u Abschluss: Wandspruenge je Wand (max-min Boden in 21x21 um steile Wandzellen, Median) und Fluss-Durchgaengigkeit. Aufruf: python3 pruefung/pruefe_final_t48u.py
import csv,json,numpy as np
from scipy import ndimage as nd
R=list(csv.DictReader(open('zellen_relief.csv')));NX=max(int(r['cx']) for r in R)+1;NY=max(int(r['cy']) for r in R)+1
A=lambda k,f=str:np.array([f(r[k]) for r in R]).reshape(NY,NX)
H=A('boden_hoehe_m',float);wn=A('wand_name');kl=A('klippe');fl=A('fluss_id');we=A('wasser_eis');ws=A('wasserspiegel_m')
d=nd.maximum_filter(H,21)-nd.minimum_filter(H,21);out={'sprung_median_m':{}}
for w in ('Nord','Suedgrat','Krater','Ostgrat'):
    m=(wn==w)&(kl!='')&(kl!='0')&(kl!='False');out['sprung_median_m'][w]=round(float(np.median(d[m])),2) if m.any() else None
wa=np.isin(we,['1','True','WASSER_EIS'])|((fl!='')&(fl!='0'))
# t54u: zusaetzlich Sprung Fuss->Krone ohne Flussbett/Seegrund (Wassertiefe zaehlt nicht als Wand) [A]
Hw=np.where(wa,np.nan,H);dw=nd.maximum_filter(np.nan_to_num(Hw,nan=-1e9),21)-(-nd.maximum_filter(np.nan_to_num(-Hw,nan=-1e9),21));out['sprung_median_ohne_wasser_m']={}
for w in ('Nord','Suedgrat','Krater','Ostgrat'):
    m=(wn==w)&(kl!='')&(kl!='0')&(kl!='False');out['sprung_median_ohne_wasser_m'][w]=round(float(np.median(dw[m])),2) if m.any() else None
lab,n=nd.label(wa);sz=np.bincount(lab.ravel())[1:];out['wasser_komponenten_ge30']=int((sz>=30).sum());out['groesste_komponente_zellen']=int(sz.max())
print(json.dumps(out,ensure_ascii=False))
# je fluss_id: Anzahl zusammenhaengender Teile (8er-Nachbarschaft); 1 = durchgaengig
fj={}
for f in sorted(set(fl.ravel())-{'','0'}):
    l,k=nd.label(fl==f,structure=np.ones((3,3)));s=np.bincount(l.ravel())[1:];fj[f]={'teile':int(k),'teile_ge5':int((s>=5).sum()),'zellen':int(s.sum())}
print(json.dumps({'fluss_id_teile':fj},ensure_ascii=False))
l,k=nd.label(wa,structure=np.ones((3,3)));s=np.sort(np.bincount(l.ravel())[1:])[::-1]
print(json.dumps({'wasser_alle_ids_8er':{'teile':int(k),'groesste':[int(x) for x in s[:6]]}}))
