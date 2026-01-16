from pydantic import BaseModel
from typing import Literal

# issue 1:
# originally the plan was to have 2 vector that are computed from synopsis and title + genre
# it was suggested however to have only one vector and a tracer for the ff reason:
#   1.  Multiple vectors per document do not represent different meanings — they 
#       represent different signal quality levels for the same meaning
#   2.  retrival ambuiguity
#           q:  is retrieval ambiguity still a problem if we have different name / key for different vector?  
#           a:  yes -> 
#                       Vector search ranks vectors, not entities
#                       Keys do not influence similarity scoring
#                       Duplicate semantic representations distort rankings
#                       You are forced into query-time reconciliation


class Vector(BaseModel):
    source: str
    source_id: str | int
    title: str
    vector: list

    # quality indecator, tracks the source 
    embedding_source: Literal[
        "synopsis",
        "title+tags",
        "title"
    ]

    # the text that we will turn to a vector
    embedding_text: str