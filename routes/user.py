from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from app.database import db 
import utilities

users_collection = db["users"]

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get("", response_model=List[dict])
async def get_users():
    users = []
    async for user in users_collection.find({}):
        user["_id"] = str(user["_id"])
        users.append(user)
    return users


@router.post("", response_model=dict)
async def create_user(user: dict):
    user["password"] = utilities.hash_password(user["password"])
    new_user = await users_collection.insert_one(user)
    return {"id": str(new_user.inserted_id)}


@router.get("/{user_id}", response_model=dict)
async def get_user_by_id(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding user with id: {user_id}'
        )
    user["_id"] = str(user["_id"])
    return user


@router.patch("/{user_id}", response_model=dict)
async def update_user(user_id: str, updated_user: dict):
    await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user})
    return {"message": "User updated successfully"}


@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding user with id: {user_id}'
        )
    return {"message": "User deleted successfully"}


@router.post("/login", response_model=dict)
async def login(user_payload: dict):
    user = await users_collection.find_one({"email": user_payload["email"]})
    if user is  None:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utilisateur inexistant "
        )
    verif_password = utilities.verify_password(user_payload["password"], user["password"])

    if(not verif_password):
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Mot de passe non valide '
        )
    token = utilities.generate_token(str(user["_id"]), user["email"])
    return token