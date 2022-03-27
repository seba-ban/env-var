from __future__ import annotations

import ipaddress
import os
import re
from dataclasses import dataclass
from distutils.util import strtobool
from enum import Enum
from multiprocessing.sharedctypes import Value
from typing import (
    Callable,
    ClassVar,
    Generic,
    Literal,
    Optional,
    Pattern,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)
from urllib.parse import urlparse

from ._transformers.date import (
    datetime_transformer,
    iso_date_string_transformer,
    iso_datetime_transformer,
    iso_duration_transformer,
)
from ._transformers.numeric import num__transformer_factory
from ._transformers.regexes import (
    email_regex,
    hostname_regex,
    regex_transformer_factory,
    uri_regex,
    url_regex,
    uuid_regex,
)
from ._transformers.varia import fqdn_transformer
from .errors import EnvVarNotDefinedError, EnvVarValidationError

T = TypeVar("T")
P = TypeVar("P")


@dataclass
class env:
    """
    Utility to validate and type cast environment variables.
    All methods return an instance of the :class:`~env._env` class.
    """

    var_name: str

    def __ret_env(self, transformer: Callable[[str], P]):
        return _env[P](self.var_name, transformer)

    # NUMERIC

    def as_int(
        self,
        base: Optional[int] = 10,
        min: Optional[int] = None,
        max: Optional[int] = None,
    ):
        """
        Cast env var to int

        :param base: the base defaults to 10; valid bases are 0 and 2-36
        :param min: min acceptable value
        :param max: max acceptable value
        """
        return self.__ret_env(num__transformer_factory(int, min=min, max=max, base=base))

    def as_int_positive(self, base: Optional[int] = None):
        """
        :param base: the base defaults to 10; valid bases are 0 and 2-36
        """
        return self.__ret_env(num__transformer_factory(int, min=0, base=base))

    def as_int_negative(self, base: Optional[int] = None):
        return self.__ret_env(num__transformer_factory(int, max=-1, base=base))

    def as_float(
        self,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ):
        return self.__ret_env(num__transformer_factory(float, min=min, max=max))

    def as_float_positive(self):
        return self.__ret_env(num__transformer_factory(float, min=0))

    def as_float_negative(self):
        return self.__ret_env(num__transformer_factory(float, max=-1))

    def as_port_number(self):
        return self.__ret_env(num__transformer_factory(int, positive=True, max=65535))

    def as_bool(self):
        return self.__ret_env(lambda s: bool(strtobool(s)))

    def as_urlparse(self):
        """
        :func:`urllib.parse.urlparse`
        """
        return self.__ret_env(lambda s: urlparse(s))

    def as_ip_address(self):
        """
        :func:`ipaddress.ip_address`
        """
        return self.__ret_env(lambda s: ipaddress.ip_address(s))

    def as_ip_network(self):
        """
        :func:`ipaddress.ip_network`
        """
        return self.__ret_env(lambda s: ipaddress.ip_network(s))

    def as_ip_interface(self):
        """
        :func:`ipaddress.ip_interface`
        """
        return self.__ret_env(lambda s: ipaddress.ip_interface(s))

    def as_enum(self, enum: Type[P]):
        """
        aaa
        """
        return self.__ret_env(lambda s: enum(s))

    def as_string(self):
        return self.__ret_env(lambda s: s)

    def as_email(self):
        """
        validates the env var is a valid email string
        """
        return self.__ret_env(regex_transformer_factory(email_regex))

    def as_uri(self):
        return self.__ret_env(regex_transformer_factory(uri_regex))

    def as_uuid(self):
        return self.__ret_env(regex_transformer_factory(uuid_regex))

    def as_url(self):
        return self.__ret_env(regex_transformer_factory(url_regex))

    def as_hostname(self):
        return self.__ret_env(regex_transformer_factory(hostname_regex))

    def should_match(self, pattern: Union[Pattern[str], str]):
        if not isinstance(pattern, str):
            pattern = re.compile(pattern)
        return self.__ret_env(regex_transformer_factory(pattern))

    def custom_transformer(self, transformer: Callable[[str], P]):
        return self.__ret_env(transformer)

    def as_iso_date(self):
        return self.__ret_env(iso_datetime_transformer)

    def as_date(self):
        return self.__ret_env(datetime_transformer)

    def as_iso_duration(self):
        return self.__ret_env(iso_duration_transformer)

    def as_iso_date_string(self):
        return self.__ret_env(iso_date_string_transformer)

    def as_fqdn(self):
        return self.__ret_env(fqdn_transformer)


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
        :returns: the parsed environment variable, if it's set; otherwise - None

        :raises EnvVarValidationError:
        """
        val = self.__getenv()
        return val

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
        val = os.getenv(self.__var_name)
        if val is None:
            return self.__default
        try:
            return self.__transformer(val)
        except ValueError as err:
            raise EnvVarValidationError(self.__var_name, *err.args) from None
