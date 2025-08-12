import os, requests
from .utils import now_iso, fp

HEADERS = {"User-Agent":"AI-Signal-Tracker"}
if os.getenv("GITHUB_TOKEN"):
    HEADERS["Authorization"] = f"Bearer {os.getenv('GITHUB_TOKEN')}"

def run(company):
    org = company.get("github_org")
    if not org: return []
    out = []
    page = 1
    while True:
        r = requests.get(f"https://api.github.com/orgs/{org}/repos?per_page=100&page={page}", headers=HEADERS, timeout=30)
        if r.status_code != 200: break
        repos = r.json()
        if not repos: break
        for repo in repos:
            out.append({
                "id": fp(company["domain"], "gh", repo["full_name"], repo.get("pushed_at")),
                "company_id": company["domain"],
                "type": "oss",
                "title": f"{repo['name']} (★{repo.get('stargazers_count',0)})",
                "source_url": repo["html_url"],
                "observed_at": now_iso(),
                "delta_metric": repo.get("stargazers_count",0)
            })
        page += 1
    return out
