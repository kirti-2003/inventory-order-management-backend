from sqlalchemy.orm import Session
from datetime import datetime

from app.models.domain.product import Product


class ProductRepository:

    def get_product_by_id(self, db: Session, product_id: str):
        return (
            db.query(Product)
            .filter(
                Product.product_id == product_id,
                Product.is_active == True
            )
            .first()
        )

    def get_product_by_sku(self, db: Session, company_id: str, sku: str):
        return (
            db.query(Product)
            .filter(
                Product.company_id == company_id,
                Product.sku == sku,
                Product.is_active == True
            )
            .first()
        )

    def get_all_products(self, db: Session):
        return (
            db.query(Product)
            .filter(Product.is_active == True)
            .all()
        )

    def create_product(self, db: Session, product_data: dict):
        product = Product(**product_data)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def update_product(self, db: Session, product: Product, update_data: dict):
        for key, value in update_data.items():
            setattr(product, key, value)

        product.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(product)
        return product

    def delete_product(self, db: Session, product: Product):
        product.is_active = False
        product.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(product)

        return product