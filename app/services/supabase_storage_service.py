import boto3
from botocore.config import Config
from app.core.config import settings

def get_s3_client():
    supabase_url = settings.SUPABASE_URL.rstrip('/')
    s3_endpoint = f"{supabase_url}/storage/v1/s3"

    return boto3.client(
        's3',
        endpoint_url=s3_endpoint,
        aws_access_key_id=settings.SUPABASE_STORAGE_ACCESS_KEY_ID,
        aws_secret_access_key=settings.SUPABASE_STORAGE_SECRET_ACCESS_KEY,
        region_name=settings.SUPABASE_STORAGE_REGION,
        config=Config(signature_version='s3v4')
    )

async def upload_file_to_supabase_storage(file_content: bytes, filename: str, content_type: str = "image/jpeg") -> str:
    """
    Uploads media directly to Supabase Storage S3 Bucket ('vibodh_assets').
    Returns public HTTPS URL: https://[PROJECT_REF].supabase.co/storage/v1/object/public/vibodh_assets/[FILENAME]
    """
    supabase_url = settings.SUPABASE_URL.rstrip('/')
    bucket = settings.SUPABASE_STORAGE_BUCKET
    safe_filename = filename.replace(" ", "_")
    public_url = f"{supabase_url}/storage/v1/object/public/{bucket}/{safe_filename}"

    try:
        s3 = get_s3_client()
        s3.put_object(
            Bucket=bucket,
            Key=safe_filename,
            Body=file_content,
            ContentType=content_type
        )
        return public_url
    except Exception as e:
        print(f"Supabase S3 upload warning: {e}")
        return public_url
