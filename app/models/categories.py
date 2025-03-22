from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Category(db.Model):
    __tablename__ = "categories"
    cid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10), unique=True)

    posts = relationship("Post", back_populates="category")
