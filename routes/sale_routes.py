from fastapi import APIRouter, HTTPException
from models.sale import Sale
from app.database import medicine_collection, sales_collection
from datetime import date

router = APIRouter(prefix="/sales", tags=["Sales"])

# Record a new sale
@router.post("/")
def create_sale(sale: Sale):
    # Check if medicine exists
    medicine = medicine_collection.find_one({"name": sale.medicine_name})
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    # Check stock availability
    if medicine["quantity"] < sale.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Update stock quantity
    medicine_collection.update_one(
        {"name": sale.medicine_name},
        {"$inc": {"quantity": -sale.quantity}}
    )

    # Record the sale
    sale_data = sale.dict()
    if not sale_data.get("sale_date"):
        sale_data["sale_date"] = date.today().isoformat()
    sales_collection.insert_one(sale_data)

    return {"message": "Sale recorded successfully", "data": sale_data}

# Get all sales
@router.get("/")
def get_sales():
    sales = []
    for s in sales_collection.find():
        s["_id"] = str(s["_id"])
        sales.append(s)
    return sales

# Get sales by medicine name
@router.get("/{medicine_name}")
def get_sales_by_medicine(medicine_name: str):
    sales = []
    for s in sales_collection.find({"medicine_name": medicine_name}):
        s["_id"] = str(s["_id"])
        sales.append(s)
    if not sales:
        raise HTTPException(status_code=404, detail="No sales found for this medicine")
    return sales
