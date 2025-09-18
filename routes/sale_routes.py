from fastapi import APIRouter, HTTPException
from models.sale import Sale
from app.database import sales_collection, medicine_collection
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/sales", tags=["Sales"])

# Helper to convert MongoDB documents to dict
def sale_helper(sale) -> dict:
    return {
        "id": str(sale["_id"]),
        "medicine_name": sale["medicine_name"],
        "quantity_sold": sale["quantity_sold"],
        "sale_date": sale["sale_date"],
        "total_price": sale["total_price"],
    }

# Create/Add a new sale
@router.post("/")
def create_sale(sale: Sale):
    medicine = medicine_collection.find_one({"name": sale.medicine_name})
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    if medicine["quantity"] < sale.quantity_sold:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    # Reduce stock
    medicine_collection.update_one(
        {"name": sale.medicine_name},
        {"$inc": {"quantity": -sale.quantity_sold}}
    )

    # Create sale record
    sale_dict = sale.dict()
    sale_dict["sale_date"] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    sale_dict["total_price"] = medicine["price"] * sale.quantity_sold

    result = sales_collection.insert_one(sale_dict)
    new_sale = sales_collection.find_one({"_id": result.inserted_id})
    return {"message": "Sale recorded successfully", "data": sale_helper(new_sale)}

# Get all sales
@router.get("/")
def get_all_sales():
    sales = []
    for sale in sales_collection.find():
        sales.append(sale_helper(sale))
    return {"message": "All sales records", "data": sales}

# Get sales by medicine name
@router.get("/{medicine_name}")
def get_sales_by_medicine(medicine_name: str):
    sales = []
    for sale in sales_collection.find({"medicine_name": medicine_name}):
        sales.append(sale_helper(sale))
    if not sales:
        raise HTTPException(status_code=404, detail=f"No sales found for {medicine_name}")
    return {"message": f"Sales records for {medicine_name}", "data": sales}

# Delete all sales
@router.delete("/delete-all/")
def delete_all_sales():
    result = sales_collection.delete_many({})
    return {"message": f"All sales deleted successfully. Count: {result.deleted_count}"}

# Delete sales by medicine name
@router.delete("/delete/{medicine_name}")
def delete_sales_by_medicine(medicine_name: str):
    result = sales_collection.delete_many({"medicine_name": medicine_name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"No sales found for {medicine_name}")
    return {"message": f"All sales for {medicine_name} deleted successfully. Count: {result.deleted_count}"}

# ✅ New Feature: Delete sale by ID
@router.delete("/delete-by-id/{sale_id}")
def delete_sale_by_id(sale_id: str):
    if not ObjectId.is_valid(sale_id):
        raise HTTPException(status_code=400, detail="Invalid sale ID format")
    
    result = sales_collection.delete_one({"_id": ObjectId(sale_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    return {"message": f"Sale with ID {sale_id} deleted successfully"}
