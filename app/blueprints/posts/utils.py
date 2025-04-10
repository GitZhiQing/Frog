import io

import frontmatter
from flask import abort, current_app, flash, redirect, render_template, request, send_file
from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.forms import CommentForm
from app.models import Comment, Post


def handle_raw_action(post: Post):
    """处理原始文件请求"""
    try:
        if post.category.name == "root":
            post_path = current_app.config.get("POST_DIR") / f"{post.title}.md"
        else:
            post_path = current_app.config.get("POST_DIR") / post.category.name / f"{post.title}.md"

        with open(post_path, encoding="utf-8") as f:
            post_content = frontmatter.load(f)

        return send_file(io.BytesIO(post_content.content.encode()), mimetype="text/markdown")
    except OSError as e:
        logger.error(f"文件读取错误: {str(e)}")
        abort(500)


def handle_read_action(post: Post):
    """处理阅读页面请求"""
    form = CommentForm()

    # 处理POST请求
    if form.validate_on_submit():
        try:
            comment = Comment(
                post=post,  # 直接关联Post对象
                name=form.name.data,
                email=form.email.data,
                link=form.link.data,
                content=form.content.data,
                parent_id=int(form.parent_id.data) if form.parent_id.data else None,
            )
            db.session.add(comment)
            db.session.commit()
            flash("评论提交成功！", "success")
            return redirect(f"{request.url}#comment-{comment.cid}")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"评论提交失败: {str(e)}")
            flash("评论提交失败，请稍后再试", "danger")
        except ValueError:
            logger.error(f"非法父评论ID: {form.parent_id.data}")
            flash("非法评论参数", "danger")

    # 获取关联评论（通过关系属性）
    comments = db.session.execute(select(Comment).where(Comment.post_path == post.relative_path)).scalars().all()
    return render_template(
        "post.html",
        title=post.title,
        post=post,
        form=form,
        comments=comments,
    )
