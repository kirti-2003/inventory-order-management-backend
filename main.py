from fastapi import FastAPI
from app.config.settings import settings
from fastapi.middleware.cors import CORSMiddleware
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


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "https://inventory-order-management-frontend-liard.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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