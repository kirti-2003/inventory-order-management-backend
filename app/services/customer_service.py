from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.schemas.customer_schema import CustomerCreate
from app.repositories import customer_repository


def create_customer_service(db: Session, customer_data: CustomerCreate):
    return customer_repository.create_customer(db, customer_data)


def get_all_customers_service(db: Session):
    return customer_repository.get_all_customers(db)


def get_customer_by_id_service(db: Session, customer_id: str):
    customer = customer_repository.get_customer_by_id(db, customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


def delete_customer_service(db: Session, customer_id: str):
    customer = customer_repository.delete_customer(db, customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        "message": "Customer deleted successfully"
    }