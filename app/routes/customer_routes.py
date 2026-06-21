from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.models.schemas.customer_schema import CustomerCreate, CustomerResponse
from app.services.customer_service import CustomerService

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

service = CustomerService()


@router.post("/", response_model=CustomerResponse)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    return service.create_customer(db, customer_data)


@router.get("/", response_model=List[CustomerResponse])
def get_all_customers(db: Session = Depends(get_db)):
    return service.get_all_customers(db)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer_by_id(
    customer_id: str,
    db: Session = Depends(get_db)
):
    return service.get_customer_by_id(db, customer_id)


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):
    return service.delete_customer(db, customer_id)