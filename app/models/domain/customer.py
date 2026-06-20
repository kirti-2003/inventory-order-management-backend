from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.config.database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String(80), primary_key=True)

    company_id = Column(
        String(80),
        ForeignKey("companies.company_id"),
        nullable=False
    )

    full_name = Column(String(150), nullable=False)

    email = Column(String(150), nullable=False)

    phone = Column(String(20))

    address = Column(Text)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime)

    updated_at = Column(DateTime)

    company = relationship(
        "Company",
        back_populates="customers"
    )

    orders = relationship(
        "Order",
        back_populates="customer"
    )