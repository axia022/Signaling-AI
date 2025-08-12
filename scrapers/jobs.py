import re, requests
from bs4 import BeautifulSoup
from .utils import now_iso, fp, title_is_ai

HEADERS = {"User-Agent": "Mozilla/5.0 (AI-Signal-Tracker)"}

def scrape_greenhouse(careers_url, company):
    # Supports typical Greenhouse boards: https://boards.greenhouse.io/<slug>
    out = []
    try:
        html = requests.get(careers_url, headers=HEADERS, timeout=30).text
    except Exception:
        return out
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.select("div.opening a[href]"):
        title = a.get_text(strip=True)
        if not title_is_ai(title):
            continue
        url = a["href"]
        out.append({
            "id": fp(company["domain"], "greenhouse", title, url),
            "company_id": company["domain"],
            "type": "hiring",
            "title": title,
            "source_url": url if url.startswith("http") else (careers_url.rstrip("/") + "/" + url.lstrip("/")),
            "observed_at": now_iso(),
            "delta_metric": 1
        })
    return out

def scrape_lever(careers_url, company):
    # Supports typical Lever boards: https://jobs.lever.co/<slug>
    out = []
    try:
        html = requests.get(careers_url, headers=HEADERS, timeout=30).text
    except Exception:
        return out
    soup = BeautifulSoup(html, "html.parser")
    for li in soup.select("div.posting a.posting-title"):
        title = li.get_text(" ", strip=True)
        if not title_is_ai(title):
            continue
        url = li["href"]
        out.append({
            "id": fp(company["domain"], "lever", title, url),
            "company_id": company["domain"],
            "type": "hiring",
            "title": title,
            "source_url": url,
            "observed_at": now_iso(),
            "delta_metric": 1
        })
    return out

def run(company):
    url = (company.get("careers_url") or "").lower()
    if "greenhouse.io" in url:
        return scrape_greenhouse(url, company)
    if "lever.co" in url:
        return scrape_lever(url, company)
    # TODO: add Ashby/Workday parsers if needed.
    return []
