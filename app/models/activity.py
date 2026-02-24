from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.organization_activity import organization_activities

if TYPE_CHECKING:
    from app.models.organization import Organization


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        CheckConstraint("parent_id IS NULL OR parent_id <> id", name="ck_activity_parent_not_self"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    parent: Mapped["Activity | None"] = relationship(
        remote_side=[id],
        back_populates="children",
    )
    children: Mapped[list["Activity"]] = relationship(back_populates="parent")
    organizations: Mapped[list["Organization"]] = relationship(
        secondary=organization_activities,
        back_populates="activities",
    )
