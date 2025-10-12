from fastapi import APIRouter, UploadFile, File, Query, Depends
from app.controllers.upload_controller import upload_file_controller, delete_file_controller
from app.core.dependencies import get_current_user 

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...), user=Depends(get_current_user)):
    return await upload_file_controller(file)

@router.delete("/delete")
async def delete_file(public_id: str = Query(..., description="Cloudinary public_id file"), user=Depends(get_current_user)):
    return await delete_file_controller(public_id)
