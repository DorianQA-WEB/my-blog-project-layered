from collections import Sequence

from app.repositories.categories import CategoryRepository
from app.schemas.category import CategoryBase
from app.models.category import Category

class CategoryService:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def get_all_categories(self, skip: int = 0, limit: int =100) -> Sequence[Category]:
        db_categories = await self.category_repo.get_all(skip=skip, limit=limit)
        return db_categories

    async def get_category_by_id(self, category_id: int) -> Category | None:
        return await self.category_repo.get_by_id(category_id)

    async def create_category(self, category: CategoryBase) -> Category | None:
        existing_category = await self.category_repo.get_by_name(category.name)
        if existing_category:
            return None # Возвращаем None, если категория с таким именем уже есть
        return await self.category_repo.create(name=category.name)


