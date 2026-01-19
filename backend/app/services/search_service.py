# app/services/search_service.py

from app.db.mongo import manhwa_vector_collection


def search_manhwa(query_vector, source="MAL"):
    pipeline = [
        {
            "$vectorSearch": {
                "index": "manhwa_vector_index", # Must match the script above
                "path": "vector",
                "queryVector": query_vector,
                "numCandidates": 100,
                "limit": 10,
                "filter": {"source": source}
            }
        }
    ]
    return list(manhwa_vector_collection.aggregate(pipeline))