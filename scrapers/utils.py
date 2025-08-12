import hashlib, re, time
from datetime import datetime, timezone

AI_TITLE_RE = re.compile(r"(ml|ai|llm|gen(erative)?\s*ai|prompt|nlp|computer\s*vision|rag|embedding|data\s*scientist)", re.I)

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def fp(*parts):
    h = hashlib.sha1(("::".join([str(p) for p in parts])).encode()).hexdigest()
    return h

def title_is_ai(title: str) -> bool:
    return bool(AI_TITLE_RE.search(title or ""))
