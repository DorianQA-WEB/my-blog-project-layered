from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.core.dependencies import get_category_service
from app.schemas.category import Category, Category, CategoryBase
from app.services.categories import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("/", response_model=List[Category])
async def read_categories(
        skip: int = 0,
        limit: int = 100,
        category_service: CategoryService = Depends(get_category_service) # Инъекция сервиса
):
    """Получить список всех категорий."""
    categories = await category_service.get_all_categories(skip=skip, limit=limit)
    return categories


@router.post("/", response_model=Category)
async def create_category(
        category: CategoryBase,
        category_service: CategoryService = Depends(get_category_service) # Инъекция сервиса
):
    """Создать новую категорию."""
    db_category = await category_service.create_category(category=category)
    if db_category is None:
        raise HTTPException(status_code=400, detail="Category with this name already exists")
    return db_category