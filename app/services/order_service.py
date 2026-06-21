from sqlalchemy.orm import Session
from fastapi import HTTPException
from decimal import Decimal
from datetime import datetime

from app.models.schemas.order_schema import OrderCreate
from app.models.domain.order import Order, OrderItem
from app.repositories.order_repository import OrderRepository
from app.utils.id_generator import (
    generate_order_id,
    generate_order_item_id
)


class OrderService:

    def __init__(self):
        self.repo = OrderRepository()

    def generate_order_number(self):
        return f"ORDER-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    def create_order(self, db: Session, order_data: OrderCreate):
        company = self.repo.get_company_by_id(db, order_data.company_id)

        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        customer = self.repo.get_customer_by_id(db, order_data.customer_id)

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        if not order_data.items:
            raise HTTPException(
                status_code=400,
                detail="Order must contain at least one product"
            )

        total_amount = Decimal("0.00")
        prepared_items = []

        for item in order_data.items:
            if item.quantity <= 0:
                raise HTTPException(
                    status_code=400,
                    detail="Quantity must be greater than 0"
                )

            product = self.repo.get_product_by_id(db, item.product_id)

            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product not found: {item.product_id}"
                )

            if product.company_id != order_data.company_id:
                raise HTTPException(
                    status_code=400,
                    detail=f"Product {product.product_name} does not belong to this company"
                )

            if product.quantity_in_stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for product: {product.product_name}"
                )

            unit_price = Decimal(str(product.price))
            line_total = unit_price * Decimal(item.quantity)
            total_amount += line_total

            prepared_items.append({
                "product": product,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": unit_price,
                "line_total": line_total
            })

        try:
            order = Order(
                order_id=generate_order_id(),
                company_id=order_data.company_id,
                customer_id=order_data.customer_id,
                order_number=self.generate_order_number(),
                total_amount=total_amount,
                status="PENDING",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            self.repo.create_order(db, order)

            for item in prepared_items:
                order_item = OrderItem(
                    order_item_id=generate_order_item_id(),
                    order_id=order.order_id,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    unit_price=item["unit_price"],
                    line_total=item["line_total"],
                    created_at=datetime.utcnow()
                )

                self.repo.create_order_item(db, order_item)

                new_stock = item["product"].quantity_in_stock - item["quantity"]

                self.repo.update_product_stock(
                    db,
                    item["product"],
                    new_stock
                )

            db.commit()
            db.refresh(order)

            return order

        except HTTPException:
            db.rollback()
            raise

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error creating order: {str(e)}"
            )

    def get_all_orders(self, db: Session):
        return self.repo.get_all_orders(db)

    def get_order_by_id(self, db: Session, order_id: str):
        order = self.repo.get_order_by_id(db, order_id)

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        return order

    def delete_order(self, db: Session, order_id: str):
        order = self.repo.get_order_by_id(db, order_id)

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.status == "CANCELLED":
            raise HTTPException(
                status_code=400,
                detail="Order is already cancelled"
            )

        try:
            for item in order.order_items:
                product = self.repo.get_product_by_id(db, item.product_id)

                if product:
                    restored_stock = product.quantity_in_stock + item.quantity

                    self.repo.update_product_stock(
                        db,
                        product,
                        restored_stock
                    )

            order.updated_at = datetime.utcnow()

            self.repo.cancel_order(db, order)

            db.commit()
            db.refresh(order)

            return {
                "message": "Order cancelled successfully"
            }

        except HTTPException:
            db.rollback()
            raise

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error cancelling order: {str(e)}"
            )