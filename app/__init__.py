from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")

    from app.routes import bp as main_bp

    app.register_blueprint(main_bp, url_prefix="/")

    with app.app_context():
        from app import errors  # noqa

    @app.context_processor
    def inject_blog_name():
        return dict(
            blog_name=app.config.get("BLOG_NAME", "Frog"),
            blog_desc=app.config.get("BLOG_DESC", "Gua Gua Gua"),
        )

    return app
