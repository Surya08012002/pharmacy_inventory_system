from fastapi import FastAPI
from routes.medicine_routes import router as medicine_router
from routes.sale_routes import router as sale_router

app = FastAPI(
    title="Pharmacy Inventory & Stock Management System",
    description="Manage medicines, sales, stock levels, and expiry tracking",
    version="2.0.0"
)

# Register routes
app.include_router(medicine_router)
app.include_router(sale_router)

@app.get("/")
def root():
    return {"message": "Pharmacy Inventory & Stock Management System is running"}
