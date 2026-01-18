from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.repositories.categories import CategoryRepository
from app.services.categories import CategoryService



async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db


# Зависимости для получения экземпляров репозиториев
def get_category_repository(db: AsyncSession = Depends(get_async_db)) -> CategoryRepository:
    return CategoryRepository(db=db)

# Зависимости для получения экземпляров сервисов
def get_category_service(db: AsyncSession = Depends(get_async_db)) -> CategoryService:
    return CategoryService(category_repo=CategoryRepository(db=db))

