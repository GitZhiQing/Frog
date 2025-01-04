import mistune
from mistune.plugins.abbr import abbr
from mistune.plugins.def_list import def_list
from mistune.plugins.footnotes import footnotes
from mistune.plugins.formatting import (
    insert,
    mark,
    strikethrough,
    subscript,
    superscript,
)
from mistune.plugins.math import math
from mistune.plugins.table import table
from mistune.plugins.task_lists import task_lists
from mistune.plugins.url import url


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
                return (
                    f'<blockquote class="{css_class}">'
                    f"<p>{text[len(key)+9:-5].strip()}</p>"
                    f"</blockquote>"
                )

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
