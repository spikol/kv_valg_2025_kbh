# DR Candidate Scraper - REFINED VERSION ⭐

## 🎯 Key Improvements in This Version

This refined scraper includes **critical improvements** over the enhanced version:

### 1. **Clicks "Vis Alle" Button** 🖱️
- Automatically finds and clicks the "show all" button
- Reveals all 19 candidate test answers that are initially hidden
- Uses multiple fallback methods to find the button
- Handles different button text variations (vis alle, vis alle svar, se alle, etc.)

### 2. **Improved Mærkesager Extraction** 📋
- Better parsing of policy priorities structure
- Extracts both **title** and **description** separately
- Multiple extraction methods for robustness
- Handles different HTML structures on DR's pages

### 3. **Robust Button Clicking** 💪
- Tries multiple selectors and methods
- JavaScript click fallback if regular click fails
- Scrolls to button before clicking
- Handles `ElementClickInterceptedException`
- Works even if button is hidden or obstructed

### 4. **Enhanced Test Answer Extraction** 📝
- Extracts **both question and answer** for each of 19 questions
- Multiple parsing methods for different page structures
- Handles dynamic content loading
- Fallback methods if primary extraction fails

---

## 📊 Complete Data Extraction

### What You Get:

#### Basic Information
- ✅ Candidate ID
- ✅ Name, Party, Municipality

#### Om Section (Biographical Data)
- ✅ **Uddannelse** (Education)
- ✅ **Bopæl** (Residence)
- ✅ **Alder** (Age)
- ✅ **Erhverv** (Occupation)
- ✅ **Sociale medier** (Social media links)

#### Mærkesager (Policy Priorities) - IMPROVED
- ✅ **Priority number** (1-10)
- ✅ **Title** (separated from description)
- ✅ **Description** (detailed policy text)
- ✅ **Full text** (complete priority statement)

#### Test Answers (19 Svars) - NEW & IMPROVED
- ✅ **Question text** for each of 19 questions
- ✅ **Answer** for each question
- ✅ Automatically clicks button to reveal all answers
- ✅ Available in both wide and long format

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install selenium webdriver-manager beautifulsoup4 pandas lxml
```

Make sure Chrome browser is installed.

### 2. Open Notebook

```bash
jupyter notebook dr_candidate_scraper_refined.ipynb
```

### 3. Run Test Cell

Start by testing with a single candidate to verify button clicking works:

```python
test_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/kandidater/kommune/7250-pernille-rosenkrantz-theil"
test_candidate = scrape_candidate_refined(test_url, driver)
```

You should see output like:
```
Scraping: https://...
  ✓ Basic info: Pernille Rosenkrantz-Theil (A)
  ✓ Om section: Uddannelse=True, Bopæl=True
  ✓ Found 3 mærkesager
  ✓ Clicked 'vis alle' button
  ✓ Extracted 19 test answers
```

### 4. Scale Up

Once testing works, scrape the full municipality:

```python
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"
candidates = scrape_municipality_refined(municipality_url, max_candidates=10)
```

---

## 📁 Output Files

The refined scraper creates **5 CSV files** + 1 JSON:

### 1. `candidates_main_refined.csv`
Main DataFrame with all candidate info:
- Basic info (name, party, municipality)
- Om section (uddannelse, bopæl, alder, erhverv)
- Counts (num_priorities, num_test_answers)

### 2. `candidates_maerkesager_refined.csv`
Policy priorities with improved structure:
```
candidate_id | name | party | priority_number | priority_title | priority_description | priority_full_text
```

### 3. `candidates_svars_wide_refined.csv`
Test answers in wide format (one column per question):
```
candidate_id | name | party | svar_1_question | svar_1_answer | svar_2_question | svar_2_answer | ...
```

### 4. `candidates_svars_long_refined.csv`
Test answers in long format (one row per answer):
```
candidate_id | name | party | question_number | question_text | answer_text
```

### 5. `candidates_complete_refined.json`
Complete raw data with all nested structures preserved.

---

## 🔧 How the Button Clicking Works

### The "Vis Alle" Button Challenge

DR's website initially shows only a preview of candidate test answers. To see all 19 answers, users must click a "vis alle" (show all) button. This refined scraper handles this automatically.

### Multiple Detection Methods

The scraper uses several methods to find and click the button:

#### Method 1: Button Text Search
```python
# Searches for buttons with text like:
- "vis alle"
- "vis alle svar"
- "se alle svar"
- "vis svar"
- "show all"
- "se alle"
```

#### Method 2: CSS Selectors
```python
# Tries multiple selectors:
- [data-action="show-all"]
- .show-all-button
- button.expand-answers
# etc.
```

#### Method 3: Expandable Elements
```python
# Looks for:
- Elements with aria-expanded="false"
- Collapsible sections
- Hidden content containers
```

### Robust Clicking

If regular click fails, the scraper:
1. Scrolls element into view
2. Waits for animations
3. Tries JavaScript click as fallback
4. Retries up to 3 times

---

## 🎨 Improved Mærkesager Extraction

### What's New

The refined scraper now extracts mærkesager with **better structure**:

**Before (Basic Version):**
```python
{
  'number': 1,
  'text': 'Gratis vuggestuer: Det er blevet alt for dyrt...'
}
```

**After (Refined Version):**
```python
{
  'number': 1,
  'title': 'Gratis vuggestuer og børnehaver',
  'description': 'Det er blevet alt for dyrt at bo i København...',
  'full_text': 'Gratis vuggestuer og børnehaver: Det er blevet...'
}
```

### Parsing Logic

1. **Finds mærkesager section** by heading
2. **Parses list items** (ul/ol elements)
3. **Splits on colon** to separate title from description
4. **Handles edge cases** (no colon, multiple colons, etc.)
5. **Fallback method** if structured parsing fails

---

## 💡 Usage Examples

### Example 1: Extract Specific Fields

```python
# After scraping
for candidate in candidates:
    if candidate.get('num_test_answers') == 19:
        print(f"{candidate['name']}: Complete test data ✓")
    
    for priority in candidate.get('priorities', []):
        if 'klima' in priority['title'].lower():
            print(f"Climate priority: {priority['title']}")
```

### Example 2: Compare Answers Across Parties

```python
# Create pivot table
pivot = df_svars_long.pivot_table(
    index='question_number',
    columns='party',
    values='answer_text',
    aggfunc='first'
)
print(pivot)
```

### Example 3: Analyze Policy Topics

```python
from collections import Counter

# Get all priority titles
titles = df_maerkesager['priority_title'].tolist()

# Find common words
words = ' '.join(titles).lower().split()
common = Counter(words).most_common(20)
print(common)
```

---

## 🐛 Troubleshooting

### Issue: Button Not Found

**Symptoms:**
```
⚠ Could not find 'vis alle' button
✓ Extracted 0 test answers
```

**Solutions:**

1. **Check if button exists manually:**
   - Visit candidate page in browser
   - Look for "vis alle" or similar button
   - Note the exact button text

2. **Update button text list:**
```python
button_texts = [
    'vis alle',
    'your_custom_text_here',  # Add found text
    # ...
]
```

3. **Inspect button element:**
   - Right-click button → Inspect
   - Note CSS classes or IDs
   - Add to selectors list

4. **Try non-headless mode:**
```python
driver = setup_driver(headless=False)
# Watch what happens on screen
```

### Issue: Test Answers Extraction Failing

**Symptoms:**
```
✓ Clicked 'vis alle' button
✓ Extracted 0 test answers
```

**Solutions:**

1. **Increase wait time after click:**
```python
time.sleep(5)  # Wait longer for content to load
```

2. **Check page structure:**
   - After clicking button, inspect HTML
   - Look for question/answer structure
   - Update selectors in `extract_test_answers_after_click()`

3. **Enable verbose logging:**
```python
# Add print statements to see what's being found
for elem in soup.find_all('div'):
    if 'question' in str(elem.get('class', '')).lower():
        print(f"Found: {elem}")
```

### Issue: Mærkesager Not Parsing Correctly

**Symptoms:**
```
✓ Found 3 mærkesager
# But titles and descriptions are empty
```

**Solutions:**

1. **Check HTML structure manually:**
   - View page source
   - Find mærkesager section
   - Note exact HTML structure

2. **Adjust parsing logic:**
```python
# In extract_maerkesager_improved()
# Update selectors based on actual structure
priority_list = container.find_next('div', class_='your-class-here')
```

3. **Use fallback method:**
   - The scraper has multiple methods
   - Check which one is being used
   - Adjust the active method

---

## 📈 Expected Results

### Data Completeness Goals

With the refined scraper, you should achieve:

| Field | Expected Completeness |
|-------|----------------------|
| Name | 100% |
| Party | 100% |
| Municipality | 100% |
| Uddannelse | 85-95% |
| Bopæl | 85-95% |
| Mærkesager | 90-100% |
| **Test Answers** | **85-100%** ⭐ |

### Test Answer Coverage

If the "vis alle" button clicking works properly, you should get:
- **19/19 answers** for most candidates
- **Full question text** for each answer
- **Complete answer text** for each question

### Mærkesager Structure

You should see:
- **Titles extracted** for 80-100% of priorities
- **Descriptions separated** from titles
- **Full text** always available as fallback

---

## 🔄 Version Comparison

| Feature | Basic | Enhanced | Refined ⭐ |
|---------|-------|----------|-----------|
| Basic info | ✅ | ✅ | ✅ |
| Om section | ❌ | ✅ | ✅ |
| Mærkesager | ✅ | ✅ | ✅✅ Better |
| Mærkesager structure | Number + Text | Number + Text | **Number + Title + Description** |
| Test answers | ❌ | Partial | ✅✅ Complete |
| Button clicking | ❌ | ❌ | ✅ **NEW** |
| Question text | ❌ | ❌ | ✅ **NEW** |
| Multiple output formats | ✅ | ✅ | ✅✅ More |

**Recommendation:** Use the **Refined version** for complete, well-structured data.

---

## 🎓 Advanced Usage

### Custom Button Selectors

If DR changes their button structure, update the selectors:

```python
def click_vis_alle_button(driver, max_attempts=3):
    # Add your custom selectors here
    custom_selectors = [
        'button[data-testid="show-all"]',
        '.custom-button-class',
        '#show-answers-button'
    ]
    
    for selector in custom_selectors:
        try:
            button = driver.find_element(By.CSS_SELECTOR, selector)
            driver.execute_script("arguments[0].click();", button)
            return True
        except:
            continue
```

### Parallel Scraping

For faster scraping of multiple municipalities:

```python
from concurrent.futures import ThreadPoolExecutor

def scrape_one_municipality(muni_id):
    driver = setup_driver()
    # ... scrape logic
    driver.quit()
    return candidates

with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(scrape_one_municipality, municipality_ids)
```

⚠️ Be respectful to the server - don't use too many workers!

---

## 📞 Support

### If Test Answers Still Not Working

The test answers may be loaded via:
1. **AJAX requests** - May need to intercept network requests
2. **React/Vue components** - May need to wait for JavaScript
3. **Authentication** - May require login (unlikely for public data)

If standard methods fail, consider:
- Using browser automation tools to record and replay actions
- Checking browser Network tab to see how data is loaded
- Looking for API endpoints that return JSON data directly

### Share Your Findings

If you discover better selectors or methods, please contribute back! Add comments to the notebook with your improvements.

---

## ✅ Success Checklist

After running the scraper, verify:

- [ ] Test candidate shows "✓ Clicked 'vis alle' button"
- [ ] Test candidate shows "✓ Extracted 19 test answers"
- [ ] Mærkesager have separated titles and descriptions
- [ ] `df_svars_wide` has 38 columns (19 questions + 19 answers)
- [ ] `df_svars_long` has rows for each question-answer pair
- [ ] All CSV files are created
- [ ] JSON file contains complete nested data

---

## 🎉 Summary

The **refined scraper** is the most complete solution:

✅ **Clicks buttons** to reveal hidden content  
✅ **Extracts 19 test answers** with questions  
✅ **Parses mærkesager** with better structure  
✅ **Multiple output formats** for different analyses  
✅ **Robust error handling** with fallback methods  
✅ **Complete biographical data** from Om section  

Use this version for comprehensive candidate database creation!

---

*Last updated: November 2025*
*Based on DR's municipal election website structure as of KV25*
