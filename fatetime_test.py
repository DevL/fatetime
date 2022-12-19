import pytest
from datetime import datetime, timedelta, timezone
from freezegun import freeze_time
from fatetime import Datetime

UTC = timezone.utc
NAIVE_DATETIME = datetime(2022, 11, 26, 13, 8, 50)
AWARE_DATETIME = datetime(2022, 11, 26, 13, 8, 50, tzinfo=UTC)
DATETIME_WITH_TZINFO = datetime(2022, 11, 26, 13, 8, 50, tzinfo=timezone(timedelta(seconds=3600)))


@freeze_time("2022-11-26 13:08:50")
def test_defaults_to_current_moment():
    assert Datetime() == AWARE_DATETIME


CREATION_TEST_CASES = {
    "a naive datetime": (NAIVE_DATETIME, AWARE_DATETIME),
    "a datetime with UTC timezone": (AWARE_DATETIME, AWARE_DATETIME),
    "a datetime with non-UTC timezone": (DATETIME_WITH_TZINFO, DATETIME_WITH_TZINFO),
    "an ISO date": ("2022-12-01", datetime(2022, 12, 1, 0, 0, 0, tzinfo=UTC)),
    "an ISO datetime": ("2022-11-26 13:08:50", AWARE_DATETIME),
    "an ISO datetime with offset": ("2022-11-26 13:08:50+01:00", DATETIME_WITH_TZINFO),
    "an ISO datetime with lowercase zulu": ("2022-11-26T13:08:50z", AWARE_DATETIME),
    "an ISO datetime with uppercase zulu": ("2022-11-26T13:08:50Z", AWARE_DATETIME),
}


@pytest.mark.parametrize(
    "moment, expected",
    CREATION_TEST_CASES.values(),
    ids=CREATION_TEST_CASES.keys(),
)
def test_creating_a_datetime(moment, expected):
    assert Datetime(moment) == expected


def test_repr():
    expected = "Datetime(2022, 11, 26, 13, 8, 50, tzinfo=datetime.timezone.utc)"
    assert repr(Datetime(AWARE_DATETIME)) == expected
    assert repr(Datetime(NAIVE_DATETIME)) == expected


def test_str():
    expected = "2022-11-26 13:08:50+00:00"
    assert str(Datetime(AWARE_DATETIME)) == expected
    assert str(Datetime(NAIVE_DATETIME)) == expected


def test_as_a_time_freezing_context():
    with Datetime(NAIVE_DATETIME):
        assert Datetime() == Datetime(NAIVE_DATETIME)
    assert Datetime() > Datetime(NAIVE_DATETIME)


def test_as_time_freezing_decorator():
    @Datetime.freeze("2022-12-03 12:36:45")
    def with_frozen_time():
        return Datetime()

    assert with_frozen_time() == Datetime("2022-12-03 12:36:45")


def test_is_same_as():
    assert Datetime(NAIVE_DATETIME).is_same_as("2022-11-26 13:08:50")


def test_comparing():
    assert Datetime(NAIVE_DATETIME) < Datetime()
    assert Datetime(AWARE_DATETIME) < Datetime()
    assert Datetime(DATETIME_WITH_TZINFO) < Datetime(AWARE_DATETIME)
    assert Datetime(NAIVE_DATETIME) < datetime.now(tz=UTC)
    assert Datetime(AWARE_DATETIME) < datetime.now(tz=UTC)
    assert Datetime(DATETIME_WITH_TZINFO) < AWARE_DATETIME
