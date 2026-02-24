from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.buildings import list_buildings
from app.repositories.organizations import list_organizations_by_building
from app.schemas.building import BuildingResponse
from app.schemas.organization import OrganizationListResponse

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.get("", response_model=list[BuildingResponse])
def get_buildings(db: Session = Depends(get_db)) -> list[BuildingResponse]:
    return list_buildings(db)


@router.get("/{building_id}/organizations", response_model=list[OrganizationListResponse])
def get_organizations_in_building(
    building_id: int,
    db: Session = Depends(get_db),
) -> list[OrganizationListResponse]:
    return list_organizations_by_building(db, building_id)
