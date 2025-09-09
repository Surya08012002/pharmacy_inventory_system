from fastapi import FastAPI
from routes.medicine_routes import router as medicine_router

app = FastAPI(title="Pharmacy Inventory & Stock Management System")

app.include_router(medicine_router)

@app.get("/")
def home():
    return {"message": "Welcome to the Pharmacy Inventory System"}
