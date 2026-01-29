from models.search_result import SearchResult

def format_search_results(results: list) -> list[SearchResult]:
    """
    Takes the raw search results (with debug/bias info) and 
    returns only the essential fields for the user.
    """
    return [
        {
            "title": res.get("title"),
            "source": res.get("source"),
            "source_id": res.get("source_id"),
            "embedding_source": res.get("embedding_source"),
            "final_score": res.get("final_score"),
            "cover_image_url": res.get("cover_image_url"), 
        }
        for res in results
    ]