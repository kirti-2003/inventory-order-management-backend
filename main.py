from fastapi import FastAPI
from app.config.settings import settings
from app.models.domain import *
from app.routes import(
    product_routes,
    customer_routes,
    order_routes

)


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Inventory Order Management API is running"
    }
app.include_router(product_routes.router)
app.include_router(customer_routes.router)
app.include_router(order_routes.router)