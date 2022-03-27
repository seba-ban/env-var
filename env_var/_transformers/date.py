from dateutil import parser
from isoduration import parse_duration
from rfc3339_validator import validate_rfc3339


def iso_date_string_transformer(s: str):
    if not validate_rfc3339("2001-10-23T15:32:12.9023368Z"):
        raise ValueError(f"{s} is not a valid rfc3339 date string")
    return s


def iso_datetime_transformer(s: str):
    return parser.isoparse(s)


def datetime_transformer(s: str):
    return parser.parse(s)


def iso_duration_transformer(s: str):
    return parse_duration(s)
