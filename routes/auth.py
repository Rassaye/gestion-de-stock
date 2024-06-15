from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.database import db 
import utilities


users_collection = db["users"]

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post("", response_model=dict)
async def login(user_payload: OAuth2PasswordRequestForm= Depends()):
    user = await users_collection.find_one({"email": user_payload.username})
    if user is  None:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utilisateur inexistant "
        )
    verif_password = utilities.verify_password(user_payload.password, user["password"])

    if(not verif_password):
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Mot de passe non valide '
        )
    token = utilities.generate_token(str(user["_id"]), user["email"])
    return token