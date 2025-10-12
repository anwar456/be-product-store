from fastapi import APIRouter, Header, Depends
from app.models.auth_model import LoginRequest
from app.controllers.auth_controller import login_controller, logout_controller
from app.core.dependencies import get_current_user 

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(payload: LoginRequest):
    return await login_controller(payload)

@router.post("/logout")
async def logout(authorization: str | None = Header(None), user=Depends(get_current_user)):
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]

    return await logout_controller(token)
