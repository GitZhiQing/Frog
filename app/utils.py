"""app/utils.py"""

from pathlib import Path
import frontmatter
import mistune
from mistune.plugins.formatting import (
    strikethrough,
    mark,
    insert,
    superscript,
    subscript,
)
from mistune.plugins.footnotes import footnotes
from mistune.plugins.table import table
from mistune.plugins.url import url
from mistune.plugins.task_lists import task_lists
from mistune.plugins.def_list import def_list
from mistune.plugins.abbr import abbr
from mistune.plugins.math import math


class FrogRenderer(mistune.HTMLRenderer):
    """
    重写 block_quote 方法，支持渲染 GitHub 风格的提示框
    """

    def block_quote(self, text):
        types = {
            "[!NOTE]": "note",
            "[!TIP]": "tip",
            "[!IMPORTANT]": "important",
            "[!WARNING]": "warning",
            "[!CAUTION]": "caution",
        }

        for key, css_class in types.items():
            if text.startswith(f"<p>{key}"):
                return f'<blockquote class="{css_class}"><p>{text[len(key)+9:-5].strip()}</p></blockquote>'

        return f"<blockquote>{text}</blockquote>"

    def slugify(self, text):
        """
        将标题转换为 slug
        """
        return text.lower().strip().replace(" ", "-").replace(".", "").replace(",", "")

    def heading(self, text, level, raw=None):
        """
        重写 heading 方法，支持为标题添加 id 属性
        """
        slug = self.slugify(text)
        return f'<h{level} id="{slug}">{text}</h{level}>\n'

    def block_html(self, html):
        return html + "\n"


renderer = FrogRenderer()
markdown = mistune.create_markdown(
    escape=False,
    hard_wrap=True,
    renderer=renderer,
    plugins=[
        strikethrough,  # 删除线
        footnotes,  # 脚注
        table,  # 表格
        url,  # 将原始 URL 转换为链接
        task_lists,  # 任务列表
        def_list,  # html definition lists: dl, dt, dd
        abbr,  # 缩写 Ref: https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/abbr
        mark,  # 标记高亮
        insert,  # 插入 Ref: https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/ins
        superscript,  # 上标
        subscript,  # 下标
        math,  # 数学公式
    ],
)


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
        html_content = convert_md_to_html(md_content)
    print(metadata)
    return html_content, metadata


def convert_md_to_html(md_content: str) -> tuple:
    """将 markdown 内容转换为 HTML"""
    html_content = markdown(md_content)
    return html_content
