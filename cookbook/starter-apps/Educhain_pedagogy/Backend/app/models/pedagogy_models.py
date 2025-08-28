from pydantic import BaseModel
from typing import Dict, Any, Optional

class ContentRequest(BaseModel):
    topic: str
    pedagogy: str
    params: Dict[str, Any] = {}

class ContentResponse(BaseModel):
    pedagogy: str
    topic: str
    content: Any

class PedagogyInfo(BaseModel):
    description: str
    parameters: Dict[str, str]

class BloomsTaxonomyParams(BaseModel):
    grade_level: str = "High School"
    target_level: str = "Intermediate"


