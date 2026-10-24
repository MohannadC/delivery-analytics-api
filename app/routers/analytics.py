from fastapi import APIRouter, HTTPException
from database import db_connect
from models import RestaurantRevenue, CancellationRate
from bson import ObjectId
from bson.errors import InvalidId
from loguru import logger

router = APIRouter()


@router.get("/analytics/revenue", response_model=list[RestaurantRevenue])
def top_5_revenue():
    collection = db_connect()
    pipeline = [
        {"$group": {"_id": "$restaurant", "total_revenue": {"$sum": "$total_price"}}},
        {"$sort": {"total_revenue": -1}},
        {"$limit": 5},
    ]
    results = list(collection.aggregate(pipeline))

    for doc in results:
        doc["restaurant"] = doc.pop("_id")

    return results


@router.get("/analytics/cancelled")
def cancellation_rate():
    collection = db_connect()
    pipeline = [
        {
            "$group": {
                "_id": None,
                "total_orders": {"$sum": 1},
                "cancelled_orders": {
                    "$sum": {"$cond": [{"$eq": ["$status", "CANCELLED"]}, 1, 0]}
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "total_orders": 1,
                "cancelled_orders": 1,
                "cancelled_rate": {"$divide": ["$cancelled_orders", "$total_orders"]},
            }
        },
    ]
    results = list(collection.aggregate(pipeline))[0]

    return results
