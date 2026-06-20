from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Text,
    Numeric,
    Integer,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.config.database import Base


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        UniqueConstraint("company_id", "sku", name="unique_company_sku"),
    )

    product_id = Column(String(80), primary_key=True)

    company_id = Column(
        String(80),
        ForeignKey("companies.company_id"),
        nullable=False
    )

    product_name = Column(String(150), nullable=False)
    sku = Column(String(100), nullable=False)

    description = Column(Text)

    price = Column(Numeric(12, 2), nullable=False)

    quantity_in_stock = Column(Integer, nullable=False)

    low_stock_threshold = Column(Integer)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    company = relationship("Company", back_populates="products")

    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )

    inventory_transactions = relationship(
        "InventoryTransaction",
        back_populates="product"
    )