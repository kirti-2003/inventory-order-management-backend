from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
    Text,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.config.database import Base


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    transaction_id = Column(String(80), primary_key=True)

    company_id = Column(
        String(80), 
        ForeignKey("companies.company_id"),
        nullable=False
    )

    product_id = Column(
        String(80), 
        ForeignKey("products.product_id"),
        nullable=False
    )

    transaction_type = Column(
        String(30),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)

    reference_type = Column(String(50))

    reference_id = Column(String(80))

    remarks = Column(Text)

    created_at = Column(DateTime)

    company = relationship(
        "Company",
        back_populates="inventory_transactions"
    )

    product = relationship(
        "Product",
        back_populates="inventory_transactions"
    )