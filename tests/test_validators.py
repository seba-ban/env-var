import os
from typing import Optional
from unittest import TestCase

from env_var import env
from env_var.errors import EnvVarNotDefinedError, EnvVarValidationError

from .helpers import VAR_NAME, check_validators, set_var


class TestValidators(TestCase):
    def test_email(self):

        valid_values = ("test@test.com", "some.dude@example.com")
        invalid_values = (
            "not-a valid@email.com",
            "dsa1",
        )

        check_validators(self, env(VAR_NAME).as_email(), valid_values, invalid_values)

    def test_hostname(self):
        valid_values = (
            "my-server",
            "monet.example.com",
            "localhost",
            "127.0.0.1",
            "8.8.8.8",
        )
        invalid_values = ("zażółćgęśląjaźń", "-example.com", "exam_ple.com")

        check_validators(
            self, env(VAR_NAME).as_hostname(), valid_values, invalid_values
        )

    def test_as_iso_date_string(self):
        # TODO: add tests
        valid_values = ()
        invalid_values = ()

        check_validators(
            self, env(VAR_NAME).as_iso_date_string(), valid_values, invalid_values
        )

    def test_as_uri(self):
        # TODO: add tests
        valid_values = ()
        invalid_values = ()

        check_validators(self, env(VAR_NAME).as_uri(), valid_values, invalid_values)

    def test_as_url(self):
        # TODO: add tests
        valid_values = ()
        invalid_values = ()

        check_validators(self, env(VAR_NAME).as_url(), valid_values, invalid_values)

    def test_as_uuid(self):
        # TODO: add tests
        valid_values = ()
        invalid_values = ()

        check_validators(self, env(VAR_NAME).as_uuid(), valid_values, invalid_values)

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
