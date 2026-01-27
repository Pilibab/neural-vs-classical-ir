from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

load_dotenv()


class Settings(BaseSettings):
    # MongoDB
    mongo_uri: str = Field(alias="MONGODB_LINK")
    db_name: str = Field(default="manhwa_db", alias="DB_NAME")

    # Collections
    vector_collection: str = Field(default="manhwa_vectors", alias="MANHWA_VECTOR_COLLECTION")
    data_collection: str = Field(default="manhwa_data", alias="MANHWA_DATA_COLLECTION")
    error_log_collection: str = Field(default="error_logs", alias="ERROR_LOGS_COLLECTION")
    frontend_url: str = Field(default="http://localhost:5173", alias="VITE_FRONTEND_URI")

    # Server
    port: int = Field(default=5000, alias="PORT")

    class Config:
        populate_by_name = True
        env_file = ".env"   # optional but explicit


settings = Settings()
