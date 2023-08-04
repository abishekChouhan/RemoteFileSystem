from fastapi import APIRouter

from .endpoints import router

api_router = APIRouter()
api_router.include_router(router, prefix="/file_system", tags=["file-system"])
