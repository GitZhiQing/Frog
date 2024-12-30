import os
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DATA_ROOT = Path(__file__).parent.parent / "data"
MD_ROOT = DATA_ROOT / "docs"
DATABASE_ROOT = DATA_ROOT / "data.db"
prefix = "sqlite:///" if sys.platform.startswith("win") else "sqlite:////"

DATABASE_CONFIG = {
    "SQLALCHEMY_DATABASE_URI": f"{prefix}{DATABASE_ROOT}?check_same_thread=False",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
}

APP_CONFIG = {
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "DATA_ROOT": DATA_ROOT,
    "MD_ROOT": MD_ROOT,
}

CONFIG = {**DATABASE_CONFIG, **APP_CONFIG}
