from .hash_text import hash_text

def normalize_manhwa_data(
    source: str,
    source_id: str | int,
    rank: int | str,
    title: str,
    synopsis: str,
    cover_image_url: str,
    rating: float | str,
    chapters: str | int,
    published_date: str,
    tags: str | list,
    link: str,
):
    # Validate id
    try:
        final_source_id = int(source_id)
    except (ValueError, TypeError):
        final_source_id = source_id
    
    # Validate rank
    try:
        final_rank = int(rank)
    except (ValueError, TypeError):
        final_rank = "N/A"
    
    # Validate rating
    try:
        final_rating = float(rating)
    except (ValueError, TypeError):
        final_rating = "N/A"
    
    # Validate chapters
    try:
        final_chapters = int(chapters)
    except (ValueError, TypeError):
        final_chapters = "unknown"
    
    # Validate tags
    try:
        if isinstance(tags, list):
            final_tags = tags
        else:
            final_tags = [tag.strip() for tag in str(tags).split(",") if tag.strip()]
    except (ValueError, TypeError, AttributeError):
        final_tags = [] 

    # Validate other strings
    def validate_str(val, default="N/A"):
        return str(val) if val is not None else default

    # hashed for checking if synopsis changed 
    hashed_synopsis = hash_text(synopsis)

    return {
        "source":source,
        "source_id": final_source_id,
        "rank": final_rank,
        "title": validate_str(title, ""),
        "synopsis": validate_str(synopsis, ""),
        "hashed_synopsis": hashed_synopsis,
        "cover_image_url": validate_str(cover_image_url, ""),
        "rating": final_rating,
        "chapters": final_chapters,
        "published_date": validate_str(published_date, ""),
        "tags": final_tags,
        "link": validate_str(link, ""),
    }