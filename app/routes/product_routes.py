from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.models.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

service = ProductService()


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return service.create_product(db, payload)


@router.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return service.get_all_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, db: Session = Depends(get_db)):
    return service.get_product_by_id(db, product_id)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    payload: ProductUpdate,
    db: Session = Depends(get_db)
):
    return service.update_product(db, product_id, payload)


@router.delete("/{product_id}")
def delete_product(product_id: str, db: Session = Depends(get_db)):
    return service.delete_product(db, product_id)