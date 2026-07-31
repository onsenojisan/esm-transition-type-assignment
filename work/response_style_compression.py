"""Punch-list item 1: can a compressive response style ERASE a second attractor?

THE GAP THIS CLOSES
-------------------
The deposited note says response degeneracy cannot manufacture a second attractor --
it destabilises the position of the one found. True, and established. But the same
note names structured response style as "the largest unaddressed threat" and says it
would RESHAPE the drift field, flattening it where a respondent avoids answering.

A flattened field can erase a shallow second attractor. That is a FALSE-NEGATIVE
mechanism acting directly on the 66/66 single-attractor result, and it was never
tested. Nothing in the note bridges its biggest stated threat and its main claim.

WHAT IS SIMULATED
-----------------
Central-tendency bias: the respondent avoids the ends of the scale and pulls answers
toward the middle. Latent value z (in SD units), compression factor c in (0, 1]:

    z_reported = c * z          then binned onto a FIXED 7-level scale spanning +-3 SD

The fixed grid is the point. Compressing and then re-binning on the OBSERVED range
would rescale the compression away; a real Likert scale has fixed anchors, so mass
genuinely migrates toward the centre levels and two wells can merge into one.

c = 1.0 is no compression and reproduces the discretised baseline.

Usage:  python work/response_style_compression.py
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
    analyse_1d, gen_bistable, gen_deep_well, gen_monostable, gen_polarized,
)
from inaccessibility_flag import inaccessibility  # noqa: E402

OUT = HERE.parent / "outputs"
TODAY = "2026-07-30"
LEVELS, HALF_RANGE = 7, 3.0          # a 7-point scale with anchors at +-3 SD


def compress_and_bin(x, c, levels=LEVELS, half=HALF_RANGE):
    """Central-tendency compression onto a fixed-anchor Likert grid."""
    x = np.asarray(x, float)
    z = (x - np.mean(x)) / np.std(x, ddof=1)
    z = c * z
    edges = np.linspace(-half, half, levels)
    step = edges[1] - edges[0]
    binned = np.clip(np.round((z - edges[0]) / step), 0, levels - 1)
    return edges[0] + binned * step


def main(reps=40, T=1476, cs=(1.0, 0.8, 0.6, 0.5, 0.4, 0.3), bw=1.4):
    rng = np.random.default_rng(20260808)
    cases = [("bistable 4SD", lambda: gen_bistable(rng, T, 4.0)),
             ("bistable 6SD", lambda: gen_bistable(rng, T, 6.0)),
             ("deep well 6SD", lambda: gen_deep_well(rng, T, 6.0)),
             ("monostable", lambda: gen_monostable(rng, T)),
             ("polarized", lambda: gen_polarized(rng, T))]
    rows = []
    print(f"fixed {LEVELS}-level scale, anchors +-{HALF_RANGE} SD, T={T}, {reps} reps, bw={bw}")
    print("c = compression toward the scale midpoint (1.0 = none)\n")
    print(f"{'case':<16}" + "".join(f"{'c='+str(c):>10}" for c in cs))
    for name, gen in cases:
        att, ina = {}, {}
        for c in cs:
            a, i = [], []
            for _ in range(reps):
                x = compress_and_bin(gen(), c)
                r = analyse_1d(x, bw_mult=bw)
                a.append(bool(r and r["n_attractors"] >= 2))
                i.append(inaccessibility(x, 0.010)["flag"])
            att[c], ina[c] = float(np.mean(a)), float(np.mean(i))
            rows.append(dict(case=name, compression=c,
                             share_2plus=att[c], share_inaccessible=ina[c]))
        print(f"{name:<16}" + "".join(f"{att[c]:>10.2f}" for c in cs))
    d = pd.DataFrame(rows)
    d.to_csv(OUT / f"response_style_compression_{TODAY}.csv", index=False)

    print(f"\n{'':16}--- inaccessibility flag, same runs ---")
    print(f"{'case':<16}" + "".join(f"{'c='+str(c):>10}" for c in cs))
    for name, _ in cases:
        s = d[d.case == name].set_index("compression").share_inaccessible
        print(f"{name:<16}" + "".join(f"{s[c]:>10.2f}" for c in cs))

    print("\nread: on the three bistable rows this is POWER under compression. A column")
    print("where power collapses is the compression at which a real second attractor")
    print("becomes invisible. monostable/polarized rows remain the false-alarm rate.")
    return d


if __name__ == "__main__":
    main()
