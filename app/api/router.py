from fastapi import APIRouter, Depends

from app.api.dependencies.auth import verify_api_key
from app.api.routes import router as routes_router

api_router = APIRouter(
    dependencies=[Depends(verify_api_key)],
)
api_router.include_router(routes_router)
