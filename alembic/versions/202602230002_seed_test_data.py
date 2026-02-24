"""Seed test data.

Revision ID: 202602230002
Revises: 202602230001
Create Date: 2026-02-23 00:00:02
"""

from typing import Sequence

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "202602230002"
down_revision: str | None = "202602230001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


buildings_table = sa.table(
    "buildings",
    sa.column("id", sa.Integer()),
    sa.column("address", sa.String(length=255)),
    sa.column("latitude", sa.Numeric(9, 6)),
    sa.column("longitude", sa.Numeric(9, 6)),
)

activities_table = sa.table(
    "activities",
    sa.column("id", sa.Integer()),
    sa.column("name", sa.String(length=255)),
    sa.column("parent_id", sa.Integer()),
)

organizations_table = sa.table(
    "organizations",
    sa.column("id", sa.Integer()),
    sa.column("name", sa.String(length=255)),
    sa.column("building_id", sa.Integer()),
)

phones_table = sa.table(
    "organization_phones",
    sa.column("organization_id", sa.Integer()),
    sa.column("phone_number", sa.String(length=32)),
)

organization_activities_table = sa.table(
    "organization_activities",
    sa.column("organization_id", sa.Integer()),
    sa.column("activity_id", sa.Integer()),
)


def upgrade() -> None:
    op.bulk_insert(
        buildings_table,
        [
            {
                "id": 1,
                "address": "г. Москва, ул. Ленина 1, офис 3",
                "latitude": 55.755826,
                "longitude": 37.6173,
            },
            {
                "id": 2,
                "address": "г. Москва, ул. Блюхера 32/1",
                "latitude": 55.763338,
                "longitude": 37.565466,
            },
            {
                "id": 3,
                "address": "г. Москва, ул. Тверская 10",
                "latitude": 55.764978,
                "longitude": 37.605042,
            },
        ],
    )

    op.bulk_insert(
        activities_table,
        [
            {"id": 1, "name": "Еда", "parent_id": None},
            {"id": 2, "name": "Мясная продукция", "parent_id": 1},
            {"id": 3, "name": "Молочная продукция", "parent_id": 1},
            {"id": 4, "name": "Автомобили", "parent_id": None},
            {"id": 5, "name": "Грузовые", "parent_id": 4},
            {"id": 6, "name": "Легковые", "parent_id": 4},
            {"id": 7, "name": "Запчасти", "parent_id": 4},
            {"id": 8, "name": "Аксессуары", "parent_id": 4},
            {"id": 9, "name": "Кузовные запчасти", "parent_id": 7},
        ],
    )

    op.bulk_insert(
        organizations_table,
        [
            {"id": 1, "name": "ООО Рога и Копыта", "building_id": 2},
            {"id": 2, "name": "ООО Молочный Мир", "building_id": 1},
            {"id": 3, "name": "АО АвтоТорг", "building_id": 3},
            {"id": 4, "name": "ООО ГрузАвто", "building_id": 3},
        ],
    )

    op.bulk_insert(
        phones_table,
        [
            {"organization_id": 1, "phone_number": "2-222-222"},
            {"organization_id": 1, "phone_number": "8-923-666-13-13"},
            {"organization_id": 2, "phone_number": "3-333-333"},
            {"organization_id": 3, "phone_number": "7-495-100-10-10"},
            {"organization_id": 4, "phone_number": "7-495-100-20-20"},
        ],
    )

    op.bulk_insert(
        organization_activities_table,
        [
            {"organization_id": 1, "activity_id": 2},
            {"organization_id": 1, "activity_id": 3},
            {"organization_id": 2, "activity_id": 3},
            {"organization_id": 3, "activity_id": 7},
            {"organization_id": 3, "activity_id": 8},
            {"organization_id": 4, "activity_id": 5},
            {"organization_id": 4, "activity_id": 9},
        ],
    )


def downgrade() -> None:
    op.execute(sa.text("DELETE FROM organization_activities WHERE organization_id IN (1,2,3,4)"))
    op.execute(sa.text("DELETE FROM organization_phones WHERE organization_id IN (1,2,3,4)"))
    op.execute(sa.text("DELETE FROM organizations WHERE id IN (1,2,3,4)"))
    op.execute(sa.text("DELETE FROM activities WHERE id IN (1,2,3,4,5,6,7,8,9)"))
    op.execute(sa.text("DELETE FROM buildings WHERE id IN (1,2,3)"))
