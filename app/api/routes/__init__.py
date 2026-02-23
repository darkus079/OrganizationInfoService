from fastapi import APIRouter, Depends

from app.api.dependencies.auth import verify_api_key

router = APIRouter(
    dependencies=[Depends(verify_api_key)],
    tags=["protected"],
)
