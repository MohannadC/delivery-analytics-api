from fastapi import APIRouter
from datetime import datetime, timedelta
from app.database import db_logs_connect

router = APIRouter()


@router.get("/metrics")
def get_metrics(time: float = 1):
    collection = db_logs_connect()

    time_threshold = datetime.now() - timedelta(hours=time)

    pipeline = [
        {"$match": {"timestamp": {"$gte": time_threshold}}},
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
                "rps": {"$divide": ["$total_requests", time * 3600]},
            },
        },
    ]
    results = list(collection.aggregate(pipeline))

    return results
