#!/usr/bin/env python3

import warnings
warnings.filterwarnings("ignore")
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import re
import os
import socket
import argparse
import requests
import urllib.parse
from pathlib import Path
from wafw00f.main import WAFW00F
from Wappalyzer import Wappalyzer, WebPage
from playwright.sync_api import sync_playwright

def take_screenshot_playwright(url, filename="screenshot.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(ignore_https_errors=True)

        print(f"Navigating to {url}...")
        page.goto(url)

        page.screenshot(path=filename, full_page=True)
        print(f"Screenshot saved as {filename}")

        browser.close()

def url_to_filename(url, max_length=150):
    decoded_url = urllib.parse.unquote(url)
    cleaned_url = re.sub(r'https?://(www\.)?', '', decoded_url)
    safe_filename = re.sub(r'[/:?#*|"<>\\]', '-', cleaned_url)
    safe_filename = re.sub(r'-+', '-', safe_filename)
    safe_filename = safe_filename.strip('.-')

    if len(safe_filename) > max_length:
        safe_filename = safe_filename[:max_length]
    return safe_filename

def domain_resolves(url):
    try:
        domain = urllib.parse.urlparse(url).netloc
        if not domain:
            return False
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False


def detect_waf(url):
    scanner = WAFW00F(url)
    wafs, attack_url = scanner.identwaf()

    if wafs:
        print(f"[+] WAF detected: {', '.join(wafs)}")
        return ", ".join(wafs)
    else:
        print("[-] No WAF detected.")

def detect_tech(url):
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
        webpage = WebPage.new_from_response(response)
        wappalyzer = Wappalyzer.latest()

        technologies = wappalyzer.analyze(webpage)

        for tech in technologies:
            print("-", tech)

        return "\n".join([f"- {t}" for t in technologies])

    except Exception as e:
        print("Error:", e)
        return "Error detecting technologies"

def main():
    parser = argparse.ArgumentParser(
        description="Snipper: Screenshot + WAF + Tech Fingerprinting Tool"
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="File containing list of URLs"
    )

    parser.add_argument(
        "-o", "--output",
        default="results",
        help="Output directory (default: results)"
    )

    args = parser.parse_args()

    OUTPUT_DIR = Path(args.output)
    SCREENSHOT_DIR = OUTPUT_DIR / "screenshots"
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    results_md = OUTPUT_DIR / "Snipper_Results.md"

    with open(args.input, 'r') as line:
        for url in line:
            current = url.strip()

            if not current.startswith(("http://", "https://")):
                current = "https://" + current

            if not domain_resolves(current):
                print(f"[SKIP] DNS failure for {current}")
                continue
            filename = url_to_filename(current) + ".png"
            path = SCREENSHOT_DIR / filename

            take_screenshot_playwright(current, path)

            waf_results = detect_waf(current)
            tech_results = detect_tech(current)

            md_image = f"""
---
# {current}

WAF Detection: **{waf_results}**

Technologies:
{tech_results}

![screenshots/{filename}](screenshots/{filename})


"""
            with open(results_md, 'a') as file:
                file.write(md_image)

if __name__ == "__main__":
    main()
