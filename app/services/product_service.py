from bson import ObjectId
from fastapi import HTTPException
from app.utils.convert_objectid_util import convert_objectid
import app.db.database as database 
import time

async def add_product(product_data):
    if database.db is None:
        raise Exception("Database is not connected")

    result = await database.db["products"].insert_one(product_data)

    return {
        "status": "success",
        "message": "Product added successfully",
        "id": str(result.inserted_id)
    }


async def get_products(query_params):
    if database.db is None:
        raise Exception("Database is not connected")

    start_time = time.time()
    collection = database.db["products"]

    mongo_query = {}

    if query_params.search and query_params.searchBy:
        mongo_query["$or"] = [
            {field: {"$regex": query_params.search, "$options": "i"}}
            for field in query_params.searchBy
        ]

    for f in query_params.filters:
        mongo_query[f.field] = f.value

    skip = (query_params.page - 1) * query_params.size
    limit = query_params.size
    sort_order = -1 if query_params.order == "desc" else 1

    cursor = collection.find(mongo_query)\
        .sort(query_params.orderBy, sort_order)\
        .skip(skip)\
        .limit(limit)

    results = await cursor.to_list(length=query_params.size)

    results = convert_objectid(results)

    total = await collection.count_documents(mongo_query)
    total_pages = (total + query_params.size - 1) // query_params.size

    execution_time = round((time.time() - start_time) * 1000, 2)

    return {
        "metaData": {
            "pagination": {
                "size": query_params.size,
                "totalElements": total,
                "totalPages": total_pages,
            },
            "status": "success",
            "responseCode": 200,
            "message": "Success",
            "executionTime": f"{execution_time} ms"
        },
        "data": results
    }
    
async def update_product(product_data):
    if database.db is None:
        raise Exception("Database is not connected")

    collection = database.db["products"]

    if "id" not in product_data or not product_data["id"]:
        raise HTTPException(status_code=400, detail="Product ID is required")

    product_id = product_data["id"]

    update_fields = {k: v for k, v in product_data.items() if k != "id"}

    result = await collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_fields}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "status": "success",
        "message": "Product updated successfully",
        "id": product_id
    }


async def get_product_by_id(product_id: str):
    if database.db is None:
        raise Exception("Database is not connected")

    collection = database.db["products"]

    try:
        product = await collection.find_one({"_id": ObjectId(product_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product["id"] = str(product["_id"])
    del product["_id"]

    return {
        "status": "success",
        "message": "Product retrieved successfully",
        "data": product
    }
    
async def delete_product(product_id: str):
    if database.db is None:
        raise Exception("Database is not connected")

    collection = database.db["products"]

    try:
        object_id = ObjectId(product_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    result = await collection.delete_one({"_id": object_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "status": "success",
        "message": "Product deleted successfully",
        "id": product_id
    }
