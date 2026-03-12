"""
Scrapes all candidates from DR districts 6–27.

Outputs to folk_version_03/:
    combined_answers.csv     — one row per (candidate × question), long format
    combined_maerkesager.csv — one row per (candidate × mærkesag), long format
    combined_wide.csv        — one row per candidate, wide format
"""

import csv
import os
import time

from scrape_candidate import fetch_candidate
from scrape_candidate2 import (
    get_url_keys,
    append_answers,
    append_maerkesager,
    append_wide,
    build_wide_fieldnames,
    ANSWERS_COLS,
    MAERKESAGER_COLS,
)

DISTRICTS = range(6, 28)  # 6 to 27 inclusive
OUT_DIR = "folk_version_03"


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

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

        for district_id in DISTRICTS:
            print(f"\n=== Distrikt {district_id} ===")
            try:
                candidates = get_url_keys(district_id)
            except Exception as e:
                print(f"  FEJL ved hentning af kandidatliste: {e}")
                continue

            print(f"Fandt {len(candidates)} kandidater.")

            for i, cand in enumerate(candidates, 1):
                url_key = cand["urlKey"]
                name    = cand["name"]
                party   = cand["partyCode"]
                print(f"  [{i:3}/{len(candidates)}] {name} ({party}) — {url_key}")

                try:
                    data = fetch_candidate(url_key)
                except Exception as e:
                    print(f"    FEJL: {e}")
                    continue

                append_answers(a_writer, data)
                append_maerkesager(m_writer, data)

                if wide_fieldnames is None:
                    wide_fieldnames = build_wide_fieldnames(data)
                    wide_file = open(wide_path, "w", encoding="utf-8", newline="")
                    wide_writer = csv.DictWriter(wide_file, fieldnames=wide_fieldnames)
                    wide_writer.writeheader()

                append_wide(wide_writer, wide_fieldnames, data, url_key)

                if i < len(candidates):
                    time.sleep(0.5)

    if wide_file:
        wide_file.close()

    print(f"\nFærdig!")
    print(f"  {answers_path}")
    print(f"  {maerkesager_path}")
    print(f"  {wide_path}")


if __name__ == "__main__":
    main()
