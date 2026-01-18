from sqlalchemy import Column, Integer, String

from app.core.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

    category_id = Column(Integer)# Нет ForeignKey, так как Category в другой БД

