# Handles the process of taking raw or cleaned text data (like manhwa summaries) 
# and generating embeddings (vector representations).
from models.manhwa import Manhwa
from models.embedding import Vector
from sentence_transformers import SentenceTransformer
from services.embedding_service import EmbeddingService
from utils.normalize_manhwa_vector import normalize_manhwa_vector


model = SentenceTransformer('all-MiniLM-L6-v2')


def embed_pipeline(manhwa: Manhwa) -> list:

    text, source = build_embedding_payload(manhwa)

    embedding = model.encode(text).tolist()
    

    normalized = normalize_manhwa_vector(manhwa, embedding, source, text)

    _manhwa = Vector(**normalized)

    service = EmbeddingService()
    service.upsert(_manhwa)




def build_embedding_payload(manhwa: Manhwa) -> tuple[str | None, str | None]:
    if manhwa.synopsis:
        return manhwa.synopsis, "synopsis"

    if manhwa.tags:
        return f"{manhwa.title}. Genres: {manhwa.tags}", "title+tags"

    return manhwa.title, "title"
