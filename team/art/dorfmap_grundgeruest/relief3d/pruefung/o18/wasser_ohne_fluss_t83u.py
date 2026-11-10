# t83u: Wasser-Anzeige-Komponenten ohne benannten Fluss (nur WASSER_FARBE = aus c20-Farbe)
import csv,collections,json,os
H=os.path.dirname(__file__)
r=list(csv.DictReader(open(os.path.join(H,'../../zellen_relief.csv'))))
W={(int(z['cx']),int(z['cy'])):(z['fluss_id'],z['untergrund']) for z in r if z['wasser_anzeige'] not in ('0','')}
seen=set();comps=[]
for p in W:
  if p in seen: continue
  st=[p];seen.add(p);c=[]
  while st:
    q=st.pop();c.append(q)
    for d in((1,0),(-1,0),(0,1),(0,-1)):
      n=(q[0]+d[0],q[1]+d[1])
      if n in W and n not in seen: seen.add(n);st.append(n)
  ids=collections.Counter(W[q][0] for q in c);ug=collections.Counter(W[q][1] for q in c)
  xs=[q[0] for q in c];ys=[q[1] for q in c]
  comps.append(dict(n=len(c),fluss=dict(ids),untergrund=dict(ug),bbox=[min(xs),min(ys),max(xs),max(ys)],feld=f"{'ABCDEFGH'[min(7,min(xs)//42)]}{min(7,min(ys)//43+1)}"))
comps.sort(key=lambda c:-c['n'])
iso=[c for c in comps if set(c['fluss'])<={'WASSER_FARBE',''}]
out=dict(wasserzellen=len(W),komponenten=len(comps),ohne_fluss=len(iso),zellen_ohne_fluss=sum(c['n'] for c in iso),liste=iso)
json.dump(out,open(os.path.join(H,'wasser_ohne_fluss_t83u.json'),'w'),indent=1)
print({k:v for k,v in out.items() if k!='liste'})
for c in iso[:30]: print(c)
