# orchestration + validation of batch[idx]
# app/pipelines/ingest_pipeline.py

import traceback
from ..utils.normalize_manhwa_data import normalize_manhwa_data
from ..models.manhwa import Manhwa
from ..services.manhwa_service import ManhwaService

def ingest(raw_manhwa: dict):
    print("ManhwaService:", ManhwaService)
    print("Type:", type(ManhwaService))
    print("Callable:", callable(ManhwaService))

    print("ManhwaService:", Manhwa)
    print("Type:", type(Manhwa))
    print("Callable:", callable(Manhwa))

    print("ManhwaService:", normalize_manhwa_data)
    print("Type:", type(normalize_manhwa_data))
    print("Callable:", callable(normalize_manhwa_data))

    try:
        print("normalizing")
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
        print("enforcing") 
        manhwa = Manhwa(**normalized)

        # persistence 
        print("upserting")

        service = ManhwaService()
        service.upsert(manhwa)

        print("upserted")

        return manhwa

    except Exception as e:
        traceback.print_exc()


