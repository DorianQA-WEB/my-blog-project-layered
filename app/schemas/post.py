from pydantic import BaseModel
from pydantic import ConfigDict

class PostBase(BaseModel):
    title: str
    content: str
    category_id: int

class Post(PostBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
