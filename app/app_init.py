from datetime import datetime

from flask import Flask, current_app, render_template, send_from_directory, url_for
from loguru import logger
from sqlalchemy import select

from app import models, utils
from app.extensions import db


def register_error(app: Flask) -> None:
    """注册错误处理"""

    @app.errorhandler(404)
    def page_not_found(_):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        logger.error(e)
        return render_template("errors/500.html"), 500


def register_image_routes(app: Flask) -> None:
    """注册图片文件路由"""

    @app.route("/imgs/<path:filename>")
    def article_image(filename):
        """
        文章图片
        """
        return send_from_directory(str(app.config.get("POST_IMGS_DIR")), filename)


def inject_vars() -> dict:
    """注入一些博客元信息"""
    now = datetime.now()
    env_vars = {
        "BLOG_NAME": current_app.config.get("BLOG_NAME", "Frog"),
        "BLOG_INTRO": current_app.config.get("BLOG_INTRO", "Gua Gua Gua"),
        "BLOG_AVATAR": current_app.config.get(
            "BLOG_AVATAR",
            url_for("static", filename="favicon.svg"),
        ),
        "NOW": {
            "year": now.year,
            "month": now.month,
            "day": now.day,
            "hour": now.hour,
            "minute": now.minute,
            "second": now.second,
        },
    }

    return env_vars


def db_init(app: Flask):
    """数据库初始化"""
    with app.app_context():
        try:
            db.drop_all()
            db.create_all()
            logger.info("数据库初始化完成!")
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
        logger.info("开始导入文档数据...")
        flat_dir_tree, _ = utils.get_flat_dir_tree(current_app.config.get("POST_DIR"))
        flat_meta_dir_tree, _ = utils.add_post_meta(flat_dir_tree, current_app.config.get("POST_DIR"))
        try:
            for item in flat_meta_dir_tree:
                if item["type"] == "file":
                    # 提取标题
                    filename = item["name"]
                    title = filename.rsplit(".", 1)[0]
                    directory = item["directory"]
                    tags = item.get("tags", [])
                    created_at = item.get("created_at")
                    relative_path = item.get("relative_path")
                    # 处理 Category
                    category = (
                        db.session.execute(select(models.Category).where(models.Category.name == directory))
                        .scalars()
                        .first()
                    )
                    if not category:
                        category = models.Category(name=directory)
                        db.session.add(category)

                    # 处理 Tags
                    tag_objs = []
                    for tag_name in tags:
                        tag = (
                            db.session.execute(select(models.Tag).where(models.Tag.name == tag_name)).scalars().first()
                        )
                        if not tag:
                            tag = models.Tag(name=tag_name)
                            db.session.add(tag)
                        tag_objs.append(tag)

                    # 创建 Post 并关联
                    post = models.Post(
                        title=title,
                        category=category,
                        tags=tag_objs,
                        created_at=created_at,
                        relative_path=relative_path,
                    )
                    db.session.add(post)

            db.session.commit()
            logger.info("文档数据导入完成!")
        except Exception as e:
            logger.error(f"文档数据导入错误: {e}")
