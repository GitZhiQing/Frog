from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TextAreaField, validators


class CommentForm(FlaskForm):
    name = StringField(
        "昵称",
        validators=[
            validators.DataRequired(message="昵称不能为空"),
            validators.Length(max=20, message="昵称长度需 <20"),
        ],
    )
    email = StringField(
        "邮箱",
        validators=[
            validators.DataRequired(message="邮箱不能为空"),
            validators.Email(message="请输入有效的邮箱地址"),
            validators.Length(max=120, message="邮箱长度需 <120"),
        ],
    )
    link = StringField(
        "链接",
        validators=[
            validators.URL(message="请输入有效的网站链接"),
            validators.Length(max=120, message="网站链接长度需 <120"),
        ],
    )
    content = TextAreaField(
        "评论内容",
        validators=[
            validators.DataRequired(message="评论内容不能为空"),
            validators.Length(min=2, max=1000, message="评论内容长度需 2-1000"),
        ],
    )
    parent_id = HiddenField("回复对象")  # 用于记录回复的父评论ID
