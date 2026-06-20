from sqlalchemy.orm import Session
from app.models.domain.company import Company
from app.models.domain.product import Product
from app.models.domain.order import OrderItem
from app.models.domain.inventory_transaction import InventoryTransaction
from app.models.domain.customer import Customer


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.product_id == product_id).first()


def get_product_by_sku(db: Session, company_id, sku: str):
    return (
        db.query(Product)
        .filter(
            Product.company_id == company_id,
            Product.sku == sku
        )
        .first()
    )


def get_all_products(db: Session):
    return db.query(Product).all()


def create_product(db: Session, product_data: dict):
    product = Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, update_data: dict):
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product):
    db.delete(product)
    db.commit()