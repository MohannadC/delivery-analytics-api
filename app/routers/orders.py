from fastapi import APIRouter, HTTPException
from database import db_connect
from models import OrderResponse, OrderCreate, OrderUpdate
from bson import ObjectId
from bson.errors import InvalidId
from loguru import logger

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


@router.post("/orders", status_code=201)
def post_order(new_order: OrderCreate):
    collection = db_connect()
    order_dict = new_order.model_dump()
    result = collection.insert_one(order_dict)
    order_dict["id"] = str(result.inserted_id)

    return OrderResponse(**order_dict)


@router.post("/orders/bulk", status_code=201)
def post_orders_bulk(new_orders: list[OrderCreate]):
    collection = db_connect()
    order_dicts = [order.model_dump() for order in new_orders]
    result = collection.insert_many(order_dicts)

    return {
        "inserted_count": len(order_dicts),
        "inserted_ids": [str(id) for id in result.inserted_ids],
    }


@router.put("/orders/{order_id}", response_model=OrderResponse)
def put_order(order_id: str, update_data: OrderUpdate):
    update_dict = update_data.model_dump(exclude_none=True)
    if not update_dict:
        raise HTTPException(400, detail="Нет данных для обновления")

    collection = db_connect()
    try:
        collection.update_one({"_id": ObjectId(order_id)}, {"$set": update_dict})
    except:
        raise HTTPException(404, detail="Заказ не найден")

    updated_doc = collection.find_one({"_id": ObjectId(order_id)})
    updated_doc["id"] = str(updated_doc.pop("_id"))
    return updated_doc
