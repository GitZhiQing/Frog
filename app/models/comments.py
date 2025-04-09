from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin


class Comment(db.Model, TimestampMixin):
    __tablename__ = "comments"
    cid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(128))
    link: Mapped[str] = mapped_column(String(64))
    content: Mapped[str] = mapped_column(Text)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("comments.cid"), nullable=True)  # 自关联回复
    post_path: Mapped[str] = mapped_column(String(256), ForeignKey("posts.relative_path"))  # 关联文章路径

    parent = relationship(
        "Comment",
        remote_side=[cid],
        back_populates="replies",
        foreign_keys=[parent_id],  # 明确指定外键
    )
    replies = relationship(
        "Comment",
        back_populates="parent",
    )
    post = relationship("Post", back_populates="comments")
