from datetime import datetime, timedelta
import random
from random import choice


def get_available_endpoints(app) -> list[dict]:
    endpoints = []

    openapi_schema = app.openapi()

    for path, methods_dict in openapi_schema["paths"].items():
        if path in [
            "/logs/generate_fake",
            "/openapi.json",
            "/docs",
            "/docs/oauth2-redirect",
            "/redoc",
        ]:
            continue

        methods = [method.upper() for method in methods_dict.keys()]

        endpoints.append({"path": path, "methods": methods})

    return endpoints


def generate_random_endpoint(app) -> dict:
    endpoints = get_available_endpoints(app)
    random_route = choice(endpoints)
    random_method = choice(random_route["methods"])

    return {"endpoint": random_route["path"], "method": random_method}


def generate_random_date(days_back: int) -> datetime:
    now = datetime.now()
    start_date = now - timedelta(days=days_back)
    total_seconds = int((now - start_date).total_seconds())

    return start_date + timedelta(seconds=random.uniform(0, total_seconds))


def generate_realistic_latency(
    mean: float = 50,
    std_dev: float = 15,
    slow_mean: float = 300,
    slow_std_dev: float = 100,
    very_slow_mean: float = 3000,
    very_slow_std_dev: float = 1000,
    min_value: float = 0,
) -> float:
    """
    Генерирует реалистичное время отклика с выбросами:
    - 95% запросов: нормальные (вокруг mean)
    - 4% запросов: медленные (вокруг slow_mean)
    - 1% запросов: очень медленные (вокруг very_slow_mean)
    """
    probability = random.random()

    if probability < 0.95:
        return max(min_value, random.gauss(mean, std_dev))
    elif probability < 0.99:
        return max(min_value, random.gauss(slow_mean, slow_std_dev))
    else:
        return max(min_value, random.gauss(very_slow_mean, very_slow_std_dev))
