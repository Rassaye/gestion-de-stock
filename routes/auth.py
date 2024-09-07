from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from model.users import User, UserInfo
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from utils.auth import verify_password, generate_token, decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post("/login", response_model=dict)
async def login(user_payload: OAuth2PasswordRequestForm= Depends()):
    user = await User.find_one({"username": user_payload.username})
    print(user)
    if user is  None:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utilisateur inexistant "
        )
    verif_password = verify_password(user_payload.password, user.password)

    if(not verif_password):
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Mot de passe non valide '
        )
    token = generate_token(str(user.id), user.username)
    return token

@router.get("/me", response_model=UserInfo)
async def get_user_info(token: str = Depends(oauth2_scheme)):
    username = decode_token(token)  # Vérifie le token et obtient l'email

    print(username)
    user = await User.find_one(User.username == username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserInfo(
        username=user.username,
        lastname=user.lastname,
        firstname=user.firstname,
        email=user.email,
        role=user.role
    )