from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int


class OrderCreate(BaseModel):
    company_id: str
    customer_id: str
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    order_item_id: str
    product_id: str
    quantity: int
    unit_price: Decimal
    line_total: Decimal
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    order_id: str
    company_id: str
    customer_id: str
    order_number: str
    total_amount: Decimal
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    order_items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True