from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.organization import Organization


class OrganizationPhone(Base):
    __tablename__ = "organization_phones"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "phone_number",
            name="uq_organization_phones_org_id_phone_number",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    phone_number: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

    organization: Mapped["Organization"] = relationship(back_populates="phones")
