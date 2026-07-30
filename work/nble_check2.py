"""Second attempt: NBLE with the time-scale separation prior enabled.

The default configuration treats the hidden process Y as fast correlated noise and
does not separate a moving well from a static one (nble_check.py: OU 1.129 vs 1.134
at travel 0 vs 3). The documented route for a SLOW hidden process is
`activate_time_scale_separation_prior=True, slow_process='Y'`, which the docs warn
also needs hand-set MAP starting guesses.

ndim = 6: four X-drift polynomial coefficients (lowest order first), one constant
X-coupling, one Y Ornstein-Uhlenbeck parameter theta_5. A slow Y means a LARGE
theta_5 (its drift is -1/theta_5^2).
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
START = np.array([0.0, -1.0, 0.0, 0.0, 1.0, 10.0])   # theta_0..theta_5


def scan(x, tss_factor):
    from antiCPy.early_warnings.drift_slope import NonMarkovEstimation
    est = NonMarkovEstimation(
        x, np.arange(x.size, dtype=float),
        activate_time_scale_separation_prior=True,
        slow_process="Y",
        time_scale_separation_factor=tss_factor,
        max_likelihood_starting_guesses=START)
    est.fast_MAP_resilience_scan(window_size=WIN, window_shift=SHIFT,
                                 num_processes="half", print_progress=False,
                                 save=False)
    return dict(slope=np.asarray(est.slope_storage)[0],
                ou=np.asarray(est.OU_param_storage)[0],
                noise=np.asarray(est.noise_level_storage)[0])


def main():
    from drift_landscape_windowed import gen_moving_ar1_batch
    rng = np.random.default_rng(20260803)
    reps, tss = 6, 10
    print(f"time_scale_separation_prior=True slow_process='Y' factor={tss}")
    print(f"window={WIN} shift={SHIFT} reps={reps} T=1476 phi=0.30\n")
    print(f"{'travel':>7} {'OU med':>9} {'OU sd':>8} {'slope med':>10} {'slope sd':>9}")
    for travel in (0.0, 3.0):
        X = gen_moving_ar1_batch(rng, reps, 1476, travel, phi=0.30)
        ou_m, ou_s, sl_m, sl_s = [], [], [], []
        t0 = _t.time()
        for x in X:
            try:
                r = scan(x, tss)
            except Exception as e:                       # noqa: BLE001
                print(f"  FAILED: {type(e).__name__}: {e}")
                return
            ou_m.append(np.median(r["ou"]));   ou_s.append(np.std(r["ou"]))
            sl_m.append(np.median(r["slope"])); sl_s.append(np.std(r["slope"]))
        print(f"{travel:>7} {np.median(ou_m):>9.3f} {np.median(ou_s):>8.3f} "
              f"{np.median(sl_m):>10.3f} {np.median(sl_s):>9.3f}   ({_t.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
