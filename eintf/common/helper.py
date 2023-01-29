import time
from datetime import datetime, timezone


def user_agent():
    return {"User-Agent": "https://github.com/ksh-b/eintf"}


def convert_time(orig_date, orig_format):
    # IDK why but timestamps are off by a day
    return int(datetime.strptime(orig_date, orig_format).timestamp()) + 86400


def now():
    return int(time.time())
