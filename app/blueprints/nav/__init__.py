from flask import Blueprint

nav_bp = Blueprint("nav", __name__, url_prefix="")

from app.blueprints.nav import routes  # noqa
