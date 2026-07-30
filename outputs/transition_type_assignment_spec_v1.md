# Transition-type assignment — spec v1.0, FROZEN

**Frozen 2026-07-30, before the estimator was run on any observed series.** Thresholds below were set on
synthetic generators only (`drift_landscape_selftest_v2_2026-07-30.csv`). The observed-data run that this
spec governs had not been executed when this file was written.

## 0. What this is, and what it is not

Cui et al. (2025), *J Psychopathol Clin Sci* 134(4) 469–482, doi:`10.1037/abn0000991`, classify clinical
transitions into **B-tipping / N-tipping / R-tipping / N-diffusion** and give an assignment rule (their
Figure 8 — **use the erratum**, doi:`10.1037/abn0001061`). Their rule is a set of counterfactual interview
questions; their demonstrations use **simulated** series; and the paper states it was **not
pre-registered**.

This spec makes **one** of their questions quantitative, freezes it before running, and declares the rest
out of scope with reasons. **The classification is not the project's** and is not claimed here — see
`bnr_prior_art_search_spec_v1.md` §5 and `bnr_tipping_prior_art_survey_2026-07-30.md`.

## 1. Which questions are in scope

| Cui et al. Figure 8 | Quantitative form | Status |
|---|---|---|
| **Q1** — is the state qualitatively different, or are you just in it more/less often? | Is there a second attractor with a barrier the noise cannot walk over? | **IN SCOPE**, §2 |
| **Q2** — would the event have caused this at another time? (B vs N) | Did local stability decline *before* the transition? | **OUT OF SCOPE**, §5 |
| **Q3** — would it have happened if the factor changed slower? (B vs R) | Rate of change of the driver | **OUT OF SCOPE**, §5 |
| *(absent from their framework)* hysteresis | Direction-dependent threshold across a decline and a recovery arm | **OUT OF SCOPE**, §5 — this is D4, frozen separately at `10.5281/zenodo.21366132` |

Q2 is out of scope for a reason that is logically prior, not merely practical: **Q2 only has a referent if
Q1 says a discrete transition exists.** Q1's answer determines whether Q2 is reachable at all.

## 2. Q1, frozen

Estimator: `work/drift_landscape.py`, the ported Bandi–Moloche multivariate kernel estimator as fitlandr
uses it. Unchanged in this respect from the run that produced
`drift_landscape_selftest_2026-07-30.csv`.

**Quantities.** From the estimated drift, the potential is U(x) = −∫μ dx, so U′ = −μ and U″ = −μ′. For
dX = −U′(X)dt + σdW the stationary density ∝ exp(−2U/σ²), which makes

> **b = 2·ΔU / σ²**

the dimensionless barrier — the log of the Arrhenius factor — where ΔU is the potential difference from a
stable point to its **shallowest adjacent** unstable point (the route the system actually leaves by) and σ²
is the estimated diffusion averaged over that path.

**Decision rule.**

| Condition | Label |
|---|---|
| fewer than 2 stable points, or no barrier found | `no-second-attractor` |
| ≥ 2 stable points and **b < 1.0** | `N-diffusion` |
| ≥ 2 stable points and **b ≥ 1.0** | `discrete-transition(B-or-N)` |

**Operating points.** bw_mult **1.4** primary (0% false alarms on both null generators at both lengths),
**1.0** sensitivity. Anything appearing only at 0.7 is not reported as a finding. Both `within_day=False`
and `True` are run. Observation gate **≥ 200** per series.

**Gate value, and where it came from.** `B_GATE = 1.0`, set on the physics rather than on the generator
spread: selftest shows the estimator reads b **low by roughly 2–3×** (measured 0.63–0.95 where the
generator's true b is 1.24; measured ~1.5 where it is ~5), so a measured 1.0 corresponds to a true barrier
of about 2–3, i.e. an Arrhenius factor of 7–20. A sensitivity gate of **0.3** is also reported; it sits
inside the empty decade between the 4 SD generator (0.049) and the 6 SD generator (0.626) at bw 1.4.

## 3. What the calibration already established, before any observed data

Recorded here because it is a finding in its own right and it constrains what the observed run can mean.

**Every one of the project's own bistable generators sits below b = 1 at every separation it ever
calibrated** (bw 1.4, T=1476): 2 SD → 0.008, 3 SD → 0.016, 4 SD → 0.049, 6 SD → 0.626. Only the newly added
deep-well generator (k=1, sub-stepped) reaches 1.504.

**So the generator on which the structure gate was calibrated is itself in the N-diffusion regime
throughout.** "Two states" in that generator has always meant two humps in a stationary density crossed
every few observations — measured mean run length 6–18 observations — not two states with rare transitions.
This is consistent with, and gives a mechanism for, the 1.92 SD median separation measured in real data and
the pre-gate's power ceiling.

**The Kramers dwell estimate is invalid here and is not used.** It requires b ≫ 1; at b ≈ 0.01 the
exponential factor is ≈ 1 and the estimate collapses to the prefactor, which measures landscape flatness,
not dwell. Selftest shows it overstating the true dwell by 5–10× in the shallow regime, and returning
30–480 observations for monostable series where the quantity has no referent. It is written to the output
column `kramers_log10_dwell_INVALID` and **must not be read as an estimate**. The reported dwell is
`run_length_obs`, the model-free mean run length either side of the barrier.

## 4. Restated D1 — the cross-case transfer test

Old D1 (one parameter set transfers, frozen) has no instrument. Restated D1: **the type assigned per
variable agrees across individuals above chance.**

**Pre-registered variable sets:** the `TARGETS` item lists already in `work/drift_landscape.py`. These were
written for the attractor-count run earlier on 2026-07-30, before the typology question was posed, and were
**not modified** by the edits that added the barrier machinery. They are used as-is; no item is added,
dropped or substituted.

**Test.** Within each dataset, one label per (person, item). Statistic: the mean over items of the modal
label's share. Null: labels permuted across (person, item) pairs within dataset, 2,000 permutations.

**Two guards, frozen now because both failure modes are anticipated:**

1. **If the label distribution is degenerate — one label holds ≥ 95% of series — the transfer test is
   UNDEFINED and is reported as undefined, not as supported.** Perfect agreement produced by a base rate is
   not evidence of transfer. This is the most likely outcome and it must not be able to read as a win.
2. **If fewer than 5 people in a dataset pass the observation gate, the test is not run for that dataset.**
   Kossakowski is N = 1 and therefore cannot contribute to it at all.

## 5. Declared out of scope, with reasons

- **Q2 (B vs N)** needs local stability estimated *before* a transition, i.e. a windowed field. Two
  blockers: it has no referent unless Q1 finds a discrete transition, and Olthof et al. (2020) report
  non-stationarity and many change points in the target series, which makes windowed slopes
  uninterpretable at this length. Route: Bayesian Langevin estimation, doi:`10.1038/s41467-025-60877-0`
  (non-Markovian, separates drift from noise, demonstrated on observed data). **Not run here, and no
  underpowered version is reported.**
- **Q3 (R-tipping)** needs the rate of change of a driver. None of the four held datasets contains a driver
  series. Cui et al.'s own route to R is a counterfactual interview question, i.e. new data collection.
- **Hysteresis** needs a decline arm and a recovery arm in one series. That is the frozen, un-run
  preregistration. Unchanged.

## 6. Pre-committed outcome statements

Fixed before the run so none can be written to fit what comes back.

- **A1 — most series assigned `N-diffusion`.** Report: *at beep scale, in the series the project holds, the
  landscape has no barrier the noise cannot cross, so there is no discrete transition for a decline arm and
  a recovery arm to be arms of.* D4's premise has nothing to attach to **in this data**. It may **not** be
  stated that D4 is refuted: the project has never measured at episode scale, where Hosenfeld et al. (2015)
  report two-state structure is common.
- **A2 — one or more series assigned `discrete-transition`.** Name them, with n, separation, b and run
  length. Q2 becomes reachable for those series and the Bayesian Langevin instrument becomes the next step.
  A single series surviving is reported as a single series, not as support for genericness.
- **A3 — most series assigned `no-second-attractor`.** Report as the monostable reading: these are
  perturbation-and-relaxation series, L4's repair / near-miss territory, with no alternative state to
  transition to. This is *also* incompatible with D4's premise, by a different route than A1.
- **A4 — restated D1.** Report per §4, including the degeneracy guard. If undefined, say undefined.

## 7. Limits this spec does not remove

Inherited from the estimator: Markov (so no hysteresis), stationary field (so a single global field is a
summary), equal spacing (ESM has night gaps; `within_day` is the partial control). Added here: b is biased
low by kernel smoothing; the barrier is read from a smoothed field; one analyst, no independent
re-implementation. Freezing the spec fixes the forking-paths problem and nothing else.

## 8. Execution record

**Executed 2026-07-30, after this spec was written. No threshold, gate, variable set or outcome statement
was altered during or after the run.**

Only **Kossakowski** passed the ≥200-observation gate (1 person, 11 units). Fisher (max 151), Geschwind
(max 119) and Marian (max 63) did not.

**Outcome: A3.** All 11 units returned a single attractor and no barrier, at both bandwidths and both
increment definitions — 11/11 in all four cells. Median run length 3 observations. At T = 1476 and bw 1.4
the instrument's power is 80% against a genuine deep-well bistable generator and 92.5–100% against 4–6 SD
separation, at a 2.5% false-alarm rate, so the null is informative.

**A4 (restated D1): not testable.** §4 guard 2 applies — Kossakowski is N = 1, and no other dataset has a
series past the gate.

**A v1.1 with a 100-point gate was considered and is not written.** A short-T calibration
(`drift_landscape_selftest_shortT_2026-07-30.csv`, run before any decision) shows that at T = 100–150 the
deep-well generator is detected in 1.7–6.7% of reps while the monostable null false-alarms at 5.0–6.7%:
**power at or below the false-alarm rate**, and the barrier index misorders (monostable median b = 0.542 at
T=120/bw 1.8 exceeds the deep well's 0.327 at bw 1.4). Cui et al.'s Appendix C 100-point robustness result
does not transfer to detection at this noise level.

Full reading: `transition_type_assignment_result_2026-07-30.md`.
