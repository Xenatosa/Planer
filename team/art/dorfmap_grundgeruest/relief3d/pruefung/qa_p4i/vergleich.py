"""Vorher (P4b-Paar, dc8c174) ueber Nachher (P4c-Paar, 8cd6d37), gleiche Kamera.
Aufruf: python3 vergleich.py VORHER_DIR NACHHER_DIR ZIEL_DIR name1 name2 ..."""
import sys,os
from PIL import Image
v,n,z=sys.argv[1:4];os.makedirs(z,exist_ok=True)
for name in sys.argv[4:]:
    a=Image.open(f'{v}/{name}.jpg');b=Image.open(f'{n}/{name}.jpg')
    c=Image.new('RGB',(a.width,a.height+b.height+4),'black');c.paste(a,(0,0));c.paste(b,(0,a.height+4));c.save(f'{z}/{name}.jpg',quality=75)
