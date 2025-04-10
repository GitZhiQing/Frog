import click
from flask.cli import with_appcontext

from app.utils import db_init


@click.command("init", help="初始化数据库并导入文档目录数据")
@click.option("--all", "drop_all", is_flag=True, help="删除所有现有数据表并重新初始化")
@with_appcontext
def init(drop_all: bool = False) -> None:
    db_init(drop_all=drop_all)
