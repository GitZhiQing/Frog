from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class BlockquoteFilterTreeprocessor(Treeprocessor):
    def run(self, root):
        for blockquote in root.findall(".//blockquote"):
            for header in (
                blockquote.findall(".//h1")
                + blockquote.findall(".//h2")
                + blockquote.findall(".//h3")
                + blockquote.findall(".//h4")
                + blockquote.findall(".//h5")
                + blockquote.findall(".//h6")
            ):
                blockquote.remove(header)


class BlockquoteFilterExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(
            BlockquoteFilterTreeprocessor(md), "blockquote_filter", 25
        )


def makeExtension(**kwargs):
    return BlockquoteFilterExtension(**kwargs)
