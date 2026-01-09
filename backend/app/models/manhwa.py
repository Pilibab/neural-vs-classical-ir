from pydantic import BaseModel
from typing import List, Optional

class Manhwa(BaseModel):
    id: Optional[str]
    title: str
    synopsis: str
    cover_image_url: str
    rating: float | None
    chapters: int | None
    published_date: str | None
    tags: List[str]
    link: str
