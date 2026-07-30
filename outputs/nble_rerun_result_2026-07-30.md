# NBLE re-run — result

**2026-07-30.** The moving-well result was produced by a Markovian estimator, and Bayesian Langevin
estimation was named as the proper non-Markovian instrument. antiCPy 1.0.0 now installs (recipe in §1), so
this re-runs the question under it.

**Headline: NBLE does not answer the moving-well question, and this was established before looking at the
data. Twice, in two configurations, its reported outputs fail to separate a moving well from a static one.
The Markovian result therefore stands — not because it was confirmed, but because NBLE measures something
else.**

**What NBLE does supply is the project's first measurement of local stability under a correlated-noise
model. It is reported here descriptively and it does not survive as a finding.**

---

## 1. The install, since it was recorded as impossible

The earlier diagnosis ("fails to build; numpy missing at build time; backend unavailable") was wrong. The
real cause is that `setup.py` line 4 runs `import antiCPy`, so the whole runtime import chain executes
during metadata generation, one missing module at a time.

```
pip install matplotlib emcee tqdm ipyparallel celerite
pip install --no-build-isolation antiCPy
```

numpy and scipy were already present. antiCPy **1.0.0** installs and imports.

## 2. NBLE does not separate a moving well from a static one

Checked before running on data, on the same generators used to calibrate the Markovian instrument
(T = 1476, φ = 0.30, 6 reps per cell, window 250 / shift 50).

| configuration | travel | θ₅ (hidden OU) | ζ (drift slope) |
|---|---:|---:|---:|
| default | 0 SD | 1.129 | −0.894 |
| default | 3 SD | **1.134** | **−0.914** |
| time-scale separation prior, `slow_process='Y'`, factor 10 | 0 SD | 2.704 | −1.374 |
| time-scale separation prior | 3 SD | **2.741** | **−1.337** |

Enabling the documented slow-hidden-process prior shifts both quantities but leaves the two conditions
indistinguishable.

**The reason is structural, not a tuning failure.** A moving well puts its signal in the *between-window*
displacement of the operating point. NBLE fits a stationary model *within* each window: a well travelling
3 SD across 1476 points moves 0.5 SD inside a 250-point window, which the third-order polynomial absorbs as
a small shift of its fixed point while ζ, ψ and θ₅ stay put. The per-window fixed point is the quantity that
carries it, and `fast_MAP_resilience_scan` does not store it.

**Consequences, stated plainly:**

- `drift_landscape_windowed.py` is **not superseded**. The two instruments answer different questions.
- The moving-well result (`mood_lonely` ≈ 4.5 local SDs, `mood_guilty` ≈ 4, `mood_down` ≈ 1.4) is
  **neither confirmed nor refuted** by this run. It remains a Markovian measurement.
- **θ₅ measured on the data carries no information about the moving-well question.** Since θ₅ ≈ 1.13 under
  both travel 0 and travel 3, a small θ₅ in the real data cannot be read as "no slow hidden variable." That
  inference is unavailable and must not be drawn.

## 3. What NBLE did measure: stability on Kossakowski

All 11 units z-scored, window 250, shift 50, 25 overlapping windows, MAP scan.
ζ < 0 is a restoring rate; closer to zero is less stable.

| unit | AR(1) | ζ median | ζ sd | ζ first → last | trend r | ψ | θ₅ |
|---|---:|---:|---:|---:|---:|---:|---:|
| mood_satisfi | 0.350 | −1.351 | 0.080 | −1.351 → −1.159 | +0.85 | 1.475 | 1.468 |
| mood_enthus | 0.336 | −1.230 | 0.044 | −1.230 → −1.190 | −0.23 | 1.445 | 1.456 |
| mood_cheerf | 0.345 | −1.190 | 0.070 | −1.190 → −1.251 | +0.26 | 1.382 | 1.492 |
| _composite | 0.159 | −1.146 | 0.110 | −1.186 → −0.926 | **+0.89** | 1.198 | 1.258 |
| mood_down | 0.436 | −1.134 | 0.057 | −1.134 → −1.050 | −0.19 | 1.566 | 1.469 |
| mood_strong | 0.355 | −1.084 | 0.050 | −1.084 → −0.955 | +0.61 | 1.309 | 1.407 |
| mood_relaxed | 0.265 | −1.075 | 0.066 | −1.051 → −1.259 | −0.91 | 1.348 | 1.414 |
| mood_guilty | 0.259 | −1.042 | 0.052 | −1.042 → −0.950 | −0.20 | 1.311 | 1.297 |
| mood_lonely | 0.324 | −0.963 | 0.057 | −0.963 → −0.776 | +0.73 | 1.130 | 1.352 |
| mood_irritat | 0.258 | −0.944 | 0.068 | −0.906 → −1.113 | −0.88 | 1.153 | 1.236 |
| **mood_anxious** | 0.223 | **+0.335** | **0.194** | +0.335 → +0.233 | +0.22 | 1.234 | 1.284 |

### 3.1 Read with the frozen spec's constraint

`transition_type_assignment_spec_v1.md` §5 put Q2 (B-tipping vs N-tipping) out of scope on the ground that
**it has no referent unless Q1 finds a discrete transition**, and Q1 found none. That constraint applies to
this table. A ζ trend here is a stability trajectory; it is **not** an approach to a bifurcation, because
there is no second state to approach.

### 3.2 The trends do not survive, and are reported as descriptive only

Windows overlap heavily (size 250, shift 50), so 25 windows carry roughly **6 independent spans**. No
p-values were computed and none should be. The directions are mixed: four units and the composite drift
toward less stable (satisfi, strong, lonely, composite), two toward more stable (relaxed, irritat), the rest
flat. The composite's ζ moves −1.186 → −0.926, a 22% loss of restoring rate — relaxation time 0.84 → 1.08
observations, which is small in absolute terms.

**Eleven units, mixed signs, ~6 independent spans: this is not a finding.** It is recorded so it can be
pre-registered elsewhere.

### 3.3 mood_anxious returns a positive ζ, and it is most parsimoniously an artifact

ζ = **+0.335** means the estimated fixed point is *repelling*. Its ζ sd (0.194) is 3–4× every other unit's.

This is the third time this unit has come out anomalous, and the previous two explain it: it has **five
response levels over a truncated range (−3 to 1)**, it carries the only bimodality coefficient above 0.555
(0.659), and it was the **most static** unit in the windowed run (travel ratio 0.026). A cubic drift fitted
to a heavily discretised, truncated variable is under-determined. **Reported as an anomaly attributable to
that item's measurement scale, not as an unstable state.**

### 3.4 One thing that is uniform, and is worth keeping

θ₅ ≈ 1.24–1.49 in every unit, ψ ≈ 1.13–1.57, coupling ≈ 1.05–1.44. There **is** a correlated-noise component
in all 11 series, so `drift_landscape.py`'s Markov assumption is not exactly satisfied. Its timescale is
short (~1.3 observations), which makes it unlikely to have moved the attractor-count result — but see §2:
θ₅'s value cannot be used to argue about slow hidden structure either way.

## 4. Net effect

- The moving-well finding stays where it was: **a Markovian measurement, unreplicated, in 3 of 11 units.**
- The B-vs-N axis has its first instrument and its first numbers, and the spec's own constraint says they
  cannot be read as tipping-related.
- **Still no second attractor, and now also no configuration of a published non-Markovian estimator that
  finds one.**
- What would actually move this: the per-window fixed point under NBLE, which the fast MAP path does not
  store. Extracting it — via `perform_MAP_resilience_scan` or the per-window `theta` — is the one concrete
  route to a non-Markovian version of the moving-well test, and it is not done here.
