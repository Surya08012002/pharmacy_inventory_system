from pydantic import BaseModel
from typing import Optional

class Medicine(BaseModel):
    name: str
    brand: str
    quantity: int
    price: float
    expiry_date: str  # Format: YYYY-MM-DD
    description: Optional[str] = None
