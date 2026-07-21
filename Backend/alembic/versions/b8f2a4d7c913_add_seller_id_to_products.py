"""add seller id to products

Revision ID: b8f2a4d7c913
Revises: a36ca6cb0810
Create Date: 2026-07-21 17:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b8f2a4d7c913"
down_revision: Union[str, Sequence[str], None] = "a36ca6cb0810"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("products", sa.Column("seller_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_products_seller_id_users",
        "products",
        "users",
        ["seller_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_products_seller_id_users", "products", type_="foreignkey")
    op.drop_column("products", "seller_id")
