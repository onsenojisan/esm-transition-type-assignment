# The catastrophe flags, from the primary source — and where this project actually sits

**2026-07-30.** The project's operating frame is the catastrophe-flag framework, adopted through a single
secondary source (Helmich et al., 2024). This reads the primary literature the framework comes from.

Source read in full: **van der Maas, H. L. J., & Molenaar, P. C. M. (1992). Stagewise cognitive
development: an application of catastrophe theory.** *Psychological Review*, 99(3), 395–417,
doi:`10.1037/0033-295X.99.3.395`. Obtained as OCR text (125k characters).

**Headline: there are eight flags, they are Gilmore's not van der Maas & Molenaar's, and only three of them
can act as predictors of a transition. Of those three, one is out of reach for observational ESM by
construction, one is the flag the field's own critique has undermined, and one is unexamined here. The
project's predictive ambition therefore rests almost entirely on the single flag that is under attack.**

---

## 1. Two attribution corrections

**The flags are Gilmore's (1981), not van der Maas & Molenaar's.** The paper is explicit:

> a set of mathematically derived criteria to detect discontinuities (Gilmore, 1981) … the correspondence
> between Gilmore's transition criteria, called catastrophe flags, and criteria used in cognitive
> development research

and later, "Each flag is a behavioral property that has been mathematically derived from catastrophe theory
by Gilmore (1981). **Gilmore distinguished eight flags.**" van der Maas & Molenaar are the *psychological
application*, not the derivation. Anyone wanting the derivation needs **Gilmore (1981), Catastrophe Theory
for Scientists and Engineers** — a book, not obtained here.

**Author order: van der Maas first.** Confirmed from PubMed (PMID 1502272: "van der Maas HL, Molenaar PC")
and from the article's own running head. **The UvA institutional repository's cover page reverses it**
("Molenaar, P.C.M.; van der Maas, H.L.J."), and its filename does not. A repository's own metadata was the
unreliable copy — the same shape of trap as the erratum earlier today.

## 2. The eight flags, and the division that matters

Five flags occur when the control variables are **inside** the bifurcation set, and the paper says they
occur **simultaneously** when the system is in transition:

**hysteresis · divergence · sudden jumps · inaccessibility · bimodality**

Three can be manifest **outside** the bifurcation set, and therefore *before* it is entered:

**divergence of linear response · critical slowing down / mode softening · anomalous variance**

> **"Only the last three flags can be used as predictors of transitions because they may occur outside the
> bifurcation set."**

That sentence reorganises how this project should read its own position. The first five are *diagnostic of
being in transition*; only the last three are *anticipatory*. And the paper also states that flag detection
"can be carried out straightforwardly and only requires the availability of behavioral measures" — which is
a weaker requirement than I expected before reading it, and it is worth recording that the expectation was
wrong.

## 3. Where this project actually sits, flag by flag

| Flag | What detection needs | Status here |
|---|---|---|
| **Bimodality** | behavioural marginal | **Done, repeatedly.** `structure_gate`, marginal modality, Haslbeck classifier. Capped below ~6 SD separation |
| **Critical slowing down** | behavioural series | **Done** — and it is the flag Helmich et al.'s critique undermines. *Predictor flag* |
| **Hysteresis** | a control path traversed in **both** directions → a decline arm and a recovery arm | **Frozen preregistration, un-run** for want of a two-arm dataset. Correctly identified as blocked |
| **Sudden jumps** | behavioural series | Partially covered — Olthof et al. (2020) found multiple regime shifts in this project's own series; not tested by the project directly |
| **Inaccessibility** | behavioural marginal — an actually **unvisited** region, not merely two humps | **NOT DONE, and cheap.** See §4 |
| **Divergence** | a splitting/control variable that is **manipulated** (their example: optimal vs suboptimal test conditions) | **Out of reach observationally.** Olthof et al. did measure sensitive dependence on initial conditions on this series |
| **Divergence of linear response** | *"densely sampled time series in which the consequences of **perturbations** can be studied"* | **Out of reach.** Dense series: yes, 1,476 points. Perturbations: none — the same lack that made R-tipping unassignable. *Predictor flag* |
| **Anomalous variance** | behavioural series (probably) | **Not isolated.** Its formal definition did not come out of this OCR cleanly; it plausibly overlaps the variance component of the EWS battery already run. **Do not assume either way.** *Predictor flag* |

## 4. The one new, cheap test: inaccessibility

Inaccessibility is **not** bimodality. Bimodality is two humps in a density; inaccessibility is a region the
system does not occupy — in the cusp, the middle sheet, which "gives rise to an inaccessible mode." A
distribution can be unimodal and still have no gap, or bimodal with the two modes contiguous.

The project has measured bimodality exhaustively and has **never** asked whether there is an unvisited
region. On 1,476 observations of a 7-level item that question is nearly free: a gap test on the marginal, per
item, with a null from the same generators already calibrated.

**Expected outcome is negative**, given ten of eleven marginals fall below the bimodality threshold. That is
not a reason to skip it — a negative on a *distinct* flag adds to the set of flags that have been checked
and come back empty, which is the actual shape of this project's empirical record.

## 5. The finding that matters for the project's position

Sorting §3 by the predictor/diagnostic split:

- **Predictor flags (the only ones that can anticipate a transition): three.**
  - *divergence of linear response* — needs perturbations, **structurally unavailable** in observational ESM
  - *critical slowing down* — **done, and under published critique**; Helmich et al. argue a CSD null may be
    uninterpretable rather than negative, which is what Amendment 1 to the preregistration conceded
  - *anomalous variance* — **unexamined**, status uncertain

> **So the project's entire anticipatory ambition rests on CSD — the one predictor flag the field's own
> critique has undermined — with one alternative permanently out of reach for observational data and one
> never looked at.**

That is a sharper statement of the project's position than anything in the deposited note, and it comes from
one reading of one primary source. It also gives the clearest single reason to examine anomalous variance:
**it is the only unexplored anticipatory flag that observational data might support.**

## 6. What Helmich's three flags were, and what they left out

Helmich et al.'s quoted definition names bimodality/multimodality, hysteresis, and "sensitivity to certain
initial conditions" — which is divergence. **Three of eight, all from the diagnostic five, none from the
predictor three** (CSD enters that review through the EWS discussion rather than as a listed flag).

The review says "include — but are not limited to", so nothing was misrepresented. But a project that
adopted the framework through that sentence inherited **the diagnostic half and none of the anticipatory
half**, and did not know the set had eight members. That is the concrete cost of holding a framework through
a secondary source, and it is the second time today that fetching a primary source changed a position.

## 7. Consequences for the note

- §1's "the cusp-catastrophe literature is not surveyed here" is **wrong** and must be replaced by the
  accurate admission recorded in `note_v04_punch_list_2026-07-30.md` §4.
- The claim that hysteresis is the project's uncontested ground weakens further: it is **one of Gilmore's
  five diagnostic flags**, named by Helmich, and it is *diagnostic rather than anticipatory* — establishing
  it would show a system is in transition, not predict one.
- **Add inaccessibility** to the flags actually tested, and report it whichever way it comes out.
- **Determine anomalous variance's requirements** from Gilmore or a source that states them, and if
  observational data supports it, run it. It is the only unexplored predictor flag.
- The van der Maas juxtaposition in §6 is no longer awkward: Hosenfeld et al. can be cited *as* a
  catastrophe-flag paper, which is what it is, with a co-author who brought the framework into psychology.

---

# 8. Inaccessibility, tested — negative, and the calibration is the interesting part

**Run the same day** (`work/inaccessibility_flag.py`, `inaccessibility_{selftest,kossakowski}_2026-07-30.csv`).

**Operationalisation.** For a Likert item the flag is a support question and can be answered exactly rather
than statistically: are there **two or more disjoint groups of occupied response levels**, separated by at
least one level the system effectively does not visit? A level counts as occupied if its share exceeds
`floor_frac`, swept over 0.000 / 0.002 / 0.005 / 0.010 so nothing rests on one threshold.

## 8.1 Calibration: share of replicates showing the flag (7 levels, T = 1476, 40 reps)

| generator | floor 0.000 | 0.002 | 0.005 | 0.010 |
|---|---:|---:|---:|---:|
| bistable 2 SD | 0.00 | 0.00 | 0.00 | 0.00 |
| bistable 3 SD | 0.00 | 0.00 | 0.00 | 0.00 |
| bistable 4 SD | 0.00 | 0.00 | 0.00 | 0.00 |
| bistable 6 SD | 0.00 | 0.00 | 0.00 | 0.00 |
| **deep well 6 SD** | 0.00 | 0.10 | 0.40 | **0.93** |
| monostable | 0.00 | 0.00 | 0.00 | 0.00 |
| polarized | 0.00 | 0.00 | 0.00 | 0.00 |

Three things fall out.

1. **At a strict floor the test has no power at all.** With 1,476 observations even a deep well eventually
   puts an observation in the middle, so "a truly empty level" is the wrong operationalisation at this
   length. The flag has to be defined against a support threshold, and that threshold is doing the work.
2. **At floor 0.010 the test is sharp**: 93% on the deep well, **0% on all six other generators**, including
   the polarized case that defeats marginal methods. As a detector of a real barrier it is *better* than the
   attractor-count test at the same length (93% vs 80%) and far cheaper.
3. **The project's own bistable generators never show it, at any floor.** Consistent with everything else
   today: at b < 1 the system crosses the middle freely, so it occupies it. Inaccessibility is a
   deep-barrier flag, and those generators have no deep barrier.

## 8.2 Observed: absent, unanimously

Every one of the ten items returns **exactly one occupied group at every floor**. No item has an unvisited
interior level. The flag is absent.

Levels actually used: 7, 7, 7, 6, 6, 6, 6, 6, 6, and **5 for `mood_anxious`** — that unit's sixth appearance
as the anomalous one.

## 8.3 What this adds

A **second, independent, differently-derived flag** now comes back negative on the same series, with
measured power against the case that matters and zero false alarms on six generators including the one built
to defeat marginal methods.

This is not a new result about depression. It is a second line of the same answer, and its value is that the
two lines fail differently: the attractor test reads the *dynamics* and can be defeated by undersampling;
this test reads the *support* and cannot. Both say the same thing.

**Flags now checked on this series: bimodality (negative), critical slowing down (done, contested),
inaccessibility (negative).** Three of Gilmore's eight. Hysteresis remains frozen and un-run; divergence and
divergence of linear response need perturbations the data does not contain; sudden jumps is partially
covered by others' work on this series; anomalous variance is next.
