from pydantic import BaseModel
from typing import Optional
from datetime import date

class Sale(BaseModel):
    medicine_name: str
    quantity: int
    sale_date: Optional[date] = None  # Defaults to today if not provided
