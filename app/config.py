import os
import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv


class Config:
    """默认配置 - 开发环境"""

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    FLASK_ENV: Literal["development", "production"] = "production"
    DEBUG: bool = False
    FLASK_DEBUG: bool = False

    DATA_DIR: Path = Path(__file__).parent.parent / "data"
    POST_DIR: Path = DATA_DIR / "posts"
    POST_IMGS_DIR: Path = DATA_DIR / "imgs"
    DATABASE_PATH: Path = DATA_DIR / "db" / "data.db"
    __prefix: str = "sqlite:///" if sys.platform.startswith("win") else "sqlite:////"
    SQLALCHEMY_DATABASE_URI: str = f"{__prefix}{DATABASE_PATH}?check_same_thread=False"


class ProductionConfig(Config):
    """生产配置"""

    FLASK_ENV: Literal["development", "production"] = "production"
    DEBUG: bool = False


load_dotenv()
flask_env = os.getenv("FLASK_ENV", "development")
if flask_env == "production":
    config = ProductionConfig
else:
    config = Config
