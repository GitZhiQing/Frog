from flask import Blueprint

manage_bp = Blueprint("manage", __name__, url_prefix="/manage")

from app.blueprints.manage import routes  # noqa
