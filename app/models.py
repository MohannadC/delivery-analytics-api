from pydantic import BaseModel
from datetime import datetime


class Item(BaseModel):
    dish: str
    quantity: int
    price: float


class OrderCreate(BaseModel):
    user: str
    restaurant: str
    total_price: float
    status: str
    items: list[Item]
    created_at: datetime


class OrderResponse(BaseModel):
    id: str
    user: str
    restaraunt: str
    total_price: float
    status: str
    items: list[Item]
    created_at: datetime
