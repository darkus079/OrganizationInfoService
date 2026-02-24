from sqlalchemy import Select, literal, select
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.organization import Organization
from app.models.organization_activity import organization_activities

MAX_ACTIVITY_DEPTH = 3


def get_activity_by_id(db: Session, activity_id: int) -> Activity | None:
    query = select(Activity).where(Activity.id == activity_id)
    return db.scalars(query).first()


def get_activity_level(db: Session, activity_id: int) -> int | None:
    # Walk up from node to root to get absolute level in tree.
    current_branch: Select[tuple[int, int | None, int]] = select(
        Activity.id.label("id"),
        Activity.parent_id.label("parent_id"),
        literal(1).label("level"),
    ).where(Activity.id == activity_id)

    branch = current_branch.cte(name="activity_branch", recursive=True)
    parents = (
        select(
            Activity.id.label("id"),
            Activity.parent_id.label("parent_id"),
            (branch.c.level + 1).label("level"),
        )
        .join(branch, branch.c.parent_id == Activity.id)
    )
    branch = branch.union_all(parents)

    query = select(branch.c.level).order_by(branch.c.level.desc()).limit(1)
    return db.scalar(query)


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
    activity_level = get_activity_level(db, activity_id)
    if activity_level is None:
        return []

    max_relative_depth = MAX_ACTIVITY_DEPTH - activity_level + 1
    if max_relative_depth <= 0:
        return []

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
        .where(activity_tree.c.depth < max_relative_depth)
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
