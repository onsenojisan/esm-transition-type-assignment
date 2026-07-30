"""
calibrate_structure_gate.py -- where does the pre-gate become usable?

The selftest showed the gate does not reach usable power on the default
generator. This asks the more useful question: as a function of well SEPARATION
and series LENGTH, where does it work? The answer is a specification the project
can carry into a data request -- "this analysis needs N observations per person
and a separation of at least S" -- instead of a bare failure.

Sweep is over:
  sep : distance between the two potential minima, in units of the noise SD
  T   : observations per person

Reported per cell: PASS rate on BISTABLE (power) and on UNIMODAL (false alarm).

Usage:  python calibrate_structure_gate.py [reps]
"""

from __future__ import annotations

import sys
import numpy as np

from structure_gate import gmm_bic, silverman_test, potential_wells

SIGMA = 0.35


def bistable(rng, T, sep):
    a = sep * SIGMA / 2.0
    x = np.empty(T)
    x[0] = -a
    for t in range(1, T):
        x[t] = x[t - 1] - (x[t - 1] ** 3 - a ** 2 * x[t - 1]) * 0.25 + SIGMA * rng.standard_normal()
    return x


def unimodal(rng, T):
    x = np.empty(T)
    x[0] = 0.0
    for t in range(1, T):
        x[t] = x[t - 1] - 0.06 * x[t - 1] + SIGMA * rng.standard_normal()
    return x


def score(x, seed, n_boot):
    g = gmm_bic(x, seed=seed)["positive"]
    s = silverman_test(x, n_boot=n_boot, rng=seed)["positive"]
    w = potential_wells(x)["positive"]
    return sum([g, s, w]), g, s, w


def main(reps=12, n_boot=80):
    rng = np.random.default_rng(20260726)
    seps = [2.0, 3.0, 4.0, 6.0]
    Ts = [600, 1500, 4000]
    print(f"structure-gate calibration -- {reps} reps/cell, PASS = >=2 of 3 scored\n")
    print(f"{'sep(SD)':>8} {'T':>6} | {'power':>6} {'false':>6} | {'GMM':>5} {'Silv':>5} {'well':>5}")
    print("-" * 56)
    for sep in seps:
        for T in Ts:
            pw = fa = 0
            gh = sh = wh = 0
            for r in range(reps):
                sc, g, s, w = score(bistable(rng, T, sep), r, n_boot)
                gh += g; sh += s; wh += w
                pw += (sc >= 2)
                sc0, *_ = score(unimodal(rng, T), r, n_boot)
                fa += (sc0 >= 2)
            print(f"{sep:8.1f} {T:6d} | {pw/reps:6.0%} {fa/reps:6.0%} | "
                  f"{gh/reps:5.0%} {sh/reps:5.0%} {wh/reps:5.0%}")
    print("\npower  = PASS rate on truly bistable data (want high)")
    print("false  = PASS rate on truly unimodal data (want <= ~10%)")
    print("\nReference: the densest real dataset in Helmich et al. Table 1 is")
    print("122 days x 5/day = 610 observations per person.")
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 12))
