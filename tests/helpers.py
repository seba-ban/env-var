import os
from typing import Any, Optional, Sequence
from unittest import TestCase

from env_var.env import _env
from env_var.errors import EnvVarNotDefinedError, EnvVarValidationError

VAR_NAME = "TEST_VAR"


def set_var(val: Optional[str] = None):
    if val is None:
        if VAR_NAME in os.environ:
            del os.environ[VAR_NAME]
        return
    os.environ[VAR_NAME] = val


def check_validators(
    test_case: TestCase,
    _env_instance: _env,
    valid_values: Sequence[Any],
    invalid_values: Sequence[Any],
):
    for valid in valid_values:
        if isinstance(valid, tuple):
            var_value, parsed = valid
        else:
            var_value = parsed = valid
        set_var(var_value)
        test_case.assertEqual(_env_instance.required(), parsed)

    for invalid in invalid_values:
        with test_case.assertRaises(EnvVarValidationError):
            set_var(invalid)
            _env_instance.required()

        with test_case.assertRaises(EnvVarValidationError):
            set_var(invalid)
            _env_instance.optional()

    set_var()
    for valid in valid_values:
        with test_case.assertRaises(EnvVarNotDefinedError):
            _env_instance.required()

    for invalid in invalid_values:
        test_case.assertIsNone(_env_instance.optional())

    for valid in valid_values:
        if isinstance(valid, tuple):
            _, parsed = valid
        else:
            parsed = valid
        test_case.assertEqual(_env_instance.default(parsed).required(), parsed)
