from pydantic import BaseModel, Field

class searchReqSchema(BaseModel):
    synopis: str = Field(min_length=5, max_length=1000)