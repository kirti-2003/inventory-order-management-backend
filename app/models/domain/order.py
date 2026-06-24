from sqlalchemy import (
    Column,
    String,
    DateTime,
    Numeric,
    Integer,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.config.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String(80), primary_key=True)

    company_id = Column(
        String(80),
        ForeignKey("companies.company_id"),
        nullable=False
    )

    customer_id = Column(
        String(80),
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    order_number = Column(String(50), nullable=False)

    total_amount = Column(Numeric(12, 2), nullable=False)

    status = Column(String(30), nullable=False)

    created_at = Column(DateTime)

    updated_at = Column(DateTime)

    company = relationship(
        "Company",
        back_populates="orders"
    )

    customer = relationship(
        "Customer",
        back_populates="orders"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    @property
    def customer_name(self):
        return self.customer.full_name if self.customer else None


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(String(80), primary_key=True)

    order_id = Column(
        String(80),
        ForeignKey("orders.order_id"),
        nullable=False
    )

    product_id = Column(
        String(80),
        ForeignKey("products.product_id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)

    unit_price = Column(Numeric(12, 2), nullable=False)

    line_total = Column(Numeric(12, 2), nullable=False)

    created_at = Column(DateTime)

    order = relationship(
        "Order",
        back_populates="order_items"
    )

    product = relationship(
        "Product",
        back_populates="order_items"
    )

    @property
    def product_name(self):
        return self.product.product_name if self.product else None