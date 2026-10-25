from fastapi import APIRouter
from loguru import logger
from database import db_logs_connect

router = APIRouter()


@router.get("/metrics")
def get_metrics():
    collection = db_logs_connect()

    pipeline = [
        {
            "$group": {
                "_id": None,
                "all_durations": {"$push": "$duration_ms"},
                "total_errors": {
                    "$sum": {"$cond": [{"$gte": ["$status_code", 500]}, 1, 0]}
                },
                "total_requests": {"$sum": 1},
            }
        },
        {
            "$project": {
                "total_requests": 1,
                "total_errors": 1,
                "sorted_durations": {
                    "$sortArray": {"input": "$all_durations", "sortBy": 1}
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "total_requests": 1,
                "total_errors": 1,
                "p50": {
                    "$arrayElemAt": [
                        "$sorted_durations",
                        {"$floor": {"$divide": ["$total_requests", 2]}},
                    ]
                },
                "p95": {
                    "$arrayElemAt": [
                        "$sorted_durations",
                        {"$floor": {"$multiply": ["$total_requests", 0.95]}},
                    ]
                },
                "p99": {
                    "$arrayElemAt": [
                        "$sorted_durations",
                        {"$floor": {"$multiply": ["$total_requests", 0.99]}},
                    ]
                },
            }
        },
    ]
    results = list(collection.aggregate(pipeline))

    return results
