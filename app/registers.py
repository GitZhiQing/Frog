from flask import Flask, send_from_directory


def register_image_routes(app: Flask) -> None:
    """注册图片文件路由"""

    @app.route("/imgs/<path:filename>")
    def article_image(filename):
        """
        文章图片
        """
        return send_from_directory(str(app.config.get("POST_IMGS_DIR")), filename)


def register_commands(app: Flask) -> None:
    """注册应用命令行"""
    from app.commands import init

    app.cli.add_command(init)


def register_extensions(app: Flask) -> None:
    """注册应用扩展"""
    from app.extensions import db

    db.init_app(app)


def register_errors(app: Flask) -> None:
    """注册错误处理器"""
    from app.errors import internal_server_error, page_not_found

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)


def register_blueprints(app: Flask) -> None:
    """注册应用蓝图"""
    from app.blueprints import blueprints

    for bp in blueprints:
        app.register_blueprint(bp)


def register_filters(app: Flask) -> None:
    """注册模板过滤器"""
    from app.filters import ts2date

    app.add_template_filter(ts2date, "ts2date")


def register_hooks(app: Flask) -> None:
    """注册请求钩子"""
    from app.hooks import set_uv_cookie, track_uv

    app.before_request(track_uv)
    app.after_request(set_uv_cookie)


def register_tp_ctx(app: Flask) -> None:
    """注册模板上下文"""
    from app.utils import blog_meta

    app.context_processor(blog_meta)
