import requests
from bs4 import BeautifulSoup
import os
import json
import time

# --------- CONFIGURATION ---------
TARGET_URLS = {
    "Hilton Pharma": "https://www.hiltonpharma.com",
    "GlaxoSmithKline Pakistan": "https://www.pk.gsk.com",
    "Getz Pharma": "https://www.getzpharma.com",
    "The Searle Company": "https://www.searlecompany.com",
    "Martin Dow": "https://www.martindow.com"
}

OUTPUT_DIR = "scraped"
JSON_FILE = os.path.join(OUTPUT_DIR, "scraped_data.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# --------- FUNCTION: SCRAPE SINGLE SITE ---------
def scrape_site(name, url):
    print(f"\n[+] Scraping: {name} ({url})")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        print(f"[-] Failed to fetch {url}: {e}")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # Create site folder
    site_dir = os.path.join(OUTPUT_DIR, name.replace(" ", "_"))
    os.makedirs(site_dir, exist_ok=True)

    # Save pretty HTML
    html_file = os.path.join(site_dir, "index.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    # Extract structured info
    data = {}
    data["url"] = url
    data["title"] = soup.title.string if soup.title else ""
    data["paragraphs"] = [p.get_text().strip() for p in soup.find_all("p")]
    data["links"] = [a.get("href") for a in soup.find_all("a", href=True)]

    # Save JSON for this site
    json_file = os.path.join(site_dir, "data.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[+] Scraped and saved HTML + JSON for {name}")
    return data

# --------- MAIN FUNCTION ---------
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_sites_data = {}

    for name, url in TARGET_URLS.items():
        site_data = scrape_site(name, url)
        if site_data:
            all_sites_data[name] = site_data
        time.sleep(2)  # polite delay

    # Save all sites data in one JSON
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(all_sites_data, f, indent=2, ensure_ascii=False)

    print(f"\n[+] All sites scraped successfully! Combined JSON: {JSON_FILE}")
    print(f"[+] Folder structure ready for GitHub + Snyk scanning.")

# --------- RUN ---------
if __name__ == "__main__":
    main()
