"""Gilmore's INACCESSIBILITY flag, tested on the held series.

WHY THIS IS NOT BIMODALITY
--------------------------
van der Maas & Molenaar (1992), reading Gilmore (1981): in the cusp, entering the
bifurcation set produces two minima and a local maximum, and "the local maximum gives
rise to an INACCESSIBLE MODE". The flag is a region the system does not occupy, not
merely a dip between two humps.

That makes it strictly stronger than bimodality. Two humps with a shallow valley are
bimodal and fully accessible; two humps with an EMPTY region between them are
inaccessible. The project has measured bimodality exhaustively (structure_gate,
Silverman, Haslbeck) and has never asked the support question.

OPERATIONALISATION, chosen for Likert data
------------------------------------------
For a discrete item the question is exact rather than statistical: are there two or
more disjoint groups of occupied response levels, separated by at least one level that
is effectively unoccupied?

  occupied(v)  :  count(v) / n >= floor_frac
  groups       :  maximal runs of contiguous occupied levels
  FLAG PRESENT :  >= 2 groups (hence >= 1 unoccupied interior level between them)

`floor_frac` is a support threshold, not a tuned parameter: it says what counts as
"the system does not go there". Reported across a sweep so nothing rests on one value.

WHAT THE CALIBRATION IS FOR
---------------------------
A negative is only informative if a system that genuinely HAS the flag would show it
here. So the same generators used all day are discretised to the item's number of
levels and passed through the same test. If a 6 SD double well does not produce a gap
at 7 levels, then this test cannot see the flag in this data type and a negative on
the real series means nothing.

Usage:  python work/inaccessibility_flag.py selftest
        python work/inaccessibility_flag.py kossakowski
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

from drift_landscape import DATA, TARGETS, gen_bistable, gen_deep_well, gen_monostable, gen_polarized  # noqa: E402
from skewed_well_null import discretise  # noqa: E402

OUT = HERE.parent / "outputs"
TODAY = "2026-07-30"
FLOORS = (0.000, 0.002, 0.005, 0.010)


def occupied_groups(x, floor_frac):
    """Maximal runs of contiguous occupied levels, on the observed level grid."""
    vals, counts = np.unique(np.asarray(x, float), return_counts=True)
    n = counts.sum()
    occ = counts / n > floor_frac
    if not occ.any():
        return [], vals, counts
    # levels are the distinct observed values; a "gap" is an unoccupied level BETWEEN
    # occupied ones on that grid. For a Likert item the grid is the integer levels, so
    # a level with zero observations never appears in `vals` -- fill the integer grid.
    if np.allclose(vals, np.round(vals)):
        lo, hi = int(round(vals.min())), int(round(vals.max()))
        grid = np.arange(lo, hi + 1, dtype=float)
        cnt = np.zeros(grid.size)
        for v, c in zip(vals, counts):
            cnt[int(round(v)) - lo] = c
        vals, counts = grid, cnt
        occ = counts / n > floor_frac
    groups, cur = [], []
    for i, o in enumerate(occ):
        if o:
            cur.append(i)
        elif cur:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups, vals, counts


def inaccessibility(x, floor_frac=0.005):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    groups, vals, counts = occupied_groups(x, floor_frac)
    n_groups = len(groups)
    gap_levels = 0
    gap_span = np.nan
    if n_groups >= 2:
        gap_levels = sum(groups[i + 1][0] - groups[i][-1] - 1 for i in range(n_groups - 1))
        sd = np.std(x, ddof=1)
        widest = max((groups[i + 1][0] - groups[i][-1] - 1) for i in range(n_groups - 1))
        step = np.median(np.diff(vals)) if vals.size > 1 else np.nan
        gap_span = float(widest * step / sd) if sd > 0 else np.nan
    return dict(n=int(x.size), n_levels=int(vals.size), n_groups=n_groups,
                flag=bool(n_groups >= 2), gap_levels=int(gap_levels),
                gap_span_sd=gap_span, modal_share=float(counts.max() / counts.sum()))


def selftest(reps=40, T=1476, levels=7):
    rng = np.random.default_rng(20260807)
    cases = [("bistable 2SD", lambda: gen_bistable(rng, T, 2.0)),
             ("bistable 3SD", lambda: gen_bistable(rng, T, 3.0)),
             ("bistable 4SD", lambda: gen_bistable(rng, T, 4.0)),
             ("bistable 6SD", lambda: gen_bistable(rng, T, 6.0)),
             ("deep well 6SD", lambda: gen_deep_well(rng, T, 6.0)),
             ("monostable", lambda: gen_monostable(rng, T)),
             ("polarized", lambda: gen_polarized(rng, T))]
    rows = []
    print(f"discretised to {levels} levels, T={T}, {reps} reps\n")
    print(f"{'case':<16}" + "".join(f"{'floor '+str(f):>13}" for f in FLOORS))
    for name, gen in cases:
        shares = {}
        for f in FLOORS:
            hits = [inaccessibility(discretise(gen(), levels), f)["flag"] for _ in range(reps)]
            shares[f] = float(np.mean(hits))
            rows.append(dict(case=name, floor_frac=f, share_flag=shares[f]))
        print(f"{name:<16}" + "".join(f"{shares[f]:>13.2f}" for f in FLOORS))
    d = pd.DataFrame(rows)
    d.to_csv(OUT / f"inaccessibility_selftest_{TODAY}.csv", index=False)
    print("\nread: on bistable rows this is POWER -- can a genuine two-state system with a")
    print("real barrier even produce an unoccupied interior level once discretised to a")
    print("Likert grid? On monostable/polarized rows it is the false-alarm rate.")
    return d


def kossakowski():
    cfg = TARGETS["kossakowski"]
    df = pd.read_csv(DATA / cfg["path"], sep=cfg["sep"], low_memory=False)
    items = [c for c in cfg["items"] if c in df.columns]
    rows = []
    for it in items:
        x = pd.to_numeric(df[it], errors="coerce").dropna().values
        for f in FLOORS:
            r = inaccessibility(x, f)
            rows.append(dict(unit=it, floor_frac=f, **r))
    d = pd.DataFrame(rows)
    d.to_csv(OUT / f"inaccessibility_kossakowski_{TODAY}.csv", index=False)
    piv = d.pivot_table(index="unit", columns="floor_frac", values="n_groups")
    print("occupied groups per item (>=2 would be the flag):\n")
    print(piv.to_string(float_format=lambda v: f"{v:.0f}"))
    print(f"\nflag present anywhere: {bool(d.flag.any())}")
    print(f"levels used per item: {d.groupby('unit').n_levels.first().to_dict()}")
    return d


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "selftest":
        selftest()
    elif arg == "kossakowski":
        kossakowski()
    else:
        print(__doc__)
