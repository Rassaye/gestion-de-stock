from typing import Annotated, List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.database import db 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

stores_collection = db["stores"]

router = APIRouter(
    prefix='/stores',
    tags=['Stores']
)

# Fonction simulée pour vérifier le token (à remplacer par une vérification réelle)
def verifier_token(token: str) -> bool:
    # Logique de vérification du token ici
    if token == "valid_token":
        return True
    return False

# Fonction de dépendance pour vérifier le token
async def utilisateur_actuel(token: Annotated[str, Depends(oauth2_scheme)]):
    if not verifier_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"user_id": "id_utilisateur_exemple"}

@router.get("", response_model=List[dict])
async def get_stores(token: Annotated[str, Depends(oauth2_scheme)]):
    stores = []
    async for store in stores_collection.find({}):
        store["_id"] = str(store["_id"])
        stores.append(store)
    return stores

@router.post("", response_model=dict)
async def create_store(store: dict, token: Annotated[str, Depends(oauth2_scheme)]):
    new_store = await stores_collection.insert_one(store)
    return {"id": str(new_store.inserted_id)}

@router.get("/{store_id}", response_model=dict)
async def get_store_by_id(store_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    store = await stores_collection.find_one({"_id": ObjectId(store_id)})
    if store is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Aucun magasin correspondant avec l\'id: {store_id}'
        )
    store["_id"] = str(store["_id"])
    return store

@router.patch("/{store_id}", response_model=dict)
async def update_store(store_id: str, updated_store: dict, token: Annotated[str, Depends(oauth2_scheme)]):
    await stores_collection.update_one({"_id": ObjectId(store_id)}, {"$set": updated_store})
    return {"message": "Magasin mis à jour avec succès"}

@router.delete("/{store_id}", response_model=dict)
async def delete_store(store_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    result = await stores_collection.delete_one({"_id": ObjectId(store_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Aucun magasin correspondant avec l\'id: {store_id}'
        )
    return {"message": "Magasin supprimé avec succès"}
