"""The missing null: can a STATIC skewed / discretised well fake a moving attractor?

WHY THIS IS THE DECISIVE TEST
-----------------------------
`moving_well_deflation_result_2026-07-30.md` established that on Kossakowski the
fitted attractor travels ~5x further between windows than the window mean does
(`mood_lonely` 1.490 vs 0.270, `mood_guilty` 1.319 vs 0.247), while on every
synthetic generator the two coincide (corr 0.97-0.997). So the finding is not mean
non-stationarity -- but the regime where they diverge has no null.

For a 1-D SDE with constant noise the stationary density is p(x) ~ exp(2 int mu/sigma^2),
so the ZERO OF THE DRIFT IS THE MODE and the window mean estimates the MEAN. Those
coincide only for a symmetric well. Skew them apart and the two statistics stop
measuring the same thing -- and the root of a nearly flat drift is sensitive, its
position error going as 1/|slope|.

Two mechanisms, both matching the real items rather than invented:

  * SKEW / PEAKEDNESS. `mood_lonely` and `mood_guilty` have bimodality coefficients
    of 0.098 and 0.125 -- extremely peaked. Built here as a nonlinear transform of an
    AR(1), the same family as Cui et al.'s "polarized" condition already in
    `drift_landscape.gen_polarized`.
  * DISCRETENESS. The items are 6-7 level Likert. Rounding can destabilise a drift
    root while leaving a mean untouched.

If a STATIC landscape (travel = 0) under realistic skew and discretisation
reproduces ratio_attractor ~ 5x ratio_mean at ratio_attractor ~ 1.3-1.5, the
Kossakowski finding is explained and must be retracted.

Usage:  python work/skewed_well_null.py
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

from drift_landscape_windowed import (                    # noqa: E402
    ar1, bimodality_coefficient, gen_moving_ar1_batch,
)
from moving_well_deflation import both_statistics         # noqa: E402

OUT = HERE.parent / "outputs"
TODAY = "2026-07-30"


def discretise(x, levels):
    """Round onto `levels` equally spaced values spanning the observed range,
    the way a Likert item quantises whatever it is measuring."""
    lo, hi = np.min(x), np.max(x)
    if hi <= lo:
        return x
    step = (hi - lo) / (levels - 1)
    return lo + np.round((x - lo) / step) * step


def gen_skewed(rng, reps, T, travel_sd, phi, beta, levels=None):
    """AR(1) pushed through g(y) = y + beta*y^2, optionally quantised.

    beta = 0 recovers the symmetric generator already calibrated. Larger beta skews
    the stationary density, so its mode and its mean separate.
    """
    y = gen_moving_ar1_batch(rng, reps, T, travel_sd, phi)
    x = y + beta * y ** 2
    if levels:
        x = np.vstack([discretise(row, levels) for row in x])
    return x


def gen_heavy_tailed(rng, reps, T, travel_sd, phi, nu, levels=None, burn=200):
    """AR(1) with Student-t innovations: a quiet baseline with rare large excursions.

    The skew transform above raises the bimodality coefficient (toward 0.6); the real
    items sit at BC 0.098-0.125, which needs the opposite -- heavy tails, i.e. excess
    kurtosis around 7 for BC ~ 0.1. Student-t innovations produce that directly and
    keep the process symmetric, so this isolates PEAKEDNESS from SKEW.

    Scaled so the stationary SD is 1: Var(t_nu) = nu/(nu-2), and an AR(1)'s
    stationary variance is Var(eps)/(1-phi^2).
    """
    scale = np.sqrt((1 - phi ** 2) * (nu - 2) / nu)
    travel = float(travel_sd)
    v = rng.standard_t(nu, size=reps) * scale - travel / 2
    for _ in range(burn):
        v = -travel / 2 + phi * (v + travel / 2) + scale * rng.standard_t(nu, size=reps)
    out = np.empty((reps, T))
    c_prev = -travel / 2
    for t in range(T):
        c = travel * (t / max(T - 1, 1) - 0.5)
        v = c + phi * (v - c_prev) + scale * rng.standard_t(nu, size=reps)
        c_prev = c
        out[:, t] = v
    if levels:
        out = np.vstack([discretise(row, levels) for row in out])
    return out


def main():
    rng = np.random.default_rng(20260805)
    reps, T, phi = 30, 1476, 0.30
    rows = []
    print("STATIC (travel=0) unless marked. Target to reproduce: attractor ~1.3-1.5")
    print("with mean ~0.25, i.e. a ratio of about 5.\n")
    print(f"{'beta':>5} {'levels':>7} {'travel':>7} {'AR1':>6} {'BC':>6} "
          f"{'attractor':>10} {'mean':>7} {'A/M':>6} {'A>0.225':>8}")
    for beta in (0.0, 0.3, 0.6, 1.0):
        for levels in (None, 7):
            for travel in (0.0, 3.0):
                X = gen_skewed(rng, reps, T, travel, phi, beta, levels)
                a, m, ars, bcs = [], [], [], []
                for x in X:
                    ars.append(ar1(x))
                    bcs.append(bimodality_coefficient(x))
                    r = both_statistics(x)
                    if r:
                        a.append(r["ratio_attractor"])
                        m.append(r["ratio_mean"])
                if not a:
                    continue
                am, mm = float(np.median(a)), float(np.median(m))
                rows.append(dict(beta=beta, levels=(levels or 0), travel_sd=travel,
                                 n=len(a), ar1_med=float(np.median(ars)),
                                 bc_med=float(np.median(bcs)),
                                 attractor_med=am, attractor_p95=float(np.percentile(a, 95)),
                                 mean_med=mm, ratio_A_over_M=(am / mm if mm else np.nan),
                                 share_above_old_gate=float(np.mean(np.array(a) > 0.225))))
                r_ = rows[-1]
                print(f"{beta:>5} {str(levels or '-'):>7} {travel:>7} "
                      f"{r_['ar1_med']:>6.3f} {r_['bc_med']:>6.3f} "
                      f"{am:>10.3f} {mm:>7.3f} {r_['ratio_A_over_M']:>6.2f} "
                      f"{r_['share_above_old_gate']:>8.2f}")
    print("\n\nHEAVY-TAILED: the skew sweep above RAISES the bimodality coefficient")
    print("(0.33-0.62) and cannot reach the items' 0.098-0.125. Student-t innovations")
    print("go the other way and isolate peakedness from skew.\n")
    print(f"{'nu':>5} {'levels':>7} {'travel':>7} {'AR1':>6} {'BC':>6} "
          f"{'attractor':>10} {'mean':>7} {'A/M':>6} {'A>0.225':>8}")
    for nu in (3, 4, 6, 12):
        for levels in (None, 7):
            for travel in (0.0, 3.0):
                X = gen_heavy_tailed(rng, reps, T, travel, phi, nu, levels)
                a, m, ars, bcs = [], [], [], []
                for x in X:
                    ars.append(ar1(x))
                    bcs.append(bimodality_coefficient(x))
                    r = both_statistics(x)
                    if r:
                        a.append(r["ratio_attractor"])
                        m.append(r["ratio_mean"])
                if not a:
                    continue
                am, mm = float(np.median(a)), float(np.median(m))
                rows.append(dict(beta=np.nan, nu=nu, levels=(levels or 0),
                                 travel_sd=travel, n=len(a),
                                 ar1_med=float(np.median(ars)),
                                 bc_med=float(np.median(bcs)),
                                 attractor_med=am, attractor_p95=float(np.percentile(a, 95)),
                                 mean_med=mm, ratio_A_over_M=(am / mm if mm else np.nan),
                                 share_above_old_gate=float(np.mean(np.array(a) > 0.225))))
                r_ = rows[-1]
                print(f"{nu:>5} {str(levels or '-'):>7} {travel:>7} "
                      f"{r_['ar1_med']:>6.3f} {r_['bc_med']:>6.3f} "
                      f"{am:>10.3f} {mm:>7.3f} {r_['ratio_A_over_M']:>6.2f} "
                      f"{r_['share_above_old_gate']:>8.2f}")

    d = pd.DataFrame(rows)
    d.to_csv(OUT / f"skewed_well_null_{TODAY}.csv", index=False)
    print(f"\nwrote skewed_well_null_{TODAY}.csv")
    print("Kossakowski for comparison: mood_lonely A=1.490 M=0.270 (A/M 5.5),")
    print("mood_guilty A=1.319 M=0.247 (5.3); their BC are 0.098 and 0.125, AR1 0.32/0.26.")


if __name__ == "__main__":
    main()
