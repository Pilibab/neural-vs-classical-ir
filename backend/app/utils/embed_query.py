# app/utils/embed_query.py (or similar)
from sentence_transformers import SentenceTransformer

# Load the model once (Global) so it stays in memory
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_query_embedding(text: str) -> list:
    """Converts a search string into a vector for MongoDB."""
    if not text:
        return []
    # .tolist() is crucial because MongoDB doesn't accept numpy arrays
    return model.encode(text).tolist()