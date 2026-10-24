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


class RestaurantRevenue(BaseModel):
    restaurant: str
    total_revenue: float


class CancellationRate(BaseModel):
    total_orders: int
    cancelled_orders: int
    cancelled_rate: float


class BusinessWeekDays(BaseModel):
    total_orders: int
    day: str


class LogCreate(BaseModel):
    number_of_logs: int
    days: int
