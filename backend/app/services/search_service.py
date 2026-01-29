# app/services/search_service.py
from db.mongo import manhwa_vector_collection
from config import settings


def search_manhwa(query_vector, source="MAL"):
    pipeline = [
        # vector search
        {
            "$vectorSearch": {
                "index": "vector_index", 
                "path": "vector",
                "queryVector": query_vector,
                "numCandidates": 100,
                # 10 -> 20 to account for weight shift 
                "limit": 20,    
                "filter": {"source": source}
            }
        }, 
        {
            "$lookup": {
            "from": "manhwa_data",
            "localField": "source_id",  # Field in your vector collection
            "foreignField": "source_id",       # Field in your data collection
            "as": "metadata"            # Name of the temporary array
            }
        }, 
        {
            # FLATTEN
            "$unwind": {
                "path": "$metadata",
                "preserveNullAndEmptyArrays": True # Don't delete if no metadata found
            }
        },
        {
            # calculate weighted score 
            "$addFields": {
                "raw_vibe_score": { "$meta": "vectorSearchScore" },


                "weight": {
                    "$switch": {
                        "branches": [
                            { "case": { "$eq": ["$embedding_source", "synopsis"] }, "then": 1.0 },
                            { "case": { "$eq": ["$embedding_source", "title + tags"] }, "then": 0.8 },
                            { "case": { "$eq": ["$embedding_source", "title"] }, "then": 0.5 }
                        ],
                        "default": 0.1 # Fallback for unknown sources
                    }
                }, 
                #calculate bias
                "bias" : {
                    "$let": {
                        "vars": { "r": { "$ifNull": ["$metadata.rating", 0] } },
                        "in": {
                            "$cond": [
                                { "$gte": ["$$r", 8.5] }, 0.15, # Masterpiece Bonus
                                { "$cond": [{ "$gte": ["$$r", 7.0] }, 0.05, 0.0] } # Good Bonus
                            ]
                        }
                    }
                }
            }
        },
        {
            # final score = weight * base_score
            "$addFields": {
                "final_score": {
                    "$add": [
                        { "$multiply": ["$raw_vibe_score", "$weight"]}, 
                        "$bias" ]
                }
            }
        },
        {
            # Re-sort based on the new weighted score
            "$sort": { "final_score": -1 }
        },
        {
            # defines exactly which fields should be sent back to your backend 
            # by default all the data within a document is sent back 
            "$project": {
                "_id": 0,
                "title": "$metadata.title",
                "source": 1,
                "source_id": 1,        # Added this
                "embedding_source": 1,
                "cover_image_url": "$metadata.cover_image_url", 

                "actual_score": "$raw_vibe_score",
                "final_score": "$final_score",
                "debug_rating": "$metadata.rating",
                "debug_bias": "$bias"
            }
        }
    ]
    return list(manhwa_vector_collection.aggregate(pipeline))