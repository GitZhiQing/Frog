from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re


class TodoExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(TodoPreprocessor(md), "todo", 175)


class TodoPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        for line in lines:
            new_line = re.sub(r"- \[( |x|X)\] (.*)", self.replace_checkbox, line)
            new_lines.append(new_line)
        return new_lines

    def replace_checkbox(self, match):
        checked = "checked" if match.group(1).strip().lower() == "x" else ""
        return f'<p class="todo-list"><input type="checkbox" disabled {checked}> {match.group(2)}</p>'


def makeExtension(**kwargs):
    return TodoExtension(**kwargs)
