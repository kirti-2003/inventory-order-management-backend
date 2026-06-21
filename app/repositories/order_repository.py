from sqlalchemy.orm import Session

from app.models.domain.order import Order, OrderItem
from app.models.domain.customer import Customer
from app.models.domain.product import Product
from app.models.domain.company import Company


class OrderRepository:

    def get_company_by_id(self, db: Session, company_id: str):
        return db.query(Company).filter(
            Company.company_id == company_id
        ).first()

    def get_customer_by_id(self, db: Session, customer_id: str):
        return db.query(Customer).filter(
            Customer.customer_id == customer_id
        ).first()

    def get_product_by_id(self, db: Session, product_id: str):
        return db.query(Product).filter(
            Product.product_id == product_id
        ).first()

    def create_order(self, db: Session, order: Order):
        db.add(order)
        db.flush()
        return order

    def create_order_item(self, db: Session, order_item: OrderItem):
        db.add(order_item)
        db.flush()
        return order_item

    def get_all_orders(self, db: Session):
        return db.query(Order).all()

    def get_order_by_id(self, db: Session, order_id: str):
        return db.query(Order).filter(
            Order.order_id == order_id
        ).first()

    def cancel_order(self, db: Session, order: Order):
        order.status = "CANCELLED"
        db.flush()
        return order

    def update_product_stock(self, db: Session, product: Product, quantity: int):
        product.quantity_in_stock = quantity
        db.flush()
        return product