from typing import List, Optional
from models.medicine import Medicine
from datetime import datetime, timedelta

def find_medicine_by_name(name: str, medicines: List[Medicine]) -> Optional[Medicine]:
    for med in medicines:
        if med.name.lower() == name.lower():
            return med
    return None

def is_expired(expiry_date: str) -> bool:
    today = datetime.today().date()
    expiry = datetime.strptime(expiry_date, "%Y-%m-%d").date()
    return expiry < today

def filter_expiring_medicines(medicines: List[Medicine], days: int = 30) -> List[Medicine]:
    today = datetime.today().date()
    limit_date = today + timedelta(days=days)
    result = []
    for med in medicines:
        expiry = datetime.strptime(med.expiry_date, "%Y-%m-%d").date()
        if today <= expiry <= limit_date:
            result.append(med)
    return result
