import asyncio
from contextlib import asynccontextmanager
from categories_service.app.core.database import DATABASE_URL
from fastapi import FastAPI, HTTPException, Depends
from typing import Optional
from app.api.router import categories
from app.core.database import create_db_and_tables
from app.core.rabbitmq_worker import run_consumer
import json
import time
from redis.asyncio as redis
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


limiter = Limiter(key_func=get_remote_address)

redis_client: Optianal[redis.Redis] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение категорий запускается. Создаем базу данных и запускаем RabbitMQ consumer...")
    consumer_task = asyncio.create_task(run_consumer())
    global redis_client
    await create_db_and_tables()
    global DATABASE_URL
    redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    try:
        await redis_client.ping()
        print("Redis доступен.")
    except redis.ConnectionError as e:
        print(f"Ошибка подключения к Redis: {e}")
        redis_client = None # Установливаем None, чтобы запросы могли продолжаться без кэширования
    print("Инициализация завершена.")
    yield
    print("Приложение категорий завершает работу. Останавливаем consumer...")
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        print("Consumer RabbitMQ успешно остановлен.")
    if redis_client:
        await redis_client.close()
        print("Redis закрыт.")


app = FastAPI(
    title="Сервис для категорий (связь через RabbitMQ)",
    lifespan=lifespan
)

app.include_router(categories.router)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Зависимость для получения клиента Redis в маршрутах
async def get_redis_client_dependency():
    if redis_client is None:
        raise HttpException(status_code=503, detail="Redis недоступен")
    return redis_client


@app.get("/")
async def root():
    """Корневой эндпоинт."""
    return {"message": "Простой блог на FastAPI с SQLAlchemy 2.0"}

# Тест подключения к Redis
@app.get("/redis-test")
async def redis_connect_test(r: redis.Redis = Depends(get_redis_client_dependency)):
    await r.ping()
    return {"message": "Redis доступен"}

