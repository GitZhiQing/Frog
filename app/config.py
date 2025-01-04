import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:
    DATA_ROOT = Path(__file__).parent.parent / "data"
    MD_ROOT = DATA_ROOT / "docs"
    DATABASE_ROOT = DATA_ROOT / "data.db"
    prefix = "sqlite:///" if sys.platform.startswith("win") else "sqlite:////"

    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f"{prefix}{DATABASE_ROOT}?check_same_thread=False"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ARTICLE_IMAGE_PATH = DATA_ROOT / "imgs"
    MD_ROOT = MD_ROOT
