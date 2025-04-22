import os
import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    默认配置
    默认为开发环境
    """

    # Flask 应用
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    FLASK_ENV: Literal["development", "production"] = "production"
    DEBUG: bool = False
    FLASK_DEBUG: bool = False
    # for url_for
    SERVER_NAME: str = os.getenv("SERVER_NAME", "127.0.0.1:5000")
    APPLICATION_ROOT: str = os.getenv("APPLICATION_ROOT", "/")
    PREFERRED_URL_SCHEME: str = "http"

    # 数据
    PROJECT_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_DIR / "data"
    POST_DIR: Path = DATA_DIR / "posts"
    POST_IMGS_DIR: Path = DATA_DIR / "imgs"
    DATABASE_PATH: Path = DATA_DIR / "db" / "data.db"
    __prefix: str = "sqlite:///" if sys.platform.startswith("win") else "sqlite:////"
    SQLALCHEMY_DATABASE_URI: str = f"{__prefix}{DATABASE_PATH}?check_same_thread=False"
    SQLALCHEMY_ECHO = False

    # 博客
    BLOG_NAME: str = os.getenv("BLOG_NAME")
    BLOG_INTRO: str = os.getenv("BLOG_INTRO")
    BLOG_AVATAR: str = os.getenv("BLOG_AVATAR")

    # Celery 配置
    REDIS_HOST: str = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")
    CELERY = {
        "broker_url": f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0",
        "result_backend": f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0",
        "task_serializer": "json",
        "result_serializer": "json",
        "accept_content": ["json"],
        "timezone": "UTC",
        "task_ignore_result": True,
    }

    # Flask Mailman 配置
    MAIL_SENDER_NAME: str = os.getenv("MAIL_SENDER_NAME")
    MAIL_SENDER_ADDRESS: str = os.getenv("MAIL_SENDER_ADDRESS")
    MAIL_DEFAULT_SENDER: str = f"{MAIL_SENDER_NAME} <{MAIL_SENDER_ADDRESS}>"  # 配置默认发件人，包含发件人名称和地址
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")  # SMTP 服务器主机
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", 465))  # SMTP 服务器端口
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")  # SMTP 服务器用户名
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")  # SMTP 服务器密码
    MAIL_USE_SSL: bool = os.getenv("MAIL_USE_SSL", "True").lower() == "true"  # 使用 SSL 加密连接


class ProductionConfig(Config):
    """生产配置"""

    FLASK_ENV: Literal["development", "production"] = "production"
    DEBUG: bool = False
    TESTING: bool = False
    # for url_for
    SERVER_NAME: str = os.getenv("SERVER_NAME")
    APPLICATION_ROOT: str = os.getenv("APPLICATION_ROOT", "/")
    PREFERRED_URL_SCHEME: str = "https"


app_env = os.getenv("FLASK_ENV", "development")
app_config = ProductionConfig if app_env == "production" else Config
