import csv, json, os, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scrapers import jobs, gh_repos, hf, crtsh, rss_sources
from scoring import score_signal

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CONFIG = ROOT / "config" / "companies.csv"

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def read_companies():
    rows = []
    with open(CONFIG, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            row = {k: (v.strip() if isinstance(v,str) else v) for k,v in row.items()}
            row["domain"] = row.get("domain") or row.get("name","").lower().replace(" ","") + ".com"
            rows.append(row)
    return rows

def load_existing():
    p = DATA / "signals.json"
    if p.exists():
        return json.loads(p.read_text())
    return []

def save_signals(sigs):
    (DATA / "signals.json").write_text(json.dumps(sigs, indent=2, ensure_ascii=False))

def save_rollup(sigs):
    # Simple per-company daily rollup top signals
    out = {}
    for s in sigs:
        cid = s["company_id"]
        out.setdefault(cid, {"company_id": cid, "signals": [], "score_7d": 0.0})
        out[cid]["signals"].append(s)
        out[cid]["score_7d"] += s.get("score", 0)
    (DATA / "rollup.json").write_text(json.dumps(list(out.values()), indent=2))

def main():
    companies = read_companies()
    prev = {s["id"]: s for s in load_existing()}
    new_sigs = []

    for c in companies:
        for mod in (jobs, gh_repos, hf, crtsh, rss_sources):
            try:
                arr = mod.run(c)
            except Exception as e:
                arr = []
            for s in arr:
                s["observed_at"] = s.get("observed_at") or now_iso()
                s["score"] = score_signal(s)
                if s["id"] not in prev:
                    new_sigs.append(s)
                    prev[s["id"]] = s
                else:
                    # keep the higher score/most recent
                    old = prev[s["id"]]
                    if s["score"] > old.get("score", 0):
                        prev[s["id"]] = s

    # Save merged
    all_sigs = sorted(prev.values(), key=lambda x: x.get("score",0), reverse=True)[:5000]
    save_signals(all_sigs)
    save_rollup(all_sigs)

    # Also write a lightweight site payload
    payload = {
        "generated_at": now_iso(),
        "top_signals": all_sigs[:200]
    }
    (ROOT / "site" / "signals.json").write_text(json.dumps(payload, indent=2))

if __name__ == "__main__":
    DATA.mkdir(parents=True, exist_ok=True)
    main()
