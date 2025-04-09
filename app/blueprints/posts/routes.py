import io
from datetime import UTC, datetime, timedelta

import frontmatter
from flask import abort, current_app, flash, redirect, render_template, request, send_file
from loguru import logger
from sqlalchemy import select

from app.blueprints.posts import posts_bp
from app.extensions import db
from app.forms import CommentForm
from app.models import Comment, Post


@posts_bp.route("/<string:title>", methods=["GET", "POST"])
def get_post(title: str):
    """获取文章"""
    action = request.args.get("action", "raw")  # raw | read
    post = db.session.execute(select(Post).where(Post.title == title)).scalar()
    if post is None:
        abort(404)
    if post.category.name == "root":
        post_path = current_app.config.get("POST_DIR") / f"{title}.md"
    else:
        post_path = current_app.config.get("POST_DIR") / post.category.name / f"{title}.md"

    if action == "raw":
        with open(post_path, encoding="utf-8") as f:
            post_content = frontmatter.load(f)
        return send_file(io.BytesIO(post_content.content.encode()), mimetype="text/markdown")
    else:
        form = CommentForm()
        category = post.category.name
        tags = []
        for tag in post.tags:
            tags.append(tag.name)
        dt_shanghai = datetime.fromtimestamp(post.created_at, tz=UTC) + timedelta(hours=8)
        dt_shanghai_str = dt_shanghai.strftime("%Y-%m-%d %H:%M:%S")

        if form.validate_on_submit():
            try:
                comment = Comment(
                    post_path=post.relative_path,
                    name=form.name.data,
                    email=form.email.data,
                    link=form.link.data,
                    content=form.content.data,
                    parent_id=int(form.parent_id.data) if form.parent_id.data else None,
                )
                db.session.add(comment)
                db.session.commit()
                logger.info(f"{comment.name} 评论了 {post.title}")
                return redirect(f"{request.url}#comment-{comment.cid}")
            except Exception as e:
                logger.error(f"评论失败: {e}")
                flash("评论失败!")
                return redirect(request.referrer)
        comments = db.session.execute(select(Comment).where(Comment.post_path == post.relative_path)).scalars().all()
        logger.info(f"comments: {comments}")
        return render_template(
            "post.html",
            title=title,
            category=category,
            tags=tags,
            date=dt_shanghai_str,
            form=form,
            comments=comments,
        )
