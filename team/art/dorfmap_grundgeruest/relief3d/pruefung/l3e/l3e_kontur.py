# L3e Hilfe: Viewer-Spiegel WR/WE (viewer_alle.js P12b nachgerechnet) und Uferkontur-Plot (python3 l3e_kontur.py out.png x0 x1 z0 z1 dateien...)
# Sichtbare Uferlinie wie viewer_alle.js (P12b): Spiegel WR (geglaettet), Ring1 WE; Kontur GL-Spiegel=0
import sys, gzip, json, base64, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def lade(p):
    D = json.loads(gzip.decompress(open(p,'rb').read()))
    return D
def arr(D, key, dt):
    v = D[key]
    if isinstance(v, dict): v = v.get('b64') or v.get('data')
    return np.frombuffer(base64.b64decode(v), dtype=dt)
def wr_von(WV, GX, GY):
    ok = WV > -900
    A = WV.copy()
    for it in range(3):
        B = A.copy()
        P = np.pad(A, 1, constant_values=-999); O = np.pad(ok, 1)
        for j in range(1, GY-1):
            pass
        # vectorised median of neighbours >A+0.3 if count>=5
        nbs = [P[1+dj:1+dj+GY, 1+di:1+di+GX] for dj in (-1,0,1) for di in (-1,0,1) if (di or dj)]
        nok = [O[1+dj:1+dj+GY, 1+di:1+di+GX] for dj in (-1,0,1) for di in (-1,0,1) if (di or dj)]
        S = np.stack(nbs); M = np.stack(nok) & (S > A + 0.3)
        cnt = M.sum(0); sel = ok & (cnt >= 5)
        if sel.any():
            Sm = np.where(M, S, np.nan)
            srt = np.sort(Sm, axis=0)  # nan last
            idx = cnt >> 1
            med = np.take_along_axis(srt, idx[None], 0)[0]
            B[sel] = med[sel]
        B[:, [0, -1]] = A[:, [0, -1]]; B[[0, -1], :] = A[[0, -1], :]
        A = B
    for it in range(16):
        P = np.pad(np.where(ok, A, 0), 1); O = np.pad(ok, 1).astype(float)
        s = sum(P[1+dj:1+dj+GY, 1+di:1+di+GX] for dj in (-1,0,1) for di in (-1,0,1))
        c = sum(O[1+dj:1+dj+GY, 1+di:1+di+GX] for dj in (-1,0,1) for di in (-1,0,1))
        B = np.minimum(WV+0.3, np.maximum(WV-0.6, s/np.maximum(c,1)))
        inner = np.zeros_like(ok); inner[1:-1,1:-1] = True
        A = np.where(ok & inner, B, A)
    return A
def feld(p):
    D = lade(p); rs = D['rs']; GX = D['nx']*rs+1; GY = D['ny']*rs+1
    GB = np.frombuffer(base64.b64decode(D['GB']), '<f4').reshape(GY, GX).astype(float)
    WV = np.frombuffer(base64.b64decode(D['WV']), '<f4').reshape(GY, GX).astype(float)
    ok = WV > -900
    WR = wr_von(WV, GX, GY)
    P = np.pad(np.where(ok, WR, 0), 1); O = np.pad(ok, 1).astype(float)
    s = sum(P[1+dj:1+dj+GY, 1+di:1+di+GX] for dj in (-1,0,1) for di in (-1,0,1) if di or dj)
    c = sum(O[1+dj:1+dj+GY, 1+di:1+di+GX] for dj in (-1,0,1) for di in (-1,0,1) if di or dj)
    ring1 = ~ok & (c > 0)
    WE = np.where(ok, WR, np.where(ring1, s/np.maximum(c,1), np.nan))
    ring3 = ring1 & (WE - GB > 0.3)
    return dict(rs=rs, GB=GB, WV=WV, ok=ok, WR=WR, WE=WE, ring1=ring1, ring3=ring3)
if __name__ == '__main__':
    out, x0, x1, z0, z1 = sys.argv[1], *map(float, sys.argv[2:6]); dateien = sys.argv[6:]
    fig, axs = plt.subplots(1, len(dateien), figsize=(9*len(dateien), 9*(z1-z0)/(x1-x0)+1))
    for ax, p in zip(np.atleast_1d(axs), dateien):
        F = feld(p); rs = F['rs']
        sl = (slice(int(z0*rs), int(z1*rs)+1), slice(int(x0*rs), int(x1*rs)+1))
        X, Z = np.meshgrid(np.arange(sl[1].start, sl[1].stop)/rs, np.arange(sl[0].start, sl[0].stop)/rs)
        D = (F['GB'] - F['WE'])[sl]
        D = np.where(F['ring3'][sl], np.nan, D)
        ax.pcolormesh(X, Z, F['GB'][sl]-np.nanmedian(F['WV'][sl][F['ok'][sl]]), cmap='terrain', vmin=-1, vmax=1, shading='nearest')
        ax.contour(X, Z, D, [0], colors='r', linewidths=1.5)
        ok = F['ok'][sl]; ax.plot(X[ok], Z[ok], 'b.', ms=2)
        r3 = F['ring3'][sl]; ax.plot(X[r3], Z[r3], 'mx', ms=4)
        for xs in range(42, 337, 42):
            if x0 <= xs <= x1: ax.axvline(xs, color='y')
        ax.set_aspect('equal'); ax.invert_yaxis(); ax.set_title(p.split('/')[-1])
    plt.tight_layout(); plt.savefig(out, dpi=70)
