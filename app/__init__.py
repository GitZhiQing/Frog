from flask import Flask, send_from_directory

from app.commands import register_commands
from app.config import config
from app.extensions import db
from app.utils import inject_env_vars


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    # 初始化扩展
    db.init_app(app)

    # 注册命令行命令
    register_commands(app)

    # 上下文管理器
    app.context_processor(inject_env_vars)

    # 注册蓝图
    from app.blueprints import blueprints

    for bp in blueprints:
        app.register_blueprint(bp)

    # 注册图片文件路由
    register_imgs_routes(app)

    # 注册错误处理
    with app.app_context():
        from app import errors  # noqa
    return app


def register_imgs_routes(app: Flask) -> None:
    """注册图片文件路由"""

    @app.route("/imgs/<path:filename>")
    def article_image(filename):
        """
        文章图片
        """
        return send_from_directory(str(app.config.get("POST_IMGS_DIR")), filename)
