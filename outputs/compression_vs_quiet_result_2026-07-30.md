# Compression, quiet symptom, or default? — the mechanism is not separated, and it does not matter

**2026-07-30.** Follow-up to `response_style_compression_result_2026-07-30.md` §6, which showed a 20%
central-tendency compression destroys detection of a second attractor and explicitly did **not** establish
whether this participant's responses are compressed.

**Result: three candidate mechanisms were tested and none is established. But the attempt produced a
mechanism-agnostic number that settles the practical question — the four concentrated items deliver
1.4–2.8 effective response levels, and no latent structure at ±2 SD is resolvable at that resolution
whatever the reason for it.**

---

## 1. What the codebook says, and how it refuted the first hypothesis

The hypothesis was that concentration at 0 on the `−3 … 3` items is a *floor* — the symptom is usually
absent. **The codebook refutes it** (`work/acquired_data/kossakowski/ESMdata/Codebook.pdf`):

> `mood_lonely` — I feel lonely — **−3 (not) … 3 (very)**
> `mood_down` — I feel down — **−3 (not) … 3 (very)**
> `mood_relaxed` — I feel relaxed — **1 (not) … 7 (very)**

**−3 is "not at all", not the opposite pole.** So 0 is not a neutral midpoint of a bipolar scale; it is the
middle of a not→very intensity scale. The absence anchor is −3, and it is used in **0.2%** of observations
while 0 takes **83.6%**. The person almost never reports "not lonely at all" and almost always reports the
middle.

## 2. The pattern that suggested an instrument default

Every item's modal response sits at or beside its own scale midpoint:

| item | scale | mode | midpoint | modal share |
|---|---|---:|---:|---:|
| mood_anxious | −3…3 | 0 | 0 | 0.909 |
| mood_lonely | −3…3 | 0 | 0 | 0.836 |
| mood_guilty | −3…3 | 0 | 0 | 0.817 |
| mood_down | −3…3 | 0 | 0 | 0.668 |
| mood_relaxed | 1…7 | 4 | 4 | 0.484 |
| mood_cheerf / enthus / strong | 1…6/7 | 4 | 4 | 0.372–0.401 |
| mood_satisfi | 1…6 | 5 | 3.5 | 0.405 |

The project has recorded this shape before, for another dataset: *"Fisher's floor mass … and its **slider
initialised at 50**."* A midpoint default would produce exactly this.

## 3. Two tests, both negative for the default hypothesis

**Co-occurrence — not diagnostic.** All eight items at their midpoint simultaneously: observed 9.1% against
1.2% under independence, an 8× excess; 42.8% of beeps have ≥6 of 8 at midpoint. **This does not
discriminate.** Mood items are genuinely correlated — someone who is not down is also not lonely and is
relaxed — so the independence null is the wrong baseline and an 8× excess is consistent with both a default
and with real covariation. Recorded as uninformative rather than as support.

**Response time — the decisive test, and it comes back negative.** If the midpoints were a default, beeps
left at default should be markedly faster.

| items at midpoint | n | median duration |
|---|---:|---:|
| 0–2 | 208 | **94 s** |
| 3–4 | 363 | 91 s |
| 5–6 | 522 | 88 s |
| 7–8 | 379 | **86 s** |

Monotone, in the predicted direction, and **statistically significant** (Mann–Whitney p = 2.2 × 10⁻⁶,
Spearman ρ = −0.141). And **far too small to mean non-response**: 8 seconds on a 90-second questionnaire,
about 9%. Leaving sliders untouched would save most of the interaction, not a twelfth of it. A 9% saving is
what an uneventful moment produces because there is less to weigh.

**So: not a default.** With n = 1,472 a trivial effect reaches significance, and this one is trivial.

## 4. The mechanism remains unseparated — stated plainly

Central-tendency compression and genuinely middling responding are **not** distinguished by anything here.
The codebook makes "compression" the less natural description — on a not→very scale, answering 0 is
reporting a middling level rather than avoiding an extreme, and the person does use −1 and +1 on both sides
— but that is an interpretive argument, not a measurement.

A model comparison was attempted (simulate compression and a quiet symptom, each tuned to the observed modal
share, and ask which reproduces end-use and skew). **It failed to discriminate because neither model fits**:
both put 8–100% of mass at the scale ends where the data has 0.1–0.5%. Reported as a failed test, not as a
result.

## 5. The number that does settle the practical question

Effective number of response levels used, exp(entropy of the level distribution):

| item | levels on the scale | levels with ≥1% | **effective levels** |
|---|---:|---:|---:|
| mood_anxious | 5 | 2 | **1.39** |
| mood_lonely | 7 | 4 | **1.86** |
| mood_guilty | 6 | 3 | **1.90** |
| mood_down | 7 | 5 | **2.75** |
| mood_relaxed | 7 | 4 | 3.03 |
| mood_cheerf / enthus / strong | 6 | 4–5 | 3.35–3.49 |
| mood_satisfi | 6 | 5 | 3.87 |
| mood_irritat | 7 | 5 | **4.24** |

**The four negative-affect items deliver between 1.4 and 2.8 distinguishable values.** `mood_anxious`
carries less than one and a half.

> **Whatever produced it — compression, middling responding, or a genuinely quiet fortnight — an item that
> yields ~2 distinct values cannot resolve two attractors separated by 2 SD.** The mechanism question is
> interesting and unresolved; the measurement question is neither.

That is mechanism-agnostic, it is measured rather than modelled, and it is the form the correction should
take in v0.4: **report effective levels per item, and treat items below ~3 as unable to support drift-field
estimation regardless of why.**

Note that `mood_irritat`, at 4.24 effective levels and with a genuine floor pile (29.7% at the "not"
anchor), is the **best-resolved** item in the set and the only one whose concentration has the shape of a
real floor. It was discounted earlier on exactly that ground — which now looks like the wrong reason to
discount it.

## 6. What is still not known

- Whether this participant compressed. Not established, and this line of testing has been exhausted with
  the data available.
- Whether other ESM datasets show the same midpoint concentration. Not checked; it would say whether this
  is a property of this person, this instrument, or the method.
- The response-time effect is real and small. It is *consistent with* less deliberation on uneventful
  beeps, and that reading is not tested against alternatives.
