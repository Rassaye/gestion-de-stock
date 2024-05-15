from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from app.database import db 

stores_collection = db["stores"]

router = APIRouter(
    prefix='/stores',
    tags=['Stores']
)

@router.get("", response_model=List[dict])
async def get_stores():
    stores = []
    async for store in stores_collection.find({}):
        store["_id"] = str(store["_id"])
        stores.append(store)
    return stores


@router.post("", response_model=dict)
async def create_store(store: dict):
    new_store = await stores_collection.insert_one(store)
    return {"id": str(new_store.inserted_id)}


@router.get("/{store_id}", response_model=dict)
async def get_store_by_id(store_id: str):
    store = await stores_collection.find_one({"_id": ObjectId(store_id)})
    if store is None:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding store with id: {store_id}'
        )
    store["_id"] = str(store["_id"])
    return store


@router.patch("/{store_id}", response_model=dict)
async def update_store(store_id: str, updated_store: dict):
    await stores_collection.update_one({"_id": ObjectId(store_id)}, {"$set": updated_store})
    return {"message": "Store updated successfully"}


@router.delete("/{store_id}", response_model=dict)
async def delete_store(store_id: str):
    result = await stores_collection.delete_one({"_id": ObjectId(store_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding store with id: {store_id}'
        )
    return {"message": "Store deleted successfully"}
