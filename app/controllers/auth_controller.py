from fastapi import HTTPException
from app.services.auth_service import login, logout
from app.models.auth_model import LoginRequest


async def login_controller(payload: LoginRequest):
    try:
        response = await login(payload.email, payload.password)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def logout_controller(token: str = None):
    try:
        response = await logout(token)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))