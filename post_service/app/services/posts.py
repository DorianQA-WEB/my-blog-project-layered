import os
from fastapi import HTTPException, status
from collections.abc import Sequence
import httpx

from app.models.post import Post as PostModel
from app.repositories.posts import PostRepository
from app.schemas.post import PostBase, Post

CATEGORIES_SERVICE_URL = os.getenv("CATEGORIES_SERVICE_URL", "http://127.0.0.1:8002")



class PostService:
    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    async def get_all_posts(self, skip: int = 0, limit: int = 100) -> Sequence[Post]:
        return await self.post_repo.get_all(skip=skip, limit=limit)

    async def get_post_by_id(self, post_id: int) -> Post | None:
        return await self.post_repo.get_by_id(post_id)


    async def get_posts_by_category(
             self, category_id: int,
             skip: int = 0,
             limit: int = 100
    ) -> Sequence[PostModel]:
        async with httpx.AsyncClient() as client:
            try:
            # Проверяем существование категории через Categories Service
                category_response = await client.get(
                    f"{CATEGORIES_SERVICE_URL}/categories/{category_id}")
                category_response.raise_for_status() # Выбрасывает исключение для 4xx/5xx

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise HTTPException(
                        status_code=400,
                        detail="invalid category_id: Category not found"
                    )
                raise HTTPException(status_code=e.response.status_code,
                                    detail=f"Error from Categories Service: {e.response.text}")
            except httpx.RequestError as e:
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                    detail=f"Categories service unavailable: {e}")

        return await self.post_repo.get_by_category_id(category_id, skip=skip, limit=limit)



    async def create_post(self, post: PostBase) -> Post | None:
    # Бизнес-логика: проверяем существование категории перед созданием поста
        async with httpx.AsyncClient() as client:
            try:
                category_response = await client.get(
                    f"{CATEGORIES_SERVICE_URL}/categories/{post.category_id}")
                category_response.raise_for_status() # Выбрасывает исключение для 4xx/5xx
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise HTTPException(
                        status_code=400,
                        detail="invalid category_id: Category not found"
                    )
                raise HTTPException(status_code=e.response.status_code,
                                    detail=f"Error from Categories Service: {e.response.text}")
            except httpx.RequestError as e:
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                    detail=f"Categories service unavailable: {e}")

        # Если категория найдена, создаем пост
        return await self.post_repo.create(
            title=post.title,
            content=post.content,
            category_id=post.category_id
        )


