from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class UVRecord(db.Model):
    __tablename__ = "uv_records"
    uv_id: Mapped[str] = mapped_column(String(32), primary_key=True)
