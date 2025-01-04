from app.extensions import db


class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
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
    db.Column("article_id", db.Integer, db.ForeignKey("articles.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.path"), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    article = db.relationship("Article", back_populates="comments")
    replies = db.relationship(
        "Comment", backref=db.backref("parent", remote_side=[id]), lazy=True
    )


Article.comments = db.relationship("Comment", back_populates="article", lazy=True)
