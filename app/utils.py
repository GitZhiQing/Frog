"""app/utils.py"""

from flask import render_template
from pathlib import Path
import frontmatter


def get_dir_tree(path: str) -> dict:
    """递归获取指定目录的目录树"""
    root = Path(path)
    if not root.is_dir():
        return {}
    tree = {}
    for item in root.iterdir():
        if item.is_dir():
            tree[item.name] = get_dir_tree(item)
        else:
            tree[item.name] = None
    return tree


def get_doc_path(root: Path, doc_name: str) -> str:
    """根据根目录获取指定文件的路径
    只返回第一个匹配的文件路径
    """
    tree = get_dir_tree(root)
    md_name = f"{doc_name}.md"

    def find_path(tree, current_path):
        for name, subtree in tree.items():
            if name == md_name:
                return current_path / name
            if subtree is not None:
                result = find_path(subtree, current_path / name)
                if result:
                    return result
        return None

    return find_path(tree, root)


def get_md_files(root: Path) -> list:
    """获取根目录下一级的 Markdown 文件的路径"""
    return [path for path in root.glob("*.md")]


def get_md_word_count(md_content: str) -> int:
    """获取 markdown 内容的字数"""
    return len(md_content.split())


def parse_md(md_path: str) -> tuple:
    """解析 markdown 文件"""
    with open(md_path, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)
        md_content = post.content
        metadata = post.metadata
        metadata["word_count"] = get_md_word_count(md_content)
        html_content = convert_md_to_html(md_content)
    return html_content, metadata


def convert_md_to_html(md_content: str) -> str:
    """将 markdown 内容转换为 HTML"""
    from app.markdown import markdown

    return markdown(md_content)


def get_nav_data(md_root: Path) -> list:
    """获取导航栏数据"""
    nav_data = []
    # 动态导航页面
    for md_file in get_md_files(md_root):
        _, metadata = parse_md(md_file)
        nav_data.append(
            {
                "name": metadata.get("nav_name", ""),
                "route": f"/{metadata.get('nav_route', '')}",
                "order": metadata.get("nav_order", 0),
                "type": "dynamic",
            }
        )

    # 默认导航页面
    nav_data.extend(
        [
            {
                "name": "归档",
                "route": "/archive",
                "order": 1000,
                "type": "static",
            },
        ]
    )

    return sorted(nav_data, key=lambda x: x["order"])


def nav_view_func(md_file: Path) -> str:
    """导航栏视图函数"""
    html_content, metadata = parse_md(md_file)
    active_nav_route = metadata.get("nav_route", "")
    return render_template(
        "nav_page.html",
        nav_data=get_nav_data(md_file.parent),
        html_content=html_content,
        active_nav_route=active_nav_route,
        metadata=metadata,
    )
