from datetime import datetime


class LoggingService:
    def __init__(self, logs_collection=None):
        self.logs_collection = logs_collection

    def log_request(
        self,
        timestamp: datetime,
        endpoint: str,
        method: str,
        duration_ms: float,
        status_code: int,
    ):
        result = {}

        log_entry = {
            "timestamp": timestamp,
            "endpoint": endpoint,
            "method": method,
            "duration_ms": duration_ms,
            "status_code": status_code,
        }

        if self.logs_collection is not None:
            result = self.logs_collection.insert_one(log_entry)

        return result
