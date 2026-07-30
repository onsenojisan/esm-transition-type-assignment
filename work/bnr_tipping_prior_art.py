"""Targeted prior-art scan: the B/N/R tipping partition, and whether it has been
applied to psychological within-person time series.

Spec is frozen in outputs/bnr_prior_art_search_spec_v1.md. Blocks, screening rule
and outcome statements were fixed BEFORE this ran; nothing here may be edited to
change what the run returns without superseding that spec in a v1.1.

Why this scan exists
--------------------
The project is considering replacing "the fold is the universal mechanism of
collapse" with "the set of collapse mechanisms is a closed classification, and
様式 patterns map onto it". The outcome side of that map already exists in
outputs/l4_generic_change_distinction_note_v0.1.md. The mechanism side appears to
be the bifurcation-induced / noise-induced / rate-induced partition, which returns
ZERO hits on grep across this repository.

Three legs (spec §3):
    P1  MECH AND TIP AND PSYCH   -- has it been applied to psychology
    P2  MECH AND TIP AND WITHIN  -- applied to any within-person / time series
    P3  MECH AND TIP             -- counts only, to size it and find the source

Screening (spec §4): S1 requires >= 2 of the three mechanism families named, because
the claim at stake is about the PARTITION. One mechanism alone is prior art for one
cell, not for the classification.

Usage:  python work/bnr_tipping_prior_art.py
Writes: outputs/bnr_prior_art_<date>_{counts,screened}.csv

No API key required. Rate-limited to stay inside NCBI's anonymous 3 req/s.
"""

import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

try:                                    # Windows console is cp932; titles are not
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "outputs"
TODAY = date.today().isoformat()
UA = "vot-empirical-workbench/1.0 (prior-art scan; mailto:thepleasureorder@gmail.com)"

sys.path.insert(0, str(HERE))
from comeasurement_systematic_search import (  # noqa: E402
    _get, pubmed_count, pubmed_ids, europepmc, norm_title,
)

# --------------------------------------------------------------------------
# Blocks -- frozen, spec v1.0 section 3. Written once here so the counts table
# is generated from the same strings that are actually run.
# --------------------------------------------------------------------------
MECH_TERMS = ['"rate-induced"', '"rate induced"', '"rate-dependent"', '"noise-induced"',
              '"noise induced"', '"bifurcation-induced"', '"bifurcation induced"',
              '"B-tipping"', '"N-tipping"', '"R-tipping"']
TIP_TERMS = ['tipping', '"critical transition"', '"critical transitions"', '"regime shift"',
             '"regime shifts"', 'bifurcation', 'attractor', '"alternative stable states"',
             '"critical slowing"', '"early warning"']
PSYCH_TERMS = ['psychiatric', 'psychopathology', 'depression', 'depressive', 'mood', 'affect',
               'emotion', 'emotional', 'anxiety', '"mental health"', '"experience sampling"',
               '"ecological momentary"', 'burnout', 'psychotherapy', 'wellbeing', '"well-being"']
WITHIN_TERMS = ['"within-person"', '"within-subject"', '"intensive longitudinal"', 'idiographic',
                '"single-case"', '"n-of-1"', '"time series"', '"individual trajectories"']

BLOCKS = {"MECH": MECH_TERMS, "TIP": TIP_TERMS, "PSYCH": PSYCH_TERMS, "WITHIN": WITHIN_TERMS}
LEGS = {"P1_psych": ["MECH", "TIP", "PSYCH"],
        "P2_within": ["MECH", "TIP", "WITHIN"],
        "P3_all": ["MECH", "TIP"]}
COUNT_ONLY = {"P3_all"}


def plain(names):
    return " AND ".join("(" + " OR ".join(BLOCKS[n]) + ")" for n in names)


def pubmed_term(names):
    parts = []
    for n in names:
        parts.append("(" + " OR ".join(f"{t}[tiab]" for t in BLOCKS[n]) + ")")
    return " AND ".join(parts)


def epmc_term(names):
    parts = []
    for n in names:
        parts.append("(" + " OR ".join(f"(TITLE_ABS:{t})" for t in BLOCKS[n]) + ")")
    return " AND ".join(parts)


# --------------------------------------------------------------------------
# Retrieval
# --------------------------------------------------------------------------
def openalex(query, pages=6, per=200):
    out, cursor, total = [], "*", None
    for _ in range(pages):
        u = ("https://api.openalex.org/works?per-page=%d&cursor=%s"
             "&select=id,doi,title,publication_year,primary_location,abstract_inverted_index"
             "&filter=title_and_abstract.search:%s"
             % (per, urllib.parse.quote(cursor), urllib.parse.quote(query)))
        d = _get(u)
        time.sleep(0.35)
        total = d["meta"]["count"]
        for w in d["results"]:
            inv = w.get("abstract_inverted_index") or {}
            pos = {}
            for word, ix in inv.items():
                for i in ix:
                    pos[i] = word
            loc = w.get("primary_location") or {}
            src = (loc.get("source") or {}).get("display_name") or ""
            out.append({"source": "openalex", "id": w["id"].split("/")[-1],
                        "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                        "year": str(w.get("publication_year") or ""), "journal": src,
                        "title": w.get("title") or "",
                        "abstract": " ".join(pos[k] for k in sorted(pos))[:5000]})
        cursor = d["meta"].get("next_cursor")
        if not cursor:
            break
    return out, total


def epmc_core(term, page_size=500, max_pages=4):
    """Europe PMC with resultType=core, which returns abstractText."""
    out, cursor = [], "*"
    for _ in range(max_pages):
        u = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json"
             f"&resultType=core&pageSize={page_size}&cursorMark={urllib.parse.quote(cursor)}"
             "&query=" + urllib.parse.quote(term))
        time.sleep(0.4)
        d = _get(u)
        for r in d.get("resultList", {}).get("result", []):
            out.append({"source": "europepmc", "id": r.get("id", ""),
                        "doi": r.get("doi", "") or "", "year": str(r.get("pubYear", "")),
                        "journal": r.get("journalTitle", "") or "",
                        "title": r.get("title", "") or "",
                        "abstract": (r.get("abstractText") or "")[:5000]})
        nxt = d.get("nextCursorMark")
        if not nxt or nxt == cursor:
            break
        cursor = nxt
    return out


def pubmed_abstracts(pmids):
    """efetch XML, because esummary carries no abstract."""
    out = []
    for i in range(0, len(pmids), 100):
        chunk = pmids[i:i + 100]
        u = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
             "?db=pubmed&retmode=xml&rettype=abstract&id=" + ",".join(chunk))
        time.sleep(0.4)
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=90) as r:
            xml = r.read().decode("utf-8", "replace")
        for art in re.split(r"<PubmedArticle>", xml)[1:]:
            pmid = (re.search(r"<PMID[^>]*>(\d+)</PMID>", art) or [None, ""])[1]
            title = re.sub(r"<[^>]+>", " ", (re.search(
                r"<ArticleTitle[^>]*>(.*?)</ArticleTitle>", art, re.S) or [None, ""])[1])
            abst = " ".join(re.sub(r"<[^>]+>", " ", m) for m in re.findall(
                r"<AbstractText[^>]*>(.*?)</AbstractText>", art, re.S))
            doi = (re.search(r'<ArticleId IdType="doi">(.*?)</ArticleId>', art) or [None, ""])[1]
            jr = (re.search(r"<Title>(.*?)</Title>", art, re.S) or [None, ""])[1]
            yr = (re.search(r"<PubDate>.*?<Year>(\d{4})</Year>", art, re.S) or [None, ""])[1]
            out.append({"source": "pubmed", "id": pmid, "doi": doi, "year": yr,
                        "journal": re.sub(r"\s+", " ", jr).strip(),
                        "title": re.sub(r"\s+", " ", title).strip(),
                        "abstract": re.sub(r"\s+", " ", abst).strip()[:5000]})
    return out


# --------------------------------------------------------------------------
# Screening -- frozen, spec v1.0 section 4
# --------------------------------------------------------------------------
FAM = {"rate": [r"rate[- ]induced", r"rate[- ]dependent", r"\bR-tipping\b"],
       "noise": [r"noise[- ]induced", r"stochastic(ally)? induced", r"\bN-tipping\b"],
       "bifurcation": [r"bifurcation[- ]induced", r"\bB-tipping\b", r"saddle[- ]node",
                       r"\bfold\b.{0,20}bifurcation", r"bifurcation[- ]?driven"]}
S2_PSYCH = [r"psychiatr", r"psychopatholog", r"depress", r"\bmood\b", r"\baffect(ive)?\b",
            r"emotion", r"anxiet", r"mental health", r"experience sampling",
            r"ecological momentary", r"burnout", r"psychotherap", r"well[- ]?being"]
S3_APPLIED = [r"participant", r"patient", r"empirical", r"dataset", r"cohort", r"observed data",
              r"experience sampling", r"ecological momentary", r"\bn\s*=\s*\d+"]


def families(text):
    return [f for f, pats in FAM.items() if any(re.search(p, text, re.I) for p in pats)]


def hits(pats, text):
    return [p for p in pats if re.search(p, text, re.I)]


def screen(rec):
    t = f"{rec['title']} {rec.get('abstract', '')}"
    fams = families(t)
    s1 = len(fams) >= 2
    s2 = bool(hits(S2_PSYCH, t))
    s3 = bool(hits(S3_APPLIED, t))
    if s1 and s2:
        d, miss = "READ", ""
    elif s1:
        d, miss = "METHOD_PRECEDENT", "S2_PSYCH"
    else:
        d = "EXCLUDE"
        miss = "S1_PARTITION" + ("" if s2 else ",S2_PSYCH")
    return dict(decision=d, missing=miss, families=";".join(sorted(fams)),
                n_families=len(fams), s3_applied=s3)


# --------------------------------------------------------------------------
def main():
    OUT.mkdir(exist_ok=True)
    counts, records, seen = [], [], set()

    print("=" * 76)
    print("B/N/R PRIOR-ART SCAN -- spec v1.0 frozen, blocks unaltered")
    print("=" * 76)

    for leg, names in LEGS.items():
        print(f"\n{leg}  ({' AND '.join(names)})")

        # cumulative PubMed counts, for the funnel table
        for k in range(1, len(names) + 1):
            try:
                c = pubmed_count(pubmed_term(names[:k]))
            except Exception as e:  # noqa: BLE001
                c = -1
                print(f"    (pubmed count failed at {names[:k]}: {e})")
            counts.append({"leg": leg, "database": "pubmed",
                           "blocks": "+".join(names[:k]), "count": c})
            print(f"    pubmed  {'+'.join(names[:k]):22s} {c:8d}")

        try:
            _, oa_total = openalex(plain(names), pages=1, per=1)
        except Exception as e:  # noqa: BLE001
            oa_total = -1
            print(f"    (openalex count failed: {e})")
        counts.append({"leg": leg, "database": "openalex", "blocks": "+".join(names),
                       "count": oa_total})
        print(f"    openalex{'':22s} {oa_total:8d}")

        if leg in COUNT_ONLY:
            print("    -> COUNT ONLY leg, no retrieval (spec section 3)")
            continue

        rows = []
        try:
            oa_rows, _ = openalex(plain(names))
            rows += oa_rows
        except Exception as e:  # noqa: BLE001
            print(f"    (openalex retrieval failed: {e})")
        try:
            rows += epmc_core(epmc_term(names))
        except Exception as e:  # noqa: BLE001
            print(f"    (europepmc retrieval failed: {e})")
        try:
            ids = pubmed_ids(pubmed_term(names), retmax=1000)
            rows += pubmed_abstracts(ids)
        except Exception as e:  # noqa: BLE001
            print(f"    (pubmed retrieval failed: {e})")

        added = 0
        for r in rows:
            key = (r["doi"].lower() or norm_title(r["title"]))
            if not key or key in seen:
                continue
            seen.add(key)
            records.append({**r, "leg": leg, **screen(r)})
            added += 1
        print(f"    retrieved {len(rows)} -> {added} new unique")

    with open(OUT / f"bnr_prior_art_{TODAY}_counts.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["leg", "database", "blocks", "count"])
        w.writeheader()
        w.writerows(counts)

    fields = ["leg", "decision", "missing", "families", "n_families", "s3_applied",
              "source", "id", "doi", "year", "journal", "title", "abstract"]
    with open(OUT / f"bnr_prior_art_{TODAY}_screened.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(records, key=lambda r: (r["decision"] != "READ",
                                                   r["decision"] != "METHOD_PRECEDENT",
                                                   -int(r["n_families"]), r["year"])))

    print("\n" + "=" * 76)
    print(f"unique screened: {len(records)}")
    for d in ("READ", "METHOD_PRECEDENT", "EXCLUDE"):
        n = sum(1 for r in records if r["decision"] == d)
        print(f"  {d:18s} {n:5d}")

    for d in ("READ", "METHOD_PRECEDENT"):
        sel = [r for r in records if r["decision"] == d]
        if not sel:
            continue
        print(f"\n--- {d} ({len(sel)}) ---")
        for r in sel:
            flag = "applied" if r["s3_applied"] else "       "
            print(f"  [{r['year']:>4}] [{r['families']:<22}] [{flag}] {r['title'][:88]}")
            print(f"         {r['journal'][:70]}  doi:{r['doi']}")

    print(f"\nwrote outputs/bnr_prior_art_{TODAY}_{{counts,screened}}.csv")


if __name__ == "__main__":
    main()
