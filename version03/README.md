# DR Municipal Election Candidate Scraper

Two Python notebooks for scraping candidate information from DR's municipal election pages.

## Files

1. **dr_candidate_scraper.ipynb** - Full-featured version using Selenium (recommended)
2. **dr_candidate_scraper_simple.ipynb** - Lightweight version using requests + BeautifulSoup

## Which Version to Use?

### Use Selenium Version (dr_candidate_scraper.ipynb) if:
- The website loads content dynamically with JavaScript
- You want more reliable scraping
- You can install Selenium and Chrome/ChromeDriver

### Use Simple Version (dr_candidate_scraper_simple.ipynb) if:
- You prefer a lightweight solution
- You have issues installing Selenium
- The website content is in the initial HTML response

## Installation

### For Selenium Version:
```bash
pip install selenium beautifulsoup4 pandas webdriver-manager requests lxml
```

You'll also need Chrome browser installed.

### For Simple Version:
```bash
pip install requests beautifulsoup4 pandas lxml
```

## Quick Start

1. Open either notebook in Jupyter
2. Run the installation cell
3. Run the setup cells
4. Modify the municipality URL (currently set to municipality 124)
5. Run the scraping cells
6. Data will be saved to CSV files

## Extracted Data Categories

### Basic Candidate Information:
- `candidate_id` - Unique identifier from URL
- `name` - Full name
- `party` - Political party (abbreviation)
- `municipality` - Municipality name
- `email` - Contact email (if available)
- `phone` - Phone number (if available)
- `url` - Candidate page URL
- `num_priorities` - Number of policy priorities listed

### Priority Information:
- `priority_number` - Priority ranking (1-10)
- `priority_text` - Full text of the policy priority

## Output Files

Both notebooks generate:
- `candidates_basic.csv` - One row per candidate with basic info
- `candidates_priorities.csv` - One row per priority (expanded format)
- `candidates_raw.json` - Complete raw data including all nested information

## Example Usage

### Scrape Single Municipality:
```python
municipality_url = "https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel/124"
candidates = scrape_municipality(municipality_url, max_candidates=5)
```

### Scrape Multiple Municipalities:
```python
municipality_ids = [124, 101, 147]
all_candidates = scrape_multiple_municipalities(municipality_ids, max_candidates_per_municipality=10)
```

## Data Analysis Features

Both notebooks include examples for:
- Counting candidates by party
- Counting candidates by municipality
- Word frequency analysis in priorities
- Text analysis of policy positions

## Important Notes

1. **Be Respectful**: The notebooks include 1-2 second delays between requests to avoid overwhelming the server
2. **Testing**: Start with `max_candidates=5` to test before scraping all candidates
3. **Dynamic Content**: If the simple version returns empty data, use the Selenium version
4. **Error Handling**: Both versions include error handling and will continue if individual pages fail
5. **Danish Text**: Files are saved with UTF-8 encoding to properly handle Danish characters (æ, ø, å)

## Troubleshooting

### Selenium Issues:
- Make sure Chrome browser is installed
- ChromeDriver will be installed automatically via webdriver-manager
- If headless mode fails, try `setup_driver(headless=False)` to debug

### No Data Returned:
- Check if the website structure has changed
- Verify URLs are correct
- Try the Selenium version if using the simple version
- Check console output for error messages

### Unicode/Danish Characters:
- Make sure to use UTF-8 encoding when opening CSV files
- In Excel, use "Data → From Text/CSV" and select UTF-8 encoding

## Finding Municipality IDs

To find municipality IDs:
1. Go to https://www.dr.dk/nyheder/politik/kommunalvalg/din-stemmeseddel
2. Select a municipality
3. The URL will change to `.../din-stemmeseddel/[ID]`
4. Use that ID number in the scraper

## Customization

You can modify the scrapers to extract additional data by:
1. Inspecting the HTML structure with browser DevTools
2. Adding new fields to the `candidate_data` dictionary
3. Updating the parsing logic in `scrape_candidate_data()`

## Support

If you encounter issues:
1. Check that URLs are still valid
2. Verify the website structure hasn't changed
3. Try both versions to see which works better
4. Check the console output for specific error messages

## Legal & Ethical Considerations

- Respect robots.txt
- Use reasonable request delays
- Only scrape publicly available data
- Comply with DR's terms of service
- This tool is for research/analysis purposes
