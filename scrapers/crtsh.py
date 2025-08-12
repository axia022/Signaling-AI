import requests, json, re
from .utils import now_iso, fp

AI_SUBSTR = ["ai","rag","agent","inference","vector","embed","studio","models","labs","ml"]

def run(company):
    domain = company.get("domain")
    if not domain: return []
    try:
        r = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=30)
        rows = r.json()
    except Exception:
        rows = []
    out = []
    for row in rows:
        name = (row.get("name_value") or "").lower()
        if any(k in name for k in AI_SUBSTR):
            out.append({
                "id": fp(domain, "crt", name, row.get("entry_timestamp")),
                "company_id": domain,
                "type": "domain",
                "title": name,
                "source_url": f"https://crt.sh/?q={domain}",
                "observed_at": now_iso(),
                "delta_metric": 1
            })
    return out
