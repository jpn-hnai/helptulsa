from pydantic import BaseModel
from typing import List, Any

class AskRequest(BaseModel):
    session_id: str
    question: str

class Resource(BaseModel):
    id: str
    name: str
    description: str
    url: str
    phone: str

class AskResponse(BaseModel):
    answer: str
    resources: List[Resource]
