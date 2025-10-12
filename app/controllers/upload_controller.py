from fastapi import UploadFile, File, HTTPException
from app.services.cloudinary_service import upload_file_to_cloudinary, delete_file_from_cloudinary

async def upload_file_controller(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="File is required")

    try:
        result = await upload_file_to_cloudinary(file.file)
        return {
            "message": "File uploaded successfully",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_file_controller(public_id: str):
    if not public_id:
        raise HTTPException(status_code=400, detail="public_id is required")

    try:
        result = await delete_file_from_cloudinary(public_id)
        return {
            "message": "File deleted successfully",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
