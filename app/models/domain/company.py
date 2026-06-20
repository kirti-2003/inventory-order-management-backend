from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.config.database import Base


class Company(Base):
    __tablename__ = "companies"

    company_id = Column(UUID(as_uuid=True), primary_key=True)

    company_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True)
    phone = Column(String(20))
    address = Column(Text)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    products = relationship("Product", back_populates="company")
    customers = relationship("Customer", back_populates="company")
    orders = relationship("Order", back_populates="company")
    inventory_transactions = relationship(
        "InventoryTransaction",
        back_populates="company"
    )