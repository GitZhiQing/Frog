from flask import Blueprint, render_template, current_app
from app import utils
import json


bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """首页，返回文章列表"""
    return render_template("index.html")


@bp.route("/articles/<title>")
def article(title):
    """阅读文章页"""
    doc_path = utils.get_doc_path(current_app.config["MD_ROOT"], title)
    html_content, meta = utils.parse_md(doc_path)
    return render_template("article.html", html_content=html_content, metadata=meta)


@bp.route("/archive")
def archive():
    """归档页"""
    dir_tree = utils.get_dir_tree(current_app.config["MD_ROOT"])
    dir_tree_json = json.dumps(dir_tree)
    return render_template("archive.html", dir_tree_json=dir_tree_json)


@bp.route("/about")
def about():
    """关于页"""
    return render_template("about.html")


@bp.route("/tags/<tag>")
def tag(tag):
    """标签页"""
    return render_template("tags.html", tag=tag)


@bp.route("/categories/<category>")
def category(category):
    """分类页"""
    return render_template("categories.html", category=category)
