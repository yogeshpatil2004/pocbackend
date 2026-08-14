from fastapi import APIRouter
from app.api.v1 import pocs, media, settings, admin, playground, training

api_router = APIRouter()

api_router.include_router(pocs.router, tags=["POCs"])
api_router.include_router(media.router, tags=["Media Upload"])
api_router.include_router(settings.router, tags=["Website Settings"])
api_router.include_router(admin.router, tags=["Admin Telemetry"])
api_router.include_router(playground.router, tags=["Playground"])
api_router.include_router(training.router, tags=["Training Materials"])
