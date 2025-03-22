from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Tag(db.Model):
    __tablename__ = "tags"
    tid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10), unique=True)

    posts = relationship("Post", secondary="posts_tags", back_populates="tags")
