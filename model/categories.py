from typing import Optional
from pydantic import BaseModel, Field
from beanie import Document, Indexed


class Categorie(Document):
    id: Optional[str] = Field(default=None, description="MongoDB document ObjectID")
    name: str

    class Settings:
        # The name of the collection to store these objects.
        name = "categories"
    class Config:
        schema_extra = {
            "example": {
                "id": "13HJJER8HH!888U",
                "name": "Abdulazeez"
            }
        }
