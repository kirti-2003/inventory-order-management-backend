"""update order status values

Revision ID: de6c650e4343
Revises: b9132b5338c8
Create Date: 2026-06-22 01:06:11.957067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de6c650e4343'
down_revision: Union[str, Sequence[str], None] = 'b9132b5338c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_constraint(
        "valid_order_status",
        "orders",
        type_="check"
    )

    op.alter_column(
        "orders",
        "status",
        server_default=sa.text("'PENDING'")
    )

    op.create_check_constraint(
        "valid_order_status",
        "orders",
        "status IN ('PENDING', 'PLACED', 'COMPLETED', 'CANCELLED')"
    )


def downgrade():
    op.drop_constraint(
        "valid_order_status",
        "orders",
        type_="check"
    )

    op.alter_column(
        "orders",
        "status",
        server_default=sa.text("'PLACED'")
    )

    op.create_check_constraint(
        "valid_order_status",
        "orders",
        "status IN ('PLACED', 'CANCELLED')"
    )