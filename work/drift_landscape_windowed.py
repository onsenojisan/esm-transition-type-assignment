"""Two instruments the 2026-07-30 result asked for, kept out of drift_landscape.py
so the frozen estimator and its calibration artifacts stay untouched.

1. UNDERSAMPLING (the narrow-but-deep well)
   `transition_type_assignment_result_2026-07-30.md` §3 left one case unexcluded: a
   well that is narrow in separation but deep in barrier. That note also claimed the
   cubic family ties the two together. IT DOES NOT -- it ties them only because the
   project's generator fixes the drift coefficient k = 0.25. With k free,

       drift  mu(x) = -k (x^3 - a^2 x),   a = sep_sd * sigma / 2
       barrier b     = k a^4 / (2 sigma^2)
       relaxation    lambda = 2 k a^2

   so separation (a) and depth (b) are independent. That correction is the point of
   this module's first half, and it opens a failure mode worth more than the hole it
   closes:

   **When lambda * dt >~ 1, the system relaxes within one sampling interval.** Then
   consecutive observations are near-independent draws from the stationary density,
   the estimated drift E[dx | x] collapses to roughly -x for every x, and the field
   has ONE zero -- at the barrier. The estimator reports a single attractor sitting
   exactly where the barrier is.

   Kossakowski's measured AR(1) is about 0.28, i.e. lambda ~ 1.3 per beep: right at
   the edge of that regime. So this is not a hypothetical. If a deep narrow well is
   sampled at that rate, today's 11/11 single-attractor result is what it would look
   like.

   The diagnostic is the MARGINAL: undersampling leaves the stationary density
   bimodal while the drift field says one attractor. (Ambiguous against Cui et al.'s
   polarized-transform case, which produces the same pair -- stated, not hidden.)

2. MOVING WELL vs STATIC WELL
   The other open shape from that result: one basin that relocates, rather than a
   second basin that captures. Windowed drift fields give attractor position,
   restoring rate and noise per window -- the Markovian reconstruction of what
   Bayesian Langevin estimation (Hessler & Kamps, doi:10.1038/s41467-025-60877-0)
   does properly. Their antiCPy package does not build in this environment; that is
   recorded as owed, and this is not a substitute for it.

   Statistic: between-window spread of the attractor position, divided by the
   within-window noise scale. Under a static well the position jitters by sampling
   error only.

Usage:  python work/drift_landscape_windowed.py undersampling
        python work/drift_landscape_windowed.py moving
        python work/drift_landscape_windowed.py kossakowski
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

from drift_landscape import (  # noqa: E402
    DATA, TARGETS, analyse_1d, run_length,
)

OUT = HERE.parent / "outputs"
SIGMA = 0.35          # the project's noise level, unchanged
TODAY = "2026-07-30"


# --------------------------------------------------------------------------
# Generators, batched over reps because the deep wells need many sub-steps
# --------------------------------------------------------------------------
def gen_double_well_batch(rng, reps, T, sep_sd, k, burn=100):
    """Double well with separation and depth decoupled. Returns (reps, T).

    One observation spans unit time, so dt = 1 for the estimator regardless of how
    many sub-steps the integration needs.
    """
    a = sep_sd * SIGMA / 2.0
    lam = 2 * k * a ** 2                      # curvature at the well
    n_sub = int(np.clip(np.ceil(40 * lam), 20, 400))
    dt = 1.0 / n_sub
    s = SIGMA * np.sqrt(dt)
    v = a * rng.choice([-1.0, 1.0], size=reps)
    out = np.empty((reps, T))
    for t in range(-burn, T):
        for _ in range(n_sub):
            v += -k * (v ** 3 - a ** 2 * v) * dt + s * rng.standard_normal(reps)
        if t >= 0:
            out[:, t] = v
    return out, dict(a=a, lam=lam, n_sub=n_sub,
                     barrier_b=k * a ** 4 / (2 * SIGMA ** 2))


def gen_moving_well_batch(rng, reps, T, travel_sd, lam=0.06, burn=200):
    """Single OU well whose centre ramps linearly across the series.

    `travel_sd` is the total travel in units of the well's own stationary SD, so 0
    is the project's `unimodal` generator and 3 means the centre moves three local
    SDs from start to finish.
    """
    stat_sd = SIGMA / np.sqrt(2 * lam)
    travel = travel_sd * stat_sd
    v = rng.standard_normal(reps) * stat_sd
    for _ in range(burn):
        v += -lam * (v + travel / 2) + SIGMA * rng.standard_normal(reps)
    out = np.empty((reps, T))
    for t in range(T):
        c = travel * (t / max(T - 1, 1) - 0.5)
        v += -lam * (v - c) + SIGMA * rng.standard_normal(reps)
        out[:, t] = v
    return out


def gen_moving_ar1_batch(rng, reps, T, travel_sd, phi, stat_sd=1.0, burn=200):
    """Moving well, parameterised by the AR(1) coefficient directly.

    `gen_moving_well_batch` integrates with an Euler step at dt = 1, which is only
    valid while lam << 1. At lam = 1.2 it produces AR(1) = -0.2 -- the step
    overshoots -- so it CANNOT be used to build a null matched to a weakly
    autocorrelated series. This uses the exact Ornstein-Uhlenbeck transition

        x_{t+1} = c_{t+1} + phi (x_t - c_t) + eps,   eps ~ N(0, stat_sd^2 (1-phi^2))

    which is stable for any phi in (-1, 1). `travel_sd` is total travel of the
    centre in units of the stationary SD, as before.
    """
    s = stat_sd * np.sqrt(max(1.0 - phi ** 2, 1e-12))
    travel = travel_sd * stat_sd
    v = rng.standard_normal(reps) * stat_sd - travel / 2
    for _ in range(burn):
        v = -travel / 2 + phi * (v + travel / 2) + s * rng.standard_normal(reps)
    out = np.empty((reps, T))
    c_prev = -travel / 2
    for t in range(T):
        c = travel * (t / max(T - 1, 1) - 0.5)
        v = c + phi * (v - c_prev) + s * rng.standard_normal(reps)
        c_prev = c
        out[:, t] = v
    return out


def ar1(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if x.size < 3:
        return np.nan
    return float(np.corrcoef(x[:-1], x[1:])[0, 1])


def bimodality_coefficient(x):
    """Hosenfeld et al.'s BC. > 0.555 conventionally suggests bimodality."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    n = x.size
    if n < 4:
        return np.nan
    m = x.mean()
    s = x.std(ddof=1)
    if s <= 0:
        return np.nan
    g = float(((x - m) ** 3).mean() / s ** 3)
    kur = float(((x - m) ** 4).mean() / s ** 4 - 3.0)
    return (g ** 2 + 1) / (kur + 3 * (n - 1) ** 2 / ((n - 2) * (n - 3)))


# --------------------------------------------------------------------------
# 1. Undersampling sweep
# --------------------------------------------------------------------------
def undersampling(reps=30, T=1476, sep_sds=(2.0, 3.0), ks=(0.25, 1, 4, 16, 49, 150),
                  bw_mult=1.4):
    rng = np.random.default_rng(20260730)
    rows = []
    for sep in sep_sds:
        for k in ks:
            X, meta = gen_double_well_batch(rng, reps, T, sep, k)
            natt, at_mid, bcs, ars, rls = [], [], [], [], []
            for x in X:
                r = analyse_1d(x, bw_mult=bw_mult)
                if r is None:
                    continue
                natt.append(r["n_attractors"])
                sd = r["sd"]
                # is the single attractor sitting at the barrier (x = 0)?
                if r["n_attractors"] == 1 and sd > 0:
                    at_mid.append(abs(r["attractors"][0]) / sd < 0.25)
                bcs.append(bimodality_coefficient(x))
                ars.append(ar1(x))
                rls.append(run_length(x, 0.0))
            natt = np.array(natt)
            rows.append(dict(
                sep_sd=sep, k=k, lam=meta["lam"], true_b=meta["barrier_b"],
                n_sub=meta["n_sub"],
                ar1_med=float(np.median(ars)),
                true_runlen_med=float(np.median(rls)),
                bc_med=float(np.median(bcs)),
                share_2plus=float((natt >= 2).mean()),
                share_1=float((natt == 1).mean()),
                share_1_at_barrier=(float(np.mean(at_mid)) if at_mid else np.nan)))
            print(f"  sep={sep} k={k:<5g} lam={meta['lam']:6.3f} b={meta['barrier_b']:7.3f} "
                  f"AR1={rows[-1]['ar1_med']:.3f} BC={rows[-1]['bc_med']:.3f} "
                  f"2+={rows[-1]['share_2plus']:.2f} 1@barrier={rows[-1]['share_1_at_barrier']}")
    d = pd.DataFrame(rows)
    d.to_csv(OUT / f"drift_landscape_undersampling_{TODAY}.csv", index=False)
    print("\nread: 'share_2plus' is power. 'share_1_at_barrier' is the UNDERSAMPLING")
    print("signature -- one attractor found, sitting where the barrier actually is.")
    print("'bc_med' > 0.555 with share_2plus ~ 0 is the diagnostic pair: marginal")
    print("bimodal, drift field says one well.")
    return d


# --------------------------------------------------------------------------
# 2. Windowed field: does the well move?
# --------------------------------------------------------------------------
def windowed_field(x, n_windows=6, bw_mult=1.4, min_win=150):
    """Per-window attractor position, restoring rate and noise level."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if x.size < n_windows * min_win:
        return None
    edges = np.linspace(0, x.size, n_windows + 1).astype(int)
    pos, lams, sds, natt = [], [], [], []
    for i in range(n_windows):
        w = x[edges[i]:edges[i + 1]]
        r = analyse_1d(w, bw_mult=bw_mult)
        if r is None or not r["attractors"]:
            pos.append(np.nan)
            lams.append(np.nan)
            sds.append(np.nan)
            natt.append(0 if r is None else r["n_attractors"])
            continue
        med = float(np.median(w))
        j = int(np.argmin([abs(a - med) for a in r["attractors"]]))   # the occupied one
        pos.append(r["attractors"][j])
        wells = r["wells"]
        lams.append(wells[j]["lam"] if j < len(wells) else np.nan)
        sds.append(wells[j]["local_sd"] if j < len(wells) else np.nan)
        natt.append(r["n_attractors"])
    pos, lams, sds = np.array(pos), np.array(lams), np.array(sds)
    ok = np.isfinite(pos)
    if ok.sum() < 3:
        return None
    local = np.nanmedian(sds[np.isfinite(sds)]) if np.isfinite(sds).any() else np.nan
    return dict(positions=pos, lams=lams, local_sds=sds, n_attractors=natt,
                travel_ratio=(float(np.std(pos[ok], ddof=1) / local)
                              if (local and np.isfinite(local) and local > 0) else np.nan),
                span_over_series_sd=float((np.nanmax(pos) - np.nanmin(pos))
                                          / np.std(x, ddof=1)),
                lam_trend=(float(np.corrcoef(np.arange(ok.sum()), lams[ok])[0, 1])
                           if np.isfinite(lams[ok]).all() and ok.sum() > 2 else np.nan))


def moving(reps=40, T=1476, travels=(0.0, 0.0, 1.0, 2.0, 3.0, 5.0), n_windows=6):
    """travels repeats 0.0 twice on purpose: the first is the reference null and the
    second is an independent draw of the same null, so the reported separation is not
    read off a single null sample."""
    rng = np.random.default_rng(20260731)
    rows = []
    for travel in travels:
        X = gen_moving_well_batch(rng, reps, T, travel)
        tr, span, lamtr = [], [], []
        for x in X:
            r = windowed_field(x, n_windows=n_windows)
            if r is None:
                continue
            tr.append(r["travel_ratio"])
            span.append(r["span_over_series_sd"])
            lamtr.append(r["lam_trend"])
        rows.append(dict(travel_sd=travel, n=len(tr),
                         travel_ratio_med=float(np.nanmedian(tr)),
                         travel_ratio_p90=float(np.nanpercentile(tr, 90)),
                         span_over_series_sd_med=float(np.nanmedian(span)),
                         lam_trend_med=float(np.nanmedian(lamtr))))
        print(f"  travel={travel:<4} ratio med={rows[-1]['travel_ratio_med']:.3f} "
              f"p90={rows[-1]['travel_ratio_p90']:.3f} "
              f"span/sd={rows[-1]['span_over_series_sd_med']:.3f}")
    d = pd.DataFrame(rows)
    d.to_csv(OUT / f"drift_landscape_movingwell_{TODAY}.csv", index=False)
    print("\nread: travel_ratio is between-window spread of the attractor position")
    print("divided by the within-window noise scale. The two travel=0 rows bound the")
    print("null; anything above their p90 is the operating threshold.")
    return d


# --------------------------------------------------------------------------
def run_kossakowski(n_windows=6, bw_mult=1.4):
    cfg = TARGETS["kossakowski"]
    df = pd.read_csv(DATA / cfg["path"], sep=cfg["sep"], low_memory=False)
    items = [c for c in cfg["items"] if c in df.columns]
    sub = df[items].apply(pd.to_numeric, errors="coerce")
    z = (sub - sub.mean()) / sub.std(ddof=1)
    units = [(it, sub[it].values) for it in items] + \
            [("_composite", z.mean(axis=1, skipna=True).values)]
    rows = []
    for unit, x in units:
        xx = np.asarray(x, float)
        xx = xx[np.isfinite(xx)]
        r = windowed_field(xx, n_windows=n_windows, bw_mult=bw_mult)
        rec = dict(unit=unit, n=int(xx.size), ar1=ar1(xx),
                   bimodality_coefficient=bimodality_coefficient(xx))
        if r:
            rec.update(travel_ratio=r["travel_ratio"],
                       span_over_series_sd=r["span_over_series_sd"],
                       lam_trend=r["lam_trend"],
                       window_attractor_counts=";".join(str(c) for c in r["n_attractors"]),
                       window_positions=";".join(f"{p:.3f}" for p in r["positions"]))
        rows.append(rec)
    d = pd.DataFrame(rows)
    d.to_csv(OUT / f"drift_landscape_windowed_kossakowski_{TODAY}.csv", index=False)
    with pd.option_context("display.width", 200, "display.max_columns", 30):
        print(d.drop(columns=[c for c in ("window_positions",) if c in d]).to_string(
            index=False, float_format=lambda v: f"{v:.3f}"))
    return d


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "undersampling":
        undersampling()
    elif arg == "moving":
        moving()
    elif arg == "kossakowski":
        run_kossakowski()
    else:
        print(__doc__)
