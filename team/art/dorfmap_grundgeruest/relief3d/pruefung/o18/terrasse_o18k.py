# O18k (t105u b): Terrassenringe / Matsch je Feld. terr = Anteil Hangpunkte mit Steigungs-Einbruch (Stufenprofil: lokale Steigung <35 % der 5-m-Mittelsteigung), rau = Std des Hochpass (G-gauss2m) am Hang, d.h. Detail; python3 ... a.json.gz [b.json.gz ...]
import json,gzip,sys,base64,numpy as np,scipy.ndimage as nd
for f in sys.argv[1:]:
    D=json.load(gzip.open(f));NX,NY,RS=D['nx'],D['ny'],D['rs'];GX,GY=NX*RS+1,NY*RS+1
    G=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(GY,GX).astype(float)
    gy,gx=np.gradient(G,1/RS);s=np.hypot(gx,gy);sm=nd.uniform_filter(s,10)
    hang=(sm>0.35)&(sm<1.2);terr=hang&(s<0.35*sm);hp=G-nd.gaussian_filter(G,2*RS)
    r=[]
    for zi in range(2):
        for c in range(8):
            m=np.zeros_like(hang);m[zi*43*RS:(zi+1)*43*RS,c*42*RS:(c+1)*42*RS]=True;hm=hang&m
            if hm.sum()<200:continue
            r.append(f"{'ABCDEFGH'[c]}{zi+1}:terr={terr[hm].mean()*100:.1f}%,rau={hp[hm].std():.3f}")
    print(f.split('/')[-1],' '.join(r))
