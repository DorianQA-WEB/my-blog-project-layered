from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from app.core.database import AsyncSessionLocal
from app.repositories.posts import PostRepository
from app.services.posts import PostService


async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db


# Зависимости для получения экземпляров репозиториев
def get_post_repository(db: AsyncSession = Depends(get_async_db)) -> PostRepository:
    return PostRepository(db=db)


def get_post_service(post_repo: PostRepository = Depends(get_post_repository)) -> PostService:
    return  PostService(post_repo=post_repo)# Посту нужен доступ к категориям для валидации