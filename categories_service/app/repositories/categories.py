from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.category import Category

class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, category_id: int) -> Category | None:
        result = await self.db.scalar(select(Category).filter(Category.id == category_id))
        return result

    async def get_by_name(self, name: str) -> Category | None :
        result = await self.db.scalar(select(Category).filter(Category.name == name))
        return result

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Category]:
        result = self.db.scalars(select(Category).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, name: str):
        db_category = Category(name=name)
        self.db.add(db_category)
        await self.db.commit()
        await self.db.refresh(db_category)
        return db_category
