import os
from typing import Optional
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
        pass

    def test_string(self):
        pass

    def test_boolean(self):
        pass

    def test_custom_transformer(self):
        pass
