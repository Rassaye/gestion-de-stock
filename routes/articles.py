
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from pymongo.errors import DuplicateKeyError
from model.articles import Article

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router = APIRouter(
    prefix='/articles',
    tags=['Articles']
)


@router.get("")
async def get_articles() -> List[Article]:
    # print(articles_collection.find_one({"_id": "66361e48fa1bfdcc510281ff"})   )
    # articles=await articles_collection.find_one({"_id": "66361e48fa1bfdcc510281ff"}) 
    # print(articles)
    articles= await Article.find_all().to_list()
    print (articles)
    return articles
   

    
@router.post("")
async def create_articles(article: Article, token: Annotated[str, Depends(oauth2_scheme)]):
    
    try:
        article_created= await article.create()
        return {"message": "Article ajouté avec succès"}
    except DuplicateKeyError as e:
        error_details = e.details
        error_message = error_details.get('errmsg', str(e))

        error_info = {
            "error_description": "Duplicate entry detected",
            "error_message": error_message          
        }
        raise HTTPException(status_code=400, detail=error_info)
        


@router.get("/{article_id}", response_model=Article)
async def get_article_by_id(article_id:  str, token: Annotated[str, Depends(oauth2_scheme)]) :
    article  = await Article.get(article_id)
    if article is None:
        raise HTTPException (
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'No corresponding product with id: {article_id}'
            )
    
    return article

""" @router.patch("/{article_id}")
async def update_article(article_id: str, updated_article: dict, token: Annotated[str, Depends(oauth2_scheme)]):
    await articles_collection.update_one({"_id": ObjectId(article_id)}, {"$set": updated_article})
    return {"message": "Article updated successfully"}


@router.delete("/{article_id}")
async def delete_article(article_id:  str, token: Annotated[str, Depends(oauth2_scheme)]):
    result = await articles_collection.delete_one({"_id": ObjectId(article_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding product with id: {article_id}'
        )
    return {"message": "Article deleted successfully"}


 """
