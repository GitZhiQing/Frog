from datetime import UTC, datetime, timedelta


def ts2date(timestamp: int) -> str:
    """将时间戳转换为日期"""
    dt_shanghai = datetime.fromtimestamp(timestamp, tz=UTC) + timedelta(hours=8)
    dt_shanghai_str = dt_shanghai.strftime("%Y-%m-%d %H:%M:%S")
    return dt_shanghai_str
