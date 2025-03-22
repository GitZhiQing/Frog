import time

from flask import current_app, render_template, request
from sqlalchemy import select

from app.blueprints.nav import nav_bp
from app.extensions import db
from app.models import Post


@nav_bp.route("/")
@nav_bp.route("/index")
def index():
    return render_template("post.html", title="首页")


@nav_bp.route("/about")
def about():
    return render_template("post.html", title="关于")


@nav_bp.route("/status")
def status():
    show_all = request.args.get("show_all", False, type=bool)
    # 获取所有状态文章（保持按时间倒序）
    posts = (
        db.session.execute(select(Post).where(Post.category.has(name="status")).order_by(Post.created_at.desc()))
        .scalars()
        .all()
    )

    if not show_all:
        # 默认只取最新一条
        latest_post = posts[0] if posts else None
        post_title = latest_post.title
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(latest_post.created_at))
        return render_template("status.html", title="当前状态", post_title=post_title, date=date)

    # 历史模式：按年份分组
    grouped_posts = {}
    for post in posts:
        year = time.strftime("%Y", time.localtime(post.created_at))
        if year not in grouped_posts:
            grouped_posts[year] = []
        grouped_posts[year].append(
            {
                "title": post.title,
                "date": time.strftime("%m/%d", time.localtime(post.created_at)),
                "created_at": post.created_at,
            }
        )

    # 排序处理（与archive一致）
    sorted_years = sorted(grouped_posts.keys(), reverse=True)
    for year in sorted_years:
        grouped_posts[year].sort(key=lambda x: x["created_at"], reverse=True)

    return render_template(
        "status.html", title="历史状态", grouped_posts=grouped_posts, sorted_years=sorted_years, show_all=True
    )


@nav_bp.route("/archive")
def archive():
    category = request.args.get("category") or "all"
    tag = request.args.get("tag") or "all"
    posts = (
        db.session.execute(
            select(Post)
            .where(
                Post.category.has(name=category) if category != "all" else True,
                Post.tags.any(name=tag) if tag != "all" else True,
                ~Post.category.has(name="status"),
                ~Post.category.has(name="root"),
            )
            .order_by(Post.created_at.desc())
        )
        .scalars()
        .all()
    )
    grouped_posts = {}
    for post in posts:
        year = time.strftime("%Y", time.localtime(post.created_at))
        if year not in grouped_posts:
            grouped_posts[year] = []
        grouped_posts[year].append(
            {
                "title": post.title,
                "date": time.strftime("%m/%d", time.localtime(post.created_at)),
                "created_at": post.created_at,
            }
        )

    sorted_years = sorted(grouped_posts.keys(), reverse=True)
    for year in sorted_years:
        grouped_posts[year].sort(key=lambda x: x["created_at"], reverse=True)
    return render_template(
        "archive.html", title="归档", grouped_posts=grouped_posts, sorted_years=sorted_years, category=category, tag=tag
    )
