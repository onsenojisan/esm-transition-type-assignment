# The missing null — and a correction to what the finding is called

**2026-07-30.** Completes the calibration `moving_well_deflation_result_2026-07-30.md` §6 said was required:
a generator in which the drift root and the window mean genuinely diverge, so the Kossakowski observation
has a null.

**Two headlines.**

**1. The static-well null does not reproduce the observation.** Across 32 cells — skew, peakedness matched
to the real items, and Likert discretisation — the largest static `ratio_attractor` is **0.172**. The
observed values are **1.490** and **1.319**. The finding survives a second, harder deflation attempt.

**2. But it is not a moving well, and calling it one was wrong.** A well that genuinely translates moves its
mean just as far as its mode: every moving generator returns attractor/mean ≈ **1.0**. The data returns
**≈ 5.3–5.5**. That combination is produced by nothing in the calibration set, moving or static. The correct
description is a change in the **shape** of the well, not a translation of it.

---

> **RETRACTED 2026-07-30 — `moving_well_retraction_2026-07-30.md`.** The attractor-movement result below is an artifact of response degeneracy: the three units concerned have 67-84% of their observations on a single Likert level (every other unit <= 48%), so the drift-field root flips between the gaps either side of the modal level while the mean stays pinned by the mass. The single-attractor result is unaffected; the movement result is withdrawn.**

---

## 1. Why the drift root and the mean are different quantities

For a 1-D SDE with constant noise the stationary density is p(x) ∝ exp(2∫μ/σ²), so **the zero of the drift
is the MODE** and the window mean estimates the **MEAN**. They coincide only for a symmetric well. This is
why the two statistics track each other perfectly on every symmetric generator and can, in principle, come
apart on a real one.

## 2. First attempt: skew. Reached the wrong distribution.

An AR(1) pushed through g(y) = y + βy² — the family of Cui et al.'s "polarized" condition already in the
codebase. Sweeping β ∈ {0, 0.3, 0.6, 1.0} × {continuous, 7 levels} × travel {0, 3}:

**It moves the bimodality coefficient the wrong way.** BC rose to 0.33–0.62; `mood_lonely` and `mood_guilty`
sit at **0.098 and 0.125**. Skew alone cannot reach the items' distribution, so this sweep does not
constitute a matched null. Static `ratio_attractor` across it: 0.100–0.172.

## 3. Second attempt: peakedness. Matched.

BC ≈ 0.1 requires excess kurtosis around 7. AR(1) with Student-t innovations delivers that and keeps the
process symmetric, isolating peakedness from skew.

| ν | levels | travel | AR(1) | BC | attractor | mean | A/M | share > 0.225 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **3** | — | **0** | **0.303** | **0.133** | **0.157** | 0.080 | 1.97 | 0.13 |
| 3 | — | 3 | 0.606 | 0.179 | 0.975 | 0.940 | 1.04 | 1.00 |
| 3 | 7 | 0 | 0.209 | 0.181 | 0.042 | 0.125 | 0.34 | 0.23 |
| 3 | 7 | 3 | 0.501 | 0.254 | 1.624 | 1.343 | 1.21 | 0.83 |
| **4** | — | **0** | **0.301** | **0.147** | **0.138** | 0.088 | 1.58 | 0.03 |
| 6 | — | 0 | 0.300 | 0.208 | 0.144 | 0.092 | 1.56 | 0.00 |
| 12 | — | 0 | 0.288 | 0.279 | 0.125 | 0.079 | 1.57 | 0.03 |

**ν = 3 continuous matches the target**: AR(1) 0.303 and BC 0.133, against `mood_lonely` (0.324 / 0.098) and
`mood_guilty` (0.259 / 0.125).

## 4. Result: the deflation fails again

**Maximum static `ratio_attractor` over all 32 cells of both sweeps: 0.172.** Observed: **1.490** and
**1.319** — roughly **eight times** anything a static landscape produced, under skew, matched peakedness,
and discretisation.

The old operating gate also survives: the share of static series exceeding 0.225 stays at **0.00–0.23**
across every cell, so the threshold quoted in the morning's run was not made fragile by these mechanisms.

## 5. The correction: it is not a translation

This is the part that changes what may be claimed.

| | attractor / mean ratio |
|---|---:|
| Static generators (all cells) | 0.34 – 1.97 |
| **Moving generators (travel = 3)** | **0.82 – 1.21** |
| **`mood_lonely` / `mood_guilty`** | **5.5 / 5.3** |

**A well that translates carries its mean with it.** Every moving generator returns A/M ≈ 1, because
translating a landscape translates its mode and its mean equally. The data does not do that: the mode moves
and the mean stays.

So the observation is anomalous with respect to *everything* in the calibration set — it is not reproduced
by a static skewed or heavy-tailed well, and it is not reproduced by a moving one either. The magnitude
(1.3–1.5) is in the range a travel of 3–5 local SDs produces; the *pattern* (mean unmoved) is not.

**Restatement, replacing "the well moves":**

> In 3 of 11 units the zero of the estimated restoring force relocates between windows while the
> distribution's centre of mass does not. That is a change in the **shape** of the well — its asymmetry —
> not a displacement of it.

### What this does to the theory-side reading

The correspondence table and the transition-type result described this shape as *the operating point moving
without anything breaking*. **That description is now wrong in a specific way.** The operating point, in the
mean sense, did **not** move. What moved is where the restoring force vanishes.

Whether that is a substantive property of the series or an estimator behaviour in a regime still not
generated is **not settled here**, and the honest status is unchanged from this morning in one respect: the
observation is not explained, and the explanations tried have all failed rather than succeeded.

## 6. The next calibration, now much more specific

A generator with **time-varying asymmetry at a fixed mean** — skew that changes across the series while the
centre of mass is held constant — at T = 1476, AR(1) ≈ 0.3, BC ≈ 0.1. That is the only remaining shape that
would produce mode movement without mean movement, and it is the direct null for the restated finding.

If that generator reproduces the observation under a *static* landscape, the finding is an artifact. If it
requires genuine time-varying skew, the finding is that the series' asymmetry changes — which is a
measurable claim about depression dynamics and a different one from anything the project has made.

## 7. Documents this amends

- `moving_well_and_undersampling_result_2026-07-30.md` §2.3 / §2.3a — the finding stands, the name does not.
- `collapse_typology_correspondence_v0.1.md` §7a and
  `transition_type_assignment_result_2026-07-30.md` §7a — both describe shape 1 as a moving well. The
  evidence supports mode relocation with a stationary mean, which is a narrower and different claim.
