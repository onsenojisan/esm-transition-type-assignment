"""Is the concentration in these items COMPRESSION or a QUIET SYMPTOM?

WHY IT MATTERS
--------------
`response_style_compression_result_2026-07-30.md` shows a 20% central-tendency
compression takes a 6 SD bistable system from 100% detection to 5%. That makes the
deposited null conditional on this participant not having compressed. The three
concentrated items (67-84% on one level) are consistent with either mechanism, and
that result explicitly did not separate them.

THE DISCRIMINATOR
-----------------
The two mechanisms put the mass in different places.

  CENTRAL-TENDENCY COMPRESSION : respondent avoids the ends.
      -> mode at the scale MIDPOINT, both extremes unused, near-symmetric.

  QUIET SYMPTOM (genuine floor) : the symptom is usually absent.
      -> mode at a scale ENDPOINT, one-sided tail, strongly skewed.

So `modal_position` -- where the modal level sits between the scale's own anchors --
separates them, with end-use and skew as corroboration.

Scale anchors are taken as the item's observed min and max, which is a floor on the
true scale: if a respondent never used an anchor, the true scale is WIDER and the
modal position moves toward the middle. That direction of error favours the
quiet-symptom reading, so it is the conservative choice here.

MODEL COMPARISON
----------------
Descriptives alone under-determine. Both mechanisms are also simulated, each tuned to
reproduce the observed modal share, and asked which reproduces the observed end-use
and skew.

Usage:  python work/compression_vs_quiet.py
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

from drift_landscape import DATA, TARGETS  # noqa: E402

OUT = HERE.parent / "outputs"
TODAY = "2026-07-30"


def describe(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    vals, counts = np.unique(x, return_counts=True)
    n = counts.sum()
    lo, hi = vals.min(), vals.max()
    mode = vals[counts.argmax()]
    m, sd = x.mean(), x.std(ddof=1)
    return dict(
        n=int(n), lo=float(lo), hi=float(hi), n_levels=int(vals.size),
        mode=float(mode),
        modal_position=float((mode - lo) / (hi - lo)) if hi > lo else np.nan,
        modal_share=float(counts.max() / n),
        share_at_lo=float(counts[0] / n), share_at_hi=float(counts[-1] / n),
        skew=float(((x - m) ** 3).mean() / sd ** 3) if sd > 0 else np.nan,
        share_below_mode=float((x < mode).mean()), share_above_mode=float((x > mode).mean()),
        levels_1pct=int((counts / n >= 0.01).sum()),
        eff_levels=float(np.exp(-(lambda p: (p * np.log(p)).sum())(counts / n))))


def sim_compression(rng, n, levels, target_share, reps=1):
    """Symmetric latent squeezed toward the scale midpoint until the modal share matches."""
    edges = np.arange(levels, dtype=float)
    mid = (levels - 1) / 2.0
    lo, hi = 0.01, 5.0
    for _ in range(60):                      # bisect on compression strength
        c = 0.5 * (lo + hi)
        z = rng.standard_normal(n * reps) / c
        b = np.clip(np.round(z + mid), 0, levels - 1)
        share = np.bincount(b.astype(int), minlength=levels).max() / b.size
        if share < target_share:
            lo = c
        else:
            hi = c
    return b


def sim_quiet(rng, n, levels, target_share, reps=1):
    """One-sided latent: symptom usually absent, occasionally present. Mass at an ANCHOR."""
    lo, hi = 0.01, 30.0
    for _ in range(60):                      # bisect on how rarely the symptom fires
        rate = 0.5 * (lo + hi)
        z = rng.exponential(1.0 / rate, n * reps)
        b = np.clip(np.round(z * (levels - 1)), 0, levels - 1)
        share = np.bincount(b.astype(int), minlength=levels).max() / b.size
        if share < target_share:
            hi = rate
        else:
            lo = rate
    return b


def main():
    rng = np.random.default_rng(20260809)
    cfg = TARGETS["kossakowski"]
    df = pd.read_csv(DATA / cfg["path"], sep=cfg["sep"], low_memory=False)
    items = [c for c in cfg["items"] if c in df.columns]

    rows = []
    for it in items:
        x = pd.to_numeric(df[it], errors="coerce").dropna().values
        d = describe(x)
        lv, n, tgt = d["n_levels"], d["n"], d["modal_share"]
        c_sim = describe(sim_compression(rng, n, lv, tgt))
        q_sim = describe(sim_quiet(rng, n, lv, tgt))
        rows.append(dict(unit=it, **d,
                         comp_modal_pos=c_sim["modal_position"], comp_skew=c_sim["skew"],
                         comp_end=c_sim["share_at_lo"] + c_sim["share_at_hi"],
                         quiet_modal_pos=q_sim["modal_position"], quiet_skew=q_sim["skew"],
                         quiet_end=q_sim["share_at_lo"] + q_sim["share_at_hi"]))
    d = pd.DataFrame(rows)
    d["end_use"] = d.share_at_lo + d.share_at_hi
    d.to_csv(OUT / f"compression_vs_quiet_{TODAY}.csv", index=False)

    print("OBSERVED — modal_position 0=low anchor, 0.5=midpoint, 1=high anchor\n")
    cols = ["unit", "n_levels", "levels_1pct", "eff_levels", "modal_share", "mode",
            "modal_position", "share_at_lo", "share_at_hi", "skew"]
    print(d.sort_values("modal_share", ascending=False)[cols]
          .to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    print("\n\nMODEL COMPARISON — each simulation tuned to the SAME modal share\n")
    print(f"{'unit':<14}{'modal_pos':>10}{'  |':>3}{'comp':>7}{'quiet':>8}{'   ':>3}"
          f"{'end_use':>9}{'  |':>3}{'comp':>7}{'quiet':>8}{'   ':>3}"
          f"{'skew':>7}{'  |':>3}{'comp':>7}{'quiet':>8}")
    for _, r in d.sort_values("modal_share", ascending=False).iterrows():
        print(f"{r.unit:<14}{r.modal_position:>10.2f}{'  |':>3}{r.comp_modal_pos:>7.2f}"
              f"{r.quiet_modal_pos:>8.2f}{'   ':>3}{r.end_use:>9.3f}{'  |':>3}"
              f"{r.comp_end:>7.3f}{r.quiet_end:>8.3f}{'   ':>3}{r['skew']:>7.2f}{'  |':>3}"
              f"{r.comp_skew:>7.2f}{r.quiet_skew:>8.2f}")
    print("\nread: for each observed statistic, which simulated mechanism is closer?")
    return d


if __name__ == "__main__":
    main()
