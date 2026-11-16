# P2: neue Treffer (nachher, >3 Zellen von jedem Vorher-Treffer derselben Regel) in verschlechterten Familien -> Liste + Nahbild (Hillshade+Vertexfarbe, vorher|nachher) [S]
# python3 pruefung/p2_analyse/p2_ausnahmen.py VORHER_ORDNER   (liest pruefung/*_letzter_lauf.json + relief_daten.json.gz)
import json,gzip,base64,sys,os,numpy as np,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
V=sys.argv[1];OUT='pruefung/p2_analyse/ausnahmen';os.makedirs(OUT,exist_ok=True)
FAM=sys.argv[2].split(',') if len(sys.argv)>2 else ['G3_spitze_unten_fein','G6_facette','G7b_wandkontur_feld','R5_loch','T1_fleckrand']
def L(f):
    D=json.load(gzip.open(f));G=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(607,673).astype(float)
    WV=np.frombuffer(base64.b64decode(D['WV']),np.float32).reshape(607,673);VC=np.frombuffer(base64.b64decode(D['VC']),np.uint8).reshape(607,673,3)
    gy,gx=np.gradient(G,0.5);sl=np.arctan(np.hypot(gx,gy));asp=np.arctan2(-gx,gy);a,e=np.radians(315),np.radians(45)
    s=np.clip(np.sin(e)*np.cos(sl)+np.cos(e)*np.sin(sl)*np.cos(a-asp),0,1);img=VC/255*(0.35+0.65*s[...,None]);w=WV>-900;img[w]=img[w]*0.5+np.array([.2,.4,.9])*.5
    return np.clip(img,0,1)
IA=L(f'{V}/relief_daten.json.gz');IB=L('relief_daten.json.gz')
a=json.load(open(f'{V}/regeln_letzter_lauf.json'))['treffer'];b=json.load(open('pruefung/regeln_letzter_lauf.json'))['treffer']
liste=[]
for r in FAM:
    A=[(t['x'],t['z']) for t in a if t['regel']==r]
    for t in b:
        if t['regel']!=r or not t.get('feld') or t['feld']=='-':continue
        if A and min(np.hypot(t['x']-x,t['z']-z) for x,z in A)<=3:continue
        n=len(liste)+1;nm=f"{n:03d}_{r}_{t['feld']}_{t['x']}_{t['z']}.jpg".replace('|','_');rr=21 if r=='G7b_wandkontur_feld' else 10
        x0,x1,z0,z1=max(0,int(t['x'])-rr),min(336,int(t['x'])+rr),max(0,int(t['z'])-rr),min(303,int(t['z'])+rr)
        fig,ax=plt.subplots(1,2,figsize=(8,4.2),dpi=80)
        for k,(I,ti) in enumerate(((IA,'vorher dc8c174'),(IB,'nachher P2'))):
            ax[k].imshow(I[z0*2:z1*2+1,x0*2:x1*2+1],extent=(x0,x1,z1,z0));ax[k].plot(t['x'],t['z'],'o',mfc='none',mec='red',ms=16,mew=2);ax[k].set_title(ti,fontsize=8);ax[k].tick_params(labelsize=6)
        fig.suptitle(f"{r} {t['feld']} {t['x']}|{t['z']} Wert {t['wert']}",fontsize=9);plt.tight_layout();plt.savefig(f'{OUT}/{nm}',pil_kwargs={'quality':80});plt.close()
        liste.append(dict(nr=n,regel=r,feld=t['feld'],x=t['x'],z=t['z'],wert=t['wert'],nahbild=f'ausnahmen/{nm}'))
json.dump(liste,open(f'{OUT}/ausnahmen_kandidaten.json','w'),indent=1,ensure_ascii=False)
import collections;print(len(liste),collections.Counter(l['regel'] for l in liste))
