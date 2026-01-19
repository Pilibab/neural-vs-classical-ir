from pymongo import MongoClient
from app.config import settings

# Initialize Client
client = MongoClient(settings.mongo_uri)

# Access Database using setting
db = client[settings.db_name]

print(f"Connecting to: {settings.mongo_uri}")
print(f"Database: {settings.db_name}")

# Access Collections using settings
manhwa_vector_collection = db[settings.vector_collection]
manhwa_data_collection = db[settings.data_collection]
error_log_collection = db[settings.error_log_collection]