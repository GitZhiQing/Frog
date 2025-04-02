from flask import Flask

from app.app_init import db_init, inject_vars, register_error, register_image_routes
from app.commands import register_commands
from app.config import config
from app.extensions import db
from app.hooks import register_hooks


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    # 初始化扩展
    db.init_app(app)

    # 注册命令行命令
    register_commands(app)

    # 注册蓝图
    from app.blueprints import blueprints

    for bp in blueprints:
        app.register_blueprint(bp)

    # 注册错误处理
    register_error(app)

    # 注册图片文件路由
    register_image_routes(app)

    # 模板上下文处理器
    app.context_processor(inject_vars)

    # 初始化数据库
    if app.config.get("FLASK_ENV", "development") != "production":
        db_init(app)

    # 请求钩子
    register_hooks(app)

    return app
