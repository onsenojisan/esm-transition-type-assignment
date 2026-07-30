"""Deflation check: is the moving-well finding anything more than "the mean moved"?

WHY
---
antiCPy defines its per-window `fixed_point_estimate` as `np.mean(self.data_window)`
-- the window mean, not a root of the fitted drift polynomial. So the route proposed
at the end of the NBLE re-run (extract NBLE's per-window fixed point) does not exist.

But it points at the test that matters. For a single-attractor system the fitted
attractor sits close to the local mean by construction, so `travel_ratio` computed
from fitted attractors may carry no more information than the same statistic
computed from window means. If so, the 2026-07-30 moving-well result restates
non-stationarity of the mean -- which Olthof et al. (2020) already reported for this
very series, and which would make it not a new finding at all.

WHAT IS COMPARED
----------------
Per window: the fitted attractor position (zero of the estimated drift with negative
slope, `drift_landscape.analyse_1d`) versus the plain window mean. Same windows, same
normaliser, so the two `travel_ratio` values are directly comparable.

Calibrated first on the synthetic static/moving generators, then applied to
Kossakowski. If the mean-based statistic matches the attractor-based one on both,
the drift field adds nothing here and the finding must be restated.

Usage:  python work/moving_well_deflation.py
"""
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

from drift_landscape import DATA, TARGETS, analyse_1d          # noqa: E402
from drift_landscape_windowed import gen_moving_ar1_batch      # noqa: E402

OUT = HERE.parent / "outputs"
TODAY = "2026-07-30"
NWIN = 6


def both_statistics(x, n_windows=NWIN, bw_mult=1.4):
    """travel_ratio from fitted attractors and from window means, same normaliser."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    edges = np.linspace(0, x.size, n_windows + 1).astype(int)
    pos, means, local = [], [], []
    for i in range(n_windows):
        w = x[edges[i]:edges[i + 1]]
        means.append(float(np.mean(w)))
        r = analyse_1d(w, bw_mult=bw_mult)
        if r is None or not r["attractors"]:
            pos.append(np.nan)
            continue
        med = float(np.median(w))
        j = int(np.argmin([abs(a - med) for a in r["attractors"]]))
        pos.append(r["attractors"][j])
        if j < len(r["wells"]) and np.isfinite(r["wells"][j]["local_sd"]):
            local.append(r["wells"][j]["local_sd"])
    pos, means = np.array(pos), np.array(means)
    ok = np.isfinite(pos)
    if ok.sum() < 3 or not local:
        return None
    nrm = float(np.median(local))
    if not np.isfinite(nrm) or nrm <= 0:
        return None
    return dict(
        ratio_attractor=float(np.std(pos[ok], ddof=1) / nrm),
        ratio_mean=float(np.std(means, ddof=1) / nrm),
        corr_pos_mean=(float(np.corrcoef(pos[ok], means[ok])[0, 1])
                       if ok.sum() > 2 else np.nan))


def calibrate(reps=40, T=1476, phi=0.30, travels=(0.0, 1.0, 3.0)):
    rng = np.random.default_rng(20260804)
    rows = []
    print("SYNTHETIC — does the drift field beat the plain mean?\n")
    print(f"{'travel':>7} {'attractor med':>14} {'attractor p95':>14} "
          f"{'mean med':>10} {'mean p95':>10} {'corr':>7}")
    for travel in travels:
        X = gen_moving_ar1_batch(rng, reps, T, travel, phi=phi)
        a, m, c = [], [], []
        for x in X:
            r = both_statistics(x)
            if r:
                a.append(r["ratio_attractor"])
                m.append(r["ratio_mean"])
                c.append(r["corr_pos_mean"])
        rows.append(dict(travel_sd=travel, n=len(a),
                         attractor_med=float(np.median(a)),
                         attractor_p95=float(np.percentile(a, 95)),
                         mean_med=float(np.median(m)),
                         mean_p95=float(np.percentile(m, 95)),
                         corr_med=float(np.nanmedian(c))))
        r_ = rows[-1]
        print(f"{travel:>7} {r_['attractor_med']:>14.3f} {r_['attractor_p95']:>14.3f} "
              f"{r_['mean_med']:>10.3f} {r_['mean_p95']:>10.3f} {r_['corr_med']:>7.3f}")
    d = pd.DataFrame(rows)
    d.to_csv(OUT / f"moving_well_deflation_synthetic_{TODAY}.csv", index=False)
    return d


def kossakowski():
    cfg = TARGETS["kossakowski"]
    df = pd.read_csv(DATA / cfg["path"], sep=cfg["sep"], low_memory=False)
    items = [c for c in cfg["items"] if c in df.columns]
    sub = df[items].apply(pd.to_numeric, errors="coerce")
    z = (sub - sub.mean()) / sub.std(ddof=1)
    units = [(it, sub[it].values) for it in items] + \
            [("_composite", z.mean(axis=1, skipna=True).values)]
    rows = []
    for unit, x in units:
        r = both_statistics(np.asarray(x, float))
        if r:
            rows.append(dict(unit=unit, **r,
                             ratio_diff=r["ratio_attractor"] - r["ratio_mean"]))
    d = pd.DataFrame(rows).sort_values("ratio_attractor", ascending=False)
    d.to_csv(OUT / f"moving_well_deflation_kossakowski_{TODAY}.csv", index=False)
    print("\n\nKOSSAKOWSKI\n")
    print(d.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    return d


if __name__ == "__main__":
    calibrate()
    kossakowski()
