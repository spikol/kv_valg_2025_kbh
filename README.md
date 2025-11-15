# DR Municipal Election Candidate Scraper

A comprehensive web scraping tool for extracting candidate information from DR's Danish municipal election pages (Kommunalvalg).

## 📋 Overview

This project scrapes detailed candidate information from DR.dk including:
- **Basic Info**: Name, party, municipality
- **Personal Details**: Education (uddannelse), residence (bopæl), age, occupation (erhverv)
- **Policy Priorities**: Mærkesager (up to 10 priorities per candidate)
- **Test Answers**: Political position test responses (19 questions)
- **Social Media**: Links to candidate social media profiles

## 🚀 Features

- ✅ **Interactive Element Handling**: Clicks "vis alle" buttons to reveal all test answers
- ✅ **Robust Extraction**: Multiple fallback methods for reliable data collection
- ✅ **Error Handling**: Comprehensive retry logic and graceful failure handling
- ✅ **Multiple Output Formats**: CSV (wide & long format) and JSON
- ✅ **Batch Processing**: Scrape single candidates or entire municipalities
- ✅ **Headless Mode**: Run without browser UI for efficiency

## 📁 Project Structure

```
kv_project/
├── version01/              # Initial development versions
├── version02/              # Improved versions
├── version03/              # Latest refined version
│   └── dr_candidate_scraper_refined01.ipynb  # Main scraper
├── dr_candidate_scraper.ipynb                # Original version
├── dr_candidate_scraper_simple.ipynb         # Simplified version
├── macOS_Selenium_Installation_Guide.md      # Setup guide
└── README.md                                  # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.12+
- Chrome browser installed
- pip package manager

### Step 1: Upgrade pip and setuptools

If you're using Python 3.12, you need to upgrade pip first to avoid compatibility issues:

```bash
curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
python /tmp/get-pip.py --force-reinstall
python -m pip install --upgrade setuptools
```

### Step 2: Install Required Packages

```bash
pip install selenium webdriver-manager beautifulsoup4 pandas lxml requests
```

Or run the first cell in the Jupyter notebook:

```python
%pip install selenium webdriver-manager beautifulsoup4 pandas lxml
```

## 🎯 Quick Start

### Scrape a Single Candidate

```python
from selenium import webdriver
from scraper import setup_driver, scrape_candidate_refined

# Initialize driver
driver = setup_driver(headless=True)

# Scrape candidate
candidate_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/kandidater/kommune/..."
candidate_data = scrape_candidate_refined(candidate_url, driver)

# Close driver
driver.quit()
```

### Scrape All Candidates from a Municipality

```python
from scraper import scrape_municipality_refined

municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/49"
candidates = scrape_municipality_refined(municipality_url)
```

### Scrape Multiple Municipalities

```python
municipality_ids = [165, 153, 159, 161]  # Municipality IDs
all_candidates = scrape_multiple_municipalities(municipality_ids)
```

## 📊 Output Data

### Main Candidate DataFrame
```csv
candidate_id,name,party,municipality,uddannelse,bopael,alder,erhverv,num_priorities,num_test_answers,url
```

### Mærkesager (Policy Priorities) DataFrame
```csv
candidate_id,name,party,municipality,priority_number,priority_title,priority_description,priority_full_text
```

### Test Answers (Wide Format)
```csv
candidate_id,name,party,municipality,svar_1_question,svar_1_answer,svar_2_question,svar_2_answer,...
```

### Test Answers (Long Format)
```csv
candidate_id,name,party,municipality,question_number,question_text,answer_text
```

### Complete JSON
Full nested structure with all data in `candidates_complete_refined.json`

## 🔧 Configuration

### WebDriver Options

Customize the Chrome driver in `setup_driver()`:

```python
def setup_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless=new')
    options.add_argument('--window-size=1920,1080')
    # Add more options as needed
    return driver
```

### Scraping Parameters

- `wait_time`: Page load timeout (default: 15 seconds)
- `max_candidates`: Limit candidates per municipality
- `max_attempts`: Button click retry attempts (default: 3)

## 🐛 Troubleshooting

### Common Issues

**1. `AttributeError: module 'pkgutil' has no attribute 'ImpImporter'`**

This is a Python 3.12 compatibility issue. Solution:
```bash
curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
python /tmp/get-pip.py --force-reinstall
```

**2. ChromeDriver not found**

The `webdriver-manager` package should handle this automatically. If issues persist:
```bash
pip install --upgrade webdriver-manager
```

**3. Incomplete data extraction**

- Check if the page structure has changed
- Increase `wait_time` parameter
- Run in non-headless mode to debug: `setup_driver(headless=False)`

**4. Rate limiting**

Add delays between requests:
```python
time.sleep(2)  # Wait 2 seconds between candidates
```

## 📝 Example Usage

See the latest notebook: `version03/dr_candidate_scraper_refined01.ipynb`

The notebook includes:
1. Installation instructions
2. Single candidate test
3. Full municipality scrape
4. Data export to multiple formats
5. Summary statistics

## 🤝 Contributing

When making improvements:
1. Create a new version folder (e.g., `version04/`)
2. Test thoroughly with single candidates first
3. Document any new features or changes
4. Update this README

## ⚠️ Legal & Ethical Considerations

- **Respect robots.txt**: Check DR.dk's robots.txt before scraping
- **Rate Limiting**: Include delays between requests
- **Terms of Service**: Ensure compliance with DR.dk's terms
- **Data Usage**: Use scraped data responsibly and ethically
- **Attribution**: Credit DR.dk as the data source

## 📈 Data Quality

The scraper includes multiple extraction methods with fallbacks:
- **Method 1**: Structured HTML parsing
- **Method 2**: Text pattern matching
- **Method 3**: DOM traversal with regex

This ensures maximum data completeness even if page structure varies.

## 🔍 Municipality IDs

Common Copenhagen area municipalities:
- 49: Frederiksberg
- 101: Copenhagen
- 151: Ballerup
- 153: Brøndby
- 159: Gladsaxe
- 161: Glostrup
- 165: Albertslund
- 173: Lyngby-Taarbæk
- 183: Ishøj
- 187: Vallensbæk
- 190: Furesø
- 230: Rudersdal
- 253: Greve

## 📅 Project Status

**Current Version**: v3 (Refined)
**Last Updated**: November 2025
**Status**: Active Development

## 📄 License

This project is for educational and research purposes. Please respect data ownership and usage rights.

## 👤 Author

Developed for scraping Danish municipal election candidate data from DR.dk

---

**Note**: This scraper is designed for the 2025 municipal elections. Page structures may change for future elections.
