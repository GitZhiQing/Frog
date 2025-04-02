import uuid

from flask import Flask, g, request
from loguru import logger

from app.extensions import db
from app.models import UVRecord


def register_hooks(app: Flask):
    @app.before_request
    def track_uv():
        uv_id = request.cookies.get("uv_id")
        # 若无 Cookie，生成新 UV_ID 并暂存到 g 对象
        if not uv_id:
            uv_id = uuid.uuid4().hex
            g.new_uv_id = uv_id

            # 创建 UV 记录并添加到数据库会话（暂不提交，由 Flask-SQLAlchemy 自动处理事务）
            try:
                record = UVRecord(uv_id=uv_id)
                db.session.add(record)
                db.session.commit()
            except Exception as e:
                logger.error(f"UV 记录创建失败: {str(e)}")
                db.session.rollback()
                g.new_uv_id = None  # 清除无效的 UV_ID

    @app.after_request
    def set_uv_cookie(response):
        # 检查是否有新生成的 UV_ID 需要设置 Cookie
        new_uv_id = getattr(g, "new_uv_id", None)
        if new_uv_id:
            response.set_cookie("uv_id", new_uv_id, max_age=365 * 24 * 60 * 60)
        return response
