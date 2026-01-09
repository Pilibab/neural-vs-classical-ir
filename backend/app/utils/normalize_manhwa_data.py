def normalize_manhwa_data(
    rank: int | str,
    title: str,
    synopsis: str,
    cover_image_url: str,
    rating: float | str,
    chapters: str | int,
    published_date: str,
    tags: str,
    link: str,
):
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
    
    # Validate other strings
    def validate_str(val, default="N/A"):
        return str(val) if val is not None else default

    return {
        "rank": final_rank,
        "title": validate_str(title, ""),
        "synopsis": validate_str(synopsis, ""),
        "cover_image_url": validate_str(cover_image_url, ""),
        "rating": final_rating,
        "chapters": final_chapters,
        "published_date": validate_str(published_date, ""),
        "tags": validate_str(tags, ""),
        "link": validate_str(link, ""),
    }