# main.py
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.routes import product_route, user_route, auth_route

app = FastAPI(title="Product Store API")

app.include_router(auth_route.router)
app.include_router(product_route.router)
app.include_router(user_route.router)

bearer_scheme = HTTPBearer()

async def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = authorization.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    from app.utils.jwt_helper import verify_access_token
    user = verify_access_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
