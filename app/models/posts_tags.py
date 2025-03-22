from sqlalchemy import Column, ForeignKey, Integer

from app.extensions import db

posts_tags = db.Table(
    "posts_tags",
    Column("pid", Integer, ForeignKey("posts.pid")),
    Column("tid", Integer, ForeignKey("tags.tid")),
)
