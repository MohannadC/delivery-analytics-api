from fastapi import APIRouter, Request
from models import LogCreate
from services.logging_service import LoggingService
from database import db_logs_connect
from services.random_service import (
    generate_random_date,
    generate_random_endpoint,
    generate_realistic_latency,
)
from random import random

router = APIRouter()


@router.post("/logs/generate_fake")
def generate_fake_logs(new_logs: LogCreate, request: Request):
    log_service = LoggingService(db_logs_connect())

    results = []
    logs = new_logs.model_dump()
    for _ in range(0, logs["number_of_logs"]):
        random_endpoint = generate_random_endpoint(request.app)
        probability = random()
        result = log_service.log_request(
            generate_random_date(logs["days"]),
            random_endpoint["endpoint"],
            random_endpoint["method"],
            generate_realistic_latency(),
            200 if probability < 0.98 else 505,
        )
        results.append(str(result.inserted_id))

    return results
