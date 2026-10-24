from fastapi import FastAPI, Request
from routers import orders, analytics
from time import time
from services.logging_service import LoggingService
from database import db_logs_connect

app = FastAPI()

app.include_router(orders.router)
app.include_router(analytics.router)
