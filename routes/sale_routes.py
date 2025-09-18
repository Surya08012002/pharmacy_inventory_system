from fastapi import APIRouter, HTTPException
from models.sale import Sale
from app.database import sales_collection, medicine_collection
from datetime import datetime

router = APIRouter(prefix="/sales", tags=["Sales"])

# Helper to safely convert MongoDB documents into JSON serializable dicts
def sale_helper(sale) -> dict:
    return {
        "id": str(sale.get("_id")),
        "medicine_name": sale.get("medicine_name"),
        "quantity_sold": sale.get("quantity_sold"),
        "sale_date": sale.get("sale_date"),
        "total_price": sale.get("total_price")
    }

# Create a sale
@router.post("/")
def create_sale(sale: Sale):
    medicine = medicine_collection.find_one({"name": sale.medicine_name})
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    if medicine["quantity"] < sale.quantity_sold:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    # Deduct sold quantity
    medicine_collection.update_one(
        {"_id": medicine["_id"]},
        {"$inc": {"quantity": -sale.quantity_sold}}
    )

    total_price = sale.quantity_sold * medicine["price"]

    sale_doc = {
        "medicine_name": sale.medicine_name,
        "quantity_sold": sale.quantity_sold,
        "sale_date": datetime.today().strftime("%Y-%m-%d"),
        "total_price": total_price
    }

    result = sales_collection.insert_one(sale_doc)
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

    return {"message": f"Sales for {medicine_name}", "data": sales}

# Delete all sales
@router.delete("/")
def delete_all_sales():
    result = sales_collection.delete_many({})  # deletes all documents in sales collection
    # result.deleted_count is the number of documents removed
    return {"message": "All sales deleted", "deleted_count": result.deleted_count}

# Delete sales by medicine name
@router.delete("/{medicine_name}")
def delete_sales_by_medicine(medicine_name: str):
    # Remove all sales documents where medicine_name matches
    result = sales_collection.delete_many({"medicine_name": medicine_name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"No sales found for {medicine_name}")
    return {"message": f"Sales for '{medicine_name}' deleted", "deleted_count": result.deleted_count}
