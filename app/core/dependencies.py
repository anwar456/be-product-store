from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException

bearer_scheme = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    
    from app.utils.jwt_helper import verify_access_token
    user = verify_access_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user
