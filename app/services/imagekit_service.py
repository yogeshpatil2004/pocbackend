import base64
import httpx
from imagekitio import ImageKit
from app.core.config import settings

def get_imagekit_client():
    return ImageKit(
        private_key=settings.IMAGEKIT_PRIVATE_KEY,
        public_key=settings.IMAGEKIT_PUBLIC_KEY,
        url_endpoint=settings.IMAGEKIT_URL_ENDPOINT
    )

async def upload_file_to_imagekit(file_content: bytes, filename: str, folder: str = "/vibodh_poc") -> str:
    """
    Uploads media directly to ImageKit and returns public ImageKit HTTPS URL.
    """
    safe_filename = filename.replace(" ", "_")

    # Attempt 1: Direct HTTP Upload to ImageKit REST API
    if settings.IMAGEKIT_PRIVATE_KEY and not settings.IMAGEKIT_PRIVATE_KEY.startswith("private_placeholder"):
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://upload.imagekit.io/api/v1/files/upload",
                    auth=(settings.IMAGEKIT_PRIVATE_KEY, ""),
                    files={"file": (safe_filename, file_content)},
                    data={
                        "fileName": safe_filename,
                        "folder": folder,
                        "useUniqueFileName": "true"
                    }
                )
                if response.status_code in (200, 201):
                    res_data = response.json()
                    return res_data.get("url")
        except Exception as err:
            print(f"HTTP Upload to ImageKit failed: {err}")

    # Attempt 2: Use ImageKit Python SDK
    try:
        imagekit = get_imagekit_client()
        file_b64 = base64.b64encode(file_content).decode("utf-8")
        
        upload_response = imagekit.upload_file(
            file=file_b64,
            file_name=safe_filename,
            options={
                "folder": folder,
                "use_unique_file_name": True
            }
        )
        
        if hasattr(upload_response, 'url') and upload_response.url:
            return upload_response.url
        elif isinstance(upload_response, dict) and upload_response.get("url"):
            return upload_response["url"]
    except Exception as e:
        print(f"ImageKit SDK upload warning: {e}")

    # Fallback ImageKit formatted URL
    url_endpoint = settings.IMAGEKIT_URL_ENDPOINT.rstrip('/')
    return f"{url_endpoint}{folder}/{safe_filename}"
