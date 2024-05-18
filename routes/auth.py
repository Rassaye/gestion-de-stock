from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from app.database import db 


users_collection = db["users"]

router = APIRouter(
    prefix='/users',
    tags=['Users']
)