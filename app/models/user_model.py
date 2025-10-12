from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Any

class UserRegister(BaseModel):
    name: str
    phoneNumber: str
    email: EmailStr
    password: str
    status: bool = True
    permissionId: str
    privileges: List[str] = []
    image: Optional[str] = ""
    
class UserUpdate(BaseModel):
    id: str = Field(..., description="Product ID to update") 
    name: str 
    phoneNumber: str 
    email: EmailStr
    status: bool = True 
    permissionId: str 
    privileges: List[str] = [] 
    image: Optional[str] = ""
    
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