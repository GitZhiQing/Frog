from flask import render_template
from loguru import logger


def page_not_found(_):
    return render_template("errors/404.html"), 404


def internal_server_error(error):
    logger.error(error)
    return render_template("errors/500.html"), 500
