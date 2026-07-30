# B/N/R tipping prior-art scan — search spec v1.0, FROZEN

**Frozen 2026-07-30, before execution.** Blocks, screening rule and outcome statements below are fixed
before any count is seen. Same discipline as `systematic_search_protocol_v1.md` §0, at a smaller scope
(see §6).

## 0. Why this exists

The project is considering a move: stop claiming the fold (saddle-node / bifurcation-induced tipping) is
the universal mechanism of collapse, and instead claim that the **set of collapse mechanisms is a closed
classification** and that 様式 patterns map onto it. The outcome side of that map already exists in
`l4_generic_change_distinction_note_v0.1.md` (repair / sustained non-repair / reorganization / near miss).
The mechanism side appears to exist in the tipping-point literature as the **bifurcation-induced /
noise-induced / rate-induced (B/N/R)** partition, which returns **zero hits** on grep across this
repository — the project has never cited it.

On 2026-07-30 the project found that Cui et al. (2023) had published one of its own conclusions two years
earlier. That is the second such finding. **This scan runs before anything is written, not after.**

## 1. Questions

- **Q1** Is the B/N/R partition an established classification, and what is its canonical source?
- **Q2** Has it been applied to **human psychological / psychiatric within-person time series**?
- **Q3** Has anyone specified a rule that **assigns an observed series to one of the classes** — as
  opposed to naming the classes theoretically or demonstrating them in simulation?
- **Q4** Has anyone tested whether the **class assignment is stable across individuals** (the quantifier
  the project would move D1 to)?

## 2. Sources (fixed)

PubMed/MEDLINE (E-utilities); Europe PMC (REST, includes preprints); OpenAlex.

**Excluded, and why:** Scopus, Web of Science, Embase, PsycINFO — no institutional subscription. Declared
coverage limit, inherited from protocol v1 §2.

## 3. Blocks (frozen — the strings in `work/bnr_tipping_prior_art.py` as of this freeze)

| Block | Content |
|---|---|
| `MECH` | rate-induced, rate induced, rate-dependent, noise-induced, noise induced, bifurcation-induced, bifurcation induced, B-tipping, N-tipping, R-tipping |
| `TIP` | tipping, critical transition\*, regime shift\*, bifurcation, attractor, alternative stable state\*, critical slowing, early warning |
| `PSYCH` | psychiatric, psychopathology, depression, depressive, mood, affect, emotion\*, anxiety, mental health, experience sampling, ecological momentary, burnout, psychotherapy, wellbeing, well-being |
| `WITHIN` | within-person, within-subject, intensive longitudinal, idiographic, single-case, n-of-1, time series, individual trajector\* |

`MECH` is ANDed with `TIP` in every leg. This is deliberate and is the one precision choice made in
advance: `MECH` alone retrieves noise-induced hearing loss and rate-dependent pharmacology in volume, and
neither is about transitions.

| Leg | Blocks | Purpose |
|---|---|---|
| **P1** | MECH AND TIP AND PSYCH | Q2 — the core question |
| **P2** | MECH AND TIP AND WITHIN | Q2/Q3 broadened past psychology to any within-person or time-series application |
| **P3** | MECH AND TIP | Q1 — counts only, to size the literature and locate the canonical source |

**No block may be altered after execution begins.** If a leg returns unmanageable volume, that is
reported as a result, not repaired.

## 4. Screening (frozen)

Mechanical first pass on title + abstract, then author read of the shortlist.

| Test | Rule |
|---|---|
| `S1_PARTITION` | **≥ 2 of the three mechanism families** named: {rate, noise, bifurcation}. The project's claim is about the *partition*; a paper on one mechanism alone is prior art for one cell, not for the classification. |
| `S2_PSYCH` | a `PSYCH` term present |
| `S3_APPLIED` | an applied-to-data marker: participants, patients, empirical, dataset, cohort, observed, experience sampling, ecological momentary |

| Decision | Condition |
|---|---|
| `READ` | S1 AND S2 |
| `METHOD_PRECEDENT` | S1 AND NOT S2 — the partition applied outside psychology; relevant as method precedent |
| `EXCLUDE` | otherwise, with the failed tests recorded |

`S3_APPLIED` is recorded but **does not gate** the decision: abstracts frequently omit it, and Q3 is
answered by reading, not by keyword.

**Declared limitations, frozen in advance:** one screener; AI assistance is a first pass and is **not**
counted as a screener; abstract-level; no Embase/PsycINFO/Scopus/WoS; OpenAlex retrieval capped at 6
pages × 200; keyword detection finds *mentions*, not designs.

## 5. Pre-committed outcome statements

Fixed now so none can be written to fit what comes back.

**Unconditional, under every outcome below:**

> **The B/N/R partition is not the project's. Whatever the canonical source turns out to be, it is cited
> as the origin of the classification, and the project claims no part of it.** If the classification
> proves to have a different canonical source than expected, that source is used instead — the
> expectation is not defended.

- **O1 — a record names ≥2 mechanism families, applies them to human psychological/clinical
  within-person data, and assigns observed cases to classes.** The application-novelty claim **falls**.
  The project cites it, positions the correspondence table as replication or extension, and does not
  describe the application as new.
- **O2 — the partition is applied, but outside psychology only.** Classification and application method
  are both established; the project's available contribution narrows to the psychological application
  plus §1 Q3's assignment rule.
- **O3 — the partition appears in psychology theoretically, with no assignment to observed cases.** The
  gap is the **assignment rule**. The contribution is described as "assignment rule + cross-case transfer
  test", never as "new typology".
- **O4 — nothing found in P1 or P2.** Reported as *"targeted prior-art scan across three sources under a
  spec frozen before execution; no application found"*, bounded by §4. It may **not** be stated that no
  such work exists.

**On Q4 specifically:** if any record tests cross-individual stability of class assignment, that is
recorded as prior art for **restated-D1** and named, whichever of O1–O4 obtains.

## 6. What this scan is not

This is a **targeted prior-art scan, not a systematic review**, and it is scoped below the
co-measurement run deliberately: it does not underwrite a published claim, it informs whether a claim may
be attempted. A frozen spec removes the forking-paths problem. It does not remove the single-screener
problem, the missing subscription databases, or abstract-level screening.

## 7. Execution record

**Executed 2026-07-30. Spec frozen before execution; no block, source, screening rule or outcome
statement was altered during or after the run.**

| Leg | Blocks | PubMed | OpenAlex |
|---|---|---:|---:|
| — | MECH | 11,944 | |
| — | MECH+TIP | 323 | |
| P1 | MECH+TIP+PSYCH | 17 | 231 |
| P2 | MECH+TIP+WITHIN | 19 | 122 |
| P3 | MECH+TIP (count only) | 323 | 3,598 |

**345 unique** after deduplication across three sources. `READ` 22 · `METHOD_PRECEDENT` 20 · `EXCLUDE` 303.
The 22 `READ` records are **8 distinct works**; the inflation is version and open-peer-review clutter, and
is decomposed in the survey §1.2.

Records: `bnr_prior_art_2026-07-30_{counts,screened}.csv`. Result and reading:
`bnr_tipping_prior_art_survey_2026-07-30.md`.

**Outcome: between §5's O2 and O3, closer to O3.** The classification and its clinical application are
established prior art (Cui et al., 2025, *J Psychopathol Clin Sci*, doi:`10.1037/abn0000991`), and an
assignment rule exists (their Figure 8) but is semi-qualitative, un-preregistered, and demonstrated on
simulated rather than observed series. Per §5 the project may **not** describe the typology or its clinical
application as new. The unconditional statement in §5 stands: the partition is not the project's.

**Post-execution edit, recorded:** `sys.stdout.reconfigure(...)` was added to
`work/bnr_tipping_prior_art.py` after the run, because the cp932 console aborted the summary print **after
both CSVs were written**. Display only; no block, rule, retrieval path or output affected.
