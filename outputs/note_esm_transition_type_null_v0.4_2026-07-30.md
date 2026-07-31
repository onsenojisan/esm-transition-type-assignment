# No alternative stable state at beep scale in one long ESM affect series

**A frozen drift-field transition-type assignment, its measured power, and a retracted positive finding**

Hiroaki Aizawa · [0009-0001-8650-6576](https://orcid.org/0009-0001-8650-6576) · **v0.4**, 2026-07-30

> **v0.4 CORRECTS v0.3 ON ITS MAIN CLAIM.** Work done after the v0.3 deposit shows that a modest
> response-style compression collapses the instrument's power (§4a). v0.3's power figures were measured with
> no such distortion and therefore overstate what the null establishes. Three further catastrophe flags were
> also examined (§5a), and §1's account of the prior-art scan's coverage was **wrong** and is replaced.
>
> **Not peer reviewed.** Published at
> doi:[10.5281/zenodo.21703785](https://doi.org/10.5281/zenodo.21703785) (concept DOI, always the latest
> version); this text is version DOI `10.5281/zenodo.21703786`, v0.3. Code, specifications, calibration
> tables and all result documents: `github.com/onsenojisan/esm-transition-type-assignment`, tagged
> `v0.3-zenodo` at the deposited state, and archived inside the Zenodo record.

---

## Abstract

Whether psychopathology has alternative stable states — two attractors separated by a barrier, so that
decline is a transition rather than a gradient — is usually tested by looking for bimodality in a marginal
distribution, which does not settle it. I make one question from a published clinical transition taxonomy
quantitative, freeze the decision rule and its outcome statements before execution, and apply it to the one
intensive longitudinal mood series in hand that is long enough for nonparametric drift estimation
(n = 1,476 beeps, one participant, ten items and a composite).

**No unit shows more than one stable fixed point**, at either of two bandwidths, under either of two
increment definitions, in a global fit or in any of six contiguous windows (66/66 window fits). The null is
informative rather than indeterminate: at this series length the instrument recovers two attractors in 80%
of synthetic deep-well cases and 92.5–100% of 4–6 SD separations against a 2.5% false-alarm rate. It is
**uninformative in principle, for any finite series**, about barriers deep enough that the second state is
never visited.

**That null is conditional, and v0.4 states the condition.** The power figures above were measured with no
response-style distortion. Under a 20% central-tendency compression — an ordinary property of Likert
self-report — detection of a 6 SD separation falls from **100% to 5%**, while false alarms stay at zero. So
the null is informative about series whose respondent used the scale without substantial compression and
**uninformative about series whose respondent did not**, and which describes this participant is not
established. Relatedly, four of the ten items deliver only **1.4–2.8 effective response levels**, and an item
yielding about two distinguishable values cannot resolve attractors 2 SD apart whatever produced the
concentration.

Three by-products are more transferable than the null. **The generators this project had calibrated on were
themselves in the barrier-free regime** at every separation ever tested. **Detection power and its target
are in tension**: seeing two attractors requires a series many dwell times long, while a deep barrier is
exactly what makes the dwell long (**one generator**, four lengths: T ≳ 20–30 × dwell as a rule of thumb,
not a calibrated relation). And **response degeneracy in Likert ESM
items manufactures spurious attractor movement** — a positive finding reported here survived four calibrated
nulls before being explained by the fact that the three items concerned are 67–84% a single response level.
That finding is retracted in §5, and the retraction is the part of this note most likely to save someone
else time.

---

## 1. What is borrowed, and what is claimed

The four-type classification of transitions — **bifurcation-induced (B), noise-induced (N), rate-induced
(R) tipping, and noise-induced diffusion (N-diffusion)** — and its application to clinical change are
published by **Cui et al. (2025)**, in the Ashwin lineage. They also supply an assignment rule: a
three-question decision tree (their Figure 8). **None of that is claimed here.**

Their rule is semi-qualitative — counterfactual interview questions, or such questions embedded in an ESM
protocol — their demonstrations use simulated series, and the paper states that it was not pre-registered.
The contribution of this note is narrow and stated at that size:

> **a quantitative, frozen-before-execution version of one of their questions, run on observed rather than
> simulated series, with the instrument's power measured.**

**A caution for anyone using their tree.** The openly accessible preprint prints the decision tree's last
two terminals **reversed**. The published correction is authoritative: *yes* → B-tipping, *no* → R-tipping.
I verified this against the preprint figure's own text coordinates and against the erratum. The free copy of
a source being the defective one is worth stating explicitly.

A frozen prior-art scan established the above and one further point: **hysteresis does not occur once in Cui
et al. (2025)**. A direction-dependent threshold — whether the level at which a system leaves a state differs
from the level at which it returns — is therefore orthogonal to their classification rather than contained in
it.

The scan searched **PubMed/MEDLINE, Europe PMC and OpenAlex** (345 unique records) with the mechanism
vocabulary of the classification — *rate-induced*, *noise-induced*, *bifurcation-induced*, *B/N/R-tipping*,
*rate-dependent* — conjoined with transition terms and then with either psychological or within-person terms.
Blocks, screening rule and outcome statements were fixed before execution and are deposited.

**Its coverage limit must be stated, and v0.3 stated it wrongly.** A vocabulary-based scan retrieves work
that uses that vocabulary, and this one would not retrieve the older cusp-catastrophe literature on
bistability in psychology. v0.3 concluded from that that the literature "is not surveyed here". **That was
false about the work itself.** The catastrophe-flag framework is this project's *operating frame* — its
structure gate was built to implement the flag-establishing families, its hysteresis instrument is positioned
as confirming a flag, and its generators are cusp processes. What was missing was not the framework but the
**primary literature defining it**, which had been taken entirely from one secondary source (Helmich et al.,
2024).

The primary source has since been read. Gilmore (1981) distinguishes **eight** flags, of which van der Maas
& Molenaar (1992) are the psychological application rather than the derivation; the secondary source named
three of the eight, all from the diagnostic half. What follows from that for this note is in §5a.

**Which repositions the hysteresis claim.** Hysteresis is absent from Cui et al. (2025) — that stands. But it
is **one of Gilmore's five diagnostic flags**, it is one of the three the secondary source names, and it is
*diagnostic rather than anticipatory*: establishing it would show a system is in transition, not predict one.
It is prescribed work rather than unclaimed ground, and v0.3 implied otherwise.

**One further prior-art observation**, moved here from v0.3's reference list where it read as an editorial
aside: Cui, Hasselman and Lichtwarck-Aschoff carry the 2023 landscape method, the 2020 complexity analysis of
this project's own dataset, and the 2025 typology alike. That is a relevant measure of how much of this
niche one group has covered, and it belongs in a prior-art section rather than a bibliography.

## 2. Method

### 2.1 Instrument

Nonparametric drift and diffusion estimation on a single series: the multivariate kernel estimator as used
by `fitlandr` (Cui, Hasselman & Lichtwarck-Aschoff, 2023), re-implemented in Python. Stable fixed points are
the downward zero-crossings of the estimated drift inside the region where the kernel actually has support;
unstable ones — barriers — are the upward crossings.

Attractors are a property of the drift, not of the histogram. That is the level at which the question should
be asked, and the reason marginal bimodality does not settle it.

### 2.2 The barrier readout

The estimator already returned a diffusion term that nothing read. With it, the potential is
U(x) = −∫μ dx, so U′ = −μ and U″ = −μ′, and for dX = −U′(X)dt + σdW the stationary density is
∝ exp(−2U/σ²). That makes

> **b = 2 ΔU / σ²**

the dimensionless barrier — the logarithm of the Arrhenius factor — where ΔU is the potential difference
from a stable point to its shallowest adjacent barrier and σ² is the estimated diffusion averaged over that
path. Small *b* means noise crosses freely: the system diffuses over the landscape rather than sitting in a
basin and occasionally jumping, which is N-diffusion rather than a discrete transition.

### 2.3 What was frozen

Written before the estimator was run on any observed series, with thresholds set on synthetic generators
only: the decision rule (fewer than two stable points → *no second attractor*; two or more with b < 1.0 →
*N-diffusion*; b ≥ 1.0 → *discrete transition, B or N undetermined*), both bandwidth operating points, the
observation gate (≥ 200), the variable set, four pre-committed outcome statements, and explicit declarations
that B-versus-N, rate-induced tipping and hysteresis were **out of scope** — the first because it has no
referent unless a discrete transition is found, the second because no held dataset contains a driver series,
the third because it needs a decline arm and a recovery arm in one series.

The gate value b ≥ 1.0 was set on the physics rather than on the generator spread: calibration shows the
estimator reads *b* low by roughly 2–3×, so a measured 1.0 corresponds to a true barrier of 2–3, an
Arrhenius factor of 7–20. That bias does not enter the main result: **no barrier was found in the observed
data, so *b* was never computed from it.** It matters for reading §3 and nowhere else.

**A reader should apply a discount here.** The specifications were frozen before execution and say so — but
they were not committed to version control before the runs, and a self-dated file cannot logically exclude
post-hoc revision. **The deposit bounds existence, not order**: the Zenodo record and the `v0.3-zenodo` tag
establish that the specifications existed no later than 2026-07-30 and establish nothing about whether they
preceded the runs. A later specification in this line of work (`anomalous_variance_spec_v1.md`, §5a) *was*
committed and pushed before its code was written, which is the only version of this discipline that produces
evidence rather than a claim.

## 3. Calibration, on synthetic data only

### 3.1 Power

Share of replicates recovering ≥ 2 attractors, primary bandwidth, 30–60 replicates per cell:

| generator | T = 100 | 120 | 150 | 300 | **1476** |
|---|---:|---:|---:|---:|---:|
| bistable, 2 SD separation | .033 | .100 | .067 | .075 | .200 |
| bistable, 3 SD | .100 | .150 | .167 | .350 | .400 |
| bistable, 4 SD | .183 | .133 | .267 | .450 | **.925** |
| bistable, 6 SD | .383 | .550 | .733 | .825 | **1.000** |
| **deep well, real barrier** | .017 | .050 | .067 | .350 | **.800** |
| monostable — false alarm | .067 | .067 | .050 | .050 | **.025** |
| monostable pushed through a saturating transform — false alarm | .000 | .000 | .000 | .000 | **.000** |

The last row is the condition that defeats every marginal-distribution method: a monostable process whose
marginal is bimodal. The drift field never false-alarms on it.

### 3.2 The calibration set was in the wrong regime all along

Measured dimensionless barriers for the generators this project had been calibrating on, at the analysed
series length: **2 SD → 0.008, 3 SD → 0.016, 4 SD → 0.049, 6 SD → 0.626.** Algebraically the true values are
0.015, 0.077, 0.245 and 1.24. **All below 1.**

So "two states" in that generator has always meant two humps in a stationary density crossed every six to
eighteen observations, not two states with rare transitions. A newly added generator with the drift
coefficient freed reaches b = 1.5 (true ≈ 5) and is the only case in the set that is a discrete-transition
system.

### 3.3 A power–dwell squeeze, and a permanent limit

The deep-well generator's measured dwell is 32–79 observations. Its detection rate is 80% at T = 1476
(≈ 20–45 × dwell), 35% at T = 300 (≈ 4–9 ×), and ≤ 7% at T ≤ 150 (≈ 2–5 ×).

> Detecting two attractors requires the system to visit both, so the series must be many dwell times long.
> But a deep barrier — the thing that makes a transition discrete rather than diffusive — is exactly what
> makes the dwell long. **Order of magnitude: T ≳ 20–30 × dwell.**

The ratio is read off **one** generator swept across four lengths, so it is a rule of thumb rather than a
calibrated relation; establishing it would need a sweep over barrier depth as well as length.

This supplies a mechanism for the ~1,500-observation requirement often quoted for this kind of analysis, and
it says the requirement is not a fixed number: it scales with the dwell time of whatever is sought.

At the far end the squeeze becomes absolute. **At b ≳ 15 the second state is never visited in 1,476
observations**: autocorrelation falls to ≈ 0, the marginal becomes unimodal, and detection falls to zero. The
series is a tight fluctuation inside one well and is genuinely indistinguishable from a monostable system.
**"No second attractor found" can never exclude a sufficiently deep one, in any finite series.**

### 3.4 Two negative methodological results

**The Kramers dwell estimate is invalid in this regime and is not used.** It requires b ≫ 1; at b ≈ 0.01 the
exponential factor is ≈ 1 and the estimate collapses to a prefactor measuring landscape flatness. It
overstates true dwell by 5–10× in the shallow regime and returns 30–480 observations for monostable series
where the quantity has no referent. It is written to a column named `INVALID` and replaced by a model-free
run length.

**An undersampling fingerprint exists and is diagnosable.** When sampling is slower than the system's
relaxation, E[Δx | x] collapses toward −x, which has a single zero — at the barrier. At b ≈ 1 the marginal is
bimodal while two attractors are recovered in only 3% of replicates, and **48% of the single-attractor
findings sit at the true barrier position.** The pair to look for is therefore *bimodal marginal with a
single-attractor drift field*. (It is not unique to undersampling: a monostable process pushed through a
saturating transform produces the same pair.)

## 4. Result

Only one held series passed the frozen observation gate (the others are treated in §6). It comprises ten
mood items and a composite, 1,473–1,476 observations each, from one participant in an antidepressant
discontinuation study.

**Every unit returned exactly one stable fixed point and no barrier** — at both bandwidths, under both
increment definitions (all consecutive pairs; pairs restricted to within one study day), and in every one of
six contiguous windows: **66 window fits, 66 single attractors.** Median model-free run length: 3
observations. The local stationary spread of the single well accounts for 38–100% of the spread of the
series.

The pre-committed outcome for this pattern was recorded before the run and applies: these are
perturbation-and-relaxation series with no alternative state to transition to.

**What is and is not excluded.** Power at this length is 80–100% against well-separated bistability with a
real barrier, so that is excluded. Power is only 20% against 2 SD separation — but a 2 SD well in this
family has b ≈ 0.008, which is barrier-free by the frozen definition and therefore not a discrete transition
either. What is *not* excluded, and cannot be, is a barrier deep enough that no transition occurs within the
series (§3.3). Ten of the eleven units have bimodality coefficients below the conventional threshold, so the
undersampling fingerprint of §3.4 is absent; the single exception has five response levels over a truncated
range and is the most static unit in the windowed analysis, which is not what an undersampled bistable
system looks like.

**The sampling design, stated because "beep scale" needs an operational definition.** The series carries a
median of **6 observations per day** (mean 6.2, range 1–10), scheduled between 07:00 and 22:00, across a span
of **366 days** — roughly 2.5-hour spacing during waking hours, for about a year. Restricting increments to
within-day pairs, which removes the night gaps, changed nothing.

**What that bounds, and what it does not.** The *span* is a year, so a transition unfolding over weeks or
months is not outside the observation window. What the increments characterise is the drift field, and a slow
transition would appear as **non-stationarity of that field** rather than as two attractors in a pooled fit.
Six contiguous windows of about 40 days each were fitted for exactly that reason, and each returned one
attractor. A transition slower than a window would instead displace the attractor *between* windows — and the
statistic built to detect that is the one retracted in §5. **So the months-scale question is open rather than
answered**, and the range between hours and clinical episodes is the least examined part of this analysis.

## 4a. The correction v0.4 exists for: the null is conditional on response style

v0.3 named response style as "the largest unaddressed threat" (§7) and separately claimed that response
degeneracy cannot manufacture a second attractor (§5). **Nothing bridged them**, and the unexamined direction
is the one that bites: a response style that flattens the drift field can **erase** a shallow second
attractor. That is a false-negative mechanism acting on the result in §4.

It was tested after the v0.3 deposit. Central-tendency compression — the respondent avoids the ends —
applied as `z_reported = c · z` and binned onto a **fixed-anchor** 7-level scale:

| generator | c = 1.0 | **0.8** | 0.6 | 0.5 |
|---|---:|---:|---:|---:|
| **bistable 6 SD** | **1.00** | **0.05** | 0.00 | 0.00 |
| deep well 6 SD | 0.68 | 0.47 | 0.15 | **0.00** |
| monostable — false alarm | 0.00 | 0.00 | 0.00 | 0.00 |
| polarized — false alarm | 0.00 | 0.00 | 0.00 | 0.00 |

**A 20% compression is enough** to take a well-separated bistable system from certain detection to 5%. False
alarms stay at zero throughout, so **compression is a pure false-negative mechanism** — it destroys real
attractors and never creates spurious ones.

**The corrected claim, replacing §4's:**

> No second attractor was found. The instrument has 80–100% power against well-separated bistability **in
> the absence of response-style compression**, and that power collapses under a 20% central-tendency
> compression, to 5% for a 6 SD separation. The null is therefore informative about series whose respondent
> used the scale without substantial compression and **uninformative about series whose respondent did
> not.** Which of those describes this participant is not established.

**A discretisation convention is doing work that v0.3 did not flag as a choice.** The `c = 1.0` baselines
above differ from §3.1 because §3.1 discretises onto the *observed range* while this table uses a *fixed
±3 SD* grid; on a fixed grid the 4 SD wells fall in adjacent bins and are unresolvable before any
compression. Within-row decline is the compression effect and the convention cancels; the level differences
are the convention. Neither convention is obviously right — a real item has fixed anchors, but these items
use 6–7 of their levels — and **v0.3 reported one of them without saying it was a choice.**

## 4b. Effective response levels — and why the mechanism does not need settling

Three candidate mechanisms for the concentration in the four negative-affect items were tested after the
deposit and **none was established**. The codebook refutes a floor reading: on these items **−3 is labelled
"not at all"**, so 0 is the middle of an intensity scale, not a neutral midpoint — and the absence anchor is
used in 0.2% of observations while the midpoint takes 83.6%. An instrument-default reading is refuted by
response times: all-midpoint beeps are faster, but by **86 s against 94 s** on a 90-second questionnaire
(p = 2×10⁻⁶, ρ = −0.14) — significant, and an order of magnitude too small for non-response. A model
comparison failed outright: both simulated mechanisms put 8–100% of mass at the scale ends where the data
has 0.1–0.5%.

**What the attempt produced instead is mechanism-agnostic and settles the practical question.** Effective
levels used, exp(entropy of the level distribution):

| item | scale levels | **effective levels** |
|---|---:|---:|
| mood_anxious | 5 | **1.39** |
| mood_lonely | 7 | **1.86** |
| mood_guilty | 6 | **1.90** |
| mood_down | 7 | **2.75** |
| positive-affect items | 6–7 | 3.03–3.87 |
| mood_irritat | 7 | 4.24 |

> **Whatever produced it, an item yielding about two distinguishable values cannot resolve two attractors
> separated by 2 SD.** The mechanism question is unresolved; the measurement question is not.

**Recommendation for anyone estimating drift fields from Likert ESM: report effective levels per item, and
treat items below about three as unable to support the estimate regardless of why.** Note that `mood_irritat`
— discounted in the retracted analysis for its 29.7% floor pile — is the **best-resolved** item in the set
and the only one whose concentration has the shape of a genuine floor.

## 5. A retracted positive finding, and the failure mode it exposed

A secondary statistic — between-window displacement of the fitted attractor, normalised by the within-window
noise scale — exceeded its calibrated null (p95 = 0.225) in three of eleven units: 1.490, 1.319 and 0.494.
Floor and ceiling effects were checked and ruled out (0.1–0.3% of observations at either extreme in the two
large cases).

**Four calibrated nulls then failed to reproduce it**, each by a factor of six to ten:

1. movement of the plain window mean — the two statistics coincide on every synthetic generator (correlation
   0.97–0.997) but diverge fivefold in the data;
2. static skew with Likert discretisation — maximum 0.172;
3. static heavy tails matched to the items' own autocorrelation and bimodality coefficient — maximum 0.157;
4. time-varying asymmetry at a fixed mean — maximum 0.238.

A further constraint sharpened the puzzle: a well that *translates* carries its mean with it, so every moving
generator returns an attractor-to-mean ratio ≈ 1.0, while the data returned 5.3–5.5. The observation appeared
anomalous with respect to every model available.

**It was not.** The three units are exactly the three with **67–84% of their observations on a single Likert
level**; the highest modal share among the remaining units is 48%. With ~85% of a series on one value the
drift field has almost no support: its zero-crossing flips between the gaps either side of the modal level
according to a handful of minority responses, while the mean cannot move because the mass is pinned. That is
the whole of the ratio. One window returned a local standard deviation **56.7× the series SD** — a λ ≈ 0
failed fit that the code accepted and passed downstream.

No generator reproduced it because **none of them concentrated mass on a single point**; the discretisation
step spreads mass across the range, which is the opposite of what the items do.

**The lesson generalises past this dataset.** A run of failed nulls is evidence about the generator family,
not about the world. The cheapest diagnostic — value counts per window — was the last one tried.

**Two guards now in the estimator**, neither of which existed before: modal share is computed and returned,
flagged as degenerate support above 0.60; and wells whose local SD exceeds 3× the series SD are rejected as
failed fits rather than reported as flat wells. A support bound on the *grid region* existed; nothing bounded
the *degeneracy of the responses* feeding it.

> **Recommendation for drift-field and landscape estimation on Likert ESM items: report the modal share of
> every series analysed, and treat it as a screening variable rather than a footnote.** Symptom items are
> routinely degenerate — most respondents answer "not at all" to most items most of the time.

**What the retraction does not touch.** Response degeneracy cannot manufacture a *second* attractor; it
destabilises the position of the one that is found. The 11/11 and 66/66 single-attractor results stand.

## 5a. Three more catastrophe flags, and where that leaves the project

Reading the primary source (§1) made the flag set explicit: **eight**, split into five that are *diagnostic*
of being in transition and occur together inside the bifurcation set, and three that can appear outside it
and are therefore the only **anticipatory** ones. Two of the eight had never been examined here. Both were,
after the deposit.

**Inaccessibility — negative, with power.** The flag is a region the system does not occupy, which is
strictly stronger than bimodality and had never been asked of this series. Operationalised for Likert data as
a support question: two or more disjoint groups of occupied response levels. Calibrated first — at a strict
support threshold the test has *no* power at this length, and at a 1% threshold it reaches **93% on a genuine
deep well against 0% on all six other generators**, including the polarized case that defeats marginal
methods. Observed: **all ten items, one occupied group, every threshold.** Absent.

That the test is *better* than the attractor count against a real barrier (93% vs 80%) and far cheaper makes
this a second line of the same answer that fails differently — the attractor test reads dynamics and can be
defeated by undersampling; this reads support and cannot. (Its power is convention-dependent in the sense of
§4a: on a fixed-anchor grid it falls to 0.10.)

**Anomalous variance — non-stationary, but in the wrong direction.** Gilmore's first consequence is
multivariate: near a catastrophe, *common factors disappear*. Run under a specification **committed and
pushed before the code was written**. Calibration confirmed the statistic has dynamic range. Observed: the
range of the ten-item first-eigenvalue share across windows is **0.1234 against a null p95 of 0.1012** at six
windows, and 0.1805 against 0.1589 at twelve. The structure is **not stationary** — but the flag is
anticipatory and no transition has been identified, so per the frozen specification this is **suggestive and
may not be reported as the flag being present**. Two things the specification did not anticipate, recorded
rather than acted on: the direction is **wrong** (the common factor gets *stronger*, 0.508 → 0.593), and the
exceedance is marginal (22% and 14% over threshold).

**The scoreboard.**

| flag | | status here |
|---|---|---|
| bimodality | diagnostic | tested, negative |
| inaccessibility | diagnostic | **tested, negative** |
| sudden jumps | diagnostic | partially covered by others on this series |
| hysteresis | diagnostic | **frozen, un-run** — needs two arms |
| divergence | diagnostic | needs manipulated conditions; unavailable |
| divergence of linear response | **anticipatory** | needs perturbations; **structurally unavailable** |
| critical slowing down | **anticipatory** | done, and under published critique |
| anomalous variance | **anticipatory** | **tested; non-stationary, wrong direction, unreadable as a flag** |

> **All three anticipatory flags are now accounted for, and none of them supports anticipation here**: one is
> unavailable to observational data by construction, one is contested, and the third moves in the direction
> opposite to its own mechanism. What remains is a diagnostic flag, hysteresis, which needs data that does
> not exist.

## 6. Two datasets that could not serve, and why

**Three multi-person ESM datasets are too short — and not because the gate was strict.** Their longest
series are 151, 119 and 63 observations. A short-length calibration run *before* any decision about
relaxing the gate shows that at T = 100–150 the deep-well generator is detected in 1.7–6.7% of replicates
while the monostable null false-alarms at 5.0–6.7%. **Power is at or below the false-alarm rate**, and the
barrier index misorders there. No relaxed gate was written.

The consequence is that the natural next claim — that a transition *type* assignment agrees across
individuals — is **untested rather than unsupported**. It needs many series; exactly one is long enough.

**Hosenfeld et al. (2015) cannot carry this analysis either.** Their abstract reports the nine DSM-IV
symptoms of depression recorded weekly for two years in 178 primary-care patients, with high bimodality
coefficients in 66% of the sample and a two-state hidden Markov model outperforming a one-state model in
90% of symptom distributions. Their Methods report that the symptoms were recorded **retrospectively for
every week in the preceding three months**, at three-monthly interviews; the 178 are those with complete
records over 104 weeks out of 267 participants, and the 104-week cut-off was chosen after inspecting the
distributions. The weekly
resolution is a recall resolution, not a sampling one. Drift, diffusion and dwell are all functions of the
increment structure, and in a retrospectively reconstructed series adjacent weekly cells are not adjacent
measurements. Blocked, step-like reconstruction is a well-known property of multi-week recall — which means
the two-state appearance that makes such data attractive is what the measurement method is most likely to
manufacture.

Both halves hold together without hedging, because the distinction is one of **scope of inference**, not of
quality. Their question was whether symptom *courses* look two-state, and their instruments are correctly
applied to what was recorded — recalled course. The inference this note would need is about *dynamics*, and
for that the series cannot serve, because adjacent weekly cells are not adjacent measurements. The two-state
appearance is therefore strong evidence about recalled course and weak evidence about dynamics. That is a
statement about what a design can support, not a doubt about what was reported.

## 7. Limits

- **Markovian, and the non-Markovian check is weaker than it sounds.** The estimator assumes drift depends
  on the current state only, so it cannot see hysteresis. A re-run using Bayesian Langevin estimation
  (Hessler & Kamps, 2025) leaves the result unchanged — but it **cannot corroborate it either**, and the
  reason should not be glossed. On the same synthetic generators, at 0 versus 3 SD of well travel, its
  reported outputs are effectively identical: hidden Ornstein–Uhlenbeck parameter 1.129 vs 1.134 and drift
  slope −0.894 vs −0.914 in the default configuration; 2.704 vs 2.741 and −1.374 vs −1.337 with the
  time-scale separation prior enabled. It fits a stationary model *within* each window, so between-window
  displacement is invisible to it by construction. **This still rests on two corners**: intermediate travels
  of 1 and 2 SD have not been run, so "cannot separate" is asserted from the endpoints rather than from a
  flat response curve. Outstanding. What it does establish is that a correlated-noise
  component is present in all eleven series on a short timescale — so the Markov assumption is not exactly
  satisfied — and, by the same token, that its own parameters carry no information about slow hidden
  structure in either direction.
- **Response style is a plausible systematic distortion, not merely added noise.** §5 shows what happens when
  mass concentrates on one response level. The same logic extends to response styles that are not degenerate
  but are structured — central-tendency bias, extreme-response avoidance, uneven use of the scale's ends.
  Those would not simply blur a drift field; they would **reshape** it, flattening the estimated restoring
  force across values a respondent avoids and steepening it where answers cluster. Nothing here separates
  that from dynamics, and no measurement-error model is fitted. **This is the largest unaddressed threat to
  the interpretation of any drift field estimated from Likert self-reports, including the ones above.**
- **Stationary field.** A single global field is a summary. Published work reports non-stationarity in this
  very series; the windowed analysis is the partial control, and it returns the same answer.
- **Equal spacing.** ESM has night gaps; restricting increments to within-day pairs changed nothing here.
- **No measurement-error model.** Likert self-reports carry substantial error, which lowers autocorrelation
  and blurs a drift field.
- **b is biased low** by kernel smoothing, by a factor of about 2–3 measured against the generators. It does
  not enter the main result: no barrier was found, so *b* was never computed from the data, and the decision
  rule short-circuits before the *b* gate.
- **Discretisation convention.** Every power figure depends on whether the synthetic series are binned onto
  the observed range or onto a fixed-anchor scale (§4a). The two are not interchangeable and neither is
  obviously correct for a real item.
- **Effective response levels.** Four of the ten items carry 1.4–2.8 distinguishable values (§4b). No
  measurement model corrects for this; it is reported so a reader can discount the per-item results
  accordingly.
- **N = 1 for the main result**, one analyst, no independent re-implementation.
- **Provenance.** The two specifications were frozen before the runs they govern, and say so. They were
  **not committed to version control before execution**, so the ordering is documented in the files rather
  than independently timestamped. That is a real weakness of this particular record. Subsequent frozen
  specifications in this line of work are committed before they are run.

## 8. Data and code availability

No participant data is redistributed. Four open ESM datasets are held, obtained via **openESM**
(openesmdata.org; Siepe et al., 2025) and named by their openESM identifiers, each cited by the publication
openESM's metadata designates — which is not always the identifier's name-bearing author:

| held series | citation | persons | longest series |
|---|---|---:|---:|
| Kossakowski | Kossakowski et al. (2017) | 1 | **1,476** |
| `0033_fisher` | Fisher et al. (2017) — Zenodo 10.5281/zenodo.17348038, CC BY-NC 4.0 | 40 | 151 |
| `0010_geschwind` | Bringmann et al. (2013) | 130 | 119 |
| `0052_marian` | Marian et al. (2023) | 145 | 63 |

**Only the first passed the observation gate**; the rest are the subject of §6. Derived summary statistics —
attractor counts and positions, barrier ratios, per-window estimates and every calibration table — are
deposited with the code and remain subject to the source datasets' own terms.

All specifications, calibration tables, result documents (including the retraction) and analysis code:
`github.com/onsenojisan/esm-transition-type-assignment`. Code is MIT; documents and derived tables are
CC BY 4.0.

The hysteresis question named in §1 is separately pre-registered, frozen and **un-run** for want of a
dataset containing both a decline and a recovery arm in one series:
doi:10.5281/zenodo.21366131 (concept DOI, resolving to the current frozen version).

> **What v0.3 got wrong here.** The files deposited at `10.5281/zenodo.21703786` cite
> `10.5281/zenodo.21366132`, the **version** DOI for the preregistration's v0.1 of 2026-07-04. A v0.2
> carrying Amendment 1 was deposited the same day as `21694817`, and the amendment is not cosmetic for a note
> about a null: it routes a CSD failure to INCONCLUSIVE rather than to a negative result. Zenodo does not
> permit file changes after publication, so v0.3's files retain the stale identifier permanently. **v0.4 is
> the correction**, and it is one of the reasons this version exists.

## References

- Ashwin, P., Perryman, C., & Wieczorek, S. (2017). Parameter shifts for nonautonomous systems in low
  dimension: bifurcation- and rate-induced tipping. *Nonlinearity*.
- Bringmann, L. F., Vissers, N., Wichers, M., Geschwind, N., Kuppens, P., Peeters, F., Borsboom, D., &
  Tuerlinckx, F. (2013). A network approach to psychopathology: New insights into clinical longitudinal
  data. *PLoS ONE, 8*(4), e60188. https://doi.org/10.1371/journal.pone.0060188
- Cui, J., Hasselman, F., & Lichtwarck-Aschoff, A. (2023). Unlocking nonlinear dynamics and multistability
  from intensive longitudinal data: A novel method. *Psychological Methods.*
  https://doi.org/10.1037/met0000623
- Cui, J., Hasselman, F., Olthof, M., & Lichtwarck-Aschoff, A. (2025). Understanding types of transitions in
  clinical change: An introduction from the complex dynamic systems perspective. *Journal of Psychopathology
  and Clinical Science, 134*(4), 469–482. https://doi.org/10.1037/abn0000991
  — **and the correction:** https://doi.org/10.1037/abn0001061
- Fisher, A. J., Reeves, J. W., Lawyer, G., Medaglia, J. D., & Rubel, J. A. (2017). Exploring the
  idiographic dynamics of mood and anxiety via network analysis. *Journal of Abnormal Psychology, 126*(8),
  1044. https://doi.org/10.1037/abn0000311
- Hessler, M., & Kamps, O. (2025). Quantifying local stability and noise levels from time series in the US
  Western Interconnection blackout on 10th August 1996. *Nature Communications.*
  https://doi.org/10.1038/s41467-025-60877-0
- Hosenfeld, B., Bos, E. H., Wardenaar, K. J., Conradi, H. J., van der Maas, H. L. J., Visser, I., & de
  Jonge, P. (2015). Major depressive disorder as a nonlinear dynamic system: bimodality in the frequency
  distribution of depressive symptoms over time. *BMC Psychiatry, 15*, 222.
  https://doi.org/10.1186/s12888-015-0596-5
- Kossakowski, J. J., Groot, P. C., Haslbeck, J. M. B., Borsboom, D., & Wichers, M. (2017). Data from
  'Critical Slowing Down as a Personalized Early Warning Signal for Depression'. *Journal of Open
  Psychology Data, 5*(1). https://doi.org/10.5334/jopd.29
- Marian, S., Costantini, G., Macsinga, I., & Sava, F. A. (2023). The dynamic interplay of anxious and
  depressive symptoms in a sample of undergraduate students. *Journal of Psychopathology and Behavioral
  Assessment, 45*(1), 150–159. https://doi.org/10.1007/s10862-022-10014-8
- Olthof, M., Hasselman, F., & Lichtwarck-Aschoff, A. (2020). Complexity in psychological self-ratings:
  implications for research and practice. *BMC Medicine, 18*, 317.
  https://doi.org/10.1186/s12916-020-01727-2
- Siepe, B. S., Haslbeck, J. M. B., Kloft, M., Büchner, A., Zhang, Y., Fried, E. I., & Heck, D. W. (2025).
  Introducing openESM: A database of openly available experience sampling datasets. *PsyArXiv.*
  https://doi.org/10.31234/osf.io/qfdtb

- Gilmore, R. (1981). *Catastrophe Theory for Scientists and Engineers.* Wiley. — the derivation of the
  eight flags. **Cited but not obtained**; the flag set here is taken from van der Maas & Molenaar's account
  of it, which is itself a secondary reading and is flagged as such.
- Helmich, M. A., et al. (2024). Early warning signals and critical transitions in psychopathology
  — the secondary source through which this project adopted the catastrophe-flag framework, and which names
  three of the eight flags.
- van der Maas, H. L. J., & Molenaar, P. C. M. (1992). Stagewise cognitive development: an application of
  catastrophe theory. *Psychological Review, 99*(3), 395–417.
  https://doi.org/10.1037/0033-295X.99.3.395

*Author lists for Cui et al. (2025) and Olthof et al. (2020) were verified against primary sources — the
accepted manuscript's title page and the Europe PMC record respectively — after two errors were found in an
earlier draft of this list. For van der Maas & Molenaar the author order was taken from PubMed and the
article's running head, because the hosting repository's own cover page reverses it.*
