import ipaddress
from enum import Enum
from typing import Tuple
from unittest import TestCase
from urllib.parse import ParseResult

from env_var import env

from .helpers import VAR_NAME, check_validators


class TestList(TestCase):
    def test_int_list(self):
        valid_values = (("1,2,3", [1, 2, 3]), ("-1,32,42", [-1, 32, 42]))
        invalid_values = ("a,d,s", "1 2 4 2")
        check_validators(
            self, env(VAR_NAME).as_int_list(), valid_values, invalid_values
        )

    def test_int_list_split(self):
        valid_values = (("1 2 3", [1, 2, 3]), ("-1 32 42", [-1, 32, 42]))
        invalid_values = ("a,d,s", "1,2,4,2")
        check_validators(
            self, env(VAR_NAME).as_int_list(split_on=" "), valid_values, invalid_values
        )

    def test_int_list_base(self):
        valid_values = (("10,f", [16, 15]),)
        invalid_values = ("a,d,s",)
        check_validators(
            self, env(VAR_NAME).as_int_list(base=16), valid_values, invalid_values
        )

    def test_int_list_min(self):
        valid_values = (("10,20", [10, 20]),)
        invalid_values = ("10,20,9",)
        check_validators(
            self,
            env(VAR_NAME).as_int_list(min_item_value=10),
            valid_values,
            invalid_values,
        )

    def test_int_list_max(self):
        valid_values = (("-100,10", [-100, 10]),)
        invalid_values = ("-100,10,11",)
        check_validators(
            self,
            env(VAR_NAME).as_int_list(max_item_value=10),
            valid_values,
            invalid_values,
        )

    def test_float_list(self):
        valid_values = (("10,2,4.23", [10.0, 2.0, 4.23]),)
        invalid_values = ("a,d,s", "1 2 4 2")
        check_validators(
            self, env(VAR_NAME).as_float_list(), valid_values, invalid_values
        )

    def test_str_list(self):
        valid_values = (("10,2,4.23", ["10", "2", "4.23"]), ("12d", ["12d"]))
        invalid_values = tuple()
        check_validators(
            self, env(VAR_NAME).as_string_list(), valid_values, invalid_values
        )

    def test_list(self):
        allowed = ["a", "b", "c"]

        def check_list(s: str):
            if s not in allowed:
                raise ValueError()
            return s

        valid_values = (
            ("a", ["a"]),
            ("a,b", ["a", "b"]),
            ("a,a,b,c,c", ["a", "a", "b", "c", "c"]),
        )
        invalid_values = ("a,b,c,d", "d,e", "aa,bb,cc")
        check_validators(
            self, env(VAR_NAME).as_list(check_list), valid_values, invalid_values
        )
