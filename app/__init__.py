from flask import Flask

from app.config import config
from app.registers import (
    register_blueprints,
    register_commands,
    register_errors,
    register_extensions,
    register_filters,
    register_hooks,
    register_image_routes,
    register_tp_ctx,
)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    # 注册应用扩展
    register_extensions(app)

    # 注册命令行命令
    register_commands(app)

    # 注册蓝图
    register_blueprints(app)

    # 注册错误处理
    register_errors(app)

    # 注册模板过滤器
    register_filters(app)

    # 模板上下文处理器
    register_tp_ctx(app)

    # 注册图片文件路由
    register_image_routes(app)

    # 请求钩子
    register_hooks(app)

    return app
