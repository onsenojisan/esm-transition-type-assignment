"""NBLE on Kossakowski: the stability trajectory, under a non-Markovian noise model.

WHAT THIS DOES AND DOES NOT ANSWER
----------------------------------
Two checks (`nble_check.py`, `nble_check2.py`) established that NBLE's reported
outputs -- drift slope zeta, noise level psi, hidden-OU parameter theta_5 -- do NOT
separate a moving well from a static one, in either the default configuration or
with the time-scale separation prior enabled. Medians at travel 0 vs 3 SD:

    default           OU 1.129 / 1.134    slope -0.894 / -0.914
    time-scale prior  OU 2.704 / 2.741    slope -1.374 / -1.337

The reason is structural: the moving-well signal lives in the BETWEEN-window
displacement of the operating point, and NBLE fits a stationary model WITHIN each
window. The per-window fixed point is what carries it, and the fast MAP scan does
not store it. So `drift_landscape_windowed.py` is not superseded for that question.

What NBLE does measure, and what nothing in this project has measured before, is
the local restoring rate estimated jointly with a correlated-noise model -- the
B-tipping versus N-tipping axis of `transition_type_assignment_spec_v1.md` Q2.

READ WITH THE SPEC'S CONSTRAINT. Q2 was declared out of scope there because it has
no referent unless Q1 finds a discrete transition, and Q1 found none. A zeta trend
here is therefore a stability trajectory, NOT an approach to a bifurcation: there is
no second state to approach.

Windows overlap heavily (size 250, shift 50), so ~25 windows carry roughly 6
independent spans. No p-values are computed and none should be.

Usage:  python work/nble_kossakowski.py
"""
import sys
import time as _t
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

OUT = HERE.parent / "outputs"
WIN, SHIFT = 250, 50
TODAY = "2026-07-30"


def main():
    from antiCPy.early_warnings.drift_slope import NonMarkovEstimation
    from drift_landscape import DATA, TARGETS
    from drift_landscape_windowed import ar1

    cfg = TARGETS["kossakowski"]
    df = pd.read_csv(DATA / cfg["path"], sep=cfg["sep"], low_memory=False)
    items = [c for c in cfg["items"] if c in df.columns]
    sub = df[items].apply(pd.to_numeric, errors="coerce")
    z = (sub - sub.mean()) / sub.std(ddof=1)
    units = [(it, sub[it].values) for it in items] + \
            [("_composite", z.mean(axis=1, skipna=True).values)]

    rows, traj = [], {}
    for unit, x in units:
        x = np.asarray(x, float)
        x = x[np.isfinite(x)]
        # z-score so zeta and psi are comparable across items with different scales
        x = (x - x.mean()) / x.std(ddof=1)
        t0 = _t.time()
        est = NonMarkovEstimation(x, np.arange(x.size, dtype=float))
        est.fast_MAP_resilience_scan(window_size=WIN, window_shift=SHIFT,
                                     num_processes="half", print_progress=False,
                                     save=False)
        zeta = np.asarray(est.slope_storage)[0]
        psi = np.asarray(est.noise_level_storage)[0]
        ou = np.asarray(est.OU_param_storage)[0]
        coup = np.asarray(est.X_coupling_storage)[0]
        traj[unit] = zeta
        idx = np.arange(zeta.size)
        rows.append(dict(
            unit=unit, n=int(x.size), ar1=ar1(x), n_windows=int(zeta.size),
            zeta_med=float(np.median(zeta)), zeta_sd=float(np.std(zeta)),
            zeta_first=float(zeta[0]), zeta_last=float(zeta[-1]),
            zeta_trend_r=float(np.corrcoef(idx, zeta)[0, 1]),
            psi_med=float(np.median(psi)),
            ou_med=float(np.median(ou)), coupling_med=float(np.median(coup))))
        print(f"  {unit:<14} zeta={rows[-1]['zeta_med']:+.3f} "
              f"(sd {rows[-1]['zeta_sd']:.3f}, {zeta[0]:+.3f} -> {zeta[-1]:+.3f}) "
              f"trend r={rows[-1]['zeta_trend_r']:+.2f}  OU={rows[-1]['ou_med']:.2f} "
              f"({_t.time()-t0:.0f}s)")

    d = pd.DataFrame(rows)
    d.to_csv(OUT / f"nble_kossakowski_{TODAY}.csv", index=False)
    pd.DataFrame(traj).to_csv(OUT / f"nble_kossakowski_zeta_traj_{TODAY}.csv", index=False)
    with pd.option_context("display.width", 200, "display.max_columns", 30):
        print("\n" + d.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    print(f"\nwrote nble_kossakowski_{TODAY}.csv and its zeta trajectories")
    print("zeta < 0 is a restoring rate; closer to 0 = less stable. Windows overlap,")
    print("so trend_r is descriptive only -- ~25 windows carry ~6 independent spans.")


if __name__ == "__main__":
    main()
