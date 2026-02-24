from sqlalchemy import Select, literal, select
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.organization import Organization
from app.models.organization_activity import organization_activities


def get_activity_by_id(db: Session, activity_id: int) -> Activity | None:
    query = select(Activity).where(Activity.id == activity_id)
    return db.scalars(query).first()


def list_organizations_by_activity(db: Session, activity_id: int) -> list[Organization]:
    query = (
        select(Organization)
        .join(
            organization_activities,
            organization_activities.c.organization_id == Organization.id,
        )
        .where(organization_activities.c.activity_id == activity_id)
        .order_by(Organization.id)
    )
    return list(db.scalars(query).all())


def list_organizations_by_activity_with_descendants(
    db: Session,
    activity_id: int,
) -> list[Organization]:
    base_tree: Select[tuple[int, int]] = select(
        Activity.id.label("id"),
        literal(1).label("depth"),
    ).where(Activity.id == activity_id)

    activity_tree = base_tree.cte(name="activity_tree", recursive=True)

    children = (
        select(
            Activity.id.label("id"),
            (activity_tree.c.depth + 1).label("depth"),
        )
        .join(activity_tree, Activity.parent_id == activity_tree.c.id)
        .where(activity_tree.c.depth < 3)
    )
    activity_tree = activity_tree.union_all(children)

    query = (
        select(Organization)
        .join(
            organization_activities,
            organization_activities.c.organization_id == Organization.id,
        )
        .where(
            organization_activities.c.activity_id.in_(
                select(activity_tree.c.id),
            )
        )
        .distinct()
        .order_by(Organization.id)
    )
    return list(db.scalars(query).all())
