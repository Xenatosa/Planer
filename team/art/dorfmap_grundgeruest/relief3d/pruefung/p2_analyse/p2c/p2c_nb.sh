cd /workspace/wt_wege_p2b_v2/team/art/dorfmap_grundgeruest/relief3d
NA=${NA:-/tmp/p2c_ak_test}
O=pruefung/p2_analyse/p2c/nahbilder; mkdir -p $O /tmp/p2c_nb2
while read n xz d el; do for st in vorher nachher; do H=/tmp/p2b2_p10_nachher; [ $st = nachher ] && H=$NA; for m in farbe clay; do o=""; [ $m = clay ] && o=--clay
NODE_PATH=/tmp/w3/node_modules node pruefung/alle_kacheln/nahbild.js --html $H/alle_kacheln.html --xz $xz --abstand $d --azimut 0 --neigung $el $o --out /tmp/p2c_nb2/${n}_${st}_$m.png >/dev/null 2>&1 || echo fail $n $st $m
done; done
python3 - "$n" <<'P'
import sys;from PIL import Image,ImageDraw
n=sys.argv[1];W,H=480,360;c=Image.new('RGB',(W*2,H*2+20),'white');d=ImageDraw.Draw(c)
for i,st in enumerate(('vorher','nachher')):
  for j,m in enumerate(('farbe','clay')):
    c.paste(Image.open(f'/tmp/p2c_nb2/{n}_{st}_{m}.png').convert('RGB').resize((W,H)),(j*W,20+i*H))
d.text((5,3),f'P2c {n}: oben vorher (P2b 2633f1d), unten nachher (P2c); links Farbe, rechts Ton',fill='black')
c.save(f'pruefung/p2_analyse/p2c/nahbilder/{n}_paar.jpg',quality=85)
P
done < /tmp/p2c_pkt.txt
echo NB_FERTIG
