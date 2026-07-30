"""The last calibration: can asymmetry alone move the mode while the mean stays put?

THE QUESTION
------------
`skewed_well_null_result_2026-07-30.md` restated the finding: in 3 of 11 Kossakowski
units the zero of the estimated restoring force relocates between windows while the
distribution's centre of mass does not (attractor/mean ratio 5.3-5.5, against ~1.0
for every generator that translates a well and 0.34-1.97 for every static one).

Since the drift root is the MODE and the window mean is the MEAN, the only remaining
shape that separates them is a change in ASYMMETRY at a fixed mean. This builds it.

DESIGN
------
Base process, already matched to the items in the previous calibration: AR(1) with
Student-t innovations, phi = 0.30, nu = 3 -> AR(1) ~ 0.30, BC ~ 0.13, against
mood_lonely (0.324 / 0.098) and mood_guilty (0.259 / 0.125).

Skew transform, monotone and asymptotically linear so the t-tails stay finite:

    g(y; beta) = y + beta * y^2 / (1 + |y|)

|beta| < 1 keeps dg/dy > 0. The added term is even, so it skews; it grows like
beta*|y| rather than exponentially, so a t(3) tail does not explode.

The mean is then held fixed BY CONSTRUCTION: x_t = g(y_t; beta_t) - m(beta_t), where
m(beta) is the mean of the transform under the process's own stationary distribution,
estimated once by Monte Carlo. So beta moves the mode and leaves the mean at zero.

TWO CONDITIONS, and the whole test is which one is needed:
  * STATIC  beta_t = beta constant           -> the null
  * RAMPED  beta_t sweeps -beta .. +beta     -> time-varying asymmetry

If STATIC reproduces attractor ~1.4 with attractor/mean ~5, the Kossakowski finding
is an artifact of skew and must be retracted. If only RAMPED reproduces it, the
finding is that the series' asymmetry changes over time.

Usage:  python work/varying_skew_null.py
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

from drift_landscape_windowed import ar1, bimodality_coefficient   # noqa: E402
from moving_well_deflation import both_statistics                  # noqa: E402
from skewed_well_null import discretise                            # noqa: E402

OUT = HERE.parent / "outputs"
TODAY = "2026-07-30"
PHI, NU, T = 0.30, 3, 1476


def skew_transform(y, beta):
    """Monotone for |beta| < 1; the added term is even, so it skews, and it grows
    like beta*|y| so heavy tails stay finite."""
    return y + beta * y ** 2 / (1.0 + np.abs(y))


def base_ar1_t(rng, reps, T, phi=PHI, nu=NU, burn=200):
    """AR(1) with Student-t innovations, stationary SD 1."""
    scale = np.sqrt((1 - phi ** 2) * (nu - 2) / nu)
    v = rng.standard_t(nu, size=reps) * scale
    for _ in range(burn):
        v = phi * v + scale * rng.standard_t(nu, size=reps)
    out = np.empty((reps, T))
    for t in range(T):
        v = phi * v + scale * rng.standard_t(nu, size=reps)
        out[:, t] = v
    return out


def transform_means(rng, betas, n=400_000):
    """m(beta) = E[g(Y; beta)] under the process's own stationary distribution."""
    y = base_ar1_t(rng, 1, n)[0]
    return {float(b): float(np.mean(skew_transform(y, b))) for b in betas}


def build(rng, reps, beta_amp, ramped, mtab, levels=None):
    y = base_ar1_t(rng, reps, T)
    if ramped:
        betas = beta_amp * (2 * np.arange(T) / max(T - 1, 1) - 1.0)     # -amp .. +amp
    else:
        betas = np.full(T, beta_amp)
    x = np.empty_like(y)
    for t in range(T):
        b = float(betas[t])
        x[:, t] = skew_transform(y[:, t], b) - mtab[round(b, 4)]
    if levels:
        x = np.vstack([discretise(r, levels) for r in x])
    return x


def main():
    rng = np.random.default_rng(20260806)
    reps = 30
    amps = (0.0, 0.3, 0.6, 0.9)
    # every beta value that will be requested, so m(beta) is exact for each
    wanted = set()
    for a in amps:
        wanted.add(round(a, 4))
        wanted.update(round(float(b), 4)
                      for b in a * (2 * np.arange(T) / (T - 1) - 1.0))
    print(f"tabulating m(beta) for {len(wanted)} beta values ...")
    mtab = transform_means(rng, sorted(wanted))

    rows = []
    print("\nmean is held fixed by construction in BOTH conditions.\n")
    print(f"{'beta_amp':>9} {'mode':>7} {'levels':>7} {'AR1':>6} {'BC':>6} "
          f"{'attractor':>10} {'mean':>7} {'A/M':>6} {'A>0.225':>8}")
    for amp in amps:
        for ramped in (False, True):
            for levels in (None, 7):
                X = build(rng, reps, amp, ramped, mtab, levels)
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
                rows.append(dict(beta_amp=amp, ramped=ramped, levels=(levels or 0),
                                 n=len(a), ar1_med=float(np.median(ars)),
                                 bc_med=float(np.median(bcs)), attractor_med=am,
                                 attractor_p95=float(np.percentile(a, 95)),
                                 mean_med=mm,
                                 ratio_A_over_M=(am / mm if mm else np.nan),
                                 share_above_gate=float(np.mean(np.array(a) > 0.225))))
                r_ = rows[-1]
                print(f"{amp:>9} {'RAMPED' if ramped else 'static':>7} "
                      f"{str(levels or '-'):>7} {r_['ar1_med']:>6.3f} "
                      f"{r_['bc_med']:>6.3f} {am:>10.3f} {mm:>7.3f} "
                      f"{r_['ratio_A_over_M']:>6.2f} {r_['share_above_gate']:>8.2f}")

    d = pd.DataFrame(rows)
    d.to_csv(OUT / f"varying_skew_null_{TODAY}.csv", index=False)
    print(f"\nwrote varying_skew_null_{TODAY}.csv")
    print("target: mood_lonely A=1.490 M=0.270 (A/M 5.5), mood_guilty A=1.319 "
          "M=0.247 (5.3),\n        BC 0.098 / 0.125, AR1 0.324 / 0.259")


if __name__ == "__main__":
    main()
