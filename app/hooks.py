import uuid

from flask import Flask, make_response, request
from loguru import logger

from app.extensions import db
from app.models import UVRecord


def register_hooks(app: Flask):
    @app.before_request
    def track_uv():
        uv_id = request.cookies.get("uv_id")

        # 若无 Cookie，生成新 UV_ID 并写入数据库
        if not uv_id:
            uv_id = uuid.uuid4().hex
            try:
                with app.app_context():
                    record = UVRecord(uv_id=uv_id)
                    db.session.add(record)
                    db.session.commit()
            except Exception as e:
                logger.error(f"UV 记录生成错误: {str(e)}")
                db.session.rollback()

            resp = make_response()
            resp.set_cookie("uv_id", uv_id, max_age=365 * 24 * 60 * 60)
            return resp
