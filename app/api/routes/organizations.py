from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.organizations import (
    get_organization_by_id,
    list_organizations_in_bounds,
    list_organizations_in_radius,
    search_organizations_by_name,
)
from app.schemas.organization import OrganizationDetailResponse, OrganizationListResponse

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get("/search/by-name", response_model=list[OrganizationListResponse])
def find_organizations_by_name(
    name: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
) -> list[OrganizationListResponse]:
    return search_organizations_by_name(db, name)


@router.get("/search/by-radius", response_model=list[OrganizationListResponse])
def find_organizations_by_radius(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(..., gt=0),
    db: Session = Depends(get_db),
) -> list[OrganizationListResponse]:
    return list_organizations_in_radius(
        db=db,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
    )


@router.get("/search/by-area", response_model=list[OrganizationListResponse])
def find_organizations_by_area(
    min_latitude: float = Query(..., ge=-90, le=90),
    max_latitude: float = Query(..., ge=-90, le=90),
    min_longitude: float = Query(..., ge=-180, le=180),
    max_longitude: float = Query(..., ge=-180, le=180),
    db: Session = Depends(get_db),
) -> list[OrganizationListResponse]:
    if min_latitude > max_latitude or min_longitude > max_longitude:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid rectangle bounds",
        )

    return list_organizations_in_bounds(
        db=db,
        min_latitude=min_latitude,
        max_latitude=max_latitude,
        min_longitude=min_longitude,
        max_longitude=max_longitude,
    )


@router.get("/{organization_id}", response_model=OrganizationDetailResponse)
def get_organization(
    organization_id: int,
    db: Session = Depends(get_db),
) -> OrganizationDetailResponse:
    organization = get_organization_by_id(db, organization_id)
    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )
    return organization
