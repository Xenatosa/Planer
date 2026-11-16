# P2: Gate-Vergleich vorher/nachher je Regel und Kachel (liest nur). python3 p2_vergleich.py VORHER_ORDNER [NACHHER_ORDNER=pruefung]
import json,sys,collections
V=sys.argv[1];N=sys.argv[2] if len(sys.argv)>2 else 'pruefung'
for f in ('regeln_letzter_lauf.json','r8_letzter_lauf.json','r9_letzter_lauf.json'):
    a=json.load(open(f'{V}/{f}'));b=json.load(open(f'{N}/{f}'))
    print('==',f,a['summe'],'->',b['summe'])
    ra=a.get('je_regel',{});rb=b.get('je_regel',{})
    for r in sorted(set(ra)|set(rb)):
        ta=[t for t in a.get('treffer',[]) if t['regel']==r];tb=[t for t in b.get('treffer',[]) if t['regel']==r]
        ca=collections.Counter(t.get('feld') for t in ta);cb=collections.Counter(t.get('feld') for t in tb)
        d={k:cb[k]-ca[k] for k in sorted(set(ca)|set(cb),key=str) if cb[k]!=ca[k]}
        flag='SCHLECHTER' if rb.get(r,0)>ra.get(r,0) else ('besser' if rb.get(r,0)<ra.get(r,0) else 'gleich')
        print(f'  {r:44s} {ra.get(r,0):4d} -> {rb.get(r,0):4d} {flag:10s} {d}')
