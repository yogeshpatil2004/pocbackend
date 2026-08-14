from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.imagekit_service import upload_file_to_imagekit
from app.services.supabase_storage_service import upload_file_to_supabase_storage

router = APIRouter()

@router.post("/media/upload")
async def upload_media(file: UploadFile = File(...)):
    """Uploads cover, banner, and media images to ImageKit (with Supabase fallback) and returns public URL."""
    try:
        content = await file.read()
        
        # Upload directly to ImageKit as primary storage
        url = await upload_file_to_imagekit(content, file.filename)
        
        return {
            "filename": file.filename,
            "url": url,
            "contentType": file.content_type,
            "provider": "imagekit"
        }
    except Exception as e:
        # Fallback to Supabase Storage if ImageKit upload fails completely
        try:
            url = await upload_file_to_supabase_storage(content, file.filename, file.content_type or "image/jpeg")
            return {
                "filename": file.filename,
                "url": url,
                "contentType": file.content_type,
                "provider": "supabase"
            }
        except Exception as sub_err:
            raise HTTPException(status_code=500, detail=f"Failed to upload media to ImageKit/Supabase: {str(e)}")
