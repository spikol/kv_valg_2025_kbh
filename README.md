# DR Folketing Election Candidate Scraper & Analysis

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/spikol/kv_valg_2025_kbh/blob/main/pca_interactive.py)

A scraper and interactive analysis tool for Danish national election (Folketingsvalg) candidate data from DR.dk, covering all 22 electoral districts (kredse).

## Overview

This project scrapes candidate information from DR.dk's election pages and provides an interactive PCA-based visualization to explore ideological positions across parties and candidates.

**Dataset**: 15,394 candidates across 22 districts, 25 policy questions each.

### Data collected per candidate

- **Basic info**: Name, party code, candidate ID, district
- **Policy positions**: Answers to 25 political questions (1=Meget enig → 5=Meget uenig)
- **Mærkesager**: Up to 3 policy priorities with title and description

## Interactive Notebook

The marimo notebook (`pca_interactive.py`) includes:

1. **PCA — all candidates**: Scatter plot with lines to party means, click to see candidate info
2. **Per-question bar chart**: Mean party response per question
3. **PCA colored by question**: See where agree/disagree candidates sit spatially
4. **PCA with lines colored by question**: Combines party structure with question-level color
5. **Party comparison**: Side-by-side mean responses for any two parties across all 25 questions
6. **Similarity network**: Connects candidates with cosine similarity above a threshold slider

## Project Structure

```
kv_project/
├── folk_version_02/        # District 6 (pilot scrape)
│   ├── combined_wide.csv
│   ├── combined_answers.csv
│   └── combined_maerkesager.csv
├── folk_version_03/        # National — all 22 districts
│   ├── combined_wide.csv       # 15,394 candidates × 25 questions (wide)
│   ├── combined_answers.csv    # Long format
│   ├── combined_maerkesager.csv
│   └── pca_input.csv           # Filtered input for PCA
├── scrape_candidate2.py    # Scraper for a single district
├── scrape_candidate3.py    # Scraper for districts 6–27
├── pca_test.py             # Party-level PCA (district 6)
├── pca_test_02.py          # Party-level PCA (national)
├── pcs_cand_01.py          # Candidate-level PCA
├── pca_candidates_02.py    # Candidate PCA with lines to party means
└── pca_interactive.py      # Interactive marimo notebook
```

## Quick Start

### Run the interactive notebook

```bash
pip install marimo pandas scikit-learn plotly numpy
marimo edit pca_interactive.py
```

### Scrape national data

```bash
python scrape_candidate3.py   # scrapes districts 6–27 into folk_version_03/
```

## Output Format

### combined_wide.csv

```
candidate_id, name, party_code,
q1_question, q1_answer_value, q1_answer_label, q1_answer_text, q1_is_important,
... (×25 questions) ...,
mk1_title, mk1_text, mk2_title, mk2_text, mk3_title, mk3_text
```

### combined_answers.csv (long format)

```
candidate_id, name, party_code, question_number, question_text, answer_value, answer_label, is_important
```

## Candidates per party (national)

| Party | Candidates |
| ----- | ---------- |
| Å | 242 |
| A | 230 |
| C | 230 |
| B | 228 |
| I | 224 |
| Ø | 217 |
| F | 212 |
| V | 195 |
| O | 179 |
| M | 136 |
| Æ | 93 |
| H | 87 |
| **Total** | **2,280** |

## PCA Results

The two principal components explain **81%** of variance in party positions:

- **PC1 (64%)**: Left-right axis — public transport / foreign aid / DR vs. tax cuts / deportation / DR cuts
- **PC2 (17%)**: Secondary axis — populist vs. pragmatic/centrist positioning

## Legal & Ethical

- Data sourced from DR.dk's public election pages
- For research and educational purposes
- Please respect DR.dk's terms of service and rate limit requests

## License

Educational and research use. Credit DR.dk as data source.
