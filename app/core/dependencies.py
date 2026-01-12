from app.core.database import AsyncSessionLocal


async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db

