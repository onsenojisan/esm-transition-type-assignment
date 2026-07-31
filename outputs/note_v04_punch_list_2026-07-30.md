# v0.4 punch list — review of the deposited v0.3

**2026-07-30, after deposit.** Not acted on: v0.3 stands as
doi:`10.5281/zenodo.21703786`. This records what a v0.4 should carry, and which review points were
declined and why, so neither has to be reconstructed later.

---

## 1. The one that reaches the main result — needs a calibration, not a sentence

**§7 names response style as "the largest unaddressed threat" and §5 claims degeneracy cannot manufacture a
second attractor. There is no bridge between them, and the missing direction is the one that matters.**

Degeneracy destabilises the *position* of the attractor that is found — established in §5. But §7 also says
structured response styles would **reshape** the drift field, flattening it where a respondent avoids
answering. A flattened field can **erase a shallow second attractor**. That is a false-negative mechanism
acting directly on the 66/66 single-attractor result, and v0.3 does not discuss it.

**The test.** Apply a compressive response-style transform to the bistable generators and measure where
detection fails. Central-tendency bias is the natural first case: map the latent value toward the scale
midpoint before quantising, sweep the compression strength, and report detection rate against compression
for the separations already calibrated (2, 3, 4, 6 SD) plus the deep well.

Two outcomes, both worth having:
- detection survives realistic compression → the main claim gains the support it currently lacks
- detection collapses at compressions plausible for symptom items → **the null is weaker than v0.3 states**,
  and the note must say so

Until run, the honest form of §4's claim is: *no second attractor was found, and the sensitivity of that
finding to response-style compression is unmeasured.*

> ### RUN 2026-07-30 — the unfavourable branch obtained
>
> `response_style_compression_result_2026-07-30.md`. **A 20% central-tendency compression takes a 6 SD
> bistable system from 100% detection to 5%**; a genuine deep well is gone by 50% compression. False alarms
> stay at zero throughout, so compression is a **pure false-negative mechanism**.
>
> **This is no longer a punch-list item. It is a correction to the deposited claim**, and v0.4 must carry it
> as the primary one rather than as a limitation bullet. The note's 80–100% power figures were all measured
> with no response-style distortion.
>
> Two qualifications found in the same run: the c = 1.0 baselines depend on a **discretisation convention**
> the note reports without flagging as a choice (fixed-anchor grid vs range-matched), and §8's "93% power"
> for the inaccessibility flag holds only under range-matching. Both go into v0.4.
>
> Not established: whether *this* participant's responses are compressed. Concentration from a quiet symptom
> and compression from a response style are not separated by this run.

## 2. Declined, with reasons

**"The abstract drops the 'sufficiently deep' condition."** It does not. The abstract reads *"uninformative
in principle, for any finite series, **about barriers deep enough that the second state is never
visited**"*. The condition is in the sentence. Misread.

**"Using an estimator whose b is biased 2–3× low to judge that b is below threshold is circular."** It is
not, on two counts. The decision rule short-circuits at *fewer than two stable points → no-second-attractor*,
so **the b gate was never applied to the observed data at all** — not merely "b was not computed", but the
gate is not on the path the data took. And the 2–3× figure comes from comparing measured b against the
generators' **algebraically known** true b, which is an external check, not the estimator judging itself.

## 3. Accepted, cheap

- **Abstract / body gradient on `T ≳ 20–30 × dwell`.** The body downgrades it to a rule of thumb read off
  one generator; the abstract states it flatly. Qualify it in the abstract.
- **What the deposit timestamp does and does not establish.** §2.3 confesses the specs were not committed
  before the runs. Add the precise consequence: the Zenodo record and the `v0.3-zenodo` tag establish an
  **upper bound** — the specifications existed no later than 2026-07-30 — and establish nothing about their
  order relative to the runs. A confession plus a bound is worth more than a confession.
- **NBLE insensitivity rests on 0 vs 3 SD only.** Add 1 and 2 SD; without intermediate points, "cannot
  separate" is asserted from two corners rather than from a flat response curve.
- **Move the "author core" note out of the reference list.** The observation — Cui, Hasselman and
  Lichtwarck-Aschoff carry the 2023 method, the 2020 complexity analysis and the 2025 typology alike — is a
  legitimate prior-art point and belongs in §1 as analysis. In a bibliography footnote it reads as an
  editorial aside about a research group, which is not the register of the rest of the note.

## 4. Accepted — and larger than "awkward": §1 is factually wrong about this project

The first reading of this point was that the van der Maas juxtaposition is a presentational oddity. It is
not. **§1's claim that the cusp-catastrophe literature "is not surveyed here" is false about the project's
own operating frame.**

From the project's own record:

- `structure_gate_build_and_power_2026-07-26.md` states the module implements "the families Helmich et al.
  2024 name as the way to establish **catastrophe flags**" — the gate exists for that purpose
- `hysteresis_prior_art_survey_2026-07-30.md` positions HysTAR as confirming "a catastrophe flag"
- `make_or_break_offline` generates "idealized **cusp**/OU processes"
- `ews_critique_helmich_2024_assessment.md` already carries the bifurcation taxonomy (Hopf, transcritical,
  pitchfork / **fold**, cusp, butterfly) and four named routes to a transition without EWS

So the framework is not unsurveyed — it is the frame the project has been working inside for weeks. What
the vocabulary-based scan failed to retrieve is the **primary literature**, and the honest statement is
therefore not "not surveyed" but:

> The catastrophe-flag framework is this project's operating frame, adopted through **one secondary source**
> (Helmich et al., 2024). The primary literature that defines the flag set has not been read, and the
> vocabulary-based scan in §1 would not have retrieved it.

**That is a different and more uncomfortable admission**, and it is the correct one. It also names the risk:
a framework held through a review's one-sentence paraphrase is the same failure shape as any other
paraphrase hardening into canon.

### The consequence that is not cosmetic

Helmich's quoted definition is *"Catastrophe flags include — **but are not limited to** — the presence of
two or more stable states (bimodality or multimodality), states with distinct tipping points
(**hysteresis**), and sensitivity to certain initial conditions."*

Three flags, explicitly non-exhaustive. **The project has never established how many there are.** If the
canonical set is larger, then flags exist that this project has not considered — and any that require
neither CSD nor a recovery arm would be applicable to the 1,476-point series already in hand. That is the
one place today's beep-scale data could still be asked something new.

### And it weakens a positioning claim

Hysteresis is **one of the flags, named by Helmich**. The note treats it as the project's uncontested
ground on the strength of its absence from Cui et al. (2025). Absent from that taxonomy: true. The
project's own distinctive ground: weaker than stated — it is a flag the field has prescribed establishing,
and the frozen preregistration answers that prescription. A legitimate contribution, but "assigned
homework" rather than "unclaimed territory," and §1 should say which.

## 5. Accepted as accurate, nothing to change

**The analysis rests on a null plus a retraction, and the surviving claim is narrow.** True, and the note
already says so in those terms. Recorded so it is not mistaken for an unaddressed criticism.

## 6. Also carried forward, from the deposit itself

The preregistration reference in the deposited files cites `10.5281/zenodo.21366132` — the version DOI for
the 2026-07-04 v0.1, superseded the same day by v0.2 + Amendment 1 (`21694817`). The concept DOI
`21366131` is correct and is already fixed in the working note and the public repository. **A v0.4 carries
the fix into the files**, which is the only way to correct it; Zenodo forbids replacing published files, and
replacing bytes under a live DOI would defeat the point of depositing.

An in-place metadata edit of the related identifier was attempted and **did not persist** — the form field
accepted the new value, `Save draft` wrote the old one, twice, by two different input methods. Cause not
identified. Do not assume the record's metadata is corrected.
