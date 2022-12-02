from datetime import datetime, timezone

UTC = timezone.utc


class Datetime(datetime):
    def __new__(cls, moment=None):
        converted = to_datetime(moment)

        if not converted.tzinfo:
            converted = converted.replace(tzinfo=UTC)

        return datetime.__new__(
            cls,
            converted.year,
            converted.month,
            converted.day,
            converted.hour,
            converted.minute,
            converted.second,
            converted.microsecond,
            converted.tzinfo,
        )


def to_datetime(moment):
    match moment:
        case None:
            return datetime.now(tz=UTC)
        case datetime():
            return moment
        case str():
            return datetime.fromisoformat(handle_zulu(moment))


def handle_zulu(iso_datetime):
    """
    >>> handle_zulu("2022-12-01T09:17:45Z")
    '2022-12-01T09:17:45+00:00'

    >>> handle_zulu("2022-12-01 09:17:45z")
    '2022-12-01 09:17:45+00:00'
    """
    if iso_datetime.endswith(("z", "Z")):
        return iso_datetime[:-1] + "+00:00"
    else:
        return iso_datetime
