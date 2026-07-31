"""Gilmore flag 8, anomalous variance -- first consequence: does the common factor move?

Governed by outputs/anomalous_variance_spec_v1.md, which was committed and pushed
BEFORE this file was written or run. That ordering is independently timestamped in the
remote, which is what the two specifications deposited earlier today lack.

Per spec section 1 this does NOT test the flag -- anomalous variance is anticipatory
and no transition has been identified, so the flag has no referent. It tests the
necessary condition: is the common-factor structure of the ten items stationary?

Per spec section 2 the claim is about CHANGE, never level. A high PC1 share is the
positive manifold, is expected, and carries no claim.

Usage:  python work/anomalous_variance.py calibrate
        python work/anomalous_variance.py run
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

from drift_landscape import DATA, TARGETS  # noqa: E402

OUT = HERE.parent / "outputs"
TODAY = "2026-07-30"
N_ITEMS, T, PHI = 10, 1476, 0.30
WINDOWS = (6, 12)


def pc1_share(X):
    """Largest eigenvalue of the correlation matrix, over the number of items."""
    X = np.asarray(X, float)
    keep = np.isfinite(X).all(axis=1)
    X = X[keep]
    if X.shape[0] < 30:
        return np.nan, np.nan
    sd = X.std(axis=0, ddof=1)
    if (sd <= 0).any():
        return np.nan, np.nan
    C = np.corrcoef(X, rowvar=False)
    if not np.isfinite(C).all():
        return np.nan, np.nan
    ev = np.linalg.eigvalsh(C)
    off = C[~np.eye(C.shape[0], dtype=bool)]
    return float(ev.max() / C.shape[0]), float(np.mean(np.abs(off)))


def windowed(X, n_windows):
    X = np.asarray(X, float)
    e = np.linspace(0, X.shape[0], n_windows + 1).astype(int)
    p, m = [], []
    for i in range(n_windows):
        a, b = pc1_share(X[e[i]:e[i + 1]])
        p.append(a)
        m.append(b)
    p, m = np.array(p, float), np.array(m, float)
    ok = np.isfinite(p)
    return dict(pc1=p, mean_abs_r=m,
                range_pc1=float(np.nanmax(p) - np.nanmin(p)) if ok.sum() >= 2 else np.nan,
                mean_pc1=float(np.nanmean(p)),
                range_r=float(np.nanmax(m) - np.nanmin(m)) if ok.sum() >= 2 else np.nan)


def gen_factor(rng, ramp, phi=PHI, n=N_ITEMS, T=T, levels=None):
    """Ten items on one latent AR(1) factor whose loading ramps down by `ramp`."""
    s = np.sqrt(1 - phi ** 2)
    f = np.empty(T)
    v = rng.standard_normal()
    for t in range(T):
        v = phi * v + s * rng.standard_normal()
        f[t] = v
    lam0 = 0.75
    lam = lam0 - ramp * np.arange(T) / max(T - 1, 1)
    lam = np.clip(lam, 0.0, 0.99)
    e = rng.standard_normal((T, n))
    X = lam[:, None] * f[:, None] + np.sqrt(1 - lam[:, None] ** 2) * e
    if levels:
        for j in range(n):
            z = X[:, j]
            edges = np.linspace(-3, 3, levels[j % len(levels)])
            step = edges[1] - edges[0]
            X[:, j] = edges[0] + np.clip(np.round((z - edges[0]) / step), 0,
                                         len(edges) - 1) * step
    return X


def calibrate(reps=60, ramps=(0.0, 0.0, 0.15, 0.30, 0.45, 0.60)):
    rng = np.random.default_rng(20260810)
    # the items' own effective resolutions, from compression_vs_quiet: four coarse, six finer
    coarse = [2, 2, 3, 3, 4, 4, 4, 5, 5, 5]
    rows = []
    for arm, levels in (("discretised (PRIMARY)", coarse), ("continuous", None)):
        print(f"\n--- {arm} ---")
        print(f"{'ramp':>6}{'nwin':>6}{'mean pc1':>10}{'range med':>11}{'range p95':>11}")
        for nw in WINDOWS:
            for ramp in ramps:
                rr, mp = [], []
                for _ in range(reps):
                    w = windowed(gen_factor(rng, ramp, levels=levels), nw)
                    if np.isfinite(w["range_pc1"]):
                        rr.append(w["range_pc1"])
                        mp.append(w["mean_pc1"])
                if not rr:
                    continue
                rows.append(dict(arm=arm, ramp=ramp, n_windows=nw, n=len(rr),
                                 mean_pc1=float(np.mean(mp)),
                                 range_med=float(np.median(rr)),
                                 range_p95=float(np.percentile(rr, 95))))
                r_ = rows[-1]
                print(f"{ramp:>6}{nw:>6}{r_['mean_pc1']:>10.3f}"
                      f"{r_['range_med']:>11.4f}{r_['range_p95']:>11.4f}")
    d = pd.DataFrame(rows)
    d.to_csv(OUT / f"anomalous_variance_calibration_{TODAY}.csv", index=False)
    print("\nread: the two ramp=0 rows bound the null. Power at each ramp is the share of")
    print("replicates whose range exceeds the null p95 -- printed by `run`. If the ramp")
    print("rows do not separate from the null rows, spec section 5 outcome AV3 applies.")
    return d


def run():
    cal = pd.read_csv(OUT / f"anomalous_variance_calibration_{TODAY}.csv")
    cfg = TARGETS["kossakowski"]
    df = pd.read_csv(DATA / cfg["path"], sep=cfg["sep"], low_memory=False)
    items = [c for c in cfg["items"] if c in df.columns]
    X = df[items].apply(pd.to_numeric, errors="coerce").values
    X = X[np.isfinite(X).all(axis=1)]
    print(f"items: {len(items)}   complete rows: {X.shape[0]}\n")
    rows = []
    for nw in WINDOWS:
        w = windowed(X, nw)
        null = cal[(cal.arm == "discretised (PRIMARY)") & (cal.ramp == 0.0) &
                   (cal.n_windows == nw)].range_p95.max()
        rows.append(dict(n_windows=nw, mean_pc1=w["mean_pc1"], range_pc1=w["range_pc1"],
                         null_p95=null, exceeds=bool(w["range_pc1"] > null),
                         range_mean_abs_r=w["range_r"],
                         pc1_by_window=";".join(f"{v:.3f}" for v in w["pc1"])))
        print(f"{nw} windows | mean pc1 {w['mean_pc1']:.3f} | range {w['range_pc1']:.4f} "
              f"| null p95 {null:.4f} | exceeds: {w['range_pc1'] > null}")
        print(f"   pc1 per window: {rows[-1]['pc1_by_window']}")
    d = pd.DataFrame(rows)
    d.to_csv(OUT / f"anomalous_variance_result_{TODAY}.csv", index=False)
    return d


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "calibrate":
        calibrate()
    elif arg == "run":
        run()
    else:
        print(__doc__)
