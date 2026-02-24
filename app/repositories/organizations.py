from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.building import Building
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


def list_organizations_in_radius(
    db: Session,
    latitude: float,
    longitude: float,
    radius_km: float,
) -> list[Organization]:
    distance_km = 6371.0 * func.acos(
        func.cos(func.radians(latitude))
        * func.cos(func.radians(Building.latitude))
        * func.cos(func.radians(Building.longitude) - func.radians(longitude))
        + func.sin(func.radians(latitude)) * func.sin(func.radians(Building.latitude))
    )

    query = (
        select(Organization)
        .join(Building, Building.id == Organization.building_id)
        .where(distance_km <= radius_km)
        .order_by(Organization.id)
    )
    return list(db.scalars(query).all())


def list_organizations_in_bounds(
    db: Session,
    min_latitude: float,
    max_latitude: float,
    min_longitude: float,
    max_longitude: float,
) -> list[Organization]:
    query = (
        select(Organization)
        .join(Building, Building.id == Organization.building_id)
        .where(Building.latitude >= min_latitude)
        .where(Building.latitude <= max_latitude)
        .where(Building.longitude >= min_longitude)
        .where(Building.longitude <= max_longitude)
        .order_by(Organization.id)
    )
    return list(db.scalars(query).all())
