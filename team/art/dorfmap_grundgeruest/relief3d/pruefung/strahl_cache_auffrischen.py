"""O11 M1/M4: Raycast-Cache pruefung/strahl_hoehe_t65u.json aus einem test_strahl_t62u.js-Lauf auffrischen.
Aufruf: python3 pruefung/strahl_cache_auffrischen.py RAYCAST.json  (Punktreihenfolge = relief_daten.json.gz)
Danach gen_relief.py + baue_html.py erneut, Raycast nachmessen. [A]"""
import json,gzip,sys
D=json.load(gzip.open('relief_daten.json.gz'));S=json.load(open(sys.argv[1]));P='pruefung/strahl_hoehe_t65u.json'
H=json.load(open(P));n={}
for nm in S:
    h=H.setdefault(nm,{});c=0
    for o,s in zip(D[nm],S[nm]):
        if s[0] is None:continue
        k=f"{o[0]:.3f}|{o[2]:.3f}"
        if h.get(k)!=s[0]:h[k]=s[0];c+=1
    n[nm]=c
json.dump(H,open(P,'w'),sort_keys=True);print('aufgefrischt',n)
