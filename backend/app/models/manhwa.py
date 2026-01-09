from pydantic import BaseModel
from typing import List, Optional

class Manhwa(BaseModel):
    # id: Optional[str]
    source: str
    source_id: str | int
    rank: int | str
    title: str
    synopsis: str
    hashed_synopsis: str
    cover_image_url: str
    rating: float | str
    chapters: int | str
    published_date: str
    tags: List[str]
    link: str
