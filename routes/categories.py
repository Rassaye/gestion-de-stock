from typing import Annotated, List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from model.categories import Categorie, CategorieUpdate
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router = APIRouter(
    prefix='/categories',
    tags=['Categories']
)




@router.get("", status_code=200)
async def get_categories() -> List[Categorie]:
    categories=  await Categorie.find_all().to_list()
    return categories

@router.post("", response_model=dict, status_code=201)
async def create_category(payload: Categorie, token: Annotated[str, Depends(oauth2_scheme)]):
    new_category = await payload.create()
    return  {"message": "categorie ajouté avec succès"}

@router.get("/{category_id}", response_model=Categorie, status_code=200)
async def get_category_by_id(category_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    category = await Categorie.get(category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Aucune catégorie correspondante avec l\'id: {category_id}'
        )
    return category

@router.patch("/{category_id}", status_code=204)
async def update_category(category_id: str, payload: CategorieUpdate, token: Annotated[str, Depends(oauth2_scheme)]):
    # Récupérer l'article à partir de la base de données
    category = await Categorie.get(category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Categorie not found")

    # Mise à jour des champs si présents dans le payload
    if payload.name is not None:
        category.name = payload.name

    # Sauvegarde des modifications
    await category.save()
    return

@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    categorie = await Categorie.get(category_id)
    if not categorie:
        raise HTTPException(status_code=404, detail="Article not found")
    
    await categorie.delete()
    return 
