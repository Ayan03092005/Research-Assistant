import re

def normalize_query(q: str) -> str:
    return re.sub(r"\s+", " ", q).strip()

def first_author(authors: list[str]) -> str:
    return authors[0] if authors else "Unknown"
