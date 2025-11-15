# How to Scrape a Single Municipality - Simple Guide

Quick guide to scrape all candidates from one municipality using the refined notebook.

---

## 🎯 Quick Answer

Find this cell in the notebook:

```python
# Scrape municipality (start with small number to test)
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"

# Start with 3 candidates to test
candidates = scrape_municipality_refined(municipality_url, max_candidates=3)
```

**Change the numbers:**

### To Test (3 candidates):
```python
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"
candidates = scrape_municipality_refined(municipality_url, max_candidates=3)
```

### To Scrape ALL Candidates:
```python
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"
candidates = scrape_municipality_refined(municipality_url)  # Remove max_candidates!
```

### To Scrape a Different Municipality:
```python
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/101"  # Change 124 to your municipality ID
candidates = scrape_municipality_refined(municipality_url)
```

---

## 📝 Step-by-Step Instructions

### Step 1: Find Your Municipality ID

Visit: https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel

1. Click on your municipality
2. Look at the URL - it will show: `.../din-stemmeseddel/124` (or another number)
3. The number at the end is your municipality ID

**Common Municipality IDs:**
- 124 = København
- 101 = København (suburbs)
- 147 = Frederiksberg
- 151 = Ballerup
- 157 = Gentofte
- 159 = Gladsaxe
- 185 = Tårnby
- 461 = Odense
- 751 = Aarhus

---

### Step 2: Locate the Cell in the Notebook

Scroll down to find the section titled:

```
## Scrape Full Municipality
```

You'll see this code:

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

### Step 3: Make Your Changes

#### Option A: Scrape All Candidates from København (124)

**Change this:**
```python
candidates = scrape_municipality_refined(municipality_url, max_candidates=3)
```

**To this:**
```python
candidates = scrape_municipality_refined(municipality_url)
```

That's it! By removing `max_candidates=3`, it will scrape ALL candidates.

---

#### Option B: Scrape Different Municipality (e.g., Aarhus = 751)

**Change this:**
```python
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"

print("\n" + "="*60)
print("SCRAPING MUNICIPALITY 124 (KØBENHAVN)")
print("="*60)

candidates = scrape_municipality_refined(municipality_url, max_candidates=3)
```

**To this:**
```python
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/751"

print("\n" + "="*60)
print("SCRAPING MUNICIPALITY 751 (AARHUS)")
print("="*60)

candidates = scrape_municipality_refined(municipality_url)  # No max_candidates = all candidates
```

---

### Step 4: Run the Cell

1. Click on the cell you just edited
2. Press `Shift + Enter` (or click the "Run" button)
3. Wait for scraping to complete

**What you'll see:**
```
============================================================
SCRAPING MUNICIPALITY 124 (KØBENHAVN)
============================================================

Fetching candidate links from: https://...
✓ Found 87 candidate links

============================================================
[1/87]
Scraping: https://...
  ✓ Basic info: Name (Party)
  ✓ Om section: Uddannelse=True, Bopæl=True
  ✓ Found 3 mærkesager
  ✓ Clicked 'vis alle' button
  ✓ Extracted 19 test answers

============================================================
[2/87]
Scraping: https://...
...
```

---

### Step 5: Wait for Completion

**Estimated time:**
- 50 candidates = ~15-20 minutes
- 100 candidates = ~30-40 minutes
- 200 candidates = ~60-80 minutes

**Progress indicators:**
- `[1/87]` shows current candidate / total candidates
- Each candidate takes ~15-25 seconds

**Don't close the browser or notebook while it's running!**

---

### Step 6: Check Results

After scraping completes, you'll see:

```
============================================================
✓ Successfully scraped 87/87 candidates
============================================================
```

The next cells will automatically:
- Create DataFrames
- Save CSV files
- Generate summary statistics

---

## 🎛️ Advanced Options

### Scrape Specific Number of Candidates

```python
# Scrape first 10 candidates
candidates = scrape_municipality_refined(municipality_url, max_candidates=10)

# Scrape first 50 candidates
candidates = scrape_municipality_refined(municipality_url, max_candidates=50)
```

### Scrape Multiple Municipalities

Find the cell with this function:

```python
def scrape_multiple_municipalities(municipality_ids: List[int], max_per_muni: Optional[int] = None):
```

**Uncomment and edit the example:**

```python
# Example (uncomment to use):
municipality_ids = [124, 101, 147]  # København, suburbs, Frederiksberg
all_candidates = scrape_multiple_municipalities(municipality_ids, max_per_muni=5)
```

**Change to:**

```python
# Scrape København, Frederiksberg, and Gentofte
municipality_ids = [124, 147, 157]
all_candidates = scrape_multiple_municipalities(municipality_ids)  # All candidates from each
```

---

## 📊 What Happens After Scraping

The notebook will automatically create these files:

### Files Created:
1. `candidates_main_refined.csv` - All candidate info
2. `candidates_maerkesager_refined.csv` - Policy priorities
3. `candidates_svars_wide_refined.csv` - Test answers (wide format)
4. `candidates_svars_long_refined.csv` - Test answers (long format)
5. `candidates_complete_refined.json` - Complete raw data

### Location:
Files are saved in the **same folder** as your notebook.

---

## ⚠️ Important Tips

### 1. Always Test First
```python
# Start with 3 candidates to test
candidates = scrape_municipality_refined(municipality_url, max_candidates=3)

# If it works, then scrape all
candidates = scrape_municipality_refined(municipality_url)
```

### 2. Don't Interrupt
- Don't close the browser
- Don't close the notebook
- Don't shut down your computer
- Let it run to completion

### 3. Save Progress
The data is only saved to files AFTER scraping completes. If you interrupt, you lose everything!

### 4. Be Patient
- Each candidate takes ~15-25 seconds
- 100 candidates = ~30-40 minutes
- This is normal and expected

---

## 🔍 Quick Reference

### Change Municipality ID:
```python
# FROM:
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"

# TO:
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/YOUR_ID"
```

### Remove Candidate Limit:
```python
# FROM:
candidates = scrape_municipality_refined(municipality_url, max_candidates=3)

# TO:
candidates = scrape_municipality_refined(municipality_url)
```

### Add Candidate Limit:
```python
# FROM:
candidates = scrape_municipality_refined(municipality_url)

# TO:
candidates = scrape_municipality_refined(municipality_url, max_candidates=10)
```

---

## 🐛 Troubleshooting

### "Can't find candidates"
**Check:**
- Is the municipality ID correct?
- Visit the URL in your browser - does it load?
- Try a different municipality to test

### "Scraping stops partway through"
**Solutions:**
- Internet connection issue - restart from beginning
- Server timeout - add longer delays:
  ```python
  time.sleep(3)  # Change from 2 to 3 seconds
  ```

### "Not getting 19 test answers"
**Check:**
- Did you see "✓ Clicked 'vis alle' button"?
- If not, the button might not exist on that page
- Try testing with the example candidate first

---

## ✅ Complete Example

Here's a **complete, working example** to copy/paste:

```python
# ==========================================
# SCRAPE KØBENHAVN (MUNICIPALITY 124)
# ==========================================

# Step 1: Set the URL
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"

# Step 2: Test with 3 candidates first
print("Testing with 3 candidates...")
test_candidates = scrape_municipality_refined(municipality_url, max_candidates=3)

# Step 3: Check if test worked
successful = [c for c in test_candidates if 'error' not in c]
print(f"✓ Test successful: {len(successful)}/3 candidates scraped")

# Step 4: If test worked, scrape all
if len(successful) == 3:
    print("\nTest successful! Scraping all candidates...")
    candidates = scrape_municipality_refined(municipality_url)
    print(f"✓ Complete! Scraped {len(candidates)} total candidates")
else:
    print("⚠ Test failed. Fix errors before scraping all candidates.")
```

**How to use:**
1. Copy this code
2. Paste into a NEW cell in the notebook
3. Run the cell
4. It will test first, then scrape all if test succeeds

---

## 📌 Summary

**To scrape an entire municipality:**

1. **Find municipality ID** from DR website URL
2. **Locate the cell** with `municipality_url = ...`
3. **Change the ID** in the URL
4. **Remove** `max_candidates=3` to scrape all candidates
5. **Run the cell** and wait for completion
6. **Check the output files** in your notebook folder

**That's it!** 🎉

---

## 🎯 Common Patterns

### Pattern 1: Test → Full Scrape
```python
# Test
candidates = scrape_municipality_refined(url, max_candidates=3)

# If successful, then full scrape
candidates = scrape_municipality_refined(url)
```

### Pattern 2: Multiple Municipalities
```python
# Scrape 3 cities
municipality_ids = [124, 461, 751]  # København, Odense, Aarhus
all_candidates = scrape_multiple_municipalities(municipality_ids)
```

### Pattern 3: Incremental Saves
```python
# Scrape and save after each municipality
for muni_id in [124, 147, 157]:
    url = f"https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/{muni_id}"
    candidates = scrape_municipality_refined(url)
    
    # Save immediately
    df = pd.DataFrame(candidates)
    df.to_csv(f'candidates_municipality_{muni_id}.csv', index=False)
    print(f"✓ Saved municipality {muni_id}")
```

---

**You're ready to scrape!** 🚀

Just change the municipality ID and remove the `max_candidates` parameter.
