from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.activities import (
    get_activity_by_id,
    list_organizations_by_activity,
    list_organizations_by_activity_with_descendants,
)
from app.schemas.organization import OrganizationListResponse

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get(
    "/{activity_id}/organizations",
    response_model=list[OrganizationListResponse],
    summary="Получить организации по виду деятельности",
    description="Возвращает организации, привязанные к указанному виду деятельности.",
)
def get_organizations_by_activity(
    activity_id: int,
    db: Session = Depends(get_db),
) -> list[OrganizationListResponse]:
    activity = get_activity_by_id(db, activity_id)
    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )
    return list_organizations_by_activity(db, activity_id)


@router.get(
    "/{activity_id}/organizations/with-children",
    response_model=list[OrganizationListResponse],
    summary="Получить организации по деятельности с дочерними видами",
    description=(
        "Возвращает организации по виду деятельности с учетом дочерних узлов "
        "дерева деятельностей в пределах допустимой глубины."
    ),
)
def get_organizations_by_activity_tree(
    activity_id: int,
    db: Session = Depends(get_db),
) -> list[OrganizationListResponse]:
    activity = get_activity_by_id(db, activity_id)
    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )
    return list_organizations_by_activity_with_descendants(db, activity_id)
