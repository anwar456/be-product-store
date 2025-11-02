from app.models.user_model import UserRegister, UserList, UserUpdate
from app.services.user_service import register_user_service, get_users, get_user_by_id, delete_user, update_user, reset_user_password
from fastapi import HTTPException

async def register_user_controller(user: UserRegister):
    user_data = user.dict()
    try:
        result = await register_user_service(user_data)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def update_user_controller(product: UserUpdate):
    try:
        return await update_user(product.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


async def get_all_users_controller(body: UserList):
    try:
        return await get_users(body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_user_by_id_controller(id: str):
    try:
        return await get_user_by_id(id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def delete_user_controller(id: str):
    try:
        return await delete_user(id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def reset_user_password_controller(body):
    return await reset_user_password(
        user_id=body.user_id,
        new_password=body.new_password
    )