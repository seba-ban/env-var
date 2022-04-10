from datetime import datetime
from enum import Enum
from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from typing import Generic, List, Tuple, TypeVar, Union
from unittest import TestCase
from urllib.parse import ParseResult

from isoduration.types import Duration

from env_var import env

from .helpers import VAR_NAME

T = TypeVar("T")


class check_type(Generic[T]):
    """
    it won't raise any error, but it will
    show an error in the IDE if types are
    not correct...
    this is not ideal as values typed as Any
    won't show any error :(
    """

    @staticmethod
    def test(val: T):
        pass


class TestTypes(TestCase):
    def test_if_types_are_correct(self):
        try:
            e = env(VAR_NAME)

            check_type[int].test(e.as_int().required())
            check_type[int].test(e.as_int_positive().required())
            check_type[int].test(e.as_int_negative().required())

            check_type[float].test(e.as_float().required())
            check_type[float].test(e.as_float_positive().required())
            check_type[float].test(e.as_float_negative().required())

            check_type[int].test(e.as_port_number().required())

            check_type[bool].test(e.as_bool().required())

            check_type[ParseResult].test(e.as_urlparse().required())

            check_type[Union[IPv4Address, IPv6Address]].test(
                e.as_ip_address().required()
            )
            check_type[Union[IPv4Network, IPv6Network]].test(
                e.as_ip_network().required()
            )
            check_type[Union[IPv4Interface, IPv6Interface]].test(
                e.as_ip_interface().required()
            )

            class TestEnum(Enum):
                ERROR = "error"

            check_type[TestEnum].test(e.as_enum(TestEnum).required())

            check_type[str].test(e.as_string().required())
            check_type[str].test(e.as_email().required())
            check_type[str].test(e.as_uri().required())
            check_type[str].test(e.as_uuid().required())
            check_type[str].test(e.as_url().required())
            check_type[str].test(e.as_hostname().required())
            check_type[str].test(e.as_iso_date_string().required())
            check_type[str].test(e.should_match(r".+").required())

            def split_string(s: str) -> Tuple[str, str]:
                my_list = s.split(",")
                if len(my_list) != 2:
                    raise ValueError()
                return tuple(my_list)

            check_type[Tuple[str, str]].test(
                e.custom_transformer(split_string).required()
            )
            check_type[TestCase].test(
                e.custom_transformer(lambda s: TestCase()).required()
            )

            check_type[datetime].test(e.as_iso_date().required())
            check_type[datetime].test(e.as_date().required())
            check_type[Duration].test(e.as_iso_duration().required())

            check_type[List[int]].test(e.as_int_list().required())
            check_type[List[float]].test(e.as_float_list().required())
            check_type[List[str]].test(e.as_str_list().required())
            check_type[List[List[int]]].test(
                e.as_list(lambda s: [i for i in range(int(s))]).required()
            )

        except:
            pass
