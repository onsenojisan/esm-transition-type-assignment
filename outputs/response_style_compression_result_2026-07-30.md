Result: **the null is weaker than the deposited note states.** A 20% central-tendency compression takes a
well-separated bistable system from 100% detection to 5%. The note's headline power figures were measured
with no response-style distortion at all.

# Response-style compression can erase a second attractor

**2026-07-30.** Punch-list item 1 — the gap between the deposited note's largest stated threat (§7, response
style) and its main claim (§4, 66/66 single attractors). The note asserts that degeneracy cannot manufacture
a second attractor. It never asked whether a response style can **remove** one.

Instrument: `work/response_style_compression.py`. Table: `response_style_compression_2026-07-30.csv`.

---

## 1. What was simulated

Central-tendency bias — the respondent avoids the ends of the scale. For latent z in SD units and
compression c ∈ (0, 1]:

> z_reported = **c · z**, then binned onto a **fixed** 7-level scale with anchors at ±3 SD

**The fixed grid is the whole point.** Compressing and then re-binning on the *observed* range would rescale
the compression away. A real Likert item has fixed anchors, so mass genuinely migrates toward the centre
levels and two wells can merge into one. c = 1.0 is no compression.

## 2. Detection of ≥ 2 attractors, by compression (T = 1476, bw 1.4, 40 reps)

| generator | c = 1.0 | **0.8** | 0.6 | 0.5 | 0.4 | 0.3 |
|---|---:|---:|---:|---:|---:|---:|
| bistable 4 SD | 0.03 | 0.00 | 0.00 | 0.00 | 0.00 | 0.03 |
| **bistable 6 SD** | **1.00** | **0.05** | 0.00 | 0.00 | 0.00 | 0.03 |
| **deep well 6 SD** | **0.68** | 0.47 | 0.15 | **0.00** | 0.00 | 0.00 |
| monostable — false alarm | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.07 |
| polarized — false alarm | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

**A 20% compression is enough.** The 6 SD case goes from certain detection to 5%. A genuine deep-barrier
system survives longer but is gone by 50% compression.

False alarms stay at zero throughout, so compression does not create spurious attractors — it only destroys
real ones. That asymmetry is the finding: **compression is a pure false-negative mechanism**, which is
exactly the direction the deposited note does not consider.

## 3. A confound that must be stated first, because it bounds the claim

**The c = 1.0 baselines here differ from the note's calibration**, and the reason is a grid convention, not
compression:

| | note's calibration | here |
|---|---|---|
| discretisation | 7 levels spanning the **observed range** | 7 levels on a **fixed ±3 SD** grid |
| bistable 4 SD at c = 1.0 | 0.925 | **0.03** |
| deep well at c = 1.0 | 0.80 | **0.68** |

On a fixed-anchor grid the 4 SD wells (at ±2 SD) fall into adjacent bins and are unresolvable before any
compression is applied. So:

- **within-row** decline (1.00 → 0.05 for 6 SD at c = 0.8) is the compression effect, and the grid
  convention cancels
- **between-convention** differences at c = 1.0 are the grid, and they are large

**Neither convention is obviously right.** A real item has fixed anchors, which favours this one; but the
Kossakowski items actually use 6–7 of their levels, which is closer to range-matched. The two bracket the
answer, and **the note reports only one of them without saying it is a choice.** That is a second, smaller
defect found by this run.

## 4. Consequence for the deposited note

Punch-list item 1 set out two branches. **The unfavourable one obtained.**

> detection collapses at compressions plausible for symptom items → **the null is weaker than v0.3 states,
> and the note must say so**

The note's power claims — 80% against a deep well, 92.5–100% against 4–6 SD separation, 2.5% false alarms —
are all measured **with no response-style distortion**. Central-tendency bias is a documented and ordinary
property of Likert self-report. Under a modest amount of it, those figures do not survive.

**The corrected form of the main claim:**

> No second attractor was found. The instrument has 80–100% power against well-separated bistability
> **in the absence of response-style compression**, and that power collapses under a 20% central-tendency
> compression — to 5% for a 6 SD separation. The null is therefore informative about systems whose
> respondents used the scale without substantial central-tendency bias, and **uninformative about systems
> whose respondents did not.** Whether this participant did is not established here.

That is a materially weaker claim than the one deposited, and it should be carried into v0.4 as the primary
correction rather than as a limitation bullet.

## 5. It also qualifies the inaccessibility result

The same runs carried the inaccessibility flag. On the fixed-anchor grid the deep well shows it in only
**0.10** of replicates at c = 1.0, against **0.93** under range-matched discretisation the same day.

So §8's "93% power, better than the attractor test" is **convention-dependent and does not hold on a
fixed-anchor scale**. The inaccessibility negative on the observed data stands — those items do use 6–7
levels, which is the range-matched regime — but the power claim attached to it must be stated with the
convention named.

## 6. What is not established

- **Whether this participant's responses are compressed.** Nothing here measures that. The three degenerate
  items (67–84% on one level) are *concentrated*, but concentration produced by a genuinely quiet symptom is
  not the same as compression produced by a response style, and this run does not separate them. That
  separation is the next question and it is not answered.
- **Whether compression of this severity is typical.** The 20% figure is where detection breaks, not an
  estimate of what respondents do.
- One analyst, one compression model (linear central-tendency), one series length.
