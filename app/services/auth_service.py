from app.db import database
from fastapi import HTTPException
from bson import ObjectId
import bcrypt
from app.utils.jwt_helper import create_access_token
from app.utils.convert_objectid_util import convert_objectid
import time

async def login(email: str, password: str):
    if database.db is None:
        raise HTTPException(status_code=500, detail="Database is not connected")

    start_time = time.time()
    users = database.db["users"]

    user = await users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    user_data = convert_objectid(user)
    user_data.pop("password", None)

    access_token = create_access_token({"user_id": str(user["_id"]), "email": email})

    execution_time = round((time.time() - start_time) * 1000, 2)

    return {
        "data": {
            "user": user_data,
            "auth": {
                "accessToken": access_token
            }
        },
        "metaData": {
            "status": "success",
            "responseCode": 200,
            "message": "Success",
            "executionTime": f"{execution_time} ms"
        }
    }

async def logout(token: str = None):
    try:
        return {
            "status": "success",
            "message": "Logout successful",
            "data": None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
