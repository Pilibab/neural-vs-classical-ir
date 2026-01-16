# services/manhwa_service.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from db.mongo import manhwa_vector_collection  # or however you get your DB connection
from db.repository import Repository
from models.embedding import Vector
from models.manhwa import Manhwa

class EmbeddingService:
    def __init__(self):
        # Initialize the repository with the manhwa collection
        self.repository = Repository(manhwa_vector_collection)  # or whatever your collection name is
    
    def get_by_source(self, source: str, source_id: str):
        """Get manhwa by source and source_id"""
        return self.repository.find_by_source(source, source_id)
    
    def insert(self, manhwa_embedded: Vector):
        """Insert a new Vector"""
        return self.repository.insert(manhwa_embedded.model_dump())
    
    def update(self, _id, Vector: Vector):
        """Update an existing Vector"""
        return self.repository.update(_id, Vector.model_dump())
    
    def upsert(self, manhwa_embedded: Vector):
        """Insert if doesn't exist, update if exists"""
        existing = self.get_by_source(manhwa_embedded.source, manhwa_embedded.source_id)
        
        if existing:
            print(f"\tUpdating existing manhwa_embedded: {manhwa_embedded.title}")
            return self.update(existing["_id"], manhwa_embedded)
        else:
            print(f"\tInserting new manhwa_embedded: {manhwa_embedded.title}")
            return self.insert(manhwa_embedded)