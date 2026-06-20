from fastapi import FastAPI
from app.config.settings import settings
from app.routes import product_routes



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