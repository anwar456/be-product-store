from fastapi import APIRouter, Depends
from app.controllers.user_controller import (
    register_user_controller, 
    get_all_users_controller, 
    delete_user_controller, 
    get_user_by_id_controller, 
    update_user_controller,
    reset_user_password_controller
)
from app.models.user_model import UserRegister, UserList, UserUpdate, UserResetPassword
from app.core.dependencies import get_current_user 

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/add")
async def add(user: UserRegister, current_user=Depends(get_current_user)):
    return await register_user_controller(user)

@router.put("/update")
async def update(body: UserUpdate, current_user=Depends(get_current_user)):
    return await update_user_controller(body)

@router.delete("/delete")
async def delete(id: str, current_user=Depends(get_current_user)):
    return await delete_user_controller(id)

@router.post("/get-all")
async def get_all(body: UserList, current_user=Depends(get_current_user)):
    return await get_all_users_controller(body)

@router.get("/get-one")
async def get_by_id(id: str, current_user=Depends(get_current_user)):
    return await get_user_by_id_controller(id)

@router.post("/reset-password")
async def reset_password(body: UserResetPassword, current_user=Depends(get_current_user)):
    return await reset_user_password_controller(body)

