# Moving well — deflation check, and where it leaves the finding

**2026-07-30.** Follow-up to `nble_rerun_result_2026-07-30.md` §4, which named "extract NBLE's per-window
fixed point" as the route to a non-Markovian moving-well test.

**That route does not exist.** antiCPy's `fixed_point_estimate` is defined in source as
`np.mean(self.data_window)` — the window mean, not a root of the fitted drift polynomial. ζ is the drift
slope *evaluated at* that mean. There is nothing to extract.

**But it named the right test.** For a single-attractor system the fitted attractor sits near the local
mean by construction, so the moving-well statistic might restate non-stationarity of the mean — which
Olthof et al. (2020) already reported for this series, and which would make it not a new finding.

**Result: the deflation does not hold. On Kossakowski the fitted attractor moves about five times as far as
the window mean in the two flagged units, while on every synthetic generator the two coincide. The finding
survives — and lands in a regime nothing in the calibration set covers.**

---

> **RETRACTED 2026-07-30 — `moving_well_retraction_2026-07-30.md`.** The attractor-movement result below is an artifact of response degeneracy: the three units concerned have 67-84% of their observations on a single Likert level (every other unit <= 48%), so the drift-field root flips between the gaps either side of the modal level while the mean stays pinned by the mass. The single-attractor result is unaffected; the movement result is withdrawn.**

---

## 1. The two statistics

Same windows, same normaliser (median within-window local SD), 6 windows:

- `ratio_attractor` — between-window spread of the **zero of the estimated drift with negative slope**
- `ratio_mean` — between-window spread of the plain **window mean**

## 2. Synthetic: the drift field adds nothing, exactly as suspected

T = 1476, φ = 0.30, 40 reps.

| travel | attractor med | attractor p95 | mean med | mean p95 | corr(attractor, mean) |
|---:|---:|---:|---:|---:|---:|
| 0 (null) | 0.141 | 0.225 | 0.092 | 0.152 | 0.675 |
| 1 | 0.376 | 0.476 | 0.347 | 0.424 | **0.972** |
| 3 | 0.991 | 1.106 | 1.002 | 1.097 | **0.997** |

**For a single moving OU well the fitted attractor *is* the mean** — correlation 0.97–0.997, and the two
statistics agree to within a few percent. The plain mean is even slightly cleaner (null p95 0.152 versus
0.225). So on anything this project has simulated, the drift field buys nothing for this question.

## 3. Kossakowski: they diverge, and only where the finding was

| unit | ratio_attractor | ratio_mean | difference | corr(attractor, mean) |
|---|---:|---:|---:|---:|
| **mood_lonely** | **1.490** | 0.270 | **+1.220** | 0.953 |
| **mood_guilty** | **1.319** | 0.247 | **+1.072** | 0.866 |
| **mood_down** | 0.494 | 0.218 | +0.276 | 0.746 |
| mood_irritat | 0.322 | 0.264 | +0.058 | 0.949 |
| _composite | 0.181 | 0.234 | −0.053 | 0.961 |
| mood_cheerf | 0.172 | 0.061 | +0.111 | −0.222 |
| mood_strong | 0.153 | 0.071 | +0.082 | 0.420 |
| mood_relaxed | 0.110 | 0.115 | −0.005 | 0.361 |
| mood_satisfi | 0.092 | 0.115 | −0.023 | 0.953 |
| mood_enthus | 0.082 | 0.047 | +0.035 | 0.740 |
| **mood_anxious** | 0.026 | **0.255** | **−0.230** | 0.432 |

**The deflation fails.** In the two units flagged this morning the attractor travels ~5× further than the
mean. That is the opposite of what the test was looking for.

**Two things are separable now, and only one of them is new:**

- **Mean non-stationarity**, in 6 of 11 units against the mean-statistic null p95 of 0.152 (lonely 0.270,
  irritat 0.264, anxious 0.255, guilty 0.247, composite 0.234, down 0.218). **This reproduces Olthof et al.
  (2020) on this series and is not new.**
- **Attractor movement beyond mean movement**, in 3 units (lonely +1.22, guilty +1.07, down +0.28). **This
  is not explained by the mean moving**, and it is what this morning's result actually measured.

## 4. Why this is not a promotion of the finding

The two statistics correlate at 0.87–0.95 in the flagged units — they move **together**, with the attractor
amplifying by roughly 5×. That is not the signature of independent estimation noise, which would decorrelate
them. It is consistent with a shallow or asymmetric well, where the zero of a nearly flat drift moves much
further than the data's centre for the same underlying shift; root sensitivity goes as 1/|slope|.

**But no generator in the calibration set produces that regime.** Every synthetic case has attractor ≈ mean
(corr ≥ 0.97). The calibrated null — attractor p95 = 0.225 at travel 0 — was measured where the two
coincide, and says nothing about a regime where they diverge fivefold.

> **Status: the finding survived the deflation test and is now uncalibrated.** Not "confirmed" — there is
> no null for what it is doing. It is *not* mean movement, and that is all that has been established.

## 5. mood_anxious, a fourth time

`ratio_attractor` 0.026 with `ratio_mean` 0.255 — the mean moves and the attractor does not, the reverse of
the flagged units. This unit has now come out anomalous in four separate analyses (five response levels over
a truncated range; the only BC above 0.555; the most static attractor; a positive ζ under NBLE). Treating it
as measurement-scale-driven rather than substantive is now the reading with four independent supports.

## 6. What the next calibration has to be

A generator in which **the attractor and the mean genuinely diverge** — a skewed or asymmetric well, or a
shallow one where root position is sensitive — run at Kossakowski's length and autocorrelation. Only that
gives a null for the quantity actually being reported.

Until it exists, the correct statement of the moving-well result is:

> In 3 of 11 units the estimated attractor position moves between windows by substantially more than the
> window mean does. This is not explained by non-stationarity of the mean, and there is currently no
> calibrated null for the regime in which it occurs.

`moving_well_and_undersampling_result_2026-07-30.md` §2.3 must be read with that sentence attached.
