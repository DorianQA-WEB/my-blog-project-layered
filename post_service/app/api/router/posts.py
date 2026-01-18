from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_post_service
from app.schemas.post import Post, PostBase
from app.services.posts import PostService

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Post not found"}},
)

@router.get("/", response_model=list[Post])
async def read_posts(
        skip: int = 0,
        limit: int = 100,
        post_service: PostService = Depends(get_post_service) # Инъекция сервиса поста
):
    """Получить список всех постов."""
    posts = await post_service.get_all_posts(skip=skip, limit=limit)
    return posts

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
        post: PostBase,
        post_service: PostService = Depends(get_post_service) # Инъекция сервиса поста
):
    """Создать новый пост."""
    # Сервис вернет None, если категория не найдена или другая бизнес-логика запрещает создание
    db_post = await post_service.create_post(post=post)
    if db_post is None:
        # Здесь можно более точно определить причину, но мы упрощаем это, для простоты понимания
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category_id or unable to create post",
        )
    return db_post

@router.get("/{post_id}", response_model=Post)
async def read_post(
        post_id: int,
        post_service: PostService = Depends(get_post_service) # Инъекция сервиса поста
):
    """Получить пост по ID."""
    db_post = await post_service.get_post_by_id(post_id=post_id)
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return db_post

