# Installing Selenium and Chrome/ChromeDriver on macOS

Complete guide for setting up Selenium with Chrome on macOS (Intel and Apple Silicon).

---

## Prerequisites

- macOS 10.13 or later
- Python 3.7 or later
- Terminal access

---

## Method 1: Easy Way (Recommended) 🎯

This method uses `webdriver-manager` which **automatically** downloads and manages ChromeDriver for you!

### Step 1: Install Chrome Browser

If you don't have Chrome already installed:

**Option A: Download from website**
```bash
# Visit: https://www.google.com/chrome/
# Download and install the .dmg file
```

**Option B: Install via Homebrew**
```bash
brew install --cask google-chrome
```

### Step 2: Install Python Packages

```bash
pip install selenium webdriver-manager beautifulsoup4 pandas lxml
```

### Step 3: Test Installation

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# This will auto-download ChromeDriver if needed
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.google.com")
print("Success! Chrome opened.")
driver.quit()
```

**That's it!** The `webdriver-manager` package will automatically:
- Download the correct ChromeDriver version
- Match it to your Chrome browser version
- Handle updates automatically

---

## Method 2: Manual ChromeDriver Installation

If you prefer to manage ChromeDriver manually:

### Step 1: Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Chrome and ChromeDriver

```bash
# Install Chrome (if needed)
brew install --cask google-chrome

# Install ChromeDriver
brew install chromedriver
```

### Step 3: Remove macOS Quarantine Flag

macOS Gatekeeper may block ChromeDriver. Remove the quarantine attribute:

```bash
# For Apple Silicon (M1/M2/M3):
xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver

# For Intel Macs:
xattr -d com.apple.quarantine /usr/local/bin/chromedriver
```

### Step 4: Install Python Packages

```bash
pip install selenium beautifulsoup4 pandas lxml
```

### Step 5: Verify Installation

```bash
# Check ChromeDriver version
chromedriver --version

# Check Chrome version
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
```

---

## Method 3: Using Conda (Anaconda/Miniconda)

If you use Anaconda or Miniconda:

```bash
# Install packages via conda
conda install -c conda-forge selenium beautifulsoup4 pandas lxml

# Install webdriver-manager via pip
pip install webdriver-manager

# Or install ChromeDriver via Homebrew (manual method)
brew install chromedriver
xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
```

---

## Verification and Testing

### Quick Test Script

Create a file `test_selenium.py`:

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_selenium():
    """Test Selenium installation"""
    options = Options()
    options.add_argument('--headless')  # Run without browser window
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        # Using webdriver-manager
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        driver.get('https://www.google.com')
        print("✅ Selenium + Chrome working perfectly!")
        print(f"📄 Page title: {driver.title}")
        print(f"🌐 Current URL: {driver.current_url}")
        driver.quit()
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_selenium()
```

Run the test:
```bash
python test_selenium.py
```

### Test in Jupyter Notebook

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

try:
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.google.com')
    print("✅ Success!")
    print(f"Title: {driver.title}")
    driver.quit()
except Exception as e:
    print(f"❌ Error: {e}")
```

---

## Common Issues and Solutions

### Issue 1: "chromedriver cannot be opened because the developer cannot be verified"

**Solution:**
```bash
# Find ChromeDriver location
which chromedriver

# Remove quarantine flag
xattr -d com.apple.quarantine /path/to/chromedriver

# Or if that doesn't work, try:
sudo spctl --master-disable  # Temporarily disable Gatekeeper
# Then re-enable after allowing ChromeDriver:
sudo spctl --master-enable
```

### Issue 2: Permission Denied

**Solution:**
```bash
chmod +x /path/to/chromedriver
```

### Issue 3: Chrome Version Mismatch

**Error:** `SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version XX`

**Solution:**

If using `webdriver-manager` (recommended):
```bash
# It should auto-update, but you can force it:
pip install --upgrade webdriver-manager
```

If using Homebrew:
```bash
# Update Chrome
brew upgrade --cask google-chrome

# Update ChromeDriver
brew upgrade chromedriver

# Remove quarantine flag again
xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
```

### Issue 4: ChromeDriver Not Found in PATH

**Solution:**
```bash
# For Homebrew ChromeDriver, add to PATH in ~/.zshrc or ~/.bash_profile:
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc  # Apple Silicon
# or
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bash_profile  # Intel Mac

# Reload shell configuration
source ~/.zshrc  # or source ~/.bash_profile
```

### Issue 5: Apple Silicon (M1/M2/M3) Specific Issues

**Solution:**

Everything should work natively on Apple Silicon. If you have issues:

```bash
# Make sure you're using ARM64 Homebrew
which brew  # Should show /opt/homebrew/bin/brew

# If you have both Intel and ARM Homebrew, use the ARM version:
/opt/homebrew/bin/brew install chromedriver
```

### Issue 6: Selenium Module Not Found

**Solution:**
```bash
# Check which Python you're using
which python
python --version

# Install in the correct Python environment
pip install selenium

# Or use python3 explicitly
pip3 install selenium

# For Jupyter, install in the same environment
python -m pip install selenium
```

---

## Advanced Configuration

### Running Chrome in Headless Mode

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)
```

### Custom ChromeDriver Location

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service('/path/to/chromedriver')
driver = webdriver.Chrome(service=service)
```

### Logging and Debugging

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import logging

# Enable Selenium logging
logging.basicConfig(level=logging.DEBUG)

# Enable ChromeDriver logging
service = Service(log_path='/tmp/chromedriver.log')
driver = webdriver.Chrome(service=service)
```

---

## Best Practices

1. **Use webdriver-manager**: Automatically handles version compatibility
2. **Use headless mode**: Faster and doesn't require display
3. **Add proper waits**: Use WebDriverWait instead of time.sleep()
4. **Close drivers**: Always use `driver.quit()` or use context managers
5. **Handle exceptions**: Wrap driver code in try/except blocks

### Example Best Practice Code

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def scrape_with_selenium(url):
    """Best practice Selenium scraping"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = None
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        driver.get(url)
        
        # Wait for element instead of sleep
        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        return driver.page_source
        
    except Exception as e:
        print(f"Error: {e}")
        return None
        
    finally:
        if driver:
            driver.quit()
```

---

## Updating Selenium and ChromeDriver

### Update via pip

```bash
pip install --upgrade selenium webdriver-manager
```

### Update via Homebrew

```bash
brew upgrade chromedriver
xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
```

### Check Versions

```bash
# Check Selenium version
pip show selenium

# Check ChromeDriver version
chromedriver --version

# Check Chrome version
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
```

---

## Uninstalling

If you need to uninstall:

```bash
# Uninstall Python packages
pip uninstall selenium webdriver-manager beautifulsoup4 pandas lxml

# Uninstall ChromeDriver (Homebrew)
brew uninstall chromedriver

# Uninstall Chrome (Homebrew)
brew uninstall --cask google-chrome

# Or manually delete Chrome
rm -rf /Applications/Google\ Chrome.app
```

---

## Additional Resources

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
- [webdriver-manager Documentation](https://github.com/SergeyPirogov/webdriver_manager)
- [Homebrew Website](https://brew.sh/)

---

## Quick Reference Commands

```bash
# Install everything (recommended method)
pip install selenium webdriver-manager beautifulsoup4 pandas lxml

# Manual ChromeDriver install
brew install chromedriver
xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver

# Test installation
python -c "from selenium import webdriver; driver = webdriver.Chrome(); driver.quit(); print('✅ Works!')"

# Check versions
chromedriver --version
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
pip show selenium

# Update everything
pip install --upgrade selenium webdriver-manager
brew upgrade chromedriver
```

---

## Summary

**For most users, Method 1 (webdriver-manager) is recommended** because it:
- ✅ Automatically downloads ChromeDriver
- ✅ Handles version matching
- ✅ Updates automatically
- ✅ Works on both Intel and Apple Silicon
- ✅ Requires minimal configuration

Just run:
```bash
pip install selenium webdriver-manager beautifulsoup4 pandas lxml
```

And you're ready to go! 🚀

---

*Last updated: November 2025*
