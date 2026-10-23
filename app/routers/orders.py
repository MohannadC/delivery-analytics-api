from fastapi import APIRouter, HTTPException
from database import db_connect
from models import OrderResponse, OrderCreate
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter()


@router.get("/orders", response_model=list[OrderResponse])
def get_orders(
    status: str | None = None,
    restaurant: str | None = None,
    user: str | None = None,
    skip: int = 0,
    limit: int = 50,
):
    query_filter = {}
    if status:
        query_filter["status"] = status
    if restaurant:
        query_filter["restaurant"] = restaurant
    if user:
        query_filter["user"] = user

    collection = db_connect()
    results = collection.find(query_filter).skip(skip).limit(limit)

    orders = []
    for doc in results:
        doc["id"] = str(doc.pop("_id"))
        orders.append(OrderResponse(**doc))
    return orders


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_by_id(order_id: str):
    collection = db_connect()
    try:
        result = collection.find_one({"_id": ObjectId(order_id)})
    except InvalidId:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    result["id"] = str(result.pop("_id"))
    return OrderResponse(**result)
