from datetime import UTC, datetime, timedelta

from flask import flash, redirect, render_template, request
from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.blueprints.nav import nav_bp
from app.extensions import db
from app.forms import CommentForm
from app.models import Comment, Post


@nav_bp.route("/")
@nav_bp.route("/index")
def index():
    return render_template("post.html", title="首页")


@nav_bp.route("/about", methods=["GET", "POST"])
def about():
    form = CommentForm()
    # 处理POST请求
    if form.validate_on_submit():
        try:
            comment = Comment(
                post_path="关于.md",
                post_title="关于",
                name=form.name.data,
                email=form.email.data,
                link=form.link.data,
                content=form.content.data,
                parent_id=int(form.parent_id.data) if form.parent_id.data else None,
            )
            db.session.add(comment)
            db.session.commit()

            from app.tasks import send_comment_notification

            result = send_comment_notification.delay(comment.to_dict(), request_path=request.path)
            logger.info(f"创建邮件发送任务: {result.id}")
            flash("评论提交成功！", "success")
            return redirect(f"{request.url}#comment-{comment.cid}")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"评论提交失败: {str(e)}")
            flash("评论提交失败，请稍后再试", "danger")
        except ValueError:
            logger.error(f"非法父评论ID: {form.parent_id.data}")
            flash("非法评论参数", "danger")
        except Exception as e:
            logger.error(f"评论提交错误: {str(e)}")
            flash("评论提交失败，请稍后再试", "danger")
    comments = db.session.execute(select(Comment).where(Comment.post_path == "关于.md")).scalars().all()
    return render_template("post.html", title="关于", form=form, comments=comments)


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
        return render_template("status.html", title="当前状态", post=latest_post)

    # 历史模式：按年份分组
    grouped_posts = {}
    for post in posts:
        dt_shanghai = datetime.fromtimestamp(post.created_at, tz=UTC) + timedelta(hours=8)
        year = dt_shanghai.strftime("%Y")
        if year not in grouped_posts:
            grouped_posts[year] = []
        grouped_posts[year].append(
            {
                "title": post.title,
                "date": dt_shanghai.strftime("%m/%d"),
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
        dt_shanghai = datetime.fromtimestamp(post.created_at, tz=UTC) + timedelta(hours=8)
        year = dt_shanghai.strftime("%Y")
        if year not in grouped_posts:
            grouped_posts[year] = []
        grouped_posts[year].append(
            {
                "title": post.title,
                "date": dt_shanghai.strftime("%m/%d"),
                "created_at": post.created_at,
            }
        )

    sorted_years = sorted(grouped_posts.keys(), reverse=True)
    for year in sorted_years:
        grouped_posts[year].sort(key=lambda x: x["created_at"], reverse=True)
    return render_template(
        "archive.html", title="归档", grouped_posts=grouped_posts, sorted_years=sorted_years, category=category, tag=tag
    )
