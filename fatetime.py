from datetime import datetime, timezone

UTC = timezone.utc


class Datetime(datetime):
    frozen = None

    def __new__(cls, moment=None):
        converted = cls.to_datetime(moment)

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

    def __enter__(self):
        self.__class__.frozen = self
        return self

    def __exit__(self, *exc_details):
        self.__class__.frozen = None

    @classmethod
    def freeze(cls, moment):
        def outer(func):
            def inner(*args, **kwargs):
                with cls(moment):
                    return func(*args, **kwargs)

            return inner

        return outer

    @classmethod
    def to_datetime(cls, moment):
        match moment:
            case None:
                return cls._now()
            case datetime():
                return moment
            case str():
                return datetime.fromisoformat(cls._handle_zulu(moment))

    @classmethod
    def _now(cls):
        return cls.frozen or datetime.now(tz=UTC)

    @staticmethod
    def _handle_zulu(iso_datetime):
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

    def is_same_as(self, other):
        """
        This is a potential precursor to changing the behaviour of __eq__ et al.
        The jury is still out on this one...
        """
        return self == self.__class__(other)
