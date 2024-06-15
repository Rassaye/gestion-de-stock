from typing import Optional
from beanie import Document, Indexed, init_beanie
from pydantic import BaseModel, Field


class Article(BaseModel):
    id: Optional[str] = Field(default=None, description="MongoDB document ObjectID")
    name: str
    description: str
    categorie_id: int
    quantity: int

class Article_Post(BaseModel):
    name: str
    description: str
    categorie_id: int
    quantity: int
 
 
       