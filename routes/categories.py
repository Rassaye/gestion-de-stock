from typing import Annotated, List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.database import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

categories_collection = db["categories"]

router = APIRouter(
    prefix='/categories',
    tags=['Categories']
)




@router.get("", response_model=List[dict])
async def get_categories():
    categories = []
    async for category in categories_collection.find({}):
        category["_id"] = str(category["_id"])
        categories.append(category)
    return categories

@router.post("", response_model=dict)
async def create_category(category: dict, token: Annotated[str, Depends(oauth2_scheme)]):
    new_category = await categories_collection.insert_one(category)
    return {"id": str(new_category.inserted_id)}

@router.get("/{category_id}", response_model=dict)
async def get_category_by_id(category_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    category = await categories_collection.find_one({"_id": ObjectId(category_id)})
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Aucune catégorie correspondante avec l\'id: {category_id}'
        )
    category["_id"] = str(category["_id"])
    return category

@router.patch("/{category_id}", response_model=dict)
async def update_category(category_id: str, updated_category: dict, token: Annotated[str, Depends(oauth2_scheme)]):
    await categories_collection.update_one({"_id": ObjectId(category_id)}, {"$set": updated_category})
    return {"message": "Catégorie mise à jour avec succès"}

@router.delete("/{category_id}", response_model=dict)
async def delete_category(category_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    result = await categories_collection.delete_one({"_id": ObjectId(category_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Aucune catégorie correspondante avec l\'id: {category_id}'
        )
    return {"message": "Catégorie supprimée avec succès"}
