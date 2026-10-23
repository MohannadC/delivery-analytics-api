from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Item(BaseModel):
    dish: str
    quantity: int
    price: float


class OrderCreate(BaseModel):
    user: str
    restaurant: str
    total_price: float
    status: str = "CREATED"
    items: list[Item]
    created_at: datetime = Field(default_factory=datetime.now)


class OrderResponse(BaseModel):
    id: str
    user: str
    restaurant: str
    total_price: float
    status: str
    items: list[Item]
    created_at: datetime


class OrderUpdate(BaseModel):
    total_price: Optional[float] = None
    status: Optional[str] = None
