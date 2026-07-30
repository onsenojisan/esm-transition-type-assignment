# Hosenfeld et al. (2015) — data assessment, and a correction to this morning's survey

**2026-07-30.** Priority item 1 of `transition_type_assignment_result_2026-07-30.md` was "obtain episode-scale
data; approach Hosenfeld." This reads the paper in full instead of from its abstract.

**Headline: the measurement is retrospective. The nine symptoms were not recorded weekly as they happened;
they were reconstructed week-by-week at three-monthly interviews. That makes the dataset unsuitable for the
use the project intended, and it also qualifies the finding this project has been citing as its best
episode-scale evidence.**

Source: PMC4574448, full text, doi:`10.1186/s12888-015-0596-5`.

---

## 1. What the Methods say that the abstract does not

The abstract says the symptoms were "recorded weekly for two years." The Methods say how:

> From 1998 to 2003, 267 patients diagnosed with MDD participated in a randomised controlled trial with
> **follow-ups every three months** during three years.

> The presence of the nine DSM-IV criteria for depression … was recorded **retrospectively for every week in
> the preceding three months**.

So the design is a **LIFE-chart-style retrospective reconstruction**: eight interviews, each asking the
patient to recall ~13 weeks of symptom presence. The weekly resolution is a *recall* resolution, not a
sampling resolution.

Two further qualifications from the same section:

- **178 of 267** are those with complete records over 104 weeks — a completer subsample, not the cohort.
- The **104-week cutoff was chosen "after inspection of the frequency distributions of responders on each of
  the time-points."** A post-hoc window choice.

## 2. Why this disqualifies it for the project's use

The project wanted this series to carry a **drift-field / dwell-time / transition-sharpness** analysis at
episode scale — the same instruments run today at beep scale.

Those instruments read the **increment structure** of a series: Δx between consecutive observations is the
entire input to the drift and diffusion estimates, and run length is a count of consecutive same-side
observations. In a retrospectively reconstructed series, consecutive weekly values are not consecutive
measurements; they are adjacent cells of one recall episode.

Retrospective recall over a multi-week block is well known to produce blocked, step-like reconstructions —
people recall "that month was bad," not a week-by-week gradient. That means:

> **The sharp jumps and two-state appearance that make this dataset attractive are exactly the features the
> measurement method is most likely to manufacture.**

This is not a claim that the paper is wrong. Hosenfeld et al. asked whether symptom *courses* look
two-state, and their instruments (bimodality coefficient, 1- vs 2-state HMM) are applied to what was
recorded. It is a claim that **the series cannot support the project's instruments**, because those
instruments interpret increments as dynamics.

## 3. Correction to `catastrophe_flag_prior_art_survey_2026-07-30.md`

That survey (§3, §5) stated:

> **178 primary-care MDD patients. The nine DSM-IV symptoms recorded WEEKLY for 104 weeks**
> … Hosenfeld is the test. Weekly, 104 points, 178 people, at the timescale D4's decline and recovery arms
> actually live at.

**That was written from the abstract and is materially incomplete.** The corrected statement:

> Hosenfeld et al. (2015) report that a two-state pattern describes the *retrospectively reconstructed*
> weekly symptom course in most of a completer subsample. The reconstruction was performed at three-monthly
> interviews. The finding is about recalled course, and the project cannot use the series for dynamical
> estimation.

**What this does to the survey's conclusion.** The survey's item 3 read "at episode scale the two-state
premise looks common, not rare — and the project has never measured at that scale." The second half stands.
The first half must be weakened: **at episode scale the two-state premise looks common *in retrospectively
recalled course data*, which is the measurement most likely to produce it.**

That was listed as the one new finding *for* the theory today. It is now the weakest of the three.

### A surname that looks like a collision and is not

Two different researchers at the same institution share the surname *Bos*; the Hosenfeld co-author and the
custodian of an unrelated bipolar EWS dataset are not the same person. Recorded so the two are not conflated.

## 4. Custodian and provenance

| | |
|---|---|
| Correspondence | The article's corresponding author, at the University of Groningen / UMCG **Interdisciplinary Center Psychopathology and Emotion regulation (ICPE)**. Contact details are printed in the open-access article; they are deliberately not reproduced here. |
| Parent study | Primary-care MDD RCT 1998–2003, 397 patients referred by 49 GP practices in the North of the Netherlands; 267 participants. Refs: Smit et al. (2006) *Psychol Med*; Conradi et al. *Psychol Med* |
| Ethics | Medical Ethics Committee, UMCG. Informed consent obtained |
| **Data availability statement** | **None in the article.** 2015 *BMC Psychiatry* predates the journal's mandatory availability statement |

**No data request is drafted and none should be sent on the strength of this.** A structural barrier
recorded elsewhere in this project applies with full force here — sensitive human clinical data, a
requester without institutional affiliation, therefore no institutional ethical oversight for secondary
use. Asking for a dataset the project has just established it cannot use would spend an approach for
nothing.

## 5. What episode scale actually requires now

The requirement is sharper than "weekly resolution over an episode":

> **Prospectively sampled**, at a fixed interval, over a decline **and** a recovery, in one person, with the
> interval short relative to the phenomenon's relaxation time and the series long relative to its dwell time
> (per today's power–dwell result, **T ≳ 20–30 × dwell**).

Retrospective reconstruction, however fine its nominal resolution, does not satisfy the first clause. This
should be added to the search predicate before any further dataset scan — it would have excluded this
candidate at screening.

## 6. Consequence for the priority order

Item 1 ("re-ask the structure question at episode scale") is **not** removed — it remains the open question.
Item 2 ("approach the Hosenfeld data") is **withdrawn**: the candidate does not meet the design predicate.

The project has now examined its two best episode-scale leads and neither survives: one where the data could
not be obtained, and Hosenfeld et al. 2015, where the measurement is unsuitable. The pattern is unchanged — **a purpose-built prospective study is not the fallback, it
is the only route**, and it needs an institutional affiliation the project does not have.

---

*Public-copy note: contact details for named third parties, and the identities of custodians who did not supply data, are omitted from this published version. They remain in the author's private working record. Nothing analytical is removed.*
