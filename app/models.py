from app.extensions import db
import time


class Article(db.Model):
    __tablename__ = "articles"
    path = db.Column(db.String(255), nullable=False, unique=True, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(
        db.Integer, default=int(time.time()), onupdate=int(time.time())
    )
    tags = db.relationship("Tag", secondary="articles_tags", back_populates="articles")


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    articles = db.relationship("Article", backref="category", lazy=True)


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    articles = db.relationship(
        "Article", secondary="articles_tags", back_populates="tags"
    )


articles_tags = db.Table(
    "articles_tags",
    db.Column(
        "article_path", db.Integer, db.ForeignKey("articles.path"), primary_key=True
    ),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)
