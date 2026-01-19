from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

load_dotenv()

class Settings(BaseSettings):
    # Connection Strings
    mongo_uri: str = Field(alias="MONGODB_LINK")
    db_name: str = Field(default="manhwa_db", alias="DB_NAME")
    
    # Collection Names
    vector_collection: str = "manhwa_vectors"
    data_collection: str = "manhwa_data"
    error_log_collection: str = "error_logs"

    class Config:
        populate_by_name = True

settings = Settings()