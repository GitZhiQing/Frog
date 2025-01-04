from flask import Blueprint, render_template
from app import utils
from app import models

bp = Blueprint("main", __name__)


@bp.route("/archive")
def archive():
    """归档页"""
    articles = models.Article.query.order_by(models.Article.created_at.desc()).all()
    archive = {}
    for article in articles:
        if article.category.name == "root":
            continue
        year = article.created_at.year
        month_day = article.created_at.strftime("%m/%d")
        if year not in archive:
            archive[year] = []
        archive[year].append({"month_day": month_day, "article": article})
    return render_template("archive.html", archive=archive, active_nav_route="archive")


@bp.route("/categories")
def categories():
    """展示所有分类"""
    categories = models.Category.query.all()
    categories_data = []

    for category in categories:
        if category.name == "root" or not category.articles:
            continue
        doc_count = len(category.articles)
        categories_data.append({"name": category.name, "count": doc_count})

    return render_template(
        "categories.html", categories=categories_data, active_nav_route="categories"
    )


@bp.route("/categories/<category>")
def category(category):
    """分类页
    分类即直接展示当前目录（category）下的所有文章
    """
    category_obj = models.Category.query.filter_by(name=category).first_or_404()
    articles = (
        models.Article.query.filter_by(category_id=category_obj.id)
        .order_by(models.Article.created_at.desc())
        .all()
    )
    return render_template("category.html", articles=articles, category=category)


@bp.route("/tags")
def tags():
    """展示所有标签"""
    tags = models.Tag.query.all()
    tags_data = []

    for tag in tags:
        article_count = len(tag.articles)
        tags_data.append({"name": tag.name, "count": article_count})

    return render_template("tags.html", tags=tags_data, active_nav_route="tags")


@bp.route("/tags/<tag>")
def tag(tag):
    """标签页"""
    tag_obj = models.Tag.query.filter_by(name=tag).first_or_404()
    articles = (
        models.Article.query.filter(models.Article.tags.contains(tag_obj))
        .order_by(models.Article.created_at.desc())
        .all()
    )
    return render_template("tag.html", articles=articles, tag=tag)


@bp.route("/articles/<string:title>")
def article(title):
    """阅读文章页"""
    article = models.Article.query.filter_by(title=title).first()
    doc_path = article.path
    html_content, meta = utils.parse_md(doc_path)
    meta["category"] = article.category.name
    return render_template("article.html", html_content=html_content, metadata=meta)
