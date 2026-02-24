from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.organization import Organization


def list_organizations_by_building(db: Session, building_id: int) -> list[Organization]:
    query = (
        select(Organization)
        .where(Organization.building_id == building_id)
        .order_by(Organization.id)
    )
    return list(db.scalars(query).all())


def get_organization_by_id(db: Session, organization_id: int) -> Organization | None:
    query = (
        select(Organization)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.phones),
        )
        .where(Organization.id == organization_id)
    )
    return db.scalars(query).first()


def search_organizations_by_name(db: Session, name_query: str) -> list[Organization]:
    query = (
        select(Organization)
        .where(Organization.name.ilike(f"%{name_query}%"))
        .order_by(Organization.id)
    )
    return list(db.scalars(query).all())
