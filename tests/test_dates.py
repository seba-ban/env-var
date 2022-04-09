from datetime import datetime, timezone
from unittest import TestCase

from isoduration.types import DateDuration, Decimal, Duration, TimeDuration

from env_var import env

from .helpers import VAR_NAME, check_validators


class TestDates(TestCase):
    def test_iso_date(self):
        valid_values = (
            (
                "2022-04-09T01:30:03.602Z",
                datetime(2022, 4, 9, 1, 30, 3, 602000, tzinfo=timezone.utc),
            ),
        )
        invalid_values = ("26f47ed0-b7a4-11ec-b909-0242ac12000",)

        check_validators(
            self, env(VAR_NAME).as_iso_date(), valid_values, invalid_values
        )

    def test_date(self):
        valid_values = (
            (
                "2022-04-09T01:30:03.602Z",
                datetime(2022, 4, 9, 1, 30, 3, 602000, tzinfo=timezone.utc),
            ),
            ("09/04/2022, 03:30:37", datetime(2022, 9, 4, 3, 30, 37)),
        )
        invalid_values = ("26f47ed0-b7a4-11ec-b909-0242ac12000",)

        check_validators(self, env(VAR_NAME).as_date(), valid_values, invalid_values)

    def test_iso_duration(self):
        valid_values = (
            (
                "P3Y6M4DT12H30M5S",
                Duration(
                    DateDuration(
                        years=Decimal("3"),
                        months=Decimal("6"),
                        days=Decimal("4"),
                        weeks=Decimal("0"),
                    ),
                    TimeDuration(
                        hours=Decimal("12"), minutes=Decimal("30"), seconds=Decimal("5")
                    ),
                ),
            ),
        )
        invalid_values = ("26f47ed0-b7a4-11ec-b909-0242ac12000",)

        check_validators(
            self, env(VAR_NAME).as_iso_duration(), valid_values, invalid_values
        )
