# db/base_repository.py
from pymongo.collection import Collection

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

    def find_all_that(self, ranked_source_ids: list):
        # Get the documents from Mongo
        results = list(self.collection.find({"source_id": {"$in": ranked_source_ids}}))
        
        # Sort the results based on the index of the ID in your input list
        # faster look up
        order_map = {id: pos for pos, id in enumerate(ranked_source_ids)}
        results.sort(key=lambda doc: order_map.get(doc["source_id"]))
        
        return results