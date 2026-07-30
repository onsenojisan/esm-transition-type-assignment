"""Does NBLE's hidden-OU parameter separate a moving well from a static one?

Quick two-condition check before committing to a full calibration. If theta_5
(OU_param) does not separate travel=0 from travel=3, the instrument does not answer
the question and a different readout is needed.
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

WIN, SHIFT = 250, 50


def scan(x):
    from antiCPy.early_warnings.drift_slope import NonMarkovEstimation
    est = NonMarkovEstimation(x, np.arange(x.size, dtype=float))
    est.fast_MAP_resilience_scan(window_size=WIN, window_shift=SHIFT,
                                 num_processes="half", print_progress=False,
                                 save=False)
    return dict(slope=np.asarray(est.slope_storage)[0],
                noise=np.asarray(est.noise_level_storage)[0],
                ou=np.asarray(est.OU_param_storage)[0],
                coup=np.asarray(est.X_coupling_storage)[0])


def main():
    from drift_landscape_windowed import gen_moving_ar1_batch
    rng = np.random.default_rng(20260802)
    reps = 6
    print(f"window={WIN} shift={SHIFT}  reps={reps}  T=1476  phi=0.30\n")
    print(f"{'travel':>7} {'OU med':>9} {'OU sd':>8} {'slope med':>10} "
          f"{'slope sd':>9} {'noise med':>10}")
    for travel in (0.0, 3.0):
        X = gen_moving_ar1_batch(rng, reps, 1476, travel, phi=0.30)
        ou_m, ou_s, sl_m, sl_s, nz_m = [], [], [], [], []
        t0 = _t.time()
        for x in X:
            r = scan(x)
            ou_m.append(np.median(r["ou"]));  ou_s.append(np.std(r["ou"]))
            sl_m.append(np.median(r["slope"])); sl_s.append(np.std(r["slope"]))
            nz_m.append(np.median(r["noise"]))
        print(f"{travel:>7} {np.median(ou_m):>9.3f} {np.median(ou_s):>8.3f} "
              f"{np.median(sl_m):>10.3f} {np.median(sl_s):>9.3f} "
              f"{np.median(nz_m):>10.3f}   ({_t.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
