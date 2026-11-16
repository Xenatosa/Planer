# Dunkle Linienpixel: Luminanz < Median(5x5) - 30 bei hellem Umfeld (Median > 120). Wasser/Himmel egal, gleiche Metrik vorher/nachher.
import sys, json, numpy as np
from PIL import Image
from scipy.ndimage import median_filter
def zaehl(f, maske=None):
    a = np.asarray(Image.open(f).convert('RGB')).astype(np.float32)
    L = 0.299*a[...,0] + 0.587*a[...,1] + 0.114*a[...,2]
    m = median_filter(L, size=5)
    d = (L < m - 30) & (m > 120)
    r = {'dunkel': int(d.sum())}
    mag = (a[...,0] > 200) & (a[...,1] < 60) & (a[...,2] > 200); grn = (a[...,1] > 200) & (a[...,0] < 60) & (a[...,2] < 60); cy = (a[...,1] > 200) & (a[...,2] > 200) & (a[...,0] < 60)
    r.update(magenta=int(mag.sum()), gruen=int(grn.sum()), cyan=int(cy.sum()))
    return r, d
if __name__ == '__main__':
    out = {}
    for f in sys.argv[1:]: out[f] = zaehl(f)[0]
    print(json.dumps(out, indent=0))
