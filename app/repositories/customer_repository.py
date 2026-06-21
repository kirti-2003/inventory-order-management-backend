from sqlalchemy.orm import Session
from datetime import datetime

from app.models.domain.customer import Customer


class CustomerRepository:

    def create_customer(self, db: Session, customer: Customer):
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

    def get_all_customers(self, db: Session):
        return db.query(Customer).filter(Customer.is_active == True).all()

    def get_customer_by_id(self, db: Session, customer_id: str):
        return (
            db.query(Customer)
            .filter(
                Customer.customer_id == customer_id,
                Customer.is_active == True
            )
            .first()
        )

    def delete_customer(self, db: Session, customer_id: str):
        customer = self.get_customer_by_id(db, customer_id)

        if not customer:
            return None

        customer.is_active = False
        customer.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(customer)

        return customer