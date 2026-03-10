"""
Scraper for DR's candidate pages (FV26).
Extracts: questions + text answers, answer scale value (graphic), and mærkesager.

Usage:
    python scrape_candidate.py
    python scrape_candidate.py 480-jarl-matthiesen
"""

import csv
import sys
import re
import json
import requests

BASE_URL = "https://www.dr.dk/nyheder/politik/folketingsvalg/din-stemmeseddel/kandidater/{}"

# Scale labels used in the graphic (1=leftmost, 5=rightmost)
ANSWER_LABELS = {
    1: "Meget enig",
    2: "Enig",
    3: "Neutral",
    4: "Uenig",
    5: "Meget uenig",
}


def fetch_candidate(url_key: str) -> dict:
    url = BASE_URL.format(url_key)
    resp = requests.get(url, headers={"Accept-Language": "da"}, timeout=15)
    resp.raise_for_status()
    return parse_page(resp.text)


def extract_json_array(text: str, key: str) -> list:
    """Find `"key":[...]` in text using a bracket counter to handle nesting."""
    start_marker = f'"{key}":'
    idx = text.find(start_marker)
    if idx == -1:
        raise ValueError(f'Key "{key}" not found in text')
    idx += len(start_marker)
    # skip whitespace
    while idx < len(text) and text[idx] in " \t\n\r":
        idx += 1
    if text[idx] != "[":
        raise ValueError(f'Expected "[" after "{key}", got {text[idx]!r}')
    depth = 0
    in_string = False
    escape = False
    start = idx
    for i, ch in enumerate(text[idx:], idx):
        if escape:
            escape = False
            continue
        if ch == "\\" and in_string:
            escape = True
            continue
        if ch == '"' and not escape:
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return json.loads(text[start: i + 1])
    raise ValueError(f'Unbalanced brackets for key "{key}"')


def extract_json_object(text: str, key: str) -> dict:
    """Find `"key":{...}` in text using a brace counter to handle nesting."""
    start_marker = f'"{key}":'
    idx = text.find(start_marker)
    if idx == -1:
        raise ValueError(f'Key "{key}" not found in text')
    idx += len(start_marker)
    while idx < len(text) and text[idx] in " \t\n\r":
        idx += 1
    if text[idx] != "{":
        raise ValueError(f'Expected "{{" after "{key}", got {text[idx]!r}')
    depth = 0
    in_string = False
    escape = False
    start = idx
    for i, ch in enumerate(text[idx:], idx):
        if escape:
            escape = False
            continue
        if ch == "\\" and in_string:
            escape = True
            continue
        if ch == '"' and not escape:
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start: i + 1])
    raise ValueError(f'Unbalanced braces for key "{key}"')


def parse_page(html: str) -> dict:
    # Find all inline scripts
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", html, re.DOTALL)

    # The RSC payload is split across multiple push([1, "..."]) calls.
    # Concatenate all of them to find the candidate data.
    rsc_chunks = []
    for s in scripts:
        m = re.search(r'self\.__next_f\.push\(\[1,"(.*)"\]\)\s*$', s, re.DOTALL)
        if m:
            try:
                decoded = json.loads('"' + m.group(1) + '"')
                rsc_chunks.append(decoded)
            except json.JSONDecodeError:
                pass

    full_rsc = "".join(rsc_chunks)

    if '"candidate":{' not in full_rsc:
        raise ValueError("Could not find candidate data in page. The page structure may have changed.")

    candidate_data = extract_json_object(full_rsc, "candidate")
    answers_data = extract_json_array(full_rsc, "candidateAnswers")
    questions_data = extract_json_array(full_rsc, "questions")

    # Build question lookup by ID
    questions_by_id = {q["Id"]: q for q in questions_data}

    # Combine answers with question text
    qa_list = []
    for ans in answers_data:
        qid = ans["QuestionID"]
        q = questions_by_id.get(qid, {})
        qa_list.append({
            "question_id": qid,
            "topic": q.get("Title", ""),
            "question": q.get("Question", ""),
            "argument_for": q.get("ArgumentFor", ""),
            "argument_against": q.get("ArgumentAgainst", ""),
            "answer_value": ans["Answer"],          # 1–5 numeric (the graphic position)
            "answer_label": ANSWER_LABELS.get(ans["Answer"], str(ans["Answer"])),
            "answer_text": ans["Info"],             # candidate's own explanation
            "is_important": bool(ans["IsImportant"]),
        })

    maerkesager = [
        {
            "number": int(kt["keyTopicNumber"]),
            "title": kt["title"],
            "text": kt["text"],
        }
        for kt in candidate_data.get("Keytopics", [])
    ]

    return {
        "candidate": {
            "id": candidate_data["ID"],
            "name": f"{candidate_data['Firstname']} {candidate_data['LastName']}",
            "party": candidate_data["CurrentParty"],
            "party_code": candidate_data["CurrentPartyCode"],
            "constituency": next(
                (lu["lineUpName"] for lu in candidate_data.get("LineUps", [])
                 if lu["groupType"] == "SmallConstituency"), ""
            ),
            "city": candidate_data.get("City", ""),
            "profession": candidate_data.get("Profession", ""),
            "education": candidate_data.get("Education", ""),
        },
        "maerkesager": maerkesager,
        "answers": qa_list,
    }


def print_result(data: dict):
    c = data["candidate"]
    print(f"\n{'='*60}")
    print(f"  {c['name']} ({c['party_code']}) — {c['constituency']}")
    print(f"  {c['party']}")
    print(f"  Bopæl: {c['city']}  |  Erhverv: {c['profession']}")
    print(f"{'='*60}")

    print("\n--- MÆRKESAGER ---")
    for mk in data["maerkesager"]:
        print(f"\n{mk['number']}. {mk['title']}")
        print(f"   {mk['text']}")

    print(f"\n--- SPØRGSMÅL & SVAR ({len(data['answers'])}) ---")
    for i, qa in enumerate(data["answers"], 1):
        important = " ★" if qa["is_important"] else ""
        print(f"\n{i:2}. [{qa['topic']}]{important}")
        print(f"    Q: {qa['question']}")
        print(f"    Grafik: {qa['answer_label']} ({qa['answer_value']}/5)")
        print(f"    Svar:   {qa['answer_text']}")


def save_wide_csv(data: dict, url_key: str):
    """One row per candidate: candidate info + 25 answers (wide) + 3 mærkesager at end."""
    import os
    candidate_id = url_key.split("-")[0]
    c = data["candidate"]

    # Build column names and row dynamically
    fieldnames = ["candidate_id", "name", "party_code"]
    row = {
        "candidate_id": c["id"],
        "name": c["name"],
        "party_code": c["party_code"],
    }

    for i, qa in enumerate(data["answers"], 1):
        for col, val in [
            (f"q{i}_question", qa["question"]),
            (f"q{i}_answer_value", qa["answer_value"]),
            (f"q{i}_answer_label", qa["answer_label"]),
            (f"q{i}_answer_text", qa["answer_text"]),
            (f"q{i}_is_important", qa["is_important"]),
        ]:
            fieldnames.append(col)
            row[col] = val

    for mk in data["maerkesager"]:
        n = mk["number"]
        for col, val in [
            (f"mk{n}_title", mk["title"]),
            (f"mk{n}_text", mk["text"]),
        ]:
            fieldnames.append(col)
            row[col] = val

    out_file = os.path.join("folk_version_02", f"{candidate_id}_wide.csv")
    with open(out_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(row)
    print(f"Gemt som {out_file}")


def save_csv(data: dict, url_key: str):
    candidate_id = url_key.split("-")[0]
    c = data["candidate"]

    # --- answers CSV ---
    answers_file = f"{candidate_id}_answers.csv"
    with open(answers_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "candidate_id", "name", "party_code",
            "question_id", "topic", "question",
            "answer_value", "answer_label", "answer_text", "is_important",
            "argument_for", "argument_against",
        ])
        writer.writeheader()
        for qa in data["answers"]:
            writer.writerow({
                "candidate_id": c["id"],
                "name": c["name"],
                "party_code": c["party_code"],
                **qa,
            })
    print(f"Gemt som {answers_file}")

    # --- mærkesager CSV ---
    mk_file = f"{candidate_id}_maerkesager.csv"
    with open(mk_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "candidate_id", "name", "party_code", "number", "title", "text",
        ])
        writer.writeheader()
        for mk in data["maerkesager"]:
            writer.writerow({
                "candidate_id": c["id"],
                "name": c["name"],
                "party_code": c["party_code"],
                **mk,
            })
    print(f"Gemt som {mk_file}")


if __name__ == "__main__":
    url_key = sys.argv[1] if len(sys.argv) > 1 else "480-jarl-matthiesen"
    print(f"Henter kandidat: {url_key} ...")
    data = fetch_candidate(url_key)
    print_result(data)
    save_csv(data, url_key)
    save_wide_csv(data, url_key)
