# index.html + neu/index.html: nur die eingebettete Datenzeile NEU_GZ durch neu/relief_neu.json.gz ersetzen (Bundle/Viewer-Code bytegleich).
# Gleiches Ergebnis wie RELIEF_NEU=1 python3 baue_html.py mit unveraenderter /tmp/w3-Toolchain (am 16.11. vor dem Box-Neustart geprueft).
import base64
d=base64.b64encode(open('neu/relief_neu.json.gz','rb').read()).decode()
for p in ('index.html','neu/index.html'):
    h=open(p,encoding='utf-8').read();i=h.index('window.NEU_GZ="')+len('window.NEU_GZ="');j=h.index('"',i)
    open(p,'w',encoding='utf-8').write(h[:i]+d+h[j:]);print(p,len(h[:i]+d+h[j:]))
