"""Smoke test: does antiCPy's NonMarkovEstimation run here, and what does it return?

Windows multiprocessing needs the __main__ guard, so this is a file, not -c.
"""
import sys
import time as _t
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass


def main():
    from antiCPy.early_warnings.drift_slope import NonMarkovEstimation
    from drift_landscape_windowed import gen_moving_ar1_batch

    rng = np.random.default_rng(7)
    x = gen_moving_ar1_batch(rng, 1, 1476, travel_sd=3.0, phi=0.30)[0]
    t = np.arange(x.size, dtype=float)

    est = NonMarkovEstimation(x, t)
    print("constructed:", type(est).__name__)
    print("  ndim:", getattr(est, "ndim", "?"), " nwalkers:", getattr(est, "nwalkers", "?"))

    t0 = _t.time()
    # summary_window_size (default 10) must not exceed the number of windows:
    # (n - window_size)/window_shift + 1. shift=50 gives 25 windows here.
    est.fast_MAP_resilience_scan(window_size=250, window_shift=50,
                                 num_processes=1, print_progress=False,
                                 save=False)
    print(f"scan done in {_t.time()-t0:.1f}s")

    for a in sorted(vars(est)):
        v = getattr(est, a)
        if not isinstance(v, np.ndarray) or v.size < 2:
            continue
        print(f"  {a:26} shape={str(v.shape):12} "
              f"{np.array2string(v.ravel()[:5], precision=3)}")


if __name__ == "__main__":
    main()
