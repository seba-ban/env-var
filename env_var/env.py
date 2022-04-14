from __future__ import annotations

import ipaddress
import os
import re
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Generic, List, Optional, Pattern, Type, TypeVar, Union
from urllib.parse import urlparse

from ._transformers.date import (
    datetime_transformer,
    iso_date_validator,
    iso_datetime_transformer,
    iso_duration_transformer,
)
from ._transformers.numeric import num_transformer_factory
from ._transformers.string_validators import (
    email_validator,
    hostname_validator,
    regex_validator_factory,
    uri_validator,
    url_validator,
    uuid_validator,
)
from .errors import EnvVarNotDefinedError, EnvVarValidationError


# as the whole distutils package is deprecated in python 3.10,
# just copying this function here with minor modifications
def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    if val in ("n", "no", "f", "false", "off", "0"):
        return False
    raise ValueError(f"invalid truth value {val}")


T = TypeVar("T")

EnumType = TypeVar("EnumType", bound=Enum)  # pylint: disable=invalid-name


@dataclass
class env:  # pylint: disable=invalid-name,too-many-public-methods
    """
    Utility to validate and type cast environment variables.
    All methods return an instance of the :class:`~env._env` class.
    """

    var_name: str

    def __ret_env(self, transformer: Callable[[str], T]) -> _env[T]:
        return _env[T](self.var_name, transformer)

    def as_int(
        self,
        base: Optional[int] = 10,
        min: Optional[int] = None,  # pylint: disable=redefined-builtin
        max: Optional[int] = None,  # pylint: disable=redefined-builtin
    ):
        """
        Parses env var as an int

        :param base: the base defaults to 10; valid bases are 0 and 2-36
        :param min: min acceptable value
        :param max: max acceptable value
        """
        return self.__ret_env(num_transformer_factory(int, min=min, max=max, base=base))

    def as_int_positive(self, base: Optional[int] = None):
        """
        Parses env var as a positive int (0 included)

        :param base: the base defaults to 10; valid bases are 0 and 2-36
        """
        return self.__ret_env(num_transformer_factory(int, min=0, base=base))

    def as_int_negative(self, base: Optional[int] = None):
        """
        Parses env var as a negative int

        :param base: the base defaults to 10; valid bases are 0 and 2-36
        """
        return self.__ret_env(num_transformer_factory(int, max=-1, base=base))

    def as_float(
        self,
        min: Optional[float] = None,  # pylint: disable=redefined-builtin
        max: Optional[float] = None,  # pylint: disable=redefined-builtin
    ):
        """
        Parses env var as a float

        :param min: min acceptable value
        :param max: max acceptable value
        """
        return self.__ret_env(num_transformer_factory(float, min=min, max=max))

    def as_float_positive(self):
        """
        Parses env var as a positive float (0 included)
        """
        return self.__ret_env(num_transformer_factory(float, min=0))

    def as_float_negative(self):
        """
        Parses env var as a negative float
        """
        return self.__ret_env(num_transformer_factory(float, max=-1))

    def as_port_number(self):
        """
        Parses env var as a port number (int between 1-65535)
        """
        return self.__ret_env(num_transformer_factory(int, min=1, max=65535))

    def as_bool(self):
        """
        Parses env var as a boolen
        """
        return self.__ret_env(strtobool)

    def as_urlparse(self):
        """
        Parses env var using :func:`urllib.parse.urlparse`
        """
        return self.__ret_env(urlparse)

    def as_ip_address(self):
        """
        Parses env var using :func:`ipaddress.ip_address`
        """
        return self.__ret_env(ipaddress.ip_address)

    def as_ip_network(self):
        """
        Parses env var using :func:`ipaddress.ip_network`
        """
        return self.__ret_env(ipaddress.ip_network)

    def as_ip_interface(self):
        """
        Parses env var using :func:`ipaddress.ip_interface`
        """
        return self.__ret_env(ipaddress.ip_interface)

    def as_enum(self, enum: Type[EnumType]) -> _env[EnumType]:
        """
        Parses env var as an Enum
        """
        return self.__ret_env(enum)

    def as_string(self):
        """
        Literally does nothing with the env var
        """
        return self.__ret_env(lambda s: s)

    def as_email(self):
        """
        Makes sure env var is a valid email string
        """
        return self.__ret_env(email_validator)

    def as_uri(self):
        """
        Makes sure env var is a valid uri string
        """
        return self.__ret_env(uri_validator)

    def as_uuid(self):
        """
        Makes sure env var is a valid uuid string
        """
        return self.__ret_env(uuid_validator)

    def as_url(self):
        """
        Makes sure env var is a valid url string
        """
        return self.__ret_env(url_validator)

    def as_hostname(self):
        """
        Makes sure env var is a valid hostname string
        """
        return self.__ret_env(hostname_validator)

    def should_match(self, pattern: Union[Pattern[str], str]):
        """
        Makes sure env var is matching given pattern
        """
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        return self.__ret_env(regex_validator_factory(pattern))

    def custom_transformer(self, transformer: Callable[[str], T]) -> _env[T]:
        """
        Parse/validate env var using custom transformer
        """
        return self.__ret_env(transformer)

    def as_iso_date(self):
        """
        Parses env var using :func:`dateutil.parser.isoparse`
        """
        return self.__ret_env(iso_datetime_transformer)

    def as_date(self):
        """
        Parses env var using :func:`dateutil.parser.parse`
        """
        return self.__ret_env(datetime_transformer)

    def as_iso_duration(self):
        """
        Parses env var using :func:`isoduration.parse_duration`
        """
        return self.__ret_env(iso_duration_transformer)

    def as_iso_date_string(self):
        """
        Makes sure env var is as a valid rfc3339 string
        """
        return self.__ret_env(iso_date_validator)

    def as_list(
        self, item_transformer: Callable[[str], T], split_on: str = ","
    ) -> _env[List[T]]:
        """
        Parses env var as a list

        :param item_transformer: function called with every value
                of the split string
        :param split_on: string on which env var should be split
        """
        return self.__ret_env(
            lambda s: [item_transformer(el) for el in s.split(split_on)]
        )

    def as_int_list(
        self,
        split_on: str = ",",
        base: Optional[int] = 10,
        min_item_value: Optional[int] = None,
        max_item_value: Optional[int] = None,
    ):
        """
        Parses env var as a list of ints

        :param split_on: string on which env var should be split
        :param base: the base defaults to 10; valid bases are 0 and 2-36
        :param min_item_value: min acceptable value for a single list item
        :param max_item_value: max acceptable value for a single list item
        """
        return self.as_list(
            num_transformer_factory(
                int, base=base, min=min_item_value, max=max_item_value
            ),
            split_on,
        )

    def as_float_list(
        self,
        split_on: str = ",",
        min_item_value: Optional[float] = None,
        max_item_value: Optional[float] = None,
    ):
        """
        Parses env var as a list of floats

        :param split_on: string on which env var should be split
        :param base: the base defaults to 10; valid bases are 0 and 2-36
        :param min_item_value: min acceptable value for a single list item
        :param max_item_value: max acceptable value for a single list item
        """
        return self.as_list(
            num_transformer_factory(float, min=min_item_value, max=max_item_value),
            split_on,
        )

    def as_string_list(
        self,
        split_on: str = ",",
    ):
        """
        Parses env var as a list of strings

        :param split_on: string on which env var should be split
        """
        return self.as_list(lambda s: s, split_on)


@dataclass
class _env(Generic[T]):
    """
    Helper generic class that is actually returned
    by all methods of the :class:`env` class. It's not
    supposed to be instantiated directly by the user
    of the library.
    """

    __var_name: str
    __transformer: Callable[[str], T]
    __default: Optional[T] = None

    def required(self) -> T:
        """
        :returns: the parsed environment variable

        :raises EnvVarNotDefinedError:
        :raises EnvVarValidationError:
        """
        val = self.__getenv()
        if val is None:
            raise EnvVarNotDefinedError(self.__var_name)
        return val

    def optional(self) -> Optional[T]:
        """
        :returns: the parsed environment variable, if it's set;
            if not, the default value if it was defined or None

        :raises EnvVarValidationError:
        """
        return self.__getenv()

    def default(self, val: T):
        """
        Sets the default value to return in case
        the environment variable is not defined.
        Note, this value will be returned as is,
        without any validation the value from the
        environment variable might go through.

        :param val: default value to use

        :returns: self
        """
        self.__default = val
        return self

    def __getenv(self) -> Optional[T]:
        val = os.getenv(self.__var_name)  # pylint: disable=invalid-envvar-value
        if val is None:
            return self.__default
        try:
            return self.__transformer(val)
        except ValueError as err:
            print(err)
            raise EnvVarValidationError(self.__var_name, *err.args) from None
