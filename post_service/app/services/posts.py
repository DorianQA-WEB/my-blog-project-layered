from fastapi import HTTPException, status
from typing import List, Optional

from app.repositories.posts import PostRepository
from app.schemas.post import PostBase, Post
from app.core.rabbitmq import RabbitMQCategoryValidator


class PostService:
    def __init__(self, post_repo: PostRepository, category_validator: RabbitMQCategoryValidator):
        self.post_repo = post_repo
        self.category_validator = category_validator

    async def get_all_posts(self, skip: int = 0, limit: int = 100) -> List[Post]:
        return await self.post_repo.get_all(skip=skip, limit=limit)

    async def get_post_by_id(self, post_id: int) -> Optional[Post]:
        return await self.post_repo.get_by_id(post_id)


    async def get_posts_by_category(
             self, category_id: int,
             skip: int = 0,
             limit: int = 100
    ) -> List[Post]:
        if category_id and not await self.category_validator.check_exists(category_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        return await self.post_repo.get_by_category_id(category_id, skip=skip, limit=limit)



    async def create_post(self, post: PostBase) -> Optional[Post]:
    # Бизнес-логика: проверяем существование категории перед созданием поста
        if not await self.category_validator.check_exists(post.category_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        # Если категория найдена, создаем пост
        return await self.post_repo.create(
            title=post.title,
            content=post.content,
            category_id=post.category_id
        )


