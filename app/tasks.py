from celery import shared_task
from flask import render_template
from flask_mailman import EmailMessage
from loguru import logger

from app.extensions import mail


@shared_task()
def send_comment_notification(comment: dict, request_path: str):
    try:
        body = render_template(
            "emails/comment_notification.txt", comment=comment, platform="FROG", request_path=request_path
        )
        msg = EmailMessage(subject=f"您的博客文章《{comment["post_title"]}》有新的评论", body=body, to=["qlear@qq.com"])
        with mail.get_connection() as conn:
            msg.connection = conn
            msg.send()
    except Exception as e:
        logger.exception(f"发送邮件失败: {e}")
