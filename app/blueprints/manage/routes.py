from flask import jsonify
from sqlalchemy import func, select

from app.blueprints.manage import manage_bp
from app.extensions import db
from app.models.uv_records import UVRecord


@manage_bp.route("/uv/count")
def total_uv():
    count = db.session.scalar(select(func.count()).select_from(UVRecord))
    return jsonify({"count": count})
