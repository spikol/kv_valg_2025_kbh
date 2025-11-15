# Quick Reference: What to Change in the Notebook

## 🎯 The One Cell You Need to Change

Find this section in your notebook:

```
## Scrape Full Municipality
```

---

## ✏️ BEFORE (Test Mode - 3 candidates):

```python
# Scrape municipality (start with small number to test)
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"

print("\n" + "="*60)
print("SCRAPING MUNICIPALITY 124 (KØBENHAVN)")
print("="*60)

# Start with 3 candidates to test
candidates = scrape_municipality_refined(municipality_url, max_candidates=3)
```

---

## ✏️ AFTER (Full Scrape - ALL candidates):

```python
# Scrape municipality (ALL candidates)
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"

print("\n" + "="*60)
print("SCRAPING MUNICIPALITY 124 (KØBENHAVN)")
print("="*60)

# Scrape ALL candidates
candidates = scrape_municipality_refined(municipality_url)
```

---

## 🔴 What Changed?

### 1. Comment
```python
# BEFORE:
# Start with 3 candidates to test

# AFTER:
# Scrape ALL candidates
```

### 2. Function Call
```python
# BEFORE:
candidates = scrape_municipality_refined(municipality_url, max_candidates=3)
#                                                           ^^^^^^^^^^^^^^^^
#                                                           Remove this part!

# AFTER:
candidates = scrape_municipality_refined(municipality_url)
#                                                         ^
#                                                         Just close the parenthesis!
```

---

## 🏙️ Change Municipality

To scrape a different city, change the **number at the end** of the URL:

```python
# København (124):
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"

# Frederiksberg (147):
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/147"

# Aarhus (751):
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/751"

# Odense (461):
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/461"
```

---

## 🎛️ Control How Many Candidates

```python
# Just 5 candidates (for testing):
candidates = scrape_municipality_refined(municipality_url, max_candidates=5)

# First 10 candidates:
candidates = scrape_municipality_refined(municipality_url, max_candidates=10)

# First 50 candidates:
candidates = scrape_municipality_refined(municipality_url, max_candidates=50)

# ALL candidates (no limit):
candidates = scrape_municipality_refined(municipality_url)
```

---

## 📋 Complete Examples

### Example 1: Test København with 3 candidates
```python
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"
candidates = scrape_municipality_refined(municipality_url, max_candidates=3)
```

### Example 2: Scrape ALL København candidates
```python
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"
candidates = scrape_municipality_refined(municipality_url)
```

### Example 3: Scrape ALL Aarhus candidates
```python
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/751"
candidates = scrape_municipality_refined(municipality_url)
```

### Example 4: Test Odense with 10 candidates
```python
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/461"
candidates = scrape_municipality_refined(municipality_url, max_candidates=10)
```

---

## 🚀 Recommended Workflow

### Step 1: Test (always start here!)
```python
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"
candidates = scrape_municipality_refined(municipality_url, max_candidates=3)
```
**Run this cell and verify it works!**

### Step 2: Edit the Same Cell
**Change the cell to:**
```python
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"
candidates = scrape_municipality_refined(municipality_url)
```

### Step 3: Run Again
**Run the edited cell to scrape ALL candidates**

---

## 🔍 Visual Guide

```
┌─────────────────────────────────────────────────────────────┐
│  Find this line in the notebook:                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  candidates = scrape_municipality_refined(                  │
│      municipality_url,                                       │
│      max_candidates=3    ← DELETE THIS LINE                 │
│  )                                                           │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  Change it to:                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  candidates = scrape_municipality_refined(municipality_url) │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚡ Ultra Quick Reference

| What I Want | What to Type |
|-------------|--------------|
| Test with 3 candidates | `max_candidates=3` |
| Test with 5 candidates | `max_candidates=5` |
| Test with 10 candidates | `max_candidates=10` |
| **Scrape ALL candidates** | **Remove `max_candidates` entirely** |

---

## 🎯 Copy-Paste Ready

Just copy this and paste it into the notebook cell:

```python
# Scrape ALL candidates from København
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"
candidates = scrape_municipality_refined(municipality_url)
```

**Then press `Shift + Enter` to run!**

---

## 📊 What You'll See

### During Scraping:
```
Fetching candidate links from: https://...
✓ Found 87 candidate links

============================================================
[1/87]
Scraping: https://...
  ✓ Basic info: Name (Party)
  ✓ Found 3 mærkesager
  ✓ Clicked 'vis alle' button
  ✓ Extracted 19 test answers

============================================================
[2/87]
...
```

### After Completion:
```
============================================================
✓ Successfully scraped 87/87 candidates
============================================================
```

---

## ⏱️ Time Estimates

| Candidates | Estimated Time |
|-----------|----------------|
| 3 (test) | 1-2 minutes |
| 10 | 3-5 minutes |
| 50 | 15-20 minutes |
| 100 | 30-40 minutes |
| 200 | 60-80 minutes |

---

## ✅ Checklist

Before running full scrape:

- [ ] Tested with 3 candidates first
- [ ] Test was successful (saw ✓ messages)
- [ ] Changed municipality URL if needed
- [ ] Removed `max_candidates=3` to scrape all
- [ ] Have stable internet connection
- [ ] Won't need to close laptop for 30-60 mins

**Ready? Run the cell!** 🚀

---

## 🎓 Pro Tip

**Save this code in a new cell** to scrape with automatic testing:

```python
# Safe scraping with test first
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"

# Test
print("Testing with 3 candidates...")
test = scrape_municipality_refined(municipality_url, max_candidates=3)

# Check test
if len([c for c in test if 'error' not in c]) == 3:
    print("✓ Test passed! Scraping all candidates...\n")
    candidates = scrape_municipality_refined(municipality_url)
else:
    print("✗ Test failed. Fix errors before continuing.")
```

This automatically tests first, then scrapes all if test passes!
