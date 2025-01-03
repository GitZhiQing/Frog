from flask import Blueprint, render_template, current_app
from app import utils
import json

bp = Blueprint("main", __name__)


@bp.route("/archive")
def archive():
    """归档页"""
    dir_tree = utils.get_dir_tree(current_app.config["MD_ROOT"])
    # 去除 imgs 文件夹
    dir_tree.pop("imgs", None)
    # 去除第一级目录下的 nav page(即以 .md 结尾的文件)
    keys_to_remove = [key for key in dir_tree.keys() if key.endswith(".md")]
    for key in keys_to_remove:
        dir_tree.pop(key)
    dir_tree_json = json.dumps(dir_tree)
    return render_template(
        "archive.html",
        dir_tree_json=dir_tree_json,
        active_nav="归档",
    )


@bp.route("/articles/<string:title>")
def article(title):
    """阅读文章页"""
    doc_path = utils.get_doc_path(current_app.config["MD_ROOT"], title)
    html_content, meta = utils.parse_md(doc_path)
    return render_template("article.html", html_content=html_content, metadata=meta)


@bp.route("/tags/<tag>")
def tag(tag):
    """标签页"""
    return render_template("tag.html", tag=tag)


@bp.route("/categories/<category>")
def category(category):
    """分类页"""
    return render_template("category.html", category=category)
