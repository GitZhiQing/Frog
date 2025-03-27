from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin


class Post(db.Model, TimestampMixin):
    __tablename__ = "posts"
    pid: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(64), index=True)
    relative_path: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.cid"))

    category = relationship("Category", back_populates="posts")
    tags = relationship("Tag", secondary="posts_tags", back_populates="posts")
