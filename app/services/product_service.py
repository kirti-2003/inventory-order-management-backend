from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.schemas.product_schema import ProductCreate, ProductUpdate
from app.repositories.product_repository import ProductRepository
from app.utils.id_generator import generate_product_id


class ProductService:

    def __init__(self):
        self.repo = ProductRepository()

    def create_product(self, db: Session, payload: ProductCreate):
        existing_product = self.repo.get_product_by_sku(
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

        return self.repo.create_product(db, product_data)

    def get_all_products(self, db: Session):
        return self.repo.get_all_products(db)

    def get_product_by_id(self, db: Session, product_id: str):
        product = self.repo.get_product_by_id(db, product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        return product

    def update_product(self, db: Session, product_id: str, payload: ProductUpdate):
        product = self.get_product_by_id(db, product_id)

        update_data = payload.model_dump(exclude_unset=True)

        return self.repo.update_product(db, product, update_data)

    def delete_product(self, db: Session, product_id: str):
        product = self.get_product_by_id(db, product_id)

        self.repo.delete_product(db, product)

        return {"message": "Product deleted successfully"}