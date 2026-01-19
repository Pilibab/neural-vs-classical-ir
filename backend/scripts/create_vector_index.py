# scripts/setup_vector_index.py
from pymongo.operations import SearchIndexModel

def create_manga_index(collection):
    search_index_model = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "path": "vector", # Your vector field name
                    "numDimensions": 384,
                    "similarity": "cosine"
                },
                {
                    "type": "filter",
                    "path": "source" # Your filter field name
                }
            ]
        },
        name="manga_vector_index",
        type="vectorSearch"
    )
    
    # Run this once and then check Atlas UI for the status
    collection.create_search_index(model=search_index_model)
    print("Manga index creation initiated.")