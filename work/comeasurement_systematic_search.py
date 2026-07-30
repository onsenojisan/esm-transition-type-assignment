"""Systematic search for the co-measurement gap note (§8's outstanding step).

Runs a block-structured search across PubMed (E-utilities) and Europe PMC for
each of the four paradigm legs, deduplicates, and writes the record set plus a
per-block count table for PRISMA-style reporting.

The predicate is fixed in §1 of the note and is NOT re-fitted here:
  (1) same individual, longitudinally
  (2) perturbation with a decline arm AND a recovery arm
  (3) a felt / experienced valence signal
  (4) an INDEPENDENT viability endpoint, not derived from (3)

Each leg searches for the conditions that leg could plausibly carry, deliberately
broad: the point is to surface candidates for screening, not to pre-filter to the
answer. Recall is preferred over precision at this stage.

Usage:  python work/comeasurement_systematic_search.py
Writes: outputs/comeasurement_systematic_search_<date>_{counts,records}.csv
        outputs/comeasurement_systematic_search_<date>_strategy.md

No API key required. Rate-limited to stay inside NCBI's anonymous 3 req/s.
"""

import csv
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

UA = "vot-empirical-workbench/1.0 (research gap audit; mailto:thepleasureorder@gmail.com)"
OUT = Path(__file__).resolve().parent.parent / "outputs"
TODAY = date.today().isoformat()

# --------------------------------------------------------------------------
# Blocks. Written once, here, so the strategy file below is generated from the
# same strings that are actually run -- the reproducibility failure this whole
# exercise exists to avoid.
# --------------------------------------------------------------------------

INDIVIDUAL = (
    '"within-person"[tiab] OR "within-subject"[tiab] OR "intensive longitudinal"[tiab] '
    'OR "repeated measures"[tiab] OR "single-case"[tiab] OR "n-of-1"[tiab] '
    'OR "same individual"[tiab] OR "individual trajector*"[tiab]'
)
RECOVERY = (
    'recovery[tiab] OR remission[tiab] OR rebound[tiab] OR relapse[tiab] OR reversal[tiab] '
    'OR "return to baseline"[tiab] OR resilience[tiab] OR hysteresis[tiab] '
    'OR "critical slowing"[tiab] OR "tipping point"[tiab] OR "early warning signal*"[tiab] '
    'OR "regime shift"[tiab] OR "alternative stable state*"[tiab]'
)
FELT = (
    '"ecological momentary assessment"[tiab] OR "experience sampling"[tiab] '
    'OR "ambulatory assessment"[tiab] OR "daily diary"[tiab] OR affect[tiab] OR mood[tiab] '
    'OR valence[tiab] OR anhedonia[tiab] OR "sucrose preference"[tiab] '
    'OR "hedonic state"[tiab] OR wellbeing[tiab] OR "well-being"[tiab]'
)
VIABILITY = (
    'survival[tiab] OR mortality[tiab] OR lifespan[tiab] OR longevity[tiab] OR telomere*[tiab] '
    'OR "immune function"[tiab] OR "physiological reserve"[tiab] OR frailty[tiab] '
    'OR "behavioral flexibility"[tiab] OR "behavioural flexibility"[tiab] OR actigraph*[tiab] '
    'OR "functional outcome*"[tiab] OR "objective outcome*"[tiab] OR biomarker*[tiab]'
)
PERTURB = (
    'perturbation[tiab] OR "chronic stress"[tiab] OR "chronic mild stress"[tiab] '
    'OR challenge[tiab] OR stressor[tiab] OR intervention[tiab] OR manipulation[tiab] '
    'OR withdrawal[tiab] OR tapering[tiab] OR discontinuation[tiab]'
)
ANIMAL = (
    'mice[tiab] OR mouse[tiab] OR rat[tiab] OR rats[tiab] OR rodent*[tiab] OR primate*[tiab] '
    'OR bird*[tiab] OR "wild population*"[tiab] OR zebrafish[tiab] OR animal*[tiab]'
)
APPRAISAL = (
    'appraisal[tiab] OR coping[tiab] OR "emotion regulation"[tiab] OR "defense style"[tiab] '
    'OR "defence style"[tiab] OR "sense of coherence"[tiab] OR reappraisal[tiab]'
)

LEGS = {
    # NOTE (search development, recorded rather than hidden): the first run of L1
    # omitted the `individual` block and returned 8,738 PubMed hits -- too many to
    # screen, and unfaithful to the predicate, whose condition (1) is exactly
    # within-person structure. Adding it is a correction toward the predicate, not
    # a narrowing chosen after seeing results.
    "L1_human_ESM": {
        "label": "Human intensive longitudinal self-report (ESM/EMA)",
        "blocks": [("felt", FELT), ("individual", INDIVIDUAL), ("recovery", RECOVERY), ("viability", VIABILITY)],
    },
    "L2_animal": {
        "label": "Animal physiology / behaviour",
        "blocks": [("animal", ANIMAL), ("felt", FELT), ("recovery", RECOVERY), ("viability", VIABILITY)],
    },
    "L3_appraisal": {
        "label": "Appraisal / coping psychology",
        "blocks": [("appraisal", APPRAISAL), ("individual", INDIVIDUAL), ("recovery", RECOVERY), ("viability", VIABILITY)],
    },
    "L4_viability": {
        "label": "Viability-indicator studies",
        "blocks": [("viability", VIABILITY), ("felt", FELT), ("individual", INDIVIDUAL), ("perturb", PERTURB)],
    },
}


def _get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001 - transient API failures are expected
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))
    return None


def pubmed_count(term):
    u = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
         "?db=pubmed&retmode=json&retmax=0&term=" + urllib.parse.quote(term))
    time.sleep(0.4)
    return int(_get(u)["esearchresult"]["count"])


def pubmed_ids(term, retmax=2000):
    u = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
         f"?db=pubmed&retmode=json&retmax={retmax}&term=" + urllib.parse.quote(term))
    time.sleep(0.4)
    return _get(u)["esearchresult"].get("idlist", [])


def pubmed_summaries(pmids):
    out = []
    for i in range(0, len(pmids), 200):
        chunk = pmids[i:i + 200]
        u = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
             "?db=pubmed&retmode=json&id=" + ",".join(chunk))
        time.sleep(0.4)
        res = _get(u).get("result", {})
        for pid in chunk:
            r = res.get(pid)
            if not r:
                continue
            doi = ""
            for aid in r.get("articleids", []):
                if aid.get("idtype") == "doi":
                    doi = aid.get("value", "")
            out.append({
                "source": "pubmed", "id": pid, "doi": doi,
                "year": (r.get("pubdate") or "")[:4],
                "journal": r.get("fulljournalname", ""),
                "title": r.get("title", ""),
            })
    return out


def europepmc(term, page_size=1000, max_pages=3):
    out, cursor = [], "*"
    for _ in range(max_pages):
        u = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json"
             f"&pageSize={page_size}&cursorMark={urllib.parse.quote(cursor)}"
             "&query=" + urllib.parse.quote(term))
        time.sleep(0.4)
        d = _get(u)
        for r in d.get("resultList", {}).get("result", []):
            out.append({
                "source": "europepmc", "id": r.get("id", ""), "doi": r.get("doi", ""),
                "year": str(r.get("pubYear", "")), "journal": r.get("journalTitle", ""),
                "title": r.get("title", ""),
            })
        nxt = d.get("nextCursorMark")
        if not nxt or nxt == cursor:
            break
        cursor = nxt
    return out


def epmc_term(blocks):
    """Europe PMC uses a different field syntax; translate the [tiab] blocks."""
    parts = []
    for _, b in blocks:
        terms = re.findall(r'"[^"]+"|\S+\[tiab\]', b)
        cleaned = [t.replace("[tiab]", "") for t in terms]
        parts.append("(" + " OR ".join(f"(TITLE_ABS:{t})" for t in cleaned if t) + ")")
    return " AND ".join(parts)


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", "", (t or "").lower())[:120]


def main():
    OUT.mkdir(exist_ok=True)
    counts, records, seen = [], [], set()

    for leg, cfg in LEGS.items():
        blocks = cfg["blocks"]
        # cumulative counts, so the funnel is visible for PRISMA reporting
        for i in range(1, len(blocks) + 1):
            term = " AND ".join(f"({b})" for _, b in blocks[:i])
            c = pubmed_count(term)
            counts.append({
                "leg": leg, "label": cfg["label"], "database": "pubmed",
                "blocks": "+".join(n for n, _ in blocks[:i]), "hits": c,
            })
            print(f"  {leg:14s} pubmed {'+'.join(n for n,_ in blocks[:i]):40s} {c:7d}")

        full = " AND ".join(f"({b})" for _, b in blocks)
        got = pubmed_summaries(pubmed_ids(full))
        try:
            epmc = europepmc(epmc_term(blocks))
        except Exception as e:  # noqa: BLE001
            print(f"    (europepmc failed for {leg}: {e})")
            epmc = []
        counts.append({
            "leg": leg, "label": cfg["label"], "database": "europepmc",
            "blocks": "all", "hits": len(epmc),
        })
        print(f"  {leg:14s} europepmc {'all':38s} {len(epmc):7d}")

        for r in got + epmc:
            key = (r["doi"] or "").lower() or norm_title(r["title"])
            if not key or key in seen:
                continue
            seen.add(key)
            r["leg"] = leg
            records.append(r)

    with open(OUT / f"comeasurement_systematic_search_{TODAY}_counts.csv", "w",
              newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["leg", "label", "database", "blocks", "hits"])
        w.writeheader()
        w.writerows(counts)

    with open(OUT / f"comeasurement_systematic_search_{TODAY}_records.csv", "w",
              newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["leg", "source", "id", "doi", "year", "journal", "title"])
        w.writeheader()
        w.writerows(records)

    print(f"\nunique records after dedup: {len(records)}")
    return counts, records


if __name__ == "__main__":
    main()
