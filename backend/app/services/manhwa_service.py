# services/manhwa_service.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from db.mongo import manhwa_data_collection  # or however you get your DB connection
from db.repository import Repository
from models.manhwa import Manhwa

class ManhwaService:
    def __init__(self):
        # Initialize the repository with the manhwa collection
        self.repository = Repository(manhwa_data_collection)  # or whatever your collection name is
    
    def get_by_source(self, source: str, source_id: str):
        """Get manhwa by source and source_id"""
        return self.repository.find_by_source(source, source_id)
    
    def insert(self, manhwa: Manhwa):
        """Insert a new manhwa"""
        return self.repository.insert(manhwa.model_dump())
    
    def update(self, _id, manhwa: Manhwa):
        """Update an existing manhwa"""
        return self.repository.update(_id, manhwa.model_dump())
    
    def upsert(self, manhwa: Manhwa):
        """Insert if doesn't exist, update if exists"""
        existing = self.get_by_source(manhwa.source, manhwa.source_id)
        
        if existing:
            print(f"\tUpdating existing manhwa: {manhwa.title}")
            return self.update(existing["_id"], manhwa)
        else:
            print(f"\tInserting new manhwa: {manhwa.title}")
            return self.insert(manhwa)