import requests
from .utils import now_iso, fp

def run(company):
    org = company.get("hf_org")
    if not org: return []
    out = []
    for typ in ("models","datasets"):
        try:
            r = requests.get(f"https://huggingface.co/api/organizations/{org}/{typ}", timeout=30)
            items = r.json() if r.status_code == 200 else []
        except Exception:
            items = []
        for it in items:
            name = it.get("modelId") or it.get("id") or "item"
            last = it.get("lastModified") or it.get("lastModifiedAt") or ""
            tags = ", ".join(it.get("tags", [])[:6])
            out.append({
                "id": fp(company["domain"], "hf", typ, name, last),
                "company_id": company["domain"],
                "type": "model_update",
                "title": f"{typ}: {name} [{tags}]",
                "source_url": f"https://huggingface.co/{org}",
                "observed_at": now_iso(),
                "delta_metric": 1,
                "quality_flag": "apache-2.0" in tags.lower() or "mit" in tags.lower()
            })
    return out
