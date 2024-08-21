from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from beanie import Document, Indexed


class User(Document):
   
    username: Indexed(str, unique=True)
    password: str
    email: Indexed(str, unique=True)
    created_at: datetime = datetime.now()

    class Settings:
        # The name of the collection to store these objects.
        name = "users"
    class Config:
        schema_extra = {
            "example": {
                "id": "13HJJER8HH!888U",
                "username": "AZED345678TFV5",
                "password": "Abdulazeez",
                "email": "test@stock.gn",
                "created_at": datetime.now()
            }
        }