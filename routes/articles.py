
from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Response
from app.database import db 


articles_collection = db["articles"]

router = APIRouter(
    prefix='/articles',
    tags=['Articles']
)
all_article = [
    {
        "id": 1,
        "name": "Bon Lait",
        "description": "String",
        "categorie_id": 1,
        "quantity": 18
    },
    {
        "id": 2,
        "name": "Sardine",
        "description": "String",
        "categorie_id": 1,
        "quantity": 18
        
    }
]


@router.get("",response_model=List[dict])
async def get_articles():
    # print(articles_collection.find_one({"_id": "66361e48fa1bfdcc510281ff"})   )
    # articles=await articles_collection.find_one({"_id": "66361e48fa1bfdcc510281ff"}) 
    # print(articles)
    articles= []
    async for article in articles_collection.find({}):
        article["_id"] = str(article["_id"])
        articles.append(article)
    return articles
   

    
@router.post("")
async def create_articles(articles: dict):
    

    new_article = await articles_collection.insert_one(articles)
    print(new_article)
    return {"id": str(new_article.inserted_id)}


@router.get("/{article_id}")
async def get_article_by_id(article_id: str):
    article = await articles_collection.find_one({"_id": ObjectId(article_id)})
    if article is None:
        raise HTTPException (
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'No corresponding product with id: {article_id}'
            )
    article["_id"] = str(article["_id"])
    
    return article

@router.patch("/{article_id}")
async def update_article(article_id: str, updated_article: dict):
    await articles_collection.update_one({"_id": ObjectId(article_id)}, {"$set": updated_article})
    return {"message": "Article updated successfully"}


@router.delete("/{article_id}")
async def delete_article(article_id: str):
    result = await articles_collection.delete_one({"_id": ObjectId(article_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding product with id: {article_id}'
        )
    return {"message": "Article deleted successfully"}



