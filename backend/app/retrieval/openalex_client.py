from .http import get_json

OPENALEX_BASE = "https://api.openalex.org/works"

async def search_openalex(query: str, per_page: int = 20, year_from: int | None = None, year_to: int | None = None):
    params = {
        "search": query,
        "per_page": per_page,
        "mailto": "openalex@example.com"  # optional but polite
    }
    if year_from or year_to:
        yfrom = year_from or 1900
        yto = year_to or 2100
        params["from_publication_date"] = f"{yfrom}-01-01"
        params["to_publication_date"] = f"{yto}-12-31"
    data = await get_json(OPENALEX_BASE, params=params)
    results = []
    for w in data.get("results", []):
        results.append({
            "title": w.get("title"),
            "first_author": (w.get("authorships") or [{}])[0].get("author", {}).get("display_name", "Unknown"),
            "year": (w.get("publication_year") or ""),
            "venue": (w.get("host_venue") or {}).get("display_name", ""),
            "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
            "url": (w.get("primary_location") or {}).get("landing_page_url") or (w.get("primary_location") or {}).get("pdf_url"),
            "provider": "openalex"
        })
    return results
