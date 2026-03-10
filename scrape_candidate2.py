"""
Scrapes all candidates from a DR constituency listing page.

Usage:
    python scrape_candidate2.py                    # default: district 6
    python scrape_candidate2.py 6
    python scrape_candidate2.py <district_id>

Outputs to folk_version_02/:
    combined_answers.csv     — one row per (candidate × question), long format
    combined_maerkesager.csv — one row per (candidate × mærkesag), long format
    combined_wide.csv        — one row per candidate, wide format
"""

import csv
import json
import os
import re
import sys
import time

import requests

# Reuse parsing logic from scrape_candidate.py
from scrape_candidate import fetch_candidate, save_wide_csv

LISTING_URL = "https://www.dr.dk/nyheder/politik/folketingsvalg/din-stemmeseddel/{}"
OUT_DIR = "folk_version_02"

ANSWERS_COLS = [
    "candidate_id", "name", "party_code",
    "question_id", "topic", "question",
    "answer_value", "answer_label", "answer_text", "is_important",
    "argument_for", "argument_against",
]
MAERKESAGER_COLS = [
    "candidate_id", "name", "party_code", "number", "title", "text",
]


def get_url_keys(district_id: int) -> list[dict]:
    """Fetch listing page and return list of {urlKey, partyCode, name} dicts."""
    url = LISTING_URL.format(district_id)
    resp = requests.get(url, headers={"Accept-Language": "da"}, timeout=15)
    resp.raise_for_status()
    html = resp.text

    scripts = re.findall(r"<script[^>]*>(.*?)</script>", html, re.DOTALL)
    rsc_chunks = []
    for s in scripts:
        m = re.search(r'self\.__next_f\.push\(\[1,"(.*)"\]\)\s*$', s, re.DOTALL)
        if m:
            try:
                rsc_chunks.append(json.loads('"' + m.group(1) + '"'))
            except json.JSONDecodeError:
                pass

    full_rsc = "".join(rsc_chunks)

    # Extract candidates array from the RSC payload
    idx = full_rsc.find('"candidates":[{')
    if idx == -1:
        raise ValueError("Could not find candidates list on page.")

    # Bracket-balance to extract the array
    start = full_rsc.index("[", idx)
    depth, in_str, esc = 0, False, False
    for i, ch in enumerate(full_rsc[start:], start):
        if esc:            esc = False; continue
        if ch == "\\" and in_str: esc = True; continue
        if ch == '"':      in_str = not in_str; continue
        if in_str:         continue
        if ch == "[":      depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                candidates = json.loads(full_rsc[start: i + 1])
                return candidates

    raise ValueError("Unbalanced brackets in candidates array.")


def append_answers(writer: csv.DictWriter, data: dict):
    c = data["candidate"]
    for qa in data["answers"]:
        writer.writerow({
            "candidate_id": c["id"],
            "name": c["name"],
            "party_code": c["party_code"],
            **qa,
        })


def append_maerkesager(writer: csv.DictWriter, data: dict):
    c = data["candidate"]
    for mk in data["maerkesager"]:
        writer.writerow({
            "candidate_id": c["id"],
            "name": c["name"],
            "party_code": c["party_code"],
            **mk,
        })


def append_wide(writer: csv.DictWriter, fieldnames: list, data: dict, url_key: str):
    c = data["candidate"]
    row = {"candidate_id": c["id"], "name": c["name"], "party_code": c["party_code"]}
    for i, qa in enumerate(data["answers"], 1):
        row[f"q{i}_question"]     = qa["question"]
        row[f"q{i}_answer_value"] = qa["answer_value"]
        row[f"q{i}_answer_label"] = qa["answer_label"]
        row[f"q{i}_answer_text"]  = qa["answer_text"]
        row[f"q{i}_is_important"] = qa["is_important"]
    for mk in data["maerkesager"]:
        n = mk["number"]
        row[f"mk{n}_title"] = mk["title"]
        row[f"mk{n}_text"]  = mk["text"]
    # Fill any missing columns with ""
    writer.writerow({col: row.get(col, "") for col in fieldnames})


def build_wide_fieldnames(sample_data: dict) -> list:
    cols = ["candidate_id", "name", "party_code"]
    for i in range(1, len(sample_data["answers"]) + 1):
        cols += [f"q{i}_question", f"q{i}_answer_value", f"q{i}_answer_label",
                 f"q{i}_answer_text", f"q{i}_is_important"]
    for mk in sample_data["maerkesager"]:
        n = mk["number"]
        cols += [f"mk{n}_title", f"mk{n}_text"]
    return cols


def main(district_id: int):
    os.makedirs(OUT_DIR, exist_ok=True)

    print(f"Henter kandidatliste for distrikt {district_id} ...")
    candidates = get_url_keys(district_id)
    print(f"Fandt {len(candidates)} kandidater.\n")

    answers_path     = os.path.join(OUT_DIR, "combined_answers.csv")
    maerkesager_path = os.path.join(OUT_DIR, "combined_maerkesager.csv")
    wide_path        = os.path.join(OUT_DIR, "combined_wide.csv")

    wide_fieldnames = None
    wide_writer = None
    wide_file = None

    with (
        open(answers_path,     "w", encoding="utf-8", newline="") as af,
        open(maerkesager_path, "w", encoding="utf-8", newline="") as mf,
    ):
        a_writer = csv.DictWriter(af, fieldnames=ANSWERS_COLS)
        m_writer = csv.DictWriter(mf, fieldnames=MAERKESAGER_COLS)
        a_writer.writeheader()
        m_writer.writeheader()

        for i, cand in enumerate(candidates, 1):
            url_key = cand["urlKey"]
            name    = cand["name"]
            party   = cand["partyCode"]
            print(f"[{i:3}/{len(candidates)}] {name} ({party}) — {url_key}")

            try:
                data = fetch_candidate(url_key)
            except Exception as e:
                print(f"  FEJL: {e}")
                continue

            append_answers(a_writer, data)
            append_maerkesager(m_writer, data)

            # Initialise wide CSV on first successful scrape
            if wide_fieldnames is None:
                wide_fieldnames = build_wide_fieldnames(data)
                wide_file = open(wide_path, "w", encoding="utf-8", newline="")
                wide_writer = csv.DictWriter(wide_file, fieldnames=wide_fieldnames)
                wide_writer.writeheader()

            append_wide(wide_writer, wide_fieldnames, data, url_key)

            # Polite delay between requests
            if i < len(candidates):
                time.sleep(0.5)

    if wide_file:
        wide_file.close()

    print(f"\nFærdig!")
    print(f"  {answers_path}")
    print(f"  {maerkesager_path}")
    print(f"  {wide_path}")


if __name__ == "__main__":
    district = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    main(district)
