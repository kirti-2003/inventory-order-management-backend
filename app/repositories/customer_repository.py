from sqlalchemy.orm import Session
from datetime import datetime

from app.models.domain.customer import Customer
from app.models.schemas.customer_schema import CustomerCreate
from app.utils.id_generator import generate_customer_id




def create_customer(db: Session, customer_data: CustomerCreate):
    customer = Customer(
        customer_id=generate_customer_id(),
        company_id=customer_data.company_id,
        full_name=customer_data.full_name,
        email=customer_data.email,
        phone=customer_data.phone,
        address=customer_data.address,
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


def get_all_customers(db: Session):
    return db.query(Customer).filter(Customer.is_active == True).all()


def get_customer_by_id(db: Session, customer_id: str):
    return (
        db.query(Customer)
        .filter(
            Customer.customer_id == customer_id,
            Customer.is_active == True
        )
        .first()
    )


def delete_customer(db: Session, customer_id: str):
    customer = get_customer_by_id(db, customer_id)

    if not customer:
        return None

    customer.is_active = False
    customer.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(customer)

    return customer