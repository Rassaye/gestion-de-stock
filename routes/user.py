from typing import List
from pymongo.errors import DuplicateKeyError
from fastapi import APIRouter, HTTPException, status
from model.users import User
import utilities


router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get("", )
async def get_users() -> List[User]:
    users =await User.find_all().to_list()
    return users


@router.post("", response_model=dict)
async def create_user(user: User):
    user.password = utilities.hash_password(user.password)
    try:

        new_user = await user.create()
        return {
            "message": "User successfuly created",
            "id": str(new_user.id)
        }
    
    except DuplicateKeyError as e:
        error_details = e.details
        error_message = error_details.get('errmsg', str(e))
        
        error_info = {
            "error_description": "Duplicate entry detected",
            "error_message": error_message          
        }
        raise HTTPException(status_code=400, detail=error_info)
        

@router.get("/{user_id}", response_model=dict)
async def get_user_by_id(user_id: str):
    user = await User.get(user_id)
    if user is None:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding user with id: {user_id}'
        )
    #user["_id"] = str(user["_id"])
    return user

""" 
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
    return {"message": "User deleted successfully"} """