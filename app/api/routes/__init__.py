from fastapi import APIRouter

from app.api.routes.activities import router as activities_router
from app.api.routes.buildings import router as buildings_router
from app.api.routes.organizations import router as organizations_router

router = APIRouter(
    tags=["organizations-directory"],
)
router.include_router(activities_router)
router.include_router(buildings_router)
router.include_router(organizations_router)
