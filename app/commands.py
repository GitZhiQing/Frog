import click
from flask import Flask
from flask.cli import with_appcontext

from app.app_init import db_init


@click.command("init", help="初始化数据库并导入文档目录数据")
@with_appcontext
def init() -> None:
    db_init()


def register_commands(app: Flask) -> None:
    app.cli.add_command(init)
