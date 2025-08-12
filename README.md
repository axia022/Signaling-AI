# AI Signal Tracker (GitHub-only, $0)

A zero-cost pipeline that scrapes **public** signals for AI companies and publishes a daily dashboard via **GitHub Pages**, all powered by **GitHub Actions** on a schedule.

**Signals covered (MVP):**
- Hiring (Greenhouse/Lever boards, keyword-filtered for AI roles)
- Tech stack/domain signals via Certificate Transparency (crt.sh)
- Open-source traction (GitHub repos: stars, releases, pushes)
- Hugging Face org activity (new/updated models/datasets, tags)
- Company blogs/PR (RSS) and arXiv (company-affiliated authors)

> No paid tools. Everything runs in Actions and commits JSON snapshots to the repo. A static dashboard (site/) renders the latest Top Movers.

## Quick start
1. Click **Use this template** (after importing to your GitHub) or upload the ZIP you downloaded.
2. Edit `config/companies.csv` with your target companies.
3. Enable **Pages**: Settings → Pages → Build from `main` → `/site` folder.
4. Enable Actions. The default schedule is **daily at 8:00 UTC** and **manual run** is available.
5. Visit the Pages URL for your dashboard after the first run.

## How it works
- A scheduled workflow runs `pipeline/run.py`.
- Each scraper fetches deltas and writes to `data/signals.json` and `data/companies.json`.
- `scoring.py` assigns a 0–100 score per signal; a daily rollup file is created.
- The workflow commits the updates (new JSON) and optionally opens a PR/Discussion comment.
- `site/index.html` renders a table of the Top 50 signals with client-side JS.

## Add/extend
- Add more companies/fields to `config/companies.csv` (see header for supported columns).
- Add new scrapers under `scrapers/` and register them in `pipeline/run.py`.
- Tweak scoring in `scoring.py`.

## Legal/ToS
Only scrape endpoints you are allowed to access. This project intentionally avoids LinkedIn and other sites that disallow scraping. Focus on official job boards (Greenhouse/Lever), public APIs (Hugging Face, GitHub), RSS, and crt.sh.
