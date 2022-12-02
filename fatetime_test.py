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
