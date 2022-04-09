import ipaddress
from enum import Enum
from typing import Tuple
from unittest import TestCase
from urllib.parse import ParseResult

from env_var import env

from .helpers import VAR_NAME, check_validators


class TestVaria(TestCase):
    def test_urlparse(self):
        valid_values = (
            (
                "https://google.com",
                ParseResult(
                    scheme="https",
                    netloc="google.com",
                    path="",
                    params="",
                    query="",
                    fragment="",
                ),
            ),
            (
                "blablabla",
                ParseResult(
                    scheme="",
                    netloc="",
                    path="blablabla",
                    params="",
                    query="",
                    fragment="",
                ),
            ),
        )
        invalid_values = tuple()
        check_validators(
            self, env(VAR_NAME).as_urlparse(), valid_values, invalid_values
        )

    def test_ip_address(self):
        valid_values = (
            ("192.168.0.1", ipaddress.IPv4Address("192.168.0.1")),
            ("2001:db8::", ipaddress.IPv6Address("2001:db8::")),
        )
        invalid_values = ("lala", "192.168.0")
        check_validators(
            self, env(VAR_NAME).as_ip_address(), valid_values, invalid_values
        )

    def test_ip_network(self):
        valid_values = (
            ("192.168.0.0/28", ipaddress.IPv4Network("192.168.0.0/28")),
            ("2001:db00::0/24", ipaddress.IPv6Network("2001:db00::0/24")),
        )
        invalid_values = ("lala", "192.168.0.1/10021")
        check_validators(
            self, env(VAR_NAME).as_ip_network(), valid_values, invalid_values
        )

    def test_ip_interface(self):
        valid_values = (
            ("192.168.0.0/28", ipaddress.IPv4Interface("192.168.0.0/28")),
            ("2001:db00::0/24", ipaddress.IPv6Interface("2001:db00::0/24")),
        )
        invalid_values = ("lala", "192.168.0")
        check_validators(
            self, env(VAR_NAME).as_ip_interface(), valid_values, invalid_values
        )

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

        check_validators(
            self,
            env(VAR_NAME).custom_transformer(split_string),
            valid_values,
            invalid_values,
        )
