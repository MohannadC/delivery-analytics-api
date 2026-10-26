from fastapi import APIRouter
from app.database import db_connect
from app.models import RestaurantRevenue, CancellationRate, BusinessWeekDays

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


@router.get("/analytics/cancelled", response_model=CancellationRate)
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


@router.get("/analytics/business", response_model=list[BusinessWeekDays])
def day_of_week_business():
    collection = db_connect()
    pipeline = [
        {"$group": {"_id": {"$dayOfWeek": "$created_at"}, "total_orders": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
        {
            "$project": {
                "_id": 0,
                "total_orders": 1,
                "day": {
                    "$switch": {
                        "branches": [
                            {"case": {"$eq": ["$_id", 1]}, "then": "Sunday"},
                            {"case": {"$eq": ["$_id", 2]}, "then": "Monday"},
                            {"case": {"$eq": ["$_id", 3]}, "then": "Tuesday"},
                            {"case": {"$eq": ["$_id", 4]}, "then": "Wednesday"},
                            {"case": {"$eq": ["$_id", 5]}, "then": "Thursday"},
                            {"case": {"$eq": ["$_id", 6]}, "then": "Friday"},
                            {"case": {"$eq": ["$_id", 7]}, "then": "Saturday"},
                        ],
                        "default": "No day of the week retrieved",
                    }
                },
            }
        },
    ]
    results = list(collection.aggregate(pipeline))

    return results
