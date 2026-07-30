# B/N/R tipping prior-art scan — result

**2026-07-30.** Executed under `bnr_prior_art_search_spec_v1.md`, frozen before the run. No block,
screening rule or outcome statement was altered during or after execution.

**Headline: the move the project was considering has already been made. Cui et al. (2025), in
*Journal of Psychopathology and Clinical Science*, publish the four-type transition classification applied
to clinical psychopathology, complete with a decision tree for assigning a case to a type. Spec §5's
outcome O2/O3 applies, not O1 — because their assignment is semi-qualitative, un-preregistered, and run
on simulated rather than observed series. And their framework contains no hysteresis at all.**

Third collision with the same research group in one day. `catastrophe_flag_prior_art_survey_2026-07-30.md`
found Cui, Hasselman & Lichtwarck-Aschoff (2023) had published one of the project's own conclusions two
years earlier, and Olthof et al. (2020) had published on the project's own dataset. **Cui is also the
first author here.**

---

## 1. Execution record (completes spec §7)

### 1.1 Counts

| Leg | Blocks | PubMed | OpenAlex |
|---|---|---:|---:|
| — | MECH | 11,944 | |
| — | MECH+TIP | 323 | |
| **P1** | MECH+TIP+PSYCH | **17** | **231** |
| **P2** | MECH+TIP+WITHIN | **19** | **122** |
| **P3** | MECH+TIP (count only) | 323 | 3,598 |

Retrieved and deduplicated across OpenAlex, Europe PMC and PubMed: **345 unique**.
Screening: **READ 22 · METHOD_PRECEDENT 20 · EXCLUDE 303**.

### 1.2 A caveat about the READ count, which is smaller than it looks

The 22 `READ` records are **8 distinct works**. The inflation is version and review clutter:

- 5 records are one work (Cui et al. — the journal article, its correction, and three preprint versions)
- 8 records are one work (an EGUsphere ice-sheet preprint plus its open peer-review thread: RC1–RC3,
  AC1–AC3, EC1 — each carries the parent abstract and so each screened in)
- 2 records are one Entropy/Preprints.org ecology review
- 2 records are one Zenodo item, twice-deposited; another 2 likewise

**Only one of the eight distinct READ works is a psychological application.** Reporting "22 READ" without
this decomposition would overstate the literature by roughly threefold.

### 1.3 Deviation from spec, recorded

One edit was made to `work/bnr_tipping_prior_art.py` after execution: `sys.stdout.reconfigure(...)`, because
the Windows console is cp932 and a title containing an en-dash aborted the summary print **after both CSVs
had been written**. This changes console display only. **No block, screening rule, retrieval path or
output was affected**, and the CSVs analysed below are the ones the frozen run wrote.

---

## 2. The finding: Cui et al. (2025)

*Understanding types of transitions in clinical change: An introduction from the complex dynamic systems
perspective.* **Journal of Psychopathology and Clinical Science** 134(4), 469–482,
doi:`10.1037/abn0000991`. Preprint `osf.io/b68wh` (v2.0.4 read in full). Code and data `osf.io/4jaqk`.
**Correction:** doi:`10.1037/abn0001061`.

### 2.1 Four types, not three

| Type | Mechanism |
|---|---|
| **B-tipping** | bifurcation-induced — the landscape destabilises as a control parameter drifts. This is the fold. This is what the project has been calling 折り返し. |
| **N-tipping** | noise-induced — stability does not change; noise throws the system out of its basin into an alternative basin that already existed. Explicitly **no EWSs are detectable**, because there is no pre-transition destabilisation. |
| **R-tipping** | rate-induced — the transition depends on how *fast* the driver changes, not on its level. |
| **N-diffusion** | noise-induced diffusion — noise is high enough that there is **no single identifiable tipping point**; the system's occupancy of the state space changes without a discrete transition. |

The fourth type is the one this project had not anticipated, and it matters: N-diffusion is the class into
which "the marginal distribution changed but nothing tipped" falls — which is a description of much of
what the project's own pre-gate has been measuring.

They cite Ashwin, Perryman & Wieczorek (2017) among others; the classification's origin is the Ashwin
lineage, as expected. **Per spec §5, the project claims no part of it.**

### 2.2 There is already an assignment rule — Figure 8

Figure 8 is a three-question decision tree. It is embedded as vector text with a stripped ToUnicode map,
so it does not survive ordinary PDF text extraction; it was recovered by decoding the form XObject's
glyph ids directly (`work/`-external, script in the session scratchpad).

**Q1.** *"Do you think your [state] is qualitatively different than before, or are you just in this state
more/less often?"*
→ *just more/less often* → **N-diffusion**  ·  *qualitatively different* → Q2

**Q2.** *"Do you think the direct event that caused the transition would also have caused a similar
transition if it happened at another time?"*
→ *Yes* → **N-tipping**  ·  *No* → Q3

**Q3.** *"Then for the factor that made the direct event specifically lead to the transition at this time,
if it had changed slower, would the transition have happened?"*
→ *Yes* → **B-tipping**  ·  *No* → **R-tipping**

### 2.3 A trap: the free version of Figure 8 is wrong

The corrected mapping is given in §2.2. **The preprint at `osf.io/b68wh` — the only openly accessible
version — prints Q3's two terminals reversed**, i.e. *Yes* → R-tipping and *No* → B-tipping. This is
confirmed twice over: by the decoded coordinates in the preprint figure, and by the published Correction,
which states that the final steps were inadvertently reversed and that Yes should lead to B-tipping.

The corrected direction is also the dynamically correct one. If the transition would still have occurred
had the driver changed more slowly, the transition depends on the driver's *level* — a threshold crossing,
B-tipping. If it would not have occurred, it depends on the driver's *rate* — R-tipping.

**Anyone in this project citing Figure 8 must cite the erratum version.** Recorded here because the
project's most reliable defect source is exactly this: a cited source paraphrased from the accessible copy.

### 2.4 What they did NOT do — and this is where the project's room is

| | Status in Cui et al. 2025 |
|---|---|
| Classification | **done** (borrowed from the Ashwin lineage) |
| Applied to clinical psychopathology | **done** |
| Assignment rule | **done** — but *semi-qualitative*: interview questions, or ESM-embedded counterfactual items. Not an estimator. |
| Applied to **observed** time series | **not done.** "we present two real-life scenarios **using simulated time series**". The illustrations are simulations built to resemble scenarios. |
| Pre-registered | **no** — the paper states plainly that it was not pre-registered |
| **Hysteresis** | **absent. The word does not occur once in the paper.** |
| Cross-individual stability of type | **not addressed**, and see §2.5 |

They name three routes to empirical examination and leave all three open: repeated controlled experiments
(in vivo or in silico), EWS detection, and the (semi-)qualitative route.

They also, again, use this project's dataset. Figure 5's caption: data retrieved from Kossakowski et al.
(2017) — the antidepressant-discontinuation series in `work/acquired_data/kossakowski/`. The analysed
series is simulated *according to* that scenario. **That is now the third paper found today to have
touched the project's own data before the project did.**

### 2.5 The sentence that constrains restated-D1

> The type of transition can therefore not be defined for the change as a whole, but is specific to the
> variables of investigation.

Their claim is that different variables **within the same person** undergo different transition types
simultaneously, and that real cases show mixed characteristics because the type is set by whichever
parameter is momentarily dominant (their Supplementary Table A1).

**This is a direct constraint on the restatement of D1 that was proposed as the way out.** The proposal was
to move D1 from "parameters transfer across cases" to "the type assignment transfers across cases",
because categorical agreement can be tabulated where continuous aggregation cannot. Cui et al. attach the
type to a **variable**, not to a person, and hold that types co-occur within one person. So the restated
D1 has to be specified per variable, on a fixed variable set, or it inherits exactly the aggregation
problem it was meant to escape. **The escape is narrower than it looked, and it is not free.**

---

## 3. Other distinct works in the shortlist

| Work | Bearing |
|---|---|
| **Bury et al. / AMOC deep-learning line** — *Deep learning for predicting rate-induced tipping*, Nature Machine Intelligence 2024, doi:`10.1038/s42256-024-00937-0`; *Probabilistic anticipation of AMOC transitions…*, Chaos Solitons & Fractals 2026, doi:`10.1016/j.chaos.2026.118374` | The strongest **method** precedent: these explicitly attack the problem of anticipating transitions when a system is susceptible to B-, N- **and** R-tipping at once, i.e. the discrimination problem. Climate, not psychology, and data-hungry. |
| **Υ-indicator / ARMA stability indicator**, Chaos 2022, doi:`10.1063/5.0089694` | A stability indicator estimated from an ARMA fit, tested against a system exposed to all three tipping routes. Closest thing to a cheap quantitative discriminator found. Simulation only. |
| **Bayesian Langevin estimation of local stability and noise**, Nature Communications 2025, doi:`10.1038/s41467-025-60877-0` | Separates deterministic drift from noise level simultaneously, on real observed data (a 1996 power-grid blackout). **Non-Markovian.** This is the estimator class `work/drift_landscape.py` is a simplified cousin of, and it separates exactly the B-vs-N axis. Worth obtaining. |
| *Early Warning Signals in Ecological Time-Series*, Entropy 2026, doi:`10.3390/e28060628` | Recent review; useful for the EWS-does-not-imply-B-tipping point, already established here. |
| *Formalization of Mental Disintegration Phenomena Through Dynamical Systems Theory*, Open MIND / Zenodo 2026 | Psychology + bifurcation/noise vocabulary, but a formalization essay mapped onto DSM-5-TR categories, single self-affiliated author, no data. Not prior art of standing. |
| Two Zenodo "unifying framework for EWS" / CRTI deposits (2026) | Self-deposited preprints proposing new EWS indices. Recorded; not weighed. |

**No record in either leg tests whether transition type is stable across individuals.** Spec §5's Q4 note
therefore returns nothing: there is no prior art for restated-D1.

---

## 4. Which outcome statement applies

Spec §5 offered O1–O4. **The answer is between O2 and O3, and closer to O3.**

- Not **O1**: no record assigns *observed* cases to classes in psychology. Cui et al. assign scenarios,
  illustrated with simulations.
- **O2 applies** to the classification and to the clinical framing: both are established. The project
  cites and borrows; it claims neither.
- **O3 applies** to the assignment: a rule exists, but it is semi-qualitative, retrospective, subject to
  the recall and counterfactual-reasoning limits its own authors list, and un-preregistered.

**Therefore, per the pre-committed statements, the project may not describe the typology or its clinical
application as new.** What remains available, stated at the size it actually is:

1. **A quantitative, pre-registered assignment on observed series.** Cui et al. supply the rule; they run
   it on simulations and interviews. The project holds `drift_landscape.py` (attractor count from the
   drift field) and the frozen HysTAR route, and holds four observed ESM datasets. Running a frozen
   quantitative version of Figure 8's partition on real series is not done and is the cheap next step.
2. **The hysteresis axis they omit.** Their four types do not include direction-dependent thresholds; the
   word does not appear in the paper. D4 — the decline arm and the recovery arm sharing one parameter set
   — is orthogonal to their classification rather than contained in it. **This is the project's frozen
   preregistration (`10.5281/zenodo.21366132`), and it is the one thing in this space that is still the
   project's own.**
3. **Cross-case transfer of the type** (restated D1), no prior art — but see §2.5 for the price.

---

## 5. What this changes about yesterday's priority order

`catastrophe_flag_prior_art_survey_2026-07-30.md` §5 set five priorities. This scan does not overturn
them; it re-weights two and adds one.

1. **Re-ask the structure question at episode scale** — unchanged, still first.
2. **Approach the Hosenfeld data** — unchanged.
3. **Run `drift_landscape.py` on Kossakowski** — **promoted.** It was "answers whether there are two
   attractors". It is now also the first component of a quantitative B/N/R assignment, and Cui et al.
   have published the partition it would feed.
4. **Decide what to do about D1** — **the restatement now has a price** (§2.5). The type is
   variable-specific in the source that defines it. Either the restated claim is specified per variable on
   a fixed variable set, or it does not escape the aggregation objection.
5. **New: obtain the Bayesian Langevin estimation paper** (doi:`10.1038/s41467-025-60877-0`). It separates
   drift from noise on real data without a Markov assumption, which is both the B-vs-N discriminator and a
   repair for `drift_landscape.py`'s inherited Markov limit.
6. Obtain Chow et al. 2014 — still owed.

---

## 6. The uncomfortable summary

Three papers found in one day, all from the same Groningen/Radboud orbit, have each occupied ground the
project believed was ahead of it: the bimodality-is-not-bistability result (2023), an analysis of the
project's own dataset (2020), and now the transition typology with its assignment rule (2025) — the last
of which also builds its central illustration on the project's dataset.

**The honest reading is not that the project is wrong. It is that the project has been deriving, alone,
what one research group has been publishing, and has been finding this out afterwards each time.** The
survivable part of today is narrow and real: hysteresis is absent from their framework, the project's
preregistration is about hysteresis, and nobody has run a quantitative type assignment on observed
psychological series.

That is a smaller claim than "a unified theory of collapse." It is also the first claim today that a
search has not already taken away.
