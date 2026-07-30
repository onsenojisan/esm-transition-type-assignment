# Transition-type assignment — result

**2026-07-30.** Run under `transition_type_assignment_spec_v1.md`, frozen before execution. No threshold,
gate, variable set or outcome statement was altered during or after the run.

**Headline: outcome A3. On the only series long enough to analyse, all 11 units returned a single attractor
and no barrier — no alternative state to transition to. And the instrument had 80% power against a genuine
deep-well bistable system at that length, so this is a result rather than a shrug.**

**Second finding, from calibration rather than data: the assignment cannot be run on any of the project's
multi-person datasets, and not because a gate excluded them. At their lengths the estimator's power against
a real discrete transition is *below* its own false-alarm rate.**

---

## 1. What ran

| Dataset | People | Items | Max observations | Passed the ≥200 gate |
|---|---:|---:|---:|---:|
| **kossakowski** | 1 | 10 | 1,476 | **1 person, 11 units** (10 items + composite) |
| fisher | 40 | 13 | 151 | 0 |
| geschwind | 130 | 6 | 119 | 0 |
| marian | 145 | 9 | 63 | 0 |

Output: `drift_landscape_result_2026-07-30.csv`. Calibration:
`drift_landscape_selftest_v2_2026-07-30.csv` (T = 300, 1476) and
`drift_landscape_selftest_shortT_2026-07-30.csv` (T = 100, 120, 150).

## 2. Q1 on Kossakowski — A3, unanimously

bw 1.4 primary, all consecutive pairs:

| unit | n | attractors | barriers | local_sd / series_sd | run length (obs) | Q1 |
|---|---:|---:|---:|---:|---:|---|
| mood_relaxed | 1476 | 1 | 0 | 0.65 | 2.9 | no-second-attractor |
| mood_down | 1474 | 1 | 0 | 0.64 | 4.9 | no-second-attractor |
| mood_irritat | 1473 | 1 | 0 | 0.71 | 2.7 | no-second-attractor |
| mood_satisfi | 1473 | 1 | 0 | 0.59 | 2.7 | no-second-attractor |
| mood_lonely | 1474 | 1 | 0 | 0.68 | 7.8 | no-second-attractor |
| mood_anxious | 1473 | 1 | 0 | 0.38 | 8.1 | no-second-attractor |
| mood_enthus | 1473 | 1 | 0 | 0.89 | 3.0 | no-second-attractor |
| mood_cheerf | 1473 | 1 | 0 | 0.70 | 3.0 | no-second-attractor |
| mood_guilty | 1473 | 1 | 0 | 1.00 | 8.1 | no-second-attractor |
| mood_strong | 1473 | 1 | 0 | 0.98 | 3.4 | no-second-attractor |
| _composite | 1476 | 1 | 0 | 0.92 | 2.4 | no-second-attractor |

Identical at the sensitivity bandwidth (1.0), and identical restricted to within-day increments — 11/11 in
all four cells. **The barrier index never had anything to measure**, because a barrier requires two
attractors and there were none.

`local_sd / series_sd` ≈ 0.4–1.0 says the single well's own stationary spread accounts for most or all of
the spread of the series. There is one basin, and the series is wandering inside it.

## 3. Why this is a result and not an absence of one

`no-second-attractor` is a null, and nulls are usually uninformative about power. Here the power is
measured. At bw 1.4, share of reps recovering ≥2 attractors:

| generator | T=100 | 120 | 150 | 300 | **1476** |
|---|---:|---:|---:|---:|---:|
| bistable 2 SD | .033 | .100 | .067 | .075 | .200 |
| bistable 3 SD | .100 | .150 | .167 | .350 | .400 |
| bistable 4 SD | .183 | .133 | .267 | .450 | **.925** |
| bistable 6 SD | .383 | .550 | .733 | .825 | **1.000** |
| **deep well 6 SD (real barrier)** | .017 | .050 | .067 | .350 | **.800** |
| monostable — false alarm | .067 | .067 | .050 | .050 | **.025** |
| polarized — false alarm | .000 | .000 | .000 | .000 | **.000** |

At T = 1476, which is Kossakowski's length, the instrument recovers two attractors in **100%** of 6 SD
cases, **92.5%** of 4 SD cases and **80%** of genuine deep-well cases, against a **2.5%** false-alarm rate.
**It looked with adequate power and found nothing, eleven times.**

### The one case that is not excluded

Power is only **20%** against 2 SD separation. So weak separation is not ruled out — but a 2 SD well in this
family has a dimensionless barrier of b ≈ 0.008, which *is* N-diffusion by the spec's own definition, not a
discrete transition. So the two branches close:

- **well separated** → the instrument had 80–100% power and saw nothing → excluded
- **weakly separated** → not excluded, but that regime is N-diffusion, not a transition

**The residual gap, stated rather than glossed:** a *narrow but deep* well — small spatial separation with a
steep barrier — is not covered by either branch, and the project has never calibrated against one. In the
cubic family used here, separation and barrier depth are tied (b = sep⁴σ²/128), so this generator set cannot
produce that case. Closing it needs a new generator, and it is the honest next calibration.

> **CORRECTION, same day** — `moving_well_and_undersampling_result_2026-07-30.md` §1.1. **The sentence above
> about the cubic family is wrong.** Separation and depth are tied only because the project's generator fixes
> the drift coefficient at k = 0.25; with k free, b = k·a⁴/(2σ²) and the two are independent. The case was
> always constructible. It has now been built and run: a 2 SD well with b = 3.0 is detected **83%** of the
> time at this length, so **this gap is largely closed**. What replaces it is a limit in the other direction
> — at b ≳ 15 the second state is never visited in 1476 observations, so no finite series can exclude a
> sufficiently deep well. Kossakowski does **not** show the undersampling fingerprint (bimodal marginal with
> a single-attractor field): 10 of 11 units have BC < 0.555.

## 4. Why the multi-person datasets cannot be used — and why the gate is not the reason

The frozen gate was ≥200 observations. Fisher (max 151), Geschwind (max 119) and Marian (max 63) all fail
it. The obvious next move is a v1.1 spec with a 100-point gate: 37 Fisher people and 48 Geschwind people
clear 100 observations, and Cui, Hasselman & Lichtwarck-Aschoff (2023) Appendix C reports that the landscape
holds up on a 100-point window.

**The short-T calibration was run before writing that v1.1, and it forbids it.** At T = 100–150 and bw 1.4,
the deep-well generator — the one case that genuinely *is* a discrete transition — is detected in **1.7% to
6.7%** of reps, while the monostable null false-alarms at **5.0% to 6.7%**.

> **Power is at or below the false-alarm rate. At ESM lengths this instrument cannot distinguish a real
> bistable system from a monostable one, in the direction that matters.**

No bandwidth rescues it: 1.0 raises deep-well detection to 10–17% but raises the monostable false alarm to
23–27%, and 1.8 collapses both. And the barrier index inverts at short T — monostable series at T=120,
bw 1.8 return a median b of 0.542, larger than the deep well's 0.327 at bw 1.4. **The index is not merely
weak there, it is misordered.**

**On the Appendix C point:** their result is that a landscape estimated from a long empirical series survives
subsampling to a 100-point window. That is a robustness claim about a case with signal already established
at full length. It does not license a 100-point gate for *detection* at this project's noise level, and the
calibration above is the direct test.

**So no v1.1 with a 100-point gate is written.** The project's multi-person data is too short for this
question, full stop.

## 5. Restated D1 — not testable on any held data

Per spec §4 guard 2, the transfer test is not run for a dataset with fewer than 5 people past the gate.
Kossakowski is N = 1 and cannot contribute. Fisher, Geschwind and Marian are excluded by §4 and, per §4
above, are excluded on power grounds independent of the gate.

**Restated D1 is therefore untested, not unsupported.** The distinction matters: the earlier reasoning was
that restating D1 as a categorical claim would escape the aggregation objection because categorical
agreement can be tabulated from N=1 fits. That escape is intact in principle. It is unreachable in practice
with data in hand, for the same reason the old D1 was — **there is exactly one series long enough, and a
transfer claim needs many.**

And per `bnr_tipping_prior_art_survey_2026-07-30.md` §2.5 it also needs the variable fixed, because Cui et
al. attach the type to a variable rather than to a person.

## 6. The power–dwell squeeze, which is a design result

The deep-well generator's measured dwell at T=1476 is 32–79 observations. Its detection rate is 80% at
T=1476 (≈ 20–45× dwell), 35% at T=300 (≈ 4–9× dwell), ≤ 7% at T ≤ 150 (≈ 2–5× dwell).

> **Detecting two attractors requires the system to visit both, which requires the series to be many dwell
> times long. But a deep barrier — the thing that makes a transition discrete rather than diffusive — is
> exactly what makes the dwell long. The instrument's power and its target are in tension.**

Order of magnitude: **T ≳ 20–30 × dwell.** This is an independent derivation of the project's existing
~1,500-observation requirement, and it supplies the mechanism the earlier claim did not have. It also says
the requirement is not a fixed number: it scales with the dwell time of whatever is being looked for, so a
slower phenomenon needs a proportionally longer series.

## 7. What this does to the theory layer

**Against D4, by the route pre-committed as A3.** D4's premise is that a decline arm and a recovery arm are
two arms of one transition sharing one parameter set. In these series, at beep scale, with adequate power,
**there is no second state for a transition to go to.** A single-attractor system with a run length of 3
observations has excursions and relaxations, not transitions.

**Per spec §6 this may not be stated as a refutation of D4.** The project has never measured at episode
scale, and Hosenfeld et al. (2015) report two-state structure is common there (66% / 90%, weekly, 104
points, n=178). The beep scale is now measured twice — first by marginal modality, now by drift-field
attractor count — and it answers the same way both times.

**On the correspondence table** (`collapse_typology_correspondence_v0.1.md`): the observed data lands in the
row the table predicted was the null. Repair and near-miss are in-basin patterns and the B/N/R trichotomy
has nothing to assign there. **The table's §3.1 deflation is now empirical, not just structural** — the
mechanism classification does no work on the data the project holds.

**What survives, unchanged:** hysteresis is absent from Cui et al.'s framework, the project's
preregistration is about hysteresis, and it remains un-run for want of a two-arm dataset. Today's work did
not touch it and did not damage it.

## 7a. Follow-up, same day

The three open shapes in §3 and §7 have been worked. See
`moving_well_and_undersampling_result_2026-07-30.md` and `hosenfeld_data_assessment_2026-07-30.md`.

- ~~**Shape 1 (a single well that moves): now has evidence.**~~ **RETRACTED the same day —
  `moving_well_retraction_2026-07-30.md`.** The attractor movement in `mood_lonely`, `mood_guilty` and
  `mood_down` is an artifact of response degeneracy: those are exactly the three units with **67–84% of
  observations on a single Likert level** (every other unit ≤ 48%), so the drift-field root flips between
  the gaps either side of the modal level while the mean stays pinned by the mass. **Shape 1 has no
  evidence. All three open shapes are again without any.**
- **The null itself survives and hardens.** All 66 window-fits (11 units × 6 windows) returned exactly one
  attractor. §2's result is not an artifact of pooling a non-stationary series into one global field.
- **Shape 3 (narrow-deep well): largely closed**, and the §3 claim that made it unreachable was wrong — see
  the correction inserted in §3 above.
- **Shape 2 (episode scale): harder, not easier.** Hosenfeld et al.'s weekly series is a *retrospective*
  reconstruction made at three-monthly interviews, so it cannot carry increment-based estimation. Priority
  item 2 of §5 is withdrawn.

## 8. Limits

Inherited: Markov (so this cannot see hysteresis), stationary field (Olthof et al. report non-stationarity
in this very series, so a single global field is a summary), equal spacing (`within_day` is a partial
control, and it changed nothing here). Added: b is biased low by kernel smoothing, by a factor of about
2–3 measured against the generators; the narrow-deep-well case in §3 is uncalibrated; one analyst, no
independent re-implementation.

**Recorded honestly:** a divide-by-zero warning was emitted by the first execution of this run and traced to
a refactor that computed the crossing interpolation before the branch that guarantees a non-zero
denominator. Fixed. Results are unchanged by construction — both branches require the two drift values to
differ, so the division was finite wherever its result was used, and the warning fired only on the
discarded path.
