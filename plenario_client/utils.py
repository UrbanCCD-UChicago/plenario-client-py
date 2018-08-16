from datetime import datetime, date


def parse_datetime(timestamp) -> datetime:
    if timestamp:
        return datetime.strptime(timestamp[:19], "%Y-%m-%dT%H:%M:%S")  # millisecond are sliced off
    return None


def parse_date(timestamp) -> date:
    if timestamp:
        return datetime.strptime(timestamp, "%Y-%m-%d").date()
    return None