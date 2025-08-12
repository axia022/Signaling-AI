import feedparser
from .utils import now_iso, fp

KEYS = ["launch","beta","preview","generally available","partner","design partner","pilot","series","seed","pricing"]

def run(company):
    url = company.get("blog_rss")
    if not url: return []
    out = []
    d = feedparser.parse(url)
    for e in d.entries[:50]:
        title = e.get("title","")
        desc = e.get("summary","")
        text = f"{title} {desc}".lower()
        if any(k in text for k in KEYS):
            out.append({
                "id": fp(company["domain"], "rss", title),
                "company_id": company["domain"],
                "type": "product",
                "title": title,
                "source_url": e.get("link"),
                "observed_at": now_iso(),
                "delta_metric": 1
            })
    return out
