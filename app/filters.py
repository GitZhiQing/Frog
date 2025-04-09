from datetime import UTC, datetime, timedelta

from flask import Flask


def ts2date(timestamp: int) -> str:
    """将时间戳转换为日期"""
    dt_shanghai = datetime.fromtimestamp(timestamp, tz=UTC) + timedelta(hours=8)
    dt_shanghai_str = dt_shanghai.strftime("%Y-%m-%d %H:%M:%S")
    return dt_shanghai_str


def register_filters(app: Flask):
    """注册过滤器"""
    app.add_template_filter(ts2date, "ts2date")
