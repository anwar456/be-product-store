import cloudinary
import cloudinary.uploader
import os
from fastapi.concurrency import run_in_threadpool

async def upload_file_to_cloudinary(file, folder=None):
    upload_folder = folder or os.getenv("CLOUDINARY_FOLDER", "uploads")
    try:
        result = await run_in_threadpool(
            cloudinary.uploader.upload,
            file,
            folder=upload_folder
        )
        return {
            "url": result.get("secure_url"),
            "public_id": result.get("public_id")
        }
    except Exception as e:
        raise Exception(f"Failed upload file: {str(e)}")

async def delete_file_from_cloudinary(public_id: str):
    try:
        result = await run_in_threadpool(
            cloudinary.uploader.destroy,
            public_id
        )
        return result
    except Exception as e:
        raise Exception(f"Failed delete file: {str(e)}")