from pydantic import BaseModel, Field

class searchReqSchema(BaseModel):
    synopsis: str = Field(min_length=5, max_length=1000)
