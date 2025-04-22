from celery import Celery, Task
from flask import Flask
from flask_mailman import Mail
from flask_sqlalchemy import SQLAlchemy
from loguru import logger
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

mail = Mail()


def celery_init_app(app: Flask) -> Celery:
    """初始化 celery 应用实例"""

    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask, include=["app.tasks"])
    logger.info(app.config["CELERY"])
    celery_app.config_from_object(app.config["CELERY"])

    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
