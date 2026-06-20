from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.models.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product_service(db, payload)


@router.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return product_service.get_all_products_service(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product_by_id_service(db, product_id)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db)
):
    return product_service.update_product_service(db, product_id, payload)


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.delete_product_service(db, product_id)