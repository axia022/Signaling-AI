from datetime import datetime, timezone
import math

BASE = {
    "hiring": 25,
    "funding": 30,
    "product": 20,
    "techstack": 15,
    "domain": 10,
    "oss": 15,
    "model_update": 18,
    "research": 12,
    "customer": 20,
}

def score_signal(sig: dict) -> float:
    base = BASE.get(sig.get("type",""), 8)
    delta = sig.get("delta_metric", 0) or 0
    senior = 8 if sig.get("seniority_flag") else 0
    quality = 6 if sig.get("quality_flag") else 0

    mag = min(20.0, math.log1p(abs(delta)) * 6.0) if delta else 0.0

    ts = sig.get("observed_at")
    try:
        dt = datetime.fromisoformat(ts.replace("Z","")).replace(tzinfo=timezone.utc)
    except Exception:
        dt = datetime.now(timezone.utc)
    days = (datetime.now(timezone.utc) - dt).days
    decay = math.exp(-days / 14.0)

    return round((base + mag + senior + quality) * decay, 2)
