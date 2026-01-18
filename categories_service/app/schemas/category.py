from pydantic import BaseModel
from pydantic import ConfigDict

class CategoryBase(BaseModel):
    name: str


class Category(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
