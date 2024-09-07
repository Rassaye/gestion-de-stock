from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from beanie import Document, Indexed


class Role(str, Enum):
    SUPER_ADMIN = "super_admin"
    SIMPLE_USER= "simple_user"

class User(Document):
    firstname: str
    lastname: str
    username: Indexed(str, unique=True) # type: ignore
    password: str
    email: Indexed(str, unique=True) # type: ignore
    role: Role
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
class UserInfo(BaseModel):
    username: str
    lastname: str
    firstname: str
    email: str
    role: str