from fastapi import APIRouter

from app.api.api_v1.endpoints import analyze, upload, search, history, analytics, settings

api_router = APIRouter()

api_router.include_router(analyze.router, prefix="/analyze", tags=["analysis"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])  
api_router.include_router(search.router, prefix="/search-sources", tags=["search"])
api_router.include_router(history.router, prefix="/history", tags=["history"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])