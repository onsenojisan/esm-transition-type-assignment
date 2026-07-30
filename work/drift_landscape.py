"""drift_landscape.py -- nonparametric drift-diffusion estimation, to ask whether a
series has one attractor or two.

Why this and not the pre-gate
-----------------------------
`structure_gate.py` asks whether the MARGINAL DISTRIBUTION has two modes. Today's
re-analysis showed that question is capped below ~6 SD separation whatever
instrument is used, and Cui, Hasselman & Lichtwarck-Aschoff (2023, Psychological
Methods, doi:10.1037/met0000623) show why it is the wrong question: bimodality in
intensive longitudinal data does not imply bistability, and their three failure
conditions -- shuffled data, sampling slower than the transitions, and bimodality
produced by a transformation of a monostable system -- are indistinguishable from
the marginal alone.

Their fitlandr works on the DYNAMICS instead: estimate the drift field
nonparametrically, and read the attractors off it. Attractors are a property of the
drift, not of the histogram. That is the level this project has never measured at.

fitlandr is R and there is no R here, so this ports the load-bearing estimator
rather than the package. What is ported is the Multivariate Kernel Estimator of
Bandi & Moloche (2018) as fitlandr uses it:

    mu_hat(x)    = sum_t w_t (X_{t+1} - X_t)            / (dt * sum_t w_t)
    sigma2_hat(x)= sum_t w_t (X_{t+1} - X_t)(...)^T     / (dt * sum_t w_t)
    w_t          = Gaussian product kernel on (X_t - x)/h

Stable fixed points are then located directly: in 1-D, zeros of mu_hat with
negative slope; in 2-D, zeros of the field with both Jacobian eigenvalues having
negative real part. The count of stable fixed points is the answer to "one
attractor or two".

NOT ported: the Monte-Carlo steady-state landscape. The landscape is a
visualisation of the same drift field, and the attractor count is what the project
needs, so the extra layer would add error without adding an answer.

Honest limits, inherited and added
----------------------------------
* Markov assumption -- drift depends on the current state only. So this can find
  two attractors; it cannot find HYSTERESIS, which is history dependence. It is
  the complement of HysTAR, not a substitute, and it cannot run D4.
* Stationarity -- the drift field is assumed not to change over time. Olthof et al.
  (2020) report non-stationarity and many change points in the very series this is
  applied to, so a single global field is a summary, not a description. There is
  NO windowing option here; an earlier version of this docstring claimed a
  `windows=` argument that was never implemented, and the claim is withdrawn
  rather than back-filled, because a windowed field is what the B-vs-N question
  needs and it should be built deliberately, not implied.
* Equal spacing -- ESM has night gaps. `within_day=` restricts increments to pairs
  inside the same day.
* Bandwidth -- fitlandr's exact selector is not reproduced. `bw_mult=` sweeps it,
  and any conclusion that does not survive the sweep is not reported as a finding.

Validation: `selftest()` runs known bistable and monostable generators at the
length and noise of the target series and reports recovered attractor counts.

Usage:  python work/drift_landscape.py selftest
        python work/drift_landscape.py kossakowski
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "outputs"


# --------------------------------------------------------------------------
# MVKE drift / diffusion
# --------------------------------------------------------------------------
def mvke_1d(x: np.ndarray, grid: np.ndarray, h: float, dt: float = 1.0,
            pairs: np.ndarray | None = None):
    """Returns (drift, diffusion, weight_mass) evaluated on `grid`.

    `pairs` selects which (t, t+1) increments are usable; default is all.
    """
    x = np.asarray(x, float)
    if pairs is None:
        pairs = np.arange(x.size - 1)
    x0 = x[pairs]
    dx = x[pairs + 1] - x[pairs]
    z = (x0[None, :] - grid[:, None]) / h
    w = np.exp(-0.5 * z ** 2)
    mass = w.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        drift = (w * dx[None, :]).sum(axis=1) / (dt * mass)
        diff = (w * (dx ** 2)[None, :]).sum(axis=1) / (dt * mass)
    return drift, diff, mass


def support_window(mass: np.ndarray, mass_frac: float = 0.02):
    """Index bounds of the region where the field is actually estimated.

    Grid points whose kernel weight mass is below `mass_frac` of the maximum drop
    out -- the field is not estimated there, and unsupported tails otherwise
    manufacture fixed points.
    """
    ok = mass >= mass_frac * np.nanmax(mass)
    idx = np.nonzero(ok)[0]
    if idx.size < 3:
        return None
    return int(idx.min()), int(idx.max())


def fixed_points_1d(grid: np.ndarray, drift: np.ndarray, mass: np.ndarray,
                    mass_frac: float = 0.02):
    """Zero crossings of the drift inside the well-supported region.

    Returns (stable, unstable). A downward crossing (drift + -> -) is a stable
    fixed point; an upward crossing (- -> +) is an unstable one, i.e. the BARRIER
    between two basins. The unstable half was not extracted before, and without it
    there is no way to ask how deep a well is -- only how many wells there are.
    """
    win = support_window(mass, mass_frac)
    if win is None:
        return [], []
    lo, hi = win
    g, d = grid[lo:hi + 1], drift[lo:hi + 1]
    stable, unstable = [], []
    for i in range(len(g) - 1):
        a, b = d[i], d[i + 1]
        if not (np.isfinite(a) and np.isfinite(b)):
            continue
        if a == 0.0:
            if i > 0 and d[i - 1] > 0:
                stable.append(g[i])
            elif i > 0 and d[i - 1] < 0:
                unstable.append(g[i])
            continue
        if a > 0 > b:                      # downward crossing == stable
            stable.append(g[i] + (a / (a - b)) * (g[i + 1] - g[i]))
        elif a < 0 < b:                    # upward crossing == barrier
            unstable.append(g[i] + (a / (a - b)) * (g[i + 1] - g[i]))
    return stable, unstable


def stable_points_1d(grid: np.ndarray, drift: np.ndarray, mass: np.ndarray,
                     mass_frac: float = 0.02):
    """The stable half of `fixed_points_1d`.

    Kept as a named entry point because the stable-point logic is unchanged from
    the run that produced `drift_landscape_selftest_2026-07-30.csv`; the attractor
    counts there stay reproducible.
    """
    return fixed_points_1d(grid, drift, mass, mass_frac)[0]


# --------------------------------------------------------------------------
# Landscape geometry: how deep is the well, relative to the noise in it
# --------------------------------------------------------------------------
# The estimator already returned the diffusion term and nothing read it. It is
# the missing half of the picture: an attractor count says how many wells there
# are, and says nothing about whether the noise can walk out of them.
#
# From the estimated drift the potential is U(x) = -int mu dx, so U' = -mu and
# U'' = -mu'. For dX = -U'(X) dt + sigma dW the stationary density is
# proportional to exp(-2U/sigma^2), which makes
#
#     b = 2 * deltaU / sigma^2
#
# the dimensionless barrier -- the log of the Arrhenius factor. Small b means
# noise crosses freely: the system diffuses over the landscape instead of sitting
# in a basin and occasionally jumping. That is Cui et al. (2025)'s N-DIFFUSION
# rather than a discrete transition, and it is the distinction the project's
# marginal-modality pre-gate cannot make even in principle.
#
# The matching escape time is the Kramers estimate
#
#     tau = 2*pi / sqrt(lambda_well * lambda_barrier) * exp(b)
#
# in units of the sampling interval (dt = 1 here), so it is directly comparable
# to the length of the series. Reported as log10 because it overflows readily.
#
# HONEST LIMIT: Kramers assumes constant sigma and a smooth double well. The
# diffusion estimate here is state-dependent, so sigma^2 is averaged over the
# path from well to barrier and that choice is recorded rather than hidden. These
# are order-of-magnitude quantities, and are used below only as thresholds
# calibrated on synthetic generators, never as point estimates.


def potential_1d(grid: np.ndarray, drift: np.ndarray) -> np.ndarray:
    """U(x) = -integral of the drift, by trapezoid. Only differences of U matter."""
    dx = np.diff(grid)
    incr = 0.5 * (drift[:-1] + drift[1:]) * dx
    return np.concatenate([[0.0], -np.cumsum(incr)])


def well_geometry(grid, drift, diffusion, mass, stable, unstable, mass_frac=0.02):
    """Per-attractor barrier height, local noise scale and Kramers dwell time.

    Returns a list of dicts, one per stable point, ordered as `stable`. Each has
    the governing (easiest) escape route -- the adjacent barrier with the smallest
    dimensionless height, because that is the one the system actually leaves by.
    """
    win = support_window(mass, mass_frac)
    if win is None or not stable:
        return []
    lo, hi = win
    g = grid[lo:hi + 1]
    d = np.asarray(drift[lo:hi + 1], float)
    s2 = np.asarray(diffusion[lo:hi + 1], float)

    # interpolate across any interior gaps so the integral is defined
    for arr in (d, s2):
        bad = ~np.isfinite(arr)
        if bad.all():
            return []
        if bad.any():
            arr[bad] = np.interp(g[bad], g[~bad], arr[~bad])

    U = potential_1d(g, d)
    slope = np.gradient(d, g)                     # mu'(x); U'' = -mu'

    out = []
    for xs in stable:
        lam = -float(np.interp(xs, g, slope))     # U''(x*) > 0 at a stable point
        sig2_w = float(np.interp(xs, g, s2))
        rec = dict(attractor=float(xs), lam=lam, sigma2=sig2_w,
                   local_sd=float(np.sqrt(sig2_w / (2 * lam))) if lam > 0 else np.nan,
                   barrier=np.nan, barrier_dist=np.nan, delta_U=np.nan,
                   barrier_ratio=np.nan, log10_dwell=np.nan)
        best = None
        for xb in unstable:
            dU = float(np.interp(xb, g, U) - np.interp(xs, g, U))
            if not np.isfinite(dU) or dU <= 0:
                continue                          # not a barrier from this well
            span = (g >= min(xs, xb)) & (g <= max(xs, xb))
            sig2_path = float(np.nanmean(s2[span])) if span.any() else sig2_w
            if sig2_path <= 0:
                continue
            b = 2 * dU / sig2_path
            lam_b = abs(float(np.interp(xb, g, slope)))
            pref = (2 * np.pi / np.sqrt(lam * lam_b)) if (lam > 0 and lam_b > 0) else np.nan
            log10_tau = (np.log10(pref) + b / np.log(10)) if np.isfinite(pref) else np.nan
            if best is None or b < best[0]:
                best = (b, xb, dU, log10_tau)
        if best is not None:
            b, xb, dU, log10_tau = best
            rec.update(barrier=float(xb), barrier_dist=float(abs(xb - xs)),
                       delta_U=float(dU), barrier_ratio=float(b),
                       log10_dwell=float(log10_tau))
        out.append(rec)
    return out


def run_length(x, split=None) -> float:
    """Mean run length on which side of `split` the series sits, in observations.

    The model-free dwell measure. `split` defaults to the mean; pass the barrier
    position when the landscape has one. Unlike the Kramers estimate this assumes
    nothing about barrier shape or noise constancy, which is why it is the one
    reported for observed series -- see the note in `analyse_1d`.
    """
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if x.size < 2:
        return np.nan
    s = np.sign(x - (np.mean(x) if split is None else split))
    s = s[s != 0]
    if s.size < 2:
        return np.nan
    flips = int(np.count_nonzero(np.diff(s) != 0))
    return float(s.size / (flips + 1))


def within_day_pairs(day: np.ndarray) -> np.ndarray:
    """Increment indices whose t and t+1 fall on the same study day."""
    day = np.asarray(day)
    return np.nonzero(day[:-1] == day[1:])[0]


def analyse_1d(x, day=None, n_grid=120, bw_mult=1.0, mass_frac=0.02,
               within_day=False):
    x = np.asarray(x, float)
    keep = np.isfinite(x)
    if day is not None:
        day = np.asarray(day)[keep]
    x = x[keep]
    if x.size < 60:
        return None
    sd = np.std(x, ddof=1)
    if sd <= 0:
        return None
    h = bw_mult * 1.06 * sd * x.size ** (-1 / 5)          # Silverman-type, swept
    grid = np.linspace(x.min(), x.max(), n_grid)
    pairs = within_day_pairs(day) if (within_day and day is not None) else None
    drift, diff, mass = mvke_1d(x, grid, h, pairs=pairs)
    roots, barriers = fixed_points_1d(grid, drift, mass, mass_frac)
    wells = well_geometry(grid, drift, diff, mass, roots, barriers, mass_frac)

    # The governing escape route is the shallowest barrier anywhere in the
    # landscape: that is the one the system actually leaves by, and it is what
    # decides whether a "transition" is a discrete event or free diffusion.
    # --- degeneracy guards, added 2026-07-30 after they were needed -------------
    # A series that is mostly ONE response level gives the drift field almost no
    # support: the estimate is driven by a handful of minority responses and its
    # zero-crossing wanders between adjacent Likert levels while the mean stays
    # pinned by the mass. That produced a spurious "moving attractor" in three
    # Kossakowski items (modal share 0.67-0.84) and cost a retraction --
    # `moving_well_retraction_2026-07-30.md`.
    vals, counts = np.unique(x, return_counts=True)
    modal_share = float(counts.max() / x.size)
    degenerate_support = modal_share > MODAL_SHARE_MAX
    # A well with lambda ~ 0 has a meaningless local SD; it is a failed fit, not a
    # flat well. Guilty's window 3 returned local_sd = 56.7 x the series SD.
    for w in wells:
        if np.isfinite(w["local_sd"]) and w["local_sd"] > LOCAL_SD_MAX_MULT * sd:
            w["local_sd"] = np.nan
            w["degenerate_fit"] = True
        else:
            w["degenerate_fit"] = False

    ratios = [w["barrier_ratio"] for w in wells if np.isfinite(w["barrier_ratio"])]
    gov = min(wells, key=lambda w: w["barrier_ratio"]) if ratios else None
    local_sds = [w["local_sd"] for w in wells if np.isfinite(w["local_sd"])]

    # Model-light dwell, because the Kramers estimate is only valid for b >> 1 and
    # selftest shows it overstates by 5-10x in the shallow-barrier regime the real
    # data sits in. Mean run length either side of the governing barrier needs no
    # landscape model at all.
    split = gov["barrier"] if (gov and np.isfinite(gov["barrier"])) else float(np.mean(x))
    run_len = run_length(x, split)

    return dict(n=int(x.size), n_pairs=int(len(pairs) if pairs is not None else x.size - 1),
                h=float(h), sd=float(sd), n_attractors=len(roots),
                attractors=[float(r) for r in roots],
                separation_sd=(float(abs(roots[-1] - roots[0]) / sd) if len(roots) >= 2 else np.nan),
                n_barriers=len(barriers), barriers=[float(b) for b in barriers],
                wells=wells,
                barrier_ratio=(float(gov["barrier_ratio"]) if gov else np.nan),
                log10_dwell=(float(gov["log10_dwell"]) if gov else np.nan),
                barrier_dist_sd=(float(gov["barrier_dist"] / sd) if gov else np.nan),
                local_sd_sd=(float(np.median(local_sds) / sd) if local_sds else np.nan),
                run_length_obs=run_len,
                modal_share=modal_share, degenerate_support=degenerate_support,
                n_degenerate_fits=int(sum(w.get("degenerate_fit", False) for w in wells)),
                grid=grid, drift=drift, diffusion=diff, mass=mass)


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------
# The generators are the project's own, from work/make_or_break_offline/
# calibrate_structure_gate.py, unchanged -- SIGMA = 0.35 there, which keeps the
# cubic Euler step stable (a naive sigma = 1 double well diverges) and makes these
# results directly comparable to the existing pre-gate calibration.
sys.path.insert(0, str(HERE / "make_or_break_offline"))
from calibrate_structure_gate import bistable as _proj_bistable      # noqa: E402
from calibrate_structure_gate import unimodal as _proj_unimodal      # noqa: E402


def gen_bistable(rng, T, sep_sd=3.0):
    """Project's double well. sep_sd is the minima separation in noise SD units."""
    return _proj_bistable(rng, T, sep_sd)


def gen_monostable(rng, T):
    return _proj_unimodal(rng, T)


def gen_polarized(rng, T, gain=1.6):
    """Cui et al.'s 'polarized interpretation' condition: a MONOSTABLE series pushed
    through a saturating transform, so the marginal is bimodal while the dynamics
    are not. This is the case that defeats every marginal-distribution method, and
    the one the drift field is supposed to get right."""
    y = _proj_unimodal(rng, T)
    y = (y - y.mean()) / y.std(ddof=1)
    return np.tanh(y * gain)


def gen_deep_well(rng, T, sep_sd=6.0, k=1.0, n_sub=20):
    """NEW generator, not part of the original calibration set.

    Same double well as the project's, but integrated with sub-steps so a larger
    drift coefficient k stays numerically stable. One observation spans unit time,
    so the series is directly comparable to the project's generators and to the
    estimator's dt = 1: per-substep noise is SIGMA*sqrt(dt).

    It exists to check that the barrier index RESPONDS. If every generator the
    project owns sits in the shallow-barrier regime, a barrier index calibrated on
    them alone would be untested at the other end of its range.
    """
    sigma = 0.35
    a = sep_sd * sigma / 2.0
    dt = 1.0 / n_sub
    x = np.empty(T)
    v = -a
    for t in range(T):
        for _ in range(n_sub):
            v += -k * (v ** 3 - a ** 2 * v) * dt + sigma * np.sqrt(dt) * rng.standard_normal()
        x[t] = v
    return x


def true_dwell(x):
    """Ground truth for the Kramers estimate.

    For these symmetric double wells the sign of the deviation from the mean says
    which basin the system is in, so `run_length` about the mean IS the dwell time.
    Meaningless for a monostable series -- there it measures how fast the series
    crosses its own mean, which is why it is reported for every case and
    interpreted only for the bistable ones.
    """
    return run_length(x)


def selftest(reps=40, Ts=(300, 1476), bw_mults=(0.7, 1.0, 1.4),
             out_name="drift_landscape_selftest_v2_2026-07-30.csv"):
    rng = np.random.default_rng(20260730)
    rows = []
    cases = [("bistable 2SD", lambda T: gen_bistable(rng, T, 2.0)),
             ("bistable 3SD", lambda T: gen_bistable(rng, T, 3.0)),
             ("bistable 4SD", lambda T: gen_bistable(rng, T, 4.0)),
             ("bistable 6SD", lambda T: gen_bistable(rng, T, 6.0)),
             ("deep well 6SD (k=1, new)", lambda T: gen_deep_well(rng, T, 6.0)),
             ("monostable", lambda T: gen_monostable(rng, T)),
             ("polarized (bimodal, monostable)", lambda T: gen_polarized(rng, T))]
    for T in Ts:
        for name, gen in cases:
            for bw in bw_mults:
                counts, brs, dwells, truedw, lsd = [], [], [], [], []
                for _ in range(reps):
                    x = gen(T)
                    r = analyse_1d(x, bw_mult=bw)
                    if not r:
                        continue
                    counts.append(r["n_attractors"])
                    truedw.append(true_dwell(x))
                    for key, acc in (("barrier_ratio", brs), ("log10_dwell", dwells),
                                     ("local_sd_sd", lsd)):
                        if np.isfinite(r[key]):
                            acc.append(r[key])
                counts = np.array(counts)
                rows.append(dict(
                    T=T, case=name, bw_mult=bw,
                    share_2plus=float((counts >= 2).mean()),
                    share_1=float((counts == 1).mean()),
                    mean_count=float(counts.mean()),
                    share_with_barrier=float(len(brs) / max(len(counts), 1)),
                    barrier_ratio_med=(float(np.median(brs)) if brs else np.nan),
                    log10_dwell_med=(float(np.median(dwells)) if dwells else np.nan),
                    true_log10_dwell_med=float(np.log10(np.nanmedian(truedw))),
                    local_sd_over_series_sd=(float(np.median(lsd)) if lsd else np.nan)))
    d = pd.DataFrame(rows)
    with pd.option_context("display.width", 200, "display.max_columns", 50):
        print(d.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    d.to_csv(OUT / out_name, index=False)
    print("\nread:")
    print("  share_2plus            on bistable rows POWER; on monostable/polarized FALSE ALARM")
    print("  barrier_ratio_med      b = 2*dU/sigma^2, the dimensionless barrier. b << 1 means")
    print("                         noise crosses freely -- N-diffusion, not discrete transitions")
    print("  log10_dwell_med        Kramers estimate, in observations")
    print("  true_log10_dwell_med   measured mean run length of the generator. The comparison")
    print("                         with the column above is the validation of the estimate")
    print("\nthe original attractor-count columns are unchanged from")
    print("drift_landscape_selftest_2026-07-30.csv; that file is not overwritten.")
    return d


# --------------------------------------------------------------------------
# Application to the acquired data
# --------------------------------------------------------------------------
DATA = HERE / "acquired_data"

TARGETS = {
    "kossakowski": dict(
        path="kossakowski/ESMdata/ESMdata.csv", sep=",", id=None, day="dayno",
        items=["mood_relaxed", "mood_down", "mood_irritat", "mood_satisfi", "mood_lonely",
               "mood_anxious", "mood_enthus", "mood_cheerf", "mood_guilty", "mood_strong"]),
    "fisher": dict(
        path="fisher/0033_fisher_ts.tsv", sep="\t", id="id", day="day",
        items=["energetic", "enthusiastic", "content", "irritable", "restless", "worried",
               "guilty", "afraid", "anhedonia", "angry", "hopeless", "down", "positive"]),
    "geschwind": dict(
        path="geschwind/0010_geschwind_ts.tsv", sep="\t", id="id", day="day",
        items=["cheerful", "pleasantness", "worried", "fearful", "sad", "relaxed"]),
    "marian": dict(
        path="marian/0052_marian_ts.tsv", sep="\t", id="id", day="day",
        items=["worry", "restless", "irritable", "anhedonia", "depressed",
               "worthlessness", "something_wrong", "dont_like_self", "no_good"]),
}

# bw_mult 1.4 is the primary operating point: 0% false alarms on BOTH null cases at
# both lengths in selftest. 1.0 is reported as a sensitivity (5% false alarm at
# T=1476). Anything that appears only at 0.7 is not reported as a finding.
BW_PRIMARY, BW_SENS = 1.4, 1.0
MIN_OBS_RUN = 200          # fitlandr's own stated working range starts around here

# Degeneracy guards (see analyse_1d). MODAL_SHARE_MAX 0.60 sits in the gap between
# the three items that produced the retracted result (0.67, 0.82, 0.84) and every
# other unit in the same dataset (<= 0.48). It is a floor on support, not a tuned
# threshold. LOCAL_SD_MAX_MULT rejects lambda ~ 0 fits, which return a local SD of
# many times the series SD.
MODAL_SHARE_MAX = 0.60
LOCAL_SD_MAX_MULT = 3.0

# --------------------------------------------------------------------------
# Q1 of the transition-type assignment. FROZEN in
# outputs/transition_type_assignment_spec_v1.md before this was run on any
# observed series; thresholds come from the synthetic selftest only.
#
#   B_GATE      1.0  primary. The estimator reads b low by roughly 2-3x (selftest:
#                    measured 0.63-0.95 where the generator's true b is 1.24;
#                    measured 1.5 where it is ~5), so measured 1.0 corresponds to a
#                    true barrier of about 2-3, i.e. an Arrhenius factor of 7-20.
#                    Set on the physics, not on the generator spread.
#   B_GATE_SENS 0.3  sensitivity. Sits inside the empty decade between the 4 SD
#                    generator (0.049) and the 6 SD generator (0.626) at bw 1.4.
B_GATE, B_GATE_SENS = 1.0, 0.3

NO_SECOND_ATTRACTOR = "no-second-attractor"
N_DIFFUSION = "N-diffusion"
DISCRETE = "discrete-transition(B-or-N)"


def assign_q1(n_attractors, barrier_ratio, gate=B_GATE):
    """Cui et al. (2025) Figure 8, Q1, made quantitative.

    Their question -- is the state qualitatively different, or are you just in it
    more or less often -- is here: is there a second attractor with a barrier the
    noise cannot walk over? A shallow barrier means occupancy changes without a
    discrete transition, which is their N-diffusion.

    Returns the label only. B versus N is Q2 and is NOT decided here; it needs a
    windowed stability estimate, and is out of scope by the spec.
    """
    if n_attractors < 2 or not np.isfinite(barrier_ratio):
        return NO_SECOND_ATTRACTOR
    return DISCRETE if barrier_ratio >= gate else N_DIFFUSION


def run(which=("kossakowski",), min_obs=MIN_OBS_RUN):
    rows = []
    for name in which:
        cfg = TARGETS[name]
        df = pd.read_csv(DATA / cfg["path"], sep=cfg["sep"], low_memory=False)
        idcol = cfg["id"]
        if idcol is None:
            df["_id"] = 1
            idcol = "_id"
        daycol = cfg["day"] if cfg["day"] in df.columns else None
        items = [c for c in cfg["items"] if c in df.columns]
        for pid, g in df.groupby(idcol):
            sub = g[items].apply(pd.to_numeric, errors="coerce")
            day = g[daycol].values if daycol else None
            units = [(it, sub[it].values) for it in items]
            z = (sub - sub.mean()) / sub.std(ddof=1)
            units.append(("_composite", z.mean(axis=1, skipna=True).values))
            for unit, x in units:
                if np.isfinite(x).sum() < min_obs:
                    continue
                for bw, tag in ((BW_PRIMARY, "primary"), (BW_SENS, "sensitivity")):
                    for wd in (False, True) if day is not None else (False,):
                        r = analyse_1d(x, day=day, bw_mult=bw, within_day=wd)
                        if r is None:
                            continue
                        rows.append(dict(dataset=name, person=str(pid), unit=unit,
                                         bw_mult=bw, bw_tag=tag, within_day=wd,
                                         n=r["n"], n_pairs=r["n_pairs"],
                                         n_attractors=r["n_attractors"],
                                         separation_sd=r["separation_sd"],
                                         n_barriers=r["n_barriers"],
                                         barrier_ratio=r["barrier_ratio"],
                                         barrier_dist_sd=r["barrier_dist_sd"],
                                         local_sd_sd=r["local_sd_sd"],
                                         run_length_obs=r["run_length_obs"],
                                         q1_primary=assign_q1(r["n_attractors"],
                                                              r["barrier_ratio"], B_GATE),
                                         q1_sensitivity=assign_q1(r["n_attractors"],
                                                                  r["barrier_ratio"], B_GATE_SENS),
                                         kramers_log10_dwell_INVALID=r["log10_dwell"],
                                         attractors=";".join(f"{a:.3f}" for a in r["attractors"])))
    d = pd.DataFrame(rows)
    if d.empty:
        print(f"no series reached {min_obs} observations")
        return d
    d.to_csv(OUT / "drift_landscape_result_2026-07-30.csv", index=False)

    print("=" * 76)
    print(f"DRIFT FIELD + BARRIER GEOMETRY  (series with >= {min_obs} observations)")
    print(f"Q1 gate: barrier_ratio >= {B_GATE} discrete, else N-diffusion "
          f"(sensitivity {B_GATE_SENS}). Frozen before this run.")
    print("=" * 76)
    for (ds, tag, wd), g in d.groupby(["dataset", "bw_tag", "within_day"]):
        lab = "within-day pairs only" if wd else "all consecutive pairs"
        print(f"\n{ds} | bw {g.bw_mult.iloc[0]} ({tag}) | {lab} | {len(g)} series")
        print(f"  median observations        {g.n.median():.0f}")
        print(f"  >= 2 attractors           {100*(g.n_attractors >= 2).mean():5.1f}%  "
              f"({int((g.n_attractors >= 2).sum())}/{len(g)})")
        print(f"  median run length          {g.run_length_obs.median():.1f} obs")
        print(f"  median local_sd / series sd {g.local_sd_sd.median():.2f}")
        print("  Q1 assignment (primary):")
        for lbl, cnt in g.q1_primary.value_counts().items():
            print(f"     {lbl:<28} {cnt:4d} / {len(g)}")
        sens = g.q1_sensitivity.value_counts().to_dict()
        print(f"  Q1 at sensitivity gate:  {sens}")
        two = g[g.n_attractors >= 2]
        if len(two):
            print(f"  where 2+: separation median {two.separation_sd.median():.2f} SD, "
                  f"barrier_ratio median {two.barrier_ratio.median():.3f}")
            for _, r in two.sort_values('barrier_ratio', ascending=False).iterrows():
                print(f"     {r['unit']:<16} n={r['n']:<5} sep={r['separation_sd']:.2f} SD  "
                      f"b={r['barrier_ratio']:.3f}  runlen={r['run_length_obs']:.1f}  "
                      f"at [{r['attractors']}]")
    print(f"\nwrote {OUT / 'drift_landscape_result_2026-07-30.csv'}")
    print("NOTE: kramers_log10_dwell_INVALID is recorded and must not be read as an")
    print("estimate -- selftest shows it overstates 5-10x when b << 1, which is the")
    print("regime these series are in. Use run_length_obs.")
    return d


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "selftest":
        selftest()
    elif arg in TARGETS:
        run((arg,))
    elif arg == "all":
        run(tuple(TARGETS))
    else:
        print(__doc__)
