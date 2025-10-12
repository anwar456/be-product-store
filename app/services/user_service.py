import app.db.database as database
from bson import ObjectId, errors
from fastapi import HTTPException
from app.utils.convert_objectid_util import convert_objectid
import bcrypt
import time

async def register_user_service(user_data: dict):
    if database.db is None:
        raise Exception("Database is not connected")

    users = database.db["users"]

    existing = await users.find_one({"email": user_data.get("email")})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hashpw(
        user_data.get("password", "").encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")
    user_data["password"] = hashed_password

    permission_id = user_data.get("permissionId")
    if not permission_id:
        raise HTTPException(status_code=400, detail="permissionId is required")

    try:
        user_data["permissionId"] = ObjectId(permission_id)
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid permissionId")

    result = await users.insert_one(user_data)

    return {
        "status": "success",
        "message": "User registered successfully",
        "id": str(result.inserted_id)
    }

async def get_users(query_params):
    if database.db is None:
        raise HTTPException(status_code=500, detail="Database is not connected")

    start_time = time.time()
    collection = database.db["users"]

    mongo_query = {}

    if getattr(query_params, "search", None) and getattr(query_params, "searchBy", None):
        mongo_query["$or"] = [
            {field: {"$regex": query_params.search, "$options": "i"}}
            for field in query_params.searchBy
        ]

    for f in getattr(query_params, "filters", []):
        mongo_query[f.field] = f.value

    page = getattr(query_params, "page", 1)
    size = getattr(query_params, "size", 10)
    skip = (page - 1) * size
    limit = size

    order_by = getattr(query_params, "orderBy", "_id")
    sort_order = -1 if getattr(query_params, "order", "desc") == "desc" else 1

    cursor = collection.find(mongo_query)\
        .sort(order_by, sort_order)\
        .skip(skip)\
        .limit(limit)

    results = await cursor.to_list(length=size)

    results = convert_objectid(results)

    total = await collection.count_documents(mongo_query)
    total_pages = (total + size - 1) // size

    execution_time = round((time.time() - start_time) * 1000, 2)

    return {
        "metaData": {
            "pagination": {
                "size": size,
                "totalElements": total,
                "totalPages": total_pages,
                "page": page
            },
            "status": "success",
            "responseCode": 200,
            "message": "Success",
            "executionTime": f"{execution_time} ms"
        },
        "data": results
    }

async def update_user(user_data):
    if database.db is None:
        raise HTTPException(status_code=500, detail="Database is not connected")

    collection = database.db["users"]

    if "id" not in user_data or not user_data["id"]:
        raise HTTPException(status_code=400, detail="User ID is required")

    user_id = user_data["id"]

    allowed_fields = ["name", "phoneNumber", "email", "status", "permissionId", "privileges", "image"]
    update_fields = {k: v for k, v in user_data.items() if k in allowed_fields}

    if "permissionId" in update_fields:
        try:
            update_fields["permissionId"] = ObjectId(update_fields["permissionId"])
        except:
            raise HTTPException(status_code=400, detail="Invalid permission ID format")

    result = await collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_fields}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "status": "success",
        "message": "User updated successfully",
        "id": user_id
    }

async def get_user_by_id(user_id: str):
    if database.db is None:
        raise Exception("Database is not connected")

    collection = database.db["users"]

    try:
        user = await collection.find_one({"_id": ObjectId(user_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user = convert_objectid(user)

    return {
        "status": "success",
        "message": "User retrieved successfully",
        "data": user
    }
    
async def delete_user(user_id: str):
    if database.db is None:
        raise Exception("Database is not connected")

    collection = database.db["users"]

    try:
        object_id = ObjectId(user_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    result = await collection.delete_one({"_id": object_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "status": "success",
        "message": "User deleted successfully",
        "id": user_id
    }