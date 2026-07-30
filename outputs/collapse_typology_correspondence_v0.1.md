# Collapse typology: the correspondence between L4's outcome patterns and the published transition classes — v0.1

**2026-07-30.** Design document. Answers priority item 4 of
`catastrophe_flag_prior_art_survey_2026-07-30.md` ("decide what to do about D1") and specifies what the
project may claim after `bnr_tipping_prior_art_survey_2026-07-30.md` closed the typology and its clinical
application as prior art.

**The proposal being specified:** stop claiming the fold is the universal mechanism of collapse. Claim
instead that the set of collapse mechanisms is a closed classification, that 様式 patterns map onto it, and
that the map is predictable in advance. This document builds the map and prices it.

**The result is deflating in three specific ways, all recorded in §3 and §4. The map is not 4×4. Two of
L4's four cells are dynamically identical, one mechanism class has no L4 partner at all, and only three of
the five distinctions the map needs are measurable with anything the project holds.**

---

## 1. The two lists

### 1.1 Outcome side — the project's own, and it never depended on the fold

From `l4_generic_change_distinction_note_v0.1.md` (2026-06-17), §1:

| Pattern | Minimal definition |
|---|---|
| **Repair** | after worsening, the 様式 restabilises |
| **Sustained non-repair** | after worsening, the non-repaired state persists |
| **Reorganization** | does not return to the original state; stabilises in a *different* 様式 |
| **Near miss** | collapse-like, but repaired |

with six categories the note requires be excluded before any of the above is claimed: spike, volatility,
mean reversion, transient worsening, phase-order, generic change.

**This list contains no reference to the fold, to bifurcation, or to hysteresis.** It was written six weeks
before the fold's universality came under pressure, and it survives that pressure untouched. Promoting it
from a proxy-validation checklist to the theory's classification layer requires no new invention.

### 1.2 Mechanism side — borrowed, and not the project's under any outcome

From Cui et al. (2025), *J Psychopathol Clin Sci* 134(4), 469–482, doi:`10.1037/abn0000991`, in the Ashwin
lineage:

| Class | Mechanism |
|---|---|
| **B-tipping** | bifurcation-induced. The landscape destabilises as a control parameter drifts. **This is the fold.** |
| **N-tipping** | noise-induced. Stability does not change; noise ejects the system into a pre-existing alternative basin. No EWSs exist to be found. |
| **R-tipping** | rate-induced. Depends on how *fast* the driver moves, not on its level. |
| **N-diffusion** | noise-induced diffusion. No single identifiable tipping point; occupancy of the state space changes without a discrete transition. |

Their Figure 8 supplies an assignment rule. **Use the erratum version** (doi:`10.1037/abn0001061`); the
open preprint prints the last two terminals reversed. See the prior-art survey §2.2–2.3.

### 1.3 The axis the mechanism side omits, and which is the project's

**"Hysteresis" does not occur once in Cui et al. (2025).** Their four classes describe *how the system
left*. None of them asks whether the return threshold differs from the departure threshold.

That question — the decline arm and the recovery arm sharing one parameter set, so the recovery threshold
is predictable from decline dynamics — is D4, and it is frozen at `10.5281/zenodo.21366132`.

**So the map is not 4 cells. It is 4 × (hysteresis: yes / no / unobserved), and the second factor is the
project's own.** This is the single structural reason the project still has a position here.

---

## 2. The map

Reading the outcome patterns for their dynamical content rather than their clinical description:

| L4 outcome pattern | Dynamical content | Compatible mechanism classes |
|---|---|---|
| **Repair** | stayed in the basin; relaxed back | **none** — no transition occurred. This is the null. |
| **Near miss** | stayed in the basin; approached its boundary | **none** — but this is B-tipping's precursor regime, and the only regime where EWSs should appear without a transition |
| **Sustained non-repair** | arrived in a different attractor, and it is worse | **B / N / R** |
| **Reorganization** | arrived in a different attractor | **B / N / R** |
| *(L4's excluded categories: volatility, generic change)* | occupancy changed; no discrete transition | **N-diffusion** |

Three things follow immediately, and each is a correction to the proposal rather than a confirmation of it.

---

## 3. Three ways the map is smaller than the proposal assumed

### 3.1 The B/N/R trichotomy does work inside exactly one L4 cell

Repair and near-miss are *non*-transitions: the system never left its basin, so there is no tipping class to
assign. The trichotomy partitions only the cases that arrived somewhere else.

**Consequence:** the mechanism classification is not a classification of 様式 patterns. It is a
sub-classification of one of them. A "unified theory of collapse" built by crossing the two lists would be
a 2-cell null plus a 3-way split of a single cell — which is a much smaller object than the phrase implies,
and it should not be published under that phrase.

### 3.2 Sustained non-repair and reorganization are the same dynamical event

Both are "the system now occupies a different attractor." The L4 note distinguishes them by whether the new
state is worse (非修復) or merely different (別様式で安定). **That distinction is evaluative, not
dynamical.** No drift field, attractor count, or tipping-class assignment can separate them; separating them
requires a valence or viability judgement supplied from outside the dynamics.

**This is a defect in L4's typology, found by building the map, and it is recorded rather than repaired.**
Two honest options:

- **(a)** State that L4 has **three** dynamical cells (in-basin / different-attractor / no-discrete-transition)
  plus an evaluative overlay that marks a different-attractor outcome as non-repair or as reorganization.
  The overlay needs its own independent measure — and an independent viability endpoint is precisely what
  the co-measurement note says no dataset supplies.
- **(b)** Drop the reorganization/non-repair distinction from the measurable layer and keep it only as
  clinical description.

**(a) is the honest option and it is expensive.** It re-imports the co-measurement gap into the typology.

### 3.3 N-diffusion has no L4 outcome partner — it is on L4's exclusion list

L4's cells all presuppose *a disruption followed by an outcome*. N-diffusion has no disruption to follow:
occupancy changes with no identifiable transition. It therefore maps onto what L4 was built to **exclude** —
"volatility", "generic change".

This is the one place the map returns something the project did not have. **L4's "generic change" confound
is not a nuisance category. It is a mechanism class with a name, a landscape interpretation, and an
estimator.** A series that fails L4's Test 1 is not merely uninformative; it is evidence for N-diffusion.

That also cuts the other way, and harder: **most of what the project's own pre-gate has been measuring —
whether the marginal distribution has two modes — is the observable signature of N-diffusion as much as of
bistability.** This is the same finding as Cui, Hasselman & Lichtwarck-Aschoff (2023)'s "bimodality does not
imply bistability", arriving from the other direction.

---

## 4. What is measurable, with what, today

| Distinction the map needs | Instrument | Status |
|---|---|---|
| in-basin vs different attractor | `work/drift_landscape.py` — stable fixed points of the nonparametric drift field | **available.** Selftest: 0% false alarms on both null generators at bw 1.4, T=300 and 1476 |
| discrete transition vs N-diffusion | the **diffusion** term of the same estimator, plus absence of change points | **available but unused.** `analyse_1d()` already returns `diffusion`; nothing reads it. Cheapest open item in the project |
| **B vs N** | whether local stability declines *before* the transition — the drift slope at the occupied fixed point, over moving windows | **partial.** Olthof et al. (2020) report non-stationarity and many change points in the target series, so windowed slopes are noisy. Proper instrument: Bayesian Langevin estimation, doi:`10.1038/s41467-025-60877-0` (non-Markovian, separates drift from noise, demonstrated on real observed data) |
| **R** | the *rate of change of the driver* | **unassignable.** None of the four held ESM datasets contains a driver series. Cui et al.'s own route to R is a counterfactual interview question, i.e. new data collection |
| **hysteresis** (the project's axis) | HysTAR, per the frozen preregistration | **unassignable with data in hand** — needs a decline arm and a recovery arm in one series, which is the un-run test |

**Score: 2 distinctions clean, 1 partial, 2 unassignable.**

So the honest answer to "how many patterns are there?" has three different numbers, and the project should
state all three rather than pick the flattering one:

- **4** in the published classification (+ combinations, which the authors say are the normal case in real
  data)
- **3** dynamically distinguishable with instruments the project holds — in-basin, different-attractor,
  no-discrete-transition
- **6** if a two-arm dataset is ever obtained (3 × hysteresis yes/no)

---

## 5. What the project may claim

Not "崩壊の統一理論". The classification is Cui et al.'s and the Ashwin lineage's; the clinical application
is Cui et al.'s; the assignment rule exists. What is left is real but narrow:

> **A pre-registered quantitative assignment rule that maps observed within-person series onto the
> published transition classification — where the published rule is semi-qualitative, retrospective, and
> demonstrated only on simulated series — extended by the recovery-direction axis the classification omits.**

Three components, in the order they can be built:

1. **Quantitative Figure 8.** Replace the counterfactual interview questions with estimator outputs where
   possible: Q1 (qualitatively different vs more/less often) → attractor count and occupancy change; Q2
   (would the event have done this at another time) → whether local stability declined pre-transition. Q3
   (rate) has no estimator without a driver series and stays qualitative. **Freeze the mapping before
   running it.** Cui et al. state their own paper was not pre-registered; this is the one methodological
   respect in which the project can be straightforwardly stronger than its prior art.
2. **The hysteresis axis.** Already frozen and already un-run. Unchanged by this document except that it is
   now the project's *only* uncontested ground.
3. **Restated D1** — see §6.

## 6. D1, restated, and what the restatement costs

Old D1: one parameter set transfers across cases, frozen. **No instrument can estimate it**, and Cui,
Hasselman & Lichtwarck-Aschoff (2023) argue on principle that the aggregate may not be meaningful.

Restated D1: **the type assignment agrees across individuals above chance.** Categorical agreement is
tabulable from N=1 fits, so fitlandr's N=1-only restriction does not block it.

**The cost, from the prior-art survey §2.5.** Cui et al. attach the transition type to a **variable**, not to
a person, and hold that different variables within one person undergo different types simultaneously.
Therefore:

> Restated D1 is only well-formed if the **variable set is fixed in advance**. "The type agrees across
> people" is not a claim until it says *for which variable*. Without that, the restatement inherits the
> aggregation objection it was meant to escape, and adds variable-shopping on top.

Specified version: *for a pre-registered variable set, the type assigned per variable agrees across
individuals above chance.* That is measurable, and it is a much weaker claim than genericness. It should be
stated as a much weaker claim.

## 7. What falls if this is wrong

Fixed here so it cannot be softened later:

- **If, on observed series, nearly every case is assigned N-diffusion** (no discrete transition), then
  collapse-as-transition is the wrong frame for ESM affect data, and D4's premise falls with it — because
  there is no transition whose two arms could share a parameter set.
- **If type assignment shows no cross-individual agreement above chance** on the pre-registered variable
  set, restated D1 falls, and the project should say plainly that genericness is not measurable in either
  its old or its new form.
- **If sustained non-repair and reorganization cannot be separated by any measurement that is not a valence
  judgement**, then L4's four-cell typology is a three-cell dynamical typology plus an evaluative overlay,
  and it must be published as such — §3.2(a), with the co-measurement gap attached.
- **If a two-arm dataset is obtained and shows no direction-dependent threshold**, the hysteresis axis —
  the project's last uncontested ground — is empty, and what remains is a pre-registered replication of
  someone else's typology.

## 7a. Update — 2026-07-30, later the same day: §7's first condition has now been tested

`transition_type_assignment_result_2026-07-30.md` ran the frozen Q1 assignment. On Kossakowski, 11/11 units
returned **a single attractor and no barrier**, with 80% power against a genuine deep-well bistable
generator at that length. That is not the N-diffusion branch of §7's first bullet — it is one step further
back: **there is no second attractor at all**, so nothing tips and nothing diffuses between basins.

Consequences for this document:

- **§3.1's deflation is now empirical.** The B/N/R trichotomy does no work on the data the project holds,
  because the data lands in the row the table predicted was the null (repair / near-miss, in-basin).
- **Shape 1 was reported as having evidence later the same day, then RETRACTED —
  `moving_well_retraction_2026-07-30.md`.** The attractor movement was an artifact of response degeneracy:
  the three units concerned are exactly the three with **67–84% of observations on a single Likert level**
  (every other unit ≤ 48%), so the drift-field root flips between the gaps either side of the modal level
  while the mean stays pinned by the mass. Four calibrations failed to reproduce it because none of the
  generators concentrated ~85% of their mass on one value. **Shape 1 has no evidence, and neither does any
  other. Nothing in this document about an operating point moving is supported.**
- **§6's restated D1 is untested, not unsupported.** The categorical escape is intact in principle and
  unreachable in practice: one series is long enough and a transfer claim needs many. At the lengths the
  multi-person datasets have, the estimator's power against a real discrete transition is *at or below* its
  false-alarm rate, so the obstacle is not the frozen gate.
- **§7's D4 bullet fires, in the pre-committed form**: at beep scale there is no transition for two arms to
  be arms of. Not a refutation — episode scale has never been measured.
- **§1.3 is untouched.** Hysteresis remains absent from the borrowed classification and remains the
  project's own frozen, un-run question.

## 8. Immediate next steps

1. Read `analyse_1d()`'s existing `diffusion` output. It is already computed and discarded, and it is the
   N-diffusion discriminator. Cheapest item in the project.
2. Run `drift_landscape.py` on Kossakowski — now the first component of a quantitative assignment, not just
   an attractor count.
3. Obtain doi:`10.1038/s41467-025-60877-0` (Bayesian Langevin). It is the B-vs-N discriminator and repairs
   `drift_landscape.py`'s inherited Markov limit.
4. Freeze the quantitative-Figure-8 mapping **before** running it on any observed series.
5. Fix the variable set for restated D1 **before** tabulating any types.

Steps 4 and 5 are the whole methodological contribution. If they are done after seeing results, there is
nothing left here that the prior art does not already own.
