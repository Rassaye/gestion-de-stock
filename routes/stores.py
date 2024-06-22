from typing import Annotated, List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from model.stores import Store
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router = APIRouter(
    prefix='/stores',
    tags=['Stores']
)

@router.get("")
async def get_stores()-> List[Store]:
    stores = Store.find_all().to_list()
    return stores

@router.post("")
async def create_store(store: Store, token: Annotated[str, Depends(oauth2_scheme)]):
    new_store = await store.create()
    return {"id": str(new_store.id)}

@router.get("/{store_id}")
async def get_store_by_id(store_id: str)-> Store:
    store = await Store.get(store_id)
    if store is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Aucun magasin correspondant avec l\'id: {store_id}'
        )
    #store["_id"] = str(store["_id"])
    return store
""" 
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
 """