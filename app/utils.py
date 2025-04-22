from datetime import UTC, datetime, timedelta
from pathlib import Path

import frontmatter
from flask import current_app
from loguru import logger
from sqlalchemy import select

from app import models, utils
from app.extensions import db


def get_flat_dir_tree(root_dir: Path):
    """扫描目录并返回扁平化文件结构列表"""
    if not root_dir.is_dir():
        raise ValueError(f"路径不存在或不是目录: {root_dir}")

    flat_dir_tree = []
    dir_set = set()

    def _process_entry(entry_path: Path):
        """处理单个路径条目，生成扁平化记录"""
        # 计算父目录相对于根目录的路径
        try:
            parent_relative = entry_path.parent.relative_to(root_dir)
            directory = str(parent_relative) if parent_relative != Path(".") else "root"
        except ValueError:
            directory = "root"  # 处理根目录自身的情况
        dir_set.add(directory)
        flat_dir_tree.append(
            {"name": entry_path.name, "type": "directory" if entry_path.is_dir() else "file", "directory": directory}
        )

        # 如果是目录则递归处理
        if entry_path.is_dir():
            for child in sorted(entry_path.iterdir(), key=lambda x: x.name):
                try:
                    if child.exists():  # 跳过无效符号链接等
                        _process_entry(child)
                except PermissionError:
                    pass  # 跳过无权限访问的条目

    # 从根目录开始处理（包含自身）
    _process_entry(root_dir)

    # 修正根目录的 directory 字段为 "root"
    if flat_dir_tree:
        flat_dir_tree[0]["directory"] = "root"

    return flat_dir_tree, dir_set


def add_post_meta(dir_tree: list[dict[str, str]], root_dir: Path):
    """为目录树中的 Markdown 文件添加元数据，并新增相对路径属性"""
    tag_set = set()
    for item in dir_tree:
        if item["type"] == "file" and item["name"].endswith(".md"):
            try:
                parent_dir = item["directory"]
                # 构建绝对路径
                if parent_dir == "root":
                    file_path = root_dir / item["name"]
                else:
                    file_path = root_dir / parent_dir / item["name"]

                # 计算相对于 root_dir 的路径
                item["relative_path"] = file_path.relative_to(root_dir).as_posix()

                # 读取文件内容并解析 frontmatter
                with open(file_path, encoding="utf-8") as f:
                    post = frontmatter.load(f)

                # 提取 tags 并标准化为列表
                tags = post.metadata.get("tags", [])
                date: datetime = post.metadata.get("date")
                if date:
                    date_utc = date - timedelta(hours=8)
                    item["created_at"] = int(date_utc.replace(tzinfo=UTC).timestamp())

                if not isinstance(tags, list):
                    tags = [str(tags)] if tags else []
                item["tags"] = tags
                tag_set.update(tags)
            except Exception as e:
                logger.error(f"文档 [{item['name']}] 元数据解析错误: {e}")
                item["tags"] = []
    return dir_tree, tag_set


def blog_meta() -> dict:
    """注入一些博客元信息"""
    now = datetime.now()
    env_vars = {
        "BLOG_NAME": current_app.config.get("BLOG_NAME") or "Frog",
        "BLOG_INTRO": current_app.config.get("BLOG_INTRO") or "Gua Gua Gua",
        "BLOG_AVATAR": current_app.config.get("BLOG_AVATAR") or "./static/favicon.svg",
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


def db_init(drop_all: bool = False):
    """数据库初始化"""
    try:
        if drop_all:
            db.drop_all()
        else:
            # 需要排除的表名
            excluded_tables = {"comments", "uv_records"}
            # 待删除的表对象列表
            tables_to_drop = [table for table in db.metadata.tables.values() if table.name not in excluded_tables]
            from app.extensions import Base

            Base.metadata.drop_all(bind=db.engine, tables=tables_to_drop)

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
                    tag = db.session.execute(select(models.Tag).where(models.Tag.name == tag_name)).scalars().first()
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
