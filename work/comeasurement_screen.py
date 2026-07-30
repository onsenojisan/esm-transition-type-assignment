"""First-pass abstract screen against the four-condition predicate.

THIS IS A FIRST-PASS SCREEN, NOT A SECOND INDEPENDENT SCREENER, and it is
rule-based: it detects whether each condition is *mentioned* in title+abstract,
which is not the same as assessing whether the study's design satisfies it. Its
job is to produce an auditable shortlist small enough to read closely, and to
record a specific reason for every exclusion so the screen can be checked.

Decision rule, applied to title + abstract:
  INCLUDE-for-reading  if all four conditions are detected
  EXCLUDE              otherwise, recording which condition(s) were absent

Condition 2 requires BOTH a decline/perturbation direction AND a recovery/return
direction, because the predicate needs both arms; a paper mentioning only one is
not a candidate.

Condition 4 additionally records whether the viability evidence found is of an
*independent* kind (observed behaviour, physiology, records, survival) or only of
a self-report kind. The latter is the recurring failure the note identifies, so
those are shortlisted separately rather than counted as satisfying (4).

Usage:  python work/comeasurement_screen.py [YYYY-MM-DD]
"""

import csv
import re
import sys
from datetime import date
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "outputs"
TODAY = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()

C1 = [  # same individual, longitudinally
    r"within[- ]person", r"within[- ]subject", r"within[- ]individual", r"intensive longitudinal",
    r"repeated measure", r"single[- ]case", r"n[- ]of[- ]1", r"same (individual|animal|subject|mice|rat)",
    r"idiographic", r"longitudinal", r"time[- ]series", r"follow[- ]?up", r"prospective(ly)? follow",
    r"each (participant|individual|animal|subject)", r"per[- ](participant|individual|animal)",
]
C2_DOWN = [  # a decline arm
    r"chronic (mild )?stress", r"stressor", r"perturbation", r"challenge", r"deteriorat",
    r"decline", r"decrease", r"worsen", r"deteriorate", r"induc(e|ed|tion)", r"depriv",
    r"withdraw", r"taper", r"discontinu", r"relapse", r"onset", r"exacerbat", r"impair",
]
C2_UP = [  # a recovery arm
    r"recover", r"remission", r"remit", r"rebound", r"reversal", r"revers(e|ed)",
    r"return(ed)? to baseline", r"restor", r"resilien", r"improv", r"rehabilitat",
    r"treatment response", r"normali[sz]", r"re[- ]establish",
]
C3 = [  # felt / experienced valence signal
    r"\baffect\b", r"affective", r"\bmood\b", r"valence", r"anhedoni", r"sucrose preference",
    r"hedonic", r"well[- ]?being", r"emotion", r"experience sampling", r"ecological momentary",
    r"ambulatory assessment", r"daily diary", r"subjective (state|experience|feeling)",
    r"self[- ]reported (mood|affect|feeling)", r"depressive symptom", r"positive affect",
    r"negative affect",
]
C4_INDEP = [  # viability endpoint, independent of self-report
    r"survival", r"mortalit", r"lifespan", r"longevity", r"telomere", r"immune function",
    r"inflammat", r"cortisol", r"physiological reserve", r"frailty index", r"grip strength",
    r"gait speed", r"actigraph", r"accelerometer", r"behaviou?ral flexibilit",
    r"hospitali[sz]ation", r"medical record", r"biomarker", r"physiologic",
    r"objective(ly)? (measured|assessed)", r"body weight", r"corticosterone",
]
C4_SELFREPORT = [  # "outcome" that is another self-report -- flagged, not counted
    r"quality of life", r"social functioning", r"self[- ]rated health", r"questionnaire",
    r"symptom (score|severity|scale)", r"self[- ]report",
]


def find(pats, text):
    return sorted({m.group(0).lower()
                   for p in pats
                   for m in re.finditer(p, text, flags=re.I)})


def main():
    src = OUT / f"comeasurement_systematic_search_{TODAY}_abstracts.csv"
    rows = list(csv.DictReader(open(src, encoding="utf-8")))

    screened, shortlist = [], []
    for r in rows:
        text = re.sub(r"<[^>]+>", " ", f"{r['title']} {r['abstract']}")
        c1 = find(C1, text)
        down, up = find(C2_DOWN, text), find(C2_UP, text)
        c3 = find(C3, text)
        c4i, c4s = find(C4_INDEP, text), find(C4_SELFREPORT, text)

        met = {"c1": bool(c1), "c2": bool(down) and bool(up), "c3": bool(c3), "c4": bool(c4i)}
        missing = [k for k, v in met.items() if not v]

        if not r["abstract"]:
            decision, reason = "NO_ABSTRACT", "no abstract retrieved; needs manual check"
        elif not missing:
            decision, reason = "READ", "all four conditions mentioned"
        else:
            decision = "EXCLUDE"
            names = {"c1": "no within-individual structure", "c2": "no decline+recovery pair",
                     "c3": "no felt signal", "c4": "no independent viability endpoint"}
            reason = "; ".join(names[m] for m in missing)

        rec = {**{k: r[k] for k in ["leg", "source", "id", "doi", "year", "journal", "title"]},
               "decision": decision, "reason": reason,
               "c1": "; ".join(c1[:6]), "c2_decline": "; ".join(down[:6]),
               "c2_recovery": "; ".join(up[:6]), "c3": "; ".join(c3[:6]),
               "c4_independent": "; ".join(c4i[:6]), "c4_selfreport_only": "; ".join(c4s[:6])}
        screened.append(rec)
        if decision in ("READ", "NO_ABSTRACT"):
            shortlist.append({**rec, "abstract": r["abstract"]})

    with open(OUT / f"comeasurement_systematic_search_{TODAY}_screened.csv", "w",
              newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(screened[0].keys()))
        w.writeheader()
        w.writerows(screened)

    with open(OUT / f"comeasurement_systematic_search_{TODAY}_shortlist.csv", "w",
              newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(shortlist[0].keys()))
        w.writeheader()
        w.writerows(shortlist)

    from collections import Counter
    print("decisions:", dict(Counter(s["decision"] for s in screened)))
    print("\nexclusion reasons (top):")
    for reason, n in Counter(s["reason"] for s in screened if s["decision"] == "EXCLUDE").most_common(8):
        print(f"  {n:5d}  {reason}")
    print("\nshortlist by leg:", dict(Counter(s["leg"] for s in shortlist)))
    print(f"shortlist size: {len(shortlist)}")


if __name__ == "__main__":
    main()
