# Snipper

**Snipper** is a simple Python tool that automates website reconnaissance by taking screenshots, detecting WAFs (Web Application Firewalls), and identifying technologies used on a website.

---

## Features

- Takes full-page screenshots of websites using Playwright.
- Checks if the domain resolves before scanning.
- Detects Web Application Firewalls using **WAFW00F**.
- Fingerprints technologies on the site using **Wappalyzer**.
- Outputs results in a Markdown file with embedded screenshots.

---

## Requirements

- Python 3.8+
- Install dependencies via pip:

```bash
git clone https://github.com/j4xx3n/Snipper.git
cd Snipper

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

chmod u+x snipper.py
```

## Usage

