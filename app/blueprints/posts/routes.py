import io
import time

import frontmatter
from flask import abort, current_app, render_template, request, send_file
from sqlalchemy import select

from app.blueprints.posts import posts_bp
from app.extensions import db
from app.models import Post


@posts_bp.route("/<string:title>")
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
        category = post.category.name
        tags = []
        for tag in post.tags:
            tags.append(tag.name)
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(post.created_at))
        return render_template("post.html", title=title, category=category, tags=tags, date=date)
