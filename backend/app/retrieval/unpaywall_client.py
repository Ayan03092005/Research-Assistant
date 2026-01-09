from .http import get_json
from ..config.settings import settings

UNPAYWALL_BASE = "https://api.unpaywall.org/v2/"

async def enrich_unpaywall(doi: str):
    if not doi:
        return None
    url = UNPAYWALL_BASE + doi
    params = {"email": settings.UNPAYWALL_EMAIL}
    try:
        data = await get_json(url, params=params)
        oa = data.get("best_oa_location") or {}
        return {
            "oa_url": oa.get("url"),
            "oa_pdf": oa.get("url_for_pdf"),
            "license": oa.get("license")
        }
    except Exception:
        return None
