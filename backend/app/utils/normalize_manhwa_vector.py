def normalize_manhwa_vector(
    source: str,
    source_id: str | int,
    title: str,
    vector: list,
):
    """
    Normalizes manhwa vector data with type validation and fallback defaults.
    
    Args:
        source: The source of the manhwa (e.g., 'myanimelist')
        source_id: The ID from the source
        title: The title of the manhwa
        vector: The embedding vector
    
    Returns:
        Dictionary with normalized vector data
    """
    # Validate source
    try:
        final_source = str(source) if source else "unknown"
    except (ValueError, TypeError):
        final_source = "unknown"
    
    # Validate source_id
    try:
        final_source_id = int(source_id)
    except (ValueError, TypeError):
        final_source_id = source_id
    
    # Validate title
    try:
        final_title = str(title) if title else ""
    except (ValueError, TypeError):
        final_title = ""
    
    # Validate vector
    try:
        if isinstance(vector, list):
            # Ensure all elements are numeric
            final_vector = [float(v) for v in vector]
        else:
            final_vector = []
    except (ValueError, TypeError):
        final_vector = []
    
    return {
        "source": final_source,
        "source_id": final_source_id,
        "title": final_title,
        "vector": final_vector,
    } 
    
