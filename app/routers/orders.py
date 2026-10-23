from fastapi import APIRouter
from database import db_connect
from models import OrderResponse, OrderCreate

router = APIRouter()


@router.get("/orders", response_model=list[OrderResponse])
def get_orders():
    collection = db_connect()
    results = collection.find({})

    orders = []
    for doc in results:
        doc["id"] = str(doc.pop("_id"))
        orders.append(OrderResponse(**doc))
    return orders
