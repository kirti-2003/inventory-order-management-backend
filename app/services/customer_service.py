from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models.domain.customer import Customer
from app.models.schemas.customer_schema import CustomerCreate
from app.repositories.customer_repository import CustomerRepository
from app.utils.id_generator import generate_customer_id


class CustomerService:

    def __init__(self):
        self.repo = CustomerRepository()

    def create_customer(self, db: Session, customer_data: CustomerCreate):
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

        return self.repo.create_customer(db, customer)

    def get_all_customers(self, db: Session):
        return self.repo.get_all_customers(db)

    def get_customer_by_id(self, db: Session, customer_id: str):
        customer = self.repo.get_customer_by_id(db, customer_id)

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        return customer

    def delete_customer(self, db: Session, customer_id: str):
        customer = self.repo.delete_customer(db, customer_id)

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        return {
            "message": "Customer deleted successfully"
        }