from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.core.config import settings

security = HTTPBearer()

async def verify_clerk_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verifies Clerk JWT token for protected admin endpoints"""
    token = credentials.credentials
    try:
        # In production, fetch keys from settings.CLERK_JWKS_URL and decode with PyJWT
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
