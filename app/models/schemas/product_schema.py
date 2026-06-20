from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class ProductCreate(BaseModel):
    company_id: str
    product_name: str = Field(..., min_length=2)
    sku: str = Field(..., min_length=2)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    quantity_in_stock: int = Field(..., ge=0)
    low_stock_threshold: Optional[int] = None


class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    quantity_in_stock: Optional[int] = Field(None, ge=0)
    low_stock_threshold: Optional[int] = None
    is_active: Optional[bool] = None


class ProductResponse(BaseModel):
    product_id: str
    company_id: str
    product_name: str
    sku: str
    description: Optional[str] = None
    price: Decimal
    quantity_in_stock: int
    low_stock_threshold: Optional[int] = None
    is_active: bool

    class Config:
        from_attributes = True