import os
from typing import Optional
from unittest import TestCase

from env_var import env
from env_var.errors import EnvVarNotDefinedError, EnvVarValidationError

from .helpers import VAR_NAME, set_var


class TestRegex(TestCase):
    def test_email(self):

        valid_values = ("test@test.com", "banaszkiewicz.sebastian@gmail.com")
        invalid_values = (
            "not-a valid@email.com",
            "dsa1",
        )

        for valid in valid_values:
            set_var(valid)
            self.assertEqual(env(VAR_NAME).as_email().required(), valid)

        for invalid in invalid_values:
            with self.assertRaises(EnvVarValidationError):
                set_var(invalid)
                env(VAR_NAME).as_email().required()

    def test_hostname(self):
        valid_values = ("my-server", "monet.example.com")
        invalid_values = ("zażółćgęśląjaźń",)

        for valid in valid_values:
            set_var(valid)
            self.assertEqual(env(VAR_NAME).as_hostname().required(), valid)

        for invalid in invalid_values:
            with self.assertRaises(EnvVarValidationError):
                set_var(invalid)
                env(VAR_NAME).as_hostname().required()

    def test_own_regex(self):
        set_var("testing_is_very_important")

        for valid in (r"^testing.*$", f".*import"):
            self.assertIsNotNone(env(VAR_NAME).should_match(valid).required())

        for invalid in (
            "testing_is_not_important",
            r"testing\s+is.*",
        ):
            with self.assertRaises(EnvVarValidationError):
                env(VAR_NAME).should_match(invalid).required()
