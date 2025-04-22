from celery.result import AsyncResult
from flask import jsonify
from sqlalchemy import func, select

from app.blueprints.manage import manage_bp
from app.extensions import db
from app.models.uv_records import UVRecord


@manage_bp.route("/uv/count")
def total_uv():
    count = db.session.scalar(select(func.count()).select_from(UVRecord))
    return jsonify({"count": count})


@manage_bp.get("/tasks/<id>/result")
def task_result(id: str) -> dict[str, object]:
    """获取异步任务状态"""
    result = AsyncResult(id)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }
