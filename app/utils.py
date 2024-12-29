"""app/utils.py"""

from pathlib import Path
import markdown
import frontmatter
import re
from app.md_extensions import TodoExtension
from app.md_extensions import BlockquoteFilterExtension


def get_dir_tree(path: str) -> dict:
    """递归获取指定目录的目录树"""
    root = Path(path)
    if not root.is_dir():
        return
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


def get_md_word_count(md_content: str) -> int:
    """获取 markdown 内容的字数"""
    word_count = len(md_content.split())
    return word_count


def parse_md(md_path: str) -> tuple:
    """解析 markdown 文件"""
    with open(md_path, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)
        md_content = post.content
        metadata = post.metadata
        word_count = get_md_word_count(md_content)
        metadata["word_count"] = word_count
        html_content, toc = convert_md_to_html(md_content)
    print(metadata)
    return html_content, metadata, toc


def convert_md_to_html(md_content: str) -> tuple:
    def slugify(value, separator):
        """自定义 slugify 函数，保留中文字符"""
        value = str(value)
        value = re.sub(r"[^\w\u4e00-\u9fff]+", separator, value)
        value = re.sub(r"[-\s]+", separator, value)
        return value.strip(separator).lower()

    """将 markdown 内容转换为 HTML"""
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.admonition",
            "markdown.extensions.codehilite",
            "markdown.extensions.toc",
            "markdown.extensions.wikilinks",
            "markdown.extensions.sane_lists",
            TodoExtension(),  # 自定义 TODO 列表扩展
            BlockquoteFilterExtension(),  # 自定义 blockquote 过滤扩展
        ],
        extension_configs={
            "markdown.extensions.toc": {
                "title": "目录",
                "title_class": "article-toc-title",
                "toc_class": "article-toc",
                "toc_depth": 3,
                "slugify": slugify,
            },
        },
    )
    html_content = md.convert(md_content)
    toc = md.toc
    return html_content, toc
