#!/usr/bin/env python3
import re
imom urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# ----- Edit these -----
START_URL = "https://example.com"
OUT_FILE = "pdf_links.txt"
# ----------------------

USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/115.0.0.0 Safari/537.36")
PDF_RE = re.compile(r'\.pdf(\?.*)?$', re.IGNORECASE)


def session_with_ua():
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def find_pdf_links(html, base):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].split("#", 1)[0]
        full = urljoin(base, href)
        if PDF_RE.search(full):
            links.add(full)
    return links


if __name__ == "__main__":
    s = session_with_ua()
    try:
        r = s.get(START_URL, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"Error fetching page: {e}")
        raise SystemExit(1)

    pdfs = find_pdf_links(r.text, START_URL)
    if not pdfs:
        print("No PDF links found.")
    else:
        with open(OUT_FILE, "w", encoding="utf-8") as f:
            for u in sorted(pdfs):
                f.write(u + "\n")
        print(f"Wrote {len(pdfs)} links to {OUT_FILE}")
