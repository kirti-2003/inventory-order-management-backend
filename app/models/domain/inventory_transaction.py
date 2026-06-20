from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
    Text,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.config.database import Base


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    transaction_id = Column(UUID(as_uuid=True), primary_key=True)

    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey("companies.company_id"),
        nullable=False
    )

    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.product_id"),
        nullable=False
    )

    transaction_type = Column(
        String(30),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)

    reference_type = Column(String(50))

    reference_id = Column(UUID(as_uuid=True))

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