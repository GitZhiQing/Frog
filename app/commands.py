import click
from flask import Flask, current_app
from flask.cli import with_appcontext
from loguru import logger
from sqlalchemy import select

from app import models, utils
from app.extensions import db


@click.command("init", help="初始化数据库并导入文档目录数据")
@with_appcontext
def init():
    try:
        db.drop_all()
        db.create_all()
        click.echo("数据库初始化完成!")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
    click.echo("开始导入文档数据...")
    flat_dir_tree, _ = utils.get_flat_dir_tree(current_app.config.get("POST_DIR"))
    flat_tags_dir_tree, _ = utils.add_post_tags(flat_dir_tree, current_app.config.get("POST_DIR"))
    try:
        for item in flat_tags_dir_tree:
            if item["type"] == "file":
                # 提取标题
                filename = item["name"]
                title = filename.rsplit(".", 1)[0]
                directory = item["directory"]
                tags = item.get("tags", [])

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
                    tag = db.session.execute(select(models.Tag).where(models.Tag.name == tag_name)).scalars().first()
                    if not tag:
                        tag = models.Tag(name=tag_name)
                        db.session.add(tag)
                    tag_objs.append(tag)

                # 创建 Post 并关联
                post = models.Post(title=title, category=category, tags=tag_objs)
                db.session.add(post)

        db.session.commit()
        click.echo("文档数据导入完成!")
    except Exception as e:
        logger.error(f"文档数据导入错误: {e}")


def register_commands(app: Flask):
    app.cli.add_command(init)
