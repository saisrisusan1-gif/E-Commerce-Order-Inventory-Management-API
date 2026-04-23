from pydantic import BaseModel,Field
from decimal import Decimal

    
class ProductRequest(BaseModel):
    name: str = Field(min_length=3)
    description: str = Field(min_length=3)
    price: Decimal = Field(gt=0)  # ✅ better for money
    stock: int
    category: str
    
class ProductUpdate(BaseModel):
    name: str = Field(min_length=3)
    description: str = Field(min_length=3)
    price: Decimal = Field(gt=0)  # ✅ better for money
    stock: int
    category: str

class ProductResponse(BaseModel):
    name: str
    description: str
    price: Decimal
    stock: int
    category: str

    class Config:
        from_attributes = True  # ✅ important for ORM