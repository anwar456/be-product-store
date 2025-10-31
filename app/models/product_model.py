from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any
from datetime import datetime


class ImageCloud(BaseModel):
    url: Optional[str] = None
    public_id: Optional[str] = None
    fileName: Optional[str] = None


class ProductCreate(BaseModel):
    category: str
    description: str
    images: List[ImageCloud] = Field(default_factory=list)
    name: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)
    status: str
    stock: int = Field(..., ge=0)
    unit: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "category": "string",
                "description": "string",
                "images": [],
                "name": "string",
                "price": 0,
                "status": "string",
                "stock": 0,
                "unit": "string",
            }
        }
    )


class ProductUpdate(BaseModel):
    id: str = Field(..., description="Product ID to update")
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    unit: Optional[str] = None
    status: Optional[str] = None
    images: Optional[List[ImageCloud]] = Field(default_factory=list)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "",
                "name": "string",
                "category": "string",
                "description": "string",
                "price": 0,
                "stock": 0,
                "unit": "string",
                "status": "string",
                "images": [],
            }
        }
    )


class FilterItem(BaseModel):
    field: str
    value: Any


class ProductList(BaseModel):
    search: Optional[str] = ""
    searchBy: List[str] = []
    orderBy: Optional[str] = "createdAt"
    order: Optional[str] = "desc"
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1)
    filters: List[FilterItem] = []
