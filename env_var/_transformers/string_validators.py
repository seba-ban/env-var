import re
from typing import Pattern

import validators
from rfc3986_validator import validate_rfc3986
from validators import ValidationFailure

# kudos for the regex: https://github.com/ajv-validator/ajv-formats
hostname_regex = re.compile(
    r"^(?=.{1,253}\.?$)[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[-0-9a-z]{0,61}[0-9a-z])?)*\.?$",
    re.IGNORECASE,
)


def regex_validator_factory(pattern: Pattern[str]):
    def validator(s: str):
        if re.match(pattern, s):
            return s
        raise ValueError(f'"{s}" doesn\'t match pattern "{pattern}"')

    return validator


hostname_validator = regex_validator_factory(hostname_regex)


def uri_validator(s: str):
    if validate_rfc3986(s, rule="URI") is None:
        raise ValueError(f"{s} is not a valid URI")
    return s


def use_validators_package(validator_name: str):
    def validator(s: str):
        validation_result = getattr(validators, validator_name)(s)
        if isinstance(validation_result, ValidationFailure):
            raise ValueError(f"{s} is not a valid {validator_name}")
        return s

    return validator


url_validator = use_validators_package("url")
email_validator = use_validators_package("email")
uuid_validator = use_validators_package("uuid")
