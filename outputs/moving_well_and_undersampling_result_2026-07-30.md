# Moving well, and the narrow-deep well — result

**2026-07-30.** Items 2 and 3 of the priority order set by
`transition_type_assignment_result_2026-07-30.md`. Instrument: `work/drift_landscape_windowed.py`, kept
separate from `drift_landscape.py` so the frozen estimator and its calibration artifacts are untouched.

**Headline: the morning's null survives — no window of any unit shows a second attractor. But it is no
longer blanket. Three of eleven units show a single attractor that MOVES across the series, two of them by
about four local SDs, and the floor-effect explanation for those two is ruled out.**

**Second: the narrow-but-deep hole is substantially closed, and closing it required correcting a claim in
the morning's result document that was simply wrong.**

---

> **RETRACTED 2026-07-30 — `moving_well_retraction_2026-07-30.md`.** The attractor-movement result below is an artifact of response degeneracy: the three units concerned have 67-84% of their observations on a single Likert level (every other unit <= 48%), so the drift-field root flips between the gaps either side of the modal level while the mean stays pinned by the mass. The single-attractor result is unaffected; the movement result is withdrawn.**

---

## 1. Item 3 — the narrow-but-deep well

### 1.1 A correction to `transition_type_assignment_result_2026-07-30.md` §3

That document said:

> In the cubic family used here, separation and barrier depth are tied (b = sep⁴σ²/128), so this generator
> set cannot produce that case.

**That is false.** The formula holds only because the project's generator fixes the drift coefficient at
k = 0.25. With k free,

```
drift  mu(x) = -k (x^3 - a^2 x),  a = sep_sd * sigma / 2
barrier   b  = k a^4 / (2 sigma^2)
relaxation lam = 2 k a^2
```

so separation and depth are independent. The case was always constructible; the claim that it was not came
from generalising one generator's fixed parameter into a property of the family.

### 1.2 The sweep

T = 1476, bw 1.4, 30 reps per cell.

| sep (SD) | k | λ | true b | AR(1) | BC | ≥2 attractors | 1 attractor sitting **at the barrier** |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 0.25 | 0.06 | 0.015 | 0.847 | 0.470 | 0.00 | 0.33 |
| 2 | 1 | 0.25 | 0.061 | 0.755 | 0.489 | 0.00 | 0.50 |
| 2 | 4 | 0.98 | 0.245 | 0.649 | 0.523 | 0.00 | 0.63 |
| 2 | 16 | 3.92 | 0.980 | 0.657 | **0.636** | **0.03** | **0.48** |
| **2** | **49** | 12.0 | **3.00** | 0.848 | 0.814 | **0.83** | 0.00 |
| 2 | 150 | 36.8 | 9.19 | 0.494 | 0.648 | 0.50 | 0.00 |
| 3 | 4 | 2.21 | 1.24 | 0.829 | 0.668 | 0.93 | 0.00 |
| 3 | 16 | 8.82 | 4.96 | 0.953 | 0.890 | 1.00 | — |
| 3 | 49 | 27.0 | 15.2 | **−0.006** | 0.338 | **0.00** | 0.00 |
| 3 | 150 | 82.7 | 46.5 | 0.016 | 0.339 | 0.00 | 0.00 |

**Three findings.**

1. **The hole is largely closed.** A narrow well (2 SD separation) with a real barrier (b = 3.0) is detected
   **83%** of the time at Kossakowski's length. The uncalibrated case is no longer uncalibrated.
2. **The undersampling signature is real and it has a fingerprint.** At b ≈ 1 the marginal is bimodal
   (BC = 0.636 > 0.555) while the drift field finds two attractors only 3% of the time, and **48% of the
   single-attractor findings sit at the true barrier position**. That is the failure mode this item was
   built to look for: sampling slower than the relaxation makes E[Δx | x] collapse toward −x, which has one
   zero, at the barrier.
3. **A new limit, in the other direction.** At b ≳ 15 the second state is *never visited* in 1476
   observations. AR(1) falls to ≈ 0, BC to 0.34, detection to 0. The series is a tight fluctuation inside
   one well and is genuinely indistinguishable from a monostable system. This is not an estimator defect —
   it is the power–dwell squeeze at its extreme, and it means **"no second attractor found" can never
   exclude a sufficiently deep one.** That limit is permanent for any finite series.

### 1.3 Kossakowski does not show the undersampling signature

Bimodality coefficients, all 11 units: 0.098, 0.125, 0.314, 0.366, 0.367, 0.433, 0.436, 0.447, 0.546,
**0.659**, 0.097 (composite).

**Ten of eleven are below the 0.555 threshold.** The exception is `mood_anxious` at 0.659 — and it has
**five response levels over a truncated range (−3 to 1)**, so a discreteness artifact is the more
parsimonious reading than a hidden deep well. It is also the **most static** unit in §2 below
(travel ratio 0.026), which is not what an undersampled bistable system looks like.

So the pair that would indicate undersampling — bimodal marginal with a single-attractor drift field — does
not appear in this data.

---

## 2. Item 2 — does the well move?

### 2.1 A bug found in the calibration, and fixed

The first null used an Euler step at dt = 1. That is valid only while λ ≪ 1; at λ = 1.2 it overshoots and
produces **AR(1) = −0.2**, so it could not be used to build a null matched to a weakly autocorrelated
series. Replaced with the exact Ornstein–Uhlenbeck transition parameterised by φ directly. The first
calibration (λ = 0.06, AR(1) ≈ 0.94) is unaffected and is retained; it simply did not match the data.

### 2.2 Statistic and null

`travel_ratio` = between-window spread of the attractor position ÷ the within-window noise scale, over 6
contiguous windows of ~246 observations. 60 reps per cell, T = 1476.

| travel (local SD) | φ = 0.30 median | φ = 0.45 median | p95 |
|---:|---:|---:|---:|
| **0 (null)** | 0.129 / 0.125 | 0.129 / 0.125 | **0.225** |
| 1 | 0.362 | 0.368 | |
| 2 | 0.693 | 0.665 | |
| 3 | 0.994 | 0.961 | |
| 5 | 1.637 | 1.563 | |

The null is tight and **stable across autocorrelation** (identical at φ = 0.30 and 0.45), which is what
makes the statistic usable here. Operating threshold: **null p95 = 0.225**. Calibration curve: 0.36 ≈ 1 SD,
0.68 ≈ 2, 0.98 ≈ 3, 1.6 ≈ 5.

### 2.3 Kossakowski

| unit | AR(1) | BC | travel_ratio | vs null p95 | implied travel | % at floor |
|---|---:|---:|---:|:--:|---:|---:|
| **mood_lonely** | 0.324 | 0.098 | **1.490** | **6.6×** | ≈ 4.5 SD | 0.2% |
| **mood_guilty** | 0.259 | 0.125 | **1.319** | **5.9×** | ≈ 4 SD | 0.1% |
| **mood_down** | 0.436 | 0.314 | **0.494** | **2.2×** | ≈ 1.4 SD | 0.2% |
| mood_irritat | 0.258 | 0.546 | 0.322 | 1.4× | ≈ 0.9 SD | **29.7%** |
| mood_cheerf | 0.345 | 0.433 | 0.172 | below | — | 0.4% |
| _composite | 0.159 | 0.097 | 0.181 | below | — | — |
| mood_strong | 0.355 | 0.436 | 0.153 | below | — | 0.2% |
| mood_relaxed | 0.265 | 0.367 | 0.110 | below | — | 0.1% |
| mood_satisfi | 0.350 | 0.447 | 0.092 | below | — | 0.5% |
| mood_enthus | 0.336 | 0.366 | 0.082 | below | — | 0.4% |
| mood_anxious | 0.223 | 0.659 | 0.026 | below | — | 0.1% |

**Every unit returned exactly one attractor in every one of its six windows — 66 window-fits, 66 single
attractors.** The morning's result is not an artifact of pooling a non-stationary series into one global
field.

**The competing explanation for the movers was checked and fails.** Floor or ceiling piling would let a
window's attractor be dragged by how many non-extreme responses happened to fall in it. The two large
movers have **0.1–0.3%** of observations at either extreme. The item that *is* floor-heavy is
`mood_irritat` (29.7% at floor) — and its 0.322 is therefore **discounted**, not counted.

**Multiplicity.** Eleven tests at the p95 threshold expect ~0.55 false positives. Four exceed it. The two
large ones exceed by a factor of 6 and correspond to ~4 local SDs of travel; those are not multiplicity
artifacts. `mood_down` at 2.2× is suggestive and no more. `mood_irritat` is discounted on the floor
ground above.

### 2.3a Required qualification — `moving_well_deflation_result_2026-07-30.md`

A deflation check was run afterwards: is this anything more than "the mean moved"? On **every synthetic
generator the fitted attractor and the window mean coincide** (corr 0.97–0.997, statistics equal to within
a few percent), so the drift field buys nothing for this question in simulation. On Kossakowski they
**diverge**: `mood_lonely` 1.490 vs 0.270, `mood_guilty` 1.319 vs 0.247 — the attractor travels ~5× the
mean.

**So the finding is not mean non-stationarity** (which is separately present in 6 units and merely
reproduces Olthof et al. 2020). But the regime in which the two diverge is **not covered by the calibration
set**, so the null quoted in §2.2 was measured where they coincide. The result below must be read as:

> In 3 of 11 units the estimated attractor moves between windows by substantially more than the window mean
> does. This is not explained by movement of the mean, and there is **no calibrated null for the regime in
> which it occurs.**

**The null now exists — `skewed_well_null_result_2026-07-30.md` — and it changes the NAME of this section,
not its survival.** A static well under skew, peakedness matched to the items (Student-t innovations,
ν = 3: AR(1) 0.303, BC 0.133 against the items' 0.32/0.098 and 0.26/0.125) and Likert discretisation gives a
maximum `ratio_attractor` of **0.172** across 32 cells — about an eighth of the observed 1.490 and 1.319. The
deflation fails a second time.

**But "moving well" is the wrong name.** Every *moving* generator returns attractor/mean ≈ **1.0**, because
translating a landscape translates its mode and its mean alike. The data returns **5.3–5.5**: the mode moves
and the centre of mass does not. Read §2.3 as **mode relocation with a stationary mean — a change in the
well's asymmetry, not a displacement of the well.**

### 2.4 A pattern, marked as post-hoc

The three units that move — lonely, guilty, down — are the dysphoric, self-referential items. The six that
are static — relaxed, satisfied, enthusiastic, cheerful, strong, anxious — are mostly the positive ones.

**This grouping was noticed after seeing the result and is not tested.** It is recorded so it can be
pre-registered on another dataset, and it carries no weight here. Per the BXKZ decision §4, nothing
load-bearing may rest on a carving of this kind, and this one does not even have a carving yet.

---

## 3. What this does to the three open shapes

`transition_type_assignment_result_2026-07-30.md` §3 left three shapes compatible with the morning's null.

| Shape | Status now |
|---|---|
| **1. A single well that moves** | **Evidence, in 3 of 11 units, 2 of them strongly.** This is the first of the three to get any. |
| 2. A discrete transition at episode scale | Unchanged and now harder to reach — see `hosenfeld_data_assessment_2026-07-30.md` |
| 3. A narrow-but-deep well | **Largely closed** at b ≈ 3 (83% detection). Permanently open at b ≳ 15, where no finite series can exclude it |

In the theory's vocabulary this is the shape that was described as *the operating point moving without
anything breaking* — but with a qualification that matters: **it is not the whole bundle.** Six units are
static and two move a long way. If this survives replication, whatever is moving is moving in part of the
system, not all of it.

**Still absent, everywhere, at every window and every bandwidth: a second attractor.**

## 4. Limits

- **Markovian.** The proper instrument is Bayesian Langevin estimation (Hessler & Kamps,
  doi:`10.1038/s41467-025-60877-0`). This module is a Markovian reconstruction of the same idea and is not
  a substitute — NBLE's hidden Ornstein–Uhlenbeck process is designed to represent exactly the "slow
  dynamics of an unobserved variable" that a moving well is.

  > **RESOLVED, same day.** The earlier note here said antiCPy "fails to build in this environment." That
  > was a wrong diagnosis: the cause is not the numpy build-time import but that `setup.py` does
  > `import antiCPy`, which runs the whole runtime import chain during metadata generation. Installing the
  > runtime dependencies first and then disabling build isolation works:
  >
  > ```
  > pip install matplotlib emcee tqdm ipyparallel celerite
  > pip install --no-build-isolation antiCPy
  > ```
  >
  > **antiCPy 1.0.0 is now installed and imports.**
  >
  > **RE-RUN DONE — `nble_rerun_result_2026-07-30.md`. It does not change §2.3, because NBLE cannot
  > answer that question.** Checked on the same generators before touching the data: θ₅ = 1.129 vs 1.134
  > and ζ = −0.894 vs −0.914 at travel 0 vs 3 SD (default), and 2.704 vs 2.741 / −1.374 vs −1.337 with the
  > time-scale separation prior enabled. A moving well puts its signal in the **between**-window
  > displacement of the operating point; NBLE fits a stationary model **within** each window, and the fast
  > MAP scan does not store the per-window fixed point. **§2.3 is therefore neither confirmed nor refuted
  > and remains a Markovian measurement.** Note also that θ₅ measured on the real data carries no
  > information about this question in either direction, precisely because it does not separate the two
  > conditions.
- **No measurement-error model.** Likert self-reports carry substantial error, which lowers AR(1) and blurs
  a drift field. Chow et al. (2014), the one regime-switching model in this space that *does* model
  measurement error, remains unobtained — owed since this morning.
- **Six windows.** `lam_trend` (whether the restoring rate declines across windows — the CSD question) was
  computed and is **not reported as a finding**: with 6 points, nothing survives 11-way multiplicity.
- **The null is a moving OU, not a moving double well.** It tests "does a single attractor move," which is
  the question asked, and does not calibrate movement of a two-well landscape.
- One analyst, no independent re-implementation.
