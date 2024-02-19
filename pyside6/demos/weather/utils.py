from datetime import datetime


def from_ts_to_time_of_day(ts):
    dt = datetime.fromtimestamp(ts)
    return dt.strftime("%I%p").lstrip("0")
