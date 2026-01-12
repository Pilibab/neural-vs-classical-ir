# Handles the process of taking raw or cleaned text data (like manhwa summaries) 
# and generating embeddings (vector representations).
from models.manhwa import Manhwa
from models.embedding import Vector
from sentence_transformers import SentenceTransformer
from services.embedding_service import EmbeddingService
from utils.normalize_manhwa_vector import normalize_manhwa_vector

model = SentenceTransformer('all-MiniLM-L6-v2')


def embed_pipeline(manhwa: Manhwa) -> list:

    synospsis_vector = model.encode(manhwa.synopsis).tolist()

    try:
        normalized = normalize_manhwa_vector(manhwa, synospsis_vector)

        manhwa = Vector(**normalized)

        EmbeddingService.upsert(manhwa)

        
    except Exception as e:
        print(e)

