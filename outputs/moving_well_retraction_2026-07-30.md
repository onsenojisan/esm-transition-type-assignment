# RETRACTION — the moving-well / mode-relocation finding

**2026-07-30.** Retracts the one positive empirical finding produced today.

> **The result reported in `moving_well_and_undersampling_result_2026-07-30.md` §2.3 — attractor movement in
> `mood_lonely`, `mood_guilty` and `mood_down` — is an artifact of response degeneracy. It is withdrawn.**

Four deflation attempts failed to explain it. The fifth check was to look at the data, and it took one
table.

---

## 1. What the data looks like

Per-window value counts, `mood_lonely` (7 levels, −3…3):

| window | n | mean | attractor | value counts |
|---:|---:|---:|---:|---|
| 0 | 245 | −0.06 | **−0.471** | −1:28 **0:205** 1:11 2:1 |
| 1 | 246 | −0.12 | **−0.486** | −2:4 −1:32 **0:201** 1:7 2:2 |
| 2 | 246 | −0.09 | **−0.486** | −3:1 −1:26 **0:212** 1:6 2:1 |
| 3 | 245 | +0.02 | **+0.420** | −3:1 −1:18 **0:204** 1:18 2:3 3:1 |
| 4 | 246 | +0.09 | **+0.477** | −1:15 **0:198** 1:28 2:5 |
| 5 | 246 | +0.10 | **+0.497** | −3:1 −1:7 **0:212** 1:20 2:3 3:3 |

**83.6% of the series is the single value 0.** The "attractor" does not travel: it **flips between −0.49 and
+0.50** — the gaps either side of the modal level — according to whether the minority responses lean
negative or positive. The mean cannot move because the mass is pinned at 0. That is the whole of the
attractor/mean ratio of 5.5.

`mood_guilty` is the same at 81.7%, and its window 3 returned a **local SD of 56.7× the series SD** with an
attractor at −0.004: a λ ≈ 0 fit, i.e. a failed one, which the code accepted and passed downstream.

## 2. It orders across the whole dataset

| unit | modal share | ratio_attractor | ratio_mean |
|---|---:|---:|---:|
| **mood_lonely** | **0.836** | 1.490 | 0.270 |
| **mood_guilty** | **0.817** | 1.319 | 0.247 |
| **mood_down** | **0.668** | 0.494 | 0.218 |
| mood_irritat | 0.376 | 0.322 | 0.264 |
| _composite | 0.047 | 0.181 | 0.234 |
| mood_cheerf | 0.401 | 0.172 | 0.061 |
| mood_strong | 0.372 | 0.153 | 0.071 |
| mood_relaxed | 0.484 | 0.110 | 0.115 |
| mood_satisfi | 0.405 | 0.092 | 0.115 |
| mood_enthus | 0.397 | 0.082 | 0.047 |
| mood_anxious | 0.909 | 0.026 | 0.255 |

**The three units that "moved" are exactly the three with 67–84% of observations on one level.** The highest
modal share among the remaining units is 0.48.

`mood_anxious` breaks a simple monotone story — 90.9% modal share and the *lowest* movement — which is why
the overall correlation is only 0.56. It is degenerate in the other direction: five levels over a truncated
range with 91% on one of them leaves the field with nothing to move at all. This is that unit's fifth
anomaly today, and the reading "measurement-scale-driven" now has five independent supports.

## 3. Why no generator reproduced it

Four calibrations were run and all failed by factors of 6–10: mean movement, static skew with Likert
discretisation, static heavy tails matched to the items' BC and AR(1), and time-varying asymmetry at a fixed
mean. **None of them had ~85% of its mass on a single value.** The discretisation step spread mass across the
range; the real items concentrate it on one point.

**The failure of four nulls was not evidence for the finding. It was evidence that the generators were the
wrong family** — and it should have prompted looking at the data sooner. The cheapest diagnostic was the
last one tried.

## 4. Guards added to the estimator

`work/drift_landscape.py`, `analyse_1d`:

- **`modal_share`** is computed and returned, with `degenerate_support = modal_share > 0.60`. The threshold
  sits in the gap between the three retracted units (0.67–0.84) and every other unit in the dataset
  (≤ 0.48). It is a floor on support, not a tuned parameter.
- **Wells whose local SD exceeds 3× the series SD have their `local_sd` set to NaN and are flagged
  `degenerate_fit`.** These are λ ≈ 0 failures, not flat wells. Guilty's window 3 would have been caught.

Neither guard existed when the retracted analysis ran. `mass_frac` bounded the *grid region* the field is
read on; nothing bounded the *degeneracy of the responses* feeding it.

## 5. What survives, and what does not

**Withdrawn:**

- Attractor movement in 3 of 11 units (`moving_well_and_undersampling_result_2026-07-30.md` §2.3, §2.3a).
- The restatement as mode relocation with a stationary mean (`skewed_well_null_result_2026-07-30.md` §5).
  Both described an artifact; the second described it more precisely.
- Shape 1 ("a single well that moves") as having evidence — in
  `transition_type_assignment_result_2026-07-30.md` §7a and `collapse_typology_correspondence_v0.1.md` §7a.
  **It has none.** All three open shapes are again without evidence.
- The post-hoc pattern "dysphoric items move, positive items are static". It was already marked as carrying
  no weight; it now has an explanation, and it is the wrong one — those items are simply the ones people
  mostly answer 0 to.

**Unaffected:**

- **11/11 units, and all 66 window-fits, return exactly one attractor.** Degeneracy cannot manufacture a
  *second* attractor; it destabilises the position of the one that is found. The core null is untouched.
- The undersampling calibration and the narrow-deep-well closure (§1 of the same document).
- Mean non-stationarity in 6 of 11 units, which reproduces Olthof et al. (2020) and was never claimed as
  new.
- The NBLE results, which do not use the attractor position at all.
- `hosenfeld_data_assessment_2026-07-30.md` and everything in the prior-art and typology track.

## 6. The honest summary of the day

The project ran a frozen assignment, found no second attractor with adequate power, generated one positive
finding on a secondary statistic, and then spent four calibrations failing to kill it before killing it by
reading the raw counts.

**Net empirical result for 2026-07-30: no second attractor at beep scale, and nothing else.**
