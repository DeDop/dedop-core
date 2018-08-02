import datetime as dt

ZERO = dt.timedelta(0)

class UTCZone(dt.tzinfo):
    """
    UTC timezone info class
    """
    def utcoffset(self, datetime) -> dt.timedelta:
        return ZERO

    def dst(self, datetime) -> dt.timedelta:
        return ZERO

    def tzname(self, datetime) -> str:
        return "UTC"

UTC = UTCZone()
UTC_BASE = dt.datetime(2000, 1, 1, tzinfo=UTC)

def iso_format(utc_secs: float=None) -> str:
    if utc_secs is None:
        time = dt.datetime.now(tz=UTC)
    else:
        time = UTC_BASE + dt.timedelta(seconds=utc_secs)
    return time.isoformat()