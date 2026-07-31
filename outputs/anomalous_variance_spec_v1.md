# Anomalous variance (Gilmore flag 8) — spec v1.0, FROZEN

**Frozen 2026-07-30. Committed to version control BEFORE execution** — unlike the two specifications
deposited earlier today, whose ordering is documented only in the files. That weakness is recorded in
`note_v04_punch_list_2026-07-30.md` §3 and this spec is the first to repair it.

## 0. What this is

`catastrophe_flags_primary_source_2026-07-30.md` established that Gilmore (1981) distinguishes **eight**
catastrophe flags, that only three are anticipatory, and that of those three the project has done one (CSD,
under critique), one is structurally unavailable (divergence of linear response — needs perturbations), and
one is unexamined: **anomalous variance**.

van der Maas & Molenaar (1992) give it two consequences:

> The first consequence for the behavioral variance arises from **changes in the correlation structure** if
> the system approaches a catastrophe point. The changes concerned imply that **common factors will
> disappear.**

> The second consequence refers to the influence of a newly emerging equilibrium … closely related to
> **response variability or oscillations**.

The **second** overlaps the variance component of the EWS battery already run. The **first** is
multivariate, has never been tested here, and is computable on the ten simultaneously-measured items.

## 1. The logical limit, fixed before running

Anomalous variance is an **anticipatory** flag: it is supposed to appear *before* the bifurcation set is
entered. **This project has not identified a transition.** So the flag has no referent, exactly as B-versus-N
had none once Q1 returned no discrete transition.

**Therefore this run does not test the flag.** It tests the necessary condition:

> **Is the common-factor structure of the ten items stationary across the series?**

- Stationary → the flag is **absent**, and that is a real negative.
- Non-stationary → **suggestive only**. It becomes flag evidence only if a transition is separately
  identified, and none is. It may **not** be reported as the flag being present.

This asymmetry is frozen here so it cannot be relaxed after seeing the result.

## 2. The trap this walks into, named in advance

The project's own record forbids the naive version. `the_pleasure_order_bxkz_layer_scheme_decision_v0.1.md`
§4:

> **No load-bearing claim may rest on the four faces being empirically separable**, and the layers must be
> measured by non-self-report means … **Self-report batteries will collapse into a general factor and
> reproduce the O/M/A outcome.**

A first-principal-component statistic on ten self-reported mood items is *precisely* the positive-manifold
quantity that sank O/M/A. Two guards follow:

1. **The claim here is about CHANGE, not level.** That PC1 share is high is expected and is not a finding.
   Only its variation across windows is read.
2. **If the statistic has no dynamic range — if PC1 share is nearly constant across windows in the
   calibration nulls AND the alternative — the test has no power and reports "cannot answer", not
   "stationary".** Determined by calibration, before the data is touched.

## 3. Statistic

Per window, on the ten items z-scored within window:

- **Primary: `pc1_share`** — the largest eigenvalue of the 10×10 Pearson correlation matrix, divided by 10.
- **Secondary: `mean_abs_r`** — the mean absolute off-diagonal correlation.

Windows: **6 contiguous**, matching every windowed analysis run today (~246 observations each). **12
windows** reported as a sensitivity.

Test statistic for stationarity: **`range_pc1` = max − min of `pc1_share` across windows.** Compared against
a null distribution from a generator with a constant common factor at matched length, item count and
autocorrelation.

## 4. Calibration, on synthetic data only, before the observed run

Generator: ten items loading on one latent AR(1) factor,
`x_i,t = λ_t · f_t + sqrt(1 − λ_t²) · e_i,t`, φ matched to the data's autocorrelation.

- **null:** λ constant
- **alternative:** λ ramps **down** across the series (the common factor weakening — the flag's own
  mechanism), swept over several ramp depths

Reported: null p95 of `range_pc1`, and power at each ramp depth.

**Discretisation is applied**, because it is not optional here: `compression_vs_quiet_result_2026-07-30.md`
established that four of these items deliver **1.4–2.8 effective response levels**, and correlations
computed on ~2-level variables are attenuated. The calibration therefore runs both continuous and
discretised-to-the-items'-own-levels, and **the discretised arm is primary** since that is what the data is.

## 5. Pre-committed outcome statements

- **AV1 — `range_pc1` below the null p95.** The common-factor structure is stationary at this resolution.
  **The flag is absent.** Report as a fourth flag checked and negative.
- **AV2 — `range_pc1` above the null p95.** The structure is non-stationary. Report as **suggestive and
  uninterpretable as a flag**, per §1, and state that identifying a transition is prerequisite. Do **not**
  report the flag as present.
- **AV3 — calibration shows power below ~50% at the largest ramp tested, or the null range exceeds the
  alternative's.** The statistic cannot answer at this length and item count. Report **"cannot answer"** and
  do not report AV1 or AV2. A negative under a powerless test is not a negative.
- **Unconditional:** the *level* of `pc1_share` is reported descriptively and **no claim of any kind rests
  on it**. If it is high, that is the positive manifold and it is expected.

## 6. Declared limits

Ten self-report items from one participant; PC1 on ten variables in a 246-observation window is estimated
with substantial error; the discretisation attenuation is corrected for by calibration rather than by a
measurement model; one analyst. Freezing the spec fixes the forking-paths problem and nothing else.

## 7. Execution record

**Executed 2026-07-30, after this spec was committed and pushed.** No statistic, window count, threshold or
outcome statement was altered during or after the run.

**Calibration (§4).** The statistic has dynamic range, so §5's AV3 does not apply. Discretised arm, 6
windows: null `range_pc1` median 0.060–0.065, **p95 0.099–0.101**; ramp 0.15 median 0.113; ramp 0.60 median
0.277. Discretisation cut mean `pc1_share` from 0.60 to 0.455, confirming the attenuation §4 anticipated and
justifying its placement in the primary arm.

**Observed.** Ten items, 1,473 complete rows.

| windows | mean pc1 | range_pc1 | null p95 | exceeds |
|---:|---:|---:|---:|:--:|
| 6 | 0.553 | **0.1234** | 0.1012 | yes |
| 12 | 0.554 | **0.1805** | 0.1589 | yes |

**Outcome: AV2.** The common-factor structure is **not stationary**. Per §1 this is **suggestive and may not
be reported as the flag being present**, because no transition has been identified.

**Two things §5 did not anticipate, both recorded rather than acted on.**

1. **The direction is wrong for the flag.** Per-window `pc1_share` at 6 windows: 0.508, 0.559, 0.483, 0.570,
   0.606, 0.593 — the common factor gets **stronger**, and the flag's mechanism is that common factors
   *disappear*. No direction test was frozen, so this is reported descriptively and is not a test result.
2. **The exceedance is marginal** — 22% over threshold at 6 windows, 14% at 12. Two window counts were
   examined, and today's own record is a lesson in what a marginal exceedance can turn out to be.

`mean pc1_share` ≈ 0.553 is the positive manifold. Per §5's unconditional clause, **no claim rests on it.**

Full reading: `anomalous_variance_result_2026-07-30.md`.
