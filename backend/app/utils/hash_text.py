import hashlib

def hash_text(text: str) -> str:
    if not text:
        return ""

    normalized = text.strip().lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
