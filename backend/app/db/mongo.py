# mongo.py: creates MongoClient and db
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

db_link = os.environ.get("MONGODB_LINK")
client = MongoClient(f'{db_link}')

db = client.manhwa_db

print(f"Connecting to: {db_link}")
print(client.list_database_names())

manhwa_vector_collection = db.manhwa_vectors
manhwa_data_collection = db.manhwa_data
error_log = db.error_log_collection