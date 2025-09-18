from pydantic import BaseModel

class Medicine(BaseModel):
    name: str
    manufacturer: str
    batch_number: str
    quantity: int
    price: float
    expiry_date: str   # format: YYYY-MM-DD
