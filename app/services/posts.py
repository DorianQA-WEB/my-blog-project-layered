from collections import Sequence
from app.repositories.posts import PostRepository
from app.schemas.post import PostBase
from app.models.post import Post
from app.repositories.categories import CategoryRepository


from app.models.post import Post

class PostsService:
    def __init__(self, post_repo: PostRepository, category_repo: CategoryRepository):
        self.post_repo = post_repo
        self.category_repo = category_repo

    async def get_all_posts(self, skip: int = 0, limit: int = 100) -> Sequence[Post]:
        return await self.post_repo.get_all(skip, limit)

    async def get_post_by_id(self, post_id: int) -> Post | None:
        result = await self.post_repo.get_by_id(post_id)

    async def get_posts_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> Sequence[Post] | None:
        category = await self.category_repo.get_by_id(category_id)
        if category is None:
            # В сервисе можем вернуть None или поднять специфичное исключение сервисного уровня
            # Роутер обработает это и вернет соответствующий HTTP ответ
            return None
        return await self.post_repo.get_by_category_id(category_id, skip=skip, limit=limit)

    async def create_post(self, post_data: PostBase) -> Post | None:
    # Бизнес-логика: проверяем существование категории перед созданием поста
        category = await self.category_repo.get_by_id(post_data.category_id)
        if category is None:
            return None # Возвращаем None, если категория не найдена

        return await self.post_repo.create(
            title=post_data.title,
            content=post_data.content,
            category_id=post_data.category_id
        )




