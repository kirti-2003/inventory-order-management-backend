"""create initial inventory tables

Revision ID: b9132b5338c8
Revises: 
Create Date: 2026-06-20 18:53:27.390897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9132b5338c8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    """Upgrade schema."""

    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')

    op.create_table(
        "companies",
        sa.Column("company_id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("company_name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=True, unique=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "products",
        sa.Column("product_id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("company_id", sa.UUID(), sa.ForeignKey("companies.company_id", ondelete="CASCADE"), nullable=False),
        sa.Column("product_name", sa.String(length=150), nullable=False),
        sa.Column("sku", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Numeric(12, 2), nullable=False),
        sa.Column("quantity_in_stock", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("low_stock_threshold", sa.Integer(), server_default=sa.text("5")),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.CheckConstraint("price >= 0", name="check_product_price_non_negative"),
        sa.CheckConstraint("quantity_in_stock >= 0", name="check_product_stock_non_negative"),
        sa.UniqueConstraint("company_id", "sku", name="unique_company_sku"),
    )

    op.create_table(
        "customers",
        sa.Column("customer_id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("company_id", sa.UUID(), sa.ForeignKey("companies.company_id", ondelete="CASCADE"), nullable=False),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("company_id", "email", name="unique_company_customer_email"),
    )

    op.create_table(
        "orders",
        sa.Column("order_id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("company_id", sa.UUID(), sa.ForeignKey("companies.company_id", ondelete="CASCADE"), nullable=False),
        sa.Column("customer_id", sa.UUID(), sa.ForeignKey("customers.customer_id"), nullable=False),
        sa.Column("order_number", sa.String(length=50), nullable=False),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("status", sa.String(length=30), nullable=False, server_default=sa.text("'PLACED'")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("company_id", "order_number", name="unique_company_order_number"),
        sa.CheckConstraint("status IN ('PLACED', 'CANCELLED')", name="valid_order_status"),
    )

    op.create_table(
        "order_items",
        sa.Column("order_item_id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("order_id", sa.UUID(), sa.ForeignKey("orders.order_id", ondelete="CASCADE"), nullable=False),
        sa.Column("product_id", sa.UUID(), sa.ForeignKey("products.product_id"), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("line_total", sa.Numeric(12, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.CheckConstraint("quantity > 0", name="check_order_item_quantity_positive"),
        sa.CheckConstraint("unit_price >= 0", name="check_order_item_unit_price_non_negative"),
        sa.CheckConstraint("line_total >= 0", name="check_order_item_line_total_non_negative"),
    )

    op.create_table(
        "inventory_transactions",
        sa.Column("transaction_id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("company_id", sa.UUID(), sa.ForeignKey("companies.company_id", ondelete="CASCADE"), nullable=False),
        sa.Column("product_id", sa.UUID(), sa.ForeignKey("products.product_id"), nullable=False),
        sa.Column("transaction_type", sa.String(length=30), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("reference_type", sa.String(length=50), nullable=True),
        sa.Column("reference_id", sa.UUID(), nullable=True),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.CheckConstraint(
            "transaction_type IN ('STOCK_IN', 'STOCK_OUT', 'ORDER_PLACED', 'ORDER_CANCELLED')",
            name="valid_transaction_type",
        ),
    )


def downgrade() :
    """Downgrade schema."""

    op.drop_table("inventory_transactions")
    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("customers")
    op.drop_table("products")
    op.drop_table("companies")
