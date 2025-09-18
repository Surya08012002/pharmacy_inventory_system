from fastapi import APIRouter, HTTPException, Query
from models.medicine import Medicine
from app.database import medicine_collection
from bson import ObjectId
from datetime import datetime, timedelta

router = APIRouter(prefix="/medicines", tags=["Medicines"])

# Helper to convert MongoDB document to dictionary
def medicine_helper(med):
    return {
        "id": str(med["_id"]),
        "name": med["name"],
        "brand": med["brand"],
        "quantity": med["quantity"],
        "price": med["price"],
        "expiry_date": med["expiry_date"],
        "description": med.get("description")
    }

# Create/Add medicine
@router.post("/")
def create_medicine(medicine: Medicine):
    med_dict = medicine.dict()
    result = medicine_collection.insert_one(med_dict)
    new_med = medicine_collection.find_one({"_id": result.inserted_id})
    return {"message": "Medicine added successfully", "data": medicine_helper(new_med)}

# Get all medicines
@router.get("/")
def get_medicines():
    medicines = []
    for med in medicine_collection.find():
        medicines.append(medicine_helper(med))
    return medicines

# Get medicine by name
@router.get("/{name}")
def get_medicine(name: str):
    med = medicine_collection.find_one({"name": name})
    if med:
        return medicine_helper(med)
    raise HTTPException(status_code=404, detail="Medicine not found")

# Update medicine by name
@router.put("/{name}")
def update_medicine(name: str, updated: Medicine):
    med = medicine_collection.find_one({"name": name})
    if med:
        medicine_collection.update_one({"name": name}, {"$set": updated.dict()})
        updated_med = medicine_collection.find_one({"name": name})
        return {"message": "Medicine updated successfully", "data": medicine_helper(updated_med)}
    raise HTTPException(status_code=404, detail="Medicine not found")

# Delete medicine by name
@router.delete("/{name}")
def delete_medicine(name: str):
    result = medicine_collection.delete_one({"name": name})
    if result.deleted_count:
        return {"message": f"Medicine '{name}' deleted successfully"}
    raise HTTPException(status_code=404, detail="Medicine not found")

# New Feature 1 – Get medicines expiring soon
@router.get("/expiry-soon/")
def get_expiring_medicines(days: int = Query(30, description="Number of days to check for expiry")):
    today = datetime.today().date()
    limit_date = today + timedelta(days=days)
    medicines = []
    for med in medicine_collection.find():
        expiry = datetime.strptime(med["expiry_date"], "%Y-%m-%d").date()
        if today <= expiry <= limit_date:
            medicines.append(medicine_helper(med))
    return {"message": f"Medicines expiring within {days} days", "data": medicines}

# New Feature 2 – Get medicines with low stock
@router.get("/low-stock/")
def get_low_stock_medicines(threshold: int = Query(10, description="Quantity threshold for low stock")):
    medicines = []
    for med in medicine_collection.find({"quantity": {"$lte": threshold}}):
        medicines.append(medicine_helper(med))
    return {"message": f"Medicines with quantity below or equal to {threshold}", "data": medicines}

# New Feature 3 – Get medicines by brand name
@router.get("/brand/{brand_name}")
def get_medicines_by_brand(brand_name: str):
    medicines = []
    for med in medicine_collection.find({"brand": brand_name}):
        medicines.append(medicine_helper(med))
    if medicines:
        return {"message": f"Medicines of brand '{brand_name}'", "data": medicines}
    raise HTTPException(status_code=404, detail=f"No medicines found for brand '{brand_name}'")
