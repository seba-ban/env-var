import os
from typing import Optional
from unittest import TestCase

from env_var import env
from env_var.errors import EnvVarNotDefinedError, EnvVarValidationError

from .helpers import VAR_NAME, set_var

# a = Env('date').as_date().required()
# print(a)
# class Dupa:
#     def __init__(self, name: str) -> None:
#         self.name = name


# a = Env('asdad').custom_transformer(lambda s: Dupa(s)).required()

# b = Env('dsa').as_int().required()

# c = Env('aaaa').


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
