import ipaddress
import os
from enum import Enum
from typing import Optional, Tuple
from unittest import TestCase

from env_var import env
from env_var.errors import EnvVarNotDefinedError, EnvVarValidationError

from .helpers import VAR_NAME, check_validators, set_var


class TestVaria(TestCase):

    # TODO: implement

    def test_urlparse(self):
        pass

    def test_ip_address(self):
        pass

    def test_ip_network(self):
        pass

    def test_ip_interface(self):
        pass

    def test_enum(self):
        class TestEnum(Enum):
            ERROR = "error"
            DEBUG = "debug"
            INFO = "info"

        valid_values = (
            ("error", TestEnum.ERROR),
            ("debug", TestEnum.DEBUG),
            ("info", TestEnum.INFO),
        )
        invalid_values = ("", "dsa1", "a,b,c", "ERROR", "DEBUG", "INFO")

        # check_type = env(VAR_NAME).as_enum(TestEnum).required()
        check_validators(
            self,
            env(VAR_NAME).as_enum(TestEnum),
            valid_values,
            invalid_values,
        )

    def test_string(self):
        valid_values = ("any string", "literally everything")
        invalid_values = ()

        check_validators(self, env(VAR_NAME).as_string(), valid_values, invalid_values)

    def test_boolean(self):
        valid_values = (
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("TrUe", True),
            ("false", False),
            ("False", False),
            ("FALSE", False),
            ("FaLsE", False),
        )
        invalid_values = (
            "",
            "dsa1",
        )

        check_validators(self, env(VAR_NAME).as_bool(), valid_values, invalid_values)

    def test_custom_transformer(self):
        def split_string(s: str) -> Tuple[str, str]:
            my_list = s.split(",")
            if len(my_list) != 2:
                raise ValueError()
            return tuple(my_list)

        valid_values = (("a,b", ("a", "b")), ("c,d", ("c", "d")))
        invalid_values = ("", "dsa1", "a,b,c")

        # check_type = env(VAR_NAME).custom_transformer(split_string).required()
        check_validators(
            self,
            env(VAR_NAME).custom_transformer(split_string),
            valid_values,
            invalid_values,
        )
