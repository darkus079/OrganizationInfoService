"""Create initial schema.

Revision ID: 202602230001
Revises:
Create Date: 2026-02-23 00:00:01
"""

from typing import Sequence

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "202602230001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.CheckConstraint("parent_id IS NULL OR parent_id <> id", name="ck_activity_parent_not_self"),
        sa.ForeignKeyConstraint(["parent_id"], ["activities.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_activities_name", "activities", ["name"], unique=False)
    op.create_index("ix_activities_parent_id", "activities", ["parent_id"], unique=False)

    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("latitude", sa.Numeric(precision=9, scale=6), nullable=False),
        sa.Column("longitude", sa.Numeric(precision=9, scale=6), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_buildings_address", "buildings", ["address"], unique=False)

    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["building_id"], ["buildings.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_organizations_name", "organizations", ["name"], unique=False)
    op.create_index("ix_organizations_building_id", "organizations", ["building_id"], unique=False)

    op.create_table(
        "organization_activities",
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("activity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["activity_id"], ["activities.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("organization_id", "activity_id"),
    )

    op.create_table(
        "organization_phones",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("phone_number", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "phone_number",
            name="uq_organization_phones_org_id_phone_number",
        ),
    )
    op.create_index("ix_organization_phones_organization_id", "organization_phones", ["organization_id"], unique=False)
    op.create_index("ix_organization_phones_phone_number", "organization_phones", ["phone_number"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_organization_phones_phone_number", table_name="organization_phones")
    op.drop_index("ix_organization_phones_organization_id", table_name="organization_phones")
    op.drop_table("organization_phones")
    op.drop_table("organization_activities")
    op.drop_index("ix_organizations_building_id", table_name="organizations")
    op.drop_index("ix_organizations_name", table_name="organizations")
    op.drop_table("organizations")
    op.drop_index("ix_buildings_address", table_name="buildings")
    op.drop_table("buildings")
    op.drop_index("ix_activities_parent_id", table_name="activities")
    op.drop_index("ix_activities_name", table_name="activities")
    op.drop_table("activities")
