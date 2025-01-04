from flask import Flask, send_from_directory
from app import utils, extensions
from app.commands import register_commands

from pathlib import Path


def create_app():
    app = Flask(__name__)

    # 导入应用配置
    configure_app(app)

    # 注册扩展
    register_extensions(app)

    # 注册命令
    register_commands(app)

    # 注册蓝图
    register_blueprints(app)

    # 添加动态导航页面
    add_dynamic_routes(app, app.config["MD_ROOT"])

    # 注册错误处理
    register_error_handlers(app)

    # 添加上下文处理器
    register_context_processors(app)

    # 注册静态文件路由
    register_static_routes(app)

    return app


def configure_app(app: Flask) -> None:
    """配置应用"""
    from app.config import Config

    app.config.from_object(Config)


def register_extensions(app: Flask) -> None:
    """注册扩展"""
    extensions.db.init_app(app)


def register_blueprints(app: Flask) -> None:
    """注册蓝图"""
    from app.routes import main_bp

    app.register_blueprint(main_bp, url_prefix="/")


def register_error_handlers(app: Flask) -> None:
    """注册错误处理"""
    with app.app_context():
        from app import errors  # noqa


def register_context_processors(app: Flask) -> None:
    """注册上下文处理器"""

    @app.context_processor
    def inject_global_data():
        md_root = Path(app.config["MD_ROOT"])
        nav_data = utils.get_nav_data(md_root)
        return dict(
            blog_name=app.config.get("BLOG_NAME", "Frog"),
            blog_desc=app.config.get("BLOG_DESC", "Gua Gua Gua"),
            blog_admin_name=app.config.get("BLOG_ADMIN_NAME", "Frog"),
            blog_admin_email=app.config.get("BLOG_ADMIN_EMAIL", "admin@frog.com"),
            blog_admin_signature=app.config.get("BLOG_ADMIN_SIGNATURE", "Gua Gua Gua"),
            nav_data=nav_data,
        )


def register_static_routes(app: Flask) -> None:
    """注册静态文件路由"""

    @app.route("/imgs/<path:filename>")
    def article_image(filename):
        """
        文章图片
        """
        return send_from_directory(
            str(app.config.get("ARTICLE_IMAGE_PATH", "")), filename
        )


def add_dynamic_routes(app: Flask, md_root: Path) -> None:
    """动态添加路由"""
    for md_file in utils.get_md_files(md_root):
        _, metadata = utils.parse_md(md_file)
        nav_route = f"/{metadata.get('nav_route', '')}"
        endpoint = f"nav_{metadata.get('nav_route', '')}"

        if nav_route == "/index":
            app.add_url_rule(
                "/",
                view_func=lambda md_file=md_file: utils.nav_view_func(md_file),
                endpoint="index",
                methods=["GET"],
            )

        app.add_url_rule(
            nav_route,
            view_func=lambda md_file=md_file: utils.nav_view_func(md_file),
            endpoint=endpoint,
            methods=["GET"],
        )
