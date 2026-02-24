from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.building import Building


def list_buildings(db: Session) -> list[Building]:
    query = select(Building).order_by(Building.id)
    return list(db.scalars(query).all())
