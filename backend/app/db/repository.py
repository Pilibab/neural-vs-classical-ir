# db/base_repository.py
from pymongo.collection import Collection
from models.manhwa import Manhwa

class Repository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def insert(self, doc: dict):
        return self.collection.insert_one(doc)

    def update(self, _id, doc: dict):
        return self.collection.update_one(
            {"_id": _id},
            {"$set": doc}
        )

    def find_one(self, query: dict):
        return self.collection.find_one(query)

    def find_by_source(self, source: str, source_id: str):
        return self.find_one({
            "source": source,
            "source_id": source_id
        })

    def find_by_source_ids(self, source_ids: list[str]) -> list[Manhwa]:
        """Pure data-access method"""
        return list(
            self.collection.find(
                {"source_id": {"$in": source_ids}},
                {"_id":0}
            )
        )
