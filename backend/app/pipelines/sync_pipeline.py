from utils.normalize_manhwa_data import normalize_manhwa_data
from app.models.manhwa import Manhwa
from app.services.sync_service import SyncService

def sync(raw_manhwa: dict):
    try:
        normalized = normalize_manhwa_data(
            source=raw_manhwa.get("source"),
            source_id=raw_manhwa.get("source_id"),
            rank=raw_manhwa.get("rank"),
            title=raw_manhwa.get("title"),
            synopsis=raw_manhwa.get("synopsis"),
            cover_image_url=raw_manhwa.get("cover_image_url"),
            rating=raw_manhwa.get("rating"),
            chapters=raw_manhwa.get("chapters"),
            published_date=raw_manhwa.get("published_date"),
            tags=raw_manhwa.get("tags"),
            link=raw_manhwa.get("link"),
        )

        # schema enforcement 
        manhwa = Manhwa(**normalized)

        # persistence 
        SyncService.upsert(manhwa)
        

    except Exception as e:
        # log and skip
        print(e)