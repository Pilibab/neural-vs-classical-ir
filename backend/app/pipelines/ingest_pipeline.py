# orchestration + validation of batch[idx]
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from utils.normalize_manhwa_data import normalize_manhwa_data

def ingest(manhwa_data):
    # Normalize the manhwa data from dict
    normalized_data = normalize_manhwa_data(
        rank=manhwa_data.get("rank"),
        title=manhwa_data.get("title"),
        synopsis=manhwa_data.get("synopsis"),
        cover_image_url=manhwa_data.get("cover_image_url"),
        rating=manhwa_data.get("rating"),
        chapters=manhwa_data.get("chapters"),
        published_date=manhwa_data.get("published_date"),
        tags=manhwa_data.get("tags"),
        link=manhwa_data.get("link")
    )
    
    return normalized_data

