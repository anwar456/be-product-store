from fastapi import HTTPException
from app.services.product_service import add_product, update_product, get_products, get_product_by_id, delete_product
from app.models.product_model import ProductCreate, ProductUpdate, ProductList
from pymongo.errors import DuplicateKeyError

async def add_product_controller(product: ProductCreate):
    try:
        return await add_product(product.model_dump())
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Product already exists")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def update_product_controller(product: ProductUpdate):
    try:
        return await update_product(product.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def get_all_products_controller(body: ProductList):
    try:
        return await get_products(body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_product_by_id_controller(id: str):
    try:
        return await get_product_by_id(id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def delete_product_controller(id: str):
    try:
        return await delete_product(id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
