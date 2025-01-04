import click
from flask import current_app
from flask.cli import with_appcontext

from app import utils
from app.models import db


@click.command("initdb")
@with_appcontext
def init_db():
    """初始化数据库并初始化文章"""
    try:
        db.drop_all()
        db.create_all()
        click.echo("[+] 数据库初始化完成")
    except Exception as e:
        click.echo(f"[-] 数据库初始化失败: {e}")
        return

    try:
        root = current_app.config["MD_ROOT"]
        utils.init_articles(root)
        click.echo("[+] 文章初始化完成")
    except Exception as e:
        click.echo(f"[-] 文章初始化失败: {e}")


def register_commands(app):
    app.cli.add_command(init_db)
