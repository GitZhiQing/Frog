import subprocess

import click
from flask import current_app
from flask.cli import with_appcontext
from loguru import logger

from app.utils import db_init


@click.command("init", help="初始化数据库并导入文档目录数据")
@click.option("--all", "drop_all", is_flag=True, help="删除所有现有数据表并重新初始化")
@with_appcontext
def init(drop_all: bool = False) -> None:
    db_init(drop_all=drop_all)


@click.command("compose", help="在项目目录下执行 docker compose build 和 docker compose up -d")
@with_appcontext
def compose() -> None:
    project_dir = current_app.config.get("PROJECT_DIR")
    if not project_dir:
        logger.warning("PROJECT_DIR 未配置，请检查配置文件。")
        return

    try:
        # 执行 docker compose build
        subprocess.run(["docker", "compose", "build"], cwd=project_dir, check=True)
        # 执行 docker compose up -d
        subprocess.run(["docker", "compose", "up", "-d"], cwd=project_dir, check=True)
        logger.success("Docker Compose 命令执行成功。")
    except subprocess.CalledProcessError as e:
        logger.error(f"执行 Docker Compose 命令时出错: {e}")
