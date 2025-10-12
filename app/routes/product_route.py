from fastapi import APIRouter, Depends
from app.models.product_model import ProductCreate, ProductUpdate, ProductList
from app.controllers.product_controller import (
    add_product_controller, 
    update_product_controller, 
    get_all_products_controller, 
    get_product_by_id_controller, 
    delete_product_controller
)
from app.core.dependencies import get_current_user 

router = APIRouter(prefix="/product", tags=["Product"])

@router.post("/add")
async def add(body: ProductCreate, user=Depends(get_current_user)):
    return await add_product_controller(body)

@router.put("/update")
async def update(body: ProductUpdate, user=Depends(get_current_user)):
    return await update_product_controller(body)

@router.delete("/delete")
async def delete(id: str, user=Depends(get_current_user)):
    return await delete_product_controller(id)

@router.post("/get-all")
async def get_all(body: ProductList, user=Depends(get_current_user)):
    return await get_all_products_controller(body)

@router.get("/get-one")
async def get_by_id(id: str, user=Depends(get_current_user)):
    return await get_product_by_id_controller(id)
