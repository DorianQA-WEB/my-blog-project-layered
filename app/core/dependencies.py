from app.core.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from app.core.database import AsyncSessionLocal
from app.repositories.categories import CategoryRepository
from app.repositories.posts import PostRepository
from app.services.categories import CategoryService
from app.services.posts import PostsService


async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db


# Зависимости для получения экземпляров репозиториев
def get_category_repository(db: AsyncSession = Depends(get_async_db)) -> CategoryRepository:
    return CategoryRepository(db=db)

def get_post_repository(db: AsyncSession = Depends(get_async_db)) -> PostRepository:
    return PostRepository(db=db)

# Зависимости для получения экземпляров сервисов
def get_category_service(db: AsyncSession = Depends(get_async_db)) -> CategoryService:
    return CategoryService(category_repo=CategoryRepository(db=db))

def get_post_service(db: AsyncSession = Depends(get_async_db)) -> PostsService:
    return PostsService(post_repo=PostRepository(db=db),
                        category_repo=CategoryRepository(db=db)) # Посту нужен доступ к категориям для валидации