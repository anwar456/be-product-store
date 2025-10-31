from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional, Any
from datetime import datetime


class UserRegister(BaseModel):
    name: str
    phoneNumber: str
    email: EmailStr
    password: str
    status: str
    permissionId: str
    privileges: List[str] = []
    image: Optional[str] = ""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "string",
                "phoneNumber": "string",
                "email": "string",
                "password": "string",
                "status": "string",
                "permissionId": "string",
                "privileges": [],
                "image": "string",
            }
        }
    )

class UserUpdate(BaseModel):
    id: str = Field(..., description="User ID to update")
    name: Optional[str] = None
    phoneNumber: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[str] = None
    permissionId: Optional[str] = None
    privileges: Optional[List[str]] = []
    image: Optional[str] = ""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "string",
                "name": "string",
                "phoneNumber": "string",
                "email": "string",
                "status": "string",
                "permissionId": "string",
                "privileges": [],
                "image": "string",
            }
        }
    )


class FilterItem(BaseModel):
    field: str
    value: Any


class UserList(BaseModel):
    search: Optional[str] = ""
    searchBy: List[str] = []
    orderBy: Optional[str] = "createdAt"
    order: Optional[str] = "desc"
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1)
    filters: List[FilterItem] = []
