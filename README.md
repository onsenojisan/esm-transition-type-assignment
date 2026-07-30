# Transition-type assignment on intensive longitudinal affect data

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21703785.svg)](https://doi.org/10.5281/zenodo.21703785)

A pre-registered quantitative test for **alternative stable states in ESM (experience-sampling) mood
series**, and what came back. One working day, 2026-07-30, deposited whole — including the parts that
failed.

The accompanying note is archived at doi:[10.5281/zenodo.21703785](https://doi.org/10.5281/zenodo.21703785),
which includes a snapshot of this repository.

**Result: no second attractor at beep scale.** In the only series long enough to analyse, all 11 units
returned a single attractor and no barrier, at every bandwidth and every increment definition, with the
instrument's power measured rather than assumed: 80% against a genuine deep-well bistable generator at that
length, 92.5–100% against 4–6 SD separation, at a 2.5% false-alarm rate.

---

## Read this first

**This repository contains a retraction.** A positive finding was produced during the day, survived four
calibrated nulls, and was then killed by looking at the raw response counts. It is
[`outputs/moving_well_retraction_2026-07-30.md`](outputs/moving_well_retraction_2026-07-30.md), and the
documents it retracts are kept in place with banners rather than deleted.

It is included deliberately. A record of four failed nulls being mistaken for support, and of what actually
explained the effect, is more useful than the finding would have been.

**The classification tested here is not mine.** The four-type transition taxonomy — bifurcation-induced,
noise-induced, rate-induced tipping and noise-induced diffusion — and its clinical assignment tree are
published by **Cui et al. (2025)**, *Journal of Psychopathology and Clinical Science* 134(4) 469–482,
doi:[10.1037/abn0000991](https://doi.org/10.1037/abn0000991), in the Ashwin lineage. This repository
borrows it and claims no part of it. What is contributed is a **quantitative, frozen-before-execution
version of one of their questions, run on observed rather than simulated series.**

> ⚠️ **If you use their Figure 8, use the erratum.** The openly accessible preprint (`osf.io/b68wh`) prints
> the decision tree's last two terminals **reversed**. The correction,
> doi:[10.1037/abn0001061](https://doi.org/10.1037/abn0001061), is canon: *yes* → B-tipping, *no* →
> R-tipping. Verified here against the preprint figure's own coordinates.

---

## What is in here

Two specifications were **written and frozen before the runs they govern**, each with pre-committed outcome
statements so neither result could be written to fit what came back.

| Document | What it is |
|---|---|
| [`bnr_prior_art_search_spec_v1.md`](outputs/bnr_prior_art_search_spec_v1.md) | Frozen search spec — blocks, screening rule, outcomes O1–O4 |
| [`bnr_tipping_prior_art_survey_2026-07-30.md`](outputs/bnr_tipping_prior_art_survey_2026-07-30.md) | Result: 345 records across PubMed / Europe PMC / OpenAlex. The typology and its clinical application are prior art |
| [`transition_type_assignment_spec_v1.md`](outputs/transition_type_assignment_spec_v1.md) | Frozen assignment spec — the estimator, the gate, what is in and out of scope, outcomes A1–A4 |
| [`transition_type_assignment_result_2026-07-30.md`](outputs/transition_type_assignment_result_2026-07-30.md) | **The main result.** Outcome A3, with the power table |
| [`moving_well_and_undersampling_result_2026-07-30.md`](outputs/moving_well_and_undersampling_result_2026-07-30.md) | Undersampling and narrow-deep-well calibration; the retracted moving-well section |
| [`nble_rerun_result_2026-07-30.md`](outputs/nble_rerun_result_2026-07-30.md) | Re-run under Bayesian Langevin estimation (antiCPy), and why it cannot answer the question |
| [`moving_well_deflation_result_2026-07-30.md`](outputs/moving_well_deflation_result_2026-07-30.md) | Deflation check against the plain window mean |
| [`skewed_well_null_result_2026-07-30.md`](outputs/skewed_well_null_result_2026-07-30.md) | Skew / peakedness / discretisation nulls |
| [`moving_well_retraction_2026-07-30.md`](outputs/moving_well_retraction_2026-07-30.md) | **The retraction** |
| [`hosenfeld_data_assessment_2026-07-30.md`](outputs/hosenfeld_data_assessment_2026-07-30.md) | Why a much-cited weekly two-state dataset cannot carry this analysis |
| [`collapse_typology_correspondence_v0.1.md`](outputs/collapse_typology_correspondence_v0.1.md) | Design note pairing the mechanism classes with an outcome typology |

## Findings that do not depend on the retracted part

- **The estimator's own calibration set was in the wrong regime all along.** Every bistable generator this
  project had calibrated on sits at a dimensionless barrier **b < 1** across every separation ever tested
  (2 SD → 0.008 … 6 SD → 0.626). "Two states" there meant two humps in a stationary density crossed every
  few observations, not two states with rare transitions.
- **A power–dwell squeeze.** Detecting two attractors needs the system to visit both, so the series must be
  many dwell times long — but a deep barrier, the thing that makes a transition discrete, is exactly what
  makes the dwell long. Empirically **T ≳ 20–30 × dwell**.
- **A permanent limit.** At b ≳ 15 the second state is never visited in 1476 observations. *No finite
  series can exclude a sufficiently deep well.* The null here is bounded by that, and says so.
- **The Kramers dwell estimate is invalid in this regime** and is written to a column named `INVALID`
  rather than quietly dropped. Model-free run length is used instead.
- **An undersampling fingerprint**: bimodal marginal with a single-attractor drift field whose root sits at
  the true barrier. Real, reproducible, and *not* present in the data analysed here.
- **Two degeneracy guards** now in the estimator, neither of which existed before the retraction:
  `modal_share > 0.60` flags a series that is mostly one response level, and wells whose local SD exceeds
  3× the series SD are rejected as λ ≈ 0 failed fits.

## Data — not included

No participant data is redistributed. The series analysed are public ESM datasets under their own terms
(Kossakowski et al.; Fisher; Geschwind/Bringmann CC BY-NC; Marian), obtained from their original
distributors. `work/acquired_data/` is absent by design; the code expects it and will report that no series
met the observation gate without it.

The CSVs in `outputs/` are **derived summary statistics** (attractor counts and positions, barrier ratios,
per-window estimates, calibration tables), not participant-level records.

## Reproducing

```bash
pip install numpy pandas scipy scikit-learn
python work/drift_landscape.py selftest        # synthetic calibration, no data needed
python work/drift_landscape.py kossakowski     # needs work/acquired_data/
```

The non-Markovian re-run needs [antiCPy](https://github.com/MartinHessler/antiCPy). It does not install
with a plain `pip install antiCPy`, because its `setup.py` imports the package itself and so runs the whole
runtime import chain during metadata generation:

```bash
pip install matplotlib emcee tqdm ipyparallel celerite
pip install --no-build-isolation antiCPy
```

`work/make_or_break_offline/` and `work/comeasurement_*.py` are dependencies of the analysis scripts,
included so the code here is **byte-identical to what was run** rather than a slimmed-down fork.

## Provenance — one honest limit

The two specifications state that they were frozen before execution, and they were. **They were not
committed to version control before the runs**, so the ordering is documented in the files rather than
independently timestamped. That is a real weakness of this particular deposit and it is stated rather than
glossed. Subsequent frozen specifications in this line of work are committed before they are run.

## Related

- Pre-registered hysteresis test (decline arm ↔ recovery arm), frozen and **un-run** for want of a
  qualifying dataset: doi:[10.5281/zenodo.21366131](https://doi.org/10.5281/zenodo.21366131) — the **concept**
  DOI, which resolves to the current frozen version (v0.2 + Amendment 1 as of 2026-07-30). An earlier
  revision of this README and of the deposited note cite the version DOI `21366132`, which is the
  **2026-07-04 v0.1** and predates Amendment 1. Hysteresis is
  absent from Cui et al.'s framework — the word does not occur in the paper — so that question is
  orthogonal to the classification tested here rather than contained in it.
- Bayesian Langevin estimation: Hessler & Kamps (2025), *Nature Communications*,
  doi:[10.1038/s41467-025-60877-0](https://doi.org/10.1038/s41467-025-60877-0).
- Nonparametric drift/landscape estimation for intensive longitudinal data: Cui, Hasselman &
  Lichtwarck-Aschoff (2023), *Psychological Methods*,
  doi:[10.1037/met0000623](https://doi.org/10.1037/met0000623) (R package `fitlandr`). The estimator here
  is a Python port of the load-bearing estimator, not of the package.

## Citing this

Cite the **note**, not the repository — the note is where the claims and their limits are stated.

> Aizawa, H. (2026). *No alternative stable state at beep scale in one long ESM affect series: a frozen
> drift-field transition-type assignment, its measured power, and a retracted positive finding.* Zenodo.
> https://doi.org/10.5281/zenodo.21703785

**Which DOI.** `10.5281/zenodo.21703785` is the **concept** DOI and always resolves to the latest version —
use it unless you need to pin. `10.5281/zenodo.21703786` is the **version** DOI for v0.3 specifically, which
is what to cite if you are quoting a number that a later revision might change.

## Licence

Code: **MIT** (see [`LICENSE`](LICENSE)). Documents in `outputs/*.md` and the derived CSVs:
**CC BY 4.0**. Derived statistics computed from CC BY-NC source datasets remain subject to those datasets'
own terms.

Author: Hiroaki Aizawa.
