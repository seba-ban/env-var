import os
from typing import Optional
from unittest import TestCase

from env_var import env
from env_var.errors import EnvVarNotDefinedError, EnvVarValidationError

from .helpers import VAR_NAME, check_validators, set_var


class TestNumeric(TestCase):
    def test_int(self):

        for valid in ("10", "1231", "412", "-121231", "0"):
            set_var(valid)
            self.assertEqual(env(VAR_NAME).as_int().required(), int(valid))

        invalid_values = ("10.", "10.5", "asd")

        for invalid in invalid_values:
            with self.assertRaises(EnvVarValidationError):
                set_var(invalid)
                env(VAR_NAME).as_int().required()

        for invalid in invalid_values:
            with self.assertRaises(EnvVarValidationError):
                set_var(invalid)
                env(VAR_NAME).as_int().optional()

    def test_int_base(self):
        set_var("100")
        for i in range(2, 37):
            self.assertEqual(env(VAR_NAME).as_int(base=i).required(), i**2)

    # TODO: implement
    def test_int_positive(self):
        pass

    def test_int_negative(self):
        pass

    def test_as_float(self):
        pass

    def test_as_float_positive(self):
        pass

    def test_as_float_negative(self):
        pass

    def test_as_port_number(self):
        pass
