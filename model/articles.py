from typing import Optional
from pydantic import BaseModel, Field
from beanie import Document, Indexed


class Article(Document):
    id: Optional[str] = Field(default=None, description="MongoDB document ObjectID")
    code_id: Indexed(str, unique=True)
    name: str
    categorie_id: str
    description: str
    quantity: int

    class Settings:
        # The name of the collection to store these objects.
        name = "articles"
    class Config:
        schema_extra = {
            "example": {
                "id": "13HJJER8HH!888U",
                "code_id": "AZED345678TFV5",
                "name": "Abdulazeez",
                "categorie_id": "1",
                "description": "une description",
                "quantity": 40
            }
        }


class Article_Post(BaseModel):
    code_id: str
    name: str
    categorie_id: str
    description: str
    quantity: str