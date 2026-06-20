from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.schemas.product_schema import ProductCreate, ProductUpdate
from app.repositories import product_repository
from app.utils.id_generator import generate_product_id


def create_product_service(db: Session, payload: ProductCreate):
    existing_product = product_repository.get_product_by_sku(  
    db,
    payload.company_id,
    payload.sku
   )

    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product SKU already exists"
        )

    product_data = payload.model_dump()
    product_data["product_id"] = generate_product_id()

    return product_repository.create_product(db, product_data)


def get_all_products_service(db: Session):
    return product_repository.get_all_products(db)


def get_product_by_id_service(db: Session, product_id: str):
    product = product_repository.get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


def update_product_service(db: Session, product_id: str, payload: ProductUpdate):
    product = get_product_by_id_service(db, product_id)

    update_data = payload.model_dump(exclude_unset=True)

    return product_repository.update_product(db, product, update_data)


def delete_product_service(db: Session, product_id: str):
    product = get_product_by_id_service(db, product_id)

    product_repository.delete_product(db, product)

    return {"message": "Product deleted successfully"}