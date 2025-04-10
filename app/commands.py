import click
from flask.cli import with_appcontext

from app.utils import db_init


@click.command("init", help="初始化数据库并导入文档目录数据")
@with_appcontext
def init() -> None:
    db_init()
