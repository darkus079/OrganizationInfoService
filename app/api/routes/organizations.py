from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.organizations import (
    get_organization_by_id,
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
