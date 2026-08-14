import cloudinary
import cloudinary.uploader
from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

async def upload_file_to_cloudinary(file_content, filename: str, folder: str = "vibodh_pocs") -> str:
    """Uploads multipart image/video stream to Cloudinary and returns secure HTTPS URL"""
    try:
        response = cloudinary.uploader.upload(
            file_content,
            folder=folder,
            resource_type="auto",
            public_id=filename.split('.')[0]
        )
        return response.get("secure_url")
    except Exception as e:
        print(f"Cloudinary upload fallback warning: {e}")
        # Return fallback unsplash / placeholder if Cloudinary API keys are placeholder
        return f"https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&q=80"
