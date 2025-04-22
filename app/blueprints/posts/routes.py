from flask import abort, request
from sqlalchemy import select

from app.blueprints.posts import posts_bp
from app.blueprints.posts.utils import handle_raw_action, handle_read_action
from app.extensions import db
from app.models import Post


@posts_bp.route("/<string:title>", methods=["GET", "POST"])
def get_post(title: str):
    """获取文章

    该路由对应两种动作(action)
    - action==raw: 此时路由相当于一个文档接口，返回原始文档数据(text/markdown)
    - action==read: 文档阅读页面，返回包装好的完整页面(text/html)
    """
    post = db.session.scalar(select(Post).where(Post.title == title))
    if not post:
        abort(404)

    action = request.args.get("action", "raw")
    action_handlers = {"raw": handle_raw_action, "read": handle_read_action}
    handler = action_handlers.get(action)
    if not handler:
        abort(404)

    request_path = request.path
    return handler(post, request_path)
