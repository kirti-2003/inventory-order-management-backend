from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.models.schemas.order_schema import OrderCreate, OrderResponse
from app.services.order_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

service = OrderService()


@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    return service.create_order(db, order_data)


@router.get("/", response_model=List[OrderResponse])
def get_all_orders(db: Session = Depends(get_db)):
    return service.get_all_orders(db)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(
    order_id: str,
    db: Session = Depends(get_db)
):
    return service.get_order_by_id(db, order_id)


@router.delete("/{order_id}")
def delete_order(
    order_id: str,
    db: Session = Depends(get_db)
):
    return service.delete_order(db, order_id)