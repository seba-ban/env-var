import os
from typing import Optional
from unittest import TestCase

from env_var import env
from env_var.errors import EnvVarNotDefinedError, EnvVarValidationError

from .helpers import VAR_NAME, check_validators, set_var


class TestDates(TestCase):

    # TODO: implement
    def test_iso_date(self):
        pass

    def test_date(self):
        pass

    def test_iso_duration(self):
        pass
