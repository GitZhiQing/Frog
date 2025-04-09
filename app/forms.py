from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TextAreaField, validators


class CommentForm(FlaskForm):
    name = StringField("昵称", validators=[validators.DataRequired(), validators.Length(max=50)])
    email = StringField("邮箱", validators=[validators.DataRequired(), validators.Email(), validators.Length(max=120)])
    link = StringField("网站", validators=[validators.URL(), validators.Length(max=200)])
    content = TextAreaField("评论内容", validators=[validators.DataRequired(), validators.Length(min=2, max=1000)])
    parent_id = HiddenField("回复对象")  # 用于记录回复的父评论ID
