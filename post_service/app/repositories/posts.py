from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.post import Post


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, post_id: int) -> Post:
        result = await self.db.scalar(select(Post).filter(Post.id == post_id))
        return result

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Post]:
        result = await self.db.scalars(select(Post).offset(skip).limit(limit))
        return result.all()

    async def get_by_category_id(self, category_id: int, skip: int = 0, limit: int = 100) -> list[Post]:
        result = await self.db.scalars(select(Post).where(Post.category_id == category_id).offset(skip).limit(limit))
        return result.all()

    async def create(self, title: str, content: str, category_id: int) -> Post:
        db_post = Post(
            title=title,
            content=content,
            category_id=category_id
        )
        self.db.add(db_post)
        await self.db.commit()
        await self.db.refresh(db_post)
        return db_post