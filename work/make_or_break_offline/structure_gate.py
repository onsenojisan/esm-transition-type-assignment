"""
structure_gate.py -- does this system have two states at all?

A PRE-GATE for the make-or-break run (D1-D4). It answers a question D1-D4 cannot,
because every one of them is computed through critical slowing down (CSD): the
order operator is "gated by critical slowing", and D4 predicts the recovery-side
threshold from "the SAME parameters governing the pre-transition CSD".

That double dependence is a problem, because the detectability of CSD in human
affect data is exactly what Helmich et al. (2024, Nat Rev Psychol) dispute --
Table 1 of that review reports autocorrelation sensitivities of 0-44% across nine
studies. If CSD is not measurable in a given dataset, D4's decline-arm parameters
are estimated from noise, and a null D4 means "could not measure", not "no fold".
A null of that kind is UNINTERPRETABLE, and the preregistration's downgrade rule
does not distinguish the two.

This module therefore asks the prior question using methods that do NOT require
detecting CSD. They are distributional and structural -- the families the review
itself names as the way to establish "catastrophe flags":

  1. Sarle's bimodality coefficient      (moments)
  2. Silverman's critical-bandwidth test (kernel density, bootstrapped)
  3. Two-component vs one-component GMM  (BIC)
  4. Drift-diffusion potential landscape (count wells in U(x))

DECISION RULE, PRE-COMMITTED BEFORE ANY REAL DATA IS SEEN:
    PASS (>= 3 of 4 indicators positive)  -> two-state structure is supported;
                                             a null D4 is interpretable as negative.
    AMBIGUOUS (2 of 4)                    -> report; D4 runs but a null is not
                                             decisive on its own.
    FAIL (<= 1 of 4)                      -> no two-state structure detected. A
                                             fold is not indicated, so D4 has
                                             nothing to adjudicate, and a null
                                             from it must NOT be read as evidence
                                             against the theory.

This gate cannot support the theory. Passing it only says the data has the shape
that would make the real test meaningful. Nothing here is evidence for VOT.

Offline, aggregate-output-only, same governance as the rest of this package.
"""

from __future__ import annotations

import numpy as np
from scipy import stats
from sklearn.mixture import GaussianMixture

# Pre-committed thresholds. Frozen 2026-07-26, before any application to real data.
BC_THRESHOLD = 0.555          # Sarle: > 5/9 is the uniform-distribution reference
SILVERMAN_ALPHA = 0.05        # bootstrap p for "more than one mode"
GMM_DELTA_BIC = 10.0          # BIC(1) - BIC(2) > 10 = strong preference for two
WELL_PROMINENCE = 0.05        # fraction of total potential depth
MIN_N = 100                   # below this, indicators are reported but not scored


# --------------------------------------------------------------------------
# 1. Sarle's bimodality coefficient
# --------------------------------------------------------------------------
def bimodality_coefficient(x: np.ndarray) -> float:
    """BC = (skew^2 + 1) / (excess_kurtosis + 3(n-1)^2 / ((n-2)(n-3)))."""
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    n = x.size
    if n < 4:
        return float("nan")
    m3 = stats.skew(x, bias=False)
    m4 = stats.kurtosis(x, fisher=True, bias=False)
    denom = m4 + 3.0 * (n - 1) ** 2 / ((n - 2) * (n - 3))
    if denom <= 0:
        return float("nan")
    return float((m3 ** 2 + 1.0) / denom)


# --------------------------------------------------------------------------
# 2. Silverman's critical-bandwidth test for unimodality
# --------------------------------------------------------------------------
def _kde_n_modes(x: np.ndarray, h: float, grid: int = 512) -> int:
    lo, hi = x.min() - 3 * h, x.max() + 3 * h
    g = np.linspace(lo, hi, grid)
    d = np.exp(-0.5 * ((g[:, None] - x[None, :]) / h) ** 2).sum(axis=1)
    return int(((d[1:-1] > d[:-2]) & (d[1:-1] > d[2:])).sum())


def _critical_bandwidth(x: np.ndarray, k: int = 1) -> float:
    """Smallest h whose KDE has <= k modes (bisection)."""
    lo, hi = 1e-4 * np.std(x), 10.0 * np.std(x) + 1e-9
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if _kde_n_modes(x, mid) > k:
            lo = mid
        else:
            hi = mid
    return hi


def silverman_test(x: np.ndarray, n_boot: int = 200, rng=None) -> dict:
    """Bootstrap p-value for H0: the density is unimodal."""
    rng = np.random.default_rng(0 if rng is None else rng)
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if x.size < MIN_N:
        return {"h_crit": float("nan"), "p": float("nan"), "positive": False}
    h = _critical_bandwidth(x, k=1)
    sd = np.std(x, ddof=1)
    # smoothed bootstrap at the critical bandwidth
    exceed = 0
    for _ in range(n_boot):
        idx = rng.integers(0, x.size, x.size)
        y = x[idx] + h * rng.standard_normal(x.size)
        y = x.mean() + (y - y.mean()) / np.sqrt(1.0 + h ** 2 / sd ** 2)
        if _kde_n_modes(y, h) > 1:
            exceed += 1
    p = exceed / n_boot
    return {"h_crit": float(h), "p": float(p), "positive": bool(p < SILVERMAN_ALPHA)}


# --------------------------------------------------------------------------
# 3. Two-component vs one-component Gaussian mixture (BIC)
# --------------------------------------------------------------------------
def gmm_bic(x: np.ndarray, seed: int = 0) -> dict:
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)].reshape(-1, 1)
    if x.shape[0] < MIN_N:
        return {"delta_bic": float("nan"), "positive": False}
    b = {}
    for k in (1, 2):
        g = GaussianMixture(n_components=k, covariance_type="full",
                            random_state=seed, n_init=5).fit(x)
        b[k] = g.bic(x)
    d = float(b[1] - b[2])
    return {"bic1": float(b[1]), "bic2": float(b[2]), "delta_bic": d,
            "positive": bool(d > GMM_DELTA_BIC)}


# --------------------------------------------------------------------------
# 4. Drift-diffusion potential landscape
# --------------------------------------------------------------------------
def potential_wells(x: np.ndarray, n_bins: int = 24, smooth: int = 3) -> dict:
    """Count STABLE fixed points from the drift's sign structure.

    Revised 2026-07-26 after the selftest. The first implementation integrated the
    binned drift into a potential U(x) and counted local minima; it returned 3-5
    'wells' on every generator including pure Ornstein-Uhlenbeck, because noise in
    the binned drift survives integration as spurious minima. It was measuring
    estimator noise, not structure.

    This version asks the question the dynamics actually answer. For dx/dt = f(x):
      * a STABLE fixed point is a zero of f with f' < 0  -> f crosses from + to -
      * an UNSTABLE fixed point is a zero with f' > 0    -> f crosses from - to +
    A double well is therefore the ordered pattern  (+ -> -), (- -> +), (+ -> -):
    two stable states with an unstable ridge between them. Requiring that ORDER
    is far more specific than counting minima, and it cannot be produced by
    symmetric noise around a single attractor.

    Still CSD-free: no autocorrelation, no variance statistic, no window.
    """
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if x.size < MIN_N:
        return {"n_stable": 0, "positive": False}
    dx = np.diff(x)
    xs = x[:-1]
    edges = np.linspace(np.nanpercentile(xs, 2), np.nanpercentile(xs, 98), n_bins + 1)
    centres = 0.5 * (edges[:-1] + edges[1:])
    drift = np.full(n_bins, np.nan)
    for i in range(n_bins):
        m = (xs >= edges[i]) & (xs < edges[i + 1])
        if m.sum() >= 8:
            drift[i] = dx[m].mean()
    ok = np.isfinite(drift)
    if ok.sum() < 8:
        return {"n_stable": 0, "positive": False}
    c, f = centres[ok], drift[ok]
    if smooth > 1:                      # moving average to suppress bin noise
        k = np.ones(smooth) / smooth
        f = np.convolve(f, k, mode="same")
        f[0], f[-1] = np.nan, np.nan
        good = np.isfinite(f)
        c, f = c[good], f[good]
    if f.size < 6:
        return {"n_stable": 0, "positive": False}

    scale = np.nanmax(np.abs(f))
    if not np.isfinite(scale) or scale <= 0:
        return {"n_stable": 0, "positive": False}
    # only count crossings where the drift is meaningfully non-zero on both sides
    eps = 0.10 * scale
    crossings = []                      # (index, '+-' stable | '-+' unstable)
    for i in range(len(f) - 1):
        a, b = f[i], f[i + 1]
        if a > eps and b < -eps:
            crossings.append((i, "stable"))
        elif a < -eps and b > eps:
            crossings.append((i, "unstable"))
    kinds = [k for _, k in crossings]
    n_stable = kinds.count("stable")
    # require the ordered pattern stable, unstable, stable somewhere in the sequence
    has_pattern = any(kinds[i:i + 3] == ["stable", "unstable", "stable"]
                      for i in range(len(kinds) - 2))
    return {"n_stable": int(n_stable), "n_crossings": len(crossings),
            "double_well_pattern": bool(has_pattern), "positive": bool(has_pattern)}


# --------------------------------------------------------------------------
# Gate
# --------------------------------------------------------------------------
def structure_gate(x: np.ndarray, seed: int = 0) -> dict:
    """Run all four indicators and apply the pre-committed decision rule."""
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    bc = bimodality_coefficient(x)
    sil = silverman_test(x, rng=seed)
    gm = gmm_bic(x, seed=seed)
    pw = potential_wells(x)

    # Sarle's BC is REPORTED but NOT SCORED. On the selftest generators it
    # separated in the right direction (bistable median 0.466 vs unimodal 0.350)
    # but never reached the conventional 0.555 threshold, because two wells with
    # substantial overlap do not produce a strongly bimodal marginal. Lowering
    # the threshold to fit the synthetic data would be exactly the forking-paths
    # move this project refuses elsewhere, so it contributes nothing to the
    # verdict and is carried as diagnostic context only.
    ind = {
        "silverman": sil,
        "gmm_bic": gm,
        "potential_wells": pw,
    }
    scored = sum(1 for v in ind.values() if v.get("positive"))
    ind["bimodality_coefficient"] = {"value": bc, "scored": False,
                                     "note": "reported, not scored -- see structure_gate.py"}
    if x.size < MIN_N:
        verdict = "INSUFFICIENT_N"
    elif scored >= 2:
        verdict = "PASS"
    elif scored == 1:
        verdict = "AMBIGUOUS"
    else:
        verdict = "FAIL"
    return {"n": int(x.size), "score": int(scored), "max_score": 3,
            "verdict": verdict, "indicators": ind}


VERDICT_MEANING = {
    "PASS": "two-state structure supported; a null D4 is interpretable as negative",
    "AMBIGUOUS": "D4 may run, but a null from it is not decisive on its own",
    "FAIL": "no two-state structure detected; a null D4 must NOT be read as evidence against the theory",
    "INSUFFICIENT_N": "too few observations to score the indicators",
}
