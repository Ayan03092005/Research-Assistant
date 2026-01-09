from .http import get_json
from ..config.settings import settings

CROSSREF_BASE = "https://api.crossref.org/works"

async def search_crossref(query: str, rows: int = 20):
    params = {"query": query, "rows": rows, "mailto": settings.CROSSREF_MAILTO}
    data = await get_json(CROSSREF_BASE, params=params)
    items = data.get("message", {}).get("items", [])
    results = []
    for it in items:
        authors = [f"{a.get('given','')} {a.get('family','')}".strip() for a in it.get("author", [])]
        results.append({
            "title": (it.get("title") or [""])[0],
            "first_author": authors[0] if authors else "Unknown",
            "year": str(it.get("issued", {}).get("date-parts", [[None]])[0][0] or ""),
            "venue": (it.get("container-title") or [""])[0],
            "doi": it.get("DOI", ""),
            "url": (it.get("URL") or ""),
            "provider": "crossref"
        })
    return results
