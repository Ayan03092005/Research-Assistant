from .http import get_json
from ..config.settings import settings

S2_BASE = "https://api.semanticscholar.org/graph/v1/paper/search"

async def search_semantic_scholar(query: str, limit: int = 20):
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,year,venue,externalIds,url,authors"
    }
    headers = {}
    if settings.SEMANTIC_SCHOLAR_API_KEY:
        headers["x-api-key"] = settings.SEMANTIC_SCHOLAR_API_KEY
    data = await get_json(S2_BASE, params=params, headers=headers or None)
    results = []
    for p in data.get("data", []):
        doi = (p.get("externalIds") or {}).get("DOI", "")
        authors = [a.get("name", "") for a in p.get("authors", [])]
        results.append({
            "title": p.get("title"),
            "first_author": authors[0] if authors else "Unknown",
            "year": str(p.get("year") or ""),
            "venue": p.get("venue") or "",
            "doi": doi,
            "url": p.get("url") or (f"https://doi.org/{doi}" if doi else ""),
            "provider": "semantic_scholar"
        })
    return results
