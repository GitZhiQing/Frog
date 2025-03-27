from datetime import UTC, datetime, timedelta
from pathlib import Path

import frontmatter
from loguru import logger


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
    """为目录树中的 Markdown 文件添加元数据"""
    tag_set = set()
    for item in dir_tree:
        # 仅处理 markdown 文件
        if item["type"] == "file" and item["name"].endswith(".md"):
            try:
                # 构建完整文件路径
                parent_dir = item["directory"]
                if parent_dir == "root":
                    file_path = root_dir / item["name"]
                else:
                    file_path = root_dir / parent_dir / item["name"]

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
                # 添加 tags 字段到目录树条目
                item["tags"] = tags
                tag_set.update(tags)
            except Exception as e:
                # 异常处理（可根据需要记录日志）
                logger.error(f"文档 [{item["name"]}] 元数据解析错误: {e}")
                item["tags"] = []

    return dir_tree, tag_set
