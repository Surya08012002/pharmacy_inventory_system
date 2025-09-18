from pydantic import BaseModel
from typing import Optional
from datetime import date

class Sale(BaseModel):
    medicine_name: str
    quantity_sold: int

