from fastapi import FastAPI
from routes.medicine_routes import router as medicine_router
from routes.sale_routes import router as sale_router  # Import new sales routes

app = FastAPI(title="Pharmacy Inventory & Stock Management System")

app.include_router(medicine_router)
app.include_router(sale_router)  # Include sales routes

@app.get("/")
def home():
    return {"message": "Welcome to the Pharmacy Inventory System"}
