from pydantic import BaseModel, Field, field_validator
from typing import Literal, List, Union
from models.manhwa import Manhwa

class Vector(BaseModel):
    source: str = "unknown"
    source_id: Union[str, int]
    title: str = ""
    vector: List[float] = Field(default_factory=list)
    
    # Quality indicators
    embedding_source: Literal["synopsis", "title+tags", "title"]
    embedding_text: str

    @field_validator("source", mode="before")
    @classmethod
    def validate_source(cls, v):
        return str(v) if v else "unknown"

    @field_validator("source_id", mode="before")
    @classmethod
    def validate_source_id(cls, v):
        try:
            return int(v)
        except (ValueError, TypeError):
            return v

    @field_validator("vector", mode="before")
    @classmethod
    def validate_vector(cls, v):
        if not isinstance(v, list):
            return []
        try:
            return [float(x) for x in v]
        except (ValueError, TypeError):
            return []

def normalize_manhwa_vector(
    manhwa: Manhwa, 
    synopsis_vector: list, 
    embedding_source: str, 
    text: str
) -> dict:
    """
    Normalizes manhwa vector data using the Pydantic Vector model.
    """
    # Instantiate the model (Pydantic performs validation automatically)
    vector_data = Vector(
        source=manhwa.source,
        source_id=manhwa.source_id,
        title=manhwa.title,
        vector=synopsis_vector,
        embedding_source=embedding_source,
        embedding_text=text
    )
    
    # Return as dict for your database/downstream task
    return vector_data.model_dump()