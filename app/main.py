from fastapi import FastAPI, Request
from routers import orders, analytics, logs
from time import time
from services.logging_service import LoggingService
from database import db_logs_connect
from datetime import datetime

app = FastAPI()

logging_service = LoggingService(
    logs_collection=db_logs_connect(),
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()

    response = await call_next(request)

    logging_service.log_request(
        timestamp=datetime.now(),
        endpoint=request.url.path,
        method=request.method,
        duration_ms=round((time() - start_time) * 1000, 2),
        status_code=response.status_code,
    )

    return response


app.include_router(orders.router)
app.include_router(analytics.router)
app.include_router(logs.router)
